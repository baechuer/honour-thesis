#!/usr/bin/env python3
"""Build the local, blinded 120-row I3C QA packet for RQ2b v1.1.

This selects a deterministic coverage sample after automatic extraction gates.
It creates an uncompleted review form only; it never decides that the QA has
passed and it does not run retrieval, embedding, or external calls.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import (
    FIELD_SPECS,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    write_json_new,
    write_jsonl_new,
)
from rq2b_v11_contract import RELATIVE_ROOT, VERSION_ID, verify as verify_v11_contract


PARENT_VERSION = "rq2b-full-library-v1-2026-08-02"
PARENT_MANIFEST = f"skill_benchmark/rq2b_full_library/{PARENT_VERSION}/i3c_extraction/manifest.json"
MERGE_MANIFEST = f"{RELATIVE_ROOT}/i3c_merged/manifest.json"
LEDGER = f"{RELATIVE_ROOT}/i3c_extraction_execution_ledger.json"
PROMPT_MANIFEST = f"{RELATIVE_ROOT}/prompt_manifest.jsonl"
QA_ROOT = f"{RELATIVE_ROOT}/i3c_manual_qa_v2"
SUPERSEDED_QA_MANIFEST = f"{RELATIVE_ROOT}/i3c_manual_qa/manifest.json"
QA_SAMPLE_SIZE = 120
QA_SAMPLE_SEED = 2026081502
FIELD_KEYS = tuple(field for field, _ in FIELD_SPECS)


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


def source_rows(root: Path) -> list[dict[str, Any]]:
    manifest = read_json(root / PARENT_MANIFEST)
    rows: list[dict[str, Any]] = []
    for chunk in manifest["chunks"]:
        source = read_jsonl(root / chunk["input_path"])
        require(len(source) == chunk["row_count"], "I3C QA input chunk row mismatch")
        rows.extend(source)
    require(len(rows) == 2433, "I3C QA source count mismatch")
    require([row["source_row_index"] for row in rows] == list(range(2433)), "I3C QA source order mismatch")
    return rows


def role_map(root: Path, skill_ids: set[str]) -> dict[str, str]:
    prompts = read_jsonl(root / PROMPT_MANIFEST)
    gold = {row["gold_skill"] for row in prompts}
    neighbours = {skill_id for row in prompts for skill_id in row["closest_alternatives"]} - gold
    require(gold.issubset(skill_ids) and neighbours.issubset(skill_ids), "I3C QA role-map skill drift")
    return {
        skill_id: "eventual_gold" if skill_id in gold else "hard_neighbour" if skill_id in neighbours else "background"
        for skill_id in skill_ids
    }


def sample_rows(root: Path, sources: list[dict[str, Any]], canonical: list[dict[str, Any]]) -> tuple[list[int], dict[int, dict[str, Any]]]:
    require(len(sources) == len(canonical) == 2433, "I3C QA source/canonical count mismatch")
    lengths = sorted(
        range(len(sources)),
        key=lambda index: (len(sources[index]["text"].encode("utf-8")), sources[index]["skill_id"]),
    )
    length_buckets = {index: quantile_bucket(rank, len(lengths)) for rank, index in enumerate(lengths)}
    density_order = sorted(
        range(len(canonical)),
        key=lambda index: (len(canonical[index]["retained_selector_spans"]), canonical[index]["skill_id"]),
    )
    density_buckets = {
        index: "sparse" if rank < len(density_order) // 3 else "dense" if rank >= 2 * len(density_order) // 3 else "medium"
        for rank, index in enumerate(density_order)
    }
    roles = role_map(root, {row["skill_id"] for row in sources})
    metadata: dict[int, dict[str, Any]] = {}
    for index, (source, extraction) in enumerate(zip(sources, canonical, strict=True)):
        require(source["source_row_index"] == extraction["source_row_index"], "I3C QA row-index mismatch")
        require(source["skill_id"] == extraction["skill_id"], "I3C QA skill identity mismatch")
        metadata[index] = {
            "role": roles[source["skill_id"]],
            "family": source["family"],
            "length_bucket": length_buckets[index],
            "density_bucket": density_buckets[index],
            "present_fields": sorted(field for field in FIELD_KEYS if extraction["fields"][field]),
            "warning_codes": sorted({str(warning["code"]) for warning in extraction["qa_warnings"]}),
        }
    uncovered = {
        *(("role", value["role"]) for value in metadata.values()),
        *(("family", value["family"]) for value in metadata.values()),
        *(("length_bucket", value["length_bucket"]) for value in metadata.values()),
        *(("density_bucket", value["density_bucket"]) for value in metadata.values()),
        *(("field", field) for value in metadata.values() for field in value["present_fields"]),
        *(("warning", warning) for value in metadata.values() for warning in value["warning_codes"]),
    }
    generator = random.Random(QA_SAMPLE_SEED)
    candidates = list(metadata)
    generator.shuffle(candidates)
    selected: list[int] = []
    selected_set: set[int] = set()
    def features(index: int) -> set[tuple[str, str]]:
        value = metadata[index]
        return {
            ("role", value["role"]),
            ("family", value["family"]),
            ("length_bucket", value["length_bucket"]),
            ("density_bucket", value["density_bucket"]),
            *(("field", field) for field in value["present_fields"]),
            *(("warning", warning) for warning in value["warning_codes"]),
        }
    while uncovered and len(selected) < QA_SAMPLE_SIZE:
        best = max((index for index in candidates if index not in selected_set), key=lambda index: (len(features(index) & uncovered), -index))
        selected.append(best)
        selected_set.add(best)
        uncovered.difference_update(features(best))
    require(not uncovered, f"I3C QA sample cannot cover: {sorted(uncovered)}")
    strata: dict[tuple[str, str, str, str], list[int]] = defaultdict(list)
    for index, value in metadata.items():
        strata[(value["role"], value["family"], value["length_bucket"], value["density_bucket"])].append(index)
    for indices in strata.values():
        generator.shuffle(indices)
    keys = sorted(strata)
    cursor = 0
    while len(selected) < QA_SAMPLE_SIZE:
        key = keys[cursor % len(keys)]
        cursor += 1
        while strata[key] and strata[key][-1] in selected_set:
            strata[key].pop()
        if not strata[key]:
            if all(not values or all(index in selected_set for index in values) for values in strata.values()):
                break
            continue
        selected.append(strata[key].pop())
        selected_set.add(selected[-1])
    require(len(selected) == QA_SAMPLE_SIZE, "I3C QA sample did not reach 120 rows")
    return selected, metadata


def build(root: Path) -> dict[str, Any]:
    verify_v11_contract(root)
    merge_path = root / MERGE_MANIFEST
    ledger_path = root / LEDGER
    require(merge_path.is_file() and ledger_path.is_file(), "I3C automatic-gate artifacts are missing")
    merge = read_json(merge_path)
    ledger = read_json(ledger_path)
    require(merge.get("state") == "automatic_gates_passed_manual_qa_pending", "I3C merge is not awaiting QA")
    require(ledger.get("state") == "complete_all_chunks_automatic_gates_passed_manual_qa_pending", "I3C ledger is not complete")
    canonical_ref = merge["artifacts"]["canonical_extractions"]
    canonical_path = root / canonical_ref["path"]
    require(sha256_file(canonical_path) == canonical_ref["sha256"], "I3C canonical extraction drift")
    canonical = read_jsonl(canonical_path)
    sources = source_rows(root)
    selected, metadata = sample_rows(root, sources, canonical)

    reviewer_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    form_rows: list[dict[str, Any]] = []
    for sample_index, source_index in enumerate(selected):
        source = sources[source_index]
        extraction = canonical[source_index]
        review_id = f"rq2b-v11-i3c-qa-{sample_index:03d}"
        reviewer_rows.append({
            "sample_index": sample_index,
            "review_id": review_id,
            "source_row_index": source_index,
            "skill_id": source["skill_id"],
            "source_path": source["source"],
            "source_sha256": source["source_sha256"],
            "source_text": source["text"],
            "extracted_fields": extraction["fields"],
            "retained_selector_spans": extraction["retained_selector_spans"],
            "omitted_selector_spans": extraction["omitted_selector_spans"],
            "field_warnings": extraction["field_warnings"],
            "qa_warnings": extraction["qa_warnings"],
        })
        key_rows.append({"sample_index": sample_index, "review_id": review_id, "source_row_index": source_index, "skill_id": source["skill_id"], **metadata[source_index]})
        form_rows.append({
            "sample_index": sample_index,
            "review_id": review_id,
            "critical_error": None,
            "major_error": None,
            "major_error_fields": [],
            "error_codes": [],
            "reviewer_notes": "",
            "reviewer_id": "",
        })
    qa_root = root / QA_ROOT
    staging = qa_root.with_name(".i3c_manual_qa_v2.staging")
    require(not qa_root.exists() and not staging.exists(), "Refusing to overwrite or mix an I3C QA packet")
    staging.mkdir(parents=True, exist_ok=False)
    reviewer_path = staging / "blinded_reviewer_packet.jsonl"
    key_path = staging / "sampling_key_do_not_give_reviewer.jsonl"
    form_path = staging / "review_form_uncompleted.jsonl"
    write_jsonl_new(reviewer_path, reviewer_rows)
    write_jsonl_new(key_path, key_rows)
    write_jsonl_new(form_path, form_rows)
    manifest = {
        "schema_version": "rq2b-v11-i3c-manual-qa-packet-v2",
        "version_id": VERSION_ID,
        "state": "blinded_review_pending",
        "sample_size": QA_SAMPLE_SIZE,
        "sample_seed": QA_SAMPLE_SEED,
        "network_calls": 0,
        "external_api_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "reviewer_packet_contains_prompt_gold_stratum_or_role": False,
        "supersedes_unreviewed_packet": {"path": SUPERSEDED_QA_MANIFEST, "sha256": sha256_file(root / SUPERSEDED_QA_MANIFEST), "reason": "missing required role-stratified sampling"},
        "i3c_merge_manifest": {"path": MERGE_MANIFEST, "sha256": sha256_file(merge_path)},
        "i3c_execution_ledger": {"path": LEDGER, "sha256": sha256_file(ledger_path)},
        "feature_coverage": {
            "roles": dict(Counter(metadata[index]["role"] for index in selected)),
            "families": dict(Counter(metadata[index]["family"] for index in selected)),
            "length_buckets": dict(Counter(metadata[index]["length_bucket"] for index in selected)),
            "density_buckets": dict(Counter(metadata[index]["density_bucket"] for index in selected)),
            "fields": {field: sum(field in metadata[index]["present_fields"] for index in selected) for field in FIELD_KEYS},
            "warning_codes": dict(Counter(warning for index in selected for warning in metadata[index]["warning_codes"])),
        },
        "artifacts": {
            "blinded_reviewer_packet": {"path": relative(qa_root / reviewer_path.name, root), "sha256": sha256_file(reviewer_path), "rows": len(reviewer_rows)},
            "sampling_key": {"path": relative(qa_root / key_path.name, root), "sha256": sha256_file(key_path), "rows": len(key_rows)},
            "uncompleted_review_form": {"path": relative(qa_root / form_path.name, root), "sha256": sha256_file(form_path), "rows": len(form_rows)},
        },
        "manual_qa_completion_authorized": False,
        "retrieval_authorized": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(qa_root)
    return verify(root)


def contains_forbidden_metadata_key(value: Any) -> bool:
    forbidden = {"prompt", "prompt_id", "gold", "gold_skill", "stratum", "role", "closest_alternatives"}
    if isinstance(value, dict):
        return bool(set(value) & forbidden) or any(contains_forbidden_metadata_key(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_forbidden_metadata_key(item) for item in value)
    return False


def verify(root: Path) -> dict[str, Any]:
    qa_root = root / QA_ROOT
    manifest_path = qa_root / "manifest.json"
    require(manifest_path.is_file(), "I3C QA manifest is missing")
    manifest = read_json(manifest_path)
    require(manifest.get("schema_version") == "rq2b-v11-i3c-manual-qa-packet-v2", "I3C QA schema mismatch")
    require(manifest.get("version_id") == VERSION_ID and manifest.get("state") == "blinded_review_pending", "I3C QA state mismatch")
    require(manifest.get("sample_size") == QA_SAMPLE_SIZE and manifest.get("sample_seed") == QA_SAMPLE_SEED, "I3C QA sample contract drift")
    require(manifest.get("network_calls") == manifest.get("external_api_calls") == 0, "I3C QA records external access")
    require(manifest.get("scientific_retrieval_or_reranking") is False, "I3C QA crossed retrieval boundary")
    require(manifest.get("manual_qa_completion_authorized") is False and manifest.get("retrieval_authorized") is False, "I3C QA authorization boundary drift")
    superseded = manifest.get("supersedes_unreviewed_packet")
    require(isinstance(superseded, dict), "I3C QA supersession binding is missing")
    require(
        superseded == {
            "path": SUPERSEDED_QA_MANIFEST,
            "sha256": sha256_file(root / SUPERSEDED_QA_MANIFEST),
            "reason": "missing required role-stratified sampling",
        },
        "I3C QA supersession binding drift",
    )
    artifacts = manifest.get("artifacts", {})
    require(set(artifacts) == {"blinded_reviewer_packet", "sampling_key", "uncompleted_review_form"}, "I3C QA artifact set mismatch")
    loaded: dict[str, list[dict[str, Any]]] = {}
    for name, artifact in artifacts.items():
        path = root / artifact["path"]
        require(path.is_file() and sha256_file(path) == artifact["sha256"], "I3C QA artifact hash drift")
        loaded[name] = read_jsonl(path)
        require(len(loaded[name]) == artifact["rows"] == QA_SAMPLE_SIZE, "I3C QA artifact row mismatch")
    reviewer = loaded["blinded_reviewer_packet"]
    key = loaded["sampling_key"]
    form = loaded["uncompleted_review_form"]
    reviewer_keys = {
        "sample_index", "review_id", "source_row_index", "skill_id", "source_path", "source_sha256", "source_text",
        "extracted_fields", "retained_selector_spans", "omitted_selector_spans", "field_warnings", "qa_warnings",
    }
    form_keys = {"sample_index", "review_id", "critical_error", "major_error", "major_error_fields", "error_codes", "reviewer_notes", "reviewer_id"}
    require(all(set(row) == reviewer_keys for row in reviewer), "I3C reviewer packet key mismatch")
    require(all(set(row) == form_keys for row in form), "I3C review form key mismatch")
    require(not contains_forbidden_metadata_key(reviewer), "I3C reviewer packet contains forbidden routing metadata")
    require(set(manifest["feature_coverage"]["roles"]) == {"eventual_gold", "hard_neighbour", "background"}, "I3C QA role coverage mismatch")
    reviewer_ids = [row["review_id"] for row in reviewer]
    require(len(set(reviewer_ids)) == QA_SAMPLE_SIZE, "I3C reviewer IDs are not unique")
    require(reviewer_ids == [row["review_id"] for row in key] == [row["review_id"] for row in form], "I3C QA packet identity alignment failure")
    require(all(row["critical_error"] is None and row["major_error"] is None and not row["reviewer_id"] for row in form), "I3C review form is not uncompleted")
    return {
        "state": "blinded_review_pending",
        "network_calls": 0,
        "external_api_calls": 0,
        "reviewer_packet_contains_prompt_gold_stratum_or_role": False,
        "sample_size": QA_SAMPLE_SIZE,
        "families_covered": len(manifest["feature_coverage"]["families"]),
        "all_fields_covered": all(count > 0 for count in manifest["feature_coverage"]["fields"].values()),
        "review_form_uncompleted": True,
        "reviewer_packet": artifacts["blinded_reviewer_packet"],
        "review_form": artifacts["uncompleted_review_form"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = verify(args.root.resolve()) if args.verify_only else build(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
