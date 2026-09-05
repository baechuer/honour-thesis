#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from field_aware_matching import (  # noqa: E402
    explain_field_set,
    field_aware_pair_score,
    parse_field_set,
)
from run_m6v1_field_aware_reranker import DEFAULT_FIELD_SET_ORDER, guess_failure  # noqa: E402
from run_offline_selectors import evaluate_rows, load_acceptables, load_jsonl, minmax  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_source_row(row: dict[str, Any], rerank_candidates: int) -> list[tuple[str, float]]:
    candidates: list[tuple[str, float]] = []
    for item in row.get("ranking", [])[:rerank_candidates]:
        if isinstance(item, dict):
            candidates.append((item["skill"], float(item.get("score", 0.0))))
        else:
            candidates.append((str(item), 0.0))
    return candidates


def candidate_recall_from_rank(rows: list[dict[str, Any]], k: int) -> float:
    if not rows:
        return 0.0
    hits = 0
    for row in rows:
        rank = row.get("gold_first_stage_rank")
        if isinstance(rank, int) and rank <= k:
            hits += 1
    return hits / len(rows)


def compute_decomposition(
    rows: list[dict[str, Any]],
    r1: dict[str, dict[str, Any]],
    acceptable_by_prompt: dict[str, dict[str, set[str]]],
    candidate_budget: int,
) -> dict[str, Any]:
    total = len(rows)
    conditional_total = 0
    conditional_top1 = 0
    conditional_accept_top1 = 0
    reranker_loss = 0
    final_top1 = 0
    non_main_top1 = 0
    first_stage_top1 = 0
    failure_counts: dict[str, int] = {}

    for row in rows:
        gold = row["gold_skill"]
        acceptable = {gold, *acceptable_by_prompt.get(row["prompt_id"], {}).get("acceptable", set())}
        ranking = row.get("ranking", [])
        top = ranking[0]["skill"] if ranking else None
        if row.get("first_stage_top1") == gold:
            first_stage_top1 += 1
        if top == gold:
            final_top1 += 1
        if top and not r1[top].get("is_main_evaluated"):
            non_main_top1 += 1
        if gold in row.get("candidate_names", []):
            conditional_total += 1
            if top == gold:
                conditional_top1 += 1
            elif top in acceptable:
                conditional_accept_top1 += 1
            else:
                reranker_loss += 1
                key = row.get("failure_guess") or "unknown"
                failure_counts[key] = failure_counts.get(key, 0) + 1

    pct = lambda value: round(value / total, 4) if total else 0.0
    cpct = lambda value: round(value / conditional_total, 4) if conditional_total else 0.0
    return {
        "first_stage_top1_accuracy": pct(first_stage_top1),
        "candidate_recall": {
            f"recall@{candidate_budget}": candidate_recall_from_rank(rows, candidate_budget),
        },
        "conditional_gold_in_candidate_count": conditional_total,
        "conditional_reranker_top1": cpct(conditional_top1),
        "conditional_reranker_acceptable_top1": cpct(conditional_top1 + conditional_accept_top1),
        "reranker_loss_count": reranker_loss,
        "reranker_loss_rate_given_gold_in_candidates": cpct(reranker_loss),
        "final_top1_accuracy_check": pct(final_top1),
        "non_main_final_top1_rate": pct(non_main_top1),
        "failure_guess_counts": dict(sorted(failure_counts.items(), key=lambda item: (-item[1], item[0]))),
    }


