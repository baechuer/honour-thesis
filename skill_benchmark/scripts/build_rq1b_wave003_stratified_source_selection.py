#!/usr/bin/env python3
"""Make a deterministic source-only SKILL.md selection for Wave 003 staging.

This is not semantic clustering. It prevents a very large, single-domain
repository from satisfying the candidate-pool count by itself. The output only
names repository-relative source paths for later byte-preserving staging.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--target-count", type=int, required=True)
    parser.add_argument(
        "--stratum-marker",
        default="skills",
        help="Directory name after which the skill directory begins (default: skills).",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def stratum_for(path: Path, root: Path, marker: str) -> str:
    parts = path.relative_to(root).parts
    if marker not in parts:
        return "unclassified"
    index = parts.index(marker)
    return "/".join(parts[:index]) or "root"


def main() -> int:
    args = parse_args()
    root = args.source_root.resolve()
    if args.target_count <= 0:
        raise SystemExit("--target-count must be positive")
    if not root.is_dir():
        raise SystemExit(f"Missing source root: {root}")

    groups: dict[str, deque[Path]] = defaultdict(deque)
    for path in sorted(root.rglob("SKILL.md")):
        if ".git" in path.parts:
            continue
        groups[stratum_for(path, root, args.stratum_marker)].append(path)
    if not groups:
        raise SystemExit("No SKILL.md files found")

    selected: list[Path] = []
    while len(selected) < args.target_count and any(groups.values()):
        for stratum in sorted(groups):
            if groups[stratum] and len(selected) < args.target_count:
                selected.append(groups[stratum].popleft())
    if len(selected) < args.target_count:
        raise SystemExit(f"Only {len(selected)} source files available for target {args.target_count}")

    payload = {
        "status": "SOURCE_ONLY_DETERMINISTIC_STRATIFIED_SELECTION_NOT_A_CLUSTER_OR_RESULT",
        "source_root_basename": root.name,
        "target_count": args.target_count,
        "stratum_marker": args.stratum_marker,
        "available_skill_files": sum(len(values) for values in groups.values()) + len(selected),
        "selected_count": len(selected),
        "selected_stratum_counts": {
            stratum: sum(stratum_for(path, root, args.stratum_marker) == stratum for path in selected)
            for stratum in sorted({stratum_for(path, root, args.stratum_marker) for path in selected})
        },
        "selection_rule": (
            "round-robin over lexicographically sorted strata, then lexicographically "
            "sorted repository-relative SKILL.md paths; no task, prompt, label, model, "
            "or retrieval information is read or used"
        ),
        "paths": [path.relative_to(root).as_posix() for path in selected],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("available_skill_files", "selected_count", "selected_stratum_counts")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
