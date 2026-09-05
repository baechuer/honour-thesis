#!/usr/bin/env python3
"""Fetch pinned Git trees and count SKILL.md paths for Round 18 M1 scheduling.

No SKILL.md blob is intentionally materialised by this census. It is only a
public-tree volume inventory used to schedule later byte staging.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "rq1b_cross_source_public_benchmark" / "manifest" / "m1_round18_source_batch_plan_2026-08-27.json"
TEMP_ROOT = Path("/private/tmp/rq1b-round18-m1-2026-08-27")


def command(args: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(args, check=True, text=True, capture_output=capture)
    return completed.stdout.strip() if capture else ""


def checkout_root(origin: str) -> Path:
    return TEMP_ROOT / origin.replace("/", "--")


def ensure_tree(origin: str, url: str, commit: str) -> Path:
    target = checkout_root(origin)
    if target.exists():
        actual = command(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"], capture=True)
        if actual != commit:
            raise RuntimeError(f"existing_fetch_head_mismatch:{actual}:{commit}")
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    command(["git", "init", "--quiet", str(target)])
    command(["git", "-C", str(target), "remote", "add", "origin", url])
    command(["git", "-C", str(target), "-c", "protocol.version=2", "fetch", "--depth=1", "--filter=blob:none", "origin", commit])
    actual = command(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"], capture=True)
    if actual != commit:
        raise RuntimeError(f"pinned_commit_mismatch:{actual}:{commit}")
    return target


def existing_rows(path: Path) -> dict[int, dict[str, Any]]:
    if not path.exists():
        return {}
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {int(row["plan_position"]): row for row in records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("status") != "M1_BATCH_PLAN_PINNED_NOT_YET_STAGED_NOT_A_CLUSTER_OR_RESULT":
        raise SystemExit("unexpected_round18_m1_plan_status")
    prior = existing_rows(args.output)
    rows: list[dict[str, Any]] = []
    for position, source in enumerate(plan["sources"], start=1):
        if position in prior:
            rows.append(prior[position])
            continue
        origin = str(source["origin"])
        url = str(source["repository_url"])
        commit = str(source["pinned_commit"])
        try:
            root = ensure_tree(origin, url, commit)
            tree = command(["git", "-C", str(root), "ls-tree", "-r", "--name-only", commit], capture=True)
            paths = [path for path in tree.splitlines() if path == "SKILL.md" or path.endswith("/SKILL.md")]
            row: dict[str, Any] = {
                "plan_position": position,
                "origin": origin,
                "repository_url": url,
                "pinned_commit": commit,
                "skill_md_path_count": len(paths),
                "tree_census_status": "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT",
            }
        except Exception as error:  # record once; no automatic retry
            row = {
                "plan_position": position,
                "origin": origin,
                "repository_url": url,
                "pinned_commit": commit,
                "skill_md_path_count": None,
                "tree_census_status": "M1_TREE_CENSUS_FAILED_NOT_ADMITTED_NOT_A_RESULT",
                "error": f"{type(error).__name__}:{error}",
            }
        rows.append(row)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("".join(json.dumps(item, ensure_ascii=True, sort_keys=True) + "\n" for item in rows), encoding="utf-8")
        print(json.dumps({"CENSUS_PROGRESS": f"{position}/{len(plan['sources'])}", "origin": origin, "status": row["tree_census_status"], "skill_md_path_count": row["skill_md_path_count"]}, sort_keys=True), flush=True)
    totals = {
        "source_count": len(rows),
        "census_complete_count": sum(row["tree_census_status"] == "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT" for row in rows),
        "census_failed_count": sum(row["tree_census_status"] == "M1_TREE_CENSUS_FAILED_NOT_ADMITTED_NOT_A_RESULT" for row in rows),
        "skill_md_path_count": sum(int(row["skill_md_path_count"] or 0) for row in rows),
    }
    summary = {
        "status": "M1_TREE_CENSUS_COMPLETE_NOT_A_SOURCE_ADMISSION_OR_RESULT",
        "plan": str(PLAN),
        "totals": totals,
        "exclusions": [
            "The census fetches pinned Git trees only; it is not source-body staging.",
            "No source content was executed, and no composition, prompt, label, retrieval input, model result, or metric was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "totals": totals}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
