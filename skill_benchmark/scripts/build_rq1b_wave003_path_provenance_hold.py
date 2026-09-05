#!/usr/bin/env python3
"""Build a conservative M1 path-level provenance hold for Wave 003 M2 navigation.

This local audit preserves staged source bodies but withholds any body that carries
an attribution/routing marker requiring later path-level provenance review. It is a
mechanical text-marker audit only: it does not inspect semantic similarity, form
candidate units, create prompts/labels, or call a model or retrieval service.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


M1_STATUS = "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER"
PATTERNS = {
    "source_repo": re.compile(r"\bsource_repo\b", re.IGNORECASE),
    "third_party": re.compile(r"\bthird[- ]party\b", re.IGNORECASE),
    "adapted_from": re.compile(r"\badapted from\b", re.IGNORECASE),
    "derived_from": re.compile(r"\bderived from\b", re.IGNORECASE),
    "upstream": re.compile(r"\bupstream\b", re.IGNORECASE),
    "mirror": re.compile(r"\bmirror\b", re.IGNORECASE),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m1-manifest", type=Path, required=True)
    parser.add_argument(
        "--staged-root",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/staged_sources"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    staged_root = args.staged_root.resolve()
    rows = [row for row in read_jsonl(args.m1_manifest.resolve()) if row.get("source_admission_status") == M1_STATUS]
    held: list[dict[str, Any]] = []
    failures: list[str] = []
    for row in rows:
        original = staged_root / str(row["stage_directory"]) / "skills" / str(row["skill_id"]) / "source" / "SKILL.original.md"
        if not original.is_file():
            failures.append(f"missing_staged_original:{row['stage_directory']}/{row['skill_id']}")
            continue
        text = original.read_text(encoding="utf-8")
        matched = [name for name, pattern in PATTERNS.items() if pattern.search(text)]
        if matched:
            held.append(
                {
                    "skill_id": row["skill_id"],
                    "stage_directory": row["stage_directory"],
                    "origin": row["origin"],
                    "source_repository_path": row["source_repository_path"],
                    "matched_markers": matched,
                }
            )
    held.sort(key=lambda row: (str(row["origin"]), str(row["skill_id"])))
    payload = {
        "status": "M1_PATH_LEVEL_PROVENANCE_HOLD_NOT_A_CLUSTER_OR_RESULT" if not failures else "M1_PATH_LEVEL_PROVENANCE_HOLD_INCOMPLETE",
        "m1_input_count": len(rows),
        "held_skill_ids": [row["skill_id"] for row in held],
        "hold_record_count": len(held),
        "eligible_for_m2_navigation_count": len(rows) - len(held),
        "marker_names": sorted(PATTERNS),
        "records": held,
        "integrity_failures": failures,
        "exclusions": [
            "The hold retains byte-preserved M1 sources and makes no rejection or validity judgement.",
            "The audit checks provenance markers only; it does not assess semantic relation or task quality.",
            "No prompt, label, acceptable set, embedding, selector, API call, or retrieval result was created.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("status", "m1_input_count", "hold_record_count", "eligible_for_m2_navigation_count", "integrity_failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
