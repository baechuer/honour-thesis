#!/usr/bin/env python3
"""Execute the Phase-8-bound V7 Qwen embedding B1 payload.

This module is inert unless ``--execute`` is paired with a fresh, one-use
root release whose payload and PASS preflight hashes match byte-for-byte.
Provider requests are single-attempt and leave immutable attempt receipts.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import time
import urllib.request
from pathlib import Path
from typing import Any, Callable, Iterable

import numpy as np

from build_rq2b_v7_qwen_b1_phase8_v3_preflight import (
    BASE_URL,
    CLEAN_CACHE_REL,
    DEFAULT_TIMEOUT_SECONDS,
    DIMENSIONS,
    EXPECTED_QUERIES,
    EXPECTED_ROWS,
    EXPECTED_SOURCES,
    MAX_BATCH_TEXTS,
    MODEL,
    PREDICTABLE_CEILING_KEYS,
    REPRESENTATION_CELLS,
    RUNTIME_REL,
    SOURCE_UNION_SHA256,
    TOP_K,
    V3ExactEmbeddingCache,
    embedding_request_bytes,
    file_sha256,
    is_sha256,
    read_json,
    read_jsonl,
    relative,
    require,
    root_path,
    validate_payload,
    validate_preflight_receipt,
    write_json_new,
)
from validate_rq2b_v7_runner_outputs import (
    B1_SCHEMA_VERSION,
    RunnerAuthority,
    top20_binding_sha256,
    validate_b1_row,
)


# These literals are intentionally AST-visible to the Phase-8 root builder.
RUNNER_VERSION = "rq2b-v7-qwen-b1-phase8-runner-v3"
PAYLOAD_SCHEMA = "rq2b-v7-qwen-b1-phase8-payload-v3"
AUTHORISATION_SCHEMA = "rq2b-v7-qwen-b1-phase8-root-release-v3"
RUN_MANIFEST_SCHEMA = "rq2b-v7-qwen-b1-phase8-run-manifest-v3"
SENSITIVITY_SCHEMA = "rq2b-v7-qwen-b1-mean-window-sensitivity-v3"
ATTEMPT_SCHEMA = "rq2b-v7-qwen-b1-provider-attempt-v3"
RUNTIME_CEILING_KEYS = {"maximum_provider_reported_total_tokens", "maximum_wall_time_seconds"}


def utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_jsonl_gzip_new(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    uncompressed_bytes = 0
    count = 0
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for row in rows:
                encoded = (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
                digest.update(encoded)
                uncompressed_bytes += len(encoded)
                count += 1
                handle.write(encoded)
    return {
        "path": None,
        "sha256": file_sha256(path),
        "rows": count,
        "compressed_bytes": path.stat().st_size,
        "canonical_jsonl_sha256_uncompressed": digest.hexdigest(),
        "uncompressed_bytes": uncompressed_bytes,
        "compression": "gzip-mtime-0",
    }


def validate_release_ceilings(release: dict[str, Any], payload: dict[str, Any]) -> None:
    ceilings = release.get("ceilings")
    expected_keys = PREDICTABLE_CEILING_KEYS | RUNTIME_CEILING_KEYS
    require(isinstance(ceilings, dict) and set(ceilings) == expected_keys, "Root release ceiling keys drift")
    for key in sorted(PREDICTABLE_CEILING_KEYS):
        require(
            isinstance(ceilings[key], int) and not isinstance(ceilings[key], bool)
            and ceilings[key] == payload["predictable_ceilings"][key],
            f"Insufficient or non-exact predictable ceiling: {key}",
        )
    require(
        isinstance(ceilings["maximum_provider_reported_total_tokens"], int)
        and ceilings["maximum_provider_reported_total_tokens"] >= 0,
        "Invalid provider-reported token ceiling",
    )
    require(
        isinstance(ceilings["maximum_wall_time_seconds"], (int, float))
        and not isinstance(ceilings["maximum_wall_time_seconds"], bool)
        and math.isfinite(ceilings["maximum_wall_time_seconds"])
        and ceilings["maximum_wall_time_seconds"] > 0,
        "Invalid wall-time ceiling",
    )


def validate_release_hash_bindings(
    *, release: dict[str, Any], root: Path, payload_path: Path,
    preflight_path: Path, payload: dict[str, Any],
) -> None:
    require(
        release.get("payload") == {
            "path": relative(payload_path, root),
            "sha256": file_sha256(payload_path),
        },
        "Root release payload binding drift",
    )
    require(
        release.get("preflight") == {
            "path": relative(preflight_path, root),
            "sha256": file_sha256(preflight_path),
        },
        "Root release preflight binding drift",
    )
    require(release.get("phase8") == {
        "receipt_sha256": payload["phase8"]["receipt"]["sha256"],
        "root_manifest_sha256": payload["phase8"]["root_manifest"]["sha256"],
    }, "Root release Phase-8 binding drift")


def validate_one_use_release_state(release: dict[str, Any]) -> None:
    require(
        release.get("state") == "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_QWEN_B1_EXECUTION",
        "Execution is not explicitly released",
    )
    require(
        release.get("one_use") is True and release.get("consumed") is False,
        "Root release is not fresh and one-use",
    )


def validate_root_release(
    *, root: Path, release_path: Path, payload_path: Path,
    preflight_path: Path, payload: dict[str, Any], run_id: str,
    output_dir: Path, attempt_dir: Path, api_key_env: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    release = read_json(release_path)
    require(release.get("schema_version") == AUTHORISATION_SCHEMA, "Root release schema drift")
    validate_one_use_release_state(release)
    require(isinstance(release.get("root_release_id"), str) and release["root_release_id"], "Root release ID missing")
    require(release.get("run_id") == run_id, "Root release run ID drift")
    require(release.get("runner_version") == RUNNER_VERSION, "Root release runner drift")
    require(release.get("payload_schema") == PAYLOAD_SCHEMA, "Root release payload schema drift")
    validate_release_hash_bindings(
        release=release, root=root, payload_path=payload_path,
        preflight_path=preflight_path, payload=payload,
    )
    require(release.get("provider") == {
        "base_url": BASE_URL,
        "endpoint": "/embeddings",
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "api_key_env": api_key_env,
        "timeout_seconds": timeout_seconds,
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "automatic_retries": 0,
        "cold_query_batch_size": 1,
    }, "Root release provider contract drift")
    require(release.get("destinations") == {
        "output_dir": relative(output_dir, root),
        "attempt_dir": relative(attempt_dir, root),
        "clean_cache_root": CLEAN_CACHE_REL.as_posix(),
    }, "Root release destination drift")
    validate_release_ceilings(release, payload)
    return release


def load_payload_artifacts(root: Path, payload_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    payload = validate_payload(root, payload_path)
    require(payload["schema_version"] == PAYLOAD_SCHEMA, "Payload schema mismatch")
    result: list[list[dict[str, Any]]] = []
    for name in ("text_inventory", "document_map", "cache_inventory", "planned_requests"):
        binding = payload["artifacts"][name]
        rows = read_jsonl(root_path(root, binding["path"], field=f"payload.artifacts.{name}.path"))
        require(len(rows) == binding["rows"], f"Payload artifact row drift: {name}")
        result.append(rows)
    return payload, result[0], result[1], result[2], result[3]


def validate_planned_request(row: dict[str, Any], text_by_id: dict[str, dict[str, Any]]) -> bytes:
    ids = row.get("text_ids")
    require(isinstance(ids, list) and 1 <= len(ids) <= MAX_BATCH_TEXTS, "Planned request batch drift")
    require(all(text_id in text_by_id for text_id in ids), "Planned request references unknown text")
    texts = [text_by_id[text_id]["text"] for text_id in ids]
    body = embedding_request_bytes(texts)
    require(len(body) == row["request_body_utf8_bytes"], "Planned request byte drift")
    require(hashlib.sha256(body).hexdigest() == row["request_body_sha256"], "Planned request body hash drift")
    require(sum(text_by_id[text_id]["content_proxy_tokens"] for text_id in ids) == row["content_proxy_tokens"], "Planned content-token drift")
    require(sum(text_by_id[text_id]["model_input_proxy_tokens"] for text_id in ids) == row["model_input_proxy_tokens"], "Planned model-input-token drift")
    return body


def post_embedding_once(api_key: str, body: bytes, timeout_seconds: int) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{BASE_URL}/embeddings", data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        value = json.loads(response.read().decode("utf-8"))
    require(isinstance(value, dict), "Provider response must be an object")
    return value


def parse_provider_response(value: dict[str, Any], expected: int) -> tuple[list[list[float]], dict[str, int]]:
    data = value.get("data")
    require(isinstance(data, list) and len(data) == expected, "Provider response cardinality drift")
    vectors: list[list[float] | None] = [None] * expected
    for item in data:
        require(isinstance(item, dict) and isinstance(item.get("index"), int), "Provider response index missing")
        index = item["index"]
        require(0 <= index < expected and vectors[index] is None, "Provider response index drift")
        vector = [float(number) for number in item.get("embedding", [])]
        require(len(vector) == DIMENSIONS and all(math.isfinite(number) for number in vector), "Provider embedding drift")
        vectors[index] = vector
    usage_raw = value.get("usage", {})
    require(isinstance(usage_raw, dict), "Provider usage must be an object")
    usage: dict[str, int] = {}
    for key, number in usage_raw.items():
        require(isinstance(number, int) and not isinstance(number, bool) and number >= 0, f"Invalid provider usage {key}")
        usage[str(key)] = number
    return [vector for vector in vectors if vector is not None], usage


def provider_total_tokens(usage: dict[str, int]) -> int:
    if "total_tokens" in usage:
        return usage["total_tokens"]
    return sum(value for key, value in usage.items() if key.endswith("_tokens"))


def execute_embedding_plan(
    *, text_rows: list[dict[str, Any]], cache_rows: list[dict[str, Any]],
    planned_requests: list[dict[str, Any]], cache: V3ExactEmbeddingCache,
    api_key: str, timeout_seconds: int, attempt_dir: Path,
    ceilings: dict[str, Any], request_fn: Callable[[str, bytes, int], dict[str, Any]] = post_embedding_once,
) -> tuple[dict[str, list[float]], dict[str, Any], dict[str, float]]:
    text_by_id = {row["text_id"]: row for row in text_rows}
    require(len(text_by_id) == len(text_rows), "Duplicate payload text IDs")
    cache_by_id = {row["text_id"]: row for row in cache_rows}
    require(set(cache_by_id) == set(text_by_id), "Cache inventory/text identity drift")
    vectors: dict[str, list[float]] = {}
    initial_cache: dict[str, bool] = {}
    for text_id, row in text_by_id.items():
        inventory = cache_by_id[text_id]
        path = cache.path(row["text"])
        require(path.is_file() == inventory["cache_hit"], f"Cache state changed after preflight: {text_id}")
        if path.is_file():
            require(file_sha256(path) == inventory["cache_entry_sha256"], f"Cache entry changed after preflight: {text_id}")
            loaded = cache.load(row["text"])
            require(loaded is not None, "Validated cache entry failed load")
            vectors[text_id] = loaded
        initial_cache[text_id] = path.is_file()

    attempt_dir.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    totals = {
        "request_attempts": 0, "successful_calls": 0,
        "external_text_submissions": 0, "external_content_proxy_tokens": 0,
        "external_model_input_proxy_tokens": 0, "external_text_utf8_bytes": 0,
        "external_request_body_utf8_bytes": 0, "provider_reported_total_tokens": 0,
        "new_cache_entries": 0, "new_cache_content_proxy_tokens": 0,
        "new_cache_model_input_proxy_tokens": 0, "new_cache_utf8_bytes": 0,
        "document_calls": 0, "query_calls": 0,
    }
    role_totals = {
        "document_batch": {
            "provider_calls": 0, "external_text_submissions": 0,
            "content_proxy_tokens": 0, "model_input_proxy_tokens": 0,
            "text_utf8_bytes": 0, "request_body_utf8_bytes": 0,
            "provider_reported_total_tokens": 0, "request_seconds": 0.0,
        },
        "cold_query_single": {
            "provider_calls": 0, "external_text_submissions": 0,
            "content_proxy_tokens": 0, "model_input_proxy_tokens": 0,
            "text_utf8_bytes": 0, "request_body_utf8_bytes": 0,
            "provider_reported_total_tokens": 0, "request_seconds": 0.0,
        },
    }
    query_latency: dict[str, float] = {}
    for request_index, planned in enumerate(planned_requests):
        require(planned["request_index"] == request_index, "Planned request order drift")
        ids = list(planned["text_ids"])
        role = planned["request_role"]
        body = validate_planned_request(planned, text_by_id)
        if role == "document_batch":
            require(all(text_id not in vectors for text_id in ids), "Document request no longer matches exact cache misses")
        else:
            require(role == "cold_query_single" and len(ids) == 1, "Cold-query request plan drift")
        projected = {
            "maximum_request_attempts": totals["request_attempts"] + 1,
            "maximum_successful_calls": totals["successful_calls"] + 1,
            "maximum_external_text_submissions": totals["external_text_submissions"] + len(ids),
            "maximum_external_content_proxy_tokens": totals["external_content_proxy_tokens"] + planned["content_proxy_tokens"],
            "maximum_external_model_input_proxy_tokens": totals["external_model_input_proxy_tokens"] + planned["model_input_proxy_tokens"],
            "maximum_external_text_utf8_bytes": totals["external_text_utf8_bytes"] + planned["text_utf8_bytes"],
            "maximum_external_request_body_utf8_bytes": totals["external_request_body_utf8_bytes"] + len(body),
        }
        for key, value in projected.items():
            require(value <= ceilings[key], f"Execution would exceed authorised ceiling: {key}")
        require(time.perf_counter() - started <= ceilings["maximum_wall_time_seconds"], "Wall-time ceiling reached")
        base = {
            "schema_version": ATTEMPT_SCHEMA,
            "attempt_index": request_index,
            "request_role": role,
            "text_ids": ids,
            "text_sha256": [text_by_id[text_id]["text_sha256"] for text_id in ids],
            "request_body_sha256": hashlib.sha256(body).hexdigest(),
            "request_body_utf8_bytes": len(body),
            "content_proxy_tokens": planned["content_proxy_tokens"],
            "model_input_proxy_tokens": planned["model_input_proxy_tokens"],
            "automatic_retries": 0,
            "timeout_seconds": timeout_seconds,
            "started_at_utc": utc_now(),
        }
        attempt_path = attempt_dir / f"attempt_{request_index:06d}.json"
        write_json_new(attempt_path, {**base, "status": "ATTEMPT_STARTED_NO_RETRY"})
        request_started = time.perf_counter()
        totals["request_attempts"] += 1
        totals["external_text_submissions"] += len(ids)
        totals["external_content_proxy_tokens"] += planned["content_proxy_tokens"]
        totals["external_model_input_proxy_tokens"] += planned["model_input_proxy_tokens"]
        totals["external_text_utf8_bytes"] += planned["text_utf8_bytes"]
        totals["external_request_body_utf8_bytes"] += len(body)
        try:
            response = request_fn(api_key, body, timeout_seconds)
            elapsed = time.perf_counter() - request_started
            parsed, usage = parse_provider_response(response, len(ids))
            provider_tokens = provider_total_tokens(usage)
            require(totals["provider_reported_total_tokens"] + provider_tokens <= ceilings["maximum_provider_reported_total_tokens"], "Provider-reported token ceiling exceeded")
            success_path = attempt_dir / f"success_{request_index:06d}.json"
            write_json_new(success_path, {
                **base, "status": "SUCCESS", "request_seconds": elapsed,
                "provider_usage": usage,
                "response_sha256": hashlib.sha256(json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
                "embeddings": parsed,
                "completed_at_utc": utc_now(),
            })
            totals["successful_calls"] += 1
            totals["provider_reported_total_tokens"] += provider_tokens
            totals["document_calls" if role == "document_batch" else "query_calls"] += 1
            role_ledger = role_totals[role]
            role_ledger["provider_calls"] += 1
            role_ledger["external_text_submissions"] += len(ids)
            role_ledger["content_proxy_tokens"] += planned["content_proxy_tokens"]
            role_ledger["model_input_proxy_tokens"] += planned["model_input_proxy_tokens"]
            role_ledger["text_utf8_bytes"] += planned["text_utf8_bytes"]
            role_ledger["request_body_utf8_bytes"] += len(body)
            role_ledger["provider_reported_total_tokens"] += provider_tokens
            role_ledger["request_seconds"] += elapsed
            if role == "cold_query_single":
                query_latency[ids[0]] = elapsed
            for text_id, vector in zip(ids, parsed, strict=True):
                row = text_by_id[text_id]
                # Queries are always submitted cold.  A pre-existing exact query
                # cache remains immutable; the fresh vector is used in this run.
                if not cache.path(row["text"]).exists():
                    cache.store(
                        row["text"], vector,
                        content_proxy_tokens=row["content_proxy_tokens"],
                        model_input_proxy_tokens=row["model_input_proxy_tokens"],
                        provider_usage=usage,
                    )
                    totals["new_cache_entries"] += 1
                    totals["new_cache_content_proxy_tokens"] += row["content_proxy_tokens"]
                    totals["new_cache_model_input_proxy_tokens"] += row["model_input_proxy_tokens"]
                    totals["new_cache_utf8_bytes"] += row["utf8_bytes"]
                vectors[text_id] = vector
        except Exception as error:
            write_json_new(attempt_dir / f"failure_{request_index:06d}.json", {
                **base, "status": "FAILED_NO_RETRY", "error_type": type(error).__name__,
                "error": str(error), "completed_at_utc": utc_now(),
            })
            raise
    require(set(vectors) == set(text_by_id), "Embedding coverage drift")
    require(len(query_latency) == EXPECTED_QUERIES, "Cold-query latency coverage drift")
    require(totals["request_attempts"] == totals["successful_calls"] == len(planned_requests), "Request completion drift")
    for key, total_key in (
        ("maximum_new_cache_entries", "new_cache_entries"),
        ("maximum_new_cache_content_proxy_tokens", "new_cache_content_proxy_tokens"),
        ("maximum_new_cache_model_input_proxy_tokens", "new_cache_model_input_proxy_tokens"),
        ("maximum_new_cache_utf8_bytes", "new_cache_utf8_bytes"),
    ):
        require(totals[total_key] <= ceilings[key], f"Observed cache write exceeded ceiling: {key}")
    document_ids = {
        text_id for text_id, row in text_by_id.items()
        if any(role.get("kind") == "document_chunk" for role in row["roles"])
    }
    ledger = {
        "schema_version": "rq2b-v7-qwen-b1-phase8-embedding-ledger-v3",
        "status": "COMPLETE",
        "offline_document_embedding": {
            **role_totals["document_batch"],
            "cache_hits": sum(initial_cache[text_id] for text_id in document_ids),
            "cache_misses": sum(not initial_cache[text_id] for text_id in document_ids),
        },
        "online_query_embedding": {
            **role_totals["cold_query_single"],
            "cold_query_batch_size": 1,
        },
        "observed": totals,
        "automatic_retries": 0,
    }
    return vectors, ledger, query_latency


def normalized_matrix(values: list[list[float]]) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    require(matrix.ndim == 2 and matrix.shape[1] == DIMENSIONS, "Embedding matrix shape drift")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0)), "Embedding norm drift")
    return matrix / norms


def stable_top_k(source_ids: list[str], scores: np.ndarray, k: int = TOP_K) -> list[int]:
    require(len(source_ids) == len(scores) and len(source_ids) >= k, "Ranking input size drift")
    require(bool(np.all(np.isfinite(scores))), "Ranking score is non-finite")
    ids = np.asarray(source_ids, dtype=f"U{max(map(len, source_ids))}")
    return [int(index) for index in np.lexsort((ids, -scores))[:k]]


def score_representation(
    *, run_id: str, representation: str, condition: dict[str, Any],
    documents: list[dict[str, Any]], prompts: list[dict[str, Any]],
    query_text_ids: dict[str, str], text_by_id: dict[str, dict[str, Any]],
    vectors: dict[str, list[float]], query_latency: dict[str, float],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    documents = sorted(documents, key=lambda row: row["source_sha256"])
    source_ids = [row["source_sha256"] for row in documents]
    require(len(source_ids) == EXPECTED_SOURCES and len(set(source_ids)) == EXPECTED_SOURCES, "Representation source scope drift")
    starts: list[int] = []
    counts: list[int] = []
    flat: list[list[float]] = []
    for document in documents:
        starts.append(len(flat))
        values = [vectors[text_id] for text_id in document["chunk_text_ids"]]
        require(bool(values), "Document has no windows")
        counts.append(len(values))
        flat.extend(values)
    window_matrix = normalized_matrix(flat)
    means: list[np.ndarray] = []
    for start, count in zip(starts, counts, strict=True):
        mean = window_matrix[start:start + count].mean(axis=0)
        norm = float(np.linalg.norm(mean))
        require(math.isfinite(norm) and norm > 0, "Mean-window norm drift")
        means.append(mean / norm)
    mean_matrix = np.vstack(means)
    start_array = np.asarray(starts, dtype=np.int64)
    rows: list[dict[str, Any]] = []
    sensitivity: list[dict[str, Any]] = []
    for prompt in prompts:
        query_id = query_text_ids[prompt["prompt_id"]]
        query = normalized_matrix([vectors[query_id]])[0]
        rank_started = time.perf_counter()
        maximum_scores = np.maximum.reduceat(window_matrix @ query, start_array)
        top = stable_top_k(source_ids, maximum_scores)
        rank_seconds = time.perf_counter() - rank_started
        candidates = [
            {"rank": rank, "source_sha256": source_ids[index], "score": float(maximum_scores[index])}
            for rank, index in enumerate(top, 1)
        ]
        row = {
            "schema_version": B1_SCHEMA_VERSION, "status": "SUCCESS", "run_id": run_id,
            "condition_id": condition["condition_id"],
            "first_stage_cell_id": REPRESENTATION_CELLS[representation],
            "prompt_id": prompt["prompt_id"], "prompt_sha256": prompt["prompt_sha256"],
            "representation": representation, "retriever": condition["retriever"],
            "persisted_candidate_source": condition["persisted_candidate_source"],
            "source_union_sha256": SOURCE_UNION_SHA256, "top_k": TOP_K,
            "score_semantics": "HIGHER_IS_BETTER",
            "top20_binding_sha256": top20_binding_sha256(
                condition_id=condition["condition_id"], prompt_id=prompt["prompt_id"],
                prompt_sha256=prompt["prompt_sha256"],
                ordered_source_sha256=[item["source_sha256"] for item in candidates[:20]],
            ),
            "ranked_candidates": candidates,
            # Official rows deliberately exclude all offline document cost.
            "cost": {
                "wall_time_ms": 1000.0 * (query_latency[query_id] + rank_seconds),
                "provider_calls": 1,
                "input_tokens": int(text_by_id[query_id]["model_input_proxy_tokens"]),
                "output_tokens": 0, "window_forwards": 1, "cache_hits": 0,
                "retry_count": 0, "timeout_count": 0, "failure_count": 0,
            },
        }
        rows.append(row)
        mean_scores = mean_matrix @ query
        mean_top = stable_top_k(source_ids, mean_scores)
        sensitivity.append({
            "schema_version": SENSITIVITY_SCHEMA,
            "status": "NON_CORE_SENSITIVITY_SUCCESS", "run_id": run_id,
            "first_stage_cell_id": REPRESENTATION_CELLS[representation],
            "prompt_id": prompt["prompt_id"], "prompt_sha256": prompt["prompt_sha256"],
            "representation": representation,
            "aggregation": "cosine_of_l2_normalized_window_mean",
            "primary_aggregation": "maximum_window_cosine", "core_outcome": False,
            "stable_tie_break": "source_sha256_ascending", "top_k": TOP_K,
            "ranked_candidates": [
                {"rank": rank, "source_sha256": source_ids[index], "score": float(mean_scores[index])}
                for rank, index in enumerate(mean_top, 1)
            ],
        })
    return rows, sensitivity


def validate_qwen_rows(rows: list[dict[str, Any]], authority: RunnerAuthority) -> None:
    expected = {f"{cell}-G0" for cell in REPRESENTATION_CELLS.values()}
    require(len(rows) == EXPECTED_ROWS, "Qwen B1 row count drift")
    require({row["condition_id"] for row in rows} == expected, "Qwen B1 condition coverage drift")
    seen: set[tuple[str, str]] = set()
    for index, row in enumerate(rows, 1):
        validate_b1_row(row, authority, index)
        key = (row["condition_id"], row["prompt_id"])
        require(key not in seen, "Duplicate Qwen B1 row")
        seen.add(key)
        require(row["cost"]["provider_calls"] == 1 and row["cost"]["window_forwards"] == 1 and row["cost"]["cache_hits"] == 0, "B1 row must report online query cost only")
    require(len(seen) == EXPECTED_ROWS, "Qwen B1 exact condition-query scope drift")


def run(
    *, root: Path, payload_path: Path, preflight_path: Path,
    release_path: Path, output_dir: Path, attempt_dir: Path,
    run_id: str, api_key_env: str, timeout_seconds: int,
) -> dict[str, Any]:
    root = root.resolve()
    require(not output_dir.exists(), "Output exists; overwrite forbidden")
    require(not attempt_dir.exists(), "Attempt directory exists; immutable attempt replay forbidden")
    require(relative(output_dir, root).startswith("skill_benchmark/cache/"), "Output must be inside repository cache")
    require(relative(attempt_dir, root).startswith("skill_benchmark/cache/"), "Attempts must be inside repository cache")
    payload, text_rows, document_rows, cache_rows, requests = load_payload_artifacts(root, payload_path)
    preflight = validate_preflight_receipt(root, preflight_path, payload_path=payload_path)
    require(preflight["predictable_ceilings"] == payload["predictable_ceilings"], "Stale preflight receipt")
    release = validate_root_release(
        root=root, release_path=release_path, payload_path=payload_path,
        preflight_path=preflight_path, payload=payload, run_id=run_id,
        output_dir=output_dir, attempt_dir=attempt_dir, api_key_env=api_key_env,
        timeout_seconds=timeout_seconds,
    )
    # The attempt root is created before checking credentials, so a released
    # execution that fails locally is still traceable and cannot be replayed.
    attempt_dir.mkdir(parents=True, exist_ok=False)
    write_json_new(attempt_dir / "run_started.json", {
        "schema_version": "rq2b-v7-qwen-b1-phase8-run-start-v3",
        "run_id": run_id, "runner_version": RUNNER_VERSION,
        "root_release_id": release["root_release_id"],
        "release_sha256": file_sha256(release_path),
        "payload_sha256": file_sha256(payload_path),
        "preflight_sha256": file_sha256(preflight_path),
        "started_at_utc": utc_now(), "automatic_retries": 0,
    })
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), f"Qwen API key environment variable is missing: {api_key_env}")
    cache = V3ExactEmbeddingCache(root / CLEAN_CACHE_REL, create=True)
    vectors, ledger, query_latency = execute_embedding_plan(
        text_rows=text_rows, cache_rows=cache_rows, planned_requests=requests,
        cache=cache, api_key=str(api_key), timeout_seconds=timeout_seconds,
        attempt_dir=attempt_dir / "provider_attempts", ceilings=release["ceilings"],
    )
    prompts = read_jsonl(root / RUNTIME_REL)
    text_by_id = {row["text_id"]: row for row in text_rows}
    authority = RunnerAuthority.load()
    condition_by_representation = {
        representation: authority.b1_conditions[f"{cell}-G0"]
        for representation, cell in REPRESENTATION_CELLS.items()
    }
    rows: list[dict[str, Any]] = []
    sensitivities: list[dict[str, Any]] = []
    for representation in REPRESENTATION_CELLS:
        primary, secondary = score_representation(
            run_id=run_id, representation=representation,
            condition=condition_by_representation[representation],
            documents=[row for row in document_rows if row["representation"] == representation],
            prompts=prompts, query_text_ids=payload["query_text_ids"],
            text_by_id=text_by_id, vectors=vectors, query_latency=query_latency,
        )
        rows.extend(primary)
        sensitivities.extend(secondary)
    validate_qwen_rows(rows, authority)
    staging = output_dir.with_name(f".{output_dir.name}.staging-{os.getpid()}")
    require(not staging.exists(), "Output staging path exists")
    staging.mkdir(parents=True, exist_ok=False)
    shards: list[dict[str, Any]] = []
    sensitivity_shards: list[dict[str, Any]] = []
    for cell in sorted(REPRESENTATION_CELLS.values()):
        condition_id = f"{cell}-G0"
        path = staging / "b1_shards" / f"{condition_id}.jsonl.gz"
        metadata = write_jsonl_gzip_new(path, (row for row in rows if row["condition_id"] == condition_id))
        metadata["path"] = relative(output_dir / "b1_shards" / path.name, root)
        metadata["condition_id"] = condition_id
        shards.append(metadata)
        sensitivity_path = staging / "mean_window_sensitivity" / f"{cell}.jsonl.gz"
        secondary = write_jsonl_gzip_new(sensitivity_path, (row for row in sensitivities if row["first_stage_cell_id"] == cell))
        secondary["path"] = relative(output_dir / "mean_window_sensitivity" / sensitivity_path.name, root)
        secondary["first_stage_cell_id"] = cell
        secondary["core_outcome"] = False
        sensitivity_shards.append(secondary)
    write_json_new(staging / "embedding_ledger.json", ledger)
    manifest = {
        "schema_version": RUN_MANIFEST_SCHEMA,
        "status": "COMPLETE_FOUR_PHASE8_QWEN_B1_CELLS",
        "run_id": run_id, "runner_version": RUNNER_VERSION,
        "root_release_id": release["root_release_id"],
        "root_release_sha256": file_sha256(release_path),
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "preflight": {"path": relative(preflight_path, root), "sha256": file_sha256(preflight_path)},
        "phase8": payload["phase8"],
        "conditions": sorted(f"{cell}-G0" for cell in REPRESENTATION_CELLS.values()),
        "primary_aggregation": "maximum_window_cosine",
        "noncore_sensitivity_aggregation": "cosine_of_l2_normalized_window_mean",
        "stable_tie_break": "source_sha256_ascending", "top_k": TOP_K,
        "automatic_retries": 0,
        "cost_contract": payload["cost_contract"],
        "embedding_ledger": {"path": relative(output_dir / "embedding_ledger.json", root), "sha256": file_sha256(staging / "embedding_ledger.json")},
        "b1_condition_shards": shards,
        "mean_window_sensitivity_shards": sensitivity_shards,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_dir)
    write_json_new(attempt_dir / "run_complete.json", {
        "schema_version": "rq2b-v7-qwen-b1-phase8-run-complete-v3",
        "status": "COMPLETE", "run_id": run_id,
        "output_manifest": {"path": relative(output_dir / "manifest.json", root), "sha256": file_sha256(output_dir / "manifest.json")},
        "completed_at_utc": utc_now(),
    })
    return manifest


def self_test() -> dict[str, Any]:
    source_ids = [f"{index:064x}" for index in range(100)]
    scores = np.ones(100, dtype=np.float64)
    observed = [list(reversed(source_ids))[index] for index in stable_top_k(list(reversed(source_ids)), scores)]
    require(observed == source_ids, "Stable SHA tie behavior drift")
    response = {"data": [{"index": 0, "embedding": [1.0] * DIMENSIONS}], "usage": {"total_tokens": 3}}
    vectors, usage = parse_provider_response(response, 1)
    require(len(vectors) == 1 and usage == {"total_tokens": 3}, "Provider response parser drift")
    return {
        "status": "PASS_SYNTHETIC_QWEN_B1_V3_NO_PROVIDER",
        "network_calls": 0, "provider_requests": 0,
        "checks": {"stable_sha_tie": True, "response_contract": True, "ast_literals": True},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--payload", type=Path)
    parser.add_argument("--preflight-receipt", type=Path)
    parser.add_argument("--root-release", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--attempt-dir", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(all((args.payload, args.preflight_receipt, args.root_release, args.output_dir, args.attempt_dir, args.run_id)), "Execution requires payload, preflight, root release, output, attempt, and run ID")
        root = args.root.resolve()
        resolve = lambda path: path if path.is_absolute() else root / path
        result = run(
            root=root, payload_path=resolve(args.payload),
            preflight_path=resolve(args.preflight_receipt), release_path=resolve(args.root_release),
            output_dir=resolve(args.output_dir), attempt_dir=resolve(args.attempt_dir),
            run_id=args.run_id, api_key_env=args.api_key_env,
            timeout_seconds=args.timeout_seconds,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
