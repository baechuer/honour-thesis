#!/usr/bin/env python3
"""Build chunked RQ1a selector inputs for Codex subagent diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_rq1a_llm_selector import build_tasks, discover_suites  # noqa: E402


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def compact_case(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": f"{task['prompt_id']}::{task['condition']}",
        "field": task["field"],
        "prompt_variant": task["prompt_variant"],
        "condition": task["condition"],
        "selector_prompt": task["selector_prompt"],
    }


def answer_row(task: dict[str, Any]) -> dict[str, Any]:
    gold_label = next(
        label for label, skill_id in task["candidate_map"].items() if skill_id == task["gold_skill_id"]
    )
    return {
        "case_id": f"{task['prompt_id']}::{task['condition']}",
        "field": task["field"],
        "prompt_variant": task["prompt_variant"],
        "condition": task["condition"],
        "gold_label": gold_label,
        "gold_skill_id": task["gold_skill_id"],
        "candidate_map": task["candidate_map"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suites", default="all")
    parser.add_argument("--conditions", default="shared_context_only,shared_context_plus_field")
    parser.add_argument("--chunk-size", type=int, default=100)
    parser.add_argument("--output-dir", default="skill_benchmark/outputs/rq1a_subagent_selector_batches")
    args = parser.parse_args()

    root = repo_root()
    suite_dirs = discover_suites(root, args.suites)
    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]
    tasks = build_tasks(suite_dirs, conditions)

    output_dir = (Path.cwd() / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "rq1a_subagent_selector_batches_v1",
        "conditions": conditions,
        "chunk_size": args.chunk_size,
        "total_cases": len(tasks),
        "chunks": [],
    }
    answer_key = {"schema_version": "rq1a_subagent_selector_answer_key_v1", "answers": []}

    for index in range(0, len(tasks), args.chunk_size):
        chunk_tasks = tasks[index : index + args.chunk_size]
        chunk_id = f"chunk_{index // args.chunk_size:03d}"
        input_path = output_dir / f"{chunk_id}.input.json"
        output_path = output_dir / f"{chunk_id}.output.json"
        cases = [compact_case(task) for task in chunk_tasks]
        input_path.write_text(
            json.dumps(
                {
                    "schema_version": "rq1a_subagent_selector_chunk_v1",
                    "chunk_id": chunk_id,
                    "instructions": (
                        "For each case, use only selector_prompt content. "
                        "Return ambiguous when candidates are indistinguishable. "
                        "Write the output JSON file requested by the main agent."
                    ),
                    "cases": cases,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        manifest["chunks"].append(
            {
                "chunk_id": chunk_id,
                "input_path": str(input_path),
                "output_path": str(output_path),
                "case_count": len(cases),
            }
        )
        answer_key["answers"].extend(answer_row(task) for task in chunk_tasks)

    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (output_dir / "answer_key.local.json").write_text(json.dumps(answer_key, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "chunks": len(manifest["chunks"]), "cases": len(tasks)}, indent=2))


if __name__ == "__main__":
    main()
