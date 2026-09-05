#!/usr/bin/env python3
"""Local B3 analysis for the completed RQ2b V3 B1/B2 matrix.

This script is deliberately read-only with respect to frozen result artifacts.
It validates result provenance, produces grouped paired statistics, decomposes
fixed/online cost measures, and classifies B1/B2 failures.
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

from rq2b_statistics import holm_adjust


ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18"
RESULTS = ROOT / "skill_benchmark/rq2bv1/results"
OUTPUT_ROOT = RESULTS / "b3_v3"
REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3-flat-evidence",
    "i3c-fielded-evidence",
)
RETRIEVERS = ("bm25", "qwen", "skillrouter")
RERANKERS = ("qwen", "skillrouter")
STRATA = ("combined", "controlled", "public_gold")
BOOTSTRAP_RESAMPLES = 10_000
SIGN_FLIP_DRAWS = 100_000
BOOTSTRAP_SEED = 2026082301
SIGN_FLIP_SEED = 2026082302
AMORTIZATION_QUERY_COUNTS = (1, 10, 100, 1_000, 10_000, 100_000)
B1_PATHS = {
    "bm25": V3 / "b1l_preflight_v3/b1l_local_bm25_run/b1l_strict_results.jsonl",
    "qwen": RESULTS / "qwen_primary_v3/qwen_primary_strict_results.jsonl",
    "skillrouter": RESULTS / "skillrouter_primary_v3/local_scoring_path_contract_amendment/skillrouter_primary_strict_results.jsonl",
}
B2_PATHS = {
    "qwen": RESULTS / "qwen_reranker_top20_v3/rows.jsonl",
    "skillrouter": RESULTS / "skillrouter_reranker_top20_v3/rows.jsonl",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"Missing input: {path}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(rows, f"No rows in {path}")
    return rows


def sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_retriever(value: str) -> str:
    value = value.lower()
    if value == "bm25":
        return "bm25"
    if "qwen" in value:
        return "qwen"
    if "skillrouter" in value:
        return "skillrouter"
    raise RuntimeError(f"Unknown retriever: {value}")


def b1_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["prompt_id"]), str(row["representation"]), canonical_retriever(str(row["retriever"])))


def b2_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["prompt_id"]), str(row["representation"]), canonical_retriever(str(row["first_stage_retriever"])))


def condition_key(row: dict[str, Any]) -> tuple[str, str, str]:
    """Stage-neutral identity for a fixed prompt/representation/retriever."""
    retriever = row.get("retriever", row.get("first_stage_retriever"))
    return (str(row["prompt_id"]), str(row["representation"]), canonical_retriever(str(retriever)))


def representation_pair_key(row: dict[str, Any]) -> tuple[str, str]:
    """Identity for I3C-versus-I2 comparisons, which intentionally vary representation."""
    retriever = row.get("retriever", row.get("first_stage_retriever"))
    return (str(row["prompt_id"]), canonical_retriever(str(retriever)))


def mrr_at_20(rank: int) -> float:
    return 1.0 / rank if 1 <= rank <= 20 else 0.0


def b1_metric(row: dict[str, Any], metric: str) -> float:
    rank = int(row["strict_gold_rank"])
    if metric == "hit_at_1":
        return float(int(rank == 1))
    if metric == "mrr_at_20":
        return mrr_at_20(rank)
    if metric == "recall_at_20":
        return float(int(rank <= 20))
    raise RuntimeError(f"Unknown B1 metric: {metric}")


def b2_metric(row: dict[str, Any], metric: str) -> float:
    if metric == "hit_at_1":
        return float(row["end_to_end_strict_top1"])
    if metric == "mrr_at_20":
        return float(row["end_to_end_strict_mrr_at_20"])
    raise RuntimeError(f"Unknown B2 metric: {metric}")


def filtered(rows: list[dict[str, Any]], stratum: str) -> list[dict[str, Any]]:
    return rows if stratum == "combined" else [row for row in rows if row["stratum"] == stratum]


def mean(values: list[float]) -> float:
    require(values, "Cannot average an empty list")
    return sum(values) / len(values)


def metric_summary(rows: list[dict[str, Any]], extractor: Callable[[dict[str, Any]], float]) -> dict[str, Any]:
    values = [extractor(row) for row in rows]
    return {"n_prompts": len(rows), "value": mean(values)}


def make_difference_rows(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
    *,
    key: Callable[[dict[str, Any]], tuple[Any, ...]],
    extractor: Callable[[dict[str, Any]], float],
    stratum: str,
    match_fields: tuple[str, ...] = ("prompt_id", "group", "stratum", "gold_skill", "representation"),
) -> list[dict[str, Any]]:
    left_map = {key(row): row for row in left}
    right_map = {key(row): row for row in right}
    require(len(left_map) == len(left), "Left paired input has duplicate keys")
    require(len(right_map) == len(right), "Right paired input has duplicate keys")
    require(set(left_map) == set(right_map), "Paired inputs do not cover identical conditions")
    output: list[dict[str, Any]] = []
    for item in sorted(left_map):
        a, b = left_map[item], right_map[item]
        for field in match_fields:
            require(a[field] == b[field], f"Paired {field} mismatch: {item}")
        if stratum != "combined" and a["stratum"] != stratum:
            continue
        output.append({"group": a["group"], "difference": extractor(a) - extractor(b)})
    require(output, f"No paired rows for {stratum}")
    return output


def inference(
    differences: list[dict[str, Any]], *, direction: str, label: str
) -> dict[str, Any]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in differences:
        grouped[str(row["group"])].append(float(row["difference"]))
    groups = sorted(grouped)
    group_sums = np.array([sum(grouped[group]) for group in groups], dtype=np.float64)
    group_counts = np.array([len(grouped[group]) for group in groups], dtype=np.float64)
    prompt_count = int(group_counts.sum())
    estimate = float(group_sums.sum() / prompt_count)
    equal_group_sensitivity = float(np.mean(group_sums / group_counts))

    bootstrap_rng = np.random.default_rng(BOOTSTRAP_SEED)
    sampled = bootstrap_rng.integers(0, len(groups), size=(BOOTSTRAP_RESAMPLES, len(groups)))
    bootstrap_draws = group_sums[sampled].sum(axis=1) / group_counts[sampled].sum(axis=1)

    sign_rng = np.random.default_rng(SIGN_FLIP_SEED)
    signs = sign_rng.integers(0, 2, size=(SIGN_FLIP_DRAWS, len(groups)), dtype=np.int8)
    signs = signs * 2 - 1
    sign_flip_draws = (signs @ group_sums) / prompt_count
    two_sided_p = float((1 + np.count_nonzero(np.abs(sign_flip_draws) >= abs(estimate))) / (SIGN_FLIP_DRAWS + 1))
    output = {
        "label": label,
        "direction": direction,
        "estimate": estimate,
        "equal_group_sensitivity": equal_group_sensitivity,
        "ci_95": [float(np.quantile(bootstrap_draws, 0.025, method="linear")), float(np.quantile(bootstrap_draws, 0.975, method="linear"))],
        "groups": len(groups),
        "prompts": prompt_count,
        "bootstrap": {"resamples": BOOTSTRAP_RESAMPLES, "seed": BOOTSTRAP_SEED},
        "sign_flip": {"draws": SIGN_FLIP_DRAWS, "seed": SIGN_FLIP_SEED},
        "two_sided_p_value": two_sided_p,
    }
    if direction == "positive_one_sided":
        output["positive_one_sided_p_value"] = float(
            (1 + np.count_nonzero(sign_flip_draws >= estimate)) / (SIGN_FLIP_DRAWS + 1)
        )
    return output


def decorate_holm(records: list[dict[str, Any]], p_key: str) -> None:
    p_values = {record["label"]: float(record[p_key]) for record in records}
    for record in records:
        record["holm"] = holm_adjust(p_values)[record["label"]]


def verify_inputs(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    expected_b1 = 381 * 4
    expected_b2 = 381 * 4 * 3
    for retriever, rows in b1.items():
        require(len(rows) == expected_b1, f"{retriever} B1 row count is not {expected_b1}")
        keys = {b1_key(row) for row in rows}
        require(len(keys) == expected_b1, f"{retriever} B1 keys are not unique")
        require({key[2] for key in keys} == {retriever}, f"{retriever} B1 retriever binding drift")
        require({key[1] for key in keys} == set(REPRESENTATIONS), f"{retriever} B1 representation coverage drift")
    for reranker, rows in b2.items():
        require(len(rows) == expected_b2, f"{reranker} B2 row count is not {expected_b2}")
        keys = {b2_key(row) for row in rows}
        require(len(keys) == expected_b2, f"{reranker} B2 keys are not unique")

    combined_b1 = {b1_key(row): row for rows in b1.values() for row in rows}
    require(len(combined_b1) == expected_b2, "Combined B1 keys do not cover 12 cells")
    for reranker, rows in b2.items():
        for row in rows:
            key = b2_key(row)
            first = combined_b1[key]
            for field in ("gold_skill", "group", "stratum", "prompt_sha256"):
                require(row[field] == first[field], f"{reranker} B2 {field} drift: {key}")
            require(row["candidate_skill_ids"] == first["top_20_skill_ids"], f"{reranker} fixed Top-20 drift: {key}")
            require(
                int(row["strict_candidate_positive"]) == int(b1_metric(first, "recall_at_20")),
                f"{reranker} B2 candidate presence drift: {key}",
            )
            require(
                int(row["first_stage_strict_top1"]) == int(b1_metric(first, "hit_at_1")),
                f"{reranker} B2 first-stage top-one drift: {key}",
            )
    metadata_rows = list(combined_b1.values())
    stratum_prompt_counts = Counter(row["stratum"] for row in metadata_rows if row["representation"] == REPRESENTATIONS[0] and row["retriever"] == metadata_rows[0]["retriever"])
    group_strata: dict[str, set[str]] = defaultdict(set)
    for row in metadata_rows:
        group_strata[str(row["group"])].add(str(row["stratum"]))
    require(all(len(values) == 1 for values in group_strata.values()), "A group spans strata")
    return {
        "b1_rows_per_retriever": expected_b1,
        "b2_rows_per_reranker": expected_b2,
        "prompt_count": 381,
        "group_count": len(group_strata),
        "stratum_prompt_counts": dict(sorted(stratum_prompt_counts.items())),
        "stratum_group_counts": dict(sorted(Counter(next(iter(v)) for v in group_strata.values()).items())),
    }


def representation_contrasts(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    definitions = (
        ("i3c_minus_i2", "i3c-fielded-evidence", "i2-original", "primary"),
        ("i3c_minus_i3_flat", "i3c-fielded-evidence", "i3-flat-evidence", "secondary"),
        ("i2_minus_i1", "i2-original", "i1-discovery", "secondary"),
    )
    output: dict[str, Any] = {}
    for name, left_rep, right_rep, role in definitions:
        records_by_metric: dict[str, list[dict[str, Any]]] = {"hit_at_1": [], "mrr_at_20": []}
        for retriever in RETRIEVERS:
            for stage, rows, key, extractor in (
                ("b1", b1[retriever], b1_key, b1_metric),
                ("b2_qwen", b2["qwen"], b2_key, b2_metric),
                ("b2_skillrouter", b2["skillrouter"], b2_key, b2_metric),
            ):
                left = [row for row in rows if row["representation"] == left_rep and canonical_retriever(str(row.get("retriever", row.get("first_stage_retriever")))) == retriever]
                right = [row for row in rows if row["representation"] == right_rep and canonical_retriever(str(row.get("retriever", row.get("first_stage_retriever")))) == retriever]
                for metric in records_by_metric:
                    differences = make_difference_rows(
                        left,
                        right,
                        key=representation_pair_key,
                        extractor=lambda row, m=metric, e=extractor: e(row, m),
                        stratum="combined",
                        match_fields=("prompt_id", "group", "stratum", "gold_skill"),
                    )
                    records_by_metric[metric].append(inference(differences, direction="two_sided", label=f"{stage}/{retriever}/{metric}"))
        for records in records_by_metric.values():
            decorate_holm(records, "two_sided_p_value")
        output[name] = {
            "role": role,
            "left_minus_right": f"{left_rep} - {right_rep}",
            "combined_only": records_by_metric,
        }
    return output


def reranker_contrasts(b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    gains: dict[str, list[dict[str, Any]]] = {"hit_at_1": [], "mrr_at_20": []}
    comparisons: dict[str, list[dict[str, Any]]] = {"hit_at_1": [], "mrr_at_20": []}
    for retriever in RETRIEVERS:
        base = [row for row in b1[retriever]]
        qwen_rows = [row for row in b2["qwen"] if canonical_retriever(row["first_stage_retriever"]) == retriever]
        sr_rows = [row for row in b2["skillrouter"] if canonical_retriever(row["first_stage_retriever"]) == retriever]
        for representation in REPRESENTATIONS:
            base_rep = [row for row in base if row["representation"] == representation]
            qwen_rep = [row for row in qwen_rows if row["representation"] == representation]
            sr_rep = [row for row in sr_rows if row["representation"] == representation]
            for reranker, rows in (("qwen", qwen_rep), ("skillrouter", sr_rep)):
                for metric in gains:
                    differences = make_difference_rows(
                        rows,
                        base_rep,
                        key=condition_key,
                        extractor=lambda row, m=metric: b2_metric(row, m) if "end_to_end_strict_top1" in row else b1_metric(row, m),
                        stratum="combined",
                    )
                    record = inference(differences, direction="positive_one_sided", label=f"{reranker}/{retriever}/{representation}/{metric}")
                    gains[metric].append(record)
            for metric in comparisons:
                differences = make_difference_rows(qwen_rep, sr_rep, key=condition_key, extractor=lambda row, m=metric: b2_metric(row, m), stratum="combined")
                comparisons[metric].append(inference(differences, direction="two_sided", label=f"qwen_minus_skillrouter/{retriever}/{representation}/{metric}"))
    for records in gains.values():
        decorate_holm(records, "positive_one_sided_p_value")
    for records in comparisons.values():
        decorate_holm(records, "two_sided_p_value")
    return {"b2_minus_b1": gains, "qwen_minus_skillrouter": comparisons}


def condition_summaries(
    b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    b1_all = {b1_key(row): row for rows in b1.values() for row in rows}
    for retriever in RETRIEVERS:
        for representation in REPRESENTATIONS:
            base_rows = [row for row in b1[retriever] if row["representation"] == representation]
            for stratum in STRATA:
                base_scope = filtered(base_rows, stratum)
                row: dict[str, Any] = {
                    "stage": "b1",
                    "first_stage_retriever": retriever,
                    "representation": representation,
                    "reranker": None,
                    "stratum": stratum,
                    "hit_at_1": metric_summary(base_scope, lambda value: b1_metric(value, "hit_at_1"))["value"],
                    "mrr_at_20": metric_summary(base_scope, lambda value: b1_metric(value, "mrr_at_20"))["value"],
                    "recall_at_20": metric_summary(base_scope, lambda value: b1_metric(value, "recall_at_20"))["value"],
                    "n_prompts": len(base_scope),
                }
                output.append(row)
            for reranker in RERANKERS:
                reranked_rows = [row for row in b2[reranker] if b2_key(row)[1:] == (representation, retriever)]
                require(len(reranked_rows) == 381, f"Missing B2 condition: {reranker}/{retriever}/{representation}")
                for stratum in STRATA:
                    scope = filtered(reranked_rows, stratum)
                    present = [row for row in scope if int(row["strict_candidate_positive"]) == 1]
                    corrections = [row for row in scope if int(row["strict_reranker_gain"]) == 1]
                    regressions = [row for row in scope if int(row["strict_reranker_regression"]) == 1]
                    output.append({
                        "stage": "b2",
                        "first_stage_retriever": retriever,
                        "representation": representation,
                        "reranker": reranker,
                        "stratum": stratum,
                        "n_prompts": len(scope),
                        "hit_at_1": mean([b2_metric(row, "hit_at_1") for row in scope]),
                        "mrr_at_20": mean([b2_metric(row, "mrr_at_20") for row in scope]),
                        "recall_at_20_fixed_from_b1": mean([float(row["strict_candidate_positive"]) for row in scope]),
                        "conditional_hit_at_1_given_gold_in_top20": mean([b2_metric(row, "hit_at_1") for row in present]) if present else None,
                        "reranker_corrections": len(corrections),
                        "reranker_regressions": len(regressions),
                    })
    return output


def failure_analysis(b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    b1_all = {b1_key(row): row for rows in b1.values() for row in rows}
    for reranker in RERANKERS:
        for retriever in RETRIEVERS:
            for representation in REPRESENTATIONS:
                rows = [row for row in b2[reranker] if b2_key(row)[1:] == (representation, retriever)]
                for stratum in STRATA:
                    scope = filtered(rows, stratum)
                    counts = Counter()
                    examples: dict[str, list[str]] = defaultdict(list)
                    for row in scope:
                        first = b1_all[b2_key(row)]
                        miss = int(row["strict_candidate_positive"]) == 0
                        b1_top1 = int(row["first_stage_strict_top1"]) == 1
                        b2_top1 = int(row["reranked_strict_top1"]) == 1
                        labels = []
                        if miss:
                            labels.append("candidate_miss")
                        if not miss and not b2_top1:
                            labels.append("ordering_error")
                        if not b1_top1 and b2_top1:
                            labels.append("reranker_correction")
                        if b1_top1 and not b2_top1:
                            labels.append("reranker_regression")
                        if not b1_top1 and not b2_top1:
                            labels.append("persistent_top1_error")
                        for label in labels:
                            counts[label] += 1
                            if len(examples[label]) < 5:
                                examples[label].append(str(row["prompt_id"]))
                    output.append({
                        "reranker": reranker,
                        "first_stage_retriever": retriever,
                        "representation": representation,
                        "stratum": stratum,
                        "n_prompts": len(scope),
                        "counts": dict(sorted(counts.items())),
                        "rates": {name: count / len(scope) for name, count in sorted(counts.items())},
                        "example_prompt_ids": dict(sorted(examples.items())),
                    })
    return output


def cost_summary(b1: dict[str, list[dict[str, Any]]], b2: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    qwen_embedding = read_json(RESULTS / "qwen_primary_v3/embedding_ledger.json")
    skillrouter_embedding = read_json(RESULTS / "skillrouter_primary_v3/embedding_ledger.json")
    qwen_rerank = read_json(RESULTS / "qwen_reranker_top20_v3/ledger.json")
    sr_rerank = read_json(RESULTS / "skillrouter_reranker_top20_v3/ledger.json")
    i3c_input_manifest = read_json(V3 / "i3c_extraction/manifest.json")
    i3c_input_counts = i3c_input_manifest["counts"]
    b1_conditions: list[dict[str, Any]] = []
    for retriever in RETRIEVERS:
        for representation in REPRESENTATIONS:
            scope = [row for row in b1[retriever] if row["representation"] == representation]
            one_time = {float(row["one_time_document_embedding_or_index_seconds"]) for row in scope}
            require(len(one_time) == 1, f"One-time B1 cost varies within {retriever}/{representation}")
            query_seconds = [float(row["query_seconds"]) for row in scope]
            selector_tokens = [int(row["selector_visible_tokens"]) for row in scope]
            condition = {
                "retriever": retriever,
                "representation": representation,
                "one_time_document_embedding_or_index_seconds": next(iter(one_time)),
                "query_seconds_mean": statistics.mean(query_seconds),
                "query_seconds_median": statistics.median(query_seconds),
                "query_seconds_p95": sorted(query_seconds)[math.ceil(0.95 * len(query_seconds)) - 1],
                "selector_visible_tokens": selector_tokens[0],
                "selector_visible_tokens_interpretation": (
                    "Recorded candidate-representation corpus token volume for this condition; "
                    "not post-selection agent context tokens."
                ),
            }
            condition["b1_amortised_seconds_per_query"] = [
                {
                    "queries": count,
                    "seconds": condition["one_time_document_embedding_or_index_seconds"] / count
                    + condition["query_seconds_mean"],
                }
                for count in AMORTIZATION_QUERY_COUNTS
            ]
            b1_conditions.append(condition)
    return {
        "scope": "Measured execution work only; no retrospective USD conversion without a pinned price source.",
        "i3c_construction_input_footprint": {
            "source_rows": i3c_input_counts["input_rows"],
            "source_chunks": i3c_input_counts["chunks"],
            "input_proxy_tokens": i3c_input_counts["total_qwen_proxy_tokens"],
            "external_api_calls": i3c_input_manifest["external_api_calls"],
            "network_calls": i3c_input_manifest["network_calls"],
            "time_interpretation": (
                "V3 records the bounded construction input volume but not a durable, directly comparable "
                "extraction wall-time or provider-cost ledger. It is reported as a one-time footprint, "
                "not folded into the measured B1 seconds."
            ),
        },
        "b1_per_condition": b1_conditions,
        "qwen_embedding_physical_execution": {
            "successful_api_calls": qwen_embedding["successful_api_calls"],
            "text_rows": qwen_embedding["text_rows"],
            "elapsed_seconds": qwen_embedding["elapsed_seconds"],
            "external_submission_proxy_tokens": qwen_embedding["external_submission_proxy_tokens"],
        },
        "skillrouter_embedding_physical_execution": {
            "model_forward_batches": skillrouter_embedding["model_forward_batches"],
            "model_input_instances": skillrouter_embedding["model_input_instances"],
            "model_input_tokens": skillrouter_embedding["model_input_tokens"],
        },
        "qwen_reranker_physical_execution": qwen_rerank,
        "skillrouter_reranker_physical_execution": sr_rerank,
        "b2_per_condition": {
            "qwen": {
                "mean_rerank_seconds": statistics.mean(float(row["rerank_seconds"]) for row in b2["qwen"]),
                "median_rerank_seconds": statistics.median(float(row["rerank_seconds"]) for row in b2["qwen"]),
                "p95_rerank_seconds": sorted(float(row["rerank_seconds"]) for row in b2["qwen"])[math.ceil(0.95 * len(b2["qwen"])) - 1],
            },
            "skillrouter": {
                "mean_amortised_model_forward_seconds": statistics.mean(float(row["amortised_model_forward_seconds"]) for row in b2["skillrouter"]),
                "median_amortised_model_forward_seconds": statistics.median(float(row["amortised_model_forward_seconds"]) for row in b2["skillrouter"]),
                "p95_amortised_model_forward_seconds": sorted(float(row["amortised_model_forward_seconds"]) for row in b2["skillrouter"])[math.ceil(0.95 * len(b2["skillrouter"])) - 1],
                "interpretation": "Summed/amortised model-forward work per fixed condition, not an interactive end-to-end latency measurement.",
            },
        },
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# RQ2b V3 B3 Local Analysis",
        "",
        "Status: `COMPLETED LOCAL ANALYSIS / PENDING USER REVIEW / NOT THESIS TEXT`",
        "",
        "## Input Validation",
        "",
        f"- {report['input_validation']['prompt_count']} strict prompts in {report['input_validation']['group_count']} groups.",
        f"- Prompt strata: `{report['input_validation']['stratum_prompt_counts']}`.",
        "- Every B2 row was checked against its matching B1 row for gold, group, stratum, prompt hash, fixed Top-20 identity, candidate presence, and B1 Top-1 state.",
        "",
        "## Combined B1 And B2 Results",
        "",
        "| First stage | Representation | B1 H@1 | B1 MRR@20 | B1 R@20 | Qwen B2 H@1 | SkillRouter B2 H@1 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    summaries = report["condition_summaries"]
    for retriever in RETRIEVERS:
        for representation in REPRESENTATIONS:
            b1_row = next(row for row in summaries if row["stage"] == "b1" and row["stratum"] == "combined" and row["first_stage_retriever"] == retriever and row["representation"] == representation)
            qwen = next(row for row in summaries if row["stage"] == "b2" and row["stratum"] == "combined" and row["first_stage_retriever"] == retriever and row["representation"] == representation and row["reranker"] == "qwen")
            sr = next(row for row in summaries if row["stage"] == "b2" and row["stratum"] == "combined" and row["first_stage_retriever"] == retriever and row["representation"] == representation and row["reranker"] == "skillrouter")
            lines.append(f"| {retriever} | {representation} | {b1_row['hit_at_1']:.3f} | {b1_row['mrr_at_20']:.3f} | {b1_row['recall_at_20']:.3f} | {qwen['hit_at_1']:.3f} | {sr['hit_at_1']:.3f} |")
    lines += [
        "",
        "## Primary Stratified H@1: I2 And I3C",
        "",
        "This table keeps the controlled and public-gold strata separate. It is descriptive stratification; the predeclared grouped paired inference remains combined because the primary contrast family is defined over the frozen full benchmark.",
        "",
        "| First stage | Representation | B1 controlled | B1 public-gold | Qwen B2 controlled | Qwen B2 public-gold | SkillRouter B2 controlled | SkillRouter B2 public-gold |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for retriever in RETRIEVERS:
        for representation in ("i2-original", "i3c-fielded-evidence"):
            def summary(stage: str, stratum: str, reranker: str | None = None) -> dict[str, Any]:
                return next(
                    row
                    for row in summaries
                    if row["stage"] == stage
                    and row["stratum"] == stratum
                    and row["first_stage_retriever"] == retriever
                    and row["representation"] == representation
                    and row["reranker"] == reranker
                )
            b1_controlled = summary("b1", "controlled")
            b1_public = summary("b1", "public_gold")
            qwen_controlled = summary("b2", "controlled", "qwen")
            qwen_public = summary("b2", "public_gold", "qwen")
            sr_controlled = summary("b2", "controlled", "skillrouter")
            sr_public = summary("b2", "public_gold", "skillrouter")
            lines.append(
                f"| {retriever} | {representation} | {b1_controlled['hit_at_1']:.3f} | {b1_public['hit_at_1']:.3f} | {qwen_controlled['hit_at_1']:.3f} | {qwen_public['hit_at_1']:.3f} | {sr_controlled['hit_at_1']:.3f} | {sr_public['hit_at_1']:.3f} |"
            )
    lines += ["", "## Primary Paired Representation Contrast: I3C - I2", ""]
    primary = report["representation_contrasts"]["i3c_minus_i2"]["combined_only"]
    for metric, records in primary.items():
        lines += [f"### {metric}", "", "| Endpoint | Delta | 95% CI | Holm-adjusted p |", "|---|---:|---|---:|"]
        for record in records:
            low, high = record["ci_95"]
            lines.append(f"| {record['label']} | {record['estimate']:+.3f} | [{low:+.3f}, {high:+.3f}] | {record['holm']['holm_adjusted_p_value']:.5f} |")
        lines.append("")
    lines += ["## Failure Decomposition", "", "Candidate miss means B1 omitted the gold from Top-20, so B2 could not recover it. Ordering error is conditional on gold already being present.", ""]
    lines += ["| Reranker | First stage | Representation | Candidate miss | Ordering error | Correction | Regression |", "|---|---|---|---:|---:|---:|---:|"]
    for row in report["failure_analysis"]:
        if row["stratum"] != "combined":
            continue
        counts = row["counts"]
        lines.append(f"| {row['reranker']} | {row['first_stage_retriever']} | {row['representation']} | {counts.get('candidate_miss', 0)} | {counts.get('ordering_error', 0)} | {counts.get('reranker_correction', 0)} | {counts.get('reranker_regression', 0)} |")
    lines += [
        "",
        "## Cost Boundary",
        "",
        "- Cost values are measured execution work. No USD estimate is made without a separately dated, sourced provider price.",
        f"- I3C construction footprint: {report['cost']['i3c_construction_input_footprint']['source_rows']} source rows, {report['cost']['i3c_construction_input_footprint']['source_chunks']} chunks, and {report['cost']['i3c_construction_input_footprint']['input_proxy_tokens']} proxy tokens. No directly comparable V3 extraction wall-time is claimed.",
        f"- Qwen B2: {report['cost']['qwen_reranker_physical_execution']['successful_calls']} successful calls and {report['cost']['qwen_reranker_physical_execution']['provider_total_tokens']} provider tokens.",
        f"- SkillRouter B2: {report['cost']['skillrouter_reranker_physical_execution']['hosted_job_elapsed_seconds']:.2f} hosted wall seconds and {report['cost']['skillrouter_reranker_physical_execution']['amortised_model_forward_seconds']:.2f} summed/amortised model-forward seconds across fixed pairs.",
        "- The JSON report contains B1 document-index amortisation schedules for 1 through 100,000 queries. Recorded selector-visible tokens are candidate-representation corpus volume, not downstream agent-context usage.",
        "",
        "| Retriever | Representation | One-time document/index seconds | Mean query seconds | Candidate-representation corpus tokens |",
        "|---|---|---:|---:|---:|",
    ]
    for row in report["cost"]["b1_per_condition"]:
        if row["representation"] not in {"i2-original", "i3c-fielded-evidence"}:
            continue
        lines.append(
            f"| {row['retriever']} | {row['representation']} | {row['one_time_document_embedding_or_index_seconds']:.3f} | {row['query_seconds_mean']:.6f} | {row['selector_visible_tokens']} |"
        )
    lines += [
        "",
        "## Claim Boundary",
        "",
        "B3 verifies deterministic row/provenance integrity and analyses strict-gold outcomes. It does not replace the waived independent manual semantic-completeness review, and it does not justify a universal claim beyond these two strata and this frozen library.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    args = parser.parse_args()
    output_root = args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    b1 = {name: read_jsonl(path) for name, path in B1_PATHS.items()}
    b2 = {name: read_jsonl(path) for name, path in B2_PATHS.items()}
    validation = verify_inputs(b1, b2)
    report = {
        "schema_version": "rq2bv1-v3-b3-local-analysis-v1",
        "state": "completed_local_analysis_pending_user_review_not_thesis_text",
        "contract": "skill_benchmark/rq2bv1/results/b3_v3/B3_ANALYSIS_CONTRACT.md",
        "inputs": {
            "b1": {name: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for name, path in B1_PATHS.items()},
            "b2": {name: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for name, path in B2_PATHS.items()},
        },
        "input_validation": validation,
        "condition_summaries": condition_summaries(b1, b2),
        "representation_contrasts": representation_contrasts(b1, b2),
        "reranker_contrasts": reranker_contrasts(b1, b2),
        "failure_analysis": failure_analysis(b1, b2),
        "cost": cost_summary(b1, b2),
    }
    json_path = output_root / "b3_local_analysis.json"
    md_path = output_root / "B3_LOCAL_ANALYSIS.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "state": report["state"]}, indent=2))


if __name__ == "__main__":
    main()
