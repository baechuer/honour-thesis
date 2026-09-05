#!/usr/bin/env python3
"""Apply the frozen RQ2b estimands and inference to complete B1/B2 rows."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from statistics import median
from typing import Any

from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    version_root,
    write_json_new,
)
from rq2b_statistics import (
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    NONINFERIORITY_MARGIN,
    SIGN_FLIP_DRAWS,
    SIGN_FLIP_SEED,
    STATISTICS_VERSION,
    grouped_percentile_bootstrap,
    grouped_sign_flip,
    holm_adjust,
)
ANALYSIS_VERSION = "rq2b-primary-analysis-v2-skillrouter-embedding-secondary"
STRATA = ("controlled", "public_gold")
REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
)
FIRST_STAGE_RETRIEVERS = ("bm25", "qwen-max-chunk", "skillrouter-embedding")


def verify_denominator_identity(rows: list[dict[str, Any]]) -> None:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row["first_stage_retriever"], row["representation"], row["stratum"])
        groups[key].append(row)
    require(bool(groups), "B2 denominator-identity input is empty")
    for key, group_rows in groups.items():
        total = len(group_rows)
        for label in ("strict", "acceptable"):
            candidates_positive = sum(int(row[f"{label}_candidate_positive"]) for row in group_rows)
            reranked_positive = sum(int(row[f"end_to_end_{label}_top1"]) for row in group_rows)
            recall = candidates_positive / total
            conditional = reranked_positive / candidates_positive if candidates_positive else 0.0
            end_to_end = reranked_positive / total
            require(abs(end_to_end - recall * conditional) <= 1e-12, f"B2 {label} denominator identity failed: {key}")


def load_run_rows(root: Path, run_root: Path, *, stage: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require(stage in {"B1", "B2"}, "Unknown RQ2b analysis stage")
    allowed = (
        {
            "rq2b-bm25-run-manifest-v1": "complete_scientific_b1_local",
            "rq2b-qwen-run-manifest-v1": "complete_scientific_b1_external",
            "rq2b-skillrouter-embedding-run-manifest-v1": "complete_scientific_b1_skillrouter_embedding",
        }
        if stage == "B1"
        else {"rq2b-skillrouter-run-manifest-v1": "complete_scientific_b2"}
    )
    rows: list[dict[str, Any]] = []
    manifests: list[dict[str, Any]] = []
    for manifest_path in sorted(run_root.glob("*/manifest.json")):
        manifest = read_json(manifest_path)
        schema = manifest.get("schema_version")
        require(schema in allowed, f"Unexpected {stage} run manifest schema: {manifest_path}")
        require(manifest.get("state") == allowed[schema], f"Incomplete {stage} run: {manifest_path}")
        require(manifest.get("version_id") == VERSION_ID, f"Wrong {stage} run version: {manifest_path}")
        artifact = manifest.get("artifacts", {}).get("rows")
        require(artifact is not None, f"{stage} run has no row artifact: {manifest_path}")
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], f"Analysis input rows drift: {path}")
        source_rows = read_jsonl(path)
        require(len(source_rows) == artifact["rows"], f"{stage} row count drift: {path}")
        rows.extend(source_rows)
        manifests.append(
            {
                "path": relative(manifest_path, root),
                "sha256": sha256_file(manifest_path),
                "rows_path": relative(path, root),
                "rows_sha256": sha256_file(path),
                "rows": len(source_rows),
            }
        )
    require(bool(manifests), f"No run manifests found under {run_root}")
    return rows, manifests


def validate_complete_matrix(
    b1_rows: list[dict[str, Any]],
    b2_rows: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
) -> None:
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    require(len(prompt_by_id) == len(prompts) == 401, "RQ2b prompt matrix must contain 401 unique prompts")

    b1_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in b1_rows:
        key = (row["retriever"], row["representation"], row["prompt_id"])
        require(key not in b1_by_key, f"Duplicate B1 matrix row: {key}")
        require(row["prompt_id"] in prompt_by_id, f"Unknown B1 prompt: {row['prompt_id']}")
        prompt = prompt_by_id[row["prompt_id"]]
        require(row["prompt_sha256"] == prompt["prompt_sha256"], f"B1 prompt hash mismatch: {key}")
        require(row["stratum"] == prompt["stratum"] and row["group"] == prompt["group"], f"B1 prompt metadata mismatch: {key}")
        require(row["gold_skill"] == prompt["gold_skill"], f"B1 strict gold mismatch: {key}")
        require(set(row["valid_skills"]) == set(prompt["valid_skills"]), f"B1 acceptable set mismatch: {key}")
        require(len(row["top_20_skill_ids"]) == len(set(row["top_20_skill_ids"])) == 20, f"B1 top-20 mismatch: {key}")
        b1_by_key[key] = row
    expected_primary = {
        (retriever, representation, prompt_id)
        for retriever in FIRST_STAGE_RETRIEVERS
        for representation in REPRESENTATIONS
        for prompt_id in prompt_by_id
    }
    expected_mean = {
        ("qwen-mean-chunk-sensitivity", representation, prompt_id)
        for representation in REPRESENTATIONS
        for prompt_id in prompt_by_id
    }
    require(set(b1_by_key) == expected_primary | expected_mean, "B1 full condition matrix is incomplete or contains extras")

    b2_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in b2_rows:
        key = (row["first_stage_retriever"], row["representation"], row["prompt_id"])
        require(key not in b2_by_key, f"Duplicate B2 matrix row: {key}")
        require(key in expected_primary, f"Unexpected B2 condition: {key}")
        prompt = prompt_by_id[row["prompt_id"]]
        require(row["stratum"] == prompt["stratum"] and row["group"] == prompt["group"], f"B2 prompt metadata mismatch: {key}")
        require(row["gold_skill"] == prompt["gold_skill"], f"B2 strict gold mismatch: {key}")
        require(set(row["valid_skills"]) == set(prompt["valid_skills"]), f"B2 acceptable set mismatch: {key}")
        require(row["candidate_skill_ids"] == b1_by_key[key]["top_20_skill_ids"], f"B2 candidate list differs from B1: {key}")
        require(len(row["reranked_skill_ids"]) == len(set(row["reranked_skill_ids"])) == 20, f"B2 reranked list mismatch: {key}")
        require(set(row["reranked_skill_ids"]) == set(row["candidate_skill_ids"]), f"B2 reranked candidate identity drift: {key}")
        b2_by_key[key] = row
    require(set(b2_by_key) == expected_primary, "B2 full condition matrix is incomplete or contains extras")


def index_b1(rows: list[dict[str, Any]]) -> dict[tuple[str, str, str], dict[str, Any]]:
    indexed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        retriever = row["retriever"]
        if retriever == "qwen-mean-chunk-sensitivity":
            continue
        key = (retriever, row["representation"], row["prompt_id"])
        require(key not in indexed, f"Duplicate B1 analysis row: {key}")
        indexed[key] = row
    return indexed


def paired_rows(
    left: dict[tuple[str, str, str], dict[str, Any]],
    *,
    retriever: str,
    representation_a: str,
    representation_b: str,
    stratum: str,
    endpoint: str,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    keys_a = {
        prompt_id
        for row_retriever, representation, prompt_id in left
        if row_retriever == retriever
        and representation == representation_a
        and left[(row_retriever, representation, prompt_id)]["stratum"] == stratum
    }
    keys_b = {
        prompt_id
        for row_retriever, representation, prompt_id in left
        if row_retriever == retriever
        and representation == representation_b
        and left[(row_retriever, representation, prompt_id)]["stratum"] == stratum
    }
    require(keys_a == keys_b and bool(keys_a), f"Paired B1 population mismatch: {representation_a}/{representation_b}/{stratum}")
    for prompt_id in sorted(keys_a):
        row_a = left[(retriever, representation_a, prompt_id)]
        row_b = left[(retriever, representation_b, prompt_id)]
        require(row_a["group"] == row_b["group"], f"Paired group mismatch: {prompt_id}")
        result.append(
            {
                "prompt_id": prompt_id,
                "group": row_a["group"],
                "difference": float(row_a[endpoint]) - float(row_b[endpoint]),
            }
        )
    return result


def p4_rows(b2_rows: list[dict[str, Any]], stratum: str) -> list[dict[str, Any]]:
    selected = [
        row
        for row in b2_rows
        if row["first_stage_retriever"] == "qwen-max-chunk"
        and row["representation"] == "i3c-fielded-evidence"
        and row["stratum"] == stratum
        and row["candidate_positive"] == 1
    ]
    require(bool(selected), f"P4 has no candidate-positive prompts in {stratum}")
    return [
        {
            "prompt_id": row["prompt_id"],
            "group": row["group"],
            "difference": float(row["reranked_acceptable_top1"])
            - float(row["first_stage_acceptable_top1"]),
        }
        for row in selected
    ]


def b1_score_margin(row: dict[str, Any]) -> float:
    top_rows = row["top_100"]
    require(len(top_rows) >= 2, "B1 row lacks two ranked candidates for a score margin")
    margin = float(top_rows[0]["score"]) - float(top_rows[1]["score"])
    require(margin >= -1e-12, "B1 score margin is negative despite sorted ranks")
    return max(0.0, margin)


def acceptable_set_coverage_at_20(row: dict[str, Any]) -> float:
    valid = set(row["valid_skills"])
    require(bool(valid), "B1 acceptable set is empty")
    return len(valid.intersection(row["top_20_skill_ids"])) / len(valid)


def descriptive_matrix(b1_rows: list[dict[str, Any]], b2_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = (
        "strict_hit_at_1",
        "acceptable_hit_at_1",
        "strict_recall_at_5",
        "acceptable_recall_at_5",
        "strict_recall_at_20",
        "acceptable_recall_at_20",
        "strict_recall_at_50",
        "acceptable_recall_at_50",
        "strict_recall_at_100",
        "acceptable_recall_at_100",
        "strict_reciprocal_rank",
        "acceptable_reciprocal_rank",
    )
    grouped_b1: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in b1_rows:
        if row["stratum"] not in STRATA:
            continue
        grouped_b1[(row["retriever"], row["representation"], row["stratum"])].append(row)
    output: list[dict[str, Any]] = []
    for (retriever, representation, stratum), rows in sorted(grouped_b1.items()):
        strict_ranks = [float(row["strict_gold_rank"]) for row in rows]
        acceptable_ranks = [float(row["acceptable_gold_rank"]) for row in rows]
        score_margins = [b1_score_margin(row) for row in rows]
        miss_classes = [
            row["top_100"][0]["destination_class"]
            for row in rows
            if not int(row["acceptable_hit_at_1"])
        ]
        output.append(
            {
                "stage": "B1",
                "retriever": retriever,
                "representation": representation,
                "stratum": stratum,
                "prompts": len(rows),
                **{
                    metric: sum(float(row[metric]) for row in rows) / len(rows)
                    for metric in metrics
                },
                "mean_strict_gold_rank": sum(strict_ranks) / len(rows),
                "median_strict_gold_rank": median(strict_ranks),
                "mean_acceptable_gold_rank": sum(acceptable_ranks) / len(rows),
                "median_acceptable_gold_rank": median(acceptable_ranks),
                "candidate_full_coverage_at_20": sum(
                    acceptable_set_coverage_at_20(row) == 1.0
                    for row in rows
                ) / len(rows),
                "mean_acceptable_set_coverage_at_20": sum(
                    acceptable_set_coverage_at_20(row) for row in rows
                ) / len(rows),
                "annotated_near_neighbour_top1_miss_rate": miss_classes.count("annotated_near_neighbour") / len(rows),
                "background_unrelated_top1_miss_rate": miss_classes.count("background_unrelated") / len(rows),
                "unresolved_public_equivalent_top1_miss_rate": miss_classes.count("unresolved_public_equivalent") / len(rows),
                "mean_score_margin": sum(score_margins) / len(rows),
                "median_score_margin": median(score_margins),
            }
        )
    grouped_b2: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in b2_rows:
        if row["stratum"] not in STRATA:
            continue
        grouped_b2[(row["first_stage_retriever"], row["representation"], row["stratum"])].append(row)
    for (retriever, representation, stratum), rows in sorted(grouped_b2.items()):
        strict_candidate_positive = sum(row["strict_candidate_positive"] for row in rows)
        acceptable_candidate_positive = sum(row["acceptable_candidate_positive"] for row in rows)
        strict_end_to_end = sum(row["end_to_end_strict_top1"] for row in rows)
        acceptable_end_to_end = sum(row["end_to_end_acceptable_top1"] for row in rows)
        output.append(
            {
                "stage": "B2",
                "retriever": retriever,
                "representation": representation,
                "stratum": stratum,
                "prompts": len(rows),
                "strict_recall_at_20": strict_candidate_positive / len(rows),
                "acceptable_recall_at_20": acceptable_candidate_positive / len(rows),
                "conditional_strict_hit_at_1": strict_end_to_end / strict_candidate_positive if strict_candidate_positive else 0.0,
                "conditional_acceptable_hit_at_1": acceptable_end_to_end / acceptable_candidate_positive if acceptable_candidate_positive else 0.0,
                "end_to_end_strict_hit_at_1": strict_end_to_end / len(rows),
                "end_to_end_acceptable_hit_at_1": acceptable_end_to_end / len(rows),
                "end_to_end_strict_mrr": sum(row["end_to_end_strict_reciprocal_rank"] for row in rows) / len(rows),
                "end_to_end_acceptable_mrr": sum(row["end_to_end_acceptable_reciprocal_rank"] for row in rows) / len(rows),
                "reranker_gain_rate": sum(row["reranker_gain"] for row in rows) / len(rows),
                "reranker_regression_rate": sum(row["reranker_regression"] for row in rows) / len(rows),
                "unrecoverable_exclusion_rate": sum(row["unrecoverable_exclusion"] for row in rows) / len(rows),
                "mean_window_strict_hit_at_1": sum(row["mean_window_sensitivity_metrics"]["strict_top1"] for row in rows) / len(rows),
                "mean_window_acceptable_hit_at_1": sum(row["mean_window_sensitivity_metrics"]["acceptable_top1"] for row in rows) / len(rows),
                "mean_window_strict_mrr_at_20": sum(row["mean_window_sensitivity_metrics"]["strict_reciprocal_rank"] for row in rows) / len(rows),
                "mean_window_acceptable_mrr_at_20": sum(row["mean_window_sensitivity_metrics"]["acceptable_reciprocal_rank"] for row in rows) / len(rows),
                "k5_strict_hit_at_1": sum(row["k5_sensitivity_metrics"]["strict_top1"] for row in rows) / len(rows),
                "k5_acceptable_hit_at_1": sum(row["k5_sensitivity_metrics"]["acceptable_top1"] for row in rows) / len(rows),
            }
        )
    return output


def top_20_jaccard(left: dict[str, Any], right: dict[str, Any]) -> float:
    left_ids = set(left["top_20_skill_ids"])
    right_ids = set(right["top_20_skill_ids"])
    require(len(left_ids) == len(right_ids) == 20, "Stress ranking has an invalid top-20")
    return len(left_ids.intersection(right_ids)) / len(left_ids.union(right_ids))


def stress_descriptive(b1_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected_retrievers = {
        "bm25",
        "qwen-max-chunk",
        "qwen-mean-chunk-sensitivity",
        "skillrouter-embedding",
    }
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in b1_rows:
        if row["stratum"] == "stress":
            grouped[(row["prompt_id"], row["representation"])].append(row)
    require(
        len({prompt_id for prompt_id, _ in grouped}) == 12,
        "Stress analysis requires exactly 12 prompts",
    )
    output: list[dict[str, Any]] = []
    for (prompt_id, representation), rows in sorted(grouped.items()):
        by_retriever = {row["retriever"]: row for row in rows}
        require(
            set(by_retriever) == expected_retrievers and len(rows) == len(by_retriever),
            f"Stress condition coverage mismatch: {prompt_id}/{representation}",
        )
        valid_sets = {tuple(sorted(row["valid_skills"])) for row in rows}
        require(len(valid_sets) == 1, f"Stress acceptable-set drift: {prompt_id}/{representation}")
        pairwise = []
        for left_name, right_name in combinations(sorted(expected_retrievers), 2):
            left = by_retriever[left_name]
            right = by_retriever[right_name]
            pairwise.append(
                {
                    "left_retriever": left_name,
                    "right_retriever": right_name,
                    "top1_agreement": left["top_20_skill_ids"][0] == right["top_20_skill_ids"][0],
                    "top20_jaccard": top_20_jaccard(left, right),
                }
            )
        output.append(
            {
                "prompt_id": prompt_id,
                "representation": representation,
                "conditions": {
                    retriever: {
                        "top_ranked_skill": row["top_20_skill_ids"][0],
                        "acceptable_set_coverage_at_20": acceptable_set_coverage_at_20(row),
                        "score_margin": b1_score_margin(row),
                    }
                    for retriever, row in sorted(by_retriever.items())
                },
                "ranking_stability": {
                    "all_retrievers_top1_agree": len(
                        {row["top_20_skill_ids"][0] for row in rows}
                    ) == 1,
                    "mean_pairwise_top20_jaccard": sum(
                        row["top20_jaccard"] for row in pairwise
                    ) / len(pairwise),
                    "pairwise": pairwise,
                },
            }
        )
    return output


def qwen_length_bias_sensitivity(b1_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    selected = [
        row
        for row in b1_rows
        if row["retriever"] in {"qwen-max-chunk", "qwen-mean-chunk-sensitivity"}
        and row["representation"] in {"i2-original", "i3c-fielded-evidence"}
        and row["stratum"] in STRATA
    ]
    require(bool(selected), "Qwen length-bias sensitivity population is empty")
    axes = {
        "by_gold_chunk_class": "strict_gold_document_chunk_class",
        "by_gold_source_length_quartile": "strict_gold_source_length_quartile",
    }
    output: dict[str, list[dict[str, Any]]] = {}
    for output_name, field in axes.items():
        grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in selected:
            require(field in row, f"Qwen sensitivity metadata missing: {field}")
            grouped[(row["retriever"], row["representation"], row["stratum"], row[field])].append(row)
        output[output_name] = [
            {
                "retriever": retriever,
                "representation": representation,
                "stratum": stratum,
                field: bucket,
                "prompts": len(rows),
                **{
                    metric: sum(float(row[metric]) for row in rows) / len(rows)
                    for metric in (
                        "strict_hit_at_1",
                        "acceptable_hit_at_1",
                        "strict_recall_at_20",
                        "acceptable_recall_at_20",
                        "strict_reciprocal_rank",
                        "acceptable_reciprocal_rank",
                    )
                },
            }
            for (retriever, representation, stratum, bucket), rows in sorted(grouped.items())
        ]
    return output


def skillrouter_embedding_replication(
    b1_rows: list[dict[str, Any]],
    *,
    bootstrap_resamples: int = BOOTSTRAP_RESAMPLES,
) -> dict[str, Any]:
    """Report preregistered secondary representation contrasts for the native encoder."""
    indexed = index_b1(b1_rows)
    contrasts = (
        ("i3c_minus_i2", "i2-original"),
        ("i3c_minus_i1", "i1-discovery"),
        ("i3c_fielded_minus_i3_flat", "i3-flat-evidence"),
    )
    rows: list[dict[str, Any]] = []
    for stratum in STRATA:
        for name, comparison in contrasts:
            paired = paired_rows(
                indexed,
                retriever="skillrouter-embedding",
                representation_a="i3c-fielded-evidence",
                representation_b=comparison,
                stratum=stratum,
                endpoint="acceptable_recall_at_20",
            )
            rows.append(
                {
                    "contrast": name,
                    "stratum": stratum,
                    "endpoint": "acceptable_recall_at_20",
                    "decision_status": "secondary_descriptive_not_in_primary_holm_family",
                    "bootstrap": grouped_percentile_bootstrap(
                        paired,
                        resamples=bootstrap_resamples,
                        seed=BOOTSTRAP_SEED,
                    ),
                }
            )
    selected = [
        row
        for row in b1_rows
        if row["retriever"] == "skillrouter-embedding"
        and row["representation"] in {"i2-original", "i3c-fielded-evidence"}
        and row["stratum"] in STRATA
    ]
    require(bool(selected), "SkillRouter embedding length sensitivity population is empty")
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        require("strict_gold_source_length_quartile" in row, "SkillRouter embedding length metadata missing")
        grouped[(row["representation"], row["stratum"], row["strict_gold_source_length_quartile"])].append(row)
    length_rows = [
        {
            "representation": representation,
            "stratum": stratum,
            "strict_gold_source_length_quartile": quartile,
            "prompts": len(values),
            "acceptable_recall_at_20": sum(float(row["acceptable_recall_at_20"]) for row in values) / len(values),
            "acceptable_hit_at_1": sum(float(row["acceptable_hit_at_1"]) for row in values) / len(values),
            "acceptable_mrr": sum(float(row["acceptable_reciprocal_rank"]) for row in values) / len(values),
        }
        for (representation, stratum, quartile), values in sorted(grouped.items())
    ]
    return {
        "status": "required_secondary_replication",
        "primary_hypotheses_unchanged": True,
        "paired_representation_contrasts": rows,
        "source_length_quartiles": length_rows,
    }


def summarize_b2_sensitivity_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
    strict_candidate = sum(int(row["strict_candidate_positive"]) for row in rows)
    acceptable_candidate = sum(int(row["acceptable_candidate_positive"]) for row in rows)
    strict_end = sum(int(row["end_to_end_strict_top1"]) for row in rows)
    acceptable_end = sum(int(row["end_to_end_acceptable_top1"]) for row in rows)
    return {
        "prompts": len(rows),
        "strict_recall_at_20": strict_candidate / len(rows),
        "acceptable_recall_at_20": acceptable_candidate / len(rows),
        "conditional_strict_hit_at_1": strict_end / strict_candidate if strict_candidate else 0.0,
        "conditional_acceptable_hit_at_1": acceptable_end / acceptable_candidate if acceptable_candidate else 0.0,
        "end_to_end_strict_hit_at_1": strict_end / len(rows),
        "end_to_end_acceptable_hit_at_1": acceptable_end / len(rows),
        "end_to_end_strict_mrr_at_20": sum(float(row["end_to_end_strict_reciprocal_rank"]) for row in rows) / len(rows),
        "end_to_end_acceptable_mrr_at_20": sum(float(row["end_to_end_acceptable_reciprocal_rank"]) for row in rows) / len(rows),
        "mean_window_strict_hit_at_1": sum(row["mean_window_sensitivity_metrics"]["strict_top1"] for row in rows) / len(rows),
        "mean_window_acceptable_hit_at_1": sum(row["mean_window_sensitivity_metrics"]["acceptable_top1"] for row in rows) / len(rows),
        "k5_strict_hit_at_1": sum(row["k5_sensitivity_metrics"]["strict_top1"] for row in rows) / len(rows),
        "k5_acceptable_hit_at_1": sum(row["k5_sensitivity_metrics"]["acceptable_top1"] for row in rows) / len(rows),
    }


def skillrouter_length_bias_sensitivity(b2_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    selected = [
        row
        for row in b2_rows
        if row["representation"] in {"i2-original", "i3c-fielded-evidence"}
        and row["stratum"] in STRATA
    ]
    require(bool(selected), "SkillRouter length-bias sensitivity population is empty")
    axes = {
        "by_gold_window_class": "strict_gold_document_window_class",
        "by_gold_source_length_quartile": "strict_gold_source_length_quartile",
    }
    output: dict[str, list[dict[str, Any]]] = {}
    for output_name, field in axes.items():
        grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in selected:
            require(field in row, f"SkillRouter sensitivity metadata missing: {field}")
            grouped[(row["first_stage_retriever"], row["representation"], row["stratum"], row[field])].append(row)
        output[output_name] = [
            {
                "first_stage_retriever": retriever,
                "representation": representation,
                "stratum": stratum,
                field: bucket,
                **summarize_b2_sensitivity_group(rows),
            }
            for (retriever, representation, stratum, bucket), rows in sorted(grouped.items())
        ]
    return output


def primary_analysis(
    b1_rows: list[dict[str, Any]],
    b2_rows: list[dict[str, Any]],
    *,
    bootstrap_resamples: int = BOOTSTRAP_RESAMPLES,
    sign_flip_draws: int = SIGN_FLIP_DRAWS,
) -> dict[str, Any]:
    verify_denominator_identity(b2_rows)
    b1 = index_b1(b1_rows)
    hypotheses: dict[str, dict[str, Any]] = {}
    p_values: dict[str, float] = {}
    for suffix, stratum in (("C", "controlled"), ("P", "public_gold")):
        p1_id = f"P1-{suffix}"
        p1_data = paired_rows(
            b1,
            retriever="qwen-max-chunk",
            representation_a="i3c-fielded-evidence",
            representation_b="i2-original",
            stratum=stratum,
            endpoint="acceptable_recall_at_20",
        )
        p1_bootstrap = grouped_percentile_bootstrap(
            p1_data,
            resamples=bootstrap_resamples,
            seed=BOOTSTRAP_SEED,
        )
        hypotheses[p1_id] = {
            "decision_form": "noninferiority",
            "contrast": "qwen_i3c_minus_i2_acceptable_recall_at_20",
            "stratum": stratum,
            "bootstrap": p1_bootstrap,
            "margin": NONINFERIORITY_MARGIN,
            "stratum_noninferior": p1_bootstrap["one_sided_95_lower"] > NONINFERIORITY_MARGIN,
        }

        for number, representation_b, decision, tail in (
            (2, "i1-discovery", "superiority", "positive_one_sided"),
            (3, "i3-flat-evidence", "two_sided_organization_effect", "absolute_two_sided"),
        ):
            hypothesis_id = f"P{number}-{suffix}"
            data = paired_rows(
                b1,
                retriever="qwen-max-chunk",
                representation_a="i3c-fielded-evidence",
                representation_b=representation_b,
                stratum=stratum,
                endpoint="acceptable_recall_at_20",
            )
            bootstrap = grouped_percentile_bootstrap(
                data,
                resamples=bootstrap_resamples,
                seed=BOOTSTRAP_SEED,
            )
            sign_flip = grouped_sign_flip(
                data,
                tail=tail,
                draws=sign_flip_draws,
                seed=SIGN_FLIP_SEED,
            )
            hypotheses[hypothesis_id] = {
                "decision_form": decision,
                "contrast": f"qwen_i3c_minus_{representation_b}_acceptable_recall_at_20",
                "stratum": stratum,
                "bootstrap": bootstrap,
                "sign_flip": sign_flip,
            }
            p_values[hypothesis_id] = sign_flip["p_value"]

        p4_id = f"P4-{suffix}"
        data = p4_rows(b2_rows, stratum)
        bootstrap = grouped_percentile_bootstrap(
            data,
            resamples=bootstrap_resamples,
            seed=BOOTSTRAP_SEED,
        )
        sign_flip = grouped_sign_flip(
            data,
            tail="positive_one_sided",
            draws=sign_flip_draws,
            seed=SIGN_FLIP_SEED,
        )
        hypotheses[p4_id] = {
            "decision_form": "conditional_superiority",
            "contrast": "skillrouter_minus_qwen_first_stage_conditional_acceptable_hit_at_1",
            "stratum": stratum,
            "bootstrap": bootstrap,
            "sign_flip": sign_flip,
        }
        p_values[p4_id] = sign_flip["p_value"]

    holm = holm_adjust(p_values)
    for hypothesis_id, correction in holm.items():
        hypotheses[hypothesis_id]["multiplicity"] = correction
    p1_intersection = all(
        hypotheses[hypothesis_id]["stratum_noninferior"]
        for hypothesis_id in ("P1-C", "P1-P")
    )
    return {
        "statistics_version": STATISTICS_VERSION,
        "analysis_version": ANALYSIS_VERSION,
        "hypotheses": hypotheses,
        "p1_intersection_noninferiority_supported": p1_intersection,
        "holm_family": sorted(p_values),
    }


def run(root: Path, b1_root: Path, b2_root: Path, output_dir: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    require(not output_dir.exists(), f"Refusing to overwrite RQ2b analysis: {output_dir}")
    b1_rows, b1_manifests = load_run_rows(root, b1_root, stage="B1")
    b2_rows, b2_manifests = load_run_rows(root, b2_root, stage="B2")
    require(len(b1_rows) > 0 and len(b2_rows) > 0, "RQ2b analysis input matrix is empty")
    prompt_manifest_path = version_root(root) / "prompt_manifest.jsonl"
    prompts = read_jsonl(prompt_manifest_path)
    validate_complete_matrix(b1_rows, b2_rows, prompts)
    primary = primary_analysis(b1_rows, b2_rows)
    matrix = descriptive_matrix(b1_rows, b2_rows)
    stress = stress_descriptive(b1_rows)
    sensitivity = {
        "qwen": qwen_length_bias_sensitivity(b1_rows),
        "skillrouter_embedding": skillrouter_embedding_replication(b1_rows),
        "skillrouter": skillrouter_length_bias_sensitivity(b2_rows),
    }
    output_dir.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": "rq2b-analysis-report-v1",
        "version_id": VERSION_ID,
        "state": "complete_pending_user_review_not_for_thesis",
        "analysis_version": ANALYSIS_VERSION,
        "network_calls": 0,
        "inputs": {
            "b1_manifests": b1_manifests,
            "b2_manifests": b2_manifests,
            "prompt_manifest": {
                "path": relative(prompt_manifest_path, root),
                "sha256": sha256_file(prompt_manifest_path),
                "rows": len(prompts),
            },
        },
        "settings": {
            "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "sign_flip_draws": SIGN_FLIP_DRAWS,
            "sign_flip_seed": SIGN_FLIP_SEED,
            "noninferiority_margin": NONINFERIORITY_MARGIN,
            "holm_family_size": 6,
        },
        "descriptive_matrix": matrix,
        "stress_descriptive": stress,
        "descriptive_length_bias_sensitivity": sensitivity,
        "primary_analysis": primary,
        "thesis_write_authorized": False,
    }
    write_json_new(output_dir / "analysis.json", report)
    return report


def self_test() -> dict[str, Any]:
    prompts = [
        ("p1", "controlled", "g1"),
        ("p2", "controlled", "g2"),
        ("p3", "public_gold", "g3"),
        ("p4", "public_gold", "g4"),
    ]
    b1_rows: list[dict[str, Any]] = []
    for prompt_id, stratum, group in prompts:
        for representation, value in (
            ("i1-discovery", 0),
            ("i2-original", 1),
            ("i3c-fielded-evidence", 1),
            ("i3-flat-evidence", 0),
        ):
            b1_rows.append(
                {
                    "retriever": "qwen-max-chunk",
                    "representation": representation,
                    "prompt_id": prompt_id,
                    "stratum": stratum,
                    "group": group,
                    "acceptable_recall_at_20": value,
                }
            )
    b2_rows = [
        {
            "first_stage_retriever": "qwen-max-chunk",
            "representation": "i3c-fielded-evidence",
            "prompt_id": prompt_id,
            "stratum": stratum,
            "group": group,
            "strict_candidate_positive": 1,
            "acceptable_candidate_positive": 1,
            "candidate_positive": 1,
            "first_stage_acceptable_top1": 0,
            "reranked_acceptable_top1": 1,
            "end_to_end_strict_top1": 1,
            "end_to_end_acceptable_top1": 1,
        }
        for prompt_id, stratum, group in prompts
    ]
    result = primary_analysis(
        b1_rows,
        b2_rows,
        bootstrap_resamples=100,
        sign_flip_draws=200,
    )
    require(result["p1_intersection_noninferiority_supported"] is True, "RQ2b P1 self-test failed")
    require(set(result["holm_family"]) == {"P2-C", "P2-P", "P3-C", "P3-P", "P4-C", "P4-P"}, "RQ2b Holm family self-test failed")

    matrix_prompts = [
        {
            "prompt_id": f"mp{index:03d}",
            "prompt_sha256": f"prompt-hash-{index}",
            "stratum": "controlled" if index < 245 else "public_gold" if index < 389 else "stress",
            "group": f"mg{index % 31}",
            "gold_skill": "s00",
            "valid_skills": ["s00"],
        }
        for index in range(401)
    ]
    candidates = [f"s{index:02d}" for index in range(20)]
    matrix_b1: list[dict[str, Any]] = []
    for prompt in matrix_prompts:
        for representation in REPRESENTATIONS:
            for retriever in (*FIRST_STAGE_RETRIEVERS, "qwen-mean-chunk-sensitivity"):
                if retriever == "qwen-mean-chunk-sensitivity" or retriever in FIRST_STAGE_RETRIEVERS:
                    matrix_b1.append(
                        {
                            "retriever": retriever,
                            "representation": representation,
                            "prompt_id": prompt["prompt_id"],
                            "prompt_sha256": prompt["prompt_sha256"],
                            "stratum": prompt["stratum"],
                            "group": prompt["group"],
                            "gold_skill": prompt["gold_skill"],
                            "valid_skills": prompt["valid_skills"],
                            "top_20_skill_ids": candidates,
                        }
                    )
    matrix_b2 = [
        {
            "first_stage_retriever": retriever,
            "representation": representation,
            "prompt_id": prompt["prompt_id"],
            "stratum": prompt["stratum"],
            "group": prompt["group"],
            "gold_skill": prompt["gold_skill"],
            "valid_skills": prompt["valid_skills"],
            "candidate_skill_ids": candidates,
            "reranked_skill_ids": candidates,
        }
        for prompt in matrix_prompts
        for representation in REPRESENTATIONS
        for retriever in FIRST_STAGE_RETRIEVERS
    ]
    validate_complete_matrix(matrix_b1, matrix_b2, matrix_prompts)
    partial_rejected = False
    try:
        validate_complete_matrix(matrix_b1[:-1], matrix_b2, matrix_prompts)
    except ValueError:
        partial_rejected = True
    require(partial_rejected, "RQ2b partial-matrix rejection self-test failed")

    def synthetic_b1_row(
        *,
        prompt_id: str,
        stratum: str,
        retriever: str,
        representation: str,
        top1: str = "s00",
    ) -> dict[str, Any]:
        top_ids = [top1] + [f"s{index:02d}" for index in range(20) if f"s{index:02d}" != top1]
        top_rows = [
            {
                "rank": index + 1,
                "skill_id": skill_id,
                "score": 1.0 - index * 0.01,
                "destination_class": "valid" if skill_id == "s00" else "background_unrelated",
            }
            for index, skill_id in enumerate(top_ids + [f"x{index:03d}" for index in range(80)])
        ]
        strict_rank = 1 if top1 == "s00" else 2
        return {
            "retriever": retriever,
            "representation": representation,
            "prompt_id": prompt_id,
            "stratum": stratum,
            "group": "synthetic",
            "gold_skill": "s00",
            "valid_skills": ["s00"],
            "strict_gold_rank": strict_rank,
            "acceptable_gold_rank": strict_rank,
            "strict_hit_at_1": int(strict_rank == 1),
            "acceptable_hit_at_1": int(strict_rank == 1),
            "strict_recall_at_5": 1,
            "acceptable_recall_at_5": 1,
            "strict_recall_at_20": 1,
            "acceptable_recall_at_20": 1,
            "strict_recall_at_50": 1,
            "acceptable_recall_at_50": 1,
            "strict_recall_at_100": 1,
            "acceptable_recall_at_100": 1,
            "strict_reciprocal_rank": 1.0 / strict_rank,
            "acceptable_reciprocal_rank": 1.0 / strict_rank,
            "top_20_skill_ids": top_ids,
            "top_100": top_rows,
        }

    secondary = descriptive_matrix(
        [
            synthetic_b1_row(
                prompt_id="secondary-1",
                stratum="controlled",
                retriever="bm25",
                representation="i1-discovery",
            )
        ],
        [],
    )
    require(
        secondary[0]["median_strict_gold_rank"] == 1
        and secondary[0]["strict_recall_at_100"] == 1
        and secondary[0]["candidate_full_coverage_at_20"] == 1
        and secondary[0]["mean_score_margin"] > 0,
        "RQ2b B1 secondary-metric self-test failed",
    )

    stress_rows = [
        synthetic_b1_row(
            prompt_id=f"stress-{prompt_index:02d}",
            stratum="stress",
            retriever=retriever,
            representation=representation,
        )
        for prompt_index in range(12)
        for representation in REPRESENTATIONS
        for retriever in (
            "bm25",
            "qwen-max-chunk",
            "qwen-mean-chunk-sensitivity",
            "skillrouter-embedding",
        )
    ]
    stress = stress_descriptive(stress_rows)
    require(
        len(stress) == 12 * len(REPRESENTATIONS)
        and all(row["ranking_stability"]["all_retrievers_top1_agree"] for row in stress),
        "RQ2b stress-descriptive self-test failed",
    )
    stress_excluded = descriptive_matrix(
        [
            synthetic_b1_row(
                prompt_id="ordinary-controlled",
                stratum="controlled",
                retriever="bm25",
                representation="i1-discovery",
            ),
            stress_rows[0],
        ],
        [{"stratum": "stress"}],
    )
    require(
        len(stress_excluded) == 1
        and stress_excluded[0]["stratum"] == "controlled"
        and all(
            set(condition)
            == {"top_ranked_skill", "acceptable_set_coverage_at_20", "score_margin"}
            for row in stress
            for condition in row["conditions"].values()
        ),
        "RQ2b stress prompts leaked into ordinary accuracy output",
    )
    return {
        "state": "synthetic_analysis_not_for_thesis",
        "network_calls": 0,
        "p1_intersection": result["p1_intersection_noninferiority_supported"],
        "holm_family": result["holm_family"],
        "complete_b1_rows": len(matrix_b1),
        "complete_b2_rows": len(matrix_b2),
        "partial_matrix_rejected": partial_rejected,
        "b1_secondary_metrics_complete": True,
        "stress_descriptive_rows": len(stress),
        "stress_excluded_from_accuracy_matrix": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--b1-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b1"))
    parser.add_argument("--b2-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b2"))
    parser.add_argument("--output-dir", type=Path, default=Path("skill_benchmark/outputs/rq2b/analysis/final"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        root = args.root.resolve()
        b1_root = args.b1_root if args.b1_root.is_absolute() else root / args.b1_root
        b2_root = args.b2_root if args.b2_root.is_absolute() else root / args.b2_root
        output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        result = run(root, b1_root, b2_root, output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
