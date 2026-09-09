#!/usr/bin/env python3
"""Validate and freeze the post-V4.1.5 blinded QA v6 returns."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import finalize_rq2b_v7_i3_blinded_qa_v4 as prior


ROOT = Path(__file__).resolve().parents[2]
PACKET = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v6")
LOCAL_RETURNS = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_qa_2026_09_09_v6/returns")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v6")
FAILED_QA = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v5/qa_final_report.json")
REPORT_SCHEMA = "rq2b-v7-i3-full-corpus-v4.1.5-blinded-qa-final-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build(replay: bool) -> dict[str, bytes]:
    failed_data = (ROOT / FAILED_QA).read_bytes()
    failed = json.loads(failed_data)
    require(failed["state"] == "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE", "failed QA v5 state drift")
    require(failed["counts"]["major_error_rows"] == 13 and failed["counts"]["critical_error_rows"] == 0, "failed QA v5 count drift")
    prior.PACKET = PACKET
    prior.LOCAL_RETURNS = LOCAL_RETURNS
    prior.OUTPUT = OUTPUT
    prior.FAILED_V2 = FAILED_QA
    payloads = prior.build(replay)
    report = json.loads(payloads["qa_final_report.json"])
    report["schema_version"] = REPORT_SCHEMA
    report["bindings"]["failed_qa_v5_report_sha256"] = report["bindings"].pop("failed_v2_report_sha256")
    require(report["bindings"]["failed_qa_v5_report_sha256"] == sha(failed_data), "failed QA v5 binding drift")
    report["bindings"]["finalizer_sha256"] = sha(Path(__file__).read_bytes())
    require(report["pass_rule_replay"] == {
        "critical_error_rows": 0,
        "maximum_field_major_error_rate": 0.05,
        "maximum_major_error_rate": 0.05,
        "maximum_major_error_rows": 6,
        "represented_field_minimum_for_threshold": 20,
    }, "QA v6 threshold drift")
    report["boundary"] = "A PASS validates the post-V4.1.5 source-to-I3 extraction fidelity sample. It is not retrieval performance or evidence for the deferred 20k scale-out."
    payloads["qa_final_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 I3 post-V4.1.5 blinded QA final v6\n\n"
        f"State: `{report['state']}`. Failed QA v5 remains preserved and hash-bound. "
        "Three cross-assigned reviewer groups must each pass the unchanged 8-row "
        "calibration and jointly satisfy the unchanged zero-critical/5% rule.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa_v6.py --verify`.\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build(args.verify)
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1.5 QA v6 final package missing")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        require(actual == set(expected), "V4.1.5 QA v6 final file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1.5 QA v6 final drift: {name}")
        status = "PASS_V7_I3_V4_1_5_QA_V6_FINAL_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1.5 QA v6 final package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_5_QA_V6_FINAL_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
