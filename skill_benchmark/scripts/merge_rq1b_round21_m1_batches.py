#!/usr/bin/env python3
"""Merge complete scheduled Round 21 M1 batch ledgers for integrity flattening."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED_BATCH = "M1_ROUND21_BATCH_COMPLETE_WITH_PER_SOURCE_STATUS_NOT_A_CLUSTER_OR_RESULT"
EXPECTED_PLAN = "M1_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT"
ACCEPTED = {
    "M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT",
    "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--schedule", type=Path, required=True)
    parser.add_argument("--batch", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = read(args.plan)
    schedule = read(args.schedule)
    if plan.get("status") != EXPECTED_PLAN:
        raise SystemExit("unexpected_plan_status")
    expected_positions = {
        int(row["plan_position"])
        for row in schedule.get("scheduled_sources", [])
    }
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    seen_positions: set[int] = set()
    for path in args.batch:
        batch = read(path)
        if batch.get("status") != EXPECTED_BATCH:
            failures.append(f"unexpected_batch_status:{path.name}")
            continue
        for row in batch.get("results", []):
            position = int(row.get("plan_position", -1))
            if position in seen_positions:
                failures.append(f"duplicate_plan_position:{position}")
            seen_positions.add(position)
            if row.get("m1_stage_status") not in ACCEPTED:
                failures.append(f"nonstage_result:{position}:{row.get('m1_stage_status')}")
            results.append(row)
    if seen_positions != expected_positions:
        failures.append(f"scheduled_coverage_mismatch:expected={len(expected_positions)}:seen={len(seen_positions)}")
    results.sort(key=lambda row: int(row["plan_position"]))
    payload = {
        "status": "M1_LOCAL_BYTE_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT" if not failures else "M1_LOCAL_BYTE_STAGING_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "round": "RQ1b cross-source Round 21 scheduled small-source intake",
        "plan": str(args.plan),
        "plan_sha256": digest(args.plan),
        "schedule": str(args.schedule),
        "schedule_sha256": digest(args.schedule),
        "source_count": len(results),
        "results": results,
        "totals": {
            "discovered_skill_files": sum(int(row.get("staging_summary", {}).get("discovered_skill_files", 0)) for row in results),
            "staged_sources": sum(int(row.get("staging_summary", {}).get("staged_sources", 0)) for row in results),
            "skipped_exact_duplicates": sum(int(row.get("staging_summary", {}).get("skipped_exact_duplicates", 0)) for row in results),
            "skipped_missing_frontmatter": sum(int(row.get("staging_summary", {}).get("skipped_missing_frontmatter", 0)) for row in results),
        },
        "failures": failures,
        "deferred_source_note": "Sources above the current per-source size budget are deferred for separate scheduling, not rejected or included in this M1 aggregate.",
        "exclusions": [
            "No source content was executed.",
            "No candidate composition, prompt, gold label, acceptable set, retrieval input, embedding, selector call, metric, or result was created.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "source_count": len(results), "totals": payload["totals"], "failures": failures}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
