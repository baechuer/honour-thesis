#!/usr/bin/env python3
"""Census pinned Round 42 Git trees and apply the declared path bound."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


TEMP_ROOT = Path("/private/tmp/rq1b-round42-m1-2026-08-28")
PLAN_STATUS = "M1_ROUND42_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def run(command: list[str]) -> str:
    completed = subprocess.run(command, text=True, capture_output=True, check=True)
    return completed.stdout.strip()


def tree_root(origin: str, repository_url: str, commit: str) -> Path:
    destination = TEMP_ROOT / origin.replace("/", "--")
    if destination.exists():
        actual = run(["git", "-C", str(destination), "rev-parse", "FETCH_HEAD"])
        if actual != commit:
            raise RuntimeError(f"existing_fetch_head_mismatch:{origin}:{actual}:{commit}")
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "--quiet", str(destination)])
    run(["git", "-C", str(destination), "remote", "add", "origin", repository_url])
    run(["git", "-C", str(destination), "-c", "protocol.version=2", "fetch", "--depth=1", "--filter=blob:none", "origin", commit])
    actual = run(["git", "-C", str(destination), "rev-parse", "FETCH_HEAD"])
    if actual != commit:
        raise RuntimeError(f"pinned_commit_mismatch:{origin}:{actual}:{commit}")
    return destination


def skill_paths(root: Path, commit: str) -> list[str]:
    names = run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", commit]).splitlines()
    return [name for name in names if name == "SKILL.md" or name.endswith("/SKILL.md")]


def census(args: argparse.Namespace) -> int:
    plan: dict[str, Any] = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("status") != PLAN_STATUS:
        raise SystemExit(f"unexpected_plan_status:{plan.get('status')}")
    sources = list(plan.get("sources", []))
    previous = {int(row["plan_position"]): row for row in (read_jsonl(args.output) if args.output.exists() else [])}
    if not set(previous).issubset(set(range(1, len(sources) + 1))):
        raise SystemExit("invalid_census_checkpoint")

    rows: list[dict[str, Any]] = []
    for number, source in enumerate(sources, start=1):
        record = previous.get(number)
        if record is None:
            try:
                root = tree_root(str(source["origin"]), str(source["repository_url"]), str(source["pinned_commit"]))
                paths = skill_paths(root, str(source["pinned_commit"]))
                record = {
                    "plan_position": number,
                    "round42_source_candidate_id": source["round42_source_candidate_id"],
                    "origin": source["origin"],
                    "repository_url": source["repository_url"],
                    "pinned_commit": source["pinned_commit"],
                    "skill_md_path_count": len(paths),
                    "tree_census_status": "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT",
                }
            except Exception as error:
                record = {
                    "plan_position": number,
                    "round42_source_candidate_id": source["round42_source_candidate_id"],
                    "origin": source["origin"],
                    "repository_url": source["repository_url"],
                    "pinned_commit": source["pinned_commit"],
                    "skill_md_path_count": None,
                    "tree_census_status": "M1_TREE_CENSUS_FAILED_NOT_ADMITTED_NOT_A_RESULT",
                    "error": f"{type(error).__name__}:{error}",
                }
        rows.append(record)
        write_jsonl(args.output, rows)
        if number not in previous and (number % 5 == 0 or number == len(sources)):
            print(json.dumps({"M1_TREE_CENSUS_PROGRESS": f"{number}/{len(sources)}", "origin": source["origin"], "status": record["tree_census_status"]}, sort_keys=True), flush=True)
    summary = {
        "status": "M1_ROUND42_TREE_CENSUS_COMPLETE_NOT_A_SOURCE_BODY_ADMISSION_OR_RESULT",
        "source_count": len(rows),
        "complete_count": sum(row["tree_census_status"].startswith("M1_TREE_CENSUS_COMPLETE") for row in rows),
        "failed_count": sum(row["tree_census_status"].startswith("M1_TREE_CENSUS_FAILED") for row in rows),
        "skill_md_path_count": sum(int(row["skill_md_path_count"] or 0) for row in rows),
        "exclusions": [
            "Only pinned Git trees were fetched with blob filtering; no SKILL.md body was materialised or executed.",
            "No candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "source_count", "complete_count", "failed_count", "skill_md_path_count")}, sort_keys=True))
    return 0


def select(args: argparse.Namespace) -> int:
    rows = read_jsonl(args.census)
    selected = [
        row for row in rows
        if row.get("tree_census_status") == "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT"
        and args.minimum_paths <= int(row.get("skill_md_path_count") or 0) <= args.maximum_paths
    ]
    selected.sort(key=lambda row: int(row["plan_position"]))
    payload = {
        "status": "M1_ROUND42_BOUNDED_DIVERSE_STAGING_SELECTION_NOT_A_CLUSTER_OR_RESULT",
        "census_input": str(args.census),
        "selection_rule": {
            "required_tree_census_status": "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT",
            "minimum_skill_md_path_count": args.minimum_paths,
            "maximum_skill_md_path_count": args.maximum_paths,
            "rule_basis": "tree metadata only; no source body was read for selection",
        },
        "source_count": len(selected),
        "skill_md_path_count": sum(int(row["skill_md_path_count"]) for row in selected),
        "sources": selected,
        "exclusions": [
            "Failed tree census records are non-admissions and receive no automatic retry.",
            "Completed sources outside the predeclared path bound are not source-quality rejections.",
            "No artifact body, candidate composition, prompt, label, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": "M1_ROUND42_SELECTION_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "census_record_count": len(rows),
        "selected_source_count": len(selected),
        "selected_skill_md_path_count": payload["skill_md_path_count"],
        "source_positions": [int(row["plan_position"]) for row in selected],
        "exclusions": payload["exclusions"],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "selected_source_count", "selected_skill_md_path_count")}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    census_parser = subparsers.add_parser("census")
    census_parser.add_argument("--plan", type=Path, required=True)
    census_parser.add_argument("--output", type=Path, required=True)
    census_parser.add_argument("--summary", type=Path, required=True)
    select_parser = subparsers.add_parser("select")
    select_parser.add_argument("--census", type=Path, required=True)
    select_parser.add_argument("--minimum-paths", type=int, default=3)
    select_parser.add_argument("--maximum-paths", type=int, default=64)
    select_parser.add_argument("--output", type=Path, required=True)
    select_parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    return {"census": census, "select": select}[args.mode](args)


if __name__ == "__main__":
    raise SystemExit(main())
