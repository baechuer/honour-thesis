#!/usr/bin/env python3
"""Partition the Round 20 C0 source pool into deterministic M0-origin lanes.

The lanes exist solely to keep parallel C0A navigation workers from proposing
the same source artefact. They are inherited from M0 discovery worker IDs,
not from a semantic similarity score or a cluster/label judgement.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


LANE_MARKERS = {
    "round20_m0_discovery_engineering_data_2026-08-27": "engineering_data",
    "round20_m0_discovery_science_health_2026-08-27": "science_health",
    "round20_m0_discovery_business_marketing_2026-08-27": "business_marketing",
    "round20_m0_discovery_creative_media_education_2026-08-27": "creative_media_education",
    "round20_m0_discovery_agent_ecosystems_2026-08-27": "agent_ecosystems",
    "round20_m0_discovery_specialised_professional_2026-08-27": "specialised_professional",
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
        originating = [str(item) for item in row["originating_discovery_ids"]]
        matches = sorted({lane for marker, lane in LANE_MARKERS.items() if any(item.startswith(marker + ":") for item in originating)})
        if not matches:
            raise ValueError(f"unmapped_m0_root:{url}")
        root_lanes[origin_from_url(url)] = matches[0]
    lane_rows: dict[str, list[dict[str, object]]] = {lane: [] for lane in LANE_MARKERS.values()}
    unassigned: list[str] = []
    for row in read_jsonl(args.pool):
        origin = str(row["origin"])
        lane = root_lanes.get(origin)
        if lane is None:
            unassigned.append(origin)
            continue
        lane_rows[lane].append({
            **row,
            "c0a_lane": lane,
            "c0a_lane_status": "SOURCE_NAVIGATION_LANE_ONLY_NOT_A_CLUSTER_OR_RESULT",
        })
    if unassigned:
        raise SystemExit(f"unassigned_pool_origins:{sorted(set(unassigned))}")
    emitted: dict[str, str] = {}
    for lane, rows in lane_rows.items():
        rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
        destination = args.output_directory / f"c0a_round20_{lane}_source_navigation_2026-08-27.jsonl"
        write_jsonl(destination, rows)
        emitted[lane] = str(destination)
    summary = {
        "status": "C0A_ROUND20_LANES_READY_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT",
        "source_pool": str(args.pool),
        "assignment_rule": "Each source origin receives the alphabetically first matching M0 worker discovery lane; this is a deterministic anti-overlap rule, not semantic classification.",
        "lane_counts": {lane: {"source_records": len(rows), "origins": len({str(row["origin"]) for row in rows})} for lane, rows in lane_rows.items()},
        "outputs": emitted,
        "exclusions": [
            "Lanes do not form candidate compositions or assert candidate peerhood.",
            "No original-source body is included in a lane; no prompt, label, retrieval input, model call, metric, or result exists.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "lane_counts": summary["lane_counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
