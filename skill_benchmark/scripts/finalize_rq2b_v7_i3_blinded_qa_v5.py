#!/usr/bin/env python3
"""Validate and freeze the post-class-repair V4.1.4 blinded QA v5."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import finalize_rq2b_v7_i3_blinded_qa_v4 as prior


ROOT = Path(__file__).resolve().parents[2]
PACKET = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v5")
LOCAL_RETURNS = Path("skill_benchmark/cache/rq2b_v7_phase7_i3_qa_2026_09_09_v5/returns")
OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v5")
FAILED_QA = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v4/qa_final_report.json")
REPORT_SCHEMA = "rq2b-v7-i3-full-corpus-v4.1.4-blinded-qa-final-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build(replay: bool) -> dict[str, bytes]:
    prior.PACKET = PACKET
    prior.LOCAL_RETURNS = LOCAL_RETURNS
    prior.OUTPUT = OUTPUT
    prior.FAILED_V2 = FAILED_QA
    payloads = prior.build(replay)
    report = json.loads(payloads["qa_final_report.json"])
    report["schema_version"] = REPORT_SCHEMA
    report["bindings"]["failed_qa_v4_report_sha256"] = report["bindings"].pop("failed_v2_report_sha256")
    report["bindings"]["finalizer_sha256"] = sha(Path(__file__).read_bytes())
    report["boundary"] = "A PASS validates the post-class-repair V4.1.4 source-to-I3 extraction fidelity sample. It is not retrieval performance or evidence for the deferred 20k scale-out."
    payloads["qa_final_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 I3 post-class-repair V4.1.4 blinded QA final v5\n\n"
        f"State: `{report['state']}`. Three cross-assigned reviewer groups each pass the unchanged 8-row calibration and review 40 freshly sampled sources.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa_v5.py --verify`.\n"
    ).encode()
    return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build(args.verify)
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1.4 QA v5 final package missing")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        require(actual == set(expected), "V4.1.4 QA v5 final file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1.4 QA v5 final drift: {name}")
        status = "PASS_V7_I3_V4_1_4_QA_V5_FINAL_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1.4 QA v5 final package")
        for name, data in expected.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        status = "PASS_V7_I3_V4_1_4_QA_V5_FINAL_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
