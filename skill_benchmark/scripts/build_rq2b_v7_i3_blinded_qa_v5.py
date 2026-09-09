#!/usr/bin/env python3
"""Build the fresh post-class-repair V4.1.4 I3 fidelity QA packet."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import build_rq2b_v7_i3_blinded_qa_v4 as prior
from build_rq2b_v7_i3_blinded_qa_v2 import calibration
from merge_rq2b_i3c import FIELD_KEYS
from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE, build as build_inputs
from validate_rq2b_v7_i3_v4_1_batch import PREP, ROOT


MERGED = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_4")
PREVIOUS_QA = (
    Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v2"),
    Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v4"),
)
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v5")
SEED = "rq2b-v7-i3-full-corpus-v4.1.4-fresh-qa-20260909-02"
SCHEMA = "rq2b-v7-i3-full-corpus-v4.1.4-blinded-qa-v1"
GUIDANCE = prior.GUIDANCE.replace("V4.1.3", "V4.1.4 post-class-repair").replace("QA v4", "QA v5")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in values).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build() -> dict[str, bytes]:
    # The inherited stratified sampler is reused with a new frozen seed.  Its
    # only stateful input is this module-level value.
    prior.SEED = SEED
    merged_manifest_path = ROOT / MERGED / "manifest.json"
    merged_manifest = json.loads(merged_manifest_path.read_bytes())
    require(merged_manifest["state"] == "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", "V4.1.4 repair merge is not QA-ready")
    canonical_path = ROOT / MERGED / "canonical_extractions.jsonl"
    canonical = rows(canonical_path.read_bytes())
    require(len(canonical) == 3798, "V4.1.4 canonical population mismatch")
    require(merged_manifest["artifacts"]["canonical_extractions.jsonl"]["sha256"] == sha(canonical_path.read_bytes()), "V4.1.4 canonical hash drift")

    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    assignments = rows(assignments_path.read_bytes())
    require(merged_manifest["bindings"]["assignment_manifest_sha256"] == sha(assignments_path.read_bytes()), "V4.1.4 assignment binding drift")
    _, input_payloads = build_inputs()
    input_by_sha: dict[str, dict] = {}
    extractor_by_sha: dict[str, int] = {}
    for assignment in assignments:
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = input_payloads[input_name]
        require(sha(input_data) == assignment["input_sha256"], f"V4.1.4 QA input hash drift: {assignment['batch_id']}")
        for row in rows(input_data):
            require(row["source_sha256"] not in input_by_sha, "duplicate V4.1.4 source identity")
            input_by_sha[row["source_sha256"]] = row
            extractor_by_sha[row["source_sha256"]] = assignment["extractor_group"]
    require(len(input_by_sha) == 3798, "V4.1.4 input population mismatch")

    excluded: set[str] = set()
    previous_bindings: list[dict[str, str | int]] = []
    for package in PREVIOUS_QA:
        manifest_path = ROOT / package / "manifest.json"
        key_path = ROOT / package / "sampling_key_do_not_give_reviewer.jsonl"
        manifest = json.loads(manifest_path.read_bytes())
        require(manifest["artifacts"]["sampling_key_do_not_give_reviewer.jsonl"]["sha256"] == sha(key_path.read_bytes()), f"prior QA key drift: {package}")
        sample = {row["source_sha256"] for row in rows(key_path.read_bytes())}
        require(len(sample) == 120 and not (excluded & sample), f"prior QA sample overlap/drift: {package}")
        excluded |= sample
        previous_bindings.append({"path": str(package / "manifest.json"), "sha256": sha(manifest_path.read_bytes()), "sample_rows": 120})
    require(len(excluded) == 240, "fresh QA cumulative exclusion mismatch")

    quartiles = prior.length_quartiles(list(input_by_sha.values()))
    population: list[dict] = []
    for extraction in canonical:
        source_sha = extraction["source_sha256"]
        if source_sha in excluded:
            continue
        source = input_by_sha[source_sha]
        fields = prior.visible_fields(extraction)
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
    require(len(population) == 3558, "V4.1.4 fresh population mismatch")
    selected = prior.sample(population)
    reviewer_groups = prior.assign_reviewers(selected)
    selected.sort(key=lambda row: prior.stable_key("review-id", row["skill_id"]))

    reviewer_rows: list[dict] = []
    key_rows: list[dict] = []
    for index, row in enumerate(selected, 1):
        review_id = "V7-I3-V414-QA-" + prior.stable_key("id", row["skill_id"])[:16].upper()
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
            "provenance": "FRESH_POST_CLASS_REPAIR_V4_1_4",
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
        group_keys = sorted((row for row in key_rows if row["assigned_reviewer_group"] == group), key=lambda row: prior.stable_key("slot", row["review_id"]))
        require(len(group_keys) == 40, f"V4.1.4 reviewer-group mismatch: {group}")
        for within_group in (0, 1):
            slot = (group - 1) * 2 + within_group + 1
            subset = group_keys[within_group * 20:(within_group + 1) * 20]
            files[f"review_slots/qa_slot_{slot:02d}.jsonl"] = rows_bytes([visible_by_id[row["review_id"]] for row in subset])
    fixtures, answers = calibration()
    files["calibration_input.jsonl"] = rows_bytes(fixtures)
    files["calibration_answer_key_do_not_give_reviewer.jsonl"] = rows_bytes(answers)

    manifest = {
        "schema_version": SCHEMA,
        "state": "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS",
        "formal_execution_ready": False,
        "sample_size": 120,
        "sampling_seed": SEED,
        "previous_samples_excluded": 240,
        "review_slots": 6,
        "rows_per_slot": 20,
        "calibration_rows": 8,
        "counts": {
            "extractor_group": dict(sorted(Counter(row["extractor_group"] for row in key_rows).items())),
            "reviewer_group": dict(sorted(Counter(row["assigned_reviewer_group"] for row in key_rows).items())),
            "length_quartile": dict(sorted(Counter(row["length_quartile"] for row in key_rows).items())),
            "present_field_rows": {field: sum(field in row["present_fields"] for row in key_rows) for field in FIELD_KEYS},
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
            "merged_manifest_sha256": sha(merged_manifest_path.read_bytes()),
            "failed_qa_v4_final_report_sha256": sha((ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v4/qa_final_report.json").read_bytes()),
            "previous_qa_packages": previous_bindings,
            "assignment_manifest_sha256": sha(assignments_path.read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "boundary": "Source-only extraction fidelity. No query, label, acceptable set, retrieval result, metric, or provider output is visible to reviewers.",
    }
    manifest["artifacts"] = {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()}
    files["manifest.json"] = json_bytes(manifest)
    files["README.md"] = (
        "# V7 I3 V4.1.4 blinded QA v5\n\n"
        "This fresh 120-row source-only sample follows the full-corpus class repair and excludes all 240 sources used in the two earlier QA samples. It preserves the same calibration, cross-assignment, quartile balance, and zero-critical/5% pass rule.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa_v5.py --verify`.\n"
    ).encode()
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1.4 QA v5 package missing")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        require(actual == set(expected), "V4.1.4 QA v5 file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1.4 QA v5 drift: {name}")
        status = "PASS_V7_I3_V4_1_4_QA_V5_PACKET_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1.4 QA v5 package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_4_QA_V5_PACKET_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
