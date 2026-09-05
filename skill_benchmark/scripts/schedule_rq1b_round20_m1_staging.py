#!/usr/bin/env python3
"""Schedule bounded Round 20 M1 byte-staging from the no-blob tree census."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--max-skill-paths", type=int, default=100)
    parser.add_argument("--max-sources-per-batch", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    census = {int(row["plan_position"]): row for row in read_jsonl(args.census)}
    if len(census) != len(plan.get("sources", [])):
        raise SystemExit(f"census_coverage_mismatch:{len(census)}:{len(plan.get('sources', []))}")
    selected: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    for position, source in enumerate(plan["sources"], start=1):
        row = census[position]
        count = row.get("skill_md_path_count")
        item = {
            "plan_position": position,
            "origin": source["origin"],
            "pinned_commit": source["pinned_commit"],
            "skill_md_path_count": count,
            "domains": source["domains"],
        }
        if row.get("tree_census_status") != "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT":
            item["defer_reason"] = "tree_census_failed"
            deferred.append(item)
        elif 1 <= int(count) <= args.max_skill_paths:
            selected.append(item)
        elif int(count) == 0:
            item["defer_reason"] = "no_skill_md_at_pinned_commit"
            deferred.append(item)
        else:
            item["defer_reason"] = f"above_current_{args.max_skill_paths}_skill_path_staging_budget"
            deferred.append(item)
    batches = []
    for offset in range(0, len(selected), args.max_sources_per_batch):
        members = selected[offset:offset + args.max_sources_per_batch]
        batches.append({
            "batch_id": f"R20-M1-SMALL-{offset // args.max_sources_per_batch + 1:02d}",
            "plan_positions": [member["plan_position"] for member in members],
            "origins": [member["origin"] for member in members],
            "source_count": len(members),
            "skill_md_path_count": sum(int(member["skill_md_path_count"]) for member in members),
            "domains": sorted({domain for member in members for domain in member["domains"]}),
        })
    payload = {
        "status": "M1_STAGING_SCHEDULE_READY_NOT_A_SOURCE_ADMISSION_OR_RESULT",
        "selection_rule": f"tree-census complete and between 1 and {args.max_skill_paths} SKILL.md paths per source",
        "batch_rule": f"at most {args.max_sources_per_batch} source families per batch",
        "scheduled_sources": selected,
        "deferred_sources": deferred,
        "batches": batches,
        "totals": {
            "scheduled_source_count": len(selected),
            "scheduled_skill_md_path_count": sum(int(row["skill_md_path_count"]) for row in selected),
            "deferred_source_count": len(deferred),
            "deferred_skill_md_path_count": sum(int(row["skill_md_path_count"] or 0) for row in deferred),
        },
        "exclusions": [
            "The size cap is an execution-scheduling rule, not a quality, originality, or cluster-validity decision.",
            "Deferred sources remain public discovery reservoirs and are not rejected or admitted.",
            "No source body, candidate composition, prompt, gold label, retrieval input, model result, or metric is created by this schedule.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "totals": payload["totals"], "batch_count": len(batches)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
