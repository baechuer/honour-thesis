#!/usr/bin/env python3
"""Freeze the pre-selection V4.1.1 unsupported-label validator amendment."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from validate_rq2b_v7_i3_v4_1_1_batch import ROOT


OUTPUT = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_1_validator_amendment_2026_09_09_v1")
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_full_reextraction_2026_09_09_v4_1")
OLD_VALIDATOR = Path("skill_benchmark/scripts/validate_rq2b_v7_i3_v4_1_batch.py")
NEW_VALIDATOR = Path("skill_benchmark/scripts/validate_rq2b_v7_i3_v4_1_1_batch.py")
TEST = Path("skill_benchmark/scripts/test_validate_rq2b_v7_i3_v4_1_1_batch.py")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build() -> dict[str, bytes]:
    report = {
        "schema_version": "rq2b-v7-i3-v4.1.1-validator-amendment-v1",
        "state": "PASS_PRE_SELECTION_POLARITY_FALSE_POSITIVE_CORRECTED",
        "formal_execution_ready": False,
        "timing": "AFTER_8_BATCH_ATTEMPTS_BUT_BEFORE_OUTPUT_SELECTION_MERGE_QA_OR_ANY_SELECTOR",
        "trigger": {
            "batch_id": "I3V41-011",
            "skill_id": "sha256-1b8cd55898987267356d9911f96100a778c181668dad6528f307f05c945bb8d5",
            "evidence": "- The task is a support check: decide whether the wording is supported, overstated, partially supported, or unsupported.",
            "v4_1_disposition": "FALSE_POSITIVE_REJECTED_STANDALONE_UNSUPPORTED_OUTCOME_LABEL",
            "v4_1_1_disposition": "PASS_POSITIVE_USE_CONDITION",
        },
        "change": "Standalone unsupported is no longer sufficient for an automatic use-condition polarity rejection. Explicit do-not-use/not-for/does-not-support language and unsupported object/platform/input constructions remain rejected.",
        "unchanged": [
            "3,798 source bytes and identities",
            "95 batch membership and extractor groups",
            "V4.1 source-only instruction and seven fields",
            "all existing worker output bytes",
            "V7 prompts, candidates, K=6 packets, tails and acceptable sets",
            "fresh 120-row QA thresholds",
        ],
        "replay_policy": "Every original and reissue attempt, including the I3V41-011 original, is replayed under V4.1.1 before mechanical output selection.",
        "bindings": {
            "v4_1_preparation_report_sha256": sha((ROOT / PREP / "preparation_report.json").read_bytes()),
            "v4_1_validator_sha256": sha((ROOT / OLD_VALIDATOR).read_bytes()),
            "v4_1_1_validator_sha256": sha((ROOT / NEW_VALIDATOR).read_bytes()),
            "v4_1_1_test_sha256": sha((ROOT / TEST).read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "validation": {
            "focused_tests": "PASS_3_OF_3",
            "i3v41_011_replay": "PASS_I3_V4_1_1_BATCH_VALIDATION",
            "selector_or_provider_calls": 0,
        },
    }
    return {
        "integrity_report.json": json_bytes(report),
        "README.md": (
            "# V7 I3 V4.1.1 validator amendment\n\n"
            "V4.1 incorrectly treated the word `unsupported` as a route-out even when a skill legitimately returns `unsupported` as one possible assessment label. Before output selection, merge, QA or selector execution, V4.1.1 narrows only that automatic guard. It preserves the original output and replays every attempt under the corrected validator.\n\n"
            "Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_v4_1_1_validator_amendment.py --verify`. Focused tests: `python3 -B skill_benchmark/scripts/test_validate_rq2b_v7_i3_v4_1_1_batch.py`.\n"
        ).encode(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    root = ROOT / OUTPUT
    if args.verify:
        require(root.is_dir(), "V4.1.1 validator amendment missing")
        require({path.name for path in root.iterdir()} == set(expected), "V4.1.1 amendment file-set drift")
        for name, data in expected.items():
            require((root / name).read_bytes() == data, f"V4.1.1 amendment drift: {name}")
        status = "PASS_V7_I3_V4_1_1_VALIDATOR_AMENDMENT_REPLAY"
    else:
        require(not root.exists(), "refusing to overwrite V4.1.1 validator amendment")
        root.mkdir(parents=True)
        for name, data in expected.items():
            (root / name).write_bytes(data)
        status = "PASS_V7_I3_V4_1_1_VALIDATOR_AMENDMENT_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
