#!/usr/bin/env python3
"""Strict-only RQ2b v1.1 execution schemas, matrix gates, and synthetic tests.

This module deliberately has no retrieval, model-loading, or provider client.
It defines the result contracts that later, separately authorised B1/B2 runners
must satisfy.  In particular, v1.1 is strict-gold-only: legacy acceptable-set
fields are rejected rather than ignored.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, repo_root, require, sha256_json, write_json_new
from rq2b_v11_contract import (
    EXPECTED_B1_RETRIEVERS,
    EXPECTED_RERANKERS,
    EXPECTED_REPRESENTATIONS,
    EXPECTED_SCORED_STRATA,
    RELATIVE_ROOT,
    VERSION_ID,
    verify as verify_v11_contract,
)


PRIMARY_K = 20
PERSISTED_K = 100
B1_SCHEMA = "rq2b-v11-b1-strict-result-row-v1"
B2_SCHEMA = "rq2b-v11-b2-strict-result-row-v1"
SMOKE_SCHEMA = "rq2b-v11-execution-contract-smoke-v1"
SCORING_STRATA = frozenset(EXPECTED_SCORED_STRATA)

B1_REQUIRED_KEYS = {
    "schema_version",
    "version_id",
    "runner_version",
    "retriever",
    "representation",
    "prompt_id",
    "prompt_sha256",
    "stratum",
    "group",
    "gold_skill",
    "strict_gold_rank",
    "strict_hit_at_1",
    "strict_recall_at_5",
    "strict_recall_at_20",
    "strict_recall_at_50",
    "strict_recall_at_100",
    "strict_mrr_at_10",
    "top_5_skill_ids",
    "top_20_skill_ids",
    "top_50_skill_ids",
    "top_100",
    "query_seconds",
}
B1_OPTIONAL_KEYS = {
    "aggregation",
    "selector_visible_tokens",
    "provider_input_tokens",
    "provider_cost",
    "one_time_document_embedding_or_index_seconds",
    "retriever_metadata",
}

B2_REQUIRED_KEYS = {
    "schema_version",
    "version_id",
    "runner_version",
    "reranker",
    "first_stage_retriever",
    "representation",
    "prompt_id",
    "prompt_sha256",
    "stratum",
    "group",
    "gold_skill",
    "candidate_skill_ids",
    "candidate_list_sha256",
    "reranked_skill_ids",
    "reranked_scores",
    "strict_candidate_positive",
    "first_stage_strict_top1",
    "reranked_strict_top1",
    "conditional_strict_top1_numerator",
    "conditional_strict_top1_denominator",
    "end_to_end_strict_top1",
    "end_to_end_strict_mrr_at_20",
    "strict_reranker_gain",
    "strict_reranker_regression",
    "rerank_seconds",
}
B2_OPTIONAL_KEYS = {
    "primary_window_aggregation",
    "mean_window_sensitivity_strict_hit_at_1",
    "mean_window_sensitivity_strict_mrr_at_20",
    "provider_input_tokens",
    "provider_cost",
    "reranker_metadata",
}


def fail_on_legacy_acceptable_fields(row: dict[str, Any], label: str) -> None:
    forbidden = sorted(
        key for key in row if "acceptable" in key.lower() or key == "valid_skills"
    )
    require(not forbidden, f"v1.1 strict-only row has legacy acceptable fields ({label}): {forbidden}")


def require_exact_keys(
    row: dict[str, Any], *, required: set[str], optional: set[str], label: str
) -> None:
    keys = set(row)
    missing = sorted(required - keys)
    unexpected = sorted(keys - required - optional)
    require(not missing, f"v1.1 row is missing required fields ({label}): {missing}")
    require(not unexpected, f"v1.1 row has unexpected fields ({label}): {unexpected}")


def binary(value: Any, label: str) -> int:
    require(value in (0, 1) and not isinstance(value, bool), f"{label} is not binary")
    return int(value)


def finite_number(value: Any, label: str) -> float:
    require(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value)),
        f"{label} is not a finite number",
    )
    return float(value)


def require_ranked_ids(value: Any, *, length: int, label: str) -> list[str]:
    require(isinstance(value, list) and len(value) == length, f"{label} length mismatch")
    require(
        all(isinstance(skill_id, str) and bool(skill_id) for skill_id in value)
        and len(value) == len(set(value)),
        f"{label} must contain unique non-empty skill IDs",
    )
    return list(value)


def load_scored_prompts(root: Path) -> tuple[dict[str, dict[str, Any]], set[str]]:
    verify_v11_contract(root)
    version_root = root / RELATIVE_ROOT
    prompt_rows = read_jsonl(version_root / "prompt_manifest.jsonl")
    prompt_by_id = {str(row["prompt_id"]): row for row in prompt_rows}
    require(len(prompt_by_id) == len(prompt_rows), "v1.1 prompt IDs are not unique")
    scored_ids = set(read_json(version_root / "scored_prompt_ids.json"))
    require(len(scored_ids) == 381, "v1.1 strict scoring population is not 381 prompts")
    require(scored_ids.issubset(prompt_by_id), "v1.1 scored IDs are not in the prompt manifest")
    selected = {prompt_id: prompt_by_id[prompt_id] for prompt_id in scored_ids}
    strata: dict[str, int] = defaultdict(int)
    for prompt in selected.values():
        require(prompt["stratum"] in SCORING_STRATA, "Stress prompt entered v1.1 accuracy population")
        strata[prompt["stratum"]] += 1
    require(dict(strata) == EXPECTED_SCORED_STRATA, "v1.1 strict scored-stratum mismatch")
    return selected, scored_ids


def validate_b1_row(row: dict[str, Any], prompt: dict[str, Any], label: str) -> None:
    fail_on_legacy_acceptable_fields(row, label)
    require_exact_keys(row, required=B1_REQUIRED_KEYS, optional=B1_OPTIONAL_KEYS, label=label)
    require(row["schema_version"] == B1_SCHEMA, f"B1 schema mismatch: {label}")
    require(row["version_id"] == VERSION_ID, f"B1 version mismatch: {label}")
    require(row["retriever"] in EXPECTED_B1_RETRIEVERS, f"B1 retriever mismatch: {label}")
    require(row["representation"] in EXPECTED_REPRESENTATIONS, f"B1 representation mismatch: {label}")
    for key in ("prompt_id", "prompt_sha256", "stratum", "group", "gold_skill"):
        require(row[key] == prompt[key], f"B1 {key} mismatch: {label}")
    rank = row["strict_gold_rank"]
    require(isinstance(rank, int) and not isinstance(rank, bool) and 1 <= rank <= 2433, f"B1 strict rank invalid: {label}")
    expected = {
        "strict_hit_at_1": int(rank == 1),
        "strict_recall_at_5": int(rank <= 5),
        "strict_recall_at_20": int(rank <= 20),
        "strict_recall_at_50": int(rank <= 50),
        "strict_recall_at_100": int(rank <= 100),
        "strict_mrr_at_10": 0.0 if rank > 10 else 1.0 / rank,
    }
    for key, value in expected.items():
        if isinstance(value, float):
            require(abs(float(row[key]) - value) <= 1e-12, f"B1 {key} mismatch: {label}")
        else:
            require(binary(row[key], f"B1 {key}: {label}") == value, f"B1 {key} mismatch: {label}")
    top5 = require_ranked_ids(row["top_5_skill_ids"], length=5, label=f"B1 top5: {label}")
    top20 = require_ranked_ids(row["top_20_skill_ids"], length=PRIMARY_K, label=f"B1 top20: {label}")
    top50 = require_ranked_ids(row["top_50_skill_ids"], length=50, label=f"B1 top50: {label}")
    top100 = row["top_100"]
    require(isinstance(top100, list) and len(top100) == PERSISTED_K, f"B1 top100 length mismatch: {label}")
    require(
        all(set(entry) == {"rank", "skill_id", "score"} for entry in top100),
        f"B1 top100 schema contains legacy labels or extra metadata: {label}",
    )
    require([entry["rank"] for entry in top100] == list(range(1, PERSISTED_K + 1)), f"B1 top100 ranks mismatch: {label}")
    top100_ids = require_ranked_ids([entry["skill_id"] for entry in top100], length=PERSISTED_K, label=f"B1 top100 IDs: {label}")
    for entry in top100:
        finite_number(entry["score"], f"B1 top100 score: {label}")
    require(top5 == top100_ids[:5] and top20 == top100_ids[:20] and top50 == top100_ids[:50], f"B1 persisted rank prefixes drift: {label}")
    if rank <= PERSISTED_K:
        require(top100_ids[rank - 1] == prompt["gold_skill"], f"B1 strict rank does not point to gold: {label}")
    else:
        require(prompt["gold_skill"] not in top100_ids, f"B1 strict gold appears inside top100 at a rank above 100: {label}")
    require(finite_number(row["query_seconds"], f"B1 query time: {label}") >= 0.0, f"B1 query time invalid: {label}")


def validate_b1_matrix(root: Path, rows: list[dict[str, Any]]) -> dict[tuple[str, str, str], dict[str, Any]]:
    prompts, scored_ids = load_scored_prompts(root)
    indexed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row.get("retriever")), str(row.get("representation")), str(row.get("prompt_id")))
        require(key not in indexed, f"Duplicate B1 condition: {key}")
        require(key[2] in prompts and key[2] in scored_ids, f"B1 prompt outside v1.1 scored population: {key}")
        validate_b1_row(row, prompts[key[2]], "/".join(key))
        indexed[key] = row
    expected = {
        (retriever, representation, prompt_id)
        for retriever in EXPECTED_B1_RETRIEVERS
        for representation in EXPECTED_REPRESENTATIONS
        for prompt_id in scored_ids
    }
    require(set(indexed) == expected, f"v1.1 B1 matrix mismatch: expected {len(expected)}, got {len(indexed)}")
    return indexed


def validate_b2_row(
    row: dict[str, Any], prompt: dict[str, Any], b1_row: dict[str, Any], label: str
) -> None:
    fail_on_legacy_acceptable_fields(row, label)
    require_exact_keys(row, required=B2_REQUIRED_KEYS, optional=B2_OPTIONAL_KEYS, label=label)
    require(row["schema_version"] == B2_SCHEMA, f"B2 schema mismatch: {label}")
    require(row["version_id"] == VERSION_ID, f"B2 version mismatch: {label}")
    require(row["reranker"] in EXPECTED_RERANKERS, f"B2 reranker mismatch: {label}")
    require(row["first_stage_retriever"] in EXPECTED_B1_RETRIEVERS, f"B2 first-stage retriever mismatch: {label}")
    require(row["representation"] in EXPECTED_REPRESENTATIONS, f"B2 representation mismatch: {label}")
    for key in ("prompt_id", "prompt_sha256", "stratum", "group", "gold_skill"):
        require(row[key] == prompt[key], f"B2 {key} mismatch: {label}")
    candidates = require_ranked_ids(row["candidate_skill_ids"], length=PRIMARY_K, label=f"B2 candidates: {label}")
    require(candidates == b1_row["top_20_skill_ids"], f"B2 candidates drift from persisted B1 Top-20: {label}")
    require(row["candidate_list_sha256"] == sha256_json(candidates), f"B2 candidate list hash mismatch: {label}")
    reranked = require_ranked_ids(row["reranked_skill_ids"], length=PRIMARY_K, label=f"B2 reranked IDs: {label}")
    require(set(reranked) == set(candidates), f"B2 reranker changed candidate identity: {label}")
    scores = row["reranked_scores"]
    require(isinstance(scores, list) and len(scores) == PRIMARY_K, f"B2 score vector length invalid: {label}")
    for score in scores:
        finite_number(score, f"B2 reranked score: {label}")
    candidate_positive = int(prompt["gold_skill"] in candidates)
    first_stage_top1 = int(candidates[0] == prompt["gold_skill"])
    reranked_top1 = int(reranked[0] == prompt["gold_skill"])
    expected = {
        "strict_candidate_positive": candidate_positive,
        "first_stage_strict_top1": first_stage_top1,
        "reranked_strict_top1": reranked_top1,
        "conditional_strict_top1_numerator": int(candidate_positive and reranked_top1),
        "conditional_strict_top1_denominator": candidate_positive,
        "end_to_end_strict_top1": reranked_top1,
        "strict_reranker_gain": int(candidate_positive and reranked_top1 and not first_stage_top1),
        "strict_reranker_regression": int(first_stage_top1 and not reranked_top1),
    }
    for key, value in expected.items():
        require(binary(row[key], f"B2 {key}: {label}") == value, f"B2 {key} mismatch: {label}")
    rank = reranked.index(prompt["gold_skill"]) + 1 if candidate_positive else None
    expected_mrr = 0.0 if rank is None else 1.0 / rank
    require(abs(finite_number(row["end_to_end_strict_mrr_at_20"], f"B2 strict MRR: {label}") - expected_mrr) <= 1e-12, f"B2 strict MRR mismatch: {label}")
    require(finite_number(row["rerank_seconds"], f"B2 rerank time: {label}") >= 0.0, f"B2 rerank time invalid: {label}")


def validate_b2_matrix(root: Path, b1_rows: list[dict[str, Any]], b2_rows: list[dict[str, Any]]) -> None:
    b1_index = validate_b1_matrix(root, b1_rows)
    prompts, scored_ids = load_scored_prompts(root)
    seen: set[tuple[str, str, str, str]] = set()
    for row in b2_rows:
        key = (
            str(row.get("reranker")),
            str(row.get("first_stage_retriever")),
            str(row.get("representation")),
            str(row.get("prompt_id")),
        )
        require(key not in seen, f"Duplicate B2 condition: {key}")
        b1_key = (key[1], key[2], key[3])
        require(key[3] in prompts and b1_key in b1_index, f"B2 condition lacks v1.1 B1 source: {key}")
        validate_b2_row(row, prompts[key[3]], b1_index[b1_key], "/".join(key))
        seen.add(key)
    expected = {
        (reranker, retriever, representation, prompt_id)
        for reranker in EXPECTED_RERANKERS
        for retriever in EXPECTED_B1_RETRIEVERS
        for representation in EXPECTED_REPRESENTATIONS
        for prompt_id in scored_ids
    }
    require(seen == expected, f"v1.1 B2 matrix mismatch: expected {len(expected)}, got {len(seen)}")


def strict_descriptive_summary(rows: list[dict[str, Any]], *, stage: str) -> list[dict[str, Any]]:
    require(stage in {"B1", "B2"}, "Unknown strict summary stage")
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    if stage == "B1":
        for row in rows:
            grouped[(row["retriever"], row["representation"], row["stratum"])].append(row)
    else:
        for row in rows:
            grouped[(row["reranker"], row["first_stage_retriever"], row["representation"], row["stratum"])].append(row)
    summary: list[dict[str, Any]] = []
    for condition, condition_rows in sorted(grouped.items()):
        common = {"stage": stage, "prompts": len(condition_rows)}
        if stage == "B1":
            retriever, representation, stratum = condition
            summary.append(
                {
                    **common,
                    "retriever": retriever,
                    "representation": representation,
                    "stratum": stratum,
                    "strict_hit_at_1": sum(int(row["strict_hit_at_1"]) for row in condition_rows) / len(condition_rows),
                    "strict_recall_at_20": sum(int(row["strict_recall_at_20"]) for row in condition_rows) / len(condition_rows),
                    "strict_mrr_at_10": sum(float(row["strict_mrr_at_10"]) for row in condition_rows) / len(condition_rows),
                }
            )
        else:
            reranker, retriever, representation, stratum = condition
            candidate_positive = sum(int(row["strict_candidate_positive"]) for row in condition_rows)
            end_to_end = sum(int(row["end_to_end_strict_top1"]) for row in condition_rows)
            summary.append(
                {
                    **common,
                    "reranker": reranker,
                    "first_stage_retriever": retriever,
                    "representation": representation,
                    "stratum": stratum,
                    "strict_recall_at_20": candidate_positive / len(condition_rows),
                    "conditional_strict_hit_at_1": end_to_end / candidate_positive if candidate_positive else 0.0,
                    "end_to_end_strict_hit_at_1": end_to_end / len(condition_rows),
                    "end_to_end_strict_mrr_at_20": sum(float(row["end_to_end_strict_mrr_at_20"]) for row in condition_rows) / len(condition_rows),
                    "strict_reranker_gain_rate": sum(int(row["strict_reranker_gain"]) for row in condition_rows) / len(condition_rows),
                    "strict_reranker_regression_rate": sum(int(row["strict_reranker_regression"]) for row in condition_rows) / len(condition_rows),
                }
            )
    return summary


def synthetic_prompt(prompt_id: str, stratum: str, group: str) -> dict[str, Any]:
    return {
        "prompt_id": prompt_id,
        "prompt_sha256": f"sha-{prompt_id}",
        "stratum": stratum,
        "group": group,
        "gold_skill": f"gold-{prompt_id}",
    }


def synthetic_b1_row(prompt: dict[str, Any], retriever: str, representation: str) -> dict[str, Any]:
    ranking = [prompt["gold_skill"], *[f"candidate-{index:04d}" for index in range(1, PERSISTED_K)]]
    top100 = [
        {"rank": index, "skill_id": skill_id, "score": float(PERSISTED_K - index)}
        for index, skill_id in enumerate(ranking, start=1)
    ]
    return {
        "schema_version": B1_SCHEMA,
        "version_id": VERSION_ID,
        "runner_version": "synthetic-no-network",
        "retriever": retriever,
        "representation": representation,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": 1,
        "strict_hit_at_1": 1,
        "strict_recall_at_5": 1,
        "strict_recall_at_20": 1,
        "strict_recall_at_50": 1,
        "strict_recall_at_100": 1,
        "strict_mrr_at_10": 1.0,
        "top_5_skill_ids": ranking[:5],
        "top_20_skill_ids": ranking[:20],
        "top_50_skill_ids": ranking[:50],
        "top_100": top100,
        "query_seconds": 0.0,
    }


def synthetic_b2_row(b1_row: dict[str, Any], reranker: str) -> dict[str, Any]:
    candidates = list(b1_row["top_20_skill_ids"])
    return {
        "schema_version": B2_SCHEMA,
        "version_id": VERSION_ID,
        "runner_version": "synthetic-no-network",
        "reranker": reranker,
        "first_stage_retriever": b1_row["retriever"],
        "representation": b1_row["representation"],
        "prompt_id": b1_row["prompt_id"],
        "prompt_sha256": b1_row["prompt_sha256"],
        "stratum": b1_row["stratum"],
        "group": b1_row["group"],
        "gold_skill": b1_row["gold_skill"],
        "candidate_skill_ids": candidates,
        "candidate_list_sha256": sha256_json(candidates),
        "reranked_skill_ids": candidates,
        "reranked_scores": [float(PRIMARY_K - index) for index in range(PRIMARY_K)],
        "strict_candidate_positive": 1,
        "first_stage_strict_top1": 1,
        "reranked_strict_top1": 1,
        "conditional_strict_top1_numerator": 1,
        "conditional_strict_top1_denominator": 1,
        "end_to_end_strict_top1": 1,
        "end_to_end_strict_mrr_at_20": 1.0,
        "strict_reranker_gain": 0,
        "strict_reranker_regression": 0,
        "rerank_seconds": 0.0,
    }


def expect_value_error(action: Any, label: str) -> None:
    try:
        action()
    except ValueError:
        return
    raise AssertionError(f"Expected strict v1.1 contract rejection: {label}")


def self_test(root: Path) -> dict[str, Any]:
    prompts, _ = load_scored_prompts(root)
    b1_rows = [
        synthetic_b1_row(prompt, retriever, representation)
        for prompt_id, prompt in sorted(prompts.items())
        for retriever in sorted(EXPECTED_B1_RETRIEVERS)
        for representation in sorted(EXPECTED_REPRESENTATIONS)
    ]
    b1_index = validate_b1_matrix(root, b1_rows)
    b2_rows = [
        synthetic_b2_row(b1_row, reranker)
        for _, b1_row in sorted(b1_index.items())
        for reranker in sorted(EXPECTED_RERANKERS)
    ]
    validate_b2_matrix(root, b1_rows, b2_rows)

    legacy = dict(b1_rows[0])
    legacy["acceptable_hit_at_1"] = 1
    expect_value_error(lambda: validate_b1_row(legacy, prompts[legacy["prompt_id"]], "legacy"), "legacy acceptable field")
    drift = dict(b2_rows[0])
    drift["candidate_skill_ids"] = list(reversed(drift["candidate_skill_ids"]))
    drift["candidate_list_sha256"] = sha256_json(drift["candidate_skill_ids"])
    expect_value_error(
        lambda: validate_b2_row(
            drift,
            prompts[drift["prompt_id"]],
            b1_index[(drift["first_stage_retriever"], drift["representation"], drift["prompt_id"])],
            "candidate-drift",
        ),
        "B2 candidate-order drift",
    )
    beyond_top100 = dict(b1_rows[0])
    beyond_ids = [f"beyond-top100-{index:03d}" for index in range(1, PERSISTED_K + 1)]
    beyond_top100["top_5_skill_ids"] = beyond_ids[:5]
    beyond_top100["top_20_skill_ids"] = beyond_ids[:20]
    beyond_top100["top_50_skill_ids"] = beyond_ids[:50]
    beyond_top100["top_100"] = [
        {"rank": index, "skill_id": skill_id, "score": float(PERSISTED_K - index)}
        for index, skill_id in enumerate(beyond_ids, start=1)
    ]
    beyond_top100["strict_gold_rank"] = 101
    beyond_top100["strict_hit_at_1"] = 0
    beyond_top100["strict_recall_at_5"] = 0
    beyond_top100["strict_recall_at_20"] = 0
    beyond_top100["strict_recall_at_50"] = 0
    beyond_top100["strict_recall_at_100"] = 0
    beyond_top100["strict_mrr_at_10"] = 0.0
    validate_b1_row(beyond_top100, prompts[beyond_top100["prompt_id"]], "beyond-top100")
    nonfinite_score_rejected = False
    nonfinite = dict(b2_rows[0])
    nonfinite["reranked_scores"] = [float("nan"), *nonfinite["reranked_scores"][1:]]
    try:
        validate_b2_row(
            nonfinite,
            prompts[nonfinite["prompt_id"]],
            b1_index[(nonfinite["first_stage_retriever"], nonfinite["representation"], nonfinite["prompt_id"])],
            "nonfinite-score",
        )
    except ValueError:
        nonfinite_score_rejected = True
    require(nonfinite_score_rejected, "Synthetic non-finite B2 score was accepted")
    summary = {
        "b1": strict_descriptive_summary(b1_rows, stage="B1"),
        "b2": strict_descriptive_summary(b2_rows, stage="B2"),
    }
    require(all(row["stratum"] in SCORING_STRATA for group in summary.values() for row in group), "Pooled or stress summary generated")
    return {
        "schema_version": SMOKE_SCHEMA,
        "state": "pass_synthetic_zero_network_no_scientific_result",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "version_id": VERSION_ID,
        "scored_prompt_count": len(prompts),
        "b1_rows": len(b1_rows),
        "b2_rows": len(b2_rows),
        "legacy_acceptable_fields_rejected": True,
        "b2_candidate_order_drift_rejected": True,
        "rank_above_persisted_top100_validated": True,
        "nonfinite_scores_rejected": nonfinite_score_rejected,
        "separate_strata_only": True,
        "synthetic_summary_condition_counts": {
            "b1": len(summary["b1"]),
            "b2": len(summary["b2"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    require(args.self_test, "This zero-network helper only supports --self-test")
    root = args.root.resolve()
    report = self_test(root)
    if args.record:
        output = root / RELATIVE_ROOT / "v11_execution_contract_smoke.json"
        write_json_new(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
