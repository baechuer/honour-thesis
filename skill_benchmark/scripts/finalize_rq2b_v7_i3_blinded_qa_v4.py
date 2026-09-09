#!/usr/bin/env python3
"""Validate and freeze full-corpus V4.1.3 blinded extraction-fidelity QA v4."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from merge_rq2b_i3c import FIELD_KEYS


ROOT = Path(__file__).resolve().parents[2]
PACKET = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v4")
LOCAL_RETURNS = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_qa_2026_09_09_v4/returns")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v4")
FAILED_V2 = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v2/qa_final_report.json")
CRITICAL_CODES = {"EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING", "BENCHMARK_OR_ROUTING_LEAKAGE"}
MAJOR_CODES = {"WRONG_OPERATIONAL_FIELD", "MISSING_SELECTION_CRITICAL_CONTENT", "NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN", "BOUNDARY_POLARITY_MISCLASSIFIED"}
ALLOWED_KEYS = {"review_id", "review_status", "critical_error", "major_error", "affected_fields", "error_codes", "reviewer_notes", "reviewer_group"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def rows_bytes(values: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in values).encode()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def validate_return(row: dict, group: int) -> None:
    require(set(row) == ALLOWED_KEYS, f"V4.1 QA return key mismatch: {row.get('review_id')}")
    require(row["review_status"] == "COMPLETE" and row["reviewer_group"] == group, f"V4.1 QA return state/group mismatch: {row['review_id']}")
    require(isinstance(row["critical_error"], bool) and isinstance(row["major_error"], bool), f"V4.1 QA invalid severity: {row['review_id']}")
    require(not (row["critical_error"] and row["major_error"]), f"V4.1 QA nonexclusive severity: {row['review_id']}")
    fields, codes = row["affected_fields"], row["error_codes"]
    require(isinstance(fields, list) and len(fields) == len(set(fields)) and set(fields) <= set(FIELD_KEYS), f"V4.1 QA invalid affected fields: {row['review_id']}")
    require(isinstance(codes, list) and len(codes) == len(set(codes)) and set(codes) <= CRITICAL_CODES | MAJOR_CODES, f"V4.1 QA invalid codes: {row['review_id']}")
    require(isinstance(row["reviewer_notes"], str) and row["reviewer_notes"].strip(), f"V4.1 QA missing notes: {row['review_id']}")
    if row["critical_error"]:
        require(bool(codes) and set(codes) <= CRITICAL_CODES, f"V4.1 QA critical-code mismatch: {row['review_id']}")
    elif row["major_error"]:
        require(bool(codes) and set(codes) <= MAJOR_CODES and bool(fields), f"V4.1 QA major-code/field mismatch: {row['review_id']}")
    else:
        require(not fields and not codes, f"V4.1 QA clean row contains errors: {row['review_id']}")


def source_path(replay: bool, name: str) -> Path:
    return ROOT / (OUTPUT / "reviewer_returns" / name if replay else LOCAL_RETURNS / name)


def build(replay: bool) -> dict[str, bytes]:
    manifest_path = ROOT / PACKET / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes())
    require(manifest["state"] == "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS", "V4.1 QA packet state mismatch")
    require(manifest["sample_size"] == 120 and manifest["review_slots"] == 6 and manifest["rows_per_slot"] == 20 and manifest["calibration_rows"] == 8, "V4.1 QA packet cardinality contract drift")
    require(manifest["pass_rule"]["critical_error_rows"] == 0 and manifest["pass_rule"]["maximum_major_error_rows"] == 6 and manifest["pass_rule"]["maximum_major_error_rate"] == 0.05, "V4.1 QA packet pass-rule drift")
    for name, artifact in manifest["artifacts"].items():
        path = ROOT / PACKET / name
        data = path.read_bytes()
        require(sha(data) == artifact["sha256"], f"V4.1 QA packet artifact hash drift: {name}")
        require(len(data.splitlines()) == artifact["rows"], f"V4.1 QA packet artifact row drift: {name}")
    key_path = ROOT / PACKET / "sampling_key_do_not_give_reviewer.jsonl"
    key_rows = rows(key_path)
    key_by_id = {row["review_id"]: row for row in key_rows}
    require(len(key_rows) == len(key_by_id) == 120, "V4.1 QA sampling-key mismatch")
    require(manifest["artifacts"]["sampling_key_do_not_give_reviewer.jsonl"]["sha256"] == sha(key_path.read_bytes()), "V4.1 QA sampling-key hash drift")
    calibration_answers = {row["review_id"]: row for row in rows(ROOT / PACKET / "calibration_answer_key_do_not_give_reviewer.jsonl")}
    require(len(calibration_answers) == 8, "V4.1 QA calibration-key mismatch")
    payloads: dict[str, bytes] = {}
    calibration_status = {}
    for group in (1, 2, 3):
        name = f"calibration_group_{group}.jsonl"
        values = rows(source_path(replay, name))
        require(len(values) == 8 and {row["review_id"] for row in values} == set(calibration_answers), f"V4.1 QA calibration coverage mismatch: {group}")
        for row in values:
            validate_return(row, group)
            expected = calibration_answers[row["review_id"]]
            for key in ("critical_error", "major_error", "affected_fields", "error_codes"):
                require(row[key] == expected[key], f"V4.1 QA calibration decision mismatch: {group}/{row['review_id']}/{key}")
        data = rows_bytes(values)
        payloads[f"reviewer_returns/{name}"] = data
        calibration_status[str(group)] = "PASS_EXACT_8_OF_8"
    all_returns = []
    for slot in range(1, 7):
        group = (slot - 1) // 2 + 1
        name = f"qa_slot_{slot:02d}_return.jsonl"
        values = rows(source_path(replay, name))
        assigned = rows(ROOT / PACKET / f"review_slots/qa_slot_{slot:02d}.jsonl")
        require(len(values) == len(assigned) == 20, f"V4.1 QA slot row mismatch: {slot}")
        require([row["review_id"] for row in values] == [row["review_id"] for row in assigned], f"V4.1 QA slot order mismatch: {slot}")
        for row in values:
            validate_return(row, group)
            key = key_by_id[row["review_id"]]
            require(key["assigned_reviewer_group"] == group and key["extractor_group"] != group, f"V4.1 QA cross-assignment mismatch: {row['review_id']}")
        data = rows_bytes(values)
        payloads[f"reviewer_returns/{name}"] = data
        all_returns.extend(values)
    require(len(all_returns) == len({row["review_id"] for row in all_returns}) == 120, "V4.1 QA return coverage mismatch")
    critical = [row for row in all_returns if row["critical_error"]]
    major = [row for row in all_returns if row["major_error"]]
    denominators = Counter()
    field_major = Counter()
    for key in key_rows:
        for field in key["present_fields"]:
            denominators[field] += 1
    for row in major:
        for field in row["affected_fields"]:
            field_major[field] += 1
            if field not in key_by_id[row["review_id"]]["present_fields"]:
                denominators[field] += 1
    field_rates = {
        field: {
            "represented_or_missing_error_rows": denominators[field],
            "major_error_rows": field_major[field],
            "major_error_rate": field_major[field] / denominators[field] if denominators[field] else None,
            "threshold_applies": denominators[field] >= 20,
        }
        for field in FIELD_KEYS
    }
    passed = len(critical) == 0 and len(major) <= 6 and all(not row["threshold_applies"] or row["major_error_rate"] <= 0.05 for row in field_rates.values())
    errors = [*critical, *major]
    error_details = [{
        "review_id": row["review_id"],
        "source_sha256": key_by_id[row["review_id"]]["source_sha256"],
        "source_path": key_by_id[row["review_id"]]["source_path"],
        "length_quartile": key_by_id[row["review_id"]]["length_quartile"],
        "extractor_group": key_by_id[row["review_id"]]["extractor_group"],
        "reviewer_group": row["reviewer_group"],
        "critical_error": row["critical_error"],
        "major_error": row["major_error"],
        "affected_fields": row["affected_fields"],
        "error_codes": row["error_codes"],
    } for row in sorted(errors, key=lambda item: item["review_id"])]
    failed_v2 = json.loads((ROOT / FAILED_V2).read_bytes())
    require(failed_v2["state"] == "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE" and not failed_v2["formal_execution_ready"], "failed v2 disposition drift")
    report = {
        "schema_version": "rq2b-v7-i3-full-corpus-v4.1-blinded-qa-final-v3",
        "state": "PASS_CURRENT_I1_I3_SEMANTIC_QA" if passed else "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE",
        "formal_execution_ready": passed,
        "sample_size": 120,
        "calibration": calibration_status,
        "counts": {
            "critical_error_rows": len(critical),
            "major_error_rows": len(major),
            "clean_rows": 120 - len(critical) - len(major),
            "errors_by_extractor_group": dict(sorted(Counter(str(key_by_id[row["review_id"]]["extractor_group"]) for row in errors).items())),
            "errors_by_reviewer_group": dict(sorted(Counter(str(row["reviewer_group"]) for row in errors).items())),
            "errors_by_length_quartile": dict(sorted(Counter(key_by_id[row["review_id"]]["length_quartile"] for row in errors).items())),
            "error_codes": dict(sorted(Counter(code for row in all_returns for code in row["error_codes"]).items())),
        },
        "major_error_rate": len(major) / 120,
        "field_strata": field_rates,
        "pass_rule_replay": {
            "critical_error_rows": 0,
            "maximum_major_error_rows": 6,
            "maximum_major_error_rate": 0.05,
            "represented_field_minimum_for_threshold": 20,
            "maximum_field_major_error_rate": 0.05,
        },
        "bindings": {
            "qa_packet_manifest_sha256": sha(manifest_path.read_bytes()),
            "sampling_key_sha256": sha(key_path.read_bytes()),
            "failed_v2_report_sha256": sha((ROOT / FAILED_V2).read_bytes()),
            "finalizer_sha256": sha(Path(__file__).read_bytes()),
        },
        "error_review_ids": [row["review_id"] for row in error_details],
        "error_details": error_details,
        "failure_rule": None if passed else "Do not patch sampled rows only. Repair the entire affected rule/class, rebuild representations, and draw another fresh source-only sample.",
        "boundary": "A PASS validates V7 source-to-I1/I3 extraction fidelity at the frozen sampled gate. It is not retrieval performance or evidence for the future 20k scale-out.",
    }
    report["reviewer_return_artifacts"] = {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in payloads.items()}
    payloads["qa_final_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 I3 full-corpus V4.1.3 blinded QA final v4\n\n"
        f"State: `{report['state']}`. Three cross-assigned reviewer groups each passed the unchanged 8-row calibration and reviewed 40 freshly sampled sources.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa_v4.py --verify`.\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build(args.verify)
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1 QA final package missing")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        require(actual == set(expected), "V4.1 QA final file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1 QA final drift: {name}")
        status = "PASS_V7_I3_V4_1_BLINDED_QA_V3_FINAL_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1 QA final package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_BLINDED_QA_V3_FINAL_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
