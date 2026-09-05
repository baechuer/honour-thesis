#!/usr/bin/env python3
"""Derive the Round 21 M0 intake set after exact prior-root exclusion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def urls_from(path: Path) -> set[str]:
    result: set[str] = set()
    for row in read_jsonl(path):
        url = row.get("canonical_public_source_url") or row.get("repository_url")
        if not isinstance(url, str):
            raise ValueError(f"source_url_missing:{path}")
        result.add(url)
    return result


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m0", type=Path, required=True)
    parser.add_argument("--prior", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prior = set().union(*(urls_from(path) for path in args.prior))
    included: list[dict[str, object]] = []
    excluded: list[dict[str, str]] = []
    original = read_jsonl(args.m0)
    for row in original:
        url = str(row["canonical_public_source_url"])
        if url in prior:
            excluded.append({
                "round21_source_candidate_id": str(row["round21_source_candidate_id"]),
                "canonical_public_source_url": url,
                "exclusion": "EXACT_PRIOR_PUBLIC_SOURCE_ROOT_NOT_A_NEW_M1_INTAKE",
            })
        else:
            included.append(row)
    write_jsonl(args.output, included)
    summary = {
        "status": "M0_ROUND21_NEW_ROOT_INTAKE_DERIVED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
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
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "canonical_input_count", "new_root_intake_count", "exact_prior_root_exclusion_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
