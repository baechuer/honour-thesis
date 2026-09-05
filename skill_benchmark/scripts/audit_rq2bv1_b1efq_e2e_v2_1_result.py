#!/usr/bin/env python3
"""Repeatable zero-network audit for the completed B1E-FQ V2.1 result."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from rq2b_common import read_json, read_jsonl, repo_root, require, sha256_file
from rq2bv1_b1efq_e2e_v2_1 import RESULT_ROOT, _strict_prompts, _validate_result_row


def main() -> None:
    root = repo_root()
    result_root = root / RESULT_ROOT
    manifest_path = result_root / "manifest.json"
    rows_path = result_root / "field_aligned_results.jsonl"
    ledger_path = result_root / "cost_ledger.json"
    receipt_path = result_root / "independent_verification.json"
    summary_path = result_root / "post_run_summary.json"
    correction_path = result_root / "location_correction.json"

    manifest = read_json(manifest_path)
    rows = read_jsonl(rows_path)
    ledger = read_json(ledger_path)
    receipt = read_json(receipt_path)
    summary = read_json(summary_path)
    correction = read_json(correction_path)
    _, prompts = _strict_prompts(root)
    prompts_by_id = {str(row["prompt_id"]): row for row in prompts}

    require(manifest["state"] == "complete_pending_user_result_review", "manifest state drift")
    require(receipt["state"] == "verified_complete_with_explicit_pure_and_fallback_subsets", "first-pass verification receipt drift")
    require(receipt["result_manifest"]["sha256"] == sha256_file(manifest_path), "receipt/manifest binding drift")
    require(len(rows) == len(prompts_by_id) == 381, "row/prompt coverage drift")
    require({str(row["prompt_id"]) for row in rows} == set(prompts_by_id), "prompt identity drift")
    for row in rows:
        _validate_result_row(row, prompts_by_id[str(row["prompt_id"])])

    sources = Counter(row["method_source"] for row in rows)
    require(sources == Counter({"pure_query_structured_field_aligned": 369, "fallback_i3c_single_vector": 12}), "pure/fallback source drift")
    require(ledger["coverage"]["all_rows"] == 381 and ledger["coverage"]["pure_field_aligned_rows"] == 369 and ledger["coverage"]["fallback_rows"] == 12, "ledger coverage drift")
    require(ledger["automatic_retries"] == 0 and ledger["candidate_field_embeddings"]["external_text_submissions_this_run"] == 0, "execution-boundary drift")
    require(summary["coverage"]["all_strict_prompts"] == 381 and summary["coverage"]["pure_field_aligned_prompts"] == 369 and summary["coverage"]["fallback_prompts"] == 12, "summary coverage drift")
    require(correction["executed_manifest"]["sha256"] == sha256_file(manifest_path), "location-correction manifest drift")
    require(correction["corrected_artifacts"]["cost_ledger"]["sha256"] == sha256_file(ledger_path), "location-correction ledger drift")
    require(correction["corrected_artifacts"]["result_rows"]["sha256"] == sha256_file(rows_path), "location-correction rows drift")

    print({
        "schema_version": "rq2bv1-v3-b1e-fq-e2e-v2-1-repeatable-post-run-audit-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
        "rows": 381,
        "pure_field_aligned_rows": 369,
        "fallback_rows": 12,
        "automatic_retries": 0,
        "manifest_path_correction_valid": True,
    })


if __name__ == "__main__":
    main()
