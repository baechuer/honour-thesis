#!/usr/bin/env python3
"""Preserve and disposition the invalid v1 I3 QA calibration attempt."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation"
PACKET = PREP / "v7_phase7_i3_blinded_qa_2026_09_08_v1"
RETURNS = ROOT / "skill_benchmark/cache/rq2b_v7_phase7_i3_qa_2026_09_08_v1/returns"
OUTPUT = PREP / "v7_phase7_i3_qa_v1_calibration_disposition_2026_09_09_v1"
RETURN_NAMES = tuple(
    [f"calibration_group_{group}.jsonl" for group in (1, 2, 3)]
    + [f"qa_slot_{slot:02d}_return.jsonl" for slot in range(1, 7)]
)
DECISION_KEYS = ("critical_error", "major_error", "affected_fields", "error_codes")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def build() -> dict[str, bytes]:
    packet_manifest_path = PACKET / "manifest.json"
    manifest = json.loads(packet_manifest_path.read_bytes())
    require(manifest["schema_version"] == "rq2b-v7-i3-blinded-qa-packet-v1", "v1 QA manifest drift")
    files: dict[str, bytes] = {}
    for name in RETURN_NAMES:
        data = (RETURNS / name).read_bytes()
        expected_rows = 8 if name.startswith("calibration") else 20
        require(len(data.splitlines()) == expected_rows, f"v1 return row count drift: {name}")
        files[f"rejected_reviewer_returns/{name}"] = data

    answers = {row["review_id"]: row for row in read_rows(PACKET / "calibration_answer_key_do_not_give_reviewer.jsonl")}
    mismatches: list[dict[str, Any]] = []
    by_group: dict[str, int] = {}
    for group in (1, 2, 3):
        rows = read_rows(RETURNS / f"calibration_group_{group}.jsonl")
        count = 0
        for row in rows:
            expected = answers[row["review_id"]]
            differing = [key for key in DECISION_KEYS if row[key] != expected[key]]
            if differing:
                count += 1
                mismatches.append({
                    "reviewer_group": group,
                    "review_id": row["review_id"],
                    "differing_keys": differing,
                    "observed": {key: row[key] for key in DECISION_KEYS},
                    "answer_key": {key: expected[key] for key in DECISION_KEYS},
                })
        by_group[str(group)] = count
    require(all(value > 0 for value in by_group.values()), "expected every v1 reviewer group to fail exact calibration")
    report = {
        "schema_version": "rq2b-v7-i3-qa-v1-calibration-disposition-v1",
        "state": "INVALID_CALIBRATION_INSTRUMENT_AND_REVIEWER_RETURNS_NOT_ACCEPTED",
        "formal_execution_ready": False,
        "threshold_changed": False,
        "raw_returns_overwritten": False,
        "calibration_mismatch_rows_by_group": by_group,
        "mismatches": mismatches,
        "instrument_findings": [
            "CAL-001 omits an explicit output while the v1 guidance permits MISSING_SELECTION_CRITICAL_CONTENT, yet the answer key marks the row clean.",
            "CAL-002 includes a second omitted output fact, so the fixture does not isolate WRONG_OPERATIONAL_FIELD.",
            "CAL-006 omits a use/boundary fact but the answer key names workflow_steps as the affected field.",
            "CAL-007 does not define whether a non-self-contained fragment also receives the missing-content code.",
            "V1 guidance never defines whether affected_fields names the defective origin, intended destination, or both.",
            "All three fresh reviewer contexts independently produced the same core calibration disagreements.",
        ],
        "disposition": {
            "v1_sample_returns": "PRESERVED_REJECTED_NOT_USED_FOR_QA_ESTIMATE",
            "next_instrument": "v7_phase7_i3_blinded_qa_2026_09_09_v2",
            "next_sample": "byte-identical v1 sample with fresh reviewer contexts; no benchmark outcome exposure occurred",
        },
        "bindings": {
            "v1_packet_manifest_sha256": sha(packet_manifest_path.read_bytes()),
            "v1_calibration_input_sha256": sha((PACKET / "calibration_input.jsonl").read_bytes()),
            "v1_calibration_answer_key_sha256": sha((PACKET / "calibration_answer_key_do_not_give_reviewer.jsonl").read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "preserved_returns": {
            name: {"sha256": sha(data), "rows": len(data.splitlines())}
            for name, data in files.items()
        },
    }
    files["disposition_report.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 I3 QA v1 calibration disposition\n\n"
        "State: `INVALID_CALIBRATION_INSTRUMENT_AND_REVIEWER_RETURNS_NOT_ACCEPTED`. All raw v1 calibration and sample returns are preserved here byte-for-byte, but none is selected as semantic-QA evidence. The v1 scientific threshold is not relaxed. A v2 instrument isolates each synthetic defect, defines code precedence and `affected_fields`, and requires fresh reviewer contexts.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_qa_v1_calibration_disposition.py --verify`.\n"
    ).encode()
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.verify:
        require(OUTPUT.is_dir(), "v1 QA calibration disposition package missing")
        actual = {path.relative_to(OUTPUT) for path in OUTPUT.rglob("*") if path.is_file()}
        require(actual == {Path(name) for name in expected}, "v1 disposition file-set drift")
        for name, data in expected.items():
            require((OUTPUT / name).read_bytes() == data, f"v1 disposition artifact drift: {name}")
        status = "PASS_V7_I3_QA_V1_CALIBRATION_DISPOSITION_REPLAY"
    else:
        require(not OUTPUT.exists(), "refusing to overwrite v1 calibration disposition package")
        for name, data in expected.items():
            path = OUTPUT / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_QA_V1_CALIBRATION_DISPOSITION_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT.relative_to(ROOT))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
