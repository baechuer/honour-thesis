#!/usr/bin/env python3
"""Locally verify and summarise one completed RQ2b V3 Qwen B1E-F run.

This script never contacts a provider, changes a scientific row, or writes to
the thesis. It binds the secondary amendment to its sealed payload and one
authorisation, validates all rows, verifies request accounting, and replays
the frozen local scoring path from exact cached vectors.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from prepare_rq2bv1_v3_qwen_field_aware_preflight import (
    FIELD_COMPONENT_REPRESENTATION,
    FIELD_ORDER,
    PACKET_NAME,
    PAYLOAD_NAME,
    PREFLIGHT_ROOT,
    RESULT_ROOT,
)
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new
from run_rq2b_qwen import ExactEmbeddingCache
from run_rq2bv1_v3_qwen_field_aware import (
    RESULT_SCHEMA,
    RUNNER_VERSION,
    _score,
    _validate_preflight,
    _validate_row,
)


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


def _metrics(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    require(rows, "Cannot summarise an empty B1E-F subset")
    return {
        "rows": len(rows),
        "strict_hit_at_1": mean(float(row["strict_hit_at_1"]) for row in rows),
        "strict_mrr_at_10": mean(float(row["strict_mrr_at_10"]) for row in rows),
        "strict_recall_at_5": mean(float(row["strict_recall_at_5"]) for row in rows),
        "strict_recall_at_20": mean(float(row["strict_recall_at_20"]) for row in rows),
        "strict_recall_at_50": mean(float(row["strict_recall_at_50"]) for row in rows),
        "strict_recall_at_100": mean(float(row["strict_recall_at_100"]) for row in rows),
    }


def _bound_file(root: Path, binding: dict[str, Any], label: str) -> Path:
    path = root / str(binding["path"])
    require(path.is_file(), f"Missing B1E-F {label}: {path}")
    require(sha256_file(path) == binding["sha256"], f"B1E-F {label} hash drift")
    return path


def _validate_top_scores(row: dict[str, Any]) -> None:
    ranked = row["top_100"]
    components = row["retriever_metadata"]["top_100_component_scores"]
    previous: tuple[float, str] | None = None
    for rank, detail in zip(ranked, components, strict=True):
        scores = [float(value) for value in detail["field_scores"]]
        require(all(math.isfinite(value) for value in scores), "B1E-F non-finite component score")
        aggregate = mean(sorted(scores, reverse=True)[:2])
        require(abs(float(rank["score"]) - aggregate) <= 1e-12, "B1E-F top-two score mismatch")
        pair = (-float(rank["score"]), str(rank["skill_id"]))
        require(previous is None or previous <= pair, "B1E-F Top-100 ordering/tie-break drift")
        previous = pair


def verify(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    payload, texts, prompts = _validate_preflight(root)
    output_root = root / RESULT_ROOT
    manifest_path = output_root / "manifest.json"
    manifest = read_json(manifest_path)
    require(manifest["state"] == "qwen_field_aware_completed_pending_user_result_review", "Unexpected B1E-F run state")
    require(manifest["runner_version"] == RUNNER_VERSION, "B1E-F runner version drift")
    require(manifest["method"] == {
        "retriever": "qwen-text-embedding-v4-field-aware",
        "representation": FIELD_COMPONENT_REPRESENTATION,
        "aggregation": "uniform_top_two",
        "field_aware": True,
        "reranking": False,
    }, "B1E-F method drift")
    require(manifest["thesis_result_writing"] is False, "B1E-F was improperly authorised to write the thesis")

    payload_path = _bound_file(root, manifest["payload"], "payload")
    require(payload_path == root / PREFLIGHT_ROOT / PAYLOAD_NAME, "B1E-F payload path drift")
    approval_path = _bound_file(root, manifest["authorisation"], "authorisation")
    approval = read_json(approval_path)
    require(approval["state"] == "explicitly_authorised_for_one_qwen_field_aware_v3_execution", "B1E-F approval state drift")
    require(approval["thesis_result_writing_authorised"] is False, "B1E-F approval permits thesis writing")
    require(int(approval["automatic_retries"]) == 0, "B1E-F approval permits retries")
    packet_path = root / PREFLIGHT_ROOT / PACKET_NAME
    packet = read_json(packet_path)
    require(
        approval["approved_packet"] == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "B1E-F authorisation/packet binding drift",
    )
    require(
        packet["payload"] == manifest["payload"] and packet["run_id"] == manifest["run_id"],
        "B1E-F packet/run binding drift",
    )

    rows_path = _bound_file(root, manifest["artifacts"]["rows"], "result rows")
    ledger_path = _bound_file(root, manifest["embedding_ledger"], "embedding ledger")
    rows = read_jsonl(rows_path)
    ledger = read_json(ledger_path)
    prompt_by_id = {str(prompt["prompt_id"]): prompt for prompt in prompts}
    require(len(prompt_by_id) == len(prompts) == 381, "B1E-F prompt population drift")
    require(Counter(prompt["stratum"] for prompt in prompts) == {"controlled": 243, "public_gold": 138}, "B1E-F stratum drift")
    require(len(rows) == int(manifest["artifacts"]["rows"]["rows"]) == 381, "B1E-F result-row count drift")

    seen: set[str] = set()
    by_stratum: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        prompt_id = str(row.get("prompt_id"))
        require(prompt_id in prompt_by_id and prompt_id not in seen, "B1E-F prompt coverage/uniqueness drift")
        seen.add(prompt_id)
        _validate_row(row, prompt_by_id[prompt_id])
        require(row["schema_version"] == RESULT_SCHEMA, "B1E-F result schema drift")
        _validate_top_scores(row)
        by_stratum[str(row["stratum"])].append(row)
    require(seen == set(prompt_by_id), "B1E-F strict prompt coverage drift")

    require(ledger["automatic_retries"] == 0, "B1E-F automatic retry occurred")
    require(ledger["cold_query_requests"] == 0 and ledger["query_external_text_submissions"] == 0, "B1E-F transmitted a query")
    require(ledger["reused_query_embeddings"] == 381, "B1E-F query-cache reuse drift")
    require(ledger["text_rows"] == int(payload["text_inventory"]["rows"]), "B1E-F inventory/ledger drift")
    require(ledger["cache_misses"] == ledger["document_cache_misses"] == ledger["external_text_submissions"], "B1E-F document cache accounting drift")
    for ledger_key, approval_key in (
        ("request_attempts", "maximum_request_attempts"),
        ("successful_api_calls", "maximum_successful_api_calls"),
        ("cache_misses", "maximum_new_cache_texts"),
        ("external_text_submissions", "maximum_external_text_submissions"),
        ("external_submission_proxy_tokens", "maximum_external_submission_proxy_tokens"),
        ("external_submission_utf8_bytes", "maximum_external_submission_utf8_bytes"),
    ):
        require(int(ledger[ledger_key]) <= int(approval[approval_key]), f"B1E-F approval cap exceeded: {ledger_key}")
    require(int(ledger["provider_usage"].get("prompt_tokens", 0)) <= int(approval["maximum_provider_prompt_tokens"]), "B1E-F provider-token ceiling exceeded")
    require(manifest["warm_replay"] == {"verified_conditions": 381}, "B1E-F warm-replay manifest drift")

    request_records = manifest["artifacts"]["request_records"]
    require(len(request_records) == 3 * int(ledger["request_attempts"]), "B1E-F request-record count drift")
    request_root = output_root / "request_records"
    actual_paths = {relative(path, root) for path in request_root.glob("*.json")}
    require(actual_paths == {str(item["path"]) for item in request_records}, "B1E-F request-record path drift")
    for item in request_records:
        _bound_file(root, item, "request record")

    # Recompute rankings locally from the exact component/query cache. This
    # establishes the scoring path without provider use or result mutation.
    cache = ExactEmbeddingCache(root / str(approval["cache_root"]))
    vectors = {str(text["text_id"]): cache.load(str(text["text"])) for text in texts}
    require(all(vector is not None for vector in vectors.values()), "B1E-F document cache coverage drift")
    replay = _score(payload, {key: value for key, value in vectors.items() if value is not None}, prompts, cache, float(manifest["document_embedding_seconds"]))
    replay_by_prompt = {str(row["prompt_id"]): row for row in replay}
    for row in rows:
        replica = replay_by_prompt[str(row["prompt_id"])]
        require(row["strict_gold_rank"] == replica["strict_gold_rank"], "B1E-F replay gold-rank drift")
        require(row["top_100"] == replica["top_100"], "B1E-F replay Top-100 drift")

    verification = {
        "schema_version": "rq2bv1-v3-qwen-field-aware-post-run-verification-v1",
        "state": "passed_local_post_run_integrity_verification",
        "run_manifest": {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)},
        "payload": manifest["payload"],
        "approval_receipt": manifest["authorisation"],
        "result_rows": {"path": relative(rows_path, root), "sha256": sha256_file(rows_path), "rows": len(rows)},
        "embedding_ledger": {"path": relative(ledger_path, root), "sha256": sha256_file(ledger_path)},
        "checks": {
            "strict_contract_rows_validated": len(rows),
            "candidate_library_skills": 2433,
            "field_components_per_candidate": 7,
            "unique_prompts_validated": len(prompt_by_id),
            "request_records_hash_validated": len(request_records),
            "query_external_text_submissions": 0,
            "automatic_retries": 0,
            "warm_replay_conditions": len(replay),
        },
        "network_calls": 0,
        "thesis_result_writing": False,
    }
    summary = {
        "schema_version": "rq2bv1-v3-qwen-field-aware-post-run-summary-v1",
        "state": "completed_pending_user_result_review",
        "scope": {
            "retriever": "qwen-text-embedding-v4-field-aware",
            "representation": FIELD_COMPONENT_REPRESENTATION,
            "aggregation": "uniform_top_two_of_seven_fields",
            "candidate_library_skills": 2433,
            "scored_prompts": 381,
            "strata": {"controlled": 243, "public_gold": 138},
            "field_aware": True,
            "reranking": False,
        },
        "quality_gate": verification["checks"],
        "provider_execution": {
            "request_attempts": int(ledger["request_attempts"]),
            "successful_api_calls": int(ledger["successful_api_calls"]),
            "automatic_retries": 0,
            "external_document_component_submissions": int(ledger["external_text_submissions"]),
            "external_query_submissions": 0,
            "reused_query_embeddings": 381,
            "provider_prompt_tokens": int(ledger["provider_usage"].get("prompt_tokens", 0)),
            "embedding_wall_seconds": float(ledger["elapsed_seconds"]),
        },
        "combined": _metrics(rows),
        "controlled": _metrics(by_stratum["controlled"]),
        "public_gold": _metrics(by_stratum["public_gold"]),
        "cost_and_latency": {
            "selector_visible_tokens": int(rows[0]["selector_visible_tokens"]),
            "one_time_document_embedding_seconds": float(manifest["document_embedding_seconds"]),
            "local_vector_search": _timing_summary([float(row["query_seconds"]) for row in rows]),
            "reused_primary_cold_query_embedding": _timing_summary([
                float(row["retriever_metadata"]["cold_query_embedding_seconds_reused_from_qwen_primary"])
                for row in rows
            ]),
        },
        "interpretation_boundary": "This is a separately registered secondary field-aware first-stage method. It does not alter the frozen 12-cell B1 primary matrix, test reranking, or settle RQ2b before all B2 conditions are completed and reviewed.",
        "thesis_result_writing": False,
    }
    return verification, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(args.verify, "Pass --verify for the local B1E-F verifier")
    root = args.root.resolve()
    output_root = root / RESULT_ROOT
    verification_path = output_root / VERIFICATION_NAME
    summary_path = output_root / SUMMARY_NAME
    require(not verification_path.exists() and not summary_path.exists(), "Refusing to overwrite B1E-F verification artifacts")
    verification, summary = verify(root)
    write_json_new(verification_path, verification)
    write_json_new(summary_path, summary)
    print({"state": verification["state"], "verification": relative(verification_path, root), "summary": relative(summary_path, root)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
