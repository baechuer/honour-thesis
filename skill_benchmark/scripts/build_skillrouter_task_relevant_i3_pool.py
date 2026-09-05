#!/usr/bin/env python3
"""Build a task-relevant SkillRouter-Eval-Core pool for external I3 parsing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path("skill_benchmark/external/skillrouter_eval_core")
DERIVED = ROOT / "derived"
OUTPUTS = ROOT / "outputs"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-i2", type=Path, default=DERIVED / "representations" / "all_I2.jsonl")
    parser.add_argument("--fts-results", type=Path, default=OUTPUTS / "skillrouter_eval_core_fts_information_layers.json")
    parser.add_argument("--tasks", type=Path, default=DERIVED / "tasks_scored.jsonl")
    parser.add_argument("--relevance", type=Path, default=ROOT / "raw" / "relevance.json")
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--output-jsonl", type=Path, default=DERIVED / "representations" / "skillrouter_task_relevant_pool_top50_I2.jsonl")
    parser.add_argument("--output-report", type=Path, default=OUTPUTS / "skillrouter_task_relevant_i3_pool_top50.md")
    parser.add_argument("--output-json", type=Path, default=OUTPUTS / "skillrouter_task_relevant_i3_pool_top50.json")
    args = parser.parse_args()

    all_rows = read_jsonl(args.all_i2)
    by_id = {str(row["skill_id"]): (index, row) for index, row in enumerate(all_rows)}
    relevance = json.loads(args.relevance.read_text(encoding="utf-8"))
    tasks = read_jsonl(args.tasks)
    fts = json.loads(args.fts_results.read_text(encoding="utf-8"))

    gold_ids: set[str] = set()
    for task in tasks:
        rel = relevance[task["task_id"]]
        gold_ids.update(str(value) for value in (rel.get("core_gt_ids") or rel.get("gt_skill_ids") or []))

    candidate_ids: set[str] = set()
    by_source: dict[str, set[str]] = {}
    max_available_ranking = 0
    for key, rows in (fts.get("results") or {}).items():
        source_set = by_source.setdefault(key, set())
        for row in rows:
            max_available_ranking = max(max_available_ranking, len(row.get("ranking", [])))
            for candidate in row.get("ranking", [])[: args.top_k]:
                skill_id = str(candidate["skill_id"])
                candidate_ids.add(skill_id)
                source_set.add(skill_id)

    pool_ids = sorted(gold_ids | candidate_ids, key=lambda value: by_id.get(value, (10**12, {}))[0])
    missing_ids = [value for value in pool_ids if value not in by_id]
    pool_rows = [by_id[value][1] for value in pool_ids if value in by_id]
    write_jsonl(args.output_jsonl, pool_rows)

    gold_indices = [by_id[value][0] for value in gold_ids if value in by_id]
    candidate_indices = [by_id[value][0] for value in candidate_ids if value in by_id]
    summary = {
        "top_k": args.top_k,
        "task_count": len(tasks),
        "unique_gold_ids": len(gold_ids),
        "unique_candidate_ids": len(candidate_ids),
        "pool_ids": len(pool_ids),
        "pool_rows_written": len(pool_rows),
        "missing_ids": missing_ids,
        "max_available_ranking_per_task": max_available_ranking,
        "effective_top_k": min(args.top_k, max_available_ranking),
        "gold_index_min": min(gold_indices) if gold_indices else None,
        "gold_index_max": max(gold_indices) if gold_indices else None,
        "candidate_index_min": min(candidate_indices) if candidate_indices else None,
        "candidate_index_max": max(candidate_indices) if candidate_indices else None,
        "by_source": {key: len(value) for key, value in sorted(by_source.items())},
        "output_jsonl": str(args.output_jsonl),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# SkillRouter-Eval-Core Task-Relevant I3 Pool",
        "",
        "Purpose: define a fixed candidate universe for external I3M/I3C parsing and reranking, without pretending that the current partial extraction slices are full-library retrieval results.",
        "",
        f"- Source ranking file: `{args.fts_results}`",
        f"- Top-k per task/source ranking: {args.top_k}",
        f"- Effective top-k from stored rankings: {summary['effective_top_k']}",
        f"- Scored tasks: {summary['task_count']}",
        f"- Unique gold skills: {summary['unique_gold_ids']}",
        f"- Unique ranked candidate skills: {summary['unique_candidate_ids']}",
        f"- Total pool rows written: {summary['pool_rows_written']}",
        f"- Output JSONL: `{args.output_jsonl}`",
        "",
        "## Source Contributions",
        "",
        "| Ranking source | Unique candidate skills |",
        "|---|---:|",
    ]
    for key, value in summary["by_source"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This pool supports a fixed-candidate external reranking/ablation experiment. It does not replace a full-library first-stage retrieval experiment.",
            "",
            "Valid use: parse this pool into I3M/I3C, then compare reranking or ranking inside the same candidate universe.",
            "",
            "Invalid use: compare this pool-only result directly against full-library I1/I2/I3H BM25 first-stage retrieval as if the selector-visible universe were identical.",
        ]
    )
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
