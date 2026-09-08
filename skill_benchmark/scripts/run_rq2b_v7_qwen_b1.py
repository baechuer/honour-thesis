#!/usr/bin/env python3
"""Run the four authorised label-free V7 Qwen B1 cells.

This runner is inert unless it receives both ``--execute`` and a separate,
payload-hash-bound release authorisation issued after Phase-7 QA.  It performs
no retries.  B1 uses maximum-window cosine; mean-window rankings are emitted
only in a separate sensitivity artifact.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from build_rq2b_v7_qwen_b1_preflight import (
    BASE_URL,
    CLEAN_CACHE_REL,
    DEFAULT_LEGACY_CACHE,
    DIMENSIONS,
    MODEL,
    PACKAGE_REL,
    PAYLOAD_REL,
    REPRESENTATION_CELLS,
    RUNNER_VERSION,
    SOURCE_UNION_SHA256,
    TOP_K,
    ReadOnlyExactEmbeddingCache,
    V2ExactEmbeddingCache,
    canonical_sha256,
    file_sha256,
    is_sha256,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    text_sha256,
    write_json,
    write_jsonl,
)
from run_rq2b_qwen import embed_texts


AUTHORISATION_SCHEMA = "rq2b-v7-qwen-b1-execution-authorisation-v2"
B1_SCHEMA = "rq2b-v7-b1-runner-output-v1"
SENSITIVITY_SCHEMA = "rq2b-v7-qwen-mean-window-sensitivity-v2"
CEILING_KEYS = (
    "maximum_new_cache_entries",
    "maximum_new_cache_proxy_tokens",
    "maximum_new_cache_utf8_bytes",
    "maximum_external_text_submissions",
    "maximum_external_submission_proxy_tokens",
    "maximum_external_submission_utf8_bytes",
    "cold_query_requests",
    "maximum_request_attempts",
    "maximum_successful_calls",
)


class HybridExactEmbeddingCache:
    """Read exact hits from clean then sealed legacy cache; write clean only."""

    def __init__(
        self,
        clean_cache: V2ExactEmbeddingCache,
        legacy_cache: ReadOnlyExactEmbeddingCache,
        text_by_sha: dict[str, dict[str, Any]],
        inventory_by_text_id: dict[str, dict[str, Any]],
    ) -> None:
        self.clean_cache = clean_cache
        self.legacy_cache = legacy_cache
        self.text_by_sha = text_by_sha
        self.inventory_by_text_id = inventory_by_text_id

    def load(self, text: str) -> list[float] | None:
        text_id = text_sha256(text)
        require(text_id in self.text_by_sha, "Cache lookup text is outside sealed payload")
        clean_path = self.clean_cache.path(text)
        if clean_path.is_file():
            return self.clean_cache.load(text)
        inventory = self.inventory_by_text_id[text_id]
        if not inventory["legacy_cache_hit"]:
            return None
        legacy_path = self.legacy_cache.path(text)
        require(legacy_path.is_file(), f"Sealed legacy cache hit disappeared: {legacy_path}")
        require(
            file_sha256(legacy_path) == inventory["legacy_cache_entry_sha256"],
            f"Sealed legacy cache entry drift: {legacy_path}",
        )
        return self.legacy_cache.load(text)

    def store(
        self,
        text: str,
        vector: list[float],
        *,
        local_proxy_tokens: int,
        provider_usage: dict[str, Any],
    ) -> None:
        self.clean_cache.store(
            text,
            vector,
            local_proxy_tokens=local_proxy_tokens,
            provider_usage=provider_usage,
        )


def load_payload(root: Path) -> tuple[
    Path,
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    manifest_path = root / PAYLOAD_REL / "payload_manifest.json"
    manifest = read_json(manifest_path)
    require(manifest["schema_version"] == "rq2b-v7-qwen-b1-payload-manifest-v2", "Payload schema drift")
    require(manifest["state"] == "SEALED_LABEL_FREE_NOT_AUTHORISED", "Payload state drift")
    require(manifest["runner_version"] == RUNNER_VERSION, "Payload runner binding drift")
    require(manifest["model"] == MODEL and manifest["dimensions"] == DIMENSIONS, "Payload model drift")
    require(manifest["document_score_aggregation"] == "maximum_window_cosine", "Primary aggregation drift")
    require(manifest["stable_tie_break"] == "source_sha256_ascending", "Tie-break drift")
    require(manifest["top_k"] == TOP_K, "Top-K drift")
    for name, implementation in manifest["implementation"].items():
        path = root / implementation["path"]
        require(path.is_file(), f"Bound implementation missing: {name}")
        require(file_sha256(path) == implementation["sha256"], f"Bound implementation drift: {name}")
    for artifact in manifest["artifacts"].values():
        path = root / artifact["path"]
        require(path.is_file(), f"Payload artifact missing: {path}")
        require(file_sha256(path) == artifact["sha256"], f"Payload artifact drift: {path}")
        require(path.stat().st_size == artifact["utf8_bytes"], f"Payload artifact size drift: {path}")
    text_rows = read_jsonl(root / manifest["artifacts"]["text_inventory"]["path"])
    document_rows = read_jsonl(root / manifest["artifacts"]["document_map"]["path"])
    cache_rows = read_jsonl(root / manifest["artifacts"]["cache_hit_inventory"]["path"])
    require(len(text_rows) == manifest["artifacts"]["text_inventory"]["rows"], "Text inventory row drift")
    require(len(document_rows) == manifest["artifacts"]["document_map"]["rows"], "Document map row drift")
    require(len(cache_rows) == manifest["artifacts"]["cache_hit_inventory"]["rows"], "Cache inventory row drift")
    require(len({row["text_id"] for row in text_rows}) == len(text_rows), "Duplicate payload text IDs")
    require(len({(row["representation"], row["source_sha256"]) for row in document_rows}) == len(document_rows), "Duplicate payload documents")
    require(len({row["text_id"] for row in cache_rows}) == len(cache_rows), "Duplicate cache inventory IDs")
    return manifest_path, manifest, text_rows, document_rows, cache_rows


def validate_release_authorisation(
    path: Path,
    *,
    root: Path,
    payload_manifest_path: Path,
    payload: dict[str, Any],
    run_id: str,
    output_dir: Path,
    timeout_seconds: int,
    legacy_cache_root: Path,
) -> dict[str, Any]:
    require(path.is_file(), f"Execution authorisation missing: {path}")
    value = read_json(path)
    require(value.get("schema_version") == AUTHORISATION_SCHEMA, "Execution authorisation schema drift")
    require(
        value.get("state") == "EXPLICITLY_AUTHORISED_FOR_ONE_EXECUTION_AFTER_PHASE7_QA",
        "Execution is not released after Phase-7 QA",
    )
    require(value.get("payload_manifest_path") == relative(payload_manifest_path, root), "Authorised payload path drift")
    require(value.get("payload_manifest_sha256") == file_sha256(payload_manifest_path), "Authorised payload hash drift")
    require(value.get("base_url") == BASE_URL and value.get("model") == MODEL, "Authorised provider/model drift")
    require(value.get("dimensions") == DIMENSIONS, "Authorised dimensions drift")
    require(value.get("automatic_retries") == 0, "Automatic retries must be zero")
    require(value.get("cold_query_latency_measurement") is True, "Cold query latency is mandatory")
    require(value.get("cold_query_batch_size") == 1, "Cold query batch size must be one")
    require(value.get("phase7_qa_status") == "PASS", "Phase-7 QA is not recorded PASS")
    require(is_sha256(value.get("phase7_qa_receipt_sha256")), "Phase-7 QA receipt hash missing")
    require(isinstance(value.get("root_release_id"), str) and value["root_release_id"], "Root release ID missing")
    require(value.get("run_id") == run_id, "Authorised run ID drift")
    require(value.get("output_dir") == relative(output_dir, root), "Authorised output directory drift")
    require(value.get("timeout_seconds") == timeout_seconds, "Authorised timeout drift")
    require(
        Path(value.get("legacy_cache_root", "")).resolve() == legacy_cache_root.resolve(),
        "Authorised legacy read-only cache root drift",
    )
    require(value.get("clean_cache_root") == CLEAN_CACHE_REL.as_posix(), "Authorised clean cache root drift")
    ceilings = value.get("ceilings")
    require(isinstance(ceilings, dict) and set(ceilings) == set(CEILING_KEYS), "Authorised ceiling keys drift")
    for key in CEILING_KEYS:
        require(isinstance(ceilings[key], int) and ceilings[key] >= 0, f"Invalid authorised ceiling: {key}")
        require(ceilings[key] == payload["counts"][key], f"Authorised ceiling differs from payload: {key}")
    return value


def embedding_authorisation(value: dict[str, Any]) -> dict[str, Any]:
    ceilings = value["ceilings"]
    return {
        "maximum_new_texts": ceilings["maximum_new_cache_entries"],
        "maximum_request_attempts": ceilings["maximum_request_attempts"],
        "maximum_successful_calls": ceilings["maximum_successful_calls"],
        "maximum_local_proxy_tokens": ceilings["maximum_new_cache_proxy_tokens"],
        "maximum_new_utf8_bytes": ceilings["maximum_new_cache_utf8_bytes"],
        "maximum_external_text_submissions": ceilings["maximum_external_text_submissions"],
        "maximum_external_submission_proxy_tokens": ceilings["maximum_external_submission_proxy_tokens"],
        "maximum_external_submission_utf8_bytes": ceilings["maximum_external_submission_utf8_bytes"],
        "maximum_cold_query_requests": ceilings["cold_query_requests"],
    }


def top20_binding_sha256(
    *,
    condition_id: str,
    prompt_id: str,
    prompt_sha256: str,
    ordered_source_sha256: Iterable[str],
) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-top20-binding-v1",
        "condition_id": condition_id,
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_sha256,
        "ordered_source_sha256": list(ordered_source_sha256),
    })


def canonical_jsonl_bytes(rows: Iterable[dict[str, Any]]) -> Iterable[bytes]:
    for row in rows:
        yield (
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")


def write_deterministic_jsonl_gzip(
    path: Path,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write canonical JSONL in deterministic gzip without changing row semantics."""
    path.parent.mkdir(parents=True, exist_ok=True)
    uncompressed = hashlib.sha256()
    uncompressed_bytes = 0
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            for encoded in canonical_jsonl_bytes(rows):
                uncompressed.update(encoded)
                uncompressed_bytes += len(encoded)
                compressed.write(encoded)
    return {
        "sha256": file_sha256(path),
        "utf8_bytes_compressed": path.stat().st_size,
        "canonical_jsonl_sha256_uncompressed": uncompressed.hexdigest(),
        "utf8_bytes_uncompressed": uncompressed_bytes,
        "rows": len(rows),
        "compression": "gzip-mtime-0",
        "jsonl_serialization": "utf8-sort-keys-compact-lf-v1",
    }


