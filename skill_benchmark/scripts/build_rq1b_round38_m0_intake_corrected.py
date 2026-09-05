#!/usr/bin/env python3
"""Build Round 38 M0 intake while excluding current-round outputs from history."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from build_rq1b_round37_m0_intake import REQUIRED, read_jsonl, repo_root, write_jsonl


def historic_roots_without_current_round(directory: Path) -> set[str]:
    roots: set[str] = set()
    for path in sorted(directory.glob("m0_round*.jsonl")):
        if path.name.startswith("m0_round38_"):
            continue
        for row in read_jsonl(path):
            value = row.get("canonical_public_source_url") or row.get("repository_url")
            if not isinstance(value, str):
                continue
            try:
                roots.add(repo_root(value))
            except ValueError:
                continue
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
            missing = sorted(key for key in REQUIRED if not str(row.get(key, "")).strip())
            if missing:
                failures.append(f"missing_fields:{path}:{line_number}:{','.join(missing)}")
                continue
            try:
                root = repo_root(str(row["repository_url"]))
            except ValueError as error:
                failures.append(str(error))
                continue
            raw.append({
                "discovery_id": f"R38-M0-{path.stem.upper()}-{line_number:03d}",
                "canonical_public_source_url": root,
                "discovery_domain": str(row["discovery_domain"]),
                "source_repository_path_hint": str(row["source_repository_path"]),
                "skill_locator_url": str(row["skill_locator_url"]),
                "skill_title_or_name": str(row["skill_title_or_name"]),
                "capability_summary": str(row["capability_summary"]),
                "discovery_rationale": str(row["discovery_rationale"]),
                "source_ref_or_commit_observation": row.get("source_ref_or_commit"),
                "source_discovery_file": path.name,
                "m0_status": "M0_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
                "exclusions": [
                    "M0 only records public navigation leads; it does not pin a commit, fetch a tree/body, or admit a source.",
                    "No candidate composition, prompt, label, retrieval input, model result, metric, or empirical conclusion exists.",
                ],
            })

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in raw:
        grouped[str(row["canonical_public_source_url"])].append(row)
    canonical: list[dict[str, Any]] = []
    for index, (root, rows) in enumerate(sorted(grouped.items()), start=1):
        canonical.append({
            "round38_source_candidate_id": f"R38-M0-S{index:03d}",
            "canonical_public_source_url": root,
            "host": "github.com",
            "originating_discovery_ids": sorted(str(row["discovery_id"]) for row in rows),
            "domains": sorted({str(row["discovery_domain"]) for row in rows}),
            "sample_path_hints": sorted({str(row["source_repository_path_hint"]) for row in rows}),
            "locator_urls": sorted({str(row["skill_locator_url"]) for row in rows}),
            "capability_summaries": sorted({str(row["capability_summary"]) for row in rows}),
            "m0_status": "M0_CANONICAL_PUBLIC_NAVIGATION_LEAD_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
        })
    prior = historic_roots_without_current_round(args.prior_manifest_dir)
    new_roots = [row for row in canonical if row["canonical_public_source_url"] not in prior]
    write_jsonl(args.raw_output, sorted(raw, key=lambda row: str(row["discovery_id"])))
    write_jsonl(args.canonical_output, canonical)
    write_jsonl(args.new_root_output, new_roots)
    summary = {
        "status": "M0_ROUND38_INTAKE_DERIVED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT" if not failures else "M0_ROUND38_INTAKE_INVALID_NOT_A_CLUSTER_OR_RESULT",
        "raw_discovery_lead_count": len(raw),
        "canonical_public_source_count": len(canonical),
        "new_root_intake_count": len(new_roots),
        "exact_prior_root_exclusion_count": len(canonical) - len(new_roots),
        "input_files": [str(path) for path in args.input],
        "prior_manifest_directory": str(args.prior_manifest_dir),
        "current_round_manifest_prefix_excluded_from_history": "m0_round38_",
        "failures": sorted(set(failures)),
        "supersedes": [
            "m0_round38_intake_summary_2026-08-28.json",
            "m0_round38_intake_summary_2026-08-28.json from the earlier malformed-lead attempt",
        ],
        "exclusions": [
            "M0 does not pin commits, fetch repository trees/bodies, or admit sources.",
            "M0 does not create a candidate composition, prompt, label, retrieval input, model call, metric, or result.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "raw_discovery_lead_count", "canonical_public_source_count", "new_root_intake_count", "exact_prior_root_exclusion_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
