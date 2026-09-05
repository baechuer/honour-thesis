#!/usr/bin/env python3
"""Build Round 36 C0 source pool and provenance-only C0A lanes.

The assignment is inherited from the discovery file, not inferred from source
content. It creates no semantic relation, candidate composition, prompt,
label, retrieval input, model call, metric, or result.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


M2_PASS = "M2A_PASS_LOCAL_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT"
PATTERN = re.compile(r"R36-M0-([A-Z_]+)-\d{3}$")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def origin(url: str) -> str:
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"not_github_root:{url}")
    return f"{parts[0]}/{parts[1]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--m2", type=Path, required=True)
    parser.add_argument("--m2-summary", type=Path, required=True)
    parser.add_argument("--pool-output", type=Path, required=True)
    parser.add_argument("--lanes-directory", type=Path, required=True)
    parser.add_argument("--pool-summary", type=Path, required=True)
    parser.add_argument("--lanes-summary", type=Path, required=True)
    args = parser.parse_args()

    m2_summary = json.loads(args.m2_summary.read_text(encoding="utf-8"))
    if m2_summary.get("status") != M2_PASS:
        raise SystemExit(f"unexpected_m2_status:{m2_summary.get('status')}")
    source_rows = read_jsonl(args.m2)
    if len(source_rows) != int(m2_summary.get("inventory_record_count", -1)):
        raise SystemExit("m2_inventory_count_mismatch")
    if len({str(row.get("skill_id")) for row in source_rows}) != len(source_rows):
        raise SystemExit("duplicate_m2_skill_id")

    root_lanes: dict[str, str] = {}
    for row in read_jsonl(args.m0):
        lanes: set[str] = set()
        for identifier in [str(value) for value in row["originating_discovery_ids"]]:
            match = PATTERN.fullmatch(identifier.rsplit(":", 1)[-1])
            if match is not None:
                lanes.add(match.group(1).lower())
        if not lanes:
            source_name = str(row.get("source_discovery_file", "coordinator_seed"))
            lanes.add(re.sub(r"[^a-z0-9]+", "_", source_name.lower()).strip("_") or "coordinator_seed")
        root_lanes[origin(str(row["canonical_public_source_url"]))] = sorted(lanes)[0]

    pool = [{**row, "c0_pool_status": "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT", "source_inventory": str(args.m2)} for row in source_rows]
    write_jsonl(args.pool_output, pool)
    pool_summary = {"status": "C0_ROUND36_SOURCE_POOL_READY_NOT_A_CLUSTER_OR_RESULT", "m2_input": str(args.m2), "source_record_count": len(pool), "origin_count": len({str(row["origin"]) for row in pool}), "integrity_failures": [], "exclusions": ["The source pool contains source-navigation metadata only.", "No full-source semantic review, candidate composition, prompt, label, retrieval input, model call, metric, or result was created."]}
    args.pool_summary.parent.mkdir(parents=True, exist_ok=True)
    args.pool_summary.write_text(json.dumps(pool_summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lanes: dict[str, list[dict[str, object]]] = {}
    for row in pool:
        item_origin = str(row["origin"])
        lane = root_lanes.get(item_origin)
        if lane is None:
            raise SystemExit(f"unassigned_pool_origin:{item_origin}")
        lanes.setdefault(lane, []).append({**row, "c0a_lane": lane, "c0a_lane_status": "SOURCE_NAVIGATION_LANE_ONLY_NOT_A_CLUSTER_OR_RESULT"})
    outputs: dict[str, str] = {}
    for lane, rows in sorted(lanes.items()):
        rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
        output = args.lanes_directory / f"c0a_round36_{lane}_source_navigation_2026-08-28.jsonl"
        write_jsonl(output, rows)
        outputs[lane] = str(output)
    lane_summary = {"status": "C0A_ROUND36_LANES_READY_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT", "source_pool": str(args.pool_output), "assignment_rule": "Each source origin is assigned to its alphabetically first originating M0 discovery lane. This is an anti-overlap rule, not semantic classification.", "lane_counts": {lane: {"source_records": len(rows), "origins": len({str(row["origin"]) for row in rows})} for lane, rows in sorted(lanes.items())}, "outputs": outputs, "integrity_failures": [], "exclusions": ["Lanes do not form candidate compositions or assert candidate peerhood.", "No source original body is included in a lane; no prompt, label, retrieval input, model call, metric, or result exists."]}
    args.lanes_summary.parent.mkdir(parents=True, exist_ok=True)
    args.lanes_summary.write_text(json.dumps(lane_summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"pool_status": pool_summary["status"], "lane_status": lane_summary["status"], "lane_counts": lane_summary["lane_counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
