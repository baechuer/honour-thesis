#!/usr/bin/env python3
"""Create a bounded, provenance-only Wave 021 public-source intake draft.

The input is M1 GitHub tree metadata. This program chooses only paths from
roots whose tree census succeeded; it never fetches bodies or infers quality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


KEYWORDS = (
    "audit",
    "compliance",
    "contract",
    "document",
    "finance",
    "incident",
    "legal",
    "migration",
    "privacy",
    "reconcile",
    "report",
    "review",
    "risk",
    "security",
    "spreadsheet",
    "test",
    "verification",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--max-total", type=int, default=100)
    parser.add_argument("--max-per-root", type=int, default=50)
    args = parser.parse_args()

    records = []
    for line in Path(args.census).read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if not record["status"].endswith("SUCCESS_NOT_A_CLUSTER"):
            continue
        selected = [
            path for path in record["skill_md_paths"]
            if any(keyword in path.lower() for keyword in KEYWORDS)
        ]
        if not selected:
            selected = record["skill_md_paths"]
        for path in selected[: args.max_per_root]:
            records.append((record, path))

    records.sort(key=lambda item: (item[0]["lane"], item[0]["repository_ref"], item[1]))
    records = records[: args.max_total]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as handle:
        for index, (root, path) in enumerate(records, start=1):
            owner_repo, commit = root["repository_ref"].split("@", 1)
            title = path.split("/")[-2] if "/" in path else path
            payload = {
                "artifact_heading_or_name": title,
                "artifact_path": path,
                "lane": root["lane"],
                "origin_url": root["origin_url"],
                "possible_peer_route_family": "Navigation hypothesis only; source-only D1 triage required after byte capture and deduplication.",
                "public_artifact_evidence": "Pinned public repository tree lists this SKILL.md path.",
                "raw_artifact_url": f"https://raw.githubusercontent.com/{owner_repo}/{commit}/{path}",
                "repository_ref": root["repository_ref"],
                "status": "RQ1B_V3_D1_W21_PUBLIC_SOURCE_INTAKE_DRAFT_NOT_A_CLUSTER",
                "visible_license_note": "Not assessed at intake; source URL and hash will be retained.",
                "wave_intake_index": index,
            }
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

    summary = {
        "status": "RQ1B_V3_D1_W21_INTAKE_DRAFT_COMPLETE_NOT_A_CLUSTER",
        "input_boundary": "M1 public repository-tree metadata only; no skill body was read by this builder.",
        "max_total": args.max_total,
        "max_per_root": args.max_per_root,
        "draft_record_count": len(records),
        "root_count": len({record["repository_ref"] for record, _ in records}),
    }
    Path(args.summary).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
