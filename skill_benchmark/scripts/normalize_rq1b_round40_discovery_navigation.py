#!/usr/bin/env python3
"""Normalise Round 40 navigation-only discovery lists for the existing M0 gate.

The six discovery agents return one public repository with one or more proposed
``SKILL.md`` paths.  M0 operates one path-hint per lead, so this script expands
that list without asserting that a path exists or reading any source body.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_INPUT = {
    "lane",
    "repository_url",
    "suggested_skill_paths",
    "discovery_rationale",
    "search_method",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise SystemExit(f"non_object_json:{path}:{line_number}")
        missing = sorted(key for key in REQUIRED_INPUT if key not in value)
        if missing:
            raise SystemExit(f"missing_input_fields:{path}:{line_number}:{','.join(missing)}")
        rows.append(value)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    output: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    source_rows = read_jsonl(args.input)
    for line_number, row in enumerate(source_rows, 1):
        paths = row["suggested_skill_paths"]
        if not isinstance(paths, list) or not paths:
            dropped.append({"source_line_number": line_number, "reason": "missing_suggested_paths"})
            continue
        for path in paths:
            if not isinstance(path, str) or not path.strip():
                dropped.append({"source_line_number": line_number, "reason": "blank_or_nonstring_path"})
                continue
            clean_path = path.strip().lstrip("/")
            root = str(row["repository_url"]).rstrip("/")
            output.append({
                "repository_url": root,
                "source_repository_path": clean_path,
                "skill_locator_url": f"{root}/blob/HEAD/{clean_path}",
                "skill_title_or_name": clean_path,
                "capability_summary": f"Navigation-only candidate path {clean_path}; source body has not been read.",
                "discovery_domain": str(row["lane"]),
                "discovery_rationale": str(row["discovery_rationale"]),
                "source_ref_or_commit": None,
                "search_method": str(row["search_method"]),
                "normalisation_status": "M0_PATH_HINT_EXPANDED_FROM_NAVIGATION_ONLY_NOT_SOURCE_VERIFIED",
                "exclusions": [
                    "The proposed path is a discovery hint only; M0 has not fetched or read source content.",
                    "Path existence, source suitability, candidate composition, prompt, label, and any empirical result remain unverified.",
                ],
            })

    write_jsonl(args.output, output)
    summary = {
        "status": "M0_ROUND40_NAVIGATION_PATH_HINTS_NORMALIZED_NOT_SOURCE_VERIFIED_NOT_A_CLUSTER_OR_RESULT",
        "input_repository_rows": len(source_rows),
        "output_path_hint_rows": len(output),
        "dropped_path_entries": dropped,
        "input": str(args.input),
        "output": str(args.output),
        "exclusions": [
            "Normalisation only changes navigation-list shape; it does not validate a repository, path, source body, or capability.",
            "No candidate composition, prompt, label, model call, retrieval input, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "input_repository_rows": summary["input_repository_rows"],
        "output_path_hint_rows": summary["output_path_hint_rows"],
        "dropped_path_entry_count": len(dropped),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
