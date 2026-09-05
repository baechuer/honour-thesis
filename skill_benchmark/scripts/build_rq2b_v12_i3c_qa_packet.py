#!/usr/bin/env python3
"""Build the approved, incomplete blinded QA packet for RQ2b v1.2 I3C.

This is deliberately a local packaging step. It samples source/extraction pairs
after automatic extraction gates have passed, but does not review a row, compute
any scientific result, or access a network.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
MERGED_ROOT = f"{RELATIVE_ROOT}/i3c_merged"
EXTRACTION_ROOT = f"{RELATIVE_ROOT}/i3c_extraction"
PACKET = f"{RELATIVE_ROOT}/i3c_source_assignment_approval_packet.json"
RECEIPT = f"{RELATIVE_ROOT}/i3c_source_assignment_approval_receipt.json"
OUTPUT_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa"
CHECKPOINT = f"{RELATIVE_ROOT}/i3c_extraction_completion_checkpoint.json"
QA_CHECKPOINT = f"{RELATIVE_ROOT}/i3c_manual_qa_packet_checkpoint.json"
APPROVED_PACKET_SHA256 = "472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe"
QA_SAMPLE_SIZE = 120
QA_SAMPLE_SEED = 2026081601
FIELD_KEYS = (
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "success_criteria",
    "constraints_boundaries",
    "dependencies_resources",
)
REVIEWER_ALLOWED_KEYS = {"review_id", "source_text", "extracted_fields", "retained_selector_spans", "omitted_selector_spans", "field_warnings", "qa_warnings"}
FORBIDDEN_REVIEWER_KEY_TOKENS = ("prompt", "gold", "alternative", "role", "stratum", "group", "retrieval", "skill_id", "source_path", "source_row_index", "source_sha256")


def require_authorised_local_only(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    packet = read_json(root / PACKET)
    receipt = read_json(root / RECEIPT)
    merged = read_json(root / MERGED_ROOT / "manifest.json")
    require(sha256_file(root / PACKET) == APPROVED_PACKET_SHA256, "v1.2 source-assignment packet hash mismatch")
    require(packet["version_id"] == receipt["approved_packet"]["path"].split("/")[-2] == VERSION_ID, "v1.2 approval identity mismatch")
    require(receipt["state"] == "explicitly_approved_for_v12_i3c_source_assignment_once", "v1.2 receipt is not approved")
    require("build but not complete a fresh blinded manual-QA packet after automatic gates pass" in packet["authorises_if_approved"], "v1.2 packet does not allow QA packet construction")
    require(merged["state"] == "automatic_gates_passed_manual_qa_pending", "automatic I3C gates are not ready for QA packet construction")
    require(merged["network_calls"] == merged["external_api_calls"] == 0, "merged I3C state crossed the local-only boundary")
    require(merged["manual_qa"]["completion_authorized"] is False, "manual QA must remain unapproved")
    require(merged["retrieval_authorized"] is False, "retrieval must remain unapproved")
    return packet, receipt, merged


def quantile_bucket(rank: int, total: int) -> str:
    fraction = rank / max(1, total)
    if fraction < 0.25:
        return "short"
    if fraction < 0.75:
        return "median"
    if fraction < 0.95:
        return "p75_to_p95"
    if fraction < 0.99:
        return "p95_to_p99"
    return "longest"


def source_cohort(source: dict[str, Any]) -> str:
    if source.get("is_main_evaluated") is True:
        return "main_evaluated"
    if "/source_overlay/background_scale/" in source["source_path"]:
        return "background_scale"
    return "other_non_main"


def build_metadata(sources: list[dict[str, Any]], canonical: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    require(len(sources) == len(canonical) == 2433, "v1.2 QA source/extraction rows must equal 2433")
    ordered_length = sorted(
        range(len(sources)),
        key=lambda index: (sources[index]["source_utf8_bytes"], sources[index]["skill_id"]),
    )
    length_bucket = {
        source_index: quantile_bucket(rank, len(ordered_length))
        for rank, source_index in enumerate(ordered_length)
    }
    item_counts = [len(row["retained_selector_spans"]) for row in canonical]
    ordered_density = sorted(range(len(canonical)), key=lambda index: (item_counts[index], canonical[index]["skill_id"]))
    density_bucket = {
        source_index: ("sparse" if rank < len(ordered_density) // 3 else "dense" if rank >= 2 * len(ordered_density) // 3 else "medium")
        for rank, source_index in enumerate(ordered_density)
    }
    metadata: dict[int, dict[str, Any]] = {}
    for index, (source, extraction) in enumerate(zip(sources, canonical, strict=True)):
        require(source["source_row_index"] == extraction["source_row_index"] == index, f"QA source-row identity mismatch: {index}")
        require(source["skill_id"] == extraction["skill_id"], f"QA skill identity mismatch: {index}")
        require(source["source_sha256"] == extraction["source_sha256"], f"QA source hash mismatch: {index}")
        metadata[index] = {
            "cohort": source_cohort(source),
            "source_policy": source["source_policy"],
            "family": source["family"],
            "length_bucket": length_bucket[index],
            "density_bucket": density_bucket[index],
            "present_fields": sorted(field for field in FIELD_KEYS if extraction["fields"][field]),
            "warning_codes": sorted({str(item.get("code") or "warning") for item in extraction["qa_warnings"] if isinstance(item, dict)}),
        }
    return metadata


def features(values: dict[str, Any]) -> set[tuple[str, str]]:
    return {
        ("cohort", values["cohort"]),
        ("source_policy", values["source_policy"]),
        ("family", values["family"]),
        ("length_bucket", values["length_bucket"]),
        ("density_bucket", values["density_bucket"]),
        *(("field", value) for value in values["present_fields"]),
        *(("warning", value) for value in values["warning_codes"]),
    }


def select_rows(metadata: dict[int, dict[str, Any]]) -> list[int]:
    require(len(metadata) >= QA_SAMPLE_SIZE, "QA population is too small")
    uncovered = set().union(*(features(values) for values in metadata.values()))
    generator = random.Random(QA_SAMPLE_SEED)
    candidates = list(metadata)
    generator.shuffle(candidates)
    selected: list[int] = []
    selected_set: set[int] = set()
    while uncovered and len(selected) < QA_SAMPLE_SIZE:
        best = max(
            (index for index in candidates if index not in selected_set),
            key=lambda index: (len(features(metadata[index]) & uncovered), -index),
        )
        selected.append(best)
        selected_set.add(best)
        uncovered.difference_update(features(metadata[best]))
    require(not uncovered, f"120-row QA packet cannot cover required source features: {sorted(uncovered)}")

    strata: dict[tuple[str, str, str, str], list[int]] = defaultdict(list)
    for index, values in metadata.items():
        strata[(values["cohort"], values["source_policy"], values["length_bucket"], values["density_bucket"])].append(index)
    for values in strata.values():
        generator.shuffle(values)
    stratum_keys = sorted(strata)
    cursor = 0
    while len(selected) < QA_SAMPLE_SIZE:
        key = stratum_keys[cursor % len(stratum_keys)]
        cursor += 1
        while strata[key] and strata[key][-1] in selected_set:
            strata[key].pop()
        if not strata[key]:
            require(any(values for values in strata.values()), "QA sampling exhausted before reaching 120 rows")
            continue
        selected.append(strata[key].pop())
        selected_set.add(selected[-1])
    require(len(selected) == QA_SAMPLE_SIZE and len(selected_set) == QA_SAMPLE_SIZE, "QA selection count/uniqueness failure")
    return selected


def reviewer_field_view(fields: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    return {
        field: [
            {key: item[key] for key in ("id", "text", "evidence", "evidence_status")}
            for item in fields[field]
        ]
        for field in FIELD_KEYS
    }


def validate_blinded_packet(rows: list[dict[str, Any]]) -> None:
    require(len(rows) == QA_SAMPLE_SIZE, "reviewer packet row count mismatch")
    require(len({row["review_id"] for row in rows}) == QA_SAMPLE_SIZE, "reviewer IDs are not unique")
    for row in rows:
        require(set(row) == REVIEWER_ALLOWED_KEYS, f"reviewer packet has an unexpected field: {set(row) - REVIEWER_ALLOWED_KEYS}")
        require(not any(token in key.lower() for key in row for token in FORBIDDEN_REVIEWER_KEY_TOKENS), f"reviewer packet leakage key: {row['review_id']}")
        require(isinstance(row["source_text"], str) and row["source_text"], f"empty reviewer source: {row['review_id']}")
        require(set(row["extracted_fields"]) == set(FIELD_KEYS), f"reviewer field keys mismatch: {row['review_id']}")
        for items in row["extracted_fields"].values():
            for item in items:
                require(item["evidence"] in row["source_text"], f"reviewer evidence drift: {row['review_id']}")


def build(root: Path) -> dict[str, Any]:
    _, _, merged = require_authorised_local_only(root)
    output_root = root / OUTPUT_ROOT
    staging_root = output_root.with_name(".i3c_manual_qa.staging")
    checkpoint_path = root / CHECKPOINT
    qa_checkpoint_path = root / QA_CHECKPOINT
    require(not output_root.exists(), f"refusing to overwrite QA packet: {output_root}")
    require(not staging_root.exists(), f"stale QA staging directory: {staging_root}")
    require(checkpoint_path.is_file(), "v1.2 extraction checkpoint is missing")
    require(not qa_checkpoint_path.exists(), f"refusing to overwrite QA packet checkpoint: {qa_checkpoint_path}")

    canonical_path = root / merged["artifacts"]["canonical_extractions"]["path"]
    require(sha256_file(canonical_path) == merged["artifacts"]["canonical_extractions"]["sha256"], "canonical extraction hash drift")
    sources = read_jsonl(root / RELATIVE_ROOT / "source_manifest.jsonl")
    canonical = read_jsonl(canonical_path)
    metadata = build_metadata(sources, canonical)
    selected = select_rows(metadata)

    reviewer_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    form_rows: list[dict[str, Any]] = []
    for sample_index, source_index in enumerate(selected):
        source = sources[source_index]
        extraction = canonical[source_index]
        source_text = (root / source["source_path"]).read_bytes().decode("utf-8")
        review_id = f"rq2b-v12-i3c-qa-{sample_index + 1:03d}"
        reviewer_rows.append(
            {
                "review_id": review_id,
                "source_text": source_text,
                "extracted_fields": reviewer_field_view(extraction["fields"]),
                "retained_selector_spans": extraction["retained_selector_spans"],
                "omitted_selector_spans": extraction["omitted_selector_spans"],
                "field_warnings": extraction["field_warnings"],
                "qa_warnings": extraction["qa_warnings"],
            }
        )
        key_rows.append(
            {
                "review_id": review_id,
                "source_row_index": source_index,
                "skill_id": source["skill_id"],
                "source_path": source["source_path"],
                "source_sha256": source["source_sha256"],
                **metadata[source_index],
            }
        )
        form_rows.append(
            {
                "review_id": review_id,
                "review_status": "unreviewed",
                "critical_error": None,
                "major_error": None,
                "major_error_fields": [],
                "error_codes": [],
                "reviewer_notes": "",
                "reviewer_id": "",
            }
        )
    validate_blinded_packet(reviewer_rows)

    staging_root.mkdir(parents=True, exist_ok=False)
    reviewer_path = staging_root / "blinded_reviewer_packet.jsonl"
    key_path = staging_root / "sampling_key_do_not_give_reviewer.jsonl"
    form_path = staging_root / "review_form_uncompleted.jsonl"
    guidance_path = staging_root / "reviewer_guidance.md"
    write_jsonl_new(reviewer_path, reviewer_rows)
    write_jsonl_new(key_path, key_rows)
    write_jsonl_new(form_path, form_rows)
    guidance_path.write_text(
        "# RQ2b v1.2 I3C Blinded QA\n\n"
        "For each anonymous record, judge whether each extracted field is supported by the source text and whether its evidence span is exact and meaningful. Record only extraction fidelity errors. Do not assess retrieval, prompt fit, gold labels, or ranking. This packet intentionally contains no such information.\n\n"
        "Mark a critical error for unsupported or identity-breaking content. Mark a major error for a material missing, unsupported, misclassified, or misleading field item. Leave the form unreviewed until a separately approved reviewer completes it.\n",
        encoding="utf-8",
    )
    coverage = {
        "cohorts": dict(Counter(metadata[index]["cohort"] for index in selected)),
        "source_policies": dict(Counter(metadata[index]["source_policy"] for index in selected)),
        "families": dict(Counter(metadata[index]["family"] for index in selected)),
        "length_buckets": dict(Counter(metadata[index]["length_bucket"] for index in selected)),
        "density_buckets": dict(Counter(metadata[index]["density_bucket"] for index in selected)),
        "fields": {field: sum(field in metadata[index]["present_fields"] for index in selected) for field in FIELD_KEYS},
        "warning_codes": dict(Counter(code for index in selected for code in metadata[index]["warning_codes"])),
    }
    manifest = {
        "schema_version": "rq2b-v12-i3c-manual-qa-packet-v1",
        "version_id": VERSION_ID,
        "state": "blinded_review_pending",
        "sample_size": QA_SAMPLE_SIZE,
        "sample_seed": QA_SAMPLE_SEED,
        "network_calls": 0,
        "external_api_calls": 0,
        "manual_qa_completion_authorized": False,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "reviewer_packet_contains_prompt_gold_stratum_role_or_retrieval": False,
        "i3c_merge_manifest": {"path": f"{MERGED_ROOT}/manifest.json", "sha256": sha256_file(root / MERGED_ROOT / "manifest.json")},
        "feature_coverage": coverage,
        "artifacts": {
            "blinded_reviewer_packet": {"path": relative(output_root / reviewer_path.name, root), "sha256": sha256_file(reviewer_path), "rows": len(reviewer_rows)},
            "sampling_key_do_not_give_reviewer": {"path": relative(output_root / key_path.name, root), "sha256": sha256_file(key_path), "rows": len(key_rows)},
            "review_form_uncompleted": {"path": relative(output_root / form_path.name, root), "sha256": sha256_file(form_path), "rows": len(form_rows)},
            "reviewer_guidance": {"path": relative(output_root / guidance_path.name, root), "sha256": sha256_file(guidance_path)},
        },
    }
    write_json_new(staging_root / "manifest.json", manifest)
    staging_root.replace(output_root)

    extraction_checkpoint = read_json(checkpoint_path)
    require(extraction_checkpoint["state"] == "automatic_gates_passed_manual_qa_packet_not_yet_built", "unexpected v1.2 extraction checkpoint state")
    write_json_new(
        qa_checkpoint_path,
        {
            "schema_version": "rq2b-v12-i3c-manual-qa-packet-checkpoint-v1",
            "version_id": VERSION_ID,
            "state": "automatic_gates_passed_blinded_manual_qa_pending",
            "source_extraction_checkpoint": {"path": CHECKPOINT, "sha256": sha256_file(checkpoint_path)},
            "manual_qa_packet": {"path": relative(output_root / "manifest.json", root), "sha256": sha256_file(output_root / "manifest.json"), "review_rows": QA_SAMPLE_SIZE},
            "network_calls": 0,
            "external_api_calls": 0,
            "manual_qa_completion_authorized": False,
            "scientific_retrieval_or_reranking": False,
            "thesis_result_writing": False,
        },
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(build(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
