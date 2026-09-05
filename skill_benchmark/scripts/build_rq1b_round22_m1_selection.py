#!/usr/bin/env python3
"""Select a bounded, diverse Round 22 M1 source-staging cohort.

The selection consumes only the completed blobless tree-census records.  It
does not read a skill body, infer a semantic relation, or create any benchmark
artefact.  The selected cohort favours origins with 3--64 ``SKILL.md`` paths:
large enough to contribute useful natural artefacts but small enough for the
first source-only navigation pass to remain auditable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COMPLETE = "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT"
SELECTION_STATUS = "M1_ROUND22_BOUNDED_DIVERSE_STAGING_SELECTION_NOT_A_CLUSTER_OR_RESULT"


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--minimum-paths", type=int, default=3)
    parser.add_argument("--maximum-paths", type=int, default=64)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    if args.minimum_paths < 1 or args.maximum_paths < args.minimum_paths:
        raise SystemExit("invalid_path_bounds")

    census = read_jsonl(args.census)
    selected = [
        row for row in census
        if row.get("tree_census_status") == COMPLETE
        and args.minimum_paths <= int(row.get("skill_md_path_count", 0)) <= args.maximum_paths
    ]
    selected.sort(key=lambda row: int(row["plan_position"]))
    positions = [int(row["plan_position"]) for row in selected]
    if len(positions) != len(set(positions)):
        raise SystemExit("duplicate_plan_positions")

    sources = [
        {
            "plan_position": int(row["plan_position"]),
            "origin": row["origin"],
            "repository_url": row["repository_url"],
            "pinned_commit": row["pinned_commit"],
            "skill_md_path_count": int(row["skill_md_path_count"]),
            "selection_rationale": "completed_blobless_tree_census_and_bounded_3_to_64_skill_paths",
            "selection_status": "M1_SELECTED_FOR_LOCAL_BYTE_STAGING_NOT_A_CLUSTER_OR_RESULT",
        }
        for row in selected
    ]
    payload = {
        "status": SELECTION_STATUS,
        "round": "RQ1b cross-source Round 22",
        "purpose": (
            "Bounded first byte-staging cohort after discovery-first public-source expansion. "
            "This is source admission bookkeeping, not candidate composition or evaluation."
        ),
        "census_input": str(args.census),
        "selection_rule": {
            "required_tree_census_status": COMPLETE,
            "minimum_skill_md_path_count": args.minimum_paths,
            "maximum_skill_md_path_count": args.maximum_paths,
            "rule_basis": "tree metadata only; no source body was read for selection",
        },
        "source_count": len(sources),
        "skill_md_path_count": sum(source["skill_md_path_count"] for source in sources),
        "sources": sources,
        "explicit_exclusions": [
            "Sources with failed or incomplete tree census are recorded non-admissions for this cohort and are not retried here.",
            "Completed origins outside the 3--64 path bound remain unselected for a later bounded cohort; this is not a source-quality verdict.",
            "No artefact body, candidate composition, prompt, gold label, acceptable set, retrieval input, embedding, model result, metric, or empirical conclusion was created.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": "M1_ROUND22_SELECTION_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "census_record_count": len(census),
        "selected_source_count": len(sources),
        "selected_skill_md_path_count": payload["skill_md_path_count"],
        "source_positions": positions,
        "selection_output": str(args.output),
        "exclusions": payload["explicit_exclusions"],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "selected_source_count": summary["selected_source_count"],
        "selected_skill_md_path_count": summary["selected_skill_md_path_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
