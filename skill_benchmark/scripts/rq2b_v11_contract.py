#!/usr/bin/env python3
"""Verify the local strict-only RQ2b v1.1 endpoint contract without scoring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, repo_root, require, sha256_file


VERSION_ID = "rq2b-full-library-v1.1-2026-08-15"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
CONTRACT_NAME = "v11_strict_endpoint_contract.json"
EXPECTED_STRATA = {"controlled": 243, "public_gold": 138, "stress": 12}
EXPECTED_SCORED_STRATA = {"controlled": 243, "public_gold": 138}
EXPECTED_B1_RETRIEVERS = {
    "bm25",
    "qwen-text-embedding-v4",
    "skillrouter-embedding-0.6b",
}
EXPECTED_REPRESENTATIONS = {
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
}
EXPECTED_RERANKERS = {"SkillRouter-Reranker-0.6B", "qwen3-rerank"}


def bound_path(root: Path, artifact: dict[str, Any], label: str) -> Path:
    path = root / artifact["path"]
    require(path.is_file(), f"v1.1 {label} artifact is missing: {path}")
    require(sha256_file(path) == artifact["sha256"], f"v1.1 {label} artifact hash drift")
    return path


def verify(root: Path) -> dict[str, Any]:
    version_root = root / RELATIVE_ROOT
    contract_path = version_root / CONTRACT_NAME
    require(contract_path.is_file(), f"v1.1 endpoint contract is missing: {contract_path}")
    contract = read_json(contract_path)
    require(
        contract.get("schema_version") == "rq2b-v11-strict-endpoint-contract-v1",
        "v1.1 endpoint contract schema mismatch",
    )
    require(contract.get("version_id") == VERSION_ID, "v1.1 endpoint contract version mismatch")
    require(
        contract.get("state") == "frozen_local_contract_no_scientific_result",
        "v1.1 endpoint contract state mismatch",
    )
    require(contract.get("network_calls") == 0, "v1.1 endpoint contract records network calls")
    require(contract.get("texts_transmitted") == 0, "v1.1 endpoint contract records text transfer")
    require(contract.get("scientific_selector_runs") == 0, "v1.1 endpoint contract records scientific scoring")
    require(contract.get("thesis_results_written") is False, "v1.1 endpoint contract records thesis results")

    overlay = contract.get("overlay_inputs")
    require(isinstance(overlay, dict) and set(overlay) == {
        "materialization_report", "prompt_manifest", "scored_prompt_ids"
    }, "v1.1 overlay input keys mismatch")
    report_path = bound_path(root, overlay["materialization_report"], "materialization report")
    prompt_path = bound_path(root, overlay["prompt_manifest"], "prompt manifest")
    scored_path = bound_path(root, overlay["scored_prompt_ids"], "scored prompt IDs")
    report = read_json(report_path)
    require(report.get("version") == VERSION_ID, "v1.1 materialization report version mismatch")
    require(report.get("evaluation_scope") == "strict_gold_only", "v1.1 materialization is not strict-only")
    require(set(report.get("accepted_metrics", [])) == {
        "strict_Hit@1", "strict_MRR@10", "strict_Recall@K"
    }, "v1.1 materialization accepted-metric mismatch")
    require(
        set(report.get("unavailable_metrics", [])) == {"acceptable_Hit@K", "acceptable_Recall@K"},
        "v1.1 materialization unavailable-metric mismatch",
    )

    prompts = read_jsonl(prompt_path)
    prompt_ids = [row.get("prompt_id") for row in prompts]
    require(len(prompt_ids) == len(set(prompt_ids)) == 393, "v1.1 prompt IDs are not unique")
    strata: dict[str, int] = {}
    for row in prompts:
        stratum = row.get("stratum")
        require(isinstance(stratum, str) and stratum in EXPECTED_STRATA, "v1.1 prompt has an invalid stratum")
        strata[stratum] = strata.get(stratum, 0) + 1
    require(strata == EXPECTED_STRATA, "v1.1 prompt-stratum count mismatch")

    scored_ids = read_json(scored_path)
    require(isinstance(scored_ids, list) and len(scored_ids) == len(set(scored_ids)) == 381, "v1.1 scored-ID count mismatch")
    prompts_by_id = {row["prompt_id"]: row for row in prompts}
    require(set(scored_ids).issubset(prompts_by_id), "v1.1 scored IDs are outside prompt manifest")
    scored_strata: dict[str, int] = {}
    for prompt_id in scored_ids:
        stratum = prompts_by_id[prompt_id]["stratum"]
        require(stratum != "stress", "v1.1 stress prompt is in a scored denominator")
        scored_strata[stratum] = scored_strata.get(stratum, 0) + 1
    require(scored_strata == EXPECTED_SCORED_STRATA, "v1.1 scored-stratum count mismatch")

    population = contract.get("population")
    require(population == {
        "scored_prompt_count": 381,
        "scored_strata": EXPECTED_SCORED_STRATA,
        "descriptive_only_strata": {"stress": 12},
        "candidate_library_skills": 2433,
    }, "v1.1 population contract mismatch")
    labels = contract.get("label_policy")
    require(
        labels == {
            "primary_endpoint": "strict_gold_only",
            "strict_gold_column": "gold_skill",
            "acceptable_skill_endpoints_permitted": False,
            "valid_skills_may_be_sent_to_provider": False,
            "gold_skill_may_be_sent_to_provider": False,
            "stress_prompts_in_accuracy_denominators": False,
        },
        "v1.1 label-policy mismatch",
    )
    b1 = contract.get("b1")
    require(set(b1.get("retrievers", [])) == EXPECTED_B1_RETRIEVERS, "v1.1 B1 retrievers mismatch")
    require(set(b1.get("representations", [])) == EXPECTED_REPRESENTATIONS, "v1.1 B1 representations mismatch")
    require(b1.get("primary_condition_cells") == 12, "v1.1 B1 cell count mismatch")
    require(b1.get("primary_result_rows") == 381 * 12, "v1.1 B1 result-row count mismatch")
    b2 = contract.get("b2")
    require(set(b2.get("rerankers", [])) == EXPECTED_RERANKERS, "v1.1 B2 reranker set mismatch")
    require(b2.get("condition_cells") == 24, "v1.1 B2 cell count mismatch")
    require(b2.get("primary_result_rows") == 381 * 24, "v1.1 B2 result-row count mismatch")
    require(b2.get("candidate_budget") == 20, "v1.1 B2 candidate budget mismatch")
    require(b2.get("reranker_scores_may_be_ensembled") is False, "v1.1 reranker ensembling is enabled")
    return {
        "state": "pass_zero_network_v11_contract_verified",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "contract_sha256": sha256_file(contract_path),
        "prompt_count": len(prompts),
        "scored_prompt_count": len(scored_ids),
        "strata": strata,
        "scored_strata": scored_strata,
        "b1_condition_cells": b1["primary_condition_cells"],
        "b2_condition_cells": b2["condition_cells"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    print(json.dumps(verify(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
