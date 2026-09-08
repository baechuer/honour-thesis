#!/usr/bin/env python3
"""Validate and freeze the three-group V7 blinded extraction-fidelity QA."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from build_rq2b_v7_i3_blinded_qa import FIELD_KEYS, OUTPUT as QA_PACKET


ROOT = Path(__file__).resolve().parents[2]
LOCAL_RETURNS = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_qa_2026_09_08_v1/returns")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_08_v1")
CRITICAL_CODES = {"EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING", "BENCHMARK_OR_ROUTING_LEAKAGE"}
MAJOR_CODES = {"WRONG_OPERATIONAL_FIELD", "MISSING_SELECTION_CRITICAL_CONTENT", "NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN", "BOUNDARY_POLARITY_MISCLASSIFIED"}
ALLOWED_KEYS = {"review_id", "review_status", "critical_error", "major_error", "affected_fields", "error_codes", "reviewer_notes", "reviewer_group"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def validate_return(row: dict[str, Any], *, expected_group: int) -> None:
    require(set(row) == ALLOWED_KEYS, f"review return key mismatch: {row.get('review_id')}")
    require(row["review_status"] == "COMPLETE", f"review incomplete: {row['review_id']}")
    require(row["reviewer_group"] == expected_group, f"reviewer group mismatch: {row['review_id']}")
    require(isinstance(row["critical_error"], bool) and isinstance(row["major_error"], bool), f"invalid severity: {row['review_id']}")
    require(not (row["critical_error"] and row["major_error"]), f"critical/major not exclusive: {row['review_id']}")
    fields = row["affected_fields"]
    codes = row["error_codes"]
    require(isinstance(fields, list) and len(fields) == len(set(fields)) and set(fields) <= set(FIELD_KEYS), f"invalid affected fields: {row['review_id']}")
    require(isinstance(codes, list) and len(codes) == len(set(codes)) and set(codes) <= CRITICAL_CODES | MAJOR_CODES, f"invalid error codes: {row['review_id']}")
    require(isinstance(row["reviewer_notes"], str) and row["reviewer_notes"].strip(), f"review notes missing: {row['review_id']}")
    if row["critical_error"]:
        require(bool(codes) and set(codes) <= CRITICAL_CODES, f"critical code mismatch: {row['review_id']}")
    elif row["major_error"]:
        require(bool(codes) and set(codes) <= MAJOR_CODES, f"major code mismatch: {row['review_id']}")
    else:
        require(not fields and not codes, f"clean row contains errors: {row['review_id']}")


def source_return_path(replay: bool, name: str) -> Path:
    return ROOT / (OUTPUT / "reviewer_returns" / name if replay else LOCAL_RETURNS / name)


def build(replay: bool) -> dict[str, bytes]:
    qa_manifest_path = ROOT / QA_PACKET / "manifest.json"
    qa_manifest = json.loads(qa_manifest_path.read_bytes())
    require(qa_manifest["state"] == "FROZEN_PENDING_THREE_CROSS_ASSIGNED_REVIEWER_GROUPS", "QA packet state mismatch")
    key_rows = read_rows(ROOT / QA_PACKET / "sampling_key_do_not_give_reviewer.jsonl")
    key_by_id = {row["review_id"]: row for row in key_rows}
    require(len(key_by_id) == len(key_rows) == 120, "QA sampling key mismatch")
    calibration_answers = {row["review_id"]: row for row in read_rows(ROOT / QA_PACKET / "calibration_answer_key_do_not_give_reviewer.jsonl")}
    require(len(calibration_answers) == 8, "QA calibration key mismatch")

    payloads: dict[str, bytes] = {}
    calibration_status = {}
    for group in (1, 2, 3):
        name = f"calibration_group_{group}.jsonl"
        rows = read_rows(source_return_path(replay, name))
        require(len(rows) == 8 and {row["review_id"] for row in rows} == set(calibration_answers), f"calibration coverage mismatch: group {group}")
        for row in rows:
            validate_return(row, expected_group=group)
            expected = calibration_answers[row["review_id"]]
            for key in ("critical_error", "major_error", "affected_fields", "error_codes"):
                require(row[key] == expected[key], f"calibration decision mismatch: group {group}/{row['review_id']}/{key}")
        data = rows_bytes(rows)
        payloads[f"reviewer_returns/{name}"] = data
        calibration_status[str(group)] = "PASS_EXACT_8_OF_8"

    all_sample_returns = []
    for slot in range(1, 7):
        group = (slot - 1) // 2 + 1
        name = f"qa_slot_{slot:02d}_return.jsonl"
        rows = read_rows(source_return_path(replay, name))
        assigned = read_rows(ROOT / QA_PACKET / f"review_slots/qa_slot_{slot:02d}.jsonl")
        require(len(rows) == len(assigned) == 20, f"QA slot row count mismatch: {slot}")
        require([row["review_id"] for row in rows] == [row["review_id"] for row in assigned], f"QA slot order/coverage mismatch: {slot}")
        for row in rows:
            validate_return(row, expected_group=group)
            require(key_by_id[row["review_id"]]["assigned_reviewer_group"] == group, f"QA cross-assignment mismatch: {row['review_id']}")
            if key_by_id[row["review_id"]]["provenance"] == "FRESH":
                require(key_by_id[row["review_id"]]["extractor_group"] != group, f"extractor reviewed own fresh row: {row['review_id']}")
        data = rows_bytes(rows)
        payloads[f"reviewer_returns/{name}"] = data
        all_sample_returns.extend(rows)
    require(len(all_sample_returns) == 120 and len({row["review_id"] for row in all_sample_returns}) == 120, "QA return coverage mismatch")

    critical_rows = [row for row in all_sample_returns if row["critical_error"]]
    major_rows = [row for row in all_sample_returns if row["major_error"]]
    field_denominators = Counter()
    field_major = Counter()
    for review_id, key in key_by_id.items():
        for field in key["present_fields"]:
            field_denominators[field] += 1
    for row in major_rows:
        for field in row["affected_fields"]:
            field_major[field] += 1
            if field not in key_by_id[row["review_id"]]["present_fields"]:
                field_denominators[field] += 1
    field_rates = {
        field: {
            "represented_or_missing_error_rows": field_denominators[field],
            "major_error_rows": field_major[field],
            "major_error_rate": field_major[field] / field_denominators[field] if field_denominators[field] else None,
            "threshold_applies": field_denominators[field] >= 20,
        }
        for field in FIELD_KEYS
    }
    overall_pass = len(critical_rows) == 0 and len(major_rows) <= 6
    field_pass = all(not row["threshold_applies"] or row["major_error_rate"] <= 0.05 for row in field_rates.values())
    passed = overall_pass and field_pass
    report = {
        "schema_version": "rq2b-v7-i3-blinded-qa-final-v1",
        "state": "PASS_CURRENT_I1_I3_SEMANTIC_QA" if passed else "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE",
        "formal_execution_ready": passed,
        "sample_size": 120,
        "calibration": calibration_status,
        "counts": {
            "critical_error_rows": len(critical_rows),
            "major_error_rows": len(major_rows),
            "clean_rows": 120 - len(critical_rows) - len(major_rows),
            "provenance": dict(sorted(Counter(key_by_id[row["review_id"]]["provenance"] for row in all_sample_returns).items())),
            "reviewer_group": dict(sorted(Counter(str(row["reviewer_group"]) for row in all_sample_returns).items())),
            "error_codes": dict(sorted(Counter(code for row in all_sample_returns for code in row["error_codes"]).items())),
        },
        "major_error_rate": len(major_rows) / 120,
        "field_strata": field_rates,
        "pass_rule_replay": {
            "critical_error_rows": 0,
            "maximum_major_error_rows": 6,
            "maximum_major_error_rate": 0.05,
            "represented_field_minimum_for_threshold": 20,
            "maximum_field_major_error_rate": 0.05,
        },
        "bindings": {
            "qa_packet_manifest_sha256": sha(qa_manifest_path.read_bytes()),
            "sampling_key_sha256": sha((ROOT / QA_PACKET / "sampling_key_do_not_give_reviewer.jsonl").read_bytes()),
            "finalizer_sha256": sha(Path(__file__).read_bytes()),
        },
        "error_review_ids": sorted(row["review_id"] for row in [*critical_rows, *major_rows]),
        "boundary": "A PASS covers current V7 source-to-I1/I3 extraction fidelity at the frozen sampled QA gate. It is not retrieval performance and does not validate unreviewed benchmark labels.",
    }
    report["reviewer_return_artifacts"] = {name: {"sha256": sha(data), "rows": len(data.splitlines())} for name, data in payloads.items()}
    payloads["qa_final_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 Phase-7 blinded I1/I3 QA final\n\n"
        f"State: `{report['state']}`. Three cross-assigned reviewer groups each passed the frozen 8-row calibration and reviewed two 20-row slots. "
        "All returns are preserved here. A failure cannot be repaired only in sampled rows; the affected extraction class must be repaired corpus-wide and a new sample frozen.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa.py --verify`\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build(args.verify)
    output = ROOT / OUTPUT
    if args.verify:
        require(output.is_dir(), "V7 I3 QA final package is missing")
        actual_files = {path.relative_to(output) for path in output.rglob("*") if path.is_file()}
        require(actual_files == {Path(name) for name in expected}, "V7 I3 QA final file-set drift")
        for name, data in expected.items():
            require((output / name).read_bytes() == data, f"V7 I3 QA final artifact drift: {name}")
        status = "PASS_V7_I3_QA_FINAL_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite versioned V7 I3 QA final package")
        for name, data in expected.items():
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_QA_FINAL_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
