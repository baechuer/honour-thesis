#!/usr/bin/env python3
"""Canonicalise and prior-root-filter Round 22 RQ1b M0 discovery leads.

The input is navigation-only public repository metadata. This tool never pins
commits, reads source bodies, or emits candidates, prompts, labels, or results.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit


REQUIRED = {
    "discovery_id",
    "canonical_public_source_url",
    "domains",
    "source_family_hints",
    "navigation_hints",
    "caveats",
    "licence_status_observations",
    "m0_status",
}
STATUS = "M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"non_object:{path}:{number}")
        missing = sorted(REQUIRED - set(row))
        if missing:
            raise ValueError(f"missing_keys:{path}:{number}:{','.join(missing)}")
        if row["m0_status"] != STATUS:
            raise ValueError(f"unexpected_status:{path}:{number}:{row['m0_status']}")
        rows.append(row)
    return rows


def repo_root(value: str) -> str:
    parsed = urlsplit(value)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) < 2:
        raise ValueError(f"github_repository_root_required:{value}")
    return f"https://github.com/{parts[0]}/{parts[1]}"


def prior_roots(path: Path) -> set[str]:
    roots: set[str] = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"non_object_prior:{path}:{number}")
        value = row.get("canonical_public_source_url") or row.get("repository_url")
        if isinstance(value, str):
            roots.add(repo_root(value))
    return roots


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--prior", action="append", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--canonical-output", type=Path, required=True)
    parser.add_argument("--new-root-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    raw: list[dict[str, object]] = []
    for path in args.input:
        for row in read_jsonl(path):
            raw.append({
                **row,
                "discovery_id": f"{path.stem}:{row['discovery_id']}",
                "local_discovery_id": row["discovery_id"],
                "source_discovery_file": path.name,
            })
    if len({str(row["discovery_id"]) for row in raw}) != len(raw):
        raise SystemExit("duplicate_namespaced_discovery_id")

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in raw:
        grouped[repo_root(str(row["canonical_public_source_url"]))].append(row)
    canonical: list[dict[str, object]] = []
    for number, (root, rows) in enumerate(sorted(grouped.items()), start=1):
        def flatten(key: str) -> list[str]:
            values: set[str] = set()
            for row in rows:
                item = row[key]
                values.update(str(value) for value in item) if isinstance(item, list) else values.add(str(item))
            return sorted(values)
        canonical.append({
            "round22_source_candidate_id": f"R22-M0-S{number:03d}",
            "canonical_public_source_url": root,
            "host": "github.com",
            "originating_discovery_ids": sorted(str(row["discovery_id"]) for row in rows),
            "domains": flatten("domains"),
            "source_family_hints": flatten("source_family_hints"),
            "navigation_hints": flatten("navigation_hints"),
            "licence_status_observations": flatten("licence_status_observations"),
            "caveats": flatten("caveats"),
            "m0_status": "M0_CANONICAL_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        })

    existing = set().union(*(prior_roots(path) for path in args.prior))
    new_roots = [row for row in canonical if str(row["canonical_public_source_url"]) not in existing]
    excluded = [row for row in canonical if str(row["canonical_public_source_url"]) in existing]
    write_jsonl(args.raw_output, sorted(raw, key=lambda row: str(row["discovery_id"])))
    write_jsonl(args.canonical_output, canonical)
    write_jsonl(args.new_root_output, new_roots)
    summary = {
        "status": "M0_ROUND22_INTAKE_DERIVED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "raw_discovery_lead_count": len(raw),
        "canonical_public_source_count": len(canonical),
        "new_root_intake_count": len(new_roots),
        "exact_prior_root_exclusion_count": len(excluded),
        "excluded_existing_roots": [str(row["canonical_public_source_url"]) for row in excluded],
        "input_files": [str(path) for path in args.input],
        "prior_inputs": [str(path) for path in args.prior],
        "exclusions": [
            "M0 does not pin commits, fetch skill bodies, admit sources, or create candidate compositions.",
            "M0 creates no prompt, label, retrieval input, model result, metric, or empirical conclusion.",
        ],
        "failures": [],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "raw_discovery_lead_count", "canonical_public_source_count", "new_root_intake_count", "exact_prior_root_exclusion_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
