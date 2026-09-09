#!/usr/bin/env python3
"""Build a fresh blinded QA v6 packet for post-repair I3 V4.1.5."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import build_rq2b_v7_i3_blinded_qa_v4 as sampler
from build_rq2b_v7_i3_blinded_qa_v2 import calibration
from merge_rq2b_i3c import FIELD_KEYS
from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE, build as build_inputs
from validate_rq2b_v7_i3_v4_1_batch import PREP, ROOT


MERGED = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_class_repair_2026_09_09_v4_1_5"
)
PREVIOUS_QA = (
    Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v2"),
    Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v4"),
    Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v5"),
)
FAILED_QA_V5 = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_blinded_qa_final_2026_09_09_v5/qa_final_report.json"
)
OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_blinded_qa_2026_09_09_v6"
)
SEED = "rq2b-v7-i3-full-corpus-v4.1.5-fresh-qa-20260909-03"
SCHEMA = "rq2b-v7-i3-full-corpus-v4.1.5-blinded-qa-v1"
GUIDANCE = sampler.GUIDANCE.replace(
    "V4.1.3", "V4.1.5 post-second-class-repair"
).replace("QA v4", "QA v6")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: list[dict]) -> bytes:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in values
    ).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build() -> dict[str, bytes]:
    sampler.SEED = SEED
    merged_manifest_path = ROOT / MERGED / "manifest.json"
    merged_manifest_data = merged_manifest_path.read_bytes()
    merged_manifest = json.loads(merged_manifest_data)
    require(merged_manifest["schema_version"] == "rq2b-v7-phase7-i3-class-repair-v4.1.5", "V4.1.5 repair schema mismatch")
    require(merged_manifest["state"] == "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", "V4.1.5 repair is not QA-ready")
    canonical_path = ROOT / MERGED / "canonical_extractions.jsonl"
    canonical_data = canonical_path.read_bytes()
    canonical = rows(canonical_data)
    require(len(canonical) == 3798, "V4.1.5 canonical population mismatch")
    require(merged_manifest["artifacts"]["canonical_extractions.jsonl"]["sha256"] == sha(canonical_data), "V4.1.5 canonical hash drift")

    failed_v5_data = (ROOT / FAILED_QA_V5).read_bytes()
    failed_v5 = json.loads(failed_v5_data)
    require(failed_v5["state"] == "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE", "failed QA v5 state drift")
    require(failed_v5["counts"]["major_error_rows"] == 13 and failed_v5["counts"]["critical_error_rows"] == 0, "failed QA v5 count drift")
    require(merged_manifest["bindings"]["failed_fresh_qa_v5_report_sha256"] == sha(failed_v5_data), "V4.1.5 failed-QA-v5 binding drift")

    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    assignments_data = assignments_path.read_bytes()
    assignments = rows(assignments_data)
    require(merged_manifest["bindings"]["assignment_manifest_sha256"] == sha(assignments_data), "V4.1.5 assignment binding drift")
    _, input_payloads = build_inputs()
    input_by_sha: dict[str, dict] = {}
    extractor_by_sha: dict[str, int] = {}
    for assignment in assignments:
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = input_payloads[input_name]
        require(sha(input_data) == assignment["input_sha256"], f"V4.1.5 QA input hash drift: {assignment['batch_id']}")
        for row in rows(input_data):
            require(row["source_sha256"] not in input_by_sha, "duplicate V4.1.5 source identity")
            input_by_sha[row["source_sha256"]] = row
            extractor_by_sha[row["source_sha256"]] = assignment["extractor_group"]
    require(len(input_by_sha) == 3798, "V4.1.5 QA input population mismatch")

    excluded: set[str] = set()
    previous_bindings: list[dict[str, str | int]] = []
    for package in PREVIOUS_QA:
        manifest_path = ROOT / package / "manifest.json"
        key_path = ROOT / package / "sampling_key_do_not_give_reviewer.jsonl"
        manifest_data = manifest_path.read_bytes()
        manifest = json.loads(manifest_data)
        key_data = key_path.read_bytes()
        require(manifest["artifacts"]["sampling_key_do_not_give_reviewer.jsonl"]["sha256"] == sha(key_data), f"prior QA key drift: {package}")
        sample = {row["source_sha256"] for row in rows(key_data)}
        require(len(sample) == 120 and not (excluded & sample), f"prior QA sample overlap/drift: {package}")
        excluded |= sample
        previous_bindings.append({
            "path": str(package / "manifest.json"),
            "sha256": sha(manifest_data),
            "sample_rows": 120,
        })
    require(len(excluded) == 360, "fresh QA v6 cumulative exclusion mismatch")

    quartiles = sampler.length_quartiles(list(input_by_sha.values()))
    population: list[dict] = []
    for extraction in canonical:
        source_sha = extraction["source_sha256"]
        if source_sha in excluded:
            continue
        source = input_by_sha[source_sha]
        fields = sampler.visible_fields(extraction)
        population.append({
            "source_row_index": extraction["source_row_index"],
            "skill_id": extraction["skill_id"],
            "source_sha256": source_sha,
            "source_path": extraction["source"],
            "source_text": source["text"],
            "name": extraction["name"],
            "description": extraction["description"],
            "visible_fields": fields,
            "present_fields": sorted(field for field, items in fields.items() if items),
            "length_quartile": quartiles[source_sha],
            "extractor_group": extractor_by_sha[source_sha],
        })
    require(len(population) == 3438, "V4.1.5 fresh population mismatch")
    selected = sampler.sample(population)
    reviewer_groups = sampler.assign_reviewers(selected)
    selected.sort(key=lambda row: sampler.stable_key("review-id", row["skill_id"]))

    reviewer_rows: list[dict] = []
    key_rows: list[dict] = []
    for index, row in enumerate(selected, 1):
        review_id = "V7-I3-V415-QA-" + sampler.stable_key("id", row["skill_id"])[:16].upper()
        reviewer_rows.append({
            "review_id": review_id,
            "source_text": row["source_text"],
            "native_selector_metadata": {"name": row["name"], "description": row["description"]},
            "selector_visible_evidence": row["visible_fields"],
        })
        key_rows.append({
            "review_id": review_id,
            "sample_index": index,
            "source_row_index": row["source_row_index"],
            "source_sha256": row["source_sha256"],
            "source_path": row["source_path"],
            "provenance": "FRESH_POST_CLASS_REPAIR_V4_1_5",
            "length_quartile": row["length_quartile"],
            "present_fields": row["present_fields"],
            "extractor_group": row["extractor_group"],
            "assigned_reviewer_group": reviewer_groups[row["skill_id"]],
        })

    visible_by_id = {row["review_id"]: row for row in reviewer_rows}
    schema = json.loads((ROOT / PREVIOUS_QA[-1] / "reviewer_return_schema.json").read_bytes())
    files: dict[str, bytes] = {
        "blinded_reviewer_packet.jsonl": rows_bytes(reviewer_rows),
        "sampling_key_do_not_give_reviewer.jsonl": rows_bytes(key_rows),
        "reviewer_guidance.md": GUIDANCE.encode(),
        "reviewer_return_schema.json": json_bytes(schema),
    }
    for group in (1, 2, 3):
        group_keys = sorted(
            (row for row in key_rows if row["assigned_reviewer_group"] == group),
            key=lambda row: sampler.stable_key("slot", row["review_id"]),
        )
        require(len(group_keys) == 40, f"V4.1.5 reviewer-group mismatch: {group}")
        for within_group in (0, 1):
            slot = (group - 1) * 2 + within_group + 1
            subset = group_keys[within_group * 20:(within_group + 1) * 20]
            files[f"review_slots/qa_slot_{slot:02d}.jsonl"] = rows_bytes(
                [visible_by_id[row["review_id"]] for row in subset]
            )
    fixtures, answers = calibration()
    files["calibration_input.jsonl"] = rows_bytes(fixtures)
    files["calibration_answer_key_do_not_give_reviewer.jsonl"] = rows_bytes(answers)

    manifest = {
        "schema_version": SCHEMA,
        "state": "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS",
        "formal_execution_ready": False,
        "sample_size": 120,
        "sampling_seed": SEED,
        "previous_samples_excluded": 360,
        "review_slots": 6,
        "rows_per_slot": 20,
        "calibration_rows": 8,
        "counts": {
            "extractor_group": dict(sorted(Counter(row["extractor_group"] for row in key_rows).items())),
            "reviewer_group": dict(sorted(Counter(row["assigned_reviewer_group"] for row in key_rows).items())),
            "length_quartile": dict(sorted(Counter(row["length_quartile"] for row in key_rows).items())),
            "present_field_rows": {
                field: sum(field in row["present_fields"] for row in key_rows)
                for field in FIELD_KEYS
            },
        },
        "pass_rule": {
            "calibration": "each reviewer group exactly matches all 8 hidden answers",
            "critical_error_rows": 0,
            "maximum_major_error_rows": 6,
            "maximum_major_error_rate": 0.05,
            "field_stratum_rule": "for each field represented in at least 20 rows, major error rate must be <=0.05",
            "failure_action": "repair the full affected class and draw another fresh versioned sample; never patch only sampled rows",
        },
        "cross_assignment": "Every sampled row is reviewed by a group different from its extractor group; each reviewer group receives 40 rows.",
        "bindings": {
            "merged_manifest_sha256": sha(merged_manifest_data),
            "failed_qa_v5_final_report_sha256": sha(failed_v5_data),
            "previous_qa_packages": previous_bindings,
            "assignment_manifest_sha256": sha(assignments_data),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "boundary": "Source-only extraction fidelity. No query, label, acceptable set, retrieval result, metric, or provider output is visible to reviewers.",
    }
    manifest["artifacts"] = {
        name: {"sha256": sha(data), "rows": len(data.splitlines())}
        for name, data in files.items()
    }
    files["manifest.json"] = json_bytes(manifest)
    files["README.md"] = (
        "# V7 I3 V4.1.5 blinded QA v6\n\n"
        "This new 120-row source-only sample follows the second full-corpus class "
        "repair and excludes all 360 source identities from QA v2, v4, and v5. "
        "It retains the same calibration, cross-assignment, extractor/quartile "
        "balance, field minimum, and zero-critical/5% pass rule. Failed QA v5 "
        "remains immutable evidence.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa_v6.py --verify`.\n"
    ).encode()
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1.5 QA v6 package missing")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        require(actual == set(expected), "V4.1.5 QA v6 file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1.5 QA v6 drift: {name}")
        status = "PASS_V7_I3_V4_1_5_QA_V6_PACKET_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1.5 QA v6 package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_5_QA_V6_PACKET_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
