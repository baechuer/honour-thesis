#!/usr/bin/env python3
"""Local-only B3-v2 synthesis for frozen RQ2b V3 B1/B2 result rows.

This script never changes frozen B1/B2 artifacts and never calls a provider or
model. It produces the post-hoc, cluster-level reporting specified by
``B3_V2_THESIS_REPORTING_AMENDMENT.md``. The older B3-v1 analysis and its
sign-flip/Holm output remain untouched.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

import numpy as np

import analyse_rq2bv1_v3_b3 as v1
from run_rq2b_qwen import ExactEmbeddingCache


ROOT = v1.ROOT
V3 = v1.V3
RESULTS = v1.RESULTS
OUTPUT_ROOT = RESULTS / "b3_v3_v2"
REPRESENTATIONS = v1.REPRESENTATIONS
RETRIEVERS = v1.RETRIEVERS
RERANKERS = v1.RERANKERS
PRIMARY_STRATA = ("controlled", "public_gold")
BOOTSTRAP_RESAMPLES = 20_000
BOOTSTRAP_SEED = 2026082303
TIE_EPSILON = 1e-12

REPRESENTATION_CONTRASTS = (
    ("i2_minus_i1", "i2-original", "i1-discovery"),
    ("i3_flat_minus_i2", "i3-flat-evidence", "i2-original"),
    ("i3c_minus_i3_flat", "i3c-fielded-evidence", "i3-flat-evidence"),
    ("i3c_minus_i2", "i3c-fielded-evidence", "i2-original"),
    ("i3_flat_minus_i1", "i3-flat-evidence", "i1-discovery"),
    ("i3c_minus_i1", "i3c-fielded-evidence", "i1-discovery"),
)
RETRIEVER_CONTRASTS = (
    ("qwen_minus_bm25", "qwen", "bm25"),
    ("skillrouter_minus_bm25", "skillrouter", "bm25"),
    ("skillrouter_minus_qwen", "skillrouter", "qwen"),
)
RERANKER_CONTRASTS = (
    ("qwen_b2_minus_b1", "qwen_b2", "b1"),
    ("skillrouter_b2_minus_b1", "skillrouter_b2", "b1"),
    ("skillrouter_b2_minus_qwen_b2", "skillrouter_b2", "qwen_b2"),
)
SENSITIVITY_REPRESENTATIONS = (
    "i2-original",
    "i3-flat-evidence",
    "i3c-fielded-evidence",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def mean(values: list[float]) -> float:
    require(bool(values), "Cannot calculate a mean of zero values")
    return float(sum(values) / len(values))


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.asarray(values, dtype=np.float64), q, method="linear"))


def stage_rows(
    b1: dict[str, list[dict[str, Any]]],
    b2: dict[str, list[dict[str, Any]]],
    *,
    stage: str,
    first_stage_retriever: str,
    representation: str,
) -> list[dict[str, Any]]:
    if stage == "b1":
        return [
            row
            for row in b1[first_stage_retriever]
            if row["representation"] == representation
        ]
    if stage in {"qwen_b2", "skillrouter_b2"}:
        reranker = stage.removesuffix("_b2")
        return [
            row
            for row in b2[reranker]
            if row["representation"] == representation
            and v1.canonical_retriever(str(row["first_stage_retriever"]))
            == first_stage_retriever
        ]
    raise RuntimeError(f"Unknown stage: {stage}")


def is_eligible(row: dict[str, Any], stage: str) -> bool:
    if stage == "b1":
        return int(row["strict_gold_rank"]) <= 20
    return int(row["strict_candidate_positive"]) == 1


def row_is_eligible(row: dict[str, Any]) -> bool:
    """Use the row schema, since paired B1/B2 stages can differ here."""
    if "strict_gold_rank" in row:
        return int(row["strict_gold_rank"]) <= 20
    return int(row["strict_candidate_positive"]) == 1


def metric_value(row: dict[str, Any], stage: str, metric: str) -> float:
    if stage == "b1":
        if metric == "hit_at_1":
            return v1.b1_metric(row, "hit_at_1")
        if metric == "mrr_at_20":
            return v1.b1_metric(row, "mrr_at_20")
        if metric == "recall_at_20":
            return v1.b1_metric(row, "recall_at_20")
    else:
        if metric == "hit_at_1":
            return v1.b2_metric(row, "hit_at_1")
        if metric == "mrr_at_20":
            return v1.b2_metric(row, "mrr_at_20")
        if metric == "recall_at_20":
            return float(int(row["strict_candidate_positive"]) == 1)
    raise RuntimeError(f"Unknown {stage} metric: {metric}")


def stratum_rows(rows: list[dict[str, Any]], stratum: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["stratum"] == stratum]


def row_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    output = {str(row["prompt_id"]): row for row in rows}
    require(len(output) == len(rows), "Duplicate prompt ID inside a condition")
    return output


def verify_pairing(
    left: list[dict[str, Any]], right: list[dict[str, Any]], *, conditional: bool
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left_by_prompt = row_map(left)
    right_by_prompt = row_map(right)
    require(
        set(left_by_prompt) == set(right_by_prompt),
        "Paired conditions do not cover the same prompts",
    )
    for prompt_id in left_by_prompt:
        a, b = left_by_prompt[prompt_id], right_by_prompt[prompt_id]
        for field in ("group", "stratum", "gold_skill", "prompt_sha256"):
            require(a[field] == b[field], f"Paired {field} mismatch: {prompt_id}")
    if not conditional:
        return left, right
    eligible = {
        prompt_id
        for prompt_id, row in left_by_prompt.items()
        if row_is_eligible(row)
    }
    right_eligible = {
        prompt_id
        for prompt_id, row in right_by_prompt.items()
        if row_is_eligible(row)
    }
    require(
        eligible == right_eligible,
        "Conditional comparison changed the fixed candidate eligibility set",
    )
    require(bool(eligible), "Conditional comparison has no eligible prompts")
    return (
        [left_by_prompt[prompt_id] for prompt_id in sorted(eligible)],
        [right_by_prompt[prompt_id] for prompt_id in sorted(eligible)],
    )


_BOOTSTRAP_INDICES: dict[int, np.ndarray] = {}


def bootstrap_indices(group_count: int) -> np.ndarray:
    require(group_count > 0, "Bootstrap needs at least one group")
    if group_count not in _BOOTSTRAP_INDICES:
        _BOOTSTRAP_INDICES[group_count] = np.random.default_rng(BOOTSTRAP_SEED).integers(
            0,
            group_count,
            size=(BOOTSTRAP_RESAMPLES, group_count),
            dtype=np.int32,
        )
    return _BOOTSTRAP_INDICES[group_count]


def group_means(
    rows: list[dict[str, Any]], *, stage: str, metric: str
) -> tuple[dict[str, float], dict[str, int]]:
    values: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        values[str(row["group"])].append(metric_value(row, stage, metric))
    return (
        {group: mean(group_values) for group, group_values in values.items()},
        {group: len(group_values) for group, group_values in values.items()},
    )


def paired_contrast(
    *,
    family: str,
    label: str,
    left_rows: list[dict[str, Any]],
    right_rows: list[dict[str, Any]],
    left_stage: str,
    right_stage: str,
    metric: str,
    stratum: str,
    conditional: bool = False,
) -> dict[str, Any]:
    left_scope = stratum_rows(left_rows, stratum)
    right_scope = stratum_rows(right_rows, stratum)
    left_scope, right_scope = verify_pairing(
        left_scope, right_scope, conditional=conditional
    )
    left_values, left_counts = group_means(
        left_scope, stage=left_stage, metric=metric
    )
    right_values, right_counts = group_means(
        right_scope, stage=right_stage, metric=metric
    )
    require(
        set(left_values) == set(right_values),
        "Paired conditions do not cover the same semantic clusters",
    )
    groups = sorted(left_values)
    left_vector = np.asarray([left_values[group] for group in groups], dtype=np.float64)
    right_vector = np.asarray([right_values[group] for group in groups], dtype=np.float64)
    delta_vector = left_vector - right_vector
    draws = delta_vector[bootstrap_indices(len(groups))].mean(axis=1)
    ties = int(np.count_nonzero(np.abs(delta_vector) <= TIE_EPSILON))
    return {
        "family": family,
        "label": label,
        "stratum": stratum,
        "metric": metric,
        "conditional_on_gold_in_top20": conditional,
        "left_stage": left_stage,
        "right_stage": right_stage,
        "estimate_left_minus_right": float(delta_vector.mean()),
        "left_cluster_macro": float(left_vector.mean()),
        "right_cluster_macro": float(right_vector.mean()),
        "ci_95_percentile": [
            float(np.quantile(draws, 0.025, method="linear")),
            float(np.quantile(draws, 0.975, method="linear")),
        ],
        "clusters": len(groups),
        "prompts": len(left_scope),
        "left_prompt_counts_by_cluster": dict(sorted(left_counts.items())),
        "right_prompt_counts_by_cluster": dict(sorted(right_counts.items())),
        "cluster_left_win_count": int(np.count_nonzero(delta_vector > TIE_EPSILON)),
        "cluster_tie_count": ties,
        "cluster_right_win_count": int(np.count_nonzero(delta_vector < -TIE_EPSILON)),
        "bootstrap": {
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed": BOOTSTRAP_SEED,
            "unit": "direct/paraphrase-averaged paired semantic cluster",
            "stratified_within": stratum,
            "interval": "percentile 2.5th/97.5th",
        },
    }


def condition_summary(
    rows: list[dict[str, Any]], *, stage: str, stratum: str
) -> dict[str, Any]:
    if stratum == "combined_prompt_weighted":
        scope = rows
    else:
        scope = stratum_rows(rows, stratum)
    require(bool(scope), f"No condition rows for {stage}/{stratum}")
    groups = sorted({str(row["group"]) for row in scope})
    summary: dict[str, Any] = {
        "stratum": stratum,
        "n_prompts": len(scope),
        "n_clusters": len(groups),
    }
    for metric in ("hit_at_1", "mrr_at_20", "recall_at_20"):
        prompt_values = [metric_value(row, stage, metric) for row in scope]
        by_group, _ = group_means(scope, stage=stage, metric=metric)
        summary[f"{metric}_prompt_weighted"] = mean(prompt_values)
        summary[f"{metric}_cluster_macro"] = (
            mean(list(by_group.values())) if stratum != "combined_prompt_weighted" else None
        )
    if stage != "b1":
        eligible = [row for row in scope if is_eligible(row, stage)]
        summary["conditional_eligible_prompts"] = len(eligible)
        eligible_groups = sorted({str(row["group"]) for row in eligible})
        summary["conditional_eligible_clusters"] = len(eligible_groups)
        if eligible:
            conditional_by_group, _ = group_means(
                eligible, stage=stage, metric="hit_at_1"
            )
            summary["conditional_hit_at_1_prompt_weighted"] = mean(
                [metric_value(row, stage, "hit_at_1") for row in eligible]
            )
            summary["conditional_hit_at_1_cluster_macro"] = (
                mean(list(conditional_by_group.values()))
                if stratum != "combined_prompt_weighted"
                else None
            )
        else:
            summary["conditional_hit_at_1_prompt_weighted"] = None
            summary["conditional_hit_at_1_cluster_macro"] = None
        corrections = [row for row in scope if int(row["strict_reranker_gain"]) == 1]
        regressions = [
            row for row in scope if int(row["strict_reranker_regression"]) == 1
        ]
        summary["reranker_correction_count"] = len(corrections)
        summary["reranker_regression_count"] = len(regressions)
        summary["reranker_correction_rate_prompt_weighted"] = len(corrections) / len(scope)
        summary["reranker_regression_rate_prompt_weighted"] = len(regressions) / len(scope)
    return summary


def all_condition_summaries(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for retriever in RETRIEVERS:
        for representation in REPRESENTATIONS:
            for stage in ("b1", "qwen_b2", "skillrouter_b2"):
                rows = stage_rows(
                    b1,
                    b2,
                    stage=stage,
                    first_stage_retriever=retriever,
                    representation=representation,
                )
                require(len(rows) == 381, f"Unexpected row count for {stage}/{retriever}/{representation}")
                for stratum in (*PRIMARY_STRATA, "combined_prompt_weighted"):
                    summary = condition_summary(rows, stage=stage, stratum=stratum)
                    summary.update(
                        {
                            "stage": stage,
                            "first_stage_retriever": retriever,
                            "representation": representation,
                            "reranker": None if stage == "b1" else stage.removesuffix("_b2"),
                        }
                    )
                    output.append(summary)
    return output


def representation_comparisons(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for name, left_representation, right_representation in REPRESENTATION_CONTRASTS:
        for retriever in RETRIEVERS:
            for stratum in PRIMARY_STRATA:
                left = stage_rows(b1, b2, stage="b1", first_stage_retriever=retriever, representation=left_representation)
                right = stage_rows(b1, b2, stage="b1", first_stage_retriever=retriever, representation=right_representation)
                for metric in ("hit_at_1", "mrr_at_20", "recall_at_20"):
                    output.append(paired_contrast(
                        family="representation_b1",
                        label=f"{name}/b1/{retriever}",
                        left_rows=left,
                        right_rows=right,
                        left_stage="b1",
                        right_stage="b1",
                        metric=metric,
                        stratum=stratum,
                    ))
                for reranker_stage in ("qwen_b2", "skillrouter_b2"):
                    left = stage_rows(b1, b2, stage=reranker_stage, first_stage_retriever=retriever, representation=left_representation)
                    right = stage_rows(b1, b2, stage=reranker_stage, first_stage_retriever=retriever, representation=right_representation)
                    for metric in ("hit_at_1", "mrr_at_20"):
                        output.append(paired_contrast(
                            family="representation_b2_end_to_end",
                            label=f"{name}/{reranker_stage}/{retriever}",
                            left_rows=left,
                            right_rows=right,
                            left_stage=reranker_stage,
                            right_stage=reranker_stage,
                            metric=metric,
                            stratum=stratum,
                        ))
    return output


def retriever_comparisons(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for representation in REPRESENTATIONS:
        for name, left_retriever, right_retriever in RETRIEVER_CONTRASTS:
            for stratum in PRIMARY_STRATA:
                left = stage_rows(b1, b2, stage="b1", first_stage_retriever=left_retriever, representation=representation)
                right = stage_rows(b1, b2, stage="b1", first_stage_retriever=right_retriever, representation=representation)
                for metric in ("hit_at_1", "mrr_at_20", "recall_at_20"):
                    output.append(paired_contrast(
                        family="retriever_b1",
                        label=f"{name}/b1/{representation}",
                        left_rows=left,
                        right_rows=right,
                        left_stage="b1",
                        right_stage="b1",
                        metric=metric,
                        stratum=stratum,
                    ))
                for reranker_stage in ("qwen_b2", "skillrouter_b2"):
                    left = stage_rows(b1, b2, stage=reranker_stage, first_stage_retriever=left_retriever, representation=representation)
                    right = stage_rows(b1, b2, stage=reranker_stage, first_stage_retriever=right_retriever, representation=representation)
                    for metric in ("hit_at_1", "mrr_at_20"):
                        output.append(paired_contrast(
                            family="retriever_b2_end_to_end",
                            label=f"{name}/{reranker_stage}/{representation}",
                            left_rows=left,
                            right_rows=right,
                            left_stage=reranker_stage,
                            right_stage=reranker_stage,
                            metric=metric,
                            stratum=stratum,
                        ))
    return output


def reranker_comparisons(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for representation in REPRESENTATIONS:
        for retriever in RETRIEVERS:
            stage_cache = {
                stage: stage_rows(b1, b2, stage=stage, first_stage_retriever=retriever, representation=representation)
                for stage in ("b1", "qwen_b2", "skillrouter_b2")
            }
            for name, left_stage, right_stage in RERANKER_CONTRASTS:
                for stratum in PRIMARY_STRATA:
                    for metric in ("hit_at_1", "mrr_at_20"):
                        output.append(paired_contrast(
                            family="reranker_end_to_end_fixed_top20",
                            label=f"{name}/{retriever}/{representation}",
                            left_rows=stage_cache[left_stage],
                            right_rows=stage_cache[right_stage],
                            left_stage=left_stage,
                            right_stage=right_stage,
                            metric=metric,
                            stratum=stratum,
                        ))
                    output.append(paired_contrast(
                        family="reranker_conditional_fixed_top20",
                        label=f"{name}/{retriever}/{representation}",
                        left_rows=stage_cache[left_stage],
                        right_rows=stage_cache[right_stage],
                        left_stage=left_stage,
                        right_stage=right_stage,
                        metric="hit_at_1",
                        stratum=stratum,
                        conditional=True,
                    ))
    return output


def failure_analysis(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for reranker_stage in ("qwen_b2", "skillrouter_b2"):
        for retriever in RETRIEVERS:
            for representation in REPRESENTATIONS:
                rows = stage_rows(b1, b2, stage=reranker_stage, first_stage_retriever=retriever, representation=representation)
                for stratum in (*PRIMARY_STRATA, "combined_prompt_weighted"):
                    scope = rows if stratum == "combined_prompt_weighted" else stratum_rows(rows, stratum)
                    counts = Counter()
                    for row in scope:
                        candidate_miss = not is_eligible(row, reranker_stage)
                        b1_top1 = int(row["first_stage_strict_top1"]) == 1
                        b2_top1 = int(row["reranked_strict_top1"]) == 1
                        if candidate_miss:
                            counts["candidate_miss"] += 1
                        if not candidate_miss and not b2_top1:
                            counts["ordering_error"] += 1
                        if not b1_top1 and b2_top1:
                            counts["reranker_correction"] += 1
                        if b1_top1 and not b2_top1:
                            counts["reranker_regression"] += 1
                        if not b1_top1 and not b2_top1:
                            counts["persistent_top1_error"] += 1
                    output.append({
                        "reranker": reranker_stage.removesuffix("_b2"),
                        "first_stage_retriever": retriever,
                        "representation": representation,
                        "stratum": stratum,
                        "n_prompts": len(scope),
                        "counts": dict(sorted(counts.items())),
                        "rates": {name: count / len(scope) for name, count in sorted(counts.items())},
                    })
    return output


def summarize_distribution(values: list[float]) -> dict[str, float | None]:
    return {
        "mean": mean(values) if values else None,
        "median": float(statistics.median(values)) if values else None,
        "p95": percentile(values, 0.95),
    }


def cost_summary(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    qwen_embedding = v1.read_json(RESULTS / "qwen_primary_v3/embedding_ledger.json")
    skillrouter_embedding = v1.read_json(RESULTS / "skillrouter_primary_v3/embedding_ledger.json")
    qwen_rerank = v1.read_json(RESULTS / "qwen_reranker_top20_v3/ledger.json")
    skillrouter_rerank = v1.read_json(RESULTS / "skillrouter_reranker_top20_v3/ledger.json")
    payload = v1.read_json(ROOT / "skill_benchmark/rq2bv1/preflight/qwen_primary_v3/payload_manifest.json")
    i3_manifest = v1.read_json(V3 / "i3c_extraction/manifest.json")

    b1_conditions: list[dict[str, Any]] = []
    for retriever in RETRIEVERS:
        for representation in REPRESENTATIONS:
            rows = stage_rows(b1, b2, stage="b1", first_stage_retriever=retriever, representation=representation)
            first = rows[0]
            one_time_values = {float(row["one_time_document_embedding_or_index_seconds"]) for row in rows}
            require(len(one_time_values) == 1, f"B1 fixed work drift: {retriever}/{representation}")
            documents = payload["documents"][representation]
            document_chunks = sum(len(document["chunk_text_ids"]) for document in documents)
            metadata = first.get("retriever_metadata", {})
            cold_embedding = [
                float(row.get("retriever_metadata", {}).get("cold_query_embedding_seconds", 0.0))
                for row in rows
                if "retriever_metadata" in row
            ]
            b1_conditions.append({
                "retriever": retriever,
                "representation": representation,
                "candidate_skills": len(documents),
                "document_chunks_or_windows": document_chunks if retriever == "qwen" else None,
                "selector_visible_corpus_tokens": int(first["selector_visible_tokens"]),
                "one_time_document_embedding_or_index_seconds": next(iter(one_time_values)),
                "query_seconds": summarize_distribution([float(row["query_seconds"]) for row in rows]),
                "cold_query_embedding_seconds": summarize_distribution(cold_embedding) if cold_embedding else None,
                "aggregation": metadata.get("document_aggregation", "lexical_index" if retriever == "bm25" else "not_persisted"),
                "notes": "Selector-visible corpus volume, not downstream agent-context tokens.",
            })

    b2_conditions: list[dict[str, Any]] = []
    for reranker_stage in ("qwen_b2", "skillrouter_b2"):
        reranker = reranker_stage.removesuffix("_b2")
        for retriever in RETRIEVERS:
            for representation in REPRESENTATIONS:
                rows = stage_rows(b1, b2, stage=reranker_stage, first_stage_retriever=retriever, representation=representation)
                if reranker == "qwen":
                    windows = [int(row["provider_document_count"]) for row in rows]
                    latency = [float(row["rerank_seconds"]) for row in rows]
                    forward = None
                else:
                    windows = [int(row["model_window_count"]) for row in rows]
                    latency = []
                    forward = [float(row["amortised_model_forward_seconds"]) for row in rows]
                b2_conditions.append({
                    "reranker": reranker,
                    "first_stage_retriever": retriever,
                    "representation": representation,
                    "fixed_top20_conditions": len(rows),
                    "candidate_pairs": len(rows) * 20,
                    "candidate_windows": sum(windows),
                    "latency_seconds": summarize_distribution(latency) if latency else None,
                    "amortised_model_forward_seconds": summarize_distribution(forward) if forward else None,
                    "selector_visible_rerank_tokens": "not persisted per condition",
                })

    return {
        "boundary": "Observed execution work only. No retrospective USD conversion is made.",
        "shared_i3_extraction": {
            "charge_rule": "One shared I3-family construction footprint; never charge it separately to I3-flat and I3C.",
            "source_rows": i3_manifest["counts"]["input_rows"],
            "source_chunks": i3_manifest["counts"]["chunks"],
            "input_proxy_tokens": i3_manifest["counts"]["total_qwen_proxy_tokens"],
            "durable_wall_time_or_invoice": "not available",
        },
        "b1_per_condition": b1_conditions,
        "qwen_embedding_physical_execution": {
            "successful_api_calls": qwen_embedding["successful_api_calls"],
            "document_texts": qwen_embedding["document_cache_misses"],
            "cold_query_texts": qwen_embedding["cold_query_requests"],
            "provider_tokens": qwen_embedding["provider_usage"]["total_tokens"],
            "elapsed_seconds": qwen_embedding["elapsed_seconds"],
        },
        "skillrouter_embedding_physical_execution": {
            "model_forward_batches": skillrouter_embedding["model_forward_batches"],
            "document_instances": skillrouter_embedding["document_cache_misses"],
            "query_instances": skillrouter_embedding["query_cache_misses"],
            "model_input_tokens": skillrouter_embedding["model_input_tokens"],
            "model_load_seconds": skillrouter_embedding["model_load_seconds"],
        },
        "b2_per_condition": b2_conditions,
        "qwen_reranker_physical_execution": qwen_rerank,
        "skillrouter_reranker_physical_execution": skillrouter_rerank,
    }


def rank_metrics(rank: int) -> dict[str, float]:
    return {
        "hit_at_1": float(int(rank == 1)),
        "mrr_at_20": float(1.0 / rank if 1 <= rank <= 20 else 0.0),
        "recall_at_20": float(int(rank <= 20)),
    }


def sensitivity_contrast(
    rows: list[dict[str, Any]], *, representation: str, stratum: str, metric: str
) -> dict[str, Any]:
    scope = [
        row
        for row in rows
        if row["representation"] == representation and row["stratum"] == stratum
    ]
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in scope:
        grouped[str(row["group"])].append(
            float(row["max_metrics"][metric]) - float(row["mean_metrics"][metric])
        )
    groups = sorted(grouped)
    values = np.asarray([mean(grouped[group]) for group in groups], dtype=np.float64)
    draws = values[bootstrap_indices(len(groups))].mean(axis=1)
    return {
        "representation": representation,
        "stratum": stratum,
        "metric": metric,
        "estimate_max_minus_mean": float(values.mean()),
        "ci_95_percentile": [
            float(np.quantile(draws, 0.025, method="linear")),
            float(np.quantile(draws, 0.975, method="linear")),
        ],
        "clusters": len(groups),
        "prompts": len(scope),
        "bootstrap": {
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed": BOOTSTRAP_SEED,
            "unit": "direct/paraphrase-averaged paired semantic cluster",
            "interval": "percentile 2.5th/97.5th",
        },
    }


def qwen_chunk_aggregation_sensitivity(
    b1: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    """Replay frozen Qwen max rankings and locally calculate mean-chunk ranks."""
    payload = v1.read_json(ROOT / "skill_benchmark/rq2bv1/preflight/qwen_primary_v3/payload_manifest.json")
    inventory_path = ROOT / "skill_benchmark/rq2bv1/preflight/qwen_primary_v3/text_inventory.jsonl"
    inventory = v1.read_jsonl(inventory_path)
    text_by_id = {str(row["text_id"]): str(row["text"]) for row in inventory}
    cache = ExactEmbeddingCache(ROOT / "skill_benchmark/cache/rq2bv1/embeddings")
    query_vectors: dict[str, np.ndarray] = {}
    for prompt_id, text_id in payload["query_text_ids"].items():
        vector = cache.load(text_by_id[str(text_id)])
        require(vector is not None, f"Missing persisted Qwen query vector: {prompt_id}")
        array = np.asarray(vector, dtype=np.float64)
        query_vectors[str(prompt_id)] = array / np.linalg.norm(array)

    frozen = {
        (str(row["representation"]), str(row["prompt_id"])): row
        for row in b1["qwen"]
    }
    replayed_conditions = 0
    records: list[dict[str, Any]] = []
    chunk_distributions: dict[str, Any] = {}
    for representation in SENSITIVITY_REPRESENTATIONS:
        documents = payload["documents"][representation]
        skill_ids = [str(document["skill_id"]) for document in documents]
        starts: list[int] = []
        counts: list[int] = []
        vectors: list[list[float]] = []
        for document in documents:
            starts.append(len(vectors))
            chunk_ids = [str(text_id) for text_id in document["chunk_text_ids"]]
            counts.append(len(chunk_ids))
            for text_id in chunk_ids:
                vector = cache.load(text_by_id[text_id])
                require(vector is not None, f"Missing persisted Qwen document vector: {representation}/{text_id}")
                vectors.append(vector)
        matrix = np.asarray(vectors, dtype=np.float64)
        matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
        starts_array = np.asarray(starts, dtype=np.int64)
        counts_array = np.asarray(counts, dtype=np.float64)
        chunk_distributions[representation] = {
            "candidate_skills": len(documents),
            "document_chunks": len(vectors),
            "chunks_per_skill": {
                "min": int(min(counts)),
                "median": float(statistics.median(counts)),
                "p95": percentile([float(value) for value in counts], 0.95),
                "max": int(max(counts)),
            },
        }
        for prompt_id, query_vector in query_vectors.items():
            chunk_scores = matrix @ query_vector
            max_scores = np.maximum.reduceat(chunk_scores, starts_array)
            mean_scores = np.add.reduceat(chunk_scores, starts_array) / counts_array
            max_ranking = sorted(zip(skill_ids, max_scores, strict=True), key=lambda item: (-item[1], item[0]))
            mean_ranking = sorted(zip(skill_ids, mean_scores, strict=True), key=lambda item: (-item[1], item[0]))
            frozen_row = frozen[(representation, prompt_id)]
            gold = str(frozen_row["gold_skill"])
            max_rank = next(index for index, (skill_id, _) in enumerate(max_ranking, start=1) if skill_id == gold)
            mean_rank = next(index for index, (skill_id, _) in enumerate(mean_ranking, start=1) if skill_id == gold)
            require(
                max_rank == int(frozen_row["strict_gold_rank"]),
                f"Frozen Qwen max-chunk gold-rank replay mismatch: {representation}/{prompt_id}",
            )
            require(
                set(skill_id for skill_id, _ in max_ranking[:20]) == set(frozen_row["top_20_skill_ids"]),
                f"Frozen Qwen max-chunk Top-20 membership replay mismatch: {representation}/{prompt_id}",
            )
            records.append({
                "representation": representation,
                "prompt_id": prompt_id,
                "group": frozen_row["group"],
                "stratum": frozen_row["stratum"],
                "gold_skill": gold,
                "max_rank": max_rank,
                "mean_rank": mean_rank,
                "max_metrics": rank_metrics(max_rank),
                "mean_metrics": rank_metrics(mean_rank),
            })
            replayed_conditions += 1

    summaries: list[dict[str, Any]] = []
    contrasts: list[dict[str, Any]] = []
    for representation in SENSITIVITY_REPRESENTATIONS:
        for stratum in PRIMARY_STRATA:
            scope = [row for row in records if row["representation"] == representation and row["stratum"] == stratum]
            for aggregation in ("max", "mean"):
                entry: dict[str, Any] = {
                    "representation": representation,
                    "stratum": stratum,
                    "aggregation": aggregation,
                    "n_prompts": len(scope),
                    "n_clusters": len({row["group"] for row in scope}),
                }
                for metric in ("hit_at_1", "mrr_at_20", "recall_at_20"):
                    prompt_values = [float(row[f"{aggregation}_metrics"][metric]) for row in scope]
                    groups: dict[str, list[float]] = defaultdict(list)
                    for row in scope:
                        groups[str(row["group"])].append(float(row[f"{aggregation}_metrics"][metric]))
                    entry[f"{metric}_prompt_weighted"] = mean(prompt_values)
                    entry[f"{metric}_cluster_macro"] = mean([mean(values) for values in groups.values()])
                summaries.append(entry)
            for metric in ("hit_at_1", "mrr_at_20", "recall_at_20"):
                contrasts.append(sensitivity_contrast(records, representation=representation, stratum=stratum, metric=metric))
    require(replayed_conditions == len(SENSITIVITY_REPRESENTATIONS) * 381, "Qwen sensitivity coverage drift")
    return {
        "status": "completed_local_cached_embedding_replay",
        "scope": "I2, I3-flat, and I3C only; Qwen cached vectors; no provider/model call.",
        "frozen_max_chunk_replay_conditions": replayed_conditions,
        "chunk_distributions": chunk_distributions,
        "summaries": summaries,
        "max_minus_mean_cluster_contrasts": contrasts,
    }


def validate_report(report: dict[str, Any]) -> dict[str, Any]:
    summaries = report["condition_summaries"]
    require(len(summaries) == 108, "Expected 108 condition/stratum summaries")
    contrasts = report["contrasts"]
    require(bool(contrasts), "No B3-v2 contrasts produced")
    for contrast in contrasts:
        require("p_value" not in contrast and "holm" not in contrast, "B3-v2 must not write p/Holm")
        require(contrast["stratum"] in PRIMARY_STRATA, "Contrast is not stratum-specific")
        require(contrast["bootstrap"]["resamples"] == BOOTSTRAP_RESAMPLES, "Bootstrap resample drift")
        require(contrast["bootstrap"]["seed"] == BOOTSTRAP_SEED, "Bootstrap seed drift")
    family_counts = Counter(contrast["family"] for contrast in contrasts)
    return {
        "state": "pass",
        "condition_summary_rows": len(summaries),
        "contrast_rows": len(contrasts),
        "contrast_family_counts": dict(sorted(family_counts.items())),
        "no_p_values_or_holm": True,
        "b3_v1_preserved_path": "skill_benchmark/rq2bv1/results/b3_v3/",
        "new_output_path": "skill_benchmark/rq2bv1/results/b3_v3_v2/",
    }


def markdown_summary(report: dict[str, Any]) -> str:
    lines = [
        "# RQ2b V3 B3-v2 Local Analysis",
        "",
        "Status: `COMPLETED LOCAL-ONLY POST-HOC SYNTHESIS / PENDING USER REVIEW / NOT THESIS TEXT`",
        "",
        "## Scope And Claim Boundary",
        "",
        "- Frozen inputs only: 2,433 skills, 381 strict-gold prompts, and 86 semantic clusters.",
        "- `controlled` (25 clusters / 243 prompts) and `public_gold` (61 clusters / 138 prompts) are reported separately.",
        "- Strict metrics measure agreement with the frozen single-gold label, not uniquely correct routing or downstream task success.",
        "- Qwen B1 is max-over-document-chunks dense retrieval. SkillRouter B1 is full-context single-vector dense retrieval.",
        "- B2 representation contrasts are end-to-end pipeline comparisons. Conditional reranker metrics apply only within the same persisted Top-20 candidate list.",
        "- This post-hoc report uses equal-cluster, within-stratum paired bootstrap stability intervals (20,000 resamples; seed 2026082303). It reports no p-values, Holm adjustment, or significance decision.",
        "- This analysis does not test graph, tree, DAG, or field-aware retrieval.",
        "",
        "## Input Validation",
        "",
        f"- {report['input_validation']['prompt_count']} prompts, {report['input_validation']['group_count']} clusters, {report['input_validation']['b1_rows_per_retriever']} B1 rows per retriever, and {report['input_validation']['b2_rows_per_reranker']} B2 rows per reranker.",
        "- Every B2 row replayed its B1 strict-gold, group, stratum, prompt hash, and exact persisted Top-20 candidate binding.",
        "",
        "## Primary Cluster-Macro H@1",
        "",
        "| Stratum | First stage | Representation | B1 | Qwen B2 end-to-end | SkillRouter B2 end-to-end |",
        "|---|---|---|---:|---:|---:|",
    ]
    summaries = report["condition_summaries"]
    for stratum in PRIMARY_STRATA:
        for retriever in RETRIEVERS:
            for representation in REPRESENTATIONS:
                def get(stage: str) -> dict[str, Any]:
                    return next(row for row in summaries if row["stratum"] == stratum and row["stage"] == stage and row["first_stage_retriever"] == retriever and row["representation"] == representation)
                b1_row = get("b1")
                qwen_row = get("qwen_b2")
                skillrouter_row = get("skillrouter_b2")
                lines.append(
                    f"| {stratum} | {retriever} | {representation} | {b1_row['hit_at_1_cluster_macro']:.3f} | {qwen_row['hit_at_1_cluster_macro']:.3f} | {skillrouter_row['hit_at_1_cluster_macro']:.3f} |"
                )
    lines += [
        "",
        "## Complete Contrast Matrix",
        "",
        f"- {report['local_validation']['contrast_rows']} paired contrast rows were generated across all predeclared representation, retriever, and fixed-Top-20 reranker comparison families.",
        "- The full interval table is `B3_V2_COMPLETE_CONTRASTS.md`; no single favourable contrast is selected as the result.",
        "",
        "## Cost Boundary",
        "",
        "- I3 extraction is shown once as shared construction footprint and is not double-charged to I3-flat and I3C.",
        "- The table's one-time seconds are B1 document embedding or lexical-index construction only. They are not complete representation-construction costs.",
        "- No durable, comparable I3/I3C extraction wall-time or provider invoice exists in V3; it is therefore reported only as a one-time source/chunk/proxy-token footprint, never as a complete time or USD comparison.",
        "- B1 selector-visible tokens are candidate-representation corpus volume, not agent-visible downstream context tokens.",
        "- Per-condition B1 and B2 work, global provider/model ledger facts, and warm/cold timing where persisted are in the JSON report.",
        "",
        "| B1 retriever | Representation | One-time seconds | Mean query seconds | Selector-visible corpus tokens |",
        "|---|---|---:|---:|---:|",
    ]
    for row in report["cost"]["b1_per_condition"]:
        lines.append(
            f"| {row['retriever']} | {row['representation']} | {row['one_time_document_embedding_or_index_seconds']:.3f} | {row['query_seconds']['mean']:.6f} | {row['selector_visible_corpus_tokens']} |"
        )
    sensitivity = report["qwen_max_vs_mean_chunk_sensitivity"]
    lines += [
        "",
        "## Qwen Max-Chunk Sensitivity",
        "",
        f"- Replayed {sensitivity['frozen_max_chunk_replay_conditions']} frozen Qwen max-chunk rankings from persisted vectors and calculated a local mean-chunk sensitivity for I2/I3-flat/I3C without a provider/model call.",
        "- I3-flat and I3C each contain exactly one chunk per skill, so their zero max-versus-mean differences are true by construction. I2 has only three two-chunk skills; its reported zero differences establish unchanged strict-gold H@1, MRR@20, and Recall@20 at these strata, not identical scores, complete rankings, or general insensitivity to chunk aggregation.",
        "- Detailed distribution and max-minus-mean interval results are in `B3_V2_QWEN_CHUNK_SENSITIVITY.md`.",
        "",
        "## Next Gate",
        "",
        "User review of these local outputs is required before any thesis LaTeX/PDF update.",
        "",
    ]
    return "\n".join(lines)


def markdown_contrasts(contrasts: list[dict[str, Any]]) -> str:
    lines = [
        "# RQ2b V3 B3-v2 Complete Predeclared Paired Contrasts",
        "",
        "Status: `LOCAL-ONLY / POST-HOC / PENDING USER REVIEW / NOT THESIS TEXT`",
        "",
        "Every predeclared comparison receives the same equal-cluster, within-stratum paired bootstrap treatment. A confidence interval is a fixed-benchmark stability range, not a significance decision or proof of equivalence when it crosses zero.",
        "",
        "| Family | Label | Stratum | Metric | Conditional fixed Top-20 only | Delta (left - right) | 95% percentile CI | Clusters | Prompts | L/T/R cluster counts |",
        "|---|---|---|---|---|---:|---|---:|---:|---:|",
    ]
    for row in contrasts:
        low, high = row["ci_95_percentile"]
        lines.append(
            f"| {row['family']} | {row['label']} | {row['stratum']} | {row['metric']} | {str(row['conditional_on_gold_in_top20']).lower()} | {row['estimate_left_minus_right']:+.3f} | [{low:+.3f}, {high:+.3f}] | {row['clusters']} | {row['prompts']} | {row['cluster_left_win_count']}/{row['cluster_tie_count']}/{row['cluster_right_win_count']} |"
        )
    lines.append("")
    return "\n".join(lines)


def markdown_sensitivity(sensitivity: dict[str, Any]) -> str:
    lines = [
        "# RQ2b V3 Qwen Max-Chunk Versus Mean-Chunk Sensitivity",
        "",
        "Status: `LOCAL CACHED-VECTOR REPLAY / PENDING USER REVIEW / NOT THESIS TEXT`",
        "",
        sensitivity["scope"],
        "",
        "## Chunk Distributions",
        "",
        "| Representation | Skills | Chunks | Min chunks/skill | Median | P95 | Max |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for representation, stats in sensitivity["chunk_distributions"].items():
        counts = stats["chunks_per_skill"]
        lines.append(f"| {representation} | {stats['candidate_skills']} | {stats['document_chunks']} | {counts['min']} | {counts['median']:.1f} | {counts['p95']:.1f} | {counts['max']} |")
    lines += [
        "",
        "## Interpretation Boundary",
        "",
        "I3-flat and I3C have exactly one chunk per skill, so their zero max-minus-mean values are true by construction. I2 contains only three two-chunk skills. For I2, this sensitivity establishes unchanged strict-gold H@1, MRR@20, and Recall@20 at the reported cluster-macro strata; it does not establish identical scores, complete rankings, or general insensitivity to chunk aggregation.",
        "",
        "## Paired Cluster-Max Minus Mean Contrasts",
        "",
        "| Representation | Stratum | Metric | Delta (max - mean) | 95% percentile CI | Clusters | Prompts |",
        "|---|---|---|---:|---|---:|---:|",
    ]
    for row in sensitivity["max_minus_mean_cluster_contrasts"]:
        low, high = row["ci_95_percentile"]
        lines.append(f"| {row['representation']} | {row['stratum']} | {row['metric']} | {row['estimate_max_minus_mean']:+.3f} | [{low:+.3f}, {high:+.3f}] | {row['clusters']} | {row['prompts']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    parser.add_argument(
        "--rewrite-markdown-only",
        action="store_true",
        help="Regenerate only explanatory Markdown from an existing local B3-v2 JSON report.",
    )
    args = parser.parse_args()
    output_root = args.output_root.resolve()
    if args.rewrite_markdown_only:
        require(output_root.is_dir(), f"Missing B3-v2 output root: {output_root}")
        report = json.loads((output_root / "b3_v2_local_analysis.json").read_text(encoding="utf-8"))
        (output_root / "B3_V2_LOCAL_ANALYSIS.md").write_text(markdown_summary(report), encoding="utf-8")
        (output_root / "B3_V2_COMPLETE_CONTRASTS.md").write_text(markdown_contrasts(report["contrasts"]), encoding="utf-8")
        (output_root / "B3_V2_QWEN_CHUNK_SENSITIVITY.md").write_text(markdown_sensitivity(report["qwen_max_vs_mean_chunk_sensitivity"]), encoding="utf-8")
        print(json.dumps({"state": "rewrote_explanatory_markdown_only", "output_root": str(output_root)}, indent=2))
        return
    require(not output_root.exists(), f"Refusing to overwrite existing B3-v2 output: {output_root}")

    b1 = {name: v1.read_jsonl(path) for name, path in v1.B1_PATHS.items()}
    b2 = {name: v1.read_jsonl(path) for name, path in v1.B2_PATHS.items()}
    input_validation = v1.verify_inputs(b1, b2)
    contrasts = [
        *representation_comparisons(b1, b2),
        *retriever_comparisons(b1, b2),
        *reranker_comparisons(b1, b2),
    ]
    report: dict[str, Any] = {
        "schema_version": "rq2bv1-v3-b3-v2-local-analysis-v1",
        "state": "completed_local_only_post_hoc_synthesis_pending_user_review_not_thesis_text",
        "protocol": "skill_benchmark/rq2bv1/analysis_protocols/B3_V2_THESIS_REPORTING_AMENDMENT.md",
        "review_log": "skill_benchmark/rq2bv1/analysis_protocols/B3_V2_INDEPENDENT_REVIEW_LOG.md",
        "inputs": {
            "b1": {name: {"path": str(path.relative_to(ROOT)), "sha256": v1.sha256(path)} for name, path in v1.B1_PATHS.items()},
            "b2": {name: {"path": str(path.relative_to(ROOT)), "sha256": v1.sha256(path)} for name, path in v1.B2_PATHS.items()},
        },
        "input_validation": input_validation,
        "condition_summaries": all_condition_summaries(b1, b2),
        "contrasts": contrasts,
        "failure_analysis": failure_analysis(b1, b2),
        "cost": cost_summary(b1, b2),
        "qwen_max_vs_mean_chunk_sensitivity": qwen_chunk_aggregation_sensitivity(b1),
    }
    report["local_validation"] = validate_report(report)

    output_root.mkdir(parents=True, exist_ok=False)
    (output_root / "b3_v2_local_analysis.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_root / "B3_V2_LOCAL_ANALYSIS.md").write_text(markdown_summary(report), encoding="utf-8")
    (output_root / "B3_V2_COMPLETE_CONTRASTS.md").write_text(markdown_contrasts(contrasts), encoding="utf-8")
    (output_root / "B3_V2_QWEN_CHUNK_SENSITIVITY.md").write_text(markdown_sensitivity(report["qwen_max_vs_mean_chunk_sensitivity"]), encoding="utf-8")
    (output_root / "B3_V2_VALIDATION.json").write_text(
        json.dumps(report["local_validation"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output_root": str(output_root), "validation": report["local_validation"]}, indent=2))


if __name__ == "__main__":
    main()
