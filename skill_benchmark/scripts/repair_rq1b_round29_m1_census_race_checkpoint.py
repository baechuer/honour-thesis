#!/usr/bin/env python3
"""Quarantine Round 29 local-cache race records before a tree-only resume.

This repair never contacts a remote.  It removes a failed checkpoint row only
when a local Git directory now proves that the exact pinned commit was already
fetched and the recorded failure was a missing-FETCH_HEAD race.  The original
checkpoint remains untouched for audit.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


FAILED = "M1_TREE_CENSUS_FAILED_NOT_ADMITTED_NOT_A_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run(command: list[str]) -> str:
    return subprocess.run(command, check=True, text=True, capture_output=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--temp-root", type=Path, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    sources = {position: source for position, source in enumerate(plan["sources"], start=1)}
    rows = read_jsonl(args.checkpoint)
    kept: list[dict[str, Any]] = []
    repaired: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    for row in rows:
        position = int(row["plan_position"])
        source = sources.get(position)
        error = str(row.get("error", ""))
        eligible = row.get("tree_census_status") == FAILED and "rev-parse', 'FETCH_HEAD'" in error
        if not eligible or source is None:
            kept.append(row)
            continue
        target = args.temp_root / str(source["origin"]).replace("/", "--")
        try:
            actual_url = run(["git", "-C", str(target), "remote", "get-url", "origin"])
            actual_head = run(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"])
        except Exception as exc:
            kept.append(row)
            blocked.append({"plan_position": position, "origin": source["origin"], "reason": f"local_proof_failed:{type(exc).__name__}"})
            continue
        if actual_url != str(source["repository_url"]) or actual_head != str(source["pinned_commit"]):
            kept.append(row)
            blocked.append({"plan_position": position, "origin": source["origin"], "reason": "local_origin_or_head_mismatch"})
            continue
        repaired.append({
            "plan_position": position,
            "origin": source["origin"],
            "repository_url": actual_url,
            "pinned_commit": actual_head,
            "removed_from_resume_checkpoint_reason": "local_cache_race_proved_after_missing_FETCH_HEAD_failure",
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in kept), encoding="utf-8")
    payload = {
        "status": "M1_ROUND29_LOCAL_CACHE_RACE_QUARANTINED_NOT_A_SOURCE_ADMISSION_OR_RESULT",
        "input_checkpoint": str(args.checkpoint),
        "resume_checkpoint": str(args.output),
        "original_row_count": len(rows),
        "retained_row_count": len(kept),
        "local_cache_race_rows_removed_for_tree_only_resume": repaired,
        "blocked_rows_retained": blocked,
        "exclusions": [
            "No network command was executed by this repair.",
            "Only failure rows with a local, exact origin-and-pinned-commit proof are removed from the resume checkpoint.",
            "The original checkpoint and every original failure record remain preserved.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "removed": len(repaired), "retained": len(kept), "blocked": len(blocked)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
