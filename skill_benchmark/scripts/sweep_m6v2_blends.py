#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_m6v1_field_aware_reranker import guess_failure  # noqa: E402
from run_offline_selectors import evaluate_rows, load_acceptables, load_jsonl  # noqa: E402


DEFAULT_SOURCES = [
    (
        "controlled",
        "qwen",
        "r1",
        "skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r1_m6v2_top20.json",
        "skill_benchmark/annotations/acceptable_alternatives.json",
    ),
    (
        "controlled",
        "qwen",
        "r2",
        "skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r2_m6v2_top20.json",
        "skill_benchmark/annotations/acceptable_alternatives.json",
    ),
    (
        "controlled",
        "qwen",
        "full",
        "skill_benchmark/outputs/frozen_v0_4_controlled_qwen_full_m6v2_top20.json",
        "skill_benchmark/annotations/acceptable_alternatives.json",
    ),
    (
        "public_gold",
        "qwen",
        "r1",
        "skill_benchmark/outputs/frozen_v0_4_public_gold_qwen_r1_m6v2_top20.json",
        "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    ),
    (
        "public_gold",
        "qwen",
        "r2",
        "skill_benchmark/outputs/frozen_v0_4_public_gold_qwen_r2_m6v2_top20.json",
        "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    ),
    (
        "public_gold",
        "qwen",
        "full",
        "skill_benchmark/outputs/frozen_v0_4_public_gold_qwen_full_m6v2_top20.json",
        "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    ),
    (
        "controlled",
        "skillrouter",
        "r1",
        "skill_benchmark/outputs/frozen_v0_4_controlled_skillrouter_r1_m6v2_task_top20.json",
        "skill_benchmark/annotations/acceptable_alternatives.json",
    ),
    (
        "controlled",
        "skillrouter",
        "r2",
        "skill_benchmark/outputs/frozen_v0_4_controlled_skillrouter_r2_m6v2_task_top20.json",
        "skill_benchmark/annotations/acceptable_alternatives.json",
    ),
    (
        "controlled",
        "skillrouter",
        "full",
        "skill_benchmark/outputs/frozen_v0_4_controlled_skillrouter_full_m6v2_task_top20.json",
        "skill_benchmark/annotations/acceptable_alternatives.json",
    ),
    (
        "public_gold",
        "skillrouter",
        "r1",
        "skill_benchmark/outputs/frozen_v0_4_public_gold_skillrouter_r1_m6v2_task_top20.json",
        "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    ),
    (
        "public_gold",
        "skillrouter",
        "r2",
        "skill_benchmark/outputs/frozen_v0_4_public_gold_skillrouter_r2_m6v2_task_top20.json",
        "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    ),
    (
        "public_gold",
        "skillrouter",
        "full",
        "skill_benchmark/outputs/frozen_v0_4_public_gold_skillrouter_full_m6v2_task_top20.json",
        "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    ),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_float_grid(raw: str) -> list[float]:
    values = [round(float(part.strip()), 6) for part in raw.split(",") if part.strip()]
    if not values:
        raise ValueError("Grid cannot be empty.")
    return values


def rescore_rows(
    rows: list[dict[str, Any]],
    base_weight: float,
    penalty_scale: float,
) -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    field_weight = 1.0 - base_weight
    for row in rows:
        reranked: list[dict[str, Any]] = []
        for item in row["ranking"]:
            penalty_delta = float(item.get("exclusion_bonus", 0.0)) - float(item.get("total_penalty", 0.0))
            score = (
                base_weight * float(item.get("base_norm", 0.0))
                + field_weight * float(item.get("semantic_positive_norm", 0.0))
                + penalty_scale * penalty_delta
            )
            new_item = dict(item)
            new_item["score"] = round(score, 6)
            new_item["sweep_base_weight"] = base_weight
            new_item["sweep_field_weight"] = round(field_weight, 6)
            new_item["sweep_penalty_scale"] = penalty_scale
            reranked.append(new_item)
        reranked.sort(key=lambda entry: (-entry["score"], entry["skill"]))
        new_row = dict(row)
        new_row["ranking"] = reranked
        new_row["gold_final_rank"] = next(
            (index + 1 for index, item in enumerate(reranked) if item["skill"] == row["gold_skill"]),
            None,
        )
        new_row["failure_guess"] = guess_failure(new_row)
        output_rows.append(new_row)
    return output_rows


def split_rows(rows: list[dict[str, Any]], split: str, dev_fraction: float) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    threshold = int(dev_fraction * 1000)
    for row in rows:
        digest = hashlib.sha256(str(row["prompt_id"]).encode("utf-8")).hexdigest()
        bucket = int(digest[:8], 16) % 1000
        is_dev = bucket < threshold
        if (split == "dev" and is_dev) or (split == "test" and not is_dev):
            output.append(row)
    return output


def candidate_recall(rows: list[dict[str, Any]], k: int) -> float:
    if not rows:
        return 0.0
    hits = 0
    for row in rows:
        rank = row.get("gold_first_stage_rank")
        if isinstance(rank, int) and rank <= k:
            hits += 1
    return hits / len(rows)


def evaluate_source(
    source: tuple[str, str, str, str, str],
    r1: dict[str, dict[str, Any]],
    base_weights: list[float],
    penalty_scales: list[float],
    dev_fraction: float,
) -> dict[str, Any] | None:
    stratum, candidate_source, representation, source_json, acceptable_path = source
    path = Path(source_json)
    if not path.exists():
        return None
    report = load_json(path)
    acceptable_by_prompt = load_acceptables(Path(acceptable_path))
    skill_count = int(report.get("skill_count") or report.get("source_metrics", {}).get("scale_skill_count") or 0)
    selector_visible_tokens = report.get("source_metrics", {}).get("selector_visible_tokens_approx", 0)
    rerank_candidates = int(report.get("rerank_candidates", 20))
    source_rows: list[dict[str, Any]] = []
    for summary in report["summary"]:
        field_set = summary["field_set"]
        result_key = summary["result_key"]
        rows = report["results"][result_key]
        source_rows.append(
            {
                "field_set": field_set,
                "source_metrics": summary["metrics"],
                "source_decomposition": summary["decomposition"],
                "rows": rows,
            }
        )

    sweep_rows: list[dict[str, Any]] = []
    dev_sweep_rows: list[dict[str, Any]] = []
    for field_block in source_rows:
        for base_weight in base_weights:
            for penalty_scale in penalty_scales:
                rows = rescore_rows(field_block["rows"], base_weight, penalty_scale)
                metrics = evaluate_rows(rows, r1, skill_count, selector_visible_tokens, acceptable_by_prompt)
                row_payload = {
                    "stratum": stratum,
                    "candidate_source": candidate_source,
                    "representation": representation,
                    "source_json": source_json,
                    "field_set": field_block["field_set"],
                    "base_weight": base_weight,
                    "field_weight": round(1.0 - base_weight, 6),
                    "penalty_scale": penalty_scale,
                    "candidate_recall_at_k": candidate_recall(rows, rerank_candidates),
                    "metrics": metrics,
                }
                sweep_rows.append(row_payload)

                dev_rows = split_rows(rows, "dev", dev_fraction)
                test_rows = split_rows(rows, "test", dev_fraction)
                dev_metrics = evaluate_rows(dev_rows, r1, skill_count, selector_visible_tokens, acceptable_by_prompt)
                test_metrics = evaluate_rows(test_rows, r1, skill_count, selector_visible_tokens, acceptable_by_prompt)
                dev_sweep_rows.append(
                    {
                        **row_payload,
                        "dev_prompt_count": len(dev_rows),
                        "test_prompt_count": len(test_rows),
                        "dev_metrics": dev_metrics,
                        "test_metrics": test_metrics,
                    }
                )

    best_top1 = max(sweep_rows, key=lambda item: item["metrics"]["top1_accuracy"])
    best_mrr = max(sweep_rows, key=lambda item: item["metrics"]["mrr"])
    best_accept = max(sweep_rows, key=lambda item: item["metrics"]["acceptable_top1_accuracy"])
    best_dev_top1 = max(dev_sweep_rows, key=lambda item: item["dev_metrics"]["top1_accuracy"])
    best_dev_mrr = max(dev_sweep_rows, key=lambda item: item["dev_metrics"]["mrr"])
    return {
        "stratum": stratum,
        "candidate_source": candidate_source,
        "representation": representation,
        "source_json": source_json,
        "rerank_candidates": rerank_candidates,
        "sweep_rows": sweep_rows,
        "best_top1": best_top1,
        "best_mrr": best_mrr,
        "best_accept_top1": best_accept,
        "best_dev_top1": best_dev_top1,
        "best_dev_mrr": best_dev_mrr,
    }


def pct(value: float) -> str:
    return f"{value:.1%}"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# M6-v2 Blend Sweep",
        "",
        "This report rescales existing M6-v2 candidate-level outputs without making new embedding API calls. It varies the blend between first-stage score and semantic field score, plus the penalty scale. This is a diagnostic calibration sweep, not a final tuned result unless a held-out development split is later used.",
        "",
        "Formula:",
        "",
        "```text",
        "score = base_weight * base_norm + (1 - base_weight) * semantic_field_norm + penalty_scale * (exclusion_bonus - total_penalty)",
        "```",
        "",
        f"- Base-weight grid: {', '.join(str(v) for v in report['base_weights'])}",
        f"- Penalty-scale grid: {', '.join(str(v) for v in report['penalty_scales'])}",
        "",
        "## Best Top-1 Per Source",
        "",
        "| Stratum | Candidate source | Representation | Field set | Base weight | Field weight | Penalty scale | Top-1 | Accept Top-1 | Top-5 | MRR | Cand R@20 |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report["sources"]:
        best = item["best_top1"]
        metrics = best["metrics"]
        lines.append(
            f"| {item['stratum']} | {item['candidate_source']} | {item['representation'].upper()} | "
            f"`{best['field_set']}` | {best['base_weight']:.2f} | {best['field_weight']:.2f} | "
            f"{best['penalty_scale']:.2f} | {pct(metrics['top1_accuracy'])} | "
            f"{pct(metrics['acceptable_top1_accuracy'])} | {pct(metrics['top5_recall'])} | "
            f"{metrics['mrr']:.3f} | {pct(best['candidate_recall_at_k'])} |"
        )

    lines.extend(
        [
            "",
            "## Best MRR Per Source",
            "",
            "| Stratum | Candidate source | Representation | Field set | Base weight | Field weight | Penalty scale | Top-1 | Accept Top-1 | Top-5 | MRR |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in report["sources"]:
        best = item["best_mrr"]
        metrics = best["metrics"]
        lines.append(
            f"| {item['stratum']} | {item['candidate_source']} | {item['representation'].upper()} | "
            f"`{best['field_set']}` | {best['base_weight']:.2f} | {best['field_weight']:.2f} | "
            f"{best['penalty_scale']:.2f} | {pct(metrics['top1_accuracy'])} | "
            f"{pct(metrics['acceptable_top1_accuracy'])} | {pct(metrics['top5_recall'])} | "
            f"{metrics['mrr']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Dev-Selected Blend, Test-Set Result",
            "",
            "These rows choose the best setting on a deterministic prompt-ID development split and report its held-out test result. This is still a lightweight calibration check, but it is safer than choosing weights on the full evaluation set.",
            "",
            f"- Development fraction: {report['dev_fraction']:.0%}",
            "",
            "| Stratum | Candidate source | Representation | Dev-selected field set | Base weight | Field weight | Penalty scale | Dev Top-1 | Test Top-1 | Test Accept Top-1 | Test Top-5 | Test MRR |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in report["sources"]:
        best = item["best_dev_top1"]
        dev_metrics = best["dev_metrics"]
        test_metrics = best["test_metrics"]
        lines.append(
            f"| {item['stratum']} | {item['candidate_source']} | {item['representation'].upper()} | "
            f"`{best['field_set']}` | {best['base_weight']:.2f} | {best['field_weight']:.2f} | "
            f"{best['penalty_scale']:.2f} | {pct(dev_metrics['top1_accuracy'])} | "
            f"{pct(test_metrics['top1_accuracy'])} | {pct(test_metrics['acceptable_top1_accuracy'])} | "
            f"{pct(test_metrics['top5_recall'])} | {test_metrics['mrr']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation Guardrail",
            "",
            "- If the best setting is `base_weight = 1.00`, M6-v2 field scoring did not improve over the fixed first-stage ordering for that source.",
            "- If the best setting is near `base_weight = 0.00`, the field score is dominating; this needs held-out validation because it can overfit to the benchmark.",
            "- A stable useful region would be a middle blend, especially if it improves both top-1 and MRR across strata.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep score blends over existing M6-v2 outputs.")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--base-weights", default="0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0")
    parser.add_argument("--penalty-scales", default="0,0.5,1.0")
    parser.add_argument("--dev-fraction", type=float, default=0.5)
    parser.add_argument("--output-md", default="skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep.json")
    args = parser.parse_args()

    r1 = {row["name"]: row for row in load_jsonl(Path(args.r1))}
    base_weights = parse_float_grid(args.base_weights)
    penalty_scales = parse_float_grid(args.penalty_scales)

    sources: list[dict[str, Any]] = []
    for source in DEFAULT_SOURCES:
        result = evaluate_source(source, r1, base_weights, penalty_scales, args.dev_fraction)
        if result is not None:
            sources.append(result)

    report = {
        "base_weights": base_weights,
        "penalty_scales": penalty_scales,
        "dev_fraction": args.dev_fraction,
        "sources": sources,
    }
    Path(args.output_json).write_text(json.dumps(report, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {args.output_md}")
    print(f"Wrote {args.output_json}")


if __name__ == "__main__":
    main()
