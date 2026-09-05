#!/usr/bin/env python3
"""Merge Round 18 RQ1b M0 discovery leads without admitting a source.

This program only normalises public navigation leads.  It neither contacts a
host nor decides provenance, skill originality, cluster validity, or labels.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit


REQUIRED = {
    "discovery_id",
    "public_url",
    "host",
    "source_family_hint",
    "candidate_paths_or_navigation_hint",
    "domain",
    "why_it_may_offer_natural_peer_skills",
    "original_artifact_status",
    "licence_status",
    "caveats",
}
STATUS = "unverified_navigation_lead"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--canonical-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"non_object:{path}:{line_no}")
        missing = sorted(REQUIRED - set(row))
        if missing:
            raise ValueError(f"missing_keys:{path}:{line_no}:{','.join(missing)}")
        if row.get("original_artifact_status") != STATUS:
            raise ValueError(f"unexpected_status:{path}:{line_no}")
        rows.append({key: str(row[key]) for key in REQUIRED})
    return rows


def repository_root(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"not_public_https_url:{url}")
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.netloc == "github.com" and len(parts) >= 2:
        return f"https://github.com/{parts[0]}/{parts[1]}"
    return f"https://{parsed.netloc}/{'/'.join(parts[:2])}" if len(parts) >= 2 else f"https://{parsed.netloc}"


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    args = parse_args()
    raw_rows: list[dict[str, str]] = []
    for path in args.input:
        # Discovery IDs are intentionally local to a domain worker. Namespace
        # them at merge time while retaining the worker's original identifier.
        for row in read_rows(path):
            local_id = row["discovery_id"]
            raw_rows.append({
                **row,
                "discovery_id": f"{path.stem}:{local_id}",
                "local_discovery_id": local_id,
                "source_discovery_file": path.name,
            })
    ids = [row["discovery_id"] for row in raw_rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate_discovery_id")

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        groups[repository_root(row["public_url"])].append(row)
    canonical_rows: list[dict[str, object]] = []
    for ordinal, (root, rows) in enumerate(sorted(groups.items()), start=1):
        canonical_rows.append({
            "round18_source_candidate_id": f"R18-M0-S{ordinal:03d}",
            "canonical_public_source_url": root,
            "host": rows[0]["host"],
            "originating_discovery_ids": sorted(row["discovery_id"] for row in rows),
            "domains": sorted({row["domain"] for row in rows}),
            "source_family_hints": sorted({row["source_family_hint"] for row in rows}),
            "navigation_hints": sorted({row["candidate_paths_or_navigation_hint"] for row in rows}),
            "licence_status_observations": sorted({row["licence_status"] for row in rows}),
            "caveats": sorted({row["caveats"] for row in rows}),
            "m0_status": "M0_CANONICAL_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        })
    raw_rows.sort(key=lambda row: row["discovery_id"])
    write_jsonl(args.raw_output, raw_rows)
    write_jsonl(args.canonical_output, canonical_rows)
    summary = {
        "status": "M0_MERGE_PASS_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "raw_discovery_lead_count": len(raw_rows),
        "canonical_public_source_count": len(canonical_rows),
        "raw_domain_counts": {
            domain: sum(row["domain"] == domain for row in raw_rows)
            for domain in sorted({row["domain"] for row in raw_rows})
        },
        "input_files": [str(path) for path in args.input],
        "identity_rule": "Each worker-local discovery_id is namespaced by its input filename during merge.",
        "failures": [],
        "exclusions": [
            "M0 does not contact, clone, pin, or admit any source.",
            "M0 does not create a candidate composition, prompt, gold label, retrieval input, model result, or metric.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