def run_field_set(
    source_rows: list[dict[str, Any]],
    field_set_name: str,
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
    rerank_candidates: int,
    base_weight: float,
    field_weight: float,
    ranking_limit: int,
) -> list[dict[str, Any]]:
    enabled = parse_field_set(field_set_name)
    output_rows: list[dict[str, Any]] = []
    for source in source_rows:
        query = source["instruction_text"]
        candidates = normalize_source_row(source, rerank_candidates)
        candidate_names = [skill for skill, _ in candidates]
        base_scores = [score for _, score in candidates]
        base_norm = minmax(base_scores)
        field_results = [
            field_aware_pair_score(query, skill, r1, r2, r3, enabled_fields=enabled)
            for skill in candidate_names
        ]
        field_scores = [result["score"] for result in field_results]
        field_norm = minmax(field_scores)

        reranked: list[dict[str, Any]] = []
        for index, skill in enumerate(candidate_names):
            final_score = base_weight * base_norm[index] + field_weight * field_norm[index]
            reranked.append(
                {
                    "skill": skill,
                    "score": round(final_score, 6),
                    "base_score": round(base_scores[index], 6),
                    "field_score": round(field_scores[index], 6),
                    "components": {
                        key: round(value, 6) for key, value in field_results[index]["components"].items()
                    },
                    "boundary_penalty": round(field_results[index]["boundary_penalty"], 6),
                    "hierarchy_penalty": round(field_results[index]["hierarchy_penalty"], 6),
                }
            )
        reranked.sort(key=lambda item: (-item["score"], item["skill"]))

        row = {
            "prompt_id": source["prompt_id"],
            "family": source["family"],
            "gold_skill": source["gold_skill"],
            "closest_alternatives": source.get("closest_alternatives", []),
            "instruction_text": query,
            "field_set": field_set_name,
            "field_set_groups": explain_field_set(field_set_name),
            "candidate_names": candidate_names,
            "first_stage_ranking": candidate_names,
            "first_stage_top1": source.get("first_stage_top1") or (candidate_names[0] if candidate_names else None),
            "gold_first_stage_rank": source.get("gold_first_stage_rank"),
            "ranking": reranked[:ranking_limit],
            "candidate_count": min(rerank_candidates, len(candidate_names)),
        }
        row["gold_final_rank"] = next(
            (index + 1 for index, item in enumerate(row["ranking"]) if item["skill"] == row["gold_skill"]),
            None,
        )
        row["failure_guess"] = guess_failure(row)
        output_rows.append(row)
    return output_rows


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# M6-v1 Field-Aware Rerank From Existing First-Stage Results",
        "",
        "This report applies the transparent M6-v1 lexical field-aware reranker to a fixed first-stage candidate set recovered from an existing selector output. It is intended for fair second-stage comparisons where the first-stage retriever and candidate budget are held fixed.",
        "",
        "## Configuration",
        "",
        f"- Source result: `{report['source_result']}`",
        f"- Source method: `{report.get('source_method', '')}`",
        f"- Prompt count: {report['prompt_count']}",
        f"- Skill count: {report['skill_count']}",
        f"- Candidate budget: {report['rerank_candidates']}",
        f"- Score blend: {report['base_weight']} first-stage + {report['field_weight']} field-aware",
        "",
        "## Summary",
        "",
        "| Field set | Fields | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Candidate R@K | Conditional top-1 | Reranker loss | Non-main top-1 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report["summary"]:
        metrics = item["metrics"]
        decomp = item["decomposition"]
        recall_key = f"recall@{report['rerank_candidates']}"
        lines.append(
            f"| `{item['field_set']}` | {item['field_set_groups']} | "
            f"{metrics['top1_accuracy']:.1%} | {metrics['acceptable_top1_accuracy']:.1%} | "
            f"{metrics['top5_recall']:.1%} | {metrics['acceptable_top5_recall']:.1%} | "
            f"{metrics['mrr']:.3f} | {decomp['candidate_recall'][recall_key]:.1%} | "
            f"{decomp['conditional_reranker_top1']:.1%} | "
            f"{decomp['reranker_loss_rate_given_gold_in_candidates']:.1%} | "
            f"{metrics['non_main_top1_rate']:.1%} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply M6-v1 reranking to existing first-stage result JSON.")
    parser.add_argument("--source-json", required=True)
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--acceptable-alternatives", default="")
    parser.add_argument("--field-sets", default=",".join(DEFAULT_FIELD_SET_ORDER))
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--base-weight", type=float, default=0.30)
    parser.add_argument("--field-weight", type=float, default=0.70)
    parser.add_argument("--ranking-limit", type=int, default=20)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    source = load_json(Path(args.source_json))
    source_rows = source["results"]
    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    acceptable_path = Path(args.acceptable_alternatives) if args.acceptable_alternatives else None
    acceptable_by_prompt = load_acceptables(acceptable_path)

    start = time.perf_counter()
    report: dict[str, Any] = {
        "source_result": args.source_json,
        "source_method": f"{source.get('embedding_model', '')} + embedding-only top-{args.rerank_candidates}",
        "prompt_count": len(source_rows),
        "skill_count": source.get("metrics", {}).get("scale_skill_count"),
        "source_metrics": source.get("metrics", {}),
        "rerank_candidates": args.rerank_candidates,
        "base_weight": args.base_weight,
        "field_weight": args.field_weight,
        "ranking_limit": args.ranking_limit,
        "summary": [],
        "results": {},
    }

    for field_set in [part.strip() for part in args.field_sets.split(",") if part.strip()]:
        rows = run_field_set(
            source_rows=source_rows,
            field_set_name=field_set,
            r1=r1,
            r2=r2,
            r3=r3,
            rerank_candidates=args.rerank_candidates,
            base_weight=args.base_weight,
            field_weight=args.field_weight,
            ranking_limit=args.ranking_limit,
        )
        selector_visible_tokens = source.get("metrics", {}).get("selector_visible_tokens_approx", 0)
        metrics = evaluate_rows(rows, r1, int(report["skill_count"] or 0), selector_visible_tokens, acceptable_by_prompt)
        decomp = compute_decomposition(rows, r1, acceptable_by_prompt, args.rerank_candidates)
        key = f"m6v1_from_first_stage::{field_set}"
        report["results"][key] = rows
        report["summary"].append(
            {
                "field_set": field_set,
                "field_set_groups": explain_field_set(field_set),
                "result_key": key,
                "metrics": metrics,
                "decomposition": decomp,
            }
        )

    report["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 2)
    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    for item in report["summary"]:
        metrics = item["metrics"]
        decomp = item["decomposition"]
        recall_key = f"recall@{args.rerank_candidates}"
        print(
            f"{Path(args.source_json).stem}/{item['field_set']}: "
            f"top1={metrics['top1_accuracy']:.1%}, "
            f"accept={metrics['acceptable_top1_accuracy']:.1%}, "
            f"top5={metrics['top5_recall']:.1%}, "
            f"mrr={metrics['mrr']:.3f}, "
            f"cand={decomp['candidate_recall'][recall_key]:.1%}, "
            f"cond={decomp['conditional_reranker_top1']:.1%}"
        )


if __name__ == "__main__":
    main()
