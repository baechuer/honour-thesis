#!/usr/bin/env python3
"""Replay-check the frozen V7 master target-blind readiness package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from materialise_rq2b_nc_phase5_v7_master_target_blind_readiness import OUTPUT, build_master_readiness, validate_no_forbidden_keys
from reconcile_rq2b_nc_phase5_v7_direct_target_blind import build_reconciliation


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    # Replaying the direct source-Git blobs is part of the master check, not a
    # trust-on-first-use shortcut through its previous report.
    build_reconciliation()
    expected_rows, expected_report = build_master_readiness()
    actual_rows = load_jsonl(output / "master_target_blind_group_reconciliation.jsonl")
    actual_report = json.loads((output / "integrity_report.json").read_text(encoding="utf-8"))
    if canonical(actual_rows) != canonical(expected_rows) or canonical(actual_report) != canonical(expected_report):
        raise SystemExit("FAIL_RQ2B_V7_MASTER_TARGET_BLIND_READINESS_REPLAY_MISMATCH")
    validate_no_forbidden_keys(actual_rows)
    if actual_report["scope"]["target_blind_reconciled_groups"] != 1065 or actual_report["scope"]["explicitly_deferred_excluded_groups"] != 1 or actual_report["scope"]["unresolved_or_blocked_groups"] != 0:
        raise SystemExit("FAIL_RQ2B_V7_MASTER_TARGET_BLIND_READINESS_SCOPE_DRIFT")
    print(json.dumps({"status": actual_report["status"], "groups": 1066, "reconciled_groups": 1065, "excluded_groups": 1, "rows_sha256": sha_path(output / "master_target_blind_group_reconciliation.jsonl"), "integrity_sha256": sha_path(output / "integrity_report.json")}, sort_keys=True))


if __name__ == "__main__":
    main()
