#!/usr/bin/env python3
"""Freeze the prospective V4.1.2 warning-evidence envelope amendment."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_2_warning_evidence_amendment_2026_09_09_v1"
)
FILES = {
    "protocol": Path("skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V4_1.md"),
    "shared_legacy_merger": Path("skill_benchmark/scripts/merge_rq2b_i3c.py"),
    "v4_1_1_validator": Path("skill_benchmark/scripts/validate_rq2b_v7_i3_v4_1_1_batch.py"),
    "v4_1_2_validator": Path("skill_benchmark/scripts/validate_rq2b_v7_i3_v4_1_2_batch.py"),
    "focused_tests": Path("skill_benchmark/scripts/test_validate_rq2b_v7_i3_v4_1_2_batch.py"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build() -> dict[str, bytes]:
    bindings = {}
    for role, relative in FILES.items():
        path = ROOT / relative
        require(path.is_file(), f"missing amendment input: {relative}")
        bindings[role] = {"path": str(relative), "sha256": sha(path)}
    report = {
        "schema_version": "rq2b-v7-i3-v4.1.2-warning-evidence-amendment-v1",
        "state": "PASS_PROSPECTIVE_QA_ONLY_SCHEMA_ENVELOPE_AMENDMENT",
        "effective_before_selector_execution": True,
        "retrieval_or_reranking_runs": 0,
        "provider_calls": 0,
        "change": {
            "old_warning_evidence_rule": "string length <= 500 and empty or exact source substring",
            "new_warning_evidence_rule": "empty or exact contiguous substring of the same frozen source",
            "warning_message_limit_unchanged": 500,
            "field_item_evidence_contract_unchanged": True,
            "representation_serialization_unchanged": True,
            "source_prompt_target_and_label_scope_unchanged": True,
        },
        "rationale": (
            "The frozen V4.1 extraction protocol already permits warning evidence to be empty or an exact source "
            "substring. Eight reviewed repairs require complete exact spans of 547-761 characters; truncation would "
            "contradict the source-only exact-and-complete gate. Exact substring membership bounds evidence by the "
            "frozen source itself, so the unrelated 500-character legacy limit is removed only for warning metadata."
        ),
        "bindings": bindings,
        "boundary": (
            "This amendment cannot change extracted field items or selector-visible text and creates no quality PASS, "
            "experiment authority, retrieval result, metric, target join, or thesis result. Historical V4.1/V4.1.1 "
            "outputs and audits remain immutable. Repairs require traceable reissue and fresh warning disposition."
        ),
    }
    return {
        "integrity_report.json": json_bytes(report),
        "README.md": (
            "# V7 I3 V4.1.2 warning-evidence amendment\n\n"
            "This prospective, pre-experiment amendment removes only the legacy 500-character cap from warning "
            "citations. A citation must still be empty or an exact contiguous substring of the same frozen source. "
            "The 500-character warning-message cap and every field-item, identity, polarity and source-only rule are "
            "unchanged. Warning metadata is not part of I3C or I3-flat selector text.\n\n"
            "Historical outputs are not overwritten. Any repaired row must be a traceable reissue, revalidated under "
            "V4.1.2 and re-enter a new warning-audit version. This package authorises no selector execution.\n\n"
            "Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_v4_1_2_warning_evidence_amendment.py --verify`.\n"
            "Tests: `python3 -B skill_benchmark/scripts/test_validate_rq2b_v7_i3_v4_1_2_batch.py`.\n"
        ).encode(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    output = ROOT / OUTPUT
    if args.verify:
        require(output.is_dir(), "amendment package missing")
        require({path.name for path in output.iterdir() if path.is_file()} == set(expected), "amendment file-set drift")
        for name, data in expected.items():
            require((output / name).read_bytes() == data, f"amendment artifact drift: {name}")
        status = "PASS_V7_I3_V4_1_2_WARNING_EVIDENCE_AMENDMENT_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite amendment package")
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale amendment staging directory")
        staging.mkdir(parents=True)
        for name, data in expected.items():
            (staging / name).write_bytes(data)
        staging.rename(output)
        status = "PASS_V7_I3_V4_1_2_WARNING_EVIDENCE_AMENDMENT_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
