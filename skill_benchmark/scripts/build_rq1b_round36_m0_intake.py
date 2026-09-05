#!/usr/bin/env python3
"""Canonicalise parallel Round 36 M0 discovery leads and filter prior roots.

This is navigation-only source discovery. It normalises reviewer discovery
notes into the frozen M0 shape without pinning a commit, fetching a tree/body,
or creating a candidate composition, prompt, label, retrieval input, or result.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


RAW_STATUS = "M0_DISCOVERY_LEAD_ONLY_NOT_A_CLUSTER_OR_RESULT"
CANONICAL_STATUS = "M0_CANONICAL_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT"


def repo_root(value: str) -> str:
    parsed = urlsplit(value)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) < 2:
        raise ValueError(f"github_repository_root_required:{value}")
    return f"https://github.com/{parts[0]}/{parts[1]}"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"non_object:{path}:{line_number}")
        rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def prior_roots(directory: Path) -> set[str]:
    roots: set[str] = set()
    for path in sorted(directory.glob("m0_round*_canonical_source_leads_*.jsonl")):
        for row in read_jsonl(path):
            value = row.get("canonical_public_source_url") or row.get("repository_url")
            if isinstance(value, str):
                roots.add(repo_root(value))
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--prior-manifest-dir", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--canonical-output", type=Path, required=True)
    parser.add_argument("--new-root-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    raw: list[dict[str, Any]] = []
    failures: list[str] = []
    for path in args.input:
        for line_number, row in enumerate(read_jsonl(path), start=1):
            if row.get("m0_status") != RAW_STATUS:
                failures.append(f"unexpected_status:{path}:{line_number}:{row.get('m0_status')}")
                continue
            repository_url = row.get("repository_url")
            if not isinstance(repository_url, str):
                failures.append(f"missing_repository_url:{path}:{line_number}")
                continue
            try:
                root = repo_root(repository_url)
            except ValueError as error:
                failures.append(str(error))
                continue
            raw.append({
                "discovery_id": f"R36-M0-{path.stem.upper()}-{line_number:03d}",
                "canonical_public_source_url": root,
                "domains": [str(row.get("domain", "unspecified"))],
                "source_family_hints": [str(row.get("expected_skill_path_or_signal", "unspecified_skill_signal"))],
                "navigation_hints": [str(row.get("discovery_query", "unspecified_query")), str(row.get("public_evidence_url", root))],
                "caveats": ["M0 navigation lead only; no repository tree or skill body was fetched or read", str(row.get("notes", ""))],
                "licence_status_observations": ["NOT_OBSERVED_AT_M0"],
                "source_discovery_file": path.name,
                "source_discovery_origin": str(row.get("origin", "")),
                "m0_status": "M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
            })
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in raw:
        grouped[str(row["canonical_public_source_url"])].append(row)
    canonical: list[dict[str, Any]] = []
    for index, (root, rows) in enumerate(sorted(grouped.items()), start=1):
        def flatten(name: str) -> list[str]:
            return sorted({str(item) for row in rows for item in row[name] if str(item)})
        canonical.append({
            "round36_source_candidate_id": f"R36-M0-S{index:03d}",
            "canonical_public_source_url": root,
            "host": "github.com",
            "originating_discovery_ids": sorted(str(row["discovery_id"]) for row in rows),
            "domains": flatten("domains"),
            "source_family_hints": flatten("source_family_hints"),
            "navigation_hints": flatten("navigation_hints"),
            "licence_status_observations": flatten("licence_status_observations"),
            "caveats": flatten("caveats"),
            "m0_status": CANONICAL_STATUS,
        })
    existing = prior_roots(args.prior_manifest_dir)
    new_roots = [row for row in canonical if row["canonical_public_source_url"] not in existing]
    write_jsonl(args.raw_output, sorted(raw, key=lambda row: str(row["discovery_id"])))
    write_jsonl(args.canonical_output, canonical)
    write_jsonl(args.new_root_output, new_roots)
    summary = {
        "status": "M0_ROUND36_INTAKE_DERIVED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT" if not failures else "M0_ROUND36_INTAKE_INVALID_NOT_A_CLUSTER_OR_RESULT",
        "raw_discovery_lead_count": len(raw),
        "canonical_public_source_count": len(canonical),
        "new_root_intake_count": len(new_roots),
        "exact_prior_root_exclusion_count": len(canonical) - len(new_roots),
        "prior_manifest_directory": str(args.prior_manifest_dir),
        "input_files": [str(path) for path in args.input],
        "failures": sorted(set(failures)),
        "exclusions": [
            "M0 does not pin commits, fetch repository trees or skill bodies, or admit sources.",
            "M0 creates no candidate composition, prompt, label, retrieval input, model result, metric, or empirical conclusion.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "raw_discovery_lead_count", "canonical_public_source_count", "new_root_intake_count", "exact_prior_root_exclusion_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
