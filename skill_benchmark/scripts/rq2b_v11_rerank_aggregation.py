#!/usr/bin/env python3
"""Strict v1.1 B2 aggregation shared by future SkillRouter and Qwen runners.

This module never calls a reranker.  It turns already-obtained per-candidate
window scores into a strict-only result row while preserving the exact B1
Top-20 candidate identity and order contract.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from rq2b_common import repo_root, require, sha256_json, write_json_new
from rq2b_v11_execution_contract import B2_SCHEMA, PRIMARY_K, validate_b2_row


RUNNER_VERSION = "rq2b-v11-rerank-aggregation-v1"


def aggregate_window_scores(window_scores: list[float], aggregation: str) -> float:
    require(bool(window_scores), "Reranker candidate has no window scores")
    require(
        all(
            isinstance(score, (int, float))
            and not isinstance(score, bool)
            and math.isfinite(float(score))
            for score in window_scores
        ),
        "Reranker score is not a finite number",
    )
    if aggregation == "maximum_window_score":
        return float(max(window_scores))
    if aggregation == "mean_window_score":
        return float(sum(window_scores) / len(window_scores))
    raise ValueError(f"Unknown reranker aggregation: {aggregation}")


def rank_candidates(
    candidate_skill_ids: list[str], scores_by_skill: dict[str, list[float]], *, aggregation: str
) -> list[tuple[str, float]]:
    require(len(candidate_skill_ids) == len(set(candidate_skill_ids)) == PRIMARY_K, "Reranker requires ordered unique Top-20 candidates")
    require(set(scores_by_skill) == set(candidate_skill_ids), "Reranker score coverage differs from B1 Top-20")
    first_stage_rank = {skill_id: index for index, skill_id in enumerate(candidate_skill_ids)}
    scored = [
        (skill_id, aggregate_window_scores(scores_by_skill[skill_id], aggregation))
        for skill_id in candidate_skill_ids
    ]
    return sorted(scored, key=lambda row: (-row[1], first_stage_rank[row[0]], row[0]))


def build_b2_row(
    *,
    prompt: dict[str, Any],
    b1_row: dict[str, Any],
    reranker: str,
    scores_by_skill: dict[str, list[float]],
    rerank_seconds: float,
    primary_window_aggregation: str = "maximum_window_score",
    runner_version: str = RUNNER_VERSION,
) -> dict[str, Any]:
    candidates = list(b1_row["top_20_skill_ids"])
    ranked = rank_candidates(candidates, scores_by_skill, aggregation=primary_window_aggregation)
    reranked_ids = [skill_id for skill_id, _ in ranked]
    candidate_positive = int(prompt["gold_skill"] in candidates)
    first_stage_top1 = int(candidates[0] == prompt["gold_skill"])
    reranked_top1 = int(reranked_ids[0] == prompt["gold_skill"])
    strict_rank = reranked_ids.index(prompt["gold_skill"]) + 1 if candidate_positive else None
    row = {
        "schema_version": B2_SCHEMA,
        "version_id": "rq2b-full-library-v1.1-2026-08-15",
        "runner_version": runner_version,
        "reranker": reranker,
        "first_stage_retriever": b1_row["retriever"],
        "representation": b1_row["representation"],
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "candidate_skill_ids": candidates,
        "candidate_list_sha256": sha256_json(candidates),
        "reranked_skill_ids": reranked_ids,
        "reranked_scores": [score for _, score in ranked],
        "strict_candidate_positive": candidate_positive,
        "first_stage_strict_top1": first_stage_top1,
        "reranked_strict_top1": reranked_top1,
        "conditional_strict_top1_numerator": int(candidate_positive and reranked_top1),
        "conditional_strict_top1_denominator": candidate_positive,
        "end_to_end_strict_top1": reranked_top1,
        "end_to_end_strict_mrr_at_20": 0.0 if strict_rank is None else 1.0 / strict_rank,
        "strict_reranker_gain": int(candidate_positive and reranked_top1 and not first_stage_top1),
        "strict_reranker_regression": int(first_stage_top1 and not reranked_top1),
        "rerank_seconds": float(rerank_seconds),
        "primary_window_aggregation": primary_window_aggregation,
    }
    validate_b2_row(row, prompt, b1_row, f"{reranker}/{b1_row['retriever']}/{b1_row['representation']}/{prompt['prompt_id']}")
    return row


def self_test() -> dict[str, Any]:
    prompt = {
        "prompt_id": "synthetic-prompt",
        "prompt_sha256": "synthetic-sha",
        "stratum": "controlled",
        "group": "synthetic-group",
        "gold_skill": "gold",
    }
    candidates = ["alternate", "gold"] + [f"background-{index:03d}" for index in range(18)]
    b1_row = {
        "retriever": "bm25",
        "representation": "i3c-fielded-evidence",
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "top_20_skill_ids": candidates,
    }
    scores = {skill_id: [0.1] for skill_id in candidates}
    scores["gold"] = [0.2, 0.9]
    scores["alternate"] = [0.8, 0.1]
    row = build_b2_row(
        prompt=prompt,
        b1_row=b1_row,
        reranker="qwen3-rerank",
        scores_by_skill=scores,
        rerank_seconds=0.0,
    )
    require(row["reranked_skill_ids"][0] == "gold", "Reranker maximum aggregation failed")
    require(row["strict_reranker_gain"] == 1, "Reranker gain calculation failed")
    require(rank_candidates(candidates, scores, aggregation="mean_window_score")[0][0] == "gold", "Reranker mean sensitivity failed")
    return {
        "state": "pass_synthetic_zero_network_no_scientific_result",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "primary_top1": row["reranked_skill_ids"][0],
        "strict_reranker_gain": row["strict_reranker_gain"],
        "candidate_order_preserved_as_tie_break": True,
        "supported_aggregations": ["maximum_window_score", "mean_window_score"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    require(args.self_test, "This aggregation module only exposes --self-test")
    report = self_test()
    if args.record is not None:
        output = args.record if args.record.is_absolute() else repo_root() / args.record
        write_json_new(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
