#!/usr/bin/env python3
"""Build a fresh 120-row blinded QA packet for full-corpus I3 V4.1.3."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from build_rq2b_v7_i3_blinded_qa_v2 import GUIDANCE as V2_GUIDANCE, calibration
from merge_rq2b_i3c import FIELD_KEYS
from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE, build as build_inputs
from validate_rq2b_v7_i3_v4_1_batch import PREP, ROOT


MERGED = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_merged_2026_09_09_v4_1_3")
PREVIOUS_QA = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v2")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v4")
SEED = "rq2b-v7-i3-full-corpus-v4.1.3-fresh-qa-20260909-01"
ROWS_PER_EXTRACTOR_GROUP = 40
ROWS_PER_GROUP_QUARTILE = 10
MIN_PRESENT_PER_FIELD = 20
GUIDANCE = V2_GUIDANCE.replace(
    "# V7 blinded I1/I3 extraction-fidelity QA v2",
    "# V7 blinded I1/I3 full-corpus V4.1.3 extraction-fidelity QA v4",
).replace(
    "The packet contains only evidence that the actual I3C/I3-flat serializers retain.",
    "All rows come from the warning-audited full-corpus V4.1.3 extraction. The packet contains only evidence that the actual I3C/I3-flat serializers retain.",
)


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


def stable_key(*values: object) -> str:
    return sha((SEED + "|" + "|".join(str(value) for value in values)).encode())


def length_quartiles(input_rows: list[dict]) -> dict[str, str]:
    ordered = sorted(input_rows, key=lambda row: (len(row["text"].encode()), row["source_sha256"]))
    return {
        row["source_sha256"]: f"Q{min(3, index * 4 // len(ordered)) + 1}"
        for index, row in enumerate(ordered)
    }


def visible_fields(canonical: dict) -> dict[str, list[dict[str, str]]]:
    result = {field: [] for field in FIELD_KEYS}
    status_by_item = {
        (field, item["id"]): item["evidence_status"]
        for field in FIELD_KEYS
        for item in canonical["fields"][field]
    }
    for span in canonical["retained_selector_spans"]:
        result[span["field_key"]].append({
            "id": span["item_id"],
            "evidence": span["evidence"],
            "evidence_status": status_by_item[(span["field_key"], span["item_id"])],
        })
    return result


def sample(population: list[dict]) -> list[dict]:
    selected: list[dict] = []
    for extractor_group in (1, 2, 3):
        for quartile in ("Q1", "Q2", "Q3", "Q4"):
            candidates = sorted(
                (row for row in population if row["extractor_group"] == extractor_group and row["length_quartile"] == quartile),
                key=lambda row: stable_key("initial", extractor_group, quartile, row["skill_id"]),
            )
            require(len(candidates) >= ROWS_PER_GROUP_QUARTILE, f"insufficient V4.1 QA population: {extractor_group}/{quartile}")
            selected.extend(candidates[:ROWS_PER_GROUP_QUARTILE])
    selected_ids = {row["skill_id"] for row in selected}
    protected: list[str] = []
    for field in FIELD_KEYS:
        while sum(field in row["present_fields"] for row in selected) < MIN_PRESENT_PER_FIELD:
            incoming_candidates = sorted(
                (row for row in population if row["skill_id"] not in selected_ids and field in row["present_fields"]),
                key=lambda row: stable_key("field-in", field, row["skill_id"]),
            )
            replacement = None
            for incoming in incoming_candidates:
                outgoing_candidates = [
                    row for row in selected
                    if row["extractor_group"] == incoming["extractor_group"]
                    and row["length_quartile"] == incoming["length_quartile"]
                    and field not in row["present_fields"]
                    and all(
                        prior not in row["present_fields"]
                        or sum(prior in item["present_fields"] for item in selected) > MIN_PRESENT_PER_FIELD
                        for prior in protected
                    )
                ]
                if outgoing_candidates:
                    outgoing = max(outgoing_candidates, key=lambda row: stable_key("field-out", field, row["skill_id"]))
                    replacement = incoming, outgoing
                    break
            require(replacement is not None, f"cannot satisfy frozen V4.1 QA field coverage: {field}")
            incoming, outgoing = replacement
            selected.remove(outgoing)
            selected_ids.remove(outgoing["skill_id"])
            selected.append(incoming)
            selected_ids.add(incoming["skill_id"])
        protected.append(field)
    require(len(selected) == 120 and len(selected_ids) == 120, "V4.1 QA sample coverage mismatch")
    require(Counter(row["extractor_group"] for row in selected) == Counter({1: 40, 2: 40, 3: 40}), "V4.1 QA extractor balance mismatch")
    require(Counter((row["extractor_group"], row["length_quartile"]) for row in selected) == Counter({(group, quartile): 10 for group in (1, 2, 3) for quartile in ("Q1", "Q2", "Q3", "Q4")}), "V4.1 QA quartile balance mismatch")
    require(all(sum(field in row["present_fields"] for row in selected) >= MIN_PRESENT_PER_FIELD for field in FIELD_KEYS), "V4.1 QA field minimum mismatch")
    return selected


def assign_reviewers(selected: list[dict]) -> dict[str, int]:
    by_extractor = {
        group: sorted((row for row in selected if row["extractor_group"] == group), key=lambda row: stable_key("review", row["skill_id"]))
        for group in (1, 2, 3)
    }
    assignment: dict[str, int] = {}
    for row in by_extractor[1][:20]:
        assignment[row["skill_id"]] = 2
    for row in by_extractor[1][20:]:
        assignment[row["skill_id"]] = 3
    for row in by_extractor[2][:20]:
        assignment[row["skill_id"]] = 1
    for row in by_extractor[2][20:]:
        assignment[row["skill_id"]] = 3
    for row in by_extractor[3][:20]:
        assignment[row["skill_id"]] = 1
    for row in by_extractor[3][20:]:
        assignment[row["skill_id"]] = 2
    require(Counter(assignment.values()) == Counter({1: 40, 2: 40, 3: 40}), "V4.1 QA reviewer balance mismatch")
    require(all(assignment[row["skill_id"]] != row["extractor_group"] for row in selected), "V4.1 extractor/reviewer self-assignment")
    return assignment


def build() -> dict[str, bytes]:
    merged_manifest_path = ROOT / MERGED / "manifest.json"
    merged_manifest = json.loads(merged_manifest_path.read_bytes())
    require(merged_manifest["state"] == "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", "V4.1 merge is not QA-ready")
    canonical_path = ROOT / MERGED / "canonical_extractions.jsonl"
    canonical = rows(canonical_path.read_bytes())
    require(merged_manifest["artifacts"]["canonical_extractions.jsonl"]["sha256"] == sha(canonical_path.read_bytes()), "V4.1 canonical extraction hash drift")
    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    assignments = rows(assignments_path.read_bytes())
    require(merged_manifest["bindings"]["assignment_manifest_sha256"] == sha(assignments_path.read_bytes()), "V4.1 QA assignment binding drift")
    _, input_payloads = build_inputs()
    input_by_sha, extractor_by_sha = {}, {}
    for assignment in assignments:
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = input_payloads[input_name]
        require(sha(input_data) == assignment["input_sha256"], f"V4.1 QA input hash drift: {assignment['batch_id']}")
        input_rows = rows(input_data)
        require(len(input_rows) == assignment["row_count"], f"V4.1 QA input row mismatch: {assignment['batch_id']}")
        for row in input_rows:
            require(row["source_sha256"] not in input_by_sha, "duplicate V4.1 QA source identity")
            input_by_sha[row["source_sha256"]] = row
            extractor_by_sha[row["source_sha256"]] = assignment["extractor_group"]
    require(len(canonical) == len(input_by_sha) == 3798, "V4.1 QA population mismatch")
    previous_manifest_path = ROOT / PREVIOUS_QA / "manifest.json"
    previous_key_path = ROOT / PREVIOUS_QA / "sampling_key_do_not_give_reviewer.jsonl"
    previous_manifest = json.loads(previous_manifest_path.read_bytes())
    require(previous_manifest["artifacts"]["sampling_key_do_not_give_reviewer.jsonl"]["sha256"] == sha(previous_key_path.read_bytes()), "previous QA sampling-key binding drift")
    previous_sample = {row["source_sha256"] for row in rows(previous_key_path.read_bytes())}
    require(len(previous_sample) == 120, "previous QA sample binding mismatch")
    quartiles = length_quartiles(list(input_by_sha.values()))
    population = []
    for extraction in canonical:
        source_sha = extraction["source_sha256"]
        input_row = input_by_sha[source_sha]
        fields = visible_fields(extraction)
        if source_sha in previous_sample:
            continue
        population.append({
            "source_row_index": extraction["source_row_index"],
            "skill_id": extraction["skill_id"],
            "source_sha256": source_sha,
            "source_path": extraction["source"],
            "source_text": input_row["text"],
            "name": extraction["name"],
            "description": extraction["description"],
            "visible_fields": fields,
            "present_fields": sorted(field for field, items in fields.items() if items),
            "length_quartile": quartiles[source_sha],
            "extractor_group": extractor_by_sha[source_sha],
        })
    require(len(population) == 3678, "V4.1 fresh QA exclusion mismatch")
    selected = sample(population)
    reviewer_groups = assign_reviewers(selected)
    selected.sort(key=lambda row: stable_key("review-id", row["skill_id"]))
    reviewer_rows, key_rows = [], []
    for index, row in enumerate(selected, 1):
        review_id = "V7-I3-V41-QA-" + stable_key("id", row["skill_id"])[:16].upper()
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
            "provenance": "FRESH_FULL_CORPUS_V4_1",
            "length_quartile": row["length_quartile"],
            "present_fields": row["present_fields"],
            "extractor_group": row["extractor_group"],
            "assigned_reviewer_group": reviewer_groups[row["skill_id"]],
        })
    visible_by_id = {row["review_id"]: row for row in reviewer_rows}
    return_schema = json.loads((ROOT / PREVIOUS_QA / "reviewer_return_schema.json").read_bytes())
    return_schema["allOf"] = [{
        "if": {"properties": {"major_error": {"const": True}}, "required": ["major_error"]},
        "then": {"properties": {"affected_fields": {"minItems": 1}}},
    }]
    files: dict[str, bytes] = {
        "blinded_reviewer_packet.jsonl": rows_bytes(reviewer_rows),
        "sampling_key_do_not_give_reviewer.jsonl": rows_bytes(key_rows),
        "reviewer_guidance.md": GUIDANCE.encode(),
        "reviewer_return_schema.json": json_bytes(return_schema),
    }
    for group in (1, 2, 3):
        group_keys = sorted((row for row in key_rows if row["assigned_reviewer_group"] == group), key=lambda row: stable_key("slot", row["review_id"]))
        require(len(group_keys) == 40, f"V4.1 QA reviewer group mismatch: {group}")
        for within_group in (0, 1):
            slot = (group - 1) * 2 + within_group + 1
            subset = group_keys[within_group * 20:(within_group + 1) * 20]
            files[f"review_slots/qa_slot_{slot:02d}.jsonl"] = rows_bytes([visible_by_id[row["review_id"]] for row in subset])
    fixtures, answers = calibration()
    files["calibration_input.jsonl"] = rows_bytes(fixtures)
    files["calibration_answer_key_do_not_give_reviewer.jsonl"] = rows_bytes(answers)
    manifest = {
        "schema_version": "rq2b-v7-i3-full-corpus-v4.1-blinded-qa-v3",
        "state": "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS",
        "formal_execution_ready": False,
        "sample_size": 120,
        "sampling_seed": SEED,
        "previous_sample_excluded": 120,
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
            "previous_qa_manifest_sha256": sha(previous_manifest_path.read_bytes()),
            "previous_sampling_key_sha256": sha(previous_key_path.read_bytes()),
            "assignment_manifest_sha256": sha(assignments_path.read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
    }
    manifest["artifacts"] = {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in files.items()}
    files["manifest.json"] = json_bytes(manifest)
    files["README.md"] = (
        "# V7 I3 full-corpus V4.1.3 blinded QA v4\n\n"
        "This source-only sample excludes all 120 rows used by the failed v2 QA, balances all three extractor groups and four global length quartiles, and cross-assigns every row to a different reviewer group. The v2 calibration and unchanged 5%/zero-critical thresholds are retained.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa_v4.py --verify`.\n"
    ).encode()
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1.3 QA v4 package missing")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        require(actual == set(expected), "V4.1.3 QA v4 file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1.3 QA v4 drift: {name}")
        status = "PASS_V7_I3_V4_1_BLINDED_QA_V3_PACKET_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1.3 QA v4 package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_BLINDED_QA_V3_PACKET_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
