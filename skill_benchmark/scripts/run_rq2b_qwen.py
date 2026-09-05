#!/usr/bin/env python3
"""Run authorised RQ2b Qwen max-chunk retrieval with exact-text caching."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    sha256_text,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    version_root,
    write_json_new,
    write_jsonl_new,
)
from rq2b_chunking import CHUNKER_VERSION
from run_rq2b_bm25 import annotate_unresolved_public_equivalents, rank_row


RUNNER_VERSION = "rq2b-qwen-max-chunk-runner-v1"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
MODEL = "text-embedding-v4"
DIMENSIONS = 1024
MAX_BATCH_TEXTS = 10


def l2_normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    require(norm > 0.0 and math.isfinite(norm), "Embedding vector has zero or invalid norm")
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    require(len(left) == len(right) == DIMENSIONS, "Qwen vector dimension mismatch")
    normalized_left = l2_normalize(left)
    normalized_right = l2_normalize(right)
    return sum(a * b for a, b in zip(normalized_left, normalized_right, strict=True))


def document_scores(
    query_vector: list[float],
    chunk_vectors: list[list[float]],
) -> tuple[float, int, float]:
    require(bool(chunk_vectors), "Document has no chunk vectors")
    chunk_scores = [cosine(query_vector, vector) for vector in chunk_vectors]
    winning_index = max(range(len(chunk_scores)), key=lambda index: (chunk_scores[index], -index))
    normalized_chunks = [l2_normalize(vector) for vector in chunk_vectors]
    mean_vector = [
        sum(vector[dimension] for vector in normalized_chunks) / len(normalized_chunks)
        for dimension in range(DIMENSIONS)
    ]
    mean_score = cosine(query_vector, mean_vector)
    return chunk_scores[winning_index], winning_index, mean_score


def cache_key(text: str) -> str:
    return sha256_json(
        {
            "base_url": BASE_URL,
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "chunker_version": CHUNKER_VERSION,
            "text_sha256": sha256_text(text),
        }
    )


class ExactEmbeddingCache:
    def __init__(self, root: Path) -> None:
        self.root = root / "qwen" / MODEL / str(DIMENSIONS)
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, text: str) -> Path:
        return self.root / f"{cache_key(text)}.json"

    def load(self, text: str) -> list[float] | None:
        path = self.path(text)
        if not path.exists():
            return None
        payload = read_json(path)
        require(payload.get("schema_version") == "rq2b-qwen-embedding-cache-v1", f"Cache schema mismatch: {path}")
        require(payload.get("base_url") == BASE_URL, f"Cache endpoint mismatch: {path}")
        require(payload.get("model") == MODEL, f"Cache model mismatch: {path}")
        require(payload.get("dimensions") == DIMENSIONS, f"Cache dimensions mismatch: {path}")
        require(payload.get("chunker_version") == CHUNKER_VERSION, f"Cache chunker mismatch: {path}")
        require(payload.get("text_sha256") == sha256_text(text), f"Cache text mismatch: {path}")
        vector = [float(value) for value in payload.get("embedding", [])]
        require(len(vector) == DIMENSIONS, f"Cache vector dimension mismatch: {path}")
        require(all(math.isfinite(value) for value in vector), f"Cache vector contains non-finite values: {path}")
        return vector

    def store(
        self,
        text: str,
        vector: list[float],
        *,
        local_proxy_tokens: int,
        provider_usage: dict[str, Any],
    ) -> None:
        path = self.path(text)
        require(not path.exists(), f"Refusing to overwrite Qwen cache entry: {path}")
        write_json_new(
            path,
            {
                "schema_version": "rq2b-qwen-embedding-cache-v1",
                "base_url": BASE_URL,
                "model": MODEL,
                "dimensions": DIMENSIONS,
                "chunker_version": CHUNKER_VERSION,
                "text_sha256": sha256_text(text),
                "local_proxy_tokens": local_proxy_tokens,
                "provider_usage": provider_usage,
                "embedding": vector,
            },
        )


def post_embedding_once(api_key: str, texts: list[str], timeout_seconds: int) -> dict[str, Any]:
    require(1 <= len(texts) <= MAX_BATCH_TEXTS, "Qwen request batch size is outside 1-10")
    payload = {
        "model": MODEL,
        "input": texts,
        "dimensions": DIMENSIONS,
        "encoding_format": "float",
    }
    request = urllib.request.Request(
        f"{BASE_URL}/embeddings",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        value = json.loads(response.read().decode("utf-8"))
    require(isinstance(value, dict), "Qwen response is not an object")
    return value


def validate_authorisation(
    path: Path,
    payload_manifest_path: Path,
    *,
    root: Path,
    run_id: str,
    output_dir: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    require(path.exists(), f"Qwen execution authorisation missing: {path}")
    authorisation = read_json(path)
    require(authorisation.get("schema_version") == "rq2b-qwen-execution-authorisation-v1", "Qwen authorisation schema mismatch")
    require(authorisation.get("state") == "explicitly_authorised_for_one_execution", "Qwen execution is not authorised")
    require(authorisation.get("base_url") == BASE_URL, "Qwen authorised endpoint mismatch")
    require(authorisation.get("model") == MODEL, "Qwen authorised model mismatch")
    require(authorisation.get("dimensions") == DIMENSIONS, "Qwen authorised dimensions mismatch")
    require(
        authorisation.get("payload_manifest_sha256") == sha256_file(payload_manifest_path),
        "Qwen payload manifest is not the authorised payload",
    )
    require(authorisation.get("automatic_retries") == 0, "Qwen authorisation must forbid retries")
    require(authorisation.get("run_id") == run_id, "Qwen authorised run ID mismatch")
    require(authorisation.get("output_dir") == relative(output_dir, root), "Qwen authorised output directory mismatch")
    require(authorisation.get("timeout_seconds") == timeout_seconds, "Qwen authorised timeout mismatch")
    for key in (
        "maximum_new_texts",
        "maximum_request_attempts",
        "maximum_successful_calls",
        "maximum_local_proxy_tokens",
        "maximum_new_utf8_bytes",
        "maximum_external_text_submissions",
        "maximum_external_submission_proxy_tokens",
        "maximum_external_submission_utf8_bytes",
        "maximum_cold_query_requests",
    ):
        require(isinstance(authorisation.get(key), int) and authorisation[key] >= 0, f"Qwen authorisation lacks {key}")
    require(
        authorisation.get("cold_query_latency_measurement") is True,
        "Qwen authorisation must require cold query-latency measurement",
    )
    require(
        authorisation.get("cold_query_batch_size") == 1,
        "Qwen cold query-latency batch size must be one",
    )
    return authorisation


def has_text_role(row: dict[str, Any], kind: str) -> bool:
    return any(role.get("kind") == kind for role in row["roles"])


def allocated_text_timings(
    batch: list[dict[str, Any]],
    request_seconds: float,
) -> list[dict[str, Any]]:
    require(bool(batch), "Cannot allocate an empty Qwen request")
    require(math.isfinite(request_seconds) and request_seconds >= 0.0, "Invalid Qwen request time")
    weights = [max(1, int(row["local_proxy_tokens"])) for row in batch]
    total_weight = sum(weights)
    timings = [
        {
            "text_id": row["text_id"],
            "local_proxy_tokens": int(row["local_proxy_tokens"]),
            "allocated_request_seconds": request_seconds * weight / total_weight,
        }
        for row, weight in zip(batch, weights, strict=True)
    ]
    require(
        abs(sum(row["allocated_request_seconds"] for row in timings) - request_seconds) <= 1e-9,
        "Qwen per-text request-time allocation does not conserve time",
    )
    return timings


def embed_texts(
    text_rows: list[dict[str, Any]],
    *,
    cache: ExactEmbeddingCache,
    api_key: str,
    authorisation: dict[str, Any],
    timeout_seconds: int,
    progress_root: Path,
) -> tuple[dict[str, list[float]], dict[str, Any]]:
    rows_by_id = {row["text_id"]: row for row in text_rows}
    require(len(rows_by_id) == len(text_rows), "Qwen text IDs are not unique")
    require(
        all(
            bool(row.get("roles"))
            and all(role.get("kind") in {"document_chunk", "query"} for role in row["roles"])
            for row in text_rows
        ),
        "Qwen text inventory contains an unknown role",
    )
    cached_by_id: dict[str, list[float] | None] = {}
    for row in text_rows:
        cached_by_id[row["text_id"]] = cache.load(row["text"])
    document_rows = [row for row in text_rows if has_text_role(row, "document_chunk")]
    query_rows = [row for row in text_rows if has_text_role(row, "query")]
    document_missing = [row for row in document_rows if cached_by_id[row["text_id"]] is None]
    new_cache_ids = {
        row["text_id"]
        for row in [*document_missing, *query_rows]
        if cached_by_id[row["text_id"]] is None
    }
    external_submission_rows = [*document_missing, *query_rows]
    maximum_new_texts = int(authorisation["maximum_new_texts"])
    maximum_calls = int(authorisation["maximum_successful_calls"])
    maximum_attempts = int(authorisation["maximum_request_attempts"])
    maximum_proxy_tokens = int(authorisation["maximum_local_proxy_tokens"])
    require(len(new_cache_ids) <= maximum_new_texts, "Qwen cache misses exceed authorised text ceiling")
    require(
        sum(int(rows_by_id[text_id]["local_proxy_tokens"]) for text_id in new_cache_ids)
        <= maximum_proxy_tokens,
        "Qwen cache misses exceed authorised token ceiling",
    )
    require(
        sum(int(rows_by_id[text_id]["utf8_bytes"]) for text_id in new_cache_ids)
        <= int(authorisation["maximum_new_utf8_bytes"]),
        "Qwen cache misses exceed authorised byte ceiling",
    )
    require(
        len(external_submission_rows) <= int(authorisation["maximum_external_text_submissions"]),
        "Qwen external text submissions exceed the authorised ceiling",
    )
    require(
        sum(int(row["local_proxy_tokens"]) for row in external_submission_rows)
        <= int(authorisation["maximum_external_submission_proxy_tokens"]),
        "Qwen external submission tokens exceed the authorised ceiling",
    )
    require(
        sum(int(row["utf8_bytes"]) for row in external_submission_rows)
        <= int(authorisation["maximum_external_submission_utf8_bytes"]),
        "Qwen external submission bytes exceed the authorised ceiling",
    )
    require(
        len(query_rows) <= int(authorisation["maximum_cold_query_requests"]),
        "Qwen cold-query requests exceed the authorised ceiling",
    )
    required_calls = math.ceil(len(document_missing) / MAX_BATCH_TEXTS) + len(query_rows)
    require(required_calls <= maximum_calls, "Qwen successful-call ceiling is too small for the cold-query contract")
    require(required_calls <= maximum_attempts, "Qwen request-attempt ceiling is too small for the cold-query contract")

    vectors = {
        row["text_id"]: cached_by_id[row["text_id"]]
        for row in document_rows
        if cached_by_id[row["text_id"]] is not None
    }
    request_attempts = 0
    successful_calls = 0
    provider_usage: dict[str, int] = {}
    request_records: list[dict[str, Any]] = []
    started = time.perf_counter()

    def execute_batch(batch: list[dict[str, Any]], *, request_role: str) -> None:
        nonlocal request_attempts, successful_calls
        require(request_attempts + 1 <= maximum_attempts, "Qwen request-attempt ceiling would be exceeded")
        require(successful_calls + 1 <= maximum_calls, "Qwen successful-call ceiling would be exceeded")
        request_index = request_attempts
        request_attempts += 1
        request_base = {
            "schema_version": "rq2b-qwen-request-record-v1",
            "request_index": request_index,
            "request_role": request_role,
            "text_ids": [row["text_id"] for row in batch],
            "text_count": len(batch),
            "local_proxy_tokens": sum(int(row["local_proxy_tokens"]) for row in batch),
            "utf8_bytes": sum(int(row["utf8_bytes"]) for row in batch),
            "automatic_retry": False,
        }
        write_json_new(progress_root / f"request_{request_index:04d}_attempt.json", {**request_base, "state": "attempt_started"})
        print(f"Qwen: request {request_attempts}, role {request_role}, texts {len(batch)}", flush=True)
        request_started = time.perf_counter()
        response = post_embedding_once(api_key, [row["text"] for row in batch], timeout_seconds)
        request_seconds = time.perf_counter() - request_started
        successful_calls += 1
        data = response.get("data")
        usage = response.get("usage") or {}
        response_record = {
            **request_base,
            "state": "provider_response_received",
            "request_seconds": request_seconds,
            "text_timings": allocated_text_timings(batch, request_seconds),
            "provider_usage": usage,
            "response_data_rows": len(data) if isinstance(data, list) else None,
        }
        response_path = progress_root / f"request_{request_index:04d}_response.json"
        write_json_new(response_path, response_record)
        require(isinstance(usage, dict), "Qwen response usage is not an object")
        require(isinstance(data, list) and len(data) == len(batch), "Qwen response row count mismatch")
        ordered = sorted(data, key=lambda row: int(row["index"]))
        require([int(row["index"]) for row in ordered] == list(range(len(batch))), "Qwen response indices mismatch")
        for key, value in usage.items():
            if isinstance(value, int):
                provider_usage[key] = provider_usage.get(key, 0) + value
        prepared_vectors: list[tuple[dict[str, Any], list[float]]] = []
        for source, result in zip(batch, ordered, strict=True):
            vector = [float(value) for value in result["embedding"]]
            require(len(vector) == DIMENSIONS, "Qwen returned the wrong vector dimension")
            require(all(math.isfinite(value) for value in vector), "Qwen returned non-finite values")
            prepared_vectors.append((source, vector))
        cache_entries_written = 0
        for source, vector in prepared_vectors:
            if cached_by_id[source["text_id"]] is None:
                cache.store(
                    source["text"],
                    vector,
                    local_proxy_tokens=int(source["local_proxy_tokens"]),
                    provider_usage=usage,
                )
                cached_by_id[source["text_id"]] = vector
                cache_entries_written += 1
            vectors[source["text_id"]] = vector
        commit_record = {
            **request_base,
            "state": "cache_commit_complete",
            "provider_response_sha256": sha256_file(response_path),
            "cache_entries_written": cache_entries_written,
        }
        commit_path = progress_root / f"request_{request_index:04d}_cache_commit.json"
        write_json_new(commit_path, commit_record)
        request_records.append(
            {
                **response_record,
                "provider_response_sha256": sha256_file(response_path),
                "cache_commit_sha256": sha256_file(commit_path),
                "cache_entries_written": cache_entries_written,
            }
        )

    for start in range(0, len(document_missing), MAX_BATCH_TEXTS):
        execute_batch(
            document_missing[start : start + MAX_BATCH_TEXTS],
            request_role="document_batch",
        )
    for query_row in query_rows:
        execute_batch([query_row], request_role="cold_query_single")

    require(len(vectors) == len(text_rows), "Qwen vector coverage is incomplete")
    return vectors, {
        "text_rows": len(text_rows),
        "cache_hits": len(text_rows) - len(new_cache_ids),
        "cache_misses": len(new_cache_ids),
        "document_cache_hits": len(document_rows) - len(document_missing),
        "document_cache_misses": len(document_missing),
        "cold_query_requests": len(query_rows),
        "query_cache_entries_preexisting": sum(
            cached_by_id[row["text_id"]] is not None and row["text_id"] not in new_cache_ids
            for row in query_rows
        ),
        "external_text_submissions": len(external_submission_rows),
        "external_submission_proxy_tokens": sum(
            int(row["local_proxy_tokens"]) for row in external_submission_rows
        ),
        "external_submission_utf8_bytes": sum(
            int(row["utf8_bytes"]) for row in external_submission_rows
        ),
        "request_attempts": request_attempts,
        "successful_api_calls": successful_calls,
        "automatic_retries": 0,
        "elapsed_seconds": time.perf_counter() - started,
        "provider_usage": provider_usage,
        "request_records": request_records,
        "cold_query_latency_contract": {
            "required": True,
            "batch_size": 1,
            "one_provider_request_per_unique_query_text": True,
            "query_cache_is_not_used_to_skip_latency_measurement": True,
        },
    }


def score_payload(
    payload: dict[str, Any],
    vectors: dict[str, list[float]],
    prompts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    import numpy as np

    def normalized_matrix(values: list[list[float]]) -> Any:
        matrix = np.asarray(values, dtype=np.float64)
        require(matrix.ndim == 2 and matrix.shape[1] == DIMENSIONS, "Qwen score matrix shape mismatch")
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), "Qwen score matrix norm mismatch")
        return matrix / norms

    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    query_text_ids = payload["query_text_ids"]
    query_vectors = {
        prompt_id: normalized_matrix([vectors[text_id]])[0]
        for prompt_id, text_id in query_text_ids.items()
    }
    rows: list[dict[str, Any]] = []
    for representation, documents in payload["documents"].items():
        skill_ids = [document["skill_id"] for document in documents]
        skill_index = {skill_id: index for index, skill_id in enumerate(skill_ids)}
        require(bool(skill_ids) and len(skill_index) == len(skill_ids), f"Qwen document identity mismatch: {representation}")
        chunk_vectors: list[list[float]] = []
        starts: list[int] = []
        counts: list[int] = []
        for document in documents:
            starts.append(len(chunk_vectors))
            document_vectors = [vectors[text_id] for text_id in document["chunk_text_ids"]]
            require(bool(document_vectors), f"Qwen document has no chunks: {document['skill_id']}")
            counts.append(len(document_vectors))
            chunk_vectors.extend(document_vectors)
        chunk_matrix = normalized_matrix(chunk_vectors)
        mean_vectors: list[Any] = []
        for start, count in zip(starts, counts, strict=True):
            mean = chunk_matrix[start : start + count].mean(axis=0)
            norm = np.linalg.norm(mean)
            require(bool(np.isfinite(norm)) and norm > 0.0, "Qwen mean-vector norm mismatch")
            mean_vectors.append(mean / norm)
        mean_matrix = np.vstack(mean_vectors)
        starts_array = np.asarray(starts, dtype=np.int64)

        for prompt_id, query_vector in query_vectors.items():
            prompt = prompt_by_id[prompt_id]
            max_started = time.perf_counter()
            flat_scores = chunk_matrix @ query_vector
            max_scores = np.maximum.reduceat(flat_scores, starts_array)
            max_ranking = list(zip(skill_ids, (float(value) for value in max_scores), strict=True))
            max_ranking.sort(key=lambda item: (-item[1], item[0]))
            winning_chunks = {
                skill_id: int(
                    np.argmax(
                        flat_scores[
                            starts[skill_index[skill_id]] : starts[skill_index[skill_id]]
                            + counts[skill_index[skill_id]]
                        ]
                    )
                )
                for skill_id, _ in max_ranking[:100]
            }
            max_query_seconds = time.perf_counter() - max_started
            mean_started = time.perf_counter()
            mean_scores = mean_matrix @ query_vector
            mean_ranking = list(zip(skill_ids, (float(value) for value in mean_scores), strict=True))
            mean_ranking.sort(key=lambda item: (-item[1], item[0]))
            mean_query_seconds = time.perf_counter() - mean_started
            primary = rank_row(
                prompt,
                max_ranking,
                representation=representation,
                query_seconds=max_query_seconds,
                retriever="qwen-max-chunk",
                runner_version=RUNNER_VERSION,
                aggregation="maximum_chunk_cosine",
            )
            gold_document = documents[skill_index[prompt["gold_skill"]]]
            sensitivity_metadata = {
                "strict_gold_document_chunk_count": len(gold_document["chunk_text_ids"]),
                "strict_gold_document_chunk_class": (
                    "one_chunk" if len(gold_document["chunk_text_ids"]) == 1 else "multi_chunk"
                ),
                "strict_gold_selector_utf8_bytes": gold_document["selector_utf8_bytes"],
                "strict_gold_source_length_quartile": gold_document["source_length_quartile"],
            }
            primary.update(sensitivity_metadata)
            primary["winning_chunk_by_top_100_skill"] = winning_chunks
            rows.append(primary)
            mean_row = rank_row(
                prompt,
                mean_ranking,
                representation=representation,
                query_seconds=mean_query_seconds,
                retriever="qwen-mean-chunk-sensitivity",
                runner_version=RUNNER_VERSION,
                aggregation="cosine_of_l2_normalized_chunk_mean",
            )
            mean_row.update(sensitivity_metadata)
            rows.append(mean_row)
    return rows


def run(
    root: Path,
    payload_manifest_path: Path,
    authorisation_path: Path,
    output_dir: Path,
    run_id: str,
    api_key_env: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    require(not output_dir.exists(), f"Refusing to overwrite Qwen run: {output_dir}")
    staging = output_dir.parent / f".{output_dir.name}.staging"
    require(not staging.exists(), f"Stale Qwen run staging directory: {staging}")
    payload = read_json(payload_manifest_path)
    require(payload.get("schema_version") == "rq2b-qwen-payload-manifest-v1", "Qwen payload schema mismatch")
    require(payload.get("state") == "sealed_not_executed", "Qwen payload is not sealed")
    authorisation = validate_authorisation(
        authorisation_path,
        payload_manifest_path,
        root=root,
        run_id=run_id,
        output_dir=output_dir,
        timeout_seconds=timeout_seconds,
    )
    text_path = root / payload["text_inventory"]["path"]
    require(sha256_file(text_path) == payload["text_inventory"]["sha256"], "Qwen text inventory drift")
    text_rows = read_jsonl(text_path)
    require(len({row["text_id"] for row in text_rows}) == len(text_rows), "Qwen text IDs are not unique")
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), f"Qwen API key environment variable is missing: {api_key_env}")
    staging.mkdir(parents=True, exist_ok=False)
    run_started_path = staging / "run_started.json"
    write_json_new(
        run_started_path,
        {
            "schema_version": "rq2b-qwen-run-start-v1",
            "version_id": VERSION_ID,
            "run_id": run_id,
            "payload_manifest_sha256": sha256_file(payload_manifest_path),
            "authorisation_sha256": sha256_file(authorisation_path),
            "text_rows": len(text_rows),
            "timeout_seconds": timeout_seconds,
            "automatic_retries": 0,
        },
    )
    progress_root = staging / "request_records"
    progress_root.mkdir(parents=False, exist_ok=False)
    cache = ExactEmbeddingCache(root / "skill_benchmark/cache/rq2b/embeddings")
    vectors, embedding_ledger = embed_texts(
        text_rows,
        cache=cache,
        api_key=api_key,
        authorisation=authorisation,
        timeout_seconds=timeout_seconds,
        progress_root=progress_root,
    )
    prompts = annotate_unresolved_public_equivalents(
        read_jsonl(version_root(root) / "prompt_manifest.jsonl"),
        read_jsonl(version_root(root) / "source_manifest.jsonl"),
    )
    result_rows = score_payload(payload, vectors, prompts)

    rows_path = staging / "rows.jsonl"
    ledger_path = staging / "embedding_ledger.json"
    write_jsonl_new(rows_path, result_rows)
    write_json_new(ledger_path, embedding_ledger)
    manifest = {
        "schema_version": "rq2b-qwen-run-manifest-v1",
        "version_id": VERSION_ID,
        "state": "complete_scientific_b1_external",
        "run_id": run_id,
        "runner_version": RUNNER_VERSION,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "payload_manifest_sha256": sha256_file(payload_manifest_path),
        "payload_manifest_path": relative(payload_manifest_path, root),
        "authorisation_sha256": sha256_file(authorisation_path),
        "authorisation_path": relative(authorisation_path, root),
        "embedding_ledger": embedding_ledger,
        "automatic_retries": 0,
        "request_attempts": embedding_ledger["request_attempts"],
        "successful_api_calls": embedding_ledger["successful_api_calls"],
        "timeout_seconds": timeout_seconds,
        "artifacts": {
            "rows": {
                "path": relative(output_dir / rows_path.name, root),
                "sha256": sha256_file(rows_path),
                "rows": len(result_rows),
            },
            "embedding_ledger": {
                "path": relative(output_dir / ledger_path.name, root),
                "sha256": sha256_file(ledger_path),
            },
            "run_started": {
                "path": relative(output_dir / run_started_path.name, root),
                "sha256": sha256_file(run_started_path),
            },
            "request_records": [
                {
                    "path": relative(output_dir / "request_records" / path.name, root),
                    "sha256": sha256_file(path),
                }
                for path in sorted(progress_root.glob("*.json"))
            ],
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_dir)
    return manifest


def self_test() -> dict[str, Any]:
    def vector(first: float, second: float) -> list[float]:
        return [first, second, *([0.0] * (DIMENSIONS - 2))]

    query = vector(1.0, 0.0)
    max_score, winning, mean_score = document_scores(
        query,
        [vector(1.0, 0.0), vector(0.8, 0.2)],
    )
    require(winning == 0, "Qwen max-chunk tie/order self-test failed")
    require(max_score > mean_score, "Qwen mean sensitivity self-test failed")
    timings = allocated_text_timings(
        [
            {"text_id": "a", "local_proxy_tokens": 1},
            {"text_id": "b", "local_proxy_tokens": 3},
        ],
        4.0,
    )
    require(
        [row["allocated_request_seconds"] for row in timings] == [1.0, 3.0],
        "Qwen per-text request timing self-test failed",
    )
    with tempfile.TemporaryDirectory() as directory:
        cache = ExactEmbeddingCache(Path(directory))
        text = "synthetic document"
        require(cache.load(text) is None, "Qwen empty-cache self-test failed")
        cache.store(text, query, local_proxy_tokens=2, provider_usage={})
        require(cache.load(text) == query, "Qwen cache round-trip self-test failed")
    synthetic_vectors = {
        "q": query,
        "d0": vector(1.0, 0.0),
        "d1": vector(0.0, 1.0),
        "d2": vector(-1.0, 0.0),
    }
    synthetic_payload = {
        "query_text_ids": {"p1": "q"},
        "documents": {
            "i1-discovery": [
                {"skill_id": "s0", "chunk_text_ids": ["d0"]},
                {"skill_id": "s1", "chunk_text_ids": ["d1"]},
                {"skill_id": "s2", "chunk_text_ids": ["d2"]},
            ]
        },
    }
    for document in synthetic_payload["documents"]["i1-discovery"]:
        document["selector_utf8_bytes"] = 10
        document["source_length_quartile"] = "q1"
    synthetic_prompts = [
        {
            "prompt_id": "p1",
            "stratum": "controlled",
            "group": "g1",
            "prompt_sha256": sha256_text("synthetic query"),
            "gold_skill": "s0",
            "valid_skills": ["s0"],
            "closest_alternatives": ["s1"],
        }
    ]
    scored = score_payload(synthetic_payload, synthetic_vectors, synthetic_prompts)
    require(len(scored) == 2, "Qwen vectorized scoring row-count self-test failed")
    require(scored[0]["strict_hit_at_1"] == 1, "Qwen vectorized scoring rank self-test failed")
    require(scored[0]["winning_chunk_by_top_100_skill"]["s0"] == 0, "Qwen vectorized winning-chunk self-test failed")
    return {
        "state": "synthetic_no_external_call_no_scientific_result",
        "network_calls": 0,
        "maximum_score": max_score,
        "mean_score": mean_score,
        "winning_chunk": winning,
        "cache_roundtrip": True,
        "vectorized_scoring": True,
        "per_text_request_time_conserved": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--payload-manifest", type=Path)
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.execute, "Qwen execution requires --execute and a separate authorisation")
        require(args.payload_manifest is not None, "--payload-manifest is required")
        require(args.authorisation is not None, "--authorisation is required")
        require(args.output_dir is not None, "--output-dir is required")
        require(args.run_id is not None, "--run-id is required")
        root = args.root.resolve()
        payload_path = args.payload_manifest if args.payload_manifest.is_absolute() else root / args.payload_manifest
        authorisation_path = args.authorisation if args.authorisation.is_absolute() else root / args.authorisation
        output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        result = run(
            root,
            payload_path,
            authorisation_path,
            output_dir,
            args.run_id,
            args.api_key_env,
            args.timeout_seconds,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
