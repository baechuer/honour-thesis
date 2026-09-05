#!/usr/bin/env python3
"""Build a deterministic Wave 025 public raw-source roster from M1 paths only.

This is navigation-to-intake planning. It uses no source body, prompt, label,
or retrieval information; capture and byte deduplication later decide admission.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote


EXCLUDED_PATH_PARTS = {"archive", "runtime", "node_modules", ".git"}


def evenly_spaced(paths: list[str], cap: int) -> list[str]:
    if len(paths) <= cap:
        return paths
    indices = {round(index * (len(paths) - 1) / (cap - 1)) for index in range(cap)}
    return [path for index, path in enumerate(paths) if index in indices]


def repository_slug(remote: str) -> str:
    prefix = "https://github.com/"
    if not remote.startswith(prefix) or not remote.endswith(".git"):
        raise ValueError(f"unsupported_public_github_remote:{remote}")
    return remote[len(prefix) : -len(".git")]


def candidate_path(path: str) -> bool:
    return not any(part.lower() in EXCLUDED_PATH_PARTS for part in Path(path).parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--per-root-cap", type=int, default=25)
    parser.add_argument("--status-prefix", default="RQ1B_V3_W25")
    args = parser.parse_args()
    if args.per_root_cap < 2:
        raise SystemExit("per_root_cap_must_be_at_least_two")
    if args.output.exists() or args.summary.exists():
        raise SystemExit("refusing_to_overwrite_existing_w25_intake_draft")

    records = [json.loads(line) for line in args.census.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows: list[dict[str, object]] = []
    root_counts: list[dict[str, object]] = []
    for record in records:
        if record.get("status") != f"{args.status_prefix}_M1_PATH_CENSUS_COMPLETE_NOT_ADMITTED":
            continue
        raw_paths = record.get("selected_skill_paths")
        commit, remote, lane, root_id = record.get("commit"), record.get("remote"), record.get("lane"), record.get("root_id")
        if not isinstance(raw_paths, list) or not all(isinstance(path, str) for path in raw_paths):
            raise SystemExit(f"invalid_paths:{root_id}")
        if not all(isinstance(value, str) for value in (commit, remote, lane, root_id)):
            raise SystemExit(f"invalid_root_metadata:{root_id}")
        filtered = [path for path in raw_paths if candidate_path(path)]
        selected = evenly_spaced(filtered, args.per_root_cap)
        root_counts.append({
            "root_id": root_id,
            "lane": lane,
            "census_path_count": len(raw_paths),
            "filtered_path_count": len(filtered),
            "selected_path_count": len(selected),
            "excluded_navigation_paths": len(raw_paths) - len(filtered),
        })
        slug = repository_slug(remote)
        for ordinal, artifact_path in enumerate(selected, start=1):
            rows.append({
                "artifact_path": artifact_path,
                "category_hint": lane,
                "lane": lane,
                "m1_root_id": root_id,
                "origin_url": f"https://github.com/{slug}",
                "raw_artifact_url": f"https://raw.githubusercontent.com/{slug}/{commit}/{quote(artifact_path, safe='/')}",
                "repository_ref": f"{slug}@{commit}",
                "selection_basis": "Pinned M1 tree path only; deterministic evenly spaced selection after exclusion of archive/runtime/node_modules/Git metadata paths. No raw artifact body was read during roster construction.",
                "selection_ordinal_within_root": ordinal,
                "status": f"{args.status_prefix}_PUBLIC_SOURCE_INTAKE_DRAFT_NOT_A_CLUSTER",
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": f"{args.status_prefix}_PATH_STRATIFIED_INTAKE_DRAFT_COMPLETE_NOT_A_CLUSTER",
        "census": str(args.census),
        "per_root_cap": args.per_root_cap,
        "root_count": len(root_counts),
        "selected_public_raw_artifact_count": len(rows),
        "root_counts": root_counts,
        "boundary": [
            "This is a raw-source fetch roster only.",
            "It is assembled from immutable pinned Git path metadata, not skill text, prompts, labels, results, or retrieval behaviour.",
            "Capture and SHA-256 deduplication alone decide whether a byte-distinct original is admitted as source provenance.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "roots": len(root_counts), "artifacts": len(rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
