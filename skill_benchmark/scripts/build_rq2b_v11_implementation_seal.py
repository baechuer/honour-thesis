#!/usr/bin/env python3
"""Seal only the local RQ2b v1.1 strict-contract implementation.

This seal is intentionally narrower than the immutable base-v1 B1S seal.  It
binds the strict schemas, synthetic component checks, Qwen payload guards, and
the independent rereview.  It does not claim that I3C exists, that a model
adapter is implemented, or that retrieval/reranking has been run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import relative, repo_root, require, sha256_file, write_json_new
from rq2b_v11_contract import RELATIVE_ROOT, VERSION_ID, verify as verify_v11_contract


SEAL_NAME = "b1s_v11_strict_contract_implementation_seal.json"
SEAL_SCHEMA = "rq2b-v11-strict-contract-implementation-seal-v1"
SCRIPT_PATHS = (
    "skill_benchmark/scripts/rq2b_v11_contract.py",
    "skill_benchmark/scripts/rq2b_v11_execution_contract.py",
    "skill_benchmark/scripts/rq2b_v11_bm25_components.py",
    "skill_benchmark/scripts/rq2b_v11_rerank_aggregation.py",
    "skill_benchmark/scripts/rq2b_v11_analysis.py",
    "skill_benchmark/scripts/rq2b_qwen_reranker.py",
    "skill_benchmark/scripts/build_rq2b_v11_implementation_seal.py",
)
ARTIFACT_PATHS = {
    "strict_endpoint_contract": "v11_strict_endpoint_contract.json",
    "strict_contract_verification": "v11_contract_verification.json",
    "execution_contract_smoke": "v11_execution_contract_smoke.json",
    "bm25_component_smoke": "v11_bm25_component_smoke.json",
    "rerank_aggregation_smoke": "v11_rerank_aggregation_smoke.json",
    "analysis_binding_smoke": "v11_analysis_binding_smoke.json",
    "qwen_amendment": "b0f_a2_qwen_reranker_amendment.json",
    "qwen_contract_smoke": "b0f_a2_local_contract_smoke.json",
    "first_review_remediation": "B1S-v1.1 Review Remediation - 2026-08-15.md",
    "independent_rereview": "b1s_v11_independent_rereview_2026-08-15.json",
}


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"v1.1 artifact is not an object: {path}")
    return value


def bound_file(root: Path, path: Path) -> dict[str, Any]:
    require(path.is_file(), f"v1.1 seal artifact is missing: {path}")
    return {
        "path": relative(path, root),
        "sha256": sha256_file(path),
        "utf8_bytes": path.stat().st_size,
    }


def verify_zero_activity(report: dict[str, Any], label: str) -> None:
    require(report.get("network_calls") == 0, f"{label} records network calls")
    require(report.get("texts_transmitted") == 0, f"{label} records text transfer")
    require(report.get("scientific_selector_runs") == 0, f"{label} records scientific execution")
    require(report.get("thesis_results_written") is False, f"{label} records thesis result writing")


def verify(root: Path, seal_path: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    v11 = root / RELATIVE_ROOT
    verify_v11_contract(root)
    seal_path = seal_path or v11 / SEAL_NAME
    seal = read_json(seal_path)
    require(seal.get("schema_version") == SEAL_SCHEMA, "v1.1 seal schema mismatch")
    require(seal.get("version_id") == VERSION_ID, "v1.1 seal version mismatch")
    require(seal.get("state") == "strict_contract_implementation_sealed_no_scientific_execution", "v1.1 seal state mismatch")
    verify_zero_activity(seal, "v1.1 seal")
    require(seal.get("scope") == {
        "strict_contract_components_only": True,
        "i3c_extraction_complete": False,
        "model_adapters_complete": False,
        "scientific_retrieval_or_reranking_complete": False,
    }, "v1.1 seal scope mismatch")
    require(seal.get("next_gate", {}).get("stage") == "B1R", "v1.1 seal next gate mismatch")
    require(seal["next_gate"].get("requires_explicit_user_approval") is True, "v1.1 seal loses B1R approval gate")
    return seal


def build(root: Path) -> dict[str, Any]:
    root = root.resolve()
    v11 = root / RELATIVE_ROOT
    verify_v11_contract(root)
    seal_path = v11 / SEAL_NAME
    require(not seal_path.exists(), f"Refusing to overwrite v1.1 seal: {seal_path}")

    reports = {name: read_json(v11 / path) for name, path in ARTIFACT_PATHS.items() if path.endswith(".json")}
    for name in (
        "strict_contract_verification",
        "execution_contract_smoke",
        "bm25_component_smoke",
        "rerank_aggregation_smoke",
        "analysis_binding_smoke",
        "qwen_contract_smoke",
    ):
        verify_zero_activity(reports[name], name)
    require(reports["execution_contract_smoke"].get("rank_above_persisted_top100_validated") is True, "v1.1 rank-above-Top100 smoke missing")
    require(reports["execution_contract_smoke"].get("nonfinite_scores_rejected") is True, "v1.1 non-finite score smoke missing")
    require(reports["qwen_contract_smoke"].get("synthetic_fixture", {}).get("source_bound_query_drift_rejected") is True, "Qwen source-bound query drift smoke missing")
    require(reports["qwen_contract_smoke"].get("synthetic_fixture", {}).get("source_bound_window_text_drift_rejected") is True, "Qwen source-bound text drift smoke missing")
    rereview = reports["independent_rereview"]
    require(rereview.get("verdict") == "PASS", "v1.1 independent rereview did not pass")
    require(rereview.get("eligible_to_prepare_refreshed_local_seal") is True, "v1.1 rereview does not permit seal preparation")
    findings = rereview.get("finding_counts")
    require(isinstance(findings, dict) and findings.get("P0") == 0 and findings.get("P1") == 0, "v1.1 rereview has P0/P1 findings")
    require(rereview.get("review_boundary", {}).get("edits_made") is False, "v1.1 rereview was not read-only")
    verify_zero_activity(rereview.get("review_boundary", {}), "v1.1 independent rereview")

    scripts: dict[str, dict[str, Any]] = {}
    for path_text in SCRIPT_PATHS:
        path = root / path_text
        compile(path.read_text(encoding="utf-8"), path_text, "exec")
        scripts[path.stem] = bound_file(root, path)
    verification = reports["strict_contract_verification"]
    verifier = verification.get("verifier", {})
    require(
        verifier.get("sha256") == scripts["rq2b_v11_contract"]["sha256"],
        "v1.1 contract verification is not bound to the current verifier",
    )
    qwen_implementation = reports["qwen_contract_smoke"].get("implementation", {})
    require(
        qwen_implementation.get("sha256") == scripts["rq2b_qwen_reranker"]["sha256"],
        "v1.1 Qwen smoke is not bound to the current implementation",
    )

    forbidden_paths = {
        "i3c_merged": v11 / "i3c_merged",
        "i3c_manual_qa": v11 / "i3c_manual_qa",
        "scientific_runs": v11 / "runs",
        "qwen_provider_payloads": v11 / "qwen_payload",
        "skillrouter_provider_payloads": v11 / "skillrouter_payload",
    }
    production_boundaries = {name: path.exists() for name, path in forbidden_paths.items()}
    require(not any(production_boundaries.values()), "v1.1 seal found unexpected scientific output")

    seal = {
        "schema_version": SEAL_SCHEMA,
        "version_id": VERSION_ID,
        "state": "strict_contract_implementation_sealed_no_scientific_execution",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "scope": {
            "strict_contract_components_only": True,
            "i3c_extraction_complete": False,
            "model_adapters_complete": False,
            "scientific_retrieval_or_reranking_complete": False,
        },
        "counts": {
            "scored_prompts": 381,
            "controlled_scored_prompts": 243,
            "public_gold_scored_prompts": 138,
            "descriptive_stress_prompts": 12,
            "b1_condition_cells": 12,
            "b1_synthetic_rows": 4572,
            "b2_condition_cells": 24,
            "b2_synthetic_rows": 9144,
            "implementation_scripts": len(scripts),
        },
        "production_boundaries": production_boundaries,
        "independent_rereview": {
            "verdict": rereview["verdict"],
            "finding_counts": findings,
            "eligible_to_prepare_refreshed_local_seal": rereview["eligible_to_prepare_refreshed_local_seal"],
        },
        "bound_artifacts": {
            name: bound_file(root, v11 / path) for name, path in ARTIFACT_PATHS.items()
        },
        "implementation_scripts": scripts,
        "next_gate": {
            "stage": "B1R",
            "requires_explicit_user_approval": True,
            "authorised_now": False,
            "external_source_text_transfer": False,
            "provider_or_model_execution": False,
            "scientific_retrieval_or_reranking": False,
            "thesis_result_writing": False,
        },
    }
    write_json_new(seal_path, seal)
    return verify(root, seal_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = verify(args.root.resolve()) if args.verify_only else build(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
