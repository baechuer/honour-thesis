#!/usr/bin/env python3
"""Freeze a balanced, metadata-only Wave 039 M1 root roster."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prior_successful_m1_roots(frame_root: Path) -> set[str]:
    """Read only historical M1 metadata summaries, never source bodies."""
    roots = set()
    for summary_path in frame_root.glob("d1_source_intake_wave_*/**/M1_PINNED_ROOTS_SUMMARY.json"):
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        for row in summary.get("root_rows", []):
            status = str(row.get("status", ""))
            root = row.get("root")
            if "PASS" in status and isinstance(root, str) and root.startswith("https://github.com/"):
                roots.add(root.rstrip("/").lower())
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leads", type=Path, required=True)
    parser.add_argument("--frame-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-lane", type=int, default=4)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_roster")
    leads = read_jsonl(args.leads)
    prior_m1_roots = prior_successful_m1_roots(args.frame_root)
    by_lane: dict[str, list[dict]] = defaultdict(list)
    for lead in leads:
        already_m1 = lead["origin_url"].rstrip("/").lower() in prior_m1_roots
        if not lead.get("prior_source_frame_origin_overlap") and not already_m1:
            lead = {**lead, "prior_m1_metadata_root_overlap": False}
            by_lane[lead["discovery_lane"]].append(lead)
    selected = []
    for lane in sorted(by_lane):
        ranked = sorted(
            by_lane[lane],
            key=lambda row: (-len(row["likely_skill_path_hints"]), row["owner_repo"]),
        )
        for lead in ranked[:args.per_lane]:
            selected.append({
                "root": lead["origin_url"],
                "domain": lead["domain"],
                "discovery_lane": lane,
                "discovery_id": lead["discovery_id"],
                "priority": "high",
                "selection_rule": "fresh origin; lane-balanced; descending path-hint count then owner/repo",
                "m1_status": "RQ1B_V3_W39_M1_ROOT_FROZEN_METADATA_ONLY_NOT_A_SOURCE_OR_RESULT",
            })
    selected.sort(key=lambda row: (row["discovery_lane"], row["root"]))
    if len({row["root"] for row in selected}) != len(selected):
        raise SystemExit("duplicate_root_selected")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(selected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": "RQ1B_V3_W39_M1_ROOT_ROSTER_FREEZE_PASS_NOT_A_SOURCE_OR_RESULT",
        "fresh_lead_count_after_source_frame_and_m1_root_exclusion": sum(len(rows) for rows in by_lane.values()),
        "historical_successful_m1_root_count": len(prior_m1_roots),
        "selected_root_count": len(selected),
        "per_lane_cap": args.per_lane,
        "selected_lane_counts": dict(sorted(Counter(row["discovery_lane"] for row in selected).items())),
        "selection_boundary": "Uses only M0 metadata/path-hint counts and owner/repo ordering. No source body, cluster, prompt, label, selector, metric or result is involved.",
    }
    (args.output.parent / "W39_M1_ROOT_ROSTER_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
