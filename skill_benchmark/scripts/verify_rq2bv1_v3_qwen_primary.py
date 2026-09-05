#!/usr/bin/env python3
"""Verify and summarise the completed RQ2b V3 Qwen primary B1 run locally.

This verifier performs no network I/O and never changes scientific result rows.
It binds the completed run to its frozen payload and approval receipt, validates
every strict result row against the frozen v1.1 contract, checks request-record
integrity, and writes separate immutable verification and summary artifacts.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new
from rq2b_v11_execution_contract import validate_b1_row


REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3-flat-evidence",
    "i3c-fielded-evidence",
)
OUTPUT_ROOT = "skill_benchmark/rq2bv1/results/qwen_primary_v3"
VERIFICATION_NAME = "post_run_verification.json"
SUMMARY_NAME = "post_run_summary.json"


def percentile(values: list[float], quantile: float) -> float:
    require(values, "Cannot calculate a percentile over no values")
    ordered = sorted(values)
    index = max(0, math.ceil(quantile * len(ordered)) - 1)
    return float(ordered[index])


def metric_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(rows, "Cannot summarise an empty result group")
    return {
        "rows": len(rows),
        "strict_hit_at_1": mean(float(row["strict_hit_at_1"]) for row in rows),
        "strict_mrr_at_10": mean(float(row["strict_mrr_at_10"]) for row in rows),
        "strict_recall_at_5": mean(float(row["strict_recall_at_5"]) for row in rows),
        "strict_recall_at_20": mean(float(row["strict_recall_at_20"]) for row in rows),
        "strict_recall_at_50": mean(float(row["strict_recall_at_50"]) for row in rows),
        "strict_recall_at_100": mean(float(row["strict_recall_at_100"]) for row in rows),
    }


def timing_summary(values: list[float]) -> dict[str, float]:
    require(values and all(math.isfinite(value) and value >= 0.0 for value in values), "Invalid timing series")
    return {
        "mean_seconds": mean(values),
        "p50_seconds": percentile(values, 0.50),
        "p95_seconds": percentile(values, 0.95),
        "max_seconds": max(values),
    }


def _load_bound_artifact(root: Path, binding: dict[str, Any], label: str) -> Path:
    path = root / str(binding["path"])
    require(path.is_file(), f"Missing {label}: {path}")
    require(sha256_file(path) == binding["sha256"], f"{label} SHA-256 drift")
    return path


def verify(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    output_root = root / OUTPUT_ROOT
    manifest_path = output_root / "manifest.json"
    manifest = read_json(manifest_path)
    require(manifest["state"] == "qwen_primary_completed_pending_user_result_review", "Unexpected Qwen run state")
    require(manifest["method"] == {
        "retriever": "qwen-text-embedding-v4",
        "document_aggregation": "maximum_chunk_cosine",
        "field_aware": False,
        "reranking": False,
    }, "Qwen primary method drift")
    require(manifest["thesis_result_writing"] is False, "Qwen run incorrectly authorised thesis writing")

    payload_path = _load_bound_artifact(root, manifest["payload"], "payload manifest")
    approval_path = _load_bound_artifact(root, manifest["authorisation"], "approval receipt")
    payload = read_json(payload_path)
    approval = read_json(approval_path)
    require(approval["state"] == "explicitly_authorised_for_one_qwen_primary_v3_execution", "Approval receipt state drift")
    require(approval["run_id"] == manifest["run_id"], "Approval/run identity drift")
    require(int(approval["automatic_retries"]) == 0, "Approval permits automatic retries")

    rows_path = _load_bound_artifact(root, manifest["artifacts"]["rows"], "Qwen result rows")
    ledger_path = _load_bound_artifact(root, manifest["embedding_ledger"], "embedding ledger")
    rows = read_jsonl(rows_path)
    ledger = read_json(ledger_path)
    require(len(rows) == int(manifest["artifacts"]["rows"]["rows"]) == 1524, "Primary row count mismatch")

    prompt_path = _load_bound_artifact(root, payload["prompt_artifact"], "strict prompt artifact")
    prompts = read_jsonl(prompt_path)
    prompt_by_id = {str(prompt["prompt_id"]): prompt for prompt in prompts}
    require(len(prompts) == len(prompt_by_id) == 381, "Strict prompt identity drift")
    require(Counter(prompt["stratum"] for prompt in prompts) == {"controlled": 243, "public_gold": 138}, "Strict prompt strata drift")
    require(set(payload["query_text_ids"]) == set(prompt_by_id), "Payload query coverage drift")
    require(tuple(payload["documents"].keys()) == REPRESENTATIONS, "Representation ordering/coverage drift")

    selector_tokens: dict[str, int] = {}
    document_chunks: dict[str, int] = {}
    for representation in REPRESENTATIONS:
        documents = payload["documents"][representation]
        require(len(documents) == 2433, f"Candidate-library count drift: {representation}")
        skill_ids = [str(document["skill_id"]) for document in documents]
        require(len(skill_ids) == len(set(skill_ids)), f"Candidate identities are not unique: {representation}")
        selector_tokens[representation] = sum(int(document["selector_local_proxy_tokens"]) for document in documents)
        document_chunks[representation] = sum(len(document["chunk_text_ids"]) for document in documents)

    seen: set[tuple[str, str]] = set()
    rows_by_representation: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rows_by_representation_stratum: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    cold_query_seconds: dict[str, float] = {}
    for row in rows:
        representation = str(row.get("representation"))
        prompt_id = str(row.get("prompt_id"))
        require(representation in REPRESENTATIONS, f"Unexpected representation: {representation}")
        require(prompt_id in prompt_by_id, f"Result row uses an unbound prompt: {prompt_id}")
        key = (representation, prompt_id)
        require(key not in seen, f"Duplicate primary condition: {key}")
        seen.add(key)
        validate_b1_row(row, prompt_by_id[prompt_id], f"qwen-primary/{representation}/{prompt_id}")
        require(row["retriever"] == "qwen-text-embedding-v4", f"Retriever label drift: {key}")
        require(int(row["selector_visible_tokens"]) == selector_tokens[representation], f"Selector token drift: {key}")
        require(
            int(row["retriever_metadata"]["document_chunks"]) == document_chunks[representation],
            f"Document chunk-count drift: {key}",
        )
        require(
            abs(float(row["one_time_document_embedding_or_index_seconds"]) - float(manifest["document_embedding_seconds_by_representation"][representation])) <= 1e-9,
            f"Document timing drift: {key}",
        )
        cold_seconds = float(row["retriever_metadata"]["cold_query_embedding_seconds"])
        previous = cold_query_seconds.setdefault(prompt_id, cold_seconds)
        require(abs(previous - cold_seconds) <= 1e-12, f"Cold-query timing diverges across representations: {prompt_id}")
        rows_by_representation[representation].append(row)
        rows_by_representation_stratum[(representation, str(row["stratum"]))].append(row)
    expected_conditions = {(representation, prompt_id) for representation in REPRESENTATIONS for prompt_id in prompt_by_id}
    require(seen == expected_conditions, "Primary matrix condition coverage drift")
    require(len(cold_query_seconds) == 381, "Cold-query timing coverage drift")

    require(ledger["automatic_retries"] == 0, "Automatic retries occurred")
    require(ledger["cache_hits"] == 0 and ledger["document_cache_hits"] == 0, "First-run cache state drift")
    require(ledger["cache_misses"] == ledger["external_text_submissions"] == int(approval["maximum_new_cache_texts"]), "Embedding text-accounting drift")
    require(ledger["document_cache_misses"] == 8945, "Document cache-miss count drift")
    require(ledger["cold_query_requests"] == len(cold_query_seconds) == int(approval["cold_query_requests"]), "Cold-query request count drift")
    require(ledger["query_cache_entries_preexisting"] == 0, "Unexpected pre-existing query cache entries")
    require(ledger["request_attempts"] == ledger["successful_api_calls"] == manifest["network_calls"], "Request/success/network-call mismatch")
    for ledger_key, approval_key in (
        ("request_attempts", "maximum_request_attempts"),
        ("successful_api_calls", "maximum_successful_api_calls"),
        ("cache_misses", "maximum_new_cache_texts"),
        ("external_text_submissions", "maximum_external_text_submissions"),
        ("external_submission_proxy_tokens", "maximum_external_submission_proxy_tokens"),
        ("external_submission_utf8_bytes", "maximum_external_submission_utf8_bytes"),
    ):
        require(int(ledger[ledger_key]) <= int(approval[approval_key]), f"Approval cap exceeded: {ledger_key}")
    require(ledger["cold_query_latency_contract"] == {
        "required": True,
        "batch_size": 1,
        "one_provider_request_per_unique_query_text": True,
        "query_cache_is_not_used_to_skip_latency_measurement": True,
    }, "Cold-query latency contract drift")
    require(manifest["warm_replay"]["verified_conditions"] == len(rows), "Warm replay coverage drift")

    request_records = manifest["artifacts"]["request_records"]
    require(len(request_records) == 3 * int(ledger["request_attempts"]), "Request-record count mismatch")
    request_dir = output_root / "request_records"
    actual_record_paths = {relative(path, root) for path in request_dir.glob("*.json")}
    bound_record_paths = {str(record["path"]) for record in request_records}
    require(actual_record_paths == bound_record_paths, "Request-record path coverage drift")
    for record in request_records:
        _load_bound_artifact(root, record, "request record")

    verification = {
        "schema_version": "rq2bv1-v3-qwen-primary-post-run-verification-v1",
        "state": "passed_local_post_run_integrity_verification",
        "run_manifest": {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)},
        "payload": manifest["payload"],
        "approval_receipt": manifest["authorisation"],
        "result_rows": {"path": relative(rows_path, root), "sha256": sha256_file(rows_path), "rows": len(rows)},
        "embedding_ledger": {"path": relative(ledger_path, root), "sha256": sha256_file(ledger_path)},
        "checks": {
            "strict_contract_rows_validated": len(rows),
            "matrix_conditions_validated": len(seen),
            "unique_prompts_validated": len(prompt_by_id),
            "candidate_library_skills_per_representation": 2433,
            "request_records_hash_validated": len(request_records),
            "automatic_retries": int(ledger["automatic_retries"]),
            "request_attempts": int(ledger["request_attempts"]),
            "successful_api_calls": int(ledger["successful_api_calls"]),
            "warm_replay_conditions": int(manifest["warm_replay"]["verified_conditions"]),
        },
        "thesis_result_writing": False,
    }

    representation_summaries: dict[str, Any] = {}
    for representation in REPRESENTATIONS:
        rep_rows = rows_by_representation[representation]
        representation_summaries[representation] = {
            "overall": metric_summary(rep_rows),
            "controlled": metric_summary(rows_by_representation_stratum[(representation, "controlled")]),
            "public_gold": metric_summary(rows_by_representation_stratum[(representation, "public_gold")]),
            "cost_and_latency": {
                "selector_visible_tokens": selector_tokens[representation],
                "document_chunks": document_chunks[representation],
                "one_time_document_embedding_seconds": float(manifest["document_embedding_seconds_by_representation"][representation]),
                "local_vector_search": timing_summary([float(row["query_seconds"]) for row in rep_rows]),
            },
        }
    summary = {
        "schema_version": "rq2bv1-v3-qwen-primary-post-run-summary-v1",
        "state": "completed_pending_user_result_review",
        "scope": {
            "retriever": "qwen-text-embedding-v4",
            "document_aggregation": "maximum_chunk_cosine",
            "representations": list(REPRESENTATIONS),
            "scored_prompts": len(prompt_by_id),
            "strata": {"controlled": 243, "public_gold": 138},
            "candidate_library_skills": 2433,
            "field_aware": False,
            "reranking": False,
        },
        "quality_gate": verification["checks"],
        "provider_execution": {
            "request_attempts": int(ledger["request_attempts"]),
            "successful_api_calls": int(ledger["successful_api_calls"]),
            "automatic_retries": int(ledger["automatic_retries"]),
            "external_text_submissions": int(ledger["external_text_submissions"]),
            "provider_prompt_tokens": int(ledger["provider_usage"]["prompt_tokens"]),
            "embedding_wall_seconds": float(ledger["elapsed_seconds"]),
            "cold_query_embedding": timing_summary(list(cold_query_seconds.values())),
        },
        "representations": representation_summaries,
        "interpretation_boundary": "This is one completed primary B1 retriever run. It does not test field-aware scoring or B2 reranking, and it does not settle RQ2b until the remaining frozen B1/B2 conditions are completed and reviewed.",
        "thesis_result_writing": False,
    }
    return verification, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(args.verify, "Pass --verify to run the local post-run verifier")
    root = args.root.resolve()
    output_root = root / OUTPUT_ROOT
    verification_path = output_root / VERIFICATION_NAME
    summary_path = output_root / SUMMARY_NAME
    require(not verification_path.exists() and not summary_path.exists(), "Refusing to overwrite post-run verification artifacts")
    verification, summary = verify(root)
    write_json_new(verification_path, verification)
    write_json_new(summary_path, summary)
    print({
        "state": verification["state"],
        "verification": {"path": relative(verification_path, root), "sha256": sha256_file(verification_path)},
        "summary": {"path": relative(summary_path, root), "sha256": sha256_file(summary_path)},
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
