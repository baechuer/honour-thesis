#!/usr/bin/env python3
"""Replay-check the frozen V7 all-scope target-blind prejoin package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from materialise_rq2b_nc_phase5_v7_all_scope_target_blind_prejoin import OUTPUT, build_prejoin


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    expected_rows, expected_report = build_prejoin()
    rows = load_jsonl(output / "all_scope_target_blind_prejoin_reconciliation.jsonl")
    report = json.loads((output / "integrity_report.json").read_text(encoding="utf-8"))
    if canonical(rows) != canonical(expected_rows) or canonical(report) != canonical(expected_report):
        raise SystemExit("FAIL_V7_ALL_SCOPE_TARGET_BLIND_PREJOIN_REPLAY_MISMATCH")
    if report["counts"]["v7_prompt_groups"] != 1226 or report["counts"]["reconciled_candidate_dispositions"] != 9800:
        raise SystemExit("FAIL_V7_ALL_SCOPE_TARGET_BLIND_PREJOIN_SCOPE_DRIFT")
    print(json.dumps({"status": "PASS_V7_ALL_SCOPE_TARGET_BLIND_PREJOIN_REPLAY", "groups": len(rows), "rows_sha256": sha_path(output / "all_scope_target_blind_prejoin_reconciliation.jsonl"), "integrity_sha256": sha_path(output / "integrity_report.json")}, sort_keys=True))


if __name__ == "__main__":
    main()
