#!/usr/bin/env python3
"""Deduplicate Wave 035 navigation metadata without retrieving source bodies."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def canonical(url: str) -> str:
    return url.rstrip("/").lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-leads", type=Path, required=True)
    parser.add_argument("--prior-wave-leads", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw = json.loads(args.raw_leads.read_text(encoding="utf-8"))
    prior = json.loads(args.prior_wave_leads.read_text(encoding="utf-8"))
    prior_urls = {canonical(str(row["root"])) for row in prior}
    grouped: dict[str, list[dict]] = defaultdict(list)
    total = 0
    for scout in raw["scouts"]:
        domain = scout["domain"]
        for lead in scout["leads"]:
            total += 1
            grouped[canonical(lead["repository_url"])].append({"domain": domain, **lead})

    records = []
    for url, entries in sorted(grouped.items()):
        records.append({
            "status": "RQ1B_V3_W35_M0_UNIQUE_NAVIGATION_LEAD_NOT_A_CLUSTER",
            "repository_url": entries[0]["repository_url"],
            "evidence_urls": sorted({entry["evidence_url"] for entry in entries}),
            "discovery_domains": sorted({entry["domain"] for entry in entries}),
            "rationales": [entry["rationale"] for entry in entries],
            "within_wave_scout_mentions": len(entries),
            "previously_navigated_in_wave_034": url in prior_urls,
            "boundary": "Navigation metadata only. This record does not establish a reachable root, commit, SKILL.md path, source-frame admission, cluster, prompt, label, selector input, metric or result.",
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    report = {
        "status": "RQ1B_V3_W35_M0_DEDUP_PASS_NOT_A_CLUSTER",
        "raw_scout_lead_count": total,
        "unique_repository_lead_count": len(records),
        "within_wave_duplicate_mention_count": total - len(records),
        "previous_wave_034_root_overlap_count": sum(item["previously_navigated_in_wave_034"] for item in records),
        "new_root_candidate_count": sum(not item["previously_navigated_in_wave_034"] for item in records),
        "network_calls": 0,
        "texts_transmitted": 0,
        "boundary": "Local navigation-metadata normalisation only; no source retrieval or scientific conclusion.",
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
