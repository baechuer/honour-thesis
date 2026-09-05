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
from run_m6v2_semantic_field_reranker import POSITIVE_FIELDS, parse_field_set  # noqa: E402
from run_offline_selectors import evaluate_rows, load_acceptables, load_jsonl, minmax  # noqa: E402


DEFAULT_SOURCES = [
    ("controlled", "qwen", "r1", "skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r1_m6v2_field_specific_top20.json", "skill_benchmark/annotations/acceptable_alternatives.json"),
    ("controlled", "qwen", "r2", "skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r2_m6v2_field_specific_top20.json", "skill_benchmark/annotations/acceptable_alternatives.json"),
    ("controlled", "qwen", "full", "skill_benchmark/outputs/frozen_v0_4_controlled_qwen_full_m6v2_field_specific_top20.json", "skill_benchmark/annotations/acceptable_alternatives.json"),
    ("public_gold", "qwen", "r1", "skill_benchmark/outputs/frozen_v0_4_public_gold_qwen_r1_m6v2_field_specific_top20.json", "skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
    ("public_gold", "qwen", "r2", "skill_benchmark/outputs/frozen_v0_4_public_gold_qwen_r2_m6v2_field_specific_top20.json", "skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
    ("public_gold", "qwen", "full", "skill_benchmark/outputs/frozen_v0_4_public_gold_qwen_full_m6v2_field_specific_top20.json", "skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
    ("controlled", "skillrouter", "r1", "skill_benchmark/outputs/frozen_v0_4_controlled_skillrouter_r1_m6v2_field_specific_top20.json", "skill_benchmark/annotations/acceptable_alternatives.json"),
    ("controlled", "skillrouter", "r2", "skill_benchmark/outputs/frozen_v0_4_controlled_skillrouter_r2_m6v2_field_specific_top20.json", "skill_benchmark/annotations/acceptable_alternatives.json"),
    ("controlled", "skillrouter", "full", "skill_benchmark/outputs/frozen_v0_4_controlled_skillrouter_full_m6v2_field_specific_top20.json", "skill_benchmark/annotations/acceptable_alternatives.json"),
    ("public_gold", "skillrouter", "r1", "skill_benchmark/outputs/frozen_v0_4_public_gold_skillrouter_r1_m6v2_field_specific_top20.json", "skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
    ("public_gold", "skillrouter", "r2", "skill_benchmark/outputs/frozen_v0_4_public_gold_skillrouter_r2_m6v2_field_specific_top20.json", "skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
    ("public_gold", "skillrouter", "full", "skill_benchmark/outputs/frozen_v0_4_public_gold_skillrouter_full_m6v2_field_specific_top20.json", "skill_benchmark/annotations/public_gold_acceptable_alternatives.json"),
]

WEIGHT_SCHEMES: dict[str, dict[str, float]] = {
    "task_only": {"task": 1.0},
    "task_heavy": {"task": 0.50, "input": 0.10, "output": 0.20, "workflow": 0.15, "dependency": 0.05},
    "task_output": {"task": 0.55, "output": 0.45},
    "task_output_workflow": {"task": 0.45, "output": 0.35, "workflow": 0.20},
    "global_core": {"task": 0.35, "input": 0.15, "output": 0.25, "workflow": 0.20, "dependency": 0.05},
    "balanced_input": {"task": 0.30, "input": 0.20, "output": 0.25, "workflow": 0.20, "dependency": 0.05},
    "balanced_core": {"task": 0.35, "input": 0.15, "output": 0.25, "workflow": 0.25},
    "dependency_balanced": {"task": 0.30, "input": 0.15, "output": 0.20, "workflow": 0.20, "dependency": 0.15},
    "output_workflow_heavy": {"task": 0.30, "input": 0.10, "output": 0.35, "workflow": 0.25},
    "workflow_heavy": {"task": 0.30, "input": 0.10, "output": 0.20, "workflow": 0.40},
    "dependency_light": {"task": 0.35, "input": 0.15, "output": 0.25, "workflow": 0.15, "dependency": 0.10},
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_float_grid(raw: str) -> list[float]:
    return [round(float(part.strip()), 6) for part in raw.split(",") if part.strip()]


def parse_filter(raw: str) -> set[str]:
    if not raw:
        return set()
    return {part.strip().lower() for part in raw.split(",") if part.strip()}


def split_rows(rows: list[dict[str, Any]], split: str, dev_fraction: float) -> list[dict[str, Any]]:
    threshold = int(dev_fraction * 1000)
    output: list[dict[str, Any]] = []
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


def active_fields(item: dict[str, Any], enabled: set[str], activation_policy: str) -> set[str]:
    positive = set(POSITIVE_FIELDS) & enabled
    if activation_policy == "cue_gated":
        return set(item.get("active_fields", [])) & positive
    if activation_policy == "all_enabled":
        return positive
    if activation_policy == "task_plus_cued":
        fields = set(item.get("active_fields", [])) & positive
        if "task" in positive:
            fields.add("task")
        return fields
    raise ValueError(f"Unknown activation policy: {activation_policy}")


def weighted_component_score(
    item: dict[str, Any],
    enabled: set[str],
    weight_scheme: dict[str, float],
    activation_policy: str,
) -> float:
    fields = active_fields(item, enabled, activation_policy)
    weights = {field: weight_scheme.get(field, 0.0) for field in fields}
    total = sum(weights.values())
    if total <= 0:
        return 0.0
    components = item.get("components", {})
    return sum((weights[field] / total) * float(components.get(field, 0.0)) for field in fields)


def rescore_rows(
    rows: list[dict[str, Any]],
    enabled: set[str],
    weight_scheme: dict[str, float],
    activation_policy: str,
    base_weight: float,
    penalty_scale: float,
) -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    field_weight = 1.0 - base_weight
    for row in rows:
        raw_field_scores = [
            weighted_component_score(item, enabled, weight_scheme, activation_policy)
            for item in row["ranking"]
        ]
        field_norm = minmax(raw_field_scores)
        reranked: list[dict[str, Any]] = []
        for index, item in enumerate(row["ranking"]):
            penalty_delta = float(item.get("exclusion_bonus", 0.0)) - float(item.get("total_penalty", 0.0))
            score = (
                base_weight * float(item.get("base_norm", 0.0))
                + field_weight * field_norm[index]
                + penalty_scale * penalty_delta
            )
            new_item = dict(item)
            new_item["score"] = round(score, 6)
            new_item["explicit_field_score"] = round(raw_field_scores[index], 6)
            new_item["explicit_field_norm"] = round(field_norm[index], 6)
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


def source_rows_for_field_set(report: dict[str, Any], field_set: str) -> list[dict[str, Any]]:
    for summary in report["summary"]:
        if summary["field_set"] == field_set:
            return report["results"][summary["result_key"]]
    raise KeyError(f"{field_set} not found in {report.get('source_result')}")


def evaluate_source(
    source: tuple[str, str, str, str, str],
    r1: dict[str, dict[str, Any]],
    base_weights: list[float],
    penalty_scales: list[float],
    activation_policies: list[str],
    dev_fraction: float,
    field_set_filter: set[str] | None = None,
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

    sweep_rows: list[dict[str, Any]] = []
    dev_sweep_rows: list[dict[str, Any]] = []
    for field_set in [summary["field_set"] for summary in report["summary"]]:
        if field_set_filter and field_set.lower() not in field_set_filter:
            continue
        enabled = parse_field_set(field_set)
        source_rows = source_rows_for_field_set(report, field_set)
        for scheme_name, scheme in WEIGHT_SCHEMES.items():
            if not (set(scheme) & enabled):
                continue
            for activation_policy in activation_policies:
                for base_weight in base_weights:
                    for penalty_scale in penalty_scales:
                        rows = rescore_rows(
                            source_rows,
                            enabled,
                            scheme,
                            activation_policy,
                            base_weight,
                            penalty_scale,
                        )
                        metrics = evaluate_rows(rows, r1, skill_count, selector_visible_tokens, acceptable_by_prompt)
                        row_payload = {
                            "stratum": stratum,
                            "candidate_source": candidate_source,
                            "representation": representation,
                            "source_json": source_json,
                            "query_field_mode": report.get("query_field_mode", ""),
                            "field_set": field_set,
                            "weight_scheme": scheme_name,
                            "activation_policy": activation_policy,
                            "base_weight": base_weight,
                            "field_weight": round(1.0 - base_weight, 6),
                            "penalty_scale": penalty_scale,
                            "candidate_recall_at_k": candidate_recall(rows, rerank_candidates),
                            "metrics": metrics,
                        }
                        sweep_rows.append(row_payload)

                        dev_rows = split_rows(rows, "dev", dev_fraction)
                        test_rows = split_rows(rows, "test", dev_fraction)
                        row_payload_dev = {
                            **row_payload,
                            "dev_prompt_count": len(dev_rows),
                            "test_prompt_count": len(test_rows),
                            "dev_metrics": evaluate_rows(dev_rows, r1, skill_count, selector_visible_tokens, acceptable_by_prompt),
                            "test_metrics": evaluate_rows(test_rows, r1, skill_count, selector_visible_tokens, acceptable_by_prompt),
                        }
                        dev_sweep_rows.append(row_payload_dev)

    if not sweep_rows:
        return None

    return {
        "stratum": stratum,
        "candidate_source": candidate_source,
        "representation": representation,
        "source_json": source_json,
        "rerank_candidates": rerank_candidates,
        "best_top1": max(sweep_rows, key=lambda item: item["metrics"]["top1_accuracy"]),
        "best_mrr": max(sweep_rows, key=lambda item: item["metrics"]["mrr"]),
        "best_accept_top1": max(sweep_rows, key=lambda item: item["metrics"]["acceptable_top1_accuracy"]),
        "best_dev_top1": max(dev_sweep_rows, key=lambda item: item["dev_metrics"]["top1_accuracy"]),
        "best_dev_mrr": max(dev_sweep_rows, key=lambda item: item["dev_metrics"]["mrr"]),
    }


def pct(value: float) -> str:
    return f"{value:.1%}"


def render_setting(item: dict[str, Any]) -> str:
    return (
        f"`{item['field_set']}` / `{item['weight_scheme']}` / `{item['activation_policy']}` "
        f"/ base {item['base_weight']:.2f}"
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# M6-v2 Explicit Field-Weight Sweep",
        "",
        "This report rescales field-specific M6-v2 outputs without new embedding calls. Unlike the blend-only sweep, it recomputes the semantic field score from saved per-field component similarities, so it tests explicit use of task/input/output/workflow/dependency fields.",
        "",
        f"- Base-weight grid: {', '.join(str(v) for v in report['base_weights'])}",
        f"- Penalty-scale grid: {', '.join(str(v) for v in report['penalty_scales'])}",
        f"- Activation policies: {', '.join(report['activation_policies'])}",
        f"- Development fraction: {report['dev_fraction']:.0%}",
        "",
        "## Best Full-Set Top-1",
        "",
        "| Stratum | Source | Rep | Setting | Top-1 | Accept Top-1 | Top-5 | MRR | Cand R@20 |",
        "|---|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for source in report["sources"]:
        best = source["best_top1"]
        metrics = best["metrics"]
        lines.append(
            f"| {source['stratum']} | {source['candidate_source']} | {source['representation'].upper()} | "
            f"{render_setting(best)} | {pct(metrics['top1_accuracy'])} | "
            f"{pct(metrics['acceptable_top1_accuracy'])} | {pct(metrics['top5_recall'])} | "
            f"{metrics['mrr']:.3f} | {pct(best['candidate_recall_at_k'])} |"
        )

    lines.extend([
        "",
        "## Dev-Selected Top-1, Held-Out Test Result",
        "",
        "| Stratum | Source | Rep | Dev-selected setting | Dev Top-1 | Test Top-1 | Test Accept Top-1 | Test Top-5 | Test MRR |",
        "|---|---|---|---|---:|---:|---:|---:|---:|",
    ])
    for source in report["sources"]:
        best = source["best_dev_top1"]
        dev = best["dev_metrics"]
        test = best["test_metrics"]
        lines.append(
            f"| {source['stratum']} | {source['candidate_source']} | {source['representation'].upper()} | "
            f"{render_setting(best)} | {pct(dev['top1_accuracy'])} | "
            f"{pct(test['top1_accuracy'])} | {pct(test['acceptable_top1_accuracy'])} | "
            f"{pct(test['top5_recall'])} | {test['mrr']:.3f} |"
        )

    lines.extend([
        "",
        "## Interpretation Guardrail",
        "",
        "- Full-set best rows are calibration diagnostics and may overfit.",
        "- Dev-selected test rows are safer, but still use a single deterministic split.",
        "- A useful M6-v2 field strategy should improve held-out top-1 or MRR without sacrificing candidate recall and should generalize across at least controlled and public-gold R2 rows.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep explicit field weights over field-specific M6-v2 outputs.")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--base-weights", default="0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0")
    parser.add_argument("--penalty-scales", default="0,0.5,1.0")
    parser.add_argument("--activation-policies", default="cue_gated,task_plus_cued")
    parser.add_argument("--only-strata", default="", help="Optional comma-separated filter, e.g. controlled,public_gold.")
    parser.add_argument("--only-sources", default="", help="Optional comma-separated filter, e.g. qwen,skillrouter.")
    parser.add_argument("--only-reps", default="", help="Optional comma-separated filter, e.g. r2,full.")
    parser.add_argument("--only-field-sets", default="", help="Optional comma-separated filter, e.g. semantic_all.")
    parser.add_argument("--only-weight-schemes", default="", help="Optional comma-separated filter, e.g. global_core.")
    parser.add_argument("--dev-fraction", type=float, default=0.5)
    parser.add_argument("--output-md", default="skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep.json")
    args = parser.parse_args()

    r1 = {row["name"]: row for row in load_jsonl(Path(args.r1))}
    report = {
        "base_weights": parse_float_grid(args.base_weights),
        "penalty_scales": parse_float_grid(args.penalty_scales),
        "activation_policies": [part.strip() for part in args.activation_policies.split(",") if part.strip()],
        "dev_fraction": args.dev_fraction,
        "sources": [],
    }
    strata_filter = parse_filter(args.only_strata)
    source_filter = parse_filter(args.only_sources)
    rep_filter = parse_filter(args.only_reps)
    field_set_filter = parse_filter(args.only_field_sets)
    weight_scheme_filter = parse_filter(args.only_weight_schemes)
    if weight_scheme_filter:
        unknown_schemes = weight_scheme_filter - set(WEIGHT_SCHEMES)
        if unknown_schemes:
            raise SystemExit(f"Unknown weight schemes: {sorted(unknown_schemes)}")
        original_schemes = dict(WEIGHT_SCHEMES)
        WEIGHT_SCHEMES.clear()
        WEIGHT_SCHEMES.update(
            {name: scheme for name, scheme in original_schemes.items() if name in weight_scheme_filter}
        )
    for source in DEFAULT_SOURCES:
        stratum, candidate_source, representation, *_ = source
        if strata_filter and stratum.lower() not in strata_filter:
            continue
        if source_filter and candidate_source.lower() not in source_filter:
            continue
        if rep_filter and representation.lower() not in rep_filter:
            continue
        result = evaluate_source(
            source,
            r1,
            report["base_weights"],
            report["penalty_scales"],
            report["activation_policies"],
            args.dev_fraction,
            field_set_filter=field_set_filter,
        )
        if result is not None:
            report["sources"].append(result)

    Path(args.output_json).write_text(json.dumps(report, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {args.output_md}")
    print(f"Wrote {args.output_json}")


if __name__ == "__main__":
    main()
