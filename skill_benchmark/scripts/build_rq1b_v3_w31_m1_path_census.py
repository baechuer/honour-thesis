#!/usr/bin/env python3
"""Build Wave 031's pinned path census from GitHub tree metadata only.

This is a navigation-stage tool.  It deliberately reads neither raw skill
artifacts nor any cluster, prompt, label, or retrieval material.  Raw source
capture is a later one-shot operation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EXCLUDED_PATH_PARTS = {"archive", "runtime", "node_modules", ".git"}


def parse_root(value: str) -> tuple[Path, Path, str, str, str]:
    """Parse tree_path|commit_path|remote|lane|root_id without reading bodies."""
    parts = value.split("|", 4)
    if len(parts) != 5:
        raise argparse.ArgumentTypeError("root_must_be_tree|commit|remote|lane|root_id")
    tree_path, commit_path, remote, lane, root_id = parts
    if not all((tree_path, commit_path, remote, lane, root_id)):
        raise argparse.ArgumentTypeError("root_argument_has_empty_component")
    if not remote.startswith("https://github.com/") or not remote.endswith(".git"):
        raise argparse.ArgumentTypeError("root_remote_must_be_github_dot_git")
    return Path(tree_path), Path(commit_path), remote, lane, root_id


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"json_object_required:{path}")
    return value


def eligible_path(path: str) -> bool:
    return not any(part.lower() in EXCLUDED_PATH_PARTS for part in Path(path).parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=parse_root, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--path-cap", type=int, default=100)
    parser.add_argument("--status-prefix", default="RQ1B_V3_W31")
    args = parser.parse_args()
    if args.path_cap < 2:
        raise SystemExit("path_cap_must_be_at_least_two")
    if args.output.exists() or args.summary.exists():
        raise SystemExit("refusing_to_overwrite_existing_w31_m1_outputs")

    records: list[dict[str, object]] = []
    for tree_path, commit_path, remote, lane, root_id in args.root:
        tree = read_json(tree_path)
        commit = read_json(commit_path)
        if tree.get("truncated") is not False:
            raise SystemExit(f"tree_not_complete:{root_id}")
        commit_sha = commit.get("sha")
        tree_sha = tree.get("sha")
        if not isinstance(commit_sha, str) or not commit_sha:
            raise SystemExit(f"missing_commit_sha:{root_id}")
        if not isinstance(tree_sha, str) or not tree_sha:
            raise SystemExit(f"missing_tree_sha:{root_id}")
        raw_paths = sorted(
            str(item["path"])
            for item in tree.get("tree", [])
            if isinstance(item, dict)
            and item.get("type") == "blob"
            and (item.get("path") == "SKILL.md" or str(item.get("path", "")).endswith("/SKILL.md"))
            and eligible_path(str(item["path"]))
        )
        if not raw_paths:
            raise SystemExit(f"no_eligible_skill_paths:{root_id}")
        selected = raw_paths[: args.path_cap]
        records.append(
            {
                "status": f"{args.status_prefix}_M1_PATH_CENSUS_COMPLETE_NOT_ADMITTED",
                "root_id": root_id,
                "lane": lane,
                "remote": remote,
                "commit": commit_sha,
                "tree_sha": tree_sha,
                "tree_metadata_path": str(tree_path),
                "commit_metadata_path": str(commit_path),
                "skill_path_count": len(raw_paths),
                "path_cap": args.path_cap,
                "path_cap_applied": len(raw_paths) > args.path_cap,
                "selected_skill_paths": selected,
                "attempt_policy": "ONE_SHOT_NO_AUTO_RETRY",
                "inspection_boundary": "Pinned Git commit and complete tree paths only; no raw skill artifact body was read or executed.",
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    summary = {
        "status": f"{args.status_prefix}_M1_PATH_CENSUS_COMPLETE_NOT_ADMITTED",
        "root_count": len(records),
        "eligible_skill_path_count": sum(int(record["skill_path_count"]) for record in records),
        "selected_path_count": sum(len(record["selected_skill_paths"]) for record in records),
        "path_cap": args.path_cap,
        "boundary": "Navigation metadata only. This does not retrieve raw skills, admit a source, propose a composition, form a cluster, create a prompt, assign a label, run a selector, or compute a result.",
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
