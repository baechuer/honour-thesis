#!/usr/bin/env python3
"""Normalise Wave 036 M0 leads without reading any source body."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def canonical(url: str) -> str:
    return url.rstrip("/").lower()


def lead_url(row: dict) -> str:
    return str(row.get("root") or row.get("repository_url") or "")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-leads", type=Path, action="append", required=True)
    parser.add_argument("--prior-leads", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prior_urls = {
        canonical(lead_url(row))
        for path in args.prior_leads
        for row in json.loads(path.read_text(encoding="utf-8"))
        if lead_url(row)
    }
    grouped: dict[str, list[dict]] = defaultdict(list)
    raw_count = 0
    for path in args.raw_leads:
        for row in json.loads(path.read_text(encoding="utf-8")):
            root = lead_url(row)
            if not root:
                raise SystemExit(f"missing_root:{path}")
            raw_count += 1
            grouped[canonical(root)].append(row)
    records = []
    for url, rows in sorted(grouped.items()):
        records.append({
            "status": "RQ1B_V3_W36_M0_UNIQUE_NAVIGATION_LEAD_NOT_A_CLUSTER",
            "root": rows[0]["root"],
            "discovery_domains": sorted({str(row["domain"]) for row in rows}),
            "rationales": [str(row["selection_reason"]) for row in rows],
            "within_wave_scout_mentions": len(rows),
            "previously_navigated_in_prior_wave": url in prior_urls,
            "boundary": "Navigation metadata only. It does not establish a reachable root, commit, SKILL.md path, source admission, cluster, prompt, label, selector input, metric or result.",
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W36_M0_DEDUP_PASS_NOT_A_CLUSTER",
        "raw_scout_lead_count": raw_count,
        "unique_repository_lead_count": len(records),
        "within_wave_duplicate_mention_count": raw_count - len(records),
        "prior_wave_overlap_count": sum(row["previously_navigated_in_prior_wave"] for row in records),
        "new_root_candidate_count": sum(not row["previously_navigated_in_prior_wave"] for row in records),
        "network_calls": 0,
        "texts_transmitted": 0,
        "boundary": "Local navigation-metadata normalisation only; no source retrieval or scientific conclusion.",
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