def read_jsonl_any(path: Path) -> list[dict[str, Any]]:
    opener = gzip.open if path.suffix == ".gz" else path.open
    rows: list[dict[str, Any]] = []
    if path.suffix == ".gz":
        handle_context = opener(path, "rt", encoding="utf-8")
    else:
        handle_context = opener(encoding="utf-8")
    with handle_context as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected object at {path}:{line_number}")
            rows.append(value)
    return rows


def normalized_matrix(values: list[list[float]]) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    require(matrix.ndim == 2 and matrix.shape[1] == DIMENSIONS, "Embedding matrix shape drift")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), "Embedding norm drift")
    return matrix / norms


def stable_top_k(source_ids: list[str], scores: np.ndarray, k: int = TOP_K) -> list[int]:
    require(len(source_ids) == len(scores) and len(source_ids) >= k, "Ranking input size drift")
    require(bool(np.all(np.isfinite(scores))), "Ranking contains non-finite scores")
    source_array = np.asarray(source_ids, dtype=f"U{max(map(len, source_ids))}")
    order = np.lexsort((source_array, -scores))
    return [int(index) for index in order[:k]]


def score_representation(
    *,
    run_id: str,
    representation: str,
    condition: dict[str, Any],
    documents: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
    query_text_ids: dict[str, str],
    text_by_id: dict[str, dict[str, Any]],
    vectors: dict[str, list[float]],
    query_latency_seconds: dict[str, float],
    initial_cache_available: dict[str, bool],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    documents = sorted(documents, key=lambda row: row["source_sha256"])
    source_ids = [row["source_sha256"] for row in documents]
    require(len(source_ids) == 3798 and len(set(source_ids)) == len(source_ids), "Representation identity drift")
    starts: list[int] = []
    counts: list[int] = []
    flat_vectors: list[list[float]] = []
    for document in documents:
        starts.append(len(flat_vectors))
        doc_vectors = [vectors[text_id] for text_id in document["chunk_text_ids"]]
        require(bool(doc_vectors), "Document has no embedding windows")
        counts.append(len(doc_vectors))
        flat_vectors.extend(doc_vectors)
    chunk_matrix = normalized_matrix(flat_vectors)
    starts_array = np.asarray(starts, dtype=np.int64)
    mean_vectors: list[np.ndarray] = []
    for start, count in zip(starts, counts, strict=True):
        mean = chunk_matrix[start:start + count].mean(axis=0)
        norm = float(np.linalg.norm(mean))
        require(math.isfinite(norm) and norm > 0.0, "Mean-window vector norm drift")
        mean_vectors.append(mean / norm)
    mean_matrix = np.vstack(mean_vectors)
    cache_hits = sum(
        initial_cache_available[text_id]
        for document in documents
        for text_id in document["chunk_text_ids"]
    )
    rows: list[dict[str, Any]] = []
    sensitivities: list[dict[str, Any]] = []
    for prompt in prompts:
        query_text_id = query_text_ids[prompt["prompt_id"]]
        query = normalized_matrix([vectors[query_text_id]])[0]
        started = time.perf_counter()
        flat_scores = chunk_matrix @ query
        maximum_scores = np.maximum.reduceat(flat_scores, starts_array)
        maximum_indices = stable_top_k(source_ids, maximum_scores)
        maximum_seconds = time.perf_counter() - started
        maximum_candidates = [
            {
                "rank": rank,
                "source_sha256": source_ids[index],
                "score": float(maximum_scores[index]),
            }
            for rank, index in enumerate(maximum_indices, 1)
        ]
        condition_id = condition["condition_id"]
        rows.append({
            "schema_version": B1_SCHEMA,
            "status": "SUCCESS",
            "run_id": run_id,
            "condition_id": condition_id,
            "first_stage_cell_id": REPRESENTATION_CELLS[representation],
            "prompt_id": prompt["prompt_id"],
            "prompt_sha256": prompt["prompt_sha256"],
            "representation": representation,
            "retriever": condition["retriever"],
            "persisted_candidate_source": condition["persisted_candidate_source"],
            "source_union_sha256": SOURCE_UNION_SHA256,
            "top_k": TOP_K,
            "score_semantics": "HIGHER_IS_BETTER",
            "top20_binding_sha256": top20_binding_sha256(
                condition_id=condition_id,
                prompt_id=prompt["prompt_id"],
                prompt_sha256=prompt["prompt_sha256"],
                ordered_source_sha256=(item["source_sha256"] for item in maximum_candidates[:20]),
            ),
            "ranked_candidates": maximum_candidates,
            "cost": {
                "wall_time_ms": 1000.0 * (query_latency_seconds[query_text_id] + maximum_seconds),
                "provider_calls": 1,
                "input_tokens": int(text_by_id[query_text_id]["local_proxy_tokens"]),
                "output_tokens": 0,
                "window_forwards": len(flat_vectors),
                "cache_hits": int(cache_hits),
                "retry_count": 0,
                "timeout_count": 0,
                "failure_count": 0,
            },
        })

        mean_started = time.perf_counter()
        mean_scores = mean_matrix @ query
        mean_indices = stable_top_k(source_ids, mean_scores)
        mean_seconds = time.perf_counter() - mean_started
        sensitivities.append({
            "schema_version": SENSITIVITY_SCHEMA,
            "status": "NON_CORE_SENSITIVITY_SUCCESS",
            "run_id": run_id,
            "first_stage_cell_id": REPRESENTATION_CELLS[representation],
            "prompt_id": prompt["prompt_id"],
            "prompt_sha256": prompt["prompt_sha256"],
            "representation": representation,
            "aggregation": "cosine_of_l2_normalized_window_mean",
            "primary_aggregation": "maximum_window_cosine",
            "core_outcome": False,
            "stable_tie_break": "source_sha256_ascending",
            "top_k": TOP_K,
            "ranked_candidates": [
                {"rank": rank, "source_sha256": source_ids[index], "score": float(mean_scores[index])}
                for rank, index in enumerate(mean_indices, 1)
            ],
            "scoring_wall_time_ms": mean_seconds * 1000.0,
        })
    return rows, sensitivities


def validate_b1_rows(rows: list[dict[str, Any]], payload: dict[str, Any]) -> None:
    expected_keys = {
        "schema_version", "status", "run_id", "condition_id", "first_stage_cell_id",
        "prompt_id", "prompt_sha256", "representation", "retriever",
        "persisted_candidate_source", "source_union_sha256", "top_k",
        "score_semantics", "top20_binding_sha256", "ranked_candidates", "cost",
    }
    cost_keys = {
        "wall_time_ms", "provider_calls", "input_tokens", "output_tokens",
        "window_forwards", "cache_hits", "retry_count", "timeout_count", "failure_count",
    }
    require(len(rows) == payload["counts"]["b1_output_rows"], "B1 output row count drift")
    seen: set[tuple[str, str]] = set()
    for row in rows:
        require(set(row) == expected_keys, "B1 row keys drift")
        require(row["schema_version"] == B1_SCHEMA and row["status"] == "SUCCESS", "B1 row status drift")
        require(row["top_k"] == TOP_K and row["score_semantics"] == "HIGHER_IS_BETTER", "B1 ranking contract drift")
        require(set(row["cost"]) == cost_keys, "B1 cost keys drift")
        candidates = row["ranked_candidates"]
        require(len(candidates) == TOP_K, "B1 Top-100 row length drift")
        require([item["rank"] for item in candidates] == list(range(1, TOP_K + 1)), "B1 ranks drift")
        identities = [item["source_sha256"] for item in candidates]
        require(len(set(identities)) == TOP_K and all(is_sha256(value) for value in identities), "B1 identities drift")
        require(all(math.isfinite(float(item["score"])) for item in candidates), "B1 non-finite score")
        require(
            row["top20_binding_sha256"] == top20_binding_sha256(
                condition_id=row["condition_id"], prompt_id=row["prompt_id"],
                prompt_sha256=row["prompt_sha256"], ordered_source_sha256=identities[:20]
            ),
            "B1 Top-20 binding drift",
        )
        key = (row["condition_id"], row["prompt_id"])
        require(key not in seen, "Duplicate B1 output row")
        seen.add(key)


def validate_b1_shards(paths: list[Path], payload: dict[str, Any]) -> None:
    require(len(paths) == 4, "Exactly four Qwen B1 condition shards are required")
    rows: list[dict[str, Any]] = []
    for path in sorted(paths):
        require(path.name.endswith(".jsonl.gz"), f"B1 shard must be deterministic gzip JSONL: {path}")
        shard_rows = read_jsonl_any(path)
        require(len({row["condition_id"] for row in shard_rows}) == 1, f"B1 shard mixes conditions: {path}")
        rows.extend(shard_rows)
    validate_b1_rows(rows, payload)


def run(
    *,
    root: Path,
    authorisation_path: Path,
    output_dir: Path,
    run_id: str,
    legacy_cache_root: Path,
    api_key_env: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    require(not output_dir.exists(), f"Refusing to overwrite output: {output_dir}")
    staging = output_dir.parent / f".{output_dir.name}.staging-{os.getpid()}"
    require(not staging.exists(), f"Stale output staging directory: {staging}")
    payload_manifest_path, payload, text_rows, document_rows, cache_rows = load_payload(root)
    authorisation = validate_release_authorisation(
        authorisation_path,
        root=root,
        payload_manifest_path=payload_manifest_path,
        payload=payload,
        run_id=run_id,
        output_dir=output_dir,
        timeout_seconds=timeout_seconds,
        legacy_cache_root=legacy_cache_root,
    )
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), f"Qwen API key environment variable is missing: {api_key_env}")

    prompts = read_jsonl(root / next(
        path for path in payload["input_artifacts"] if path.endswith("label_free_query_runtime.jsonl")
    ))
    require(len(prompts) == 1077, "Runtime query count drift")
    text_by_id = {row["text_id"]: row for row in text_rows}
    inventory_by_id = {row["text_id"]: row for row in cache_rows}
    require(set(text_by_id) == set(inventory_by_id), "Cache/text inventory identity drift")
    require(len(set(payload["query_text_ids"].values())) == len(prompts), "Cold query contract requires unique query texts")

    clean_cache = V2ExactEmbeddingCache(root / CLEAN_CACHE_REL)
    legacy_cache = ReadOnlyExactEmbeddingCache(legacy_cache_root)
    cache = HybridExactEmbeddingCache(clean_cache, legacy_cache, text_by_id, inventory_by_id)
    initial_cache_available = {
        text_id: cache.load(row["text"]) is not None for text_id, row in text_by_id.items()
    }

    staging.mkdir(parents=True, exist_ok=False)
    try:
        write_json(staging / "run_started.json", {
            "schema_version": "rq2b-v7-qwen-b1-run-start-v2",
            "run_id": run_id,
            "runner_version": RUNNER_VERSION,
            "payload_manifest_sha256": file_sha256(payload_manifest_path),
            "authorisation_sha256": file_sha256(authorisation_path),
            "phase7_qa_receipt_sha256": authorisation["phase7_qa_receipt_sha256"],
            "root_release_id": authorisation["root_release_id"],
            "automatic_retries": 0,
            "timeout_seconds": timeout_seconds,
        })
        request_root = staging / "request_records"
        request_root.mkdir()
        vectors, embedding_ledger = embed_texts(
            text_rows,
            cache=cache,  # type: ignore[arg-type]
            api_key=str(api_key),
            authorisation=embedding_authorisation(authorisation),
            timeout_seconds=timeout_seconds,
            progress_root=request_root,
        )
        query_latency_seconds: dict[str, float] = {}
        for record in embedding_ledger["request_records"]:
            if record["request_role"] == "cold_query_single":
                require(len(record["text_ids"]) == 1, "Cold query request batch drift")
                query_latency_seconds[record["text_ids"][0]] = float(record["request_seconds"])
        require(set(query_latency_seconds) == set(payload["query_text_ids"].values()), "Cold query latency coverage drift")

        documents_by_representation = {
            representation: [row for row in document_rows if row["representation"] == representation]
            for representation in REPRESENTATION_CELLS
        }
        rows: list[dict[str, Any]] = []
        sensitivities: list[dict[str, Any]] = []
        for representation, cell in REPRESENTATION_CELLS.items():
            cell_rows, sensitivity_rows = score_representation(
                run_id=run_id,
                representation=representation,
                condition=payload["conditions"][cell],
                documents=documents_by_representation[representation],
                prompts=prompts,
                query_text_ids=payload["query_text_ids"],
                text_by_id=text_by_id,
                vectors=vectors,
                query_latency_seconds=query_latency_seconds,
                initial_cache_available=initial_cache_available,
            )
            rows.extend(cell_rows)
            sensitivities.extend(sensitivity_rows)
        validate_b1_rows(rows, payload)

        ledger_path = staging / "embedding_ledger.json"
        b1_shards: list[dict[str, Any]] = []
        sensitivity_shards: list[dict[str, Any]] = []
        b1_paths: list[Path] = []
        for cell in sorted(REPRESENTATION_CELLS.values()):
            condition_id = f"{cell}-G0"
            shard_rows = [row for row in rows if row["condition_id"] == condition_id]
            sensitivity_rows = [
                row for row in sensitivities if row["first_stage_cell_id"] == cell
            ]
            b1_path = staging / "b1_shards" / f"{condition_id}.jsonl.gz"
            sensitivity_path = staging / "mean_window_sensitivity_shards" / f"{cell}.jsonl.gz"
            b1_metadata = write_deterministic_jsonl_gzip(b1_path, shard_rows)
            sensitivity_metadata = write_deterministic_jsonl_gzip(
                sensitivity_path, sensitivity_rows
            )
            b1_paths.append(b1_path)
            b1_shards.append({
                "condition_id": condition_id,
                "path": relative(output_dir / "b1_shards" / b1_path.name, root),
                **b1_metadata,
            })
            sensitivity_shards.append({
                "first_stage_cell_id": cell,
                "path": relative(
                    output_dir / "mean_window_sensitivity_shards" / sensitivity_path.name,
                    root,
                ),
                "core_outcome": False,
                **sensitivity_metadata,
            })
        validate_b1_shards(b1_paths, payload)
        write_json(ledger_path, embedding_ledger)
        request_artifacts = [
            {"path": relative(output_dir / "request_records" / path.name, root), "sha256": file_sha256(path)}
            for path in sorted(request_root.glob("*.json"))
        ]
        manifest = {
            "schema_version": "rq2b-v7-qwen-b1-run-manifest-v2",
            "status": "COMPLETE_FOUR_LABEL_FREE_QWEN_B1_CELLS",
            "run_id": run_id,
            "runner_version": RUNNER_VERSION,
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "primary_aggregation": "maximum_window_cosine",
            "noncore_sensitivity_aggregation": "cosine_of_l2_normalized_window_mean",
            "stable_tie_break": "source_sha256_ascending",
            "top_k": TOP_K,
            "payload_manifest_sha256": file_sha256(payload_manifest_path),
            "authorisation_sha256": file_sha256(authorisation_path),
            "phase7_qa_receipt_sha256": authorisation["phase7_qa_receipt_sha256"],
            "root_release_id": authorisation["root_release_id"],
            "automatic_retries": 0,
            "output_storage": {
                "condition_sharded": True,
                "compression": "gzip-mtime-0",
                "jsonl_serialization": "utf8-sort-keys-compact-lf-v1",
                "compression_does_not_change_row_semantics_or_hash_bindings": True,
            },
            "embedding_ledger": embedding_ledger,
            "artifacts": {
                "b1_condition_shards": b1_shards,
                "mean_window_sensitivity_condition_shards": sensitivity_shards,
                "embedding_ledger": {"path": relative(output_dir / ledger_path.name, root), "sha256": file_sha256(ledger_path)},
                "run_started": {"path": relative(output_dir / "run_started.json", root), "sha256": file_sha256(staging / "run_started.json")},
                "request_records": request_artifacts,
            },
        }
        write_json(staging / "manifest.json", manifest)
        staging.replace(output_dir)
        return manifest
    except Exception:
        # Preserve run_started/request attempt receipts and any committed clean
        # exact-cache entries for diagnosis and bounded resume planning.  A
        # failed run never gets renamed to the scientific output directory.
        raise


