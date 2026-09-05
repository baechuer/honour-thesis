#!/usr/bin/env python3
"""Verify and summarise completed local scoring for the recovered V3 SkillRouter run."""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new
from rq2b_v11_execution_contract import validate_b1_row
from rq2bv1_v3_skillrouter_primary_constants import MODEL, REPRESENTATIONS, RESULT_ROOT, REVISION


SCORING_ROOT = f"{RESULT_ROOT}/local_scoring_path_contract_amendment"
RECOVERY_ROOT = f"{RESULT_ROOT}/recovery"
AMENDMENT_PATH = f"{RESULT_ROOT}/local_path_contract_amendment_2026-08-22.json"
VERIFICATION_NAME = "post_run_verification.json"
SUMMARY_NAME = "post_run_summary.json"


def _timing_summary(values: list[float]) -> dict[str, float]:
    require(values and all(math.isfinite(value) and value >= 0.0 for value in values), "Invalid timing series")
    ordered = sorted(values)
    return {
        "mean_seconds": mean(values),
        "p50_seconds": ordered[max(0, math.ceil(0.50 * len(ordered)) - 1)],
        "p95_seconds": ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)],
        "max_seconds": max(values),
    }


def _metric_summary(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    require(rows, "Cannot summarise no result rows")
    return {
        "rows": len(rows),
        "strict_hit_at_1": mean(float(row["strict_hit_at_1"]) for row in rows),
        "strict_mrr_at_10": mean(float(row["strict_mrr_at_10"]) for row in rows),
        "strict_recall_at_5": mean(float(row["strict_recall_at_5"]) for row in rows),
        "strict_recall_at_20": mean(float(row["strict_recall_at_20"]) for row in rows),
        "strict_recall_at_50": mean(float(row["strict_recall_at_50"]) for row in rows),
        "strict_recall_at_100": mean(float(row["strict_recall_at_100"]) for row in rows),
    }


def verify(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    scoring_root = root / SCORING_ROOT
    scoring_path = scoring_root / "manifest.json"
    scoring = read_json(scoring_path)
    require(scoring["state"] == "completed_pending_user_result_review", "Local scoring state drift")
    require(scoring["method"] == {
        "retriever": "skillrouter-embedding-0.6b",
        "document_aggregation": "single_full_context_cosine",
        "field_aware": False,
        "reranking": False,
    }, "SkillRouter scoring method drift")
    require(scoring["network_calls"] == 0 and scoring["thesis_result_writing"] is False, "Local scoring boundary drift")
    require(scoring["runner_version"] == "rq2bv1-v3-skillrouter-primary-local-path-contract-amendment-v3", "Path amendment runner-version drift")
    amendment_path = root / AMENDMENT_PATH
    amendment = read_json(amendment_path)
    require(amendment["state"] == "completed_local_scoring_pending_post_run_verification", "Path amendment state drift")
    require(amendment["amended_finalizer"]["sha256"] == "1da718896d7d3d5b5052b5d6004a112cf2b59a3c30ea4c28e867919e8b55725f", "Path amendment finaliser drift")

    host_path = root / RESULT_ROOT / "manifest.json"
    host = read_json(host_path)
    require(host["state"] == "hosted_embedding_complete_pending_local_scoring", "Hosted embedding state drift")
    require(scoring["hosted_embedding"] == {"path": relative(host_path, root), "sha256": sha256_file(host_path)}, "Hosted manifest binding drift")
    require(host["hosted_scoring"] is False and host["gold_labels_transferred"] is False, "Hosted-boundary drift")
    ledger_path = root / str(host["embedding_ledger"]["path"])
    require(sha256_file(ledger_path) == host["embedding_ledger"]["sha256"], "Embedding-ledger hash drift")
    ledger = read_json(ledger_path)
    require(ledger == {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hosted-embedding-ledger-v1",
        "cache_hits": 0,
        "cache_misses": 9323,
        "document_cache_hits": 0,
        "document_cache_misses": 8942,
        "query_cache_hits": 0,
        "query_cache_misses": 381,
        "model_input_instances": 9323,
        "model_input_tokens": 2217994,
        "model_forward_batches": 1501,
        "automatic_retries": 0,
        "warm_cache_entries_verified": 9323,
        "model_load_seconds": ledger["model_load_seconds"],
    } and math.isfinite(float(ledger["model_load_seconds"])), "Embedding-ledger value drift")

    recovery_path = root / RECOVERY_ROOT / "recovery_manifest.json"
    recovery = read_json(recovery_path)
    require(recovery["state"] == "hosted_artifacts_recovered_and_verified_pending_local_scoring", "Recovery state drift")
    require(recovery["recovered_forward_records"] == 1501, "Recovered forward-record count drift")
    require(len(recovery["checkpoint_archives"]) == 61, "Checkpoint archive count drift")
    require([int(item["records"]) for item in recovery["checkpoint_archives"]] == [25] * 60 + [1], "Checkpoint record cadence drift")

    payload_path = root / str(host["payload"]["path"])
    require(sha256_file(payload_path) == host["payload"]["sha256"], "Payload hash drift")
    payload = read_json(payload_path)
    inventory_path = root / str(payload["text_inventory"]["path"])
    require(sha256_file(inventory_path) == payload["text_inventory"]["sha256"], "Inventory hash drift")
    inventory = {str(row["text_id"]): row for row in read_jsonl(inventory_path)}
    require(len(inventory) == 9323, "Inventory identity drift")
    prompt_path = root / str(payload["prompt_artifact"]["path"])
    require(sha256_file(prompt_path) == payload["prompt_artifact"]["sha256"], "Prompt hash drift")
    prompts = {str(row["prompt_id"]): row for row in read_jsonl(prompt_path)}
    require(len(prompts) == 381 and Counter(row["stratum"] for row in prompts.values()) == {"controlled": 243, "public_gold": 138}, "Prompt population drift")

    timings: dict[str, float] = {}
    for binding in host["forward_records"]:
        path = root / str(binding["path"])
        require(path.is_file() and sha256_file(path) == binding["sha256"], f"Forward-record hash drift: {path}")
        record = read_json(path)
        elapsed = float(record["elapsed_seconds"])
        require(math.isfinite(elapsed) and elapsed >= 0.0, f"Forward timing drift: {path}")
        for text_id in record["text_ids"]:
            require(text_id not in timings, f"Duplicate forwarded text: {text_id}")
            timings[str(text_id)] = elapsed / int(record["items"])
    require(set(timings) == set(inventory), "Forward-record text coverage drift")

    rows_path = root / str(scoring["rows"]["path"])
    require(rows_path.is_file() and sha256_file(rows_path) == scoring["rows"]["sha256"], "Result-row hash drift")
    rows = read_jsonl(rows_path)
    require(len(rows) == int(scoring["rows"]["rows"]) == 1524, "Result row-count drift")
    expected_pairs = {(representation, prompt_id) for representation in REPRESENTATIONS for prompt_id in prompts}
    seen: set[tuple[str, str]] = set()
    by_representation: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_representation_stratum: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    cold_query_seconds: dict[str, float] = {}
    selector_tokens: dict[str, int] = {}
    document_seconds: dict[str, float] = {}
    for representation in REPRESENTATIONS:
        documents = payload["documents"][representation]
        require(len(documents) == 2433, f"Candidate-library drift: {representation}")
        text_ids = [str(document["text_id"]) for document in documents]
        selector_tokens[representation] = sum(int(inventory[text_id]["model_tokens"]) for text_id in text_ids)
        document_seconds[representation] = sum(timings[text_id] for text_id in text_ids)
    for row in rows:
        representation, prompt_id = str(row["representation"]), str(row["prompt_id"])
        require(representation in REPRESENTATIONS and prompt_id in prompts, "Result identity drift")
        require((representation, prompt_id) not in seen, "Duplicate result condition")
        seen.add((representation, prompt_id))
        validate_b1_row(row, prompts[prompt_id], f"skillrouter-primary/{representation}/{prompt_id}")
        require(row["retriever"] == "skillrouter-embedding-0.6b", "Retriever label drift")
        require(int(row["selector_visible_tokens"]) == selector_tokens[representation], "Selector-token drift")
        require(abs(float(row["one_time_document_embedding_or_index_seconds"]) - document_seconds[representation]) <= 1e-9, "Document-time drift")
        metadata = row["retriever_metadata"]
        require(metadata["model"] == MODEL and metadata["revision"] == REVISION and int(metadata["dimensions"]) == 1024, "Retriever metadata drift")
        cold = float(metadata["cold_query_embedding_seconds"])
        require(math.isfinite(cold) and cold >= 0.0, "Cold-query timing drift")
        previous = cold_query_seconds.setdefault(prompt_id, cold)
        require(abs(previous - cold) <= 1e-12, "Cold-query timing differs by representation")
        by_representation[representation].append(row)
        by_representation_stratum[(representation, str(row["stratum"]))].append(row)
    require(seen == expected_pairs and len(cold_query_seconds) == 381, "Primary matrix coverage drift")
    require(scoring["warm_replay"] == {"state": "passed_zero_forward_warm_replay", "verified_conditions": 1524}, "Warm-replay drift")

    verification = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-post-run-verification-v1",
        "state": "passed_local_post_run_integrity_verification",
        "run_manifest": {"path": relative(scoring_path, root), "sha256": sha256_file(scoring_path)},
        "path_contract_amendment": {"path": relative(amendment_path, root), "sha256": sha256_file(amendment_path)},
        "hosted_embedding_manifest": {"path": relative(host_path, root), "sha256": sha256_file(host_path)},
        "recovery_manifest": {"path": relative(recovery_path, root), "sha256": sha256_file(recovery_path)},
        "result_rows": {"path": relative(rows_path, root), "sha256": sha256_file(rows_path), "rows": len(rows)},
        "checks": {
            "strict_contract_rows_validated": len(rows),
            "matrix_conditions_validated": len(seen),
            "unique_prompts_validated": len(prompts),
            "candidate_library_skills_per_representation": 2433,
            "recovered_forward_records_hash_validated": len(timings),
            "checkpoint_archives_hash_validated_during_recovery": len(recovery["checkpoint_archives"]),
            "automatic_retries": ledger["automatic_retries"],
            "warm_replay_conditions": scoring["warm_replay"]["verified_conditions"],
        },
        "network_calls": 0,
        "thesis_result_writing": False,
    }
    representations: dict[str, Any] = {}
    for representation in REPRESENTATIONS:
        rep_rows = by_representation[representation]
        representations[representation] = {
            "combined": _metric_summary(rep_rows),
            "controlled": _metric_summary(by_representation_stratum[(representation, "controlled")]),
            "public_gold": _metric_summary(by_representation_stratum[(representation, "public_gold")]),
            "cost_and_latency": {
                "selector_visible_tokens": selector_tokens[representation],
                "one_time_document_embedding_seconds": document_seconds[representation],
                "local_vector_search": _timing_summary([float(row["query_seconds"]) for row in rep_rows]),
            },
        }
    summary = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-post-run-summary-v1",
        "state": "completed_pending_user_result_review",
        "scope": {
            "retriever": "skillrouter-embedding-0.6b",
            "document_aggregation": "single_full_context_cosine",
            "representations": list(REPRESENTATIONS),
            "candidate_library_skills": 2433,
            "scored_prompts": 381,
            "strata": {"controlled": 243, "public_gold": 138},
            "field_aware": False,
            "reranking": False,
        },
        "quality_gate": verification["checks"],
        "hosted_execution": {
            "model_forward_batches": ledger["model_forward_batches"],
            "model_input_instances": ledger["model_input_instances"],
            "model_input_tokens": ledger["model_input_tokens"],
            "automatic_retries": ledger["automatic_retries"],
            "hosted_scoring": False,
            "gold_labels_transferred": False,
            "cold_query_embedding": _timing_summary(list(cold_query_seconds.values())),
        },
        "representations": representations,
        "interpretation_boundary": "This completes one frozen B1 native-SkillRouter single-vector condition. It does not test field-aware scoring or either B2 reranker, and it does not settle RQ2b until the remaining frozen conditions are completed and reviewed.",
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
    output = root / SCORING_ROOT
    verification_path = output / VERIFICATION_NAME
    summary_path = output / SUMMARY_NAME
    require(not verification_path.exists() and not summary_path.exists(), "Refusing to overwrite verification artifacts")
    verification, summary = verify(root)
    write_json_new(verification_path, verification)
    write_json_new(summary_path, summary)
    print({"state": verification["state"], "verification": relative(verification_path, root), "summary": relative(summary_path, root)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
