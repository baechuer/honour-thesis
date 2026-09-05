#!/usr/bin/env python3
"""Run Round 37 M0 mechanics and relabel outputs for Round 38 only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build_rq1b_round37_m0_intake import main as build_round37_shape


def argument_path(argv: list[str], name: str) -> Path:
    try:
        return Path(argv[argv.index(name) + 1])
    except (ValueError, IndexError) as error:
        raise SystemExit(f"{name} is required") from error


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    argv = sys.argv[1:]
    exit_code = build_round37_shape()
    raw_path = argument_path(argv, "--raw-output")
    canonical_path = argument_path(argv, "--canonical-output")
    new_root_path = argument_path(argv, "--new-root-output")
    summary_path = argument_path(argv, "--summary")

    for path in (raw_path,):
        rows = read_jsonl(path)
        for row in rows:
            row["discovery_id"] = str(row["discovery_id"]).replace("R37-M0-", "R38-M0-", 1)
        write_jsonl(path, rows)
    for path in (canonical_path, new_root_path):
        rows = read_jsonl(path)
        for row in rows:
            row["round38_source_candidate_id"] = str(row.pop("round37_source_candidate_id")).replace("R37-M0-", "R38-M0-", 1)
        write_jsonl(path, rows)

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["status"] = str(summary["status"]).replace("ROUND37", "ROUND38")
    summary["round37_intake_mechanics_reused_only"] = True
    summary["round"] = "RQ1b cross-source Round 38"
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "raw_discovery_lead_count", "canonical_public_source_count", "new_root_intake_count", "exact_prior_root_exclusion_count", "failures")}, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