def self_test() -> dict[str, Any]:
    source_ids = [f"{index:064x}" for index in range(100)]
    scores = np.ones(100, dtype=np.float64)
    order = stable_top_k(list(reversed(source_ids)), scores)
    ranked = [list(reversed(source_ids))[index] for index in order]
    require(ranked == source_ids, "Stable source-SHA tie self-test failed")
    binding = top20_binding_sha256(
        condition_id="B02-G0", prompt_id="p", prompt_sha256="0" * 64,
        ordered_source_sha256=source_ids[:20],
    )
    require(is_sha256(binding), "Top-20 binding self-test failed")
    return {
        "state": "SYNTHETIC_NO_PROVIDER_REQUEST_NO_SCIENTIFIC_RESULT",
        "network_calls": 0,
        "stable_tie_break": True,
        "top20_binding": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--legacy-cache-root", type=Path, default=DEFAULT_LEGACY_CACHE)
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.execute, "Provider execution requires --execute")
        require(args.authorisation is not None, "--authorisation is required")
        require(args.output_dir is not None, "--output-dir is required")
        require(args.run_id is not None and args.run_id, "--run-id is required")
        root = args.root.resolve()
        authorisation = args.authorisation if args.authorisation.is_absolute() else root / args.authorisation
        output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        result = run(
            root=root,
            authorisation_path=authorisation,
            output_dir=output_dir,
            run_id=args.run_id,
            legacy_cache_root=args.legacy_cache_root.resolve(),
            api_key_env=args.api_key_env,
            timeout_seconds=args.timeout_seconds,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
