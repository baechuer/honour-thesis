#!/usr/bin/env python3
"""Merge Round 20 RQ1b M0 discovery leads without admitting a source.

Round 20 is navigation-only. It records public repository roots for a later
commit-pinning stage; it never asserts that a repository contains an original
skill or that any set of skills forms a routing cluster.
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


def repo_root(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        raise ValueError(f"github_https_required:{url}")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise ValueError(f"github_repository_path_required:{url}")
    return f"https://github.com/{parts[0]}/{parts[1]}"


def read_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"non_object:{path}:{line_number}")
        missing = sorted(REQUIRED - set(row))
        if missing:
            raise ValueError(f"missing_keys:{path}:{line_number}:{','.join(missing)}")
        if row["original_artifact_status"] != STATUS:
            raise ValueError(f"status:{path}:{line_number}")
        row = {key: str(row[key]) for key in REQUIRED}
        repo_root(row["public_url"])
        rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    raw_rows: list[dict[str, str]] = []
    for input_path in args.input:
        for row in read_rows(input_path):
            local_id = row["discovery_id"]
            raw_rows.append({
                **row,
                "discovery_id": f"{input_path.stem}:{local_id}",
                "local_discovery_id": local_id,
                "source_discovery_file": input_path.name,
            })
    if len({row["discovery_id"] for row in raw_rows}) != len(raw_rows):
        raise SystemExit("duplicate_namespaced_discovery_id")

    roots: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        roots[repo_root(row["public_url"])].append(row)
    canonical_rows: list[dict[str, object]] = []
    for number, (root, rows) in enumerate(sorted(roots.items()), 1):
        canonical_rows.append({
            "round20_source_candidate_id": f"R20-M0-S{number:03d}",
            "canonical_public_source_url": root,
            "host": "github.com",
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
        "input_files": [str(path) for path in args.input],
        "identity_rule": "Worker-local discovery IDs are namespaced by input filename.",
        "exclusions": [
            "M0 does not pin commits, fetch skill bodies, admit sources, or create candidate compositions.",
            "M0 creates no prompt, label, retrieval input, model result, metric, or empirical conclusion.",
        ],
        "failures": [],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
