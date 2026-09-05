#!/usr/bin/env python3
"""Prepare disjoint Round 41 C0A navigation lanes from M0/M1 metadata only."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


M1_STATUS = "M1_PASS_ROUND41_PINNED_BYTE_VERIFIED_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def origin(repository_url: str) -> str:
    parsed = urlsplit(repository_url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"not_github_root:{repository_url}")
    return f"{parts[0]}/{parts[1]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--m1-inventory", type=Path, required=True)
    parser.add_argument("--m1-summary", type=Path, required=True)
    parser.add_argument("--pool-output", type=Path, required=True)
    parser.add_argument("--lanes-directory", type=Path, required=True)
    parser.add_argument("--pool-summary", type=Path, required=True)
    parser.add_argument("--lanes-summary", type=Path, required=True)
    args = parser.parse_args()

    m1_summary = json.loads(args.m1_summary.read_text(encoding="utf-8"))
    if m1_summary.get("status") != M1_STATUS:
        raise SystemExit(f"unexpected_m1_status:{m1_summary.get('status')}")
    source_rows = read_jsonl(args.m1_inventory)
    if len(source_rows) != int(m1_summary.get("m1_staged_source_count", -1)):
        raise SystemExit("m1_inventory_count_mismatch")
    if len({str(row["skill_id"]) for row in source_rows}) != len(source_rows):
        raise SystemExit("duplicate_m1_skill_id")

    root_lanes = {
        origin(str(row["canonical_public_source_url"])): sorted(str(value) for value in row["domains"])[0]
        for row in read_jsonl(args.m0)
    }
    pool: list[dict[str, Any]] = []
    for row in source_rows:
        lane = root_lanes.get(str(row["origin"]))
        if lane is None:
            raise SystemExit(f"unassigned_pool_origin:{row['origin']}")
        pool.append({
            **row,
            "source_name": row.get("frontmatter_name"),
            "source_description_preview": row.get("frontmatter_description"),
            "source_heading_preview": None,
            "c0a_lane": lane,
            "c0_pool_status": "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT",
            "source_inventory": str(args.m1_inventory),
            "exclusions": [
                "C0A exposes only source inventory metadata, not original skill bodies.",
                "No prompt, label, candidate composition validity, retrieval input, model call, metric, or result exists.",
            ],
        })
    pool.sort(key=lambda row: (str(row["c0a_lane"]), str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    write_jsonl(args.pool_output, pool)

    by_lane: dict[str, list[dict[str, Any]]] = {}
    for row in pool:
        by_lane.setdefault(str(row["c0a_lane"]), []).append(row)
    args.lanes_directory.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    for lane, rows in sorted(by_lane.items()):
        output = args.lanes_directory / f"c0a_round41_{lane}_source_navigation_2026-08-28.jsonl"
        write_jsonl(output, rows)
        outputs[lane] = str(output)

    pool_summary = {
        "status": "C0_ROUND41_SOURCE_POOL_READY_NOT_A_CLUSTER_OR_RESULT",
        "source_record_count": len(pool),
        "origin_count": len({str(row["origin"]) for row in pool}),
        "integrity_failures": [],
        "exclusions": [
            "The pool provides source-provided navigation metadata only and has no source-body text.",
            "No candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    lane_summary = {
        "status": "C0A_ROUND41_LANES_READY_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT",
        "source_pool": str(args.pool_output),
        "assignment_rule": "Each frozen source origin inherits its sole Round 41 M0 discovery lane. This prevents agent overlap and is not semantic validation.",
        "lane_counts": {
            lane: {"source_records": len(rows), "origins": len({str(row["origin"]) for row in rows})}
            for lane, rows in sorted(by_lane.items())
        },
        "outputs": outputs,
        "exclusions": [
            "A lane does not establish operational peerhood or form a valid candidate composition.",
            "Agents receive only navigation metadata in C0A; C0B alone may inspect literal original source evidence.",
        ],
    }
    args.pool_summary.parent.mkdir(parents=True, exist_ok=True)
    args.pool_summary.write_text(json.dumps(pool_summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.lanes_summary.write_text(json.dumps(lane_summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "pool_status": pool_summary["status"],
        "lane_status": lane_summary["status"],
        "lane_counts": lane_summary["lane_counts"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
