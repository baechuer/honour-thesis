#!/usr/bin/env python3
"""Strict-only local RQ2b v1.1 analysis binding.

This module accepts already-created B1/B2 rows, validates their full v1.1
matrix contract, and creates only separate controlled/public-gold summaries.
It intentionally has no CLI for real result analysis until the future runner,
independent review, and implementation seal are complete.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import repo_root, require, write_json_new
from rq2b_v11_execution_contract import (
    EXPECTED_B1_RETRIEVERS,
    EXPECTED_RERANKERS,
    EXPECTED_REPRESENTATIONS,
    strict_descriptive_summary,
    synthetic_b1_row,
    synthetic_b2_row,
    validate_b1_matrix,
    validate_b2_matrix,
)


ANALYSIS_VERSION = "rq2b-v11-strict-analysis-binding-v1"


def analyse(root: Path, b1_rows: list[dict[str, Any]], b2_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate one full v1.1 matrix, then return strict-only descriptive rows."""
    b1_index = validate_b1_matrix(root, b1_rows)
    validate_b2_matrix(root, b1_rows, b2_rows)
    b1_summary = strict_descriptive_summary(b1_rows, stage="B1")
    b2_summary = strict_descriptive_summary(b2_rows, stage="B2")
    require(len(b1_summary) == 24, "v1.1 B1 summary must have 12 cells x 2 strata")
    require(len(b2_summary) == 48, "v1.1 B2 summary must have 24 cells x 2 strata")
    require(
        all(row["stratum"] in {"controlled", "public_gold"} for row in [*b1_summary, *b2_summary]),
        "v1.1 analysis generated a pooled or stress accuracy summary",
    )
    return {
        "schema_version": "rq2b-v11-strict-analysis-report-v1",
        "state": "strict_matrix_validated_not_for_thesis_until_user_review",
        "analysis_version": ANALYSIS_VERSION,
        "network_calls": 0,
        "scientific_selector_runs": 0,
        "texts_transmitted": 0,
        "thesis_results_written": False,
        "inputs": {
            "b1_rows": len(b1_index),
            "b2_rows": len(b2_rows),
            "b1_retrievers": sorted(EXPECTED_B1_RETRIEVERS),
            "b2_rerankers": sorted(EXPECTED_RERANKERS),
            "representations": sorted(EXPECTED_REPRESENTATIONS),
        },
        "reporting_policy": {
            "strict_gold_only": True,
            "separate_controlled_and_public_gold": True,
            "pooled_accuracy_headline_permitted": False,
            "acceptable_endpoints_permitted": False,
        },
        "b1_descriptive_matrix": b1_summary,
        "b2_descriptive_matrix": b2_summary,
    }


def self_test(root: Path) -> dict[str, Any]:
    from rq2b_v11_execution_contract import load_scored_prompts

    prompts, _ = load_scored_prompts(root)
    b1_rows = [
        synthetic_b1_row(prompt, retriever, representation)
        for _, prompt in sorted(prompts.items())
        for retriever in sorted(EXPECTED_B1_RETRIEVERS)
        for representation in sorted(EXPECTED_REPRESENTATIONS)
    ]
    b2_rows = [
        synthetic_b2_row(b1_row, reranker)
        for b1_row in b1_rows
        for reranker in sorted(EXPECTED_RERANKERS)
    ]
    report = analyse(root, b1_rows, b2_rows)
    require(report["inputs"]["b1_rows"] == 4572, "v1.1 analysis B1 cardinality regression")
    require(report["inputs"]["b2_rows"] == 9144, "v1.1 analysis B2 cardinality regression")
    require(report["reporting_policy"]["pooled_accuracy_headline_permitted"] is False, "v1.1 analysis allowed a pooled headline")
    return {
        "schema_version": "rq2b-v11-strict-analysis-smoke-v1",
        "state": "pass_synthetic_zero_network_no_scientific_result",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "b1_rows": report["inputs"]["b1_rows"],
        "b2_rows": report["inputs"]["b2_rows"],
        "b1_summary_rows": len(report["b1_descriptive_matrix"]),
        "b2_summary_rows": len(report["b2_descriptive_matrix"]),
        "strict_only": report["reporting_policy"]["strict_gold_only"],
        "pooled_accuracy_headline_permitted": report["reporting_policy"]["pooled_accuracy_headline_permitted"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    require(args.self_test, "This analysis binding only exposes --self-test")
    report = self_test(repo_root())
    if args.record is not None:
        output = args.record if args.record.is_absolute() else repo_root() / args.record
        write_json_new(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
