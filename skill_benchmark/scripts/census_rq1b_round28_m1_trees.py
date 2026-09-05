#!/usr/bin/env python3
"""Census Round 28 ``SKILL.md`` paths from pinned Git trees only.

The census fetches no blobs unless Git metadata itself needs them. It writes a
durable row after each source and records failures as non-admissions without an
automatic retry. It does not stage source bodies or make any cluster claim.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


TEMP_ROOT = Path("/private/tmp/rq1b-round28-m1-2026-08-28")
PLAN_STATUS = "M1_ROUND28_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT"
COMPLETE = "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT"
FAILED = "M1_TREE_CENSUS_FAILED_NOT_ADMITTED_NOT_A_RESULT"


def run(command: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(command, check=True, text=True, capture_output=capture)
    return completed.stdout.strip() if capture else ""


def fetch_tree(origin: str, url: str, commit: str) -> Path:
    target = TEMP_ROOT / origin.replace("/", "--")
    if target.exists():
        actual = run(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"], capture=True)
        if actual != commit:
            raise RuntimeError(f"existing_fetch_head_mismatch:{origin}:{actual}:{commit}")
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "--quiet", str(target)])
    run(["git", "-C", str(target), "remote", "add", "origin", url])
    run(["git", "-C", str(target), "-c", "protocol.version=2", "fetch", "--depth=1", "--filter=blob:none", "origin", commit], capture=True)
    actual = run(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"], capture=True)
    if actual != commit:
        raise RuntimeError(f"pinned_commit_mismatch:{origin}:{actual}:{commit}")
    return target


def read_existing(path: Path) -> dict[int, dict[str, Any]]:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_position = {int(row["plan_position"]): row for row in rows}
    if len(by_position) != len(rows):
        raise ValueError("duplicate_existing_plan_position")
    return by_position


def write(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("status") != PLAN_STATUS:
        raise SystemExit("unexpected_round28_m1_plan_status")
    sources = plan["sources"]
    prior = read_existing(args.output)
    if not set(prior).issubset(set(range(1, len(sources) + 1))):
        raise SystemExit("invalid_existing_tree_checkpoint")

    rows: list[dict[str, Any]] = []
    for position, source in enumerate(sources, start=1):
        row = prior.get(position)
        if row is None:
            origin = str(source["origin"])
            try:
                root = fetch_tree(origin, str(source["repository_url"]), str(source["pinned_commit"]))
                tree = run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", str(source["pinned_commit"])], capture=True)
                paths = [item for item in tree.splitlines() if item == "SKILL.md" or item.endswith("/SKILL.md")]
                row = {"plan_position": position, "origin": origin, "repository_url": source["repository_url"], "pinned_commit": source["pinned_commit"], "skill_md_path_count": len(paths), "tree_census_status": COMPLETE}
            except Exception as error:
                row = {"plan_position": position, "origin": origin, "repository_url": source["repository_url"], "pinned_commit": source["pinned_commit"], "skill_md_path_count": None, "tree_census_status": FAILED, "error": f"{type(error).__name__}:{error}"}
        rows.append(row)
        write(args.output, rows)
        if not args.quiet and (position % 5 == 0 or position == len(sources)):
            print(json.dumps({"M1_TREE_CENSUS_PROGRESS": f"{position}/{len(sources)}", "status": row["tree_census_status"]}, sort_keys=True), flush=True)
    summary = {
        "status": "M1_ROUND28_TREE_CENSUS_COMPLETE_NOT_A_SOURCE_BODY_ADMISSION_OR_RESULT",
        "plan": str(args.plan),
        "source_count": len(rows),
        "complete_count": sum(row["tree_census_status"] == COMPLETE for row in rows),
        "failed_count": sum(row["tree_census_status"] == FAILED for row in rows),
        "skill_md_path_count": sum(int(row["skill_md_path_count"] or 0) for row in rows),
        "exclusions": [
            "Only pinned Git trees were fetched; no SKILL.md body was materialised or executed.",
            "No candidate composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "source_count", "complete_count", "failed_count", "skill_md_path_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
