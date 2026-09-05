#!/usr/bin/env python3
"""Derive the Round 20 M0 intake set after prior-root de-duplication.

This is a provenance operation only. It preserves the raw/canonical M0 files
and makes no source-quality or cluster decision.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def rows(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def existing_urls(path: Path) -> set[str]:
    urls: set[str] = set()
    for row in rows(path):
        url = row.get("canonical_public_source_url") or row.get("repository_url")
        if not isinstance(url, str):
            raise ValueError(f"source_url_missing:{path}")
        urls.add(url)
    return urls


def write_jsonl(path: Path, payload: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in payload),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--prior", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    prior = set().union(*(existing_urls(path) for path in args.prior))
    original = rows(args.m0)
    included: list[dict[str, object]] = []
    excluded: list[dict[str, str]] = []
    for row in original:
        url = str(row["canonical_public_source_url"])
        if url in prior:
            excluded.append({
                "round20_source_candidate_id": str(row["round20_source_candidate_id"]),
                "canonical_public_source_url": url,
                "exclusion": "EXACT_PRIOR_PUBLIC_SOURCE_ROOT_NOT_A_NEW_M1_INTAKE",
            })
        else:
            included.append(row)
    write_jsonl(args.output, included)
    payload = {
        "status": "M0_ROUND20_NEW_ROOT_INTAKE_DERIVED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        "canonical_input_count": len(original),
        "new_root_intake_count": len(included),
        "exact_prior_root_exclusion_count": len(excluded),
        "excluded_existing_roots": excluded,
        "m0_canonical_input": str(args.m0),
        "prior_inputs": [str(path) for path in args.prior],
        "exclusions": [
            "The canonical M0 lead file remains preserved and unmodified.",
            "This filter does not pin commits, fetch files, admit a source, or create a composition, prompt, label, retrieval input, result, or metric.",
        ],
        "failures": [],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("status", "canonical_input_count", "new_root_intake_count", "exact_prior_root_exclusion_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
