#!/usr/bin/env python3
"""Canonicalise Wave 038 M0 navigation leads without reading skill bodies."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


REQUIRED = {
    "repository_url", "owner_repo", "discovery_lane",
    "likely_skill_path_or_hint", "navigation_rationale",
}


def normalise_owner_repo(value: str) -> str:
    owner_repo = value.strip().rstrip("/").lower()
    if not re.fullmatch(r"[a-z0-9_.-]+/[a-z0-9_.-]+", owner_repo):
        raise ValueError(f"invalid_owner_repo:{value}")
    return owner_repo


def prior_owner_repos(staged_roots: list[Path]) -> set[str]:
    """Infer historical owner/repo metadata from directory names only."""
    prior = set()
    marker = re.compile(r"(?:round|rq1b)[^-]*-m1-([a-z0-9_.-]+)--([a-z0-9_.-]+?)-[0-9a-f]{8}$", re.I)
    for root in staged_roots:
        if not root.is_dir():
            continue
        for child in root.iterdir():
            if not child.is_dir():
                continue
            match = marker.search(child.name)
            if match:
                prior.add(f"{match.group(1).lower()}/{match.group(2).lower()}")
    return prior


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0-dir", type=Path, required=True)
    parser.add_argument("--staged-root", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    raw_paths = sorted(args.m0_dir.glob("SCOUT_*_RAW.json"))
    if not raw_paths:
        raise SystemExit("no_raw_m0_returns")
    prior = prior_owner_repos(args.staged_root)
    seen = set()
    records = []
    within_wave_duplicates = []
    for raw_path in raw_paths:
        rows = json.loads(raw_path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            raise SystemExit(f"nonarray_raw_return:{raw_path}")
        for row in rows:
            if set(row) != REQUIRED or not all(isinstance(row[key], str) and row[key].strip() for key in REQUIRED):
                raise SystemExit(f"invalid_raw_row:{raw_path}")
            owner_repo = normalise_owner_repo(row["owner_repo"])
            expected_url = f"https://github.com/{owner_repo}"
            if row["repository_url"].rstrip("/").lower() != expected_url:
                raise SystemExit(f"url_owner_mismatch:{row['repository_url']}")
            if owner_repo in seen:
                within_wave_duplicates.append(owner_repo)
                continue
            seen.add(owner_repo)
            records.append({
                "discovery_id": f"RQ1B-V3-W38-M0-{len(records) + 1:03d}",
                "repository_url": expected_url,
                "owner_repo": owner_repo,
                "discovery_lane": row["discovery_lane"],
                "likely_skill_path_or_hint": row["likely_skill_path_or_hint"],
                "navigation_rationale": row["navigation_rationale"],
                "prior_origin_overlap": owner_repo in prior,
                "m0_status": "M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
                "claim_boundary": "Navigation metadata only. No source body was read, pinned, captured, parsed, embedded, scored or used to form a cluster.",
            })
    output_rows = sorted(records, key=lambda row: (row["prior_origin_overlap"], row["owner_repo"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in output_rows), encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W38_M0_MERGE_PASS_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "raw_return_count": len(raw_paths),
        "raw_lead_count": sum(1 for _ in records) + len(within_wave_duplicates),
        "within_wave_duplicate_count": len(within_wave_duplicates),
        "unique_lead_count": len(records),
        "prior_origin_overlap_count": sum(row["prior_origin_overlap"] for row in records),
        "fresh_navigation_candidate_count": sum(not row["prior_origin_overlap"] for row in records),
        "lane_counts": dict(sorted(Counter(row["discovery_lane"] for row in records).items())),
        "network_calls": 0,
        "source_body_reads": 0,
        "source_body_transfers": 0,
        "claim_boundary": "M0 is navigation-only discovery and does not admit a source or establish a candidate composition, prompt, label, selector input, metric or result.",
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("unique_lead_count", "fresh_navigation_candidate_count", "prior_origin_overlap_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
