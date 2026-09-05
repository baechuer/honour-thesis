#!/usr/bin/env python3
"""Summarise RQ1a at the cluster level from frozen row-level selector outputs.

The RQ1a prompt variants within a cluster are paired observations, so this
script averages them within cluster before bootstrapping.  It also reports a
retrieval-leading-negative margin: the gold score minus the highest-scoring
non-gold score.  This is deliberately not described as a semantic-distance
measure because the source units do not pre-annotate one negative as the
semantically closest alternative.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "skill_benchmark/outputs/rq1a_cluster_uncertainty_2026-08-30"

ROW_FILES = {
    "use_condition": "rq1a_use_condition_bm25_qwen_embedding_rows.jsonl",
    "input_precondition": "rq1a_input_precondition_bm25_qwen_embedding_rows.jsonl",
    "output_artifact": "rq1a_output_artifact_bm25_qwen_embedding_rows.jsonl",
    "dependency_resource": "rq1a_dependency_resource_isolation_bm25_qwen_embedding_rows.jsonl",
    "boundary_not_for": "rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit_rows.jsonl",
    "success_verification": "rq1a_success_verification_bm25_qwen_embedding_rows.jsonl",
    "workflow_procedure": "rq1a_workflow_procedure_bm25_qwen_embedding_rows.jsonl",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--resamples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260830)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        raise ValueError("cannot calculate percentile of empty sequence")
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def bootstrap_ci(values: list[float], *, resamples: int, rng: random.Random) -> tuple[float, float]:
    if not values:
        raise ValueError("cannot bootstrap empty values")
    size = len(values)
    draws = [mean(values[rng.randrange(size)] for _ in range(size)) for _ in range(resamples)]
    return percentile(draws, 0.025), percentile(draws, 0.975)


def leading_negative(row: dict) -> tuple[str, float]:
    gold = row["gold_skill_id"]
    negatives = {skill_id: score for skill_id, score in row["scores"].items() if skill_id != gold}
    if not negatives:
        raise ValueError(f"{row['prompt_id']} has no negative candidates")
    skill_id, score = sorted(negatives.items(), key=lambda item: (-item[1], item[0]))[0]
    return skill_id, score


def cluster_means(rows: list[dict]) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["cluster_id"]].append(row)

    results: dict[str, dict[str, float]] = {}
    for cluster_id, cluster_rows in grouped.items():
        top1 = [row["top1_tie_adjusted"] for row in cluster_rows]
        mrr = [row["mrr_tie_adjusted"] for row in cluster_rows]
        margins = []
        leading_negative_wins = []
        for row in cluster_rows:
            _, negative_score = leading_negative(row)
            gold_score = row["scores"][row["gold_skill_id"]]
            margin = gold_score - negative_score
            margins.append(margin)
            leading_negative_wins.append(1.0 if margin > 0 else (0.5 if margin == 0 else 0.0))
        results[cluster_id] = {
            "top1_tie_adjusted": mean(top1),
            "mrr_tie_adjusted": mean(mrr),
            "leading_negative_margin": mean(margins),
            "gold_beats_leading_negative": mean(leading_negative_wins),
            "prompt_rows": len(cluster_rows),
        }
    return results


def analyse_field(field: str, rows: list[dict], *, resamples: int, seed: int) -> tuple[list[dict], list[dict]]:
    field_rows = [row for row in rows if row["field"] == field]
    expected_conditions = {"shared_context_only", "shared_context_plus_field"}
    retrievers = sorted({row["retriever"] for row in field_rows})
    summary_rows: list[dict] = []
    detail_rows: list[dict] = []

    for retriever_index, retriever in enumerate(retrievers):
        retriever_rows = [row for row in field_rows if row["retriever"] == retriever]
        by_condition = {
            condition: cluster_means([row for row in retriever_rows if row["condition"] == condition])
            for condition in expected_conditions
        }
        if set(by_condition) != expected_conditions or not all(by_condition.values()):
            raise ValueError(f"{field}/{retriever}: missing primary condition rows")
        clusters = sorted(set(by_condition["shared_context_only"]) & set(by_condition["shared_context_plus_field"]))
        if len(clusters) != 50:
            raise ValueError(f"{field}/{retriever}: expected 50 aligned clusters, got {len(clusters)}")

        metrics = ("top1_tie_adjusted", "mrr_tie_adjusted", "leading_negative_margin", "gold_beats_leading_negative")
        row = {
            "field": field,
            "retriever": retriever,
            "cluster_count": len(clusters),
            "prompt_rows_per_condition": sum(by_condition["shared_context_plus_field"][cluster]["prompt_rows"] for cluster in clusters),
            "leading_negative_definition": "highest-scoring non-gold candidate within the same three-sibling retrieval row; not a semantic-distance annotation",
        }
        for metric_index, metric in enumerate(metrics):
            hidden = [by_condition["shared_context_only"][cluster][metric] for cluster in clusters]
            exposed = [by_condition["shared_context_plus_field"][cluster][metric] for cluster in clusters]
            delta = [exposed_value - hidden_value for exposed_value, hidden_value in zip(exposed, hidden)]
            rng = random.Random(seed + retriever_index * 100 + metric_index)
            ci_low, ci_high = bootstrap_ci(delta, resamples=resamples, rng=rng)
            row[f"hidden_{metric}"] = mean(hidden)
            row[f"exposed_{metric}"] = mean(exposed)
            row[f"delta_{metric}"] = mean(delta)
            row[f"delta_{metric}_ci95"] = [ci_low, ci_high]

        summary_rows.append(row)
        for cluster in clusters:
            detail_rows.append(
                {
                    "field": field,
                    "retriever": retriever,
                    "cluster_id": cluster,
                    "hidden": by_condition["shared_context_only"][cluster],
                    "exposed": by_condition["shared_context_plus_field"][cluster],
                }
            )
    return summary_rows, detail_rows


def build_markdown(rows: list[dict]) -> str:
    lines = [
        "# RQ1a Cluster-Level Uncertainty and Leading-Negative Diagnostics",
        "",
        "This local-only analysis uses the frozen RQ1a row-level results. Prompt variants are averaged within each cluster before resampling, so the bootstrap unit is the cluster rather than the individual prompt. `Leading negative` means the highest-scoring non-gold sibling in a row; it is not a pre-annotated semantic-nearest negative.",
        "",
        "| Field | Retriever | Clusters | Exposed Top-1 | Top-1 lift 95% CI | Exposed MRR | MRR lift 95% CI | Exposed leading-negative margin | Margin lift 95% CI |",
        "|---|---|---:|---:|---|---:|---|---:|---|",
    ]
    for row in rows:
        top_ci = row["delta_top1_tie_adjusted_ci95"]
        mrr_ci = row["delta_mrr_tie_adjusted_ci95"]
        margin_ci = row["delta_leading_negative_margin_ci95"]
        lines.append(
            "| {field} | {retriever} | {cluster_count} | {top:.3f} | [{top_low:.3f}, {top_high:.3f}] | {mrr:.3f} | [{mrr_low:.3f}, {mrr_high:.3f}] | {margin:.4f} | [{margin_low:.4f}, {margin_high:.4f}] |".format(
                field=row["field"],
                retriever=row["retriever"],
                cluster_count=row["cluster_count"],
                top=row["exposed_top1_tie_adjusted"],
                top_low=top_ci[0],
                top_high=top_ci[1],
                mrr=row["exposed_mrr_tie_adjusted"],
                mrr_low=mrr_ci[0],
                mrr_high=mrr_ci[1],
                margin=row["exposed_leading_negative_margin"],
                margin_low=margin_ci[0],
                margin_high=margin_ci[1],
            )
        )
    lines.extend(
        [
            "",
            "Interpretation boundary: every row comes from an authored three-sibling controlled unit. The uncertainty intervals quantify variation across those 50 clusters; they do not establish a population effect for arbitrary public skills. Because no unit pre-annotates one alternative as semantically closer than the other, the leading-negative metrics diagnose the retriever's strongest competing sibling rather than a human semantic-distance judgement.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    outputs_root = ROOT / "skill_benchmark/outputs"
    all_summary: list[dict] = []
    all_details: list[dict] = []
    source_records = []
    for field, filename in ROW_FILES.items():
        path = outputs_root / filename
        if not path.exists():
            raise FileNotFoundError(path)
        rows = read_jsonl(path)
        summary, details = analyse_field(field, rows, resamples=args.resamples, seed=args.seed)
        all_summary.extend(summary)
        all_details.extend(details)
        source_records.append({"field": field, "path": str(path.relative_to(ROOT)), "rows": len(rows)})

    if len(all_summary) != 14 or len(all_details) != 700:
        raise ValueError(f"unexpected output shape: {len(all_summary)} summaries, {len(all_details)} cluster rows")

    payload = {
        "schema_version": "RQ1A_CLUSTER_UNCERTAINTY_V1",
        "analysis_scope": "frozen existing RQ1a row-level results only; no selector rerun",
        "bootstrap_unit": "cluster, after averaging prompt variants within cluster",
        "resamples": args.resamples,
        "seed": args.seed,
        "leading_negative_definition": "highest-scoring non-gold candidate in the same retrieval row; not semantic-distance annotation",
        "source_records": source_records,
        "summary": all_summary,
    }

    if args.check:
        print(json.dumps({"status": "PASS", "summary_rows": len(all_summary), "cluster_rows": len(all_details), "sources": source_records}, indent=2))
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "cluster_rows.jsonl").open("w", encoding="utf-8") as handle:
        for row in all_details:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    (output_dir / "SUMMARY.md").write_text(build_markdown(all_summary), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output_dir": str(output_dir), "summary_rows": len(all_summary), "cluster_rows": len(all_details)}, indent=2))


if __name__ == "__main__":
    main()
