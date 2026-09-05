#!/usr/bin/env python3
"""Partition the Round 23 source-only pool into anti-overlap C0A lanes.

The lane assignment is inherited only from the M0 discovery worker that found
the public repository. It is neither a semantic judgement nor a candidate
composition. Each origin occurs in exactly one lane so independent C0A workers
cannot reuse a source artefact.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


LANE_MARKERS = {
    "round23_m0_discovery_data_business_2026-08-27": "data_business",
    "round23_m0_discovery_docs_professional_2026-08-27": "docs_professional",
    "round23_m0_discovery_engineering_platform_2026-08-27": "engineering_platform",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def origin_from_url(url: str) -> str:
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"bad_root:{url}")
    return f"{parts[0]}/{parts[1]}"


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    root_lanes: dict[str, str] = {}
    for row in read_jsonl(args.m0):
        url = str(row["canonical_public_source_url"])
        discovery_ids = [str(value) for value in row["originating_discovery_ids"]]
        matches = sorted({lane for marker, lane in LANE_MARKERS.items() if any(value.startswith(marker + ":") for value in discovery_ids)})
        if not matches:
            raise SystemExit(f"unmapped_m0_root:{url}")
        root_lanes[origin_from_url(url)] = matches[0]

    lane_rows: dict[str, list[dict[str, object]]] = {lane: [] for lane in sorted(set(LANE_MARKERS.values()))}
    unassigned: set[str] = set()
    for row in read_jsonl(args.pool):
        origin = str(row["origin"])
        lane = root_lanes.get(origin)
        if lane is None:
            unassigned.add(origin)
            continue
        lane_rows[lane].append({
            **row,
            "c0a_lane": lane,
            "c0a_lane_status": "SOURCE_NAVIGATION_LANE_ONLY_NOT_A_CLUSTER_OR_RESULT",
        })
    if unassigned:
        raise SystemExit(f"unassigned_pool_origins:{sorted(unassigned)}")

    outputs: dict[str, str] = {}
    for lane, rows in lane_rows.items():
        rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
        output = args.output_directory / f"c0a_round23_{lane}_source_navigation_2026-08-27.jsonl"
        write_jsonl(output, rows)
        outputs[lane] = str(output)
    summary = {
        "status": "C0A_ROUND23_LANES_READY_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT",
        "source_pool": str(args.pool),
        "assignment_rule": "Each source origin is assigned to its alphabetically first originating M0 discovery lane. This is an anti-overlap rule, not semantic classification.",
        "lane_counts": {lane: {"source_records": len(rows), "origins": len({str(row["origin"]) for row in rows})} for lane, rows in lane_rows.items()},
        "outputs": outputs,
        "exclusions": [
            "Lanes do not form candidate compositions or assert candidate peerhood.",
            "No source original body is included in a lane; no prompt, label, retrieval input, model call, metric, or result exists.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "lane_counts": summary["lane_counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
