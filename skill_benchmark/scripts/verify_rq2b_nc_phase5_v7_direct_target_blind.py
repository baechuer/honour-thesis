#!/usr/bin/env python3
"""Replay-check the frozen V7 direct target-blind reconciliation package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from reconcile_rq2b_nc_phase5_v7_direct_target_blind import OUTPUT, build_reconciliation


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    expected_rows, expected_report = build_reconciliation()
    actual_rows = load_jsonl(output / "target_blind_direct_group_reconciliation.jsonl")
    actual_report = json.loads((output / "integrity_report.json").read_text(encoding="utf-8"))
    if canonical(actual_rows) != canonical(expected_rows) or canonical(actual_report) != canonical(expected_report):
        raise SystemExit("FAIL_V7_DIRECT_RECONCILIATION_REPLAY_MISMATCH")
    forbidden = {"target_id", "target_identity", "gold_label", "retrieval_result", "source_full_skill"}
    for row in actual_rows:
        if forbidden & set(row):
            raise SystemExit("FAIL_V7_DIRECT_RECONCILIATION_BLINDNESS_KEY_DRIFT")
    print(json.dumps({"status": "PASS_V7_DIRECT_TARGET_BLIND_RECONCILIATION_REPLAY", "output_sha256": {"rows": sha_path(output / "target_blind_direct_group_reconciliation.jsonl"), "integrity": sha_path(output / "integrity_report.json")}, "groups": len(actual_rows), "candidates": sum(len(row["candidate_dispositions"]) for row in actual_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
