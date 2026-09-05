#!/usr/bin/env python3
"""Zero-network post-run analysis for the completed B1E-FQ V2.1 amendment.

This creates a small, explicit comparison artifact without modifying the
frozen B1 primary matrix or the executed B1E-FQ result rows.  It reports both
the pure field-aligned subset and the predeclared hybrid fallback coverage.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import read_jsonl, relative, repo_root, sha256_file, write_json_new


RESULT_ROOT = "skill_benchmark/rq2bv1/results/qwen_field_aligned_e2e_v2_1_full"
FQ_ROWS = "field_aligned_results.jsonl"
PRIMARY_ROWS = "skill_benchmark/rq2bv1/results/qwen_primary_v3/qwen_primary_strict_results.jsonl"
METRIC_KEYS = (
    "strict_hit_at_1",
    "strict_mrr_at_10",
    "strict_recall_at_5",
    "strict_recall_at_20",
    "strict_recall_at_50",
    "strict_recall_at_100",
)


def _metrics(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    if not rows:
        raise ValueError("Cannot summarise an empty subset")
    return {"rows": len(rows), **{key: sum(float(row[key]) for row in rows) / len(rows) for key in METRIC_KEYS}}


def _paired(fq_rows: list[dict[str, Any]], baseline: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pairs = [(row, baseline[str(row["prompt_id"])]) for row in fq_rows]
    hit_pairs = Counter((int(row["strict_hit_at_1"]), int(base["strict_hit_at_1"])) for row, base in pairs)
    rank_pairs = [(int(row["strict_gold_rank"]), int(base["strict_gold_rank"])) for row, base in pairs]
    return {
        "hit_at_1": {
            "field_aligned_only_correct": hit_pairs[(1, 0)],
            "single_vector_only_correct": hit_pairs[(0, 1)],
            "both_correct": hit_pairs[(1, 1)],
            "both_incorrect": hit_pairs[(0, 0)],
        },
        "strict_gold_rank_direction": {
            "field_aligned_better": sum(field_rank < base_rank for field_rank, base_rank in rank_pairs),
            "single_vector_better": sum(field_rank > base_rank for field_rank, base_rank in rank_pairs),
            "tied": sum(field_rank == base_rank for field_rank, base_rank in rank_pairs),
        },
    }


def _comparison(name: str, fq_rows: list[dict[str, Any]], baseline: dict[str, dict[str, Any]]) -> dict[str, Any]:
    field_metrics = _metrics(fq_rows)
    baseline_rows = [baseline[str(row["prompt_id"])] for row in fq_rows]
    single_metrics = _metrics(baseline_rows)
    return {
        "subset": name,
        "field_aligned": field_metrics,
        "qwen_i3c_single_vector_matched_prompts": single_metrics,
        "field_aligned_minus_single_vector": {
            key: field_metrics[key] - single_metrics[key] for key in METRIC_KEYS
        },
        "paired": _paired(fq_rows, baseline),
    }


def build(root: Path) -> dict[str, Any]:
    result_root = root / RESULT_ROOT
    fq_path = result_root / FQ_ROWS
    primary_path = root / PRIMARY_ROWS
    fq_rows = read_jsonl(fq_path)
    primary_rows = read_jsonl(primary_path)
    baseline = {
        str(row["prompt_id"]): row
        for row in primary_rows
        if row.get("representation") == "i3c-fielded-evidence"
        and row.get("retriever") == "qwen-text-embedding-v4"
    }
    if len(fq_rows) != len(baseline) or len(fq_rows) != 381:
        raise ValueError("B1E-FQ/primary prompt coverage drift")
    if {str(row["prompt_id"]) for row in fq_rows} != set(baseline):
        raise ValueError("B1E-FQ/primary prompt identity drift")

    pure = [row for row in fq_rows if row.get("method_source") == "pure_query_structured_field_aligned"]
    fallback = [row for row in fq_rows if row.get("method_source") == "fallback_i3c_single_vector"]
    if len(pure) + len(fallback) != len(fq_rows):
        raise ValueError("Unexpected B1E-FQ method source")

    return {
        "schema_version": "rq2bv1-v3-b1e-fq-e2e-v2-1-post-run-summary-v1",
        "state": "completed_pending_user_result_review_not_thesis_text",
        "method_boundary": {
            "name": "qwen_query_structured_field_aligned",
            "pure_subset": "only prompts with a valid exact-span parser result and valid query-field embeddings",
            "hybrid_subset": "all strict prompts; parser/embedding failures use the declared completed Qwen I3C single-vector fallback",
            "not_claimed": [
                "a change to the frozen 12-cell B1 primary matrix",
                "a reranking result",
                "a result for target-agnostic candidate-field late interaction",
                "thesis-ready evidence before user review",
            ],
        },
        "inputs": {
            "field_aligned_rows": {"path": relative(fq_path, root), "sha256": sha256_file(fq_path), "rows": len(fq_rows)},
            "matched_qwen_i3c_single_vector_rows": {"path": relative(primary_path, root), "sha256": sha256_file(primary_path), "rows": len(baseline)},
        },
        "coverage": {
            "all_strict_prompts": len(fq_rows),
            "pure_field_aligned_prompts": len(pure),
            "fallback_prompts": len(fallback),
            "fallback_failure_classes": dict(Counter(row.get("parser", {}).get("failure_class") for row in fallback)),
            "pure_active_field_count_distribution": dict(Counter(len(row.get("parser", {}).get("active_fields", [])) for row in pure)),
        },
        "comparisons": {
            "all_381_hybrid_fallback": _comparison("all_381_hybrid_fallback", fq_rows, baseline),
            "pure_369_only": _comparison("pure_369_only", pure, baseline),
            "controlled_pure": _comparison("controlled_pure", [row for row in pure if row["stratum"] == "controlled"], baseline),
            "public_gold_pure": _comparison("public_gold_pure", [row for row in pure if row["stratum"] == "public_gold"], baseline),
        },
        "network_calls": 0,
        "thesis_result_writing": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local B1E-FQ post-run comparison summary.")
    parser.add_argument("--write", action="store_true", help="Write the summary beside completed B1E-FQ rows.")
    args = parser.parse_args()
    if not args.write:
        raise ValueError("Pass --write to materialise the local summary")
    root = repo_root()
    output = root / RESULT_ROOT / "post_run_summary.json"
    if output.exists():
        raise ValueError(f"Refusing to overwrite existing summary: {output}")
    write_json_new(output, build(root))
    print(output.relative_to(root))


if __name__ == "__main__":
    main()
