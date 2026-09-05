#!/usr/bin/env python3
"""Build a deterministic 120-row blinded manual-QA packet for RQ2b I3C."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import (
    FIELD_SPECS,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    version_root,
    write_json_new,
    write_jsonl_new,
)


QA_SAMPLE_SIZE = 120
QA_SAMPLE_SEED = 2026080203
FIELD_KEYS = tuple(field for field, _ in FIELD_SPECS)


def role_map(prompts: list[dict[str, Any]], skill_ids: set[str]) -> dict[str, str]:
    gold = {row["gold_skill"] for row in prompts}
    neighbours = {
        skill_id
        for row in prompts
        for skill_id in row["closest_alternatives"]
    } - gold
    return {
        skill_id: (
            "eventual_gold"
            if skill_id in gold
            else "hard_neighbour"
            if skill_id in neighbours
            else "background"
        )
        for skill_id in skill_ids
    }


def quantile_bucket(index: int, total: int) -> str:
    fraction = index / max(1, total)
    if fraction < 0.25:
        return "short"
    if fraction < 0.75:
        return "median"
    if fraction < 0.95:
        return "p75_to_p95"
    if fraction < 0.99:
        return "p95_to_p99"
    return "longest"


def sample_rows(
    sources: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
) -> tuple[list[int], dict[int, dict[str, Any]]]:
    require(len(sources) == len(canonical), "QA source/extraction row count mismatch")
    require(len(sources) >= QA_SAMPLE_SIZE, "QA population is smaller than the sample")
    skill_ids = {row["skill_id"] for row in sources}
    roles = role_map(prompts, skill_ids)
    by_length = sorted(
        range(len(sources)),
        key=lambda index: (
            int(sources[index].get("qa_source_utf8_bytes", sources[index]["source_utf8_bytes"])),
            sources[index]["skill_id"],
        ),
    )
    length_bucket_by_index = {
        source_index: quantile_bucket(rank, len(by_length))
        for rank, source_index in enumerate(by_length)
    }
    item_counts = [len(row["retained_selector_spans"]) for row in canonical]
    ordered_density = sorted(range(len(canonical)), key=lambda index: (item_counts[index], canonical[index]["skill_id"]))
    density_by_index = {
        source_index: (
            "sparse"
            if rank < len(ordered_density) // 3
            else "dense"
            if rank >= 2 * len(ordered_density) // 3
            else "medium"
        )
        for rank, source_index in enumerate(ordered_density)
    }
    metadata: dict[int, dict[str, Any]] = {}
    for index, (source, extraction) in enumerate(zip(sources, canonical, strict=True)):
        require(source["skill_id"] == extraction["skill_id"], f"QA identity mismatch: {index}")
        warning_codes = sorted(
            {
                str(warning.get("code") or "warning")
                for warning in extraction["qa_warnings"]
                if isinstance(warning, dict)
            }
        )
        present_fields = sorted(
            field for field in FIELD_KEYS if extraction["fields"][field]
        )
        metadata[index] = {
            "role": roles[source["skill_id"]],
            "source_policy": source["source_policy"],
            "length_bucket": length_bucket_by_index[index],
            "density_bucket": density_by_index[index],
            "present_fields": present_fields,
            "warning_codes": warning_codes,
        }

    uncovered: set[tuple[str, str]] = set()
    for values in metadata.values():
        uncovered.add(("role", values["role"]))
        uncovered.add(("source_policy", values["source_policy"]))
        uncovered.add(("length_bucket", values["length_bucket"]))
        uncovered.add(("density_bucket", values["density_bucket"]))
        uncovered.update(("field", value) for value in values["present_fields"])
        uncovered.update(("warning", value) for value in values["warning_codes"])

    generator = random.Random(QA_SAMPLE_SEED)
    candidates = list(metadata)
    generator.shuffle(candidates)
    selected: list[int] = []
    selected_set: set[int] = set()
    while uncovered and len(selected) < QA_SAMPLE_SIZE:
        best_index = max(
            (index for index in candidates if index not in selected_set),
            key=lambda index: (
                sum(
                    feature in uncovered
                    for feature in [
                        ("role", metadata[index]["role"]),
                        ("source_policy", metadata[index]["source_policy"]),
                        ("length_bucket", metadata[index]["length_bucket"]),
                        ("density_bucket", metadata[index]["density_bucket"]),
                        *(("field", value) for value in metadata[index]["present_fields"]),
                        *(("warning", value) for value in metadata[index]["warning_codes"]),
                    ]
                ),
                -index,
            ),
        )
        features = {
            ("role", metadata[best_index]["role"]),
            ("source_policy", metadata[best_index]["source_policy"]),
            ("length_bucket", metadata[best_index]["length_bucket"]),
            ("density_bucket", metadata[best_index]["density_bucket"]),
            *(("field", value) for value in metadata[best_index]["present_fields"]),
            *(("warning", value) for value in metadata[best_index]["warning_codes"]),
        }
        selected.append(best_index)
        selected_set.add(best_index)
        uncovered.difference_update(features)
    require(not uncovered, f"QA sample cannot cover all required features within 120 rows: {sorted(uncovered)}")

    strata: dict[tuple[str, str, str, str], list[int]] = defaultdict(list)
    for index, values in metadata.items():
        strata[
            (
                values["role"],
                values["source_policy"],
                values["length_bucket"],
                values["density_bucket"],
            )
        ].append(index)
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
            if all(not values or all(index in selected_set for index in values) for values in strata.values()):
                break
            continue
        index = strata[key].pop()
        selected.append(index)
        selected_set.add(index)
    require(len(selected) == QA_SAMPLE_SIZE, "QA sample did not reach 120 rows")
    return selected, metadata


def build(root: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    frozen_root = version_root(root)
    i3_root = frozen_root / "i3c_merged"
    i3_manifest = read_json(i3_root / "manifest.json")
    require(i3_manifest.get("state") == "automatic_gates_passed_manual_qa_pending", "I3C automatic gates are not ready for QA")
    canonical_path = root / i3_manifest["artifacts"]["canonical_extractions"]["path"]
    require(sha256_file(canonical_path) == i3_manifest["artifacts"]["canonical_extractions"]["sha256"], "Canonical I3C extraction drift")
    canonical = read_jsonl(canonical_path)
    sources = read_jsonl(frozen_root / "source_manifest.jsonl")
    prompts = read_jsonl(frozen_root / "prompt_manifest.jsonl")
    require(len(sources) == len(canonical) == 2433, "QA source/extraction row count mismatch")
    sampling_sources = []
    for source in sources:
        sampling_source = dict(source)
        sampling_source["qa_source_utf8_bytes"] = len((root / source["source_path"]).read_bytes())
        sampling_sources.append(sampling_source)
    selected, metadata = sample_rows(sampling_sources, canonical, prompts)

    reviewer_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    review_form_rows: list[dict[str, Any]] = []
    for sample_index, source_index in enumerate(selected):
        source = sources[source_index]
        extraction = canonical[source_index]
        source_text = (root / source["source_path"]).read_bytes().decode("utf-8")
        reviewer_rows.append(
            {
                "sample_index": sample_index,
                "review_id": f"rq2b-qa-{sample_index:03d}",
                "source_row_index": source_index,
                "skill_id": source["skill_id"],
                "source_path": source["source_path"],
                "source_sha256": source["source_sha256"],
                "source_text": source_text,
                "extracted_fields": extraction["fields"],
                "retained_selector_spans": extraction["retained_selector_spans"],
                "omitted_selector_spans": extraction["omitted_selector_spans"],
                "field_warnings": extraction["field_warnings"],
                "qa_warnings": extraction["qa_warnings"],
            }
        )
        key_rows.append(
            {
                "sample_index": sample_index,
                "review_id": f"rq2b-qa-{sample_index:03d}",
                "source_row_index": source_index,
                "skill_id": source["skill_id"],
                **metadata[source_index],
            }
        )
        review_form_rows.append(
            {
                "sample_index": sample_index,
                "review_id": f"rq2b-qa-{sample_index:03d}",
                "critical_error": None,
                "major_error": None,
                "major_error_fields": [],
                "error_codes": [],
                "reviewer_notes": "",
                "reviewer_id": "",
            }
        )

    output_root = frozen_root / "i3c_manual_qa"
    staging = frozen_root / ".i3c_manual_qa.staging"
    require(not output_root.exists(), f"I3C manual-QA root exists: {output_root}")
    require(not staging.exists(), f"Stale I3C manual-QA staging root: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    reviewer_path = staging / "blinded_reviewer_packet.jsonl"
    key_path = staging / "sampling_key_do_not_give_reviewer.jsonl"
    form_path = staging / "review_form_uncompleted.jsonl"
    write_jsonl_new(reviewer_path, reviewer_rows)
    write_jsonl_new(key_path, key_rows)
    write_jsonl_new(form_path, review_form_rows)
    manifest = {
        "schema_version": "rq2b-i3c-manual-qa-packet-v1",
        "version_id": VERSION_ID,
        "state": "blinded_review_pending",
        "sample_size": QA_SAMPLE_SIZE,
        "sample_seed": QA_SAMPLE_SEED,
        "network_calls": 0,
        "reviewer_packet_contains_prompt_gold_stratum_or_role": False,
        "i3c_manifest_sha256": sha256_file(i3_root / "manifest.json"),
        "feature_coverage": {
            "roles": dict(Counter(metadata[index]["role"] for index in selected)),
            "source_policies": dict(Counter(metadata[index]["source_policy"] for index in selected)),
            "length_buckets": dict(Counter(metadata[index]["length_bucket"] for index in selected)),
            "density_buckets": dict(Counter(metadata[index]["density_bucket"] for index in selected)),
            "fields": {
                field: sum(field in metadata[index]["present_fields"] for index in selected)
                for field in FIELD_KEYS
            },
            "warning_codes": dict(
                Counter(
                    warning
                    for index in selected
                    for warning in metadata[index]["warning_codes"]
                )
            ),
        },
        "artifacts": {
            "blinded_reviewer_packet": {"path": relative(output_root / reviewer_path.name, root), "sha256": sha256_file(reviewer_path), "rows": len(reviewer_rows)},
            "sampling_key": {"path": relative(output_root / key_path.name, root), "sha256": sha256_file(key_path), "rows": len(key_rows)},
            "uncompleted_review_form": {"path": relative(output_root / form_path.name, root), "sha256": sha256_file(form_path), "rows": len(review_form_rows)},
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    sources: list[dict[str, Any]] = []
    canonical: list[dict[str, Any]] = []
    for index in range(150):
        skill_id = f"s{index:03d}"
        sources.append(
            {
                "source_row_index": index,
                "skill_id": skill_id,
                "source_policy": "public_original" if index % 2 else "authored_skill",
                "source_utf8_bytes": index + 1,
            }
        )
        fields = {field: [] for field in FIELD_KEYS}
        fields[FIELD_KEYS[index % len(FIELD_KEYS)]] = [{"id": "x"}]
        canonical.append(
            {
                "source_row_index": index,
                "skill_id": skill_id,
                "fields": fields,
                "retained_selector_spans": [{}] * (index % 8),
                "qa_warnings": ([{"code": f"w{index % 3}"}] if index % 5 == 0 else []),
            }
        )
    prompts = [
        {
            "gold_skill": "s000",
            "closest_alternatives": ["s001", "s002"],
        }
    ]
    selected_a, metadata_a = sample_rows(sources, canonical, prompts)
    selected_b, metadata_b = sample_rows(sources, canonical, prompts)
    require(selected_a == selected_b and metadata_a == metadata_b, "I3C QA sampling is not deterministic")
    require(len(selected_a) == QA_SAMPLE_SIZE, "I3C QA sample-size self-test failed")
    require({metadata_a[index]["role"] for index in selected_a} == {"eventual_gold", "hard_neighbour", "background"}, "I3C QA role coverage failed")
    return {
        "state": "synthetic_blinded_sampling_only",
        "sample_size": len(selected_a),
        "deterministic": True,
        "roles_covered": sorted({metadata_a[index]["role"] for index in selected_a}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = self_test() if args.self_test else build(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
