#!/usr/bin/env python3
"""Execute one separately authorised RQ2b V3 Qwen primary retrieval run.

The default action is a synthetic self-test.  ``--execute`` is fail-closed:
it needs a user-approved receipt whose packet hash, caps, model, endpoint,
output path, cache path, and runner dependency hashes exactly match the frozen
local preflight.  The primary method is max-chunk cosine only; field-aware
scoring and reranking are explicitly excluded from this runner.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path
from typing import Any

from rq2b_common import (
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    write_json_new,
    write_jsonl_new,
)
from rq2b_v11_contract import VERSION_ID as STRICT_VERSION_ID
from rq2b_v11_execution_contract import B1_SCHEMA, validate_b1_row
from run_rq2b_qwen import (
    BASE_URL,
    DIMENSIONS,
    MAX_BATCH_TEXTS,
    MODEL,
    ExactEmbeddingCache,
    embed_texts,
)


RUNNER_VERSION = "rq2bv1-v3-qwen-primary-runner-v1"
PREFLIGHT_ROOT = "skill_benchmark/rq2bv1/preflight/qwen_primary_v3"
PAYLOAD_NAME = "payload_manifest.json"
REPORT_NAME = "preflight_report.json"
CHECKPOINT_NAME = "preflight_checkpoint.json"
PACKET_NAME = "execution_approval_packet.json"
DEFAULT_AUTHORISATION = "skill_benchmark/rq2bv1/approvals/qwen_primary_v3_execution_authorisation.json"
RUN_ID = "rq2bv1-v3-qwen-primary-001"
RESULT_ROOT = "skill_benchmark/rq2bv1/results/qwen_primary_v3"
CACHE_ROOT = "skill_benchmark/cache/rq2bv1/embeddings"
TIMEOUT_SECONDS = 120
REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
)


def _path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _execution_packet(root: Path) -> tuple[Path, dict[str, Any]]:
    packet_path = root / PREFLIGHT_ROOT / PACKET_NAME
    require(packet_path.is_file(), f"Qwen V3 execution packet missing: {packet_path}")
    packet = read_json(packet_path)
    require(
        packet.get("schema_version") == "rq2bv1-v3-qwen-primary-execution-approval-packet-v1",
        "Qwen V3 execution packet schema mismatch",
    )
    require(
        packet.get("state") == "awaiting_explicit_external_transfer_authorisation",
        "Qwen V3 execution packet is not awaiting authorisation",
    )
    return packet_path, packet


def _validate_preflight(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    preflight_root = root / PREFLIGHT_ROOT
    checkpoint_path = preflight_root / CHECKPOINT_NAME
    report_path = preflight_root / REPORT_NAME
    payload_path = preflight_root / PAYLOAD_NAME
    require(checkpoint_path.is_file() and report_path.is_file() and payload_path.is_file(), "Qwen V3 preflight artefacts are incomplete")
    checkpoint = read_json(checkpoint_path)
    report = read_json(report_path)
    payload = read_json(payload_path)
    require(
        checkpoint.get("state") == "qwen_primary_preflight_frozen_external_authorisation_required",
        "Qwen V3 preflight checkpoint state mismatch",
    )
    require(checkpoint.get("report", {}).get("sha256") == sha256_file(report_path), "Qwen V3 preflight report hash drift")
    require(checkpoint.get("payload", {}).get("sha256") == sha256_file(payload_path), "Qwen V3 payload hash drift")
    require(
        report.get("state") == "preflight_passed_no_network_no_scoring_external_authorisation_required",
        "Qwen V3 preflight report state mismatch",
    )
    require(
        payload.get("schema_version") == "rq2bv1-v3-qwen-primary-payload-v1"
        and payload.get("state") == "sealed_not_executed",
        "Qwen V3 payload state/schema mismatch",
    )
    require(payload.get("base_url") == BASE_URL and payload.get("model") == MODEL and payload.get("dimensions") == DIMENSIONS, "Qwen V3 model contract drift")
    population = payload.get("strict_population", {})
    require(
        population == {
            "candidate_library_skills": 2433,
            "strict_prompts": 381,
            "representations": list(REPRESENTATIONS),
            "expected_primary_result_rows": 1524,
        },
        "Qwen V3 strict population drift",
    )
    inventory_path = _path(root, payload["text_inventory"]["path"])
    require(sha256_file(inventory_path) == payload["text_inventory"]["sha256"], "Qwen V3 text inventory hash drift")
    text_rows = read_jsonl(inventory_path)
    require(len(text_rows) == int(payload["text_inventory"]["rows"]), "Qwen V3 text inventory count drift")
    text_by_id = {str(row["text_id"]): row for row in text_rows}
    require(len(text_by_id) == len(text_rows), "Qwen V3 text IDs are not unique")
    for text_id, row in text_by_id.items():
        require(set(row) == {"schema_version", "text_id", "text_sha256", "text", "utf8_bytes", "local_proxy_tokens", "roles"}, f"Qwen V3 text row schema drift: {text_id}")
        require(row["schema_version"] == "rq2bv1-qwen-primary-text-v1", f"Qwen V3 text schema version drift: {text_id}")
        require(row["text_id"] == text_id == row["text_sha256"] == sha256_text(row["text"]), f"Qwen V3 text digest drift: {text_id}")
        require(int(row["utf8_bytes"]) == len(row["text"].encode("utf-8")), f"Qwen V3 text byte count drift: {text_id}")
        require(isinstance(row["roles"], list) and bool(row["roles"]), f"Qwen V3 text roles missing: {text_id}")
    require(set(payload.get("documents", {})) == set(REPRESENTATIONS), "Qwen V3 representation payload map drift")
    for representation in REPRESENTATIONS:
        documents = payload["documents"][representation]
        require(len(documents) == 2433, f"Qwen V3 document count drift: {representation}")
        skill_ids = [str(document["skill_id"]) for document in documents]
        require(len(skill_ids) == len(set(skill_ids)), f"Qwen V3 duplicate candidate ID: {representation}")
        for document in documents:
            chunks = document.get("chunk_text_ids")
            require(isinstance(chunks, list) and bool(chunks), f"Qwen V3 document has no chunks: {representation}:{document.get('skill_id')}")
            require(all(chunk_id in text_by_id for chunk_id in chunks), f"Qwen V3 document chunk absent from inventory: {representation}:{document.get('skill_id')}")
            require(len(chunks) == len(document.get("chunks", [])), f"Qwen V3 chunk metadata length drift: {representation}:{document.get('skill_id')}")
            for chunk in document["chunks"]:
                require(int(chunk["token_count"]) <= int(payload["chunk_tokens"]), f"Qwen V3 chunk token ceiling exceeded: {representation}:{document.get('skill_id')}")
    query_text_ids = payload.get("query_text_ids")
    require(isinstance(query_text_ids, dict) and len(query_text_ids) == 381, "Qwen V3 query map drift")
    require(all(text_id in text_by_id for text_id in query_text_ids.values()), "Qwen V3 query absent from text inventory")
    return payload, text_rows, report


def _validate_authorisation(root: Path, authorisation_path: Path, packet_path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    require(authorisation_path.is_file(), "Qwen V3 external execution is not authorised: receipt is absent")
    authorisation = read_json(authorisation_path)
    require(
        authorisation.get("schema_version") == "rq2bv1-v3-qwen-primary-execution-authorisation-v1",
        "Qwen V3 authorisation schema mismatch",
    )
    require(
        authorisation.get("state") == "explicitly_authorised_for_one_qwen_primary_v3_execution",
        "Qwen V3 authorisation state mismatch",
    )
    require(authorisation.get("approved_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "Qwen V3 authorisation packet binding mismatch")
    for key in ("run_id", "output_dir", "cache_root", "base_url", "model", "dimensions", "timeout_seconds", "automatic_retries"):
        require(authorisation.get(key) == packet.get(key), f"Qwen V3 authorisation mismatch: {key}")
    for key in (
        "maximum_new_cache_texts",
        "maximum_new_cache_proxy_tokens",
        "maximum_new_cache_utf8_bytes",
        "maximum_external_text_submissions",
        "maximum_external_submission_proxy_tokens",
        "maximum_external_submission_utf8_bytes",
        "maximum_request_attempts",
        "maximum_successful_api_calls",
        "cold_query_requests",
    ):
        require(authorisation.get(key) == packet.get(key), f"Qwen V3 authorisation cap mismatch: {key}")
    require(authorisation.get("thesis_result_writing_authorised") is False, "Qwen V3 authorisation cannot write thesis results")
    expected_scripts = packet.get("execution_scripts")
    require(authorisation.get("execution_scripts") == expected_scripts, "Qwen V3 authorisation script list mismatch")
    for script in expected_scripts:
        path = _path(root, script["path"])
        require(path.is_file() and sha256_file(path) == script["sha256"], f"Qwen V3 execution script hash drift: {script['path']}")
    return authorisation


def _timing_maps(text_rows: list[dict[str, Any]], ledger: dict[str, Any]) -> tuple[dict[str, float], dict[str, float]]:
    text_by_id = {str(row["text_id"]): row for row in text_rows}
    document_seconds = {representation: 0.0 for representation in REPRESENTATIONS}
    query_seconds: dict[str, float] = {}
    for record in ledger["request_records"]:
        request_role = record["request_role"]
        for timing in record["text_timings"]:
            text_id = str(timing["text_id"])
            seconds = float(timing["allocated_request_seconds"])
            roles = text_by_id[text_id]["roles"]
            if request_role == "document_batch":
                document_roles = [role for role in roles if role["kind"] == "document_chunk"]
                require(bool(document_roles), f"Document request has no document role: {text_id}")
                for role in document_roles:
                    document_seconds[str(role["representation"])] += seconds / len(document_roles)
            elif request_role == "cold_query_single":
                query_roles = [role for role in roles if role["kind"] == "query"]
                require(len(query_roles) == 1, f"Cold query request role mismatch: {text_id}")
                query_seconds[text_id] = seconds
            else:
                raise ValueError(f"Unknown Qwen V3 request role: {request_role}")
    return document_seconds, query_seconds


def _primary_row(
    prompt: dict[str, Any],
    ranking: list[tuple[str, float]],
    *,
    representation: str,
    search_seconds: float,
    selector_tokens: int,
    document_embedding_seconds: float,
    cold_query_embedding_seconds: float,
    document_chunks: int,
) -> dict[str, Any]:
    require(len(ranking) == 2433, "Qwen V3 ranking candidate count mismatch")
    rank_by_id = {skill_id: index for index, (skill_id, _) in enumerate(ranking, start=1)}
    gold_rank = int(rank_by_id[prompt["gold_skill"]])
    top100 = ranking[:100]
    row = {
        "schema_version": B1_SCHEMA,
        "version_id": STRICT_VERSION_ID,
        "runner_version": RUNNER_VERSION,
        "retriever": "qwen-text-embedding-v4",
        "representation": representation,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": gold_rank,
        "strict_hit_at_1": int(gold_rank == 1),
        "strict_recall_at_5": int(gold_rank <= 5),
        "strict_recall_at_20": int(gold_rank <= 20),
        "strict_recall_at_50": int(gold_rank <= 50),
        "strict_recall_at_100": int(gold_rank <= 100),
        "strict_mrr_at_10": 0.0 if gold_rank > 10 else 1.0 / gold_rank,
        "top_5_skill_ids": [skill_id for skill_id, _ in ranking[:5]],
        "top_20_skill_ids": [skill_id for skill_id, _ in ranking[:20]],
        "top_50_skill_ids": [skill_id for skill_id, _ in ranking[:50]],
        "top_100": [
            {"rank": index, "skill_id": skill_id, "score": float(score)}
            for index, (skill_id, score) in enumerate(top100, start=1)
        ],
        "query_seconds": float(search_seconds),
        "selector_visible_tokens": int(selector_tokens),
        "one_time_document_embedding_or_index_seconds": float(document_embedding_seconds),
        "retriever_metadata": {
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "document_aggregation": "maximum_chunk_cosine",
            "document_chunks": int(document_chunks),
            "cold_query_embedding_seconds": float(cold_query_embedding_seconds),
        },
    }
    validate_b1_row(row, prompt, f"qwen-v3:{representation}:{prompt['prompt_id']}")
    return row


def score_primary(
    payload: dict[str, Any],
    vectors: dict[str, list[float]],
    prompts: list[dict[str, Any]],
    *,
    document_embedding_seconds: dict[str, float],
    query_embedding_seconds: dict[str, float],
) -> list[dict[str, Any]]:
    import numpy as np

    prompt_by_id = {str(prompt["prompt_id"]): prompt for prompt in prompts}
    require(len(prompt_by_id) == 381, "Qwen V3 prompt identity drift")
    query_vectors: dict[str, Any] = {}
    for prompt_id, text_id in payload["query_text_ids"].items():
        vector = np.asarray(vectors[text_id], dtype=np.float64)
        norm = float(np.linalg.norm(vector))
        require(math.isfinite(norm) and norm > 0.0, f"Invalid Qwen V3 query vector: {prompt_id}")
        query_vectors[prompt_id] = vector / norm
    rows: list[dict[str, Any]] = []
    for representation in REPRESENTATIONS:
        documents = payload["documents"][representation]
        skill_ids = [str(document["skill_id"]) for document in documents]
        require(len(skill_ids) == len(set(skill_ids)) == 2433, f"Qwen V3 document identities drift: {representation}")
        starts: list[int] = []
        counts: list[int] = []
        all_chunk_vectors: list[list[float]] = []
        for document in documents:
            starts.append(len(all_chunk_vectors))
            chunk_vectors = [vectors[text_id] for text_id in document["chunk_text_ids"]]
            require(bool(chunk_vectors), f"Qwen V3 document vector missing: {representation}:{document['skill_id']}")
            counts.append(len(chunk_vectors))
            all_chunk_vectors.extend(chunk_vectors)
        chunk_matrix = np.asarray(all_chunk_vectors, dtype=np.float64)
        norms = np.linalg.norm(chunk_matrix, axis=1, keepdims=True)
        require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), f"Invalid Qwen V3 document vectors: {representation}")
        chunk_matrix = chunk_matrix / norms
        starts_array = np.asarray(starts, dtype=np.int64)
        selector_tokens = sum(int(document["selector_local_proxy_tokens"]) for document in documents)
        for prompt_id, query_vector in query_vectors.items():
            started = time.perf_counter()
            scores = np.maximum.reduceat(chunk_matrix @ query_vector, starts_array)
            ranking = list(zip(skill_ids, (float(score) for score in scores), strict=True))
            ranking.sort(key=lambda item: (-item[1], item[0]))
            search_seconds = time.perf_counter() - started
            row = _primary_row(
                prompt_by_id[prompt_id],
                ranking,
                representation=representation,
                search_seconds=search_seconds,
                selector_tokens=selector_tokens,
                document_embedding_seconds=float(document_embedding_seconds[representation]),
                cold_query_embedding_seconds=float(query_embedding_seconds[payload["query_text_ids"][prompt_id]]),
                document_chunks=len(all_chunk_vectors),
            )
            rows.append(row)
    require(len(rows) == 1524, "Qwen V3 primary result row count mismatch")
    return rows


def _warm_replay(
    payload: dict[str, Any],
    cache: ExactEmbeddingCache,
    text_rows: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    *,
    document_embedding_seconds: dict[str, float],
    query_embedding_seconds: dict[str, float],
) -> dict[str, Any]:
    warm_started = time.perf_counter()
    vectors = {str(row["text_id"]): cache.load(row["text"]) for row in text_rows}
    require(all(vector is not None for vector in vectors.values()), "Qwen V3 warm replay cache coverage is incomplete")
    replay_rows = score_primary(
        payload,
        {text_id: vector for text_id, vector in vectors.items() if vector is not None},
        prompts,
        document_embedding_seconds=document_embedding_seconds,
        query_embedding_seconds=query_embedding_seconds,
    )
    expected = {(row["representation"], row["prompt_id"]): row for row in rows}
    actual = {(row["representation"], row["prompt_id"]): row for row in replay_rows}
    require(set(actual) == set(expected), "Qwen V3 warm replay condition coverage drift")
    for key in expected:
        require(
            [entry["skill_id"] for entry in actual[key]["top_100"]]
            == [entry["skill_id"] for entry in expected[key]["top_100"]],
            f"Qwen V3 warm replay ranking mismatch: {key}",
        )
        require(actual[key]["strict_gold_rank"] == expected[key]["strict_gold_rank"], f"Qwen V3 warm replay gold-rank mismatch: {key}")
    return {"verified_conditions": len(replay_rows), "elapsed_seconds": time.perf_counter() - warm_started}


def run(root: Path, authorisation_path: Path, api_key_env: str) -> dict[str, Any]:
    payload, text_rows, report = _validate_preflight(root)
    packet_path, packet = _execution_packet(root)
    authorisation = _validate_authorisation(root, authorisation_path, packet_path, packet)
    require(report["execution_packet"] == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "Qwen V3 preflight/packet binding drift")
    output_root = root / str(packet["output_dir"])
    staging = output_root.with_name(f".{output_root.name}.staging")
    require(not output_root.exists() and not staging.exists(), "Refusing to overwrite or resume a Qwen V3 scientific run")
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), f"Qwen API key environment variable is missing: {api_key_env}")
    staging.mkdir(parents=True, exist_ok=False)
    run_started = {
        "schema_version": "rq2bv1-v3-qwen-primary-run-start-v1",
        "run_id": packet["run_id"],
        "payload": {"path": relative(root / PREFLIGHT_ROOT / PAYLOAD_NAME, root), "sha256": sha256_file(root / PREFLIGHT_ROOT / PAYLOAD_NAME)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
        "automatic_retries": 0,
        "network_calls_before_start": 0,
    }
    write_json_new(staging / "run_started.json", run_started)
    progress_root = staging / "request_records"
    progress_root.mkdir(parents=False, exist_ok=False)
    cache = ExactEmbeddingCache(root / str(packet["cache_root"]))
    vectors, embedding_ledger = embed_texts(
        text_rows,
        cache=cache,
        api_key=api_key,
        authorisation={
            "maximum_new_texts": int(authorisation["maximum_new_cache_texts"]),
            "maximum_successful_calls": int(authorisation["maximum_successful_api_calls"]),
            "maximum_request_attempts": int(authorisation["maximum_request_attempts"]),
            "maximum_local_proxy_tokens": int(authorisation["maximum_new_cache_proxy_tokens"]),
            "maximum_new_utf8_bytes": int(authorisation["maximum_new_cache_utf8_bytes"]),
            "maximum_external_text_submissions": int(authorisation["maximum_external_text_submissions"]),
            "maximum_external_submission_proxy_tokens": int(authorisation["maximum_external_submission_proxy_tokens"]),
            "maximum_external_submission_utf8_bytes": int(authorisation["maximum_external_submission_utf8_bytes"]),
            "maximum_cold_query_requests": int(authorisation["cold_query_requests"]),
        },
        timeout_seconds=int(authorisation["timeout_seconds"]),
        progress_root=progress_root,
    )
    require(embedding_ledger["automatic_retries"] == 0, "Qwen V3 runner used automatic retries")
    require(embedding_ledger["request_attempts"] <= int(authorisation["maximum_request_attempts"]), "Qwen V3 request attempt cap exceeded")
    require(embedding_ledger["successful_api_calls"] <= int(authorisation["maximum_successful_api_calls"]), "Qwen V3 API call cap exceeded")
    document_embedding_seconds, query_embedding_seconds = _timing_maps(text_rows, embedding_ledger)
    require(set(query_embedding_seconds) == set(payload["query_text_ids"].values()), "Qwen V3 cold query timing coverage drift")
    prompts_path = _path(root, payload["prompt_artifact"]["path"])
    require(sha256_file(prompts_path) == payload["prompt_artifact"]["sha256"], "Qwen V3 strict prompt artifact drift")
    prompts = read_jsonl(prompts_path)
    rows = score_primary(
        payload,
        vectors,
        prompts,
        document_embedding_seconds=document_embedding_seconds,
        query_embedding_seconds=query_embedding_seconds,
    )
    warm = _warm_replay(
        payload,
        cache,
        text_rows,
        prompts,
        rows,
        document_embedding_seconds=document_embedding_seconds,
        query_embedding_seconds=query_embedding_seconds,
    )
    rows_path = staging / "qwen_primary_strict_results.jsonl"
    ledger_path = staging / "embedding_ledger.json"
    write_jsonl_new(rows_path, rows)
    write_json_new(ledger_path, embedding_ledger)
    manifest = {
        "schema_version": "rq2bv1-v3-qwen-primary-run-manifest-v1",
        "state": "qwen_primary_completed_pending_user_result_review",
        "run_id": packet["run_id"],
        "runner_version": RUNNER_VERSION,
        "method": {
            "retriever": "qwen-text-embedding-v4",
            "document_aggregation": "maximum_chunk_cosine",
            "field_aware": False,
            "reranking": False,
        },
        "payload": run_started["payload"],
        "authorisation": run_started["authorisation"],
        "embedding_ledger": {
            "path": relative(output_root / ledger_path.name, root),
            "sha256": sha256_file(ledger_path),
            "cache_hits": embedding_ledger["cache_hits"],
            "cache_misses": embedding_ledger["cache_misses"],
            "document_cache_hits": embedding_ledger["document_cache_hits"],
            "document_cache_misses": embedding_ledger["document_cache_misses"],
            "request_attempts": embedding_ledger["request_attempts"],
            "successful_api_calls": embedding_ledger["successful_api_calls"],
            "elapsed_seconds": embedding_ledger["elapsed_seconds"],
        },
        "document_embedding_seconds_by_representation": document_embedding_seconds,
        "warm_replay": warm,
        "artifacts": {
            "rows": {"path": relative(output_root / rows_path.name, root), "sha256": sha256_file(rows_path), "rows": len(rows)},
            "embedding_ledger": {"path": relative(output_root / ledger_path.name, root), "sha256": sha256_file(ledger_path)},
            "run_started": {"path": relative(output_root / "run_started.json", root), "sha256": sha256_file(staging / "run_started.json")},
            "request_records": [
                {"path": relative(output_root / "request_records" / item.name, root), "sha256": sha256_file(item)}
                for item in sorted(progress_root.glob("*.json"))
            ],
        },
        "network_calls": embedding_ledger["successful_api_calls"],
        "thesis_result_writing": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.rename(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    import numpy as np

    query = np.asarray([1.0, 0.0] + [0.0] * (DIMENSIONS - 2), dtype=np.float64)
    document_a = np.asarray([1.0, 0.0] + [0.0] * (DIMENSIONS - 2), dtype=np.float64)
    document_b = np.asarray([0.0, 1.0] + [0.0] * (DIMENSIONS - 2), dtype=np.float64)
    score_a = float((document_a / np.linalg.norm(document_a)) @ (query / np.linalg.norm(query)))
    score_b = float((document_b / np.linalg.norm(document_b)) @ (query / np.linalg.norm(query)))
    require(score_a > score_b, "Qwen V3 max-cosine self-test failed")
    return {
        "schema_version": "rq2bv1-v3-qwen-primary-runner-self-test-v1",
        "state": "self_test_passed_no_external_call",
        "network_calls": 0,
        "scientific_retrieval_or_reranking": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorisation", type=Path, default=Path(DEFAULT_AUTHORISATION))
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    args = parser.parse_args()
    require(args.self_test != args.execute, "choose exactly one of --self-test or --execute")
    root = args.root.resolve()
    result = self_test() if args.self_test else run(root, _path(root, args.authorisation), args.api_key_env)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
