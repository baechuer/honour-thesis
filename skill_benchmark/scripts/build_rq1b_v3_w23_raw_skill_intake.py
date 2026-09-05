#!/usr/bin/env python3
"""Build a path-only W23 public skill intake roster from pinned local clones."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STATUS = "RQ1B_V3_W23_PUBLIC_SOURCE_INTAKE_DRAFT_NOT_A_CLUSTER"


def argument(value: str) -> tuple[Path, str, str, str, int, set[str]]:
    parts = value.split("|", 5)
    if len(parts) != 6:
        raise argparse.ArgumentTypeError("source_must_be_root|origin_url|commit|lane|max_per_group|excluded_groups_csv")
    root, origin_url, commit, lane, cap_text, excluded = parts
    try:
        cap = int(cap_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("max_per_group_must_be_integer") from error
    if not root or not origin_url.startswith("https://github.com/") or not commit or not lane or cap < 1:
        raise argparse.ArgumentTypeError("invalid_source_argument")
    return Path(root), origin_url.rstrip("/"), commit, lane, cap, {item for item in excluded.split(",") if item}


def group_for(relative: Path) -> str:
    return relative.parts[1] if len(relative.parts) >= 3 and relative.parts[0] == "skills" else "root"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=argument, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_existing_output")

    rows: list[dict[str, object]] = []
    for root, origin_url, commit, lane, cap, excluded in args.source:
        if not root.is_dir():
            raise SystemExit(f"missing_clone_root:{root}")
        selected_by_group: dict[str, int] = {}
        for skill_path in sorted(root.glob("**/SKILL.md")):
            relative = skill_path.relative_to(root)
            group = group_for(relative)
            if group in excluded or selected_by_group.get(group, 0) >= cap:
                continue
            selected_by_group[group] = selected_by_group.get(group, 0) + 1
            raw_url = f"https://raw.githubusercontent.com/{origin_url.removeprefix('https://github.com/')}/{commit}/{relative.as_posix()}"
            rows.append(
                {
                    "status": STATUS,
                    "lane": lane,
                    "origin_url": origin_url,
                    "repository_ref": f"{origin_url.removeprefix('https://github.com/')}@{commit}",
                    "artifact_path": relative.as_posix(),
                    "raw_artifact_url": raw_url,
                    "selection_basis": "Pinned local clone path metadata only; no skill body was read during roster construction.",
                    "category_hint": group,
                }
            )
    urls = [str(row["raw_artifact_url"]) for row in rows]
    if len(urls) != len(set(urls)):
        raise SystemExit("duplicate_raw_url")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    print(json.dumps({"status": "RQ1B_V3_W23_PATH_ROSTER_COMPLETE_NOT_A_CLUSTER", "row_count": len(rows), "origins": len({row['origin_url'] for row in rows})}, sort_keys=True))


if __name__ == "__main__":
    main()
