#!/usr/bin/env python3
"""Run the authorised full-context SkillRouter embedding first stage for RQ2b."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
import time
from pathlib import Path
from typing import Any

from rq2b_common import (
    B0F_A1_AMENDMENT_SHA256,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    sha256_text,
    verify_b0f_a1_amendment,
    verify_b1s_implementation_seal,
    verify_frozen_manifest,
    version_root,
    write_json_new,
    write_jsonl_new,
)
from run_rq2b_bm25 import annotate_unresolved_public_equivalents, rank_row


RUNNER_VERSION = "rq2b-skillrouter-embedding-full-context-runner-v1"
MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
REVISION = "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
DIMENSIONS = 1024
MAX_MODEL_TOKENS = 32768
TOKENIZER_SHA256 = "def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a"
MODEL_CONFIG_SHA256 = "02b34f6be10ee6a35304e32b67ac37be4b2b04e327efff49a689136b0913a0e8"
MODEL_WEIGHTS_SHA256 = "cbab45b8a3c786b8c23aedb24fb22aff74d0e9b62a52369a3090c37f26b00360"
QUERY_INSTRUCTION = (
    "Instruct: Given a task description, retrieve the most relevant "
    "skill document that would help an agent complete the task\nQuery:"
)
RUNTIME_DTYPE = "bfloat16"
RUNTIME_DEVICE = "cuda"


def l2_normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    require(math.isfinite(norm) and norm > 0.0, "SkillRouter embedding has invalid norm")
    return [value / norm for value in vector]


def cache_key(text: str) -> str:
    return sha256_json(
        {
            "model": MODEL,
            "revision": REVISION,
            "dimensions": DIMENSIONS,
            "maximum_model_tokens": MAX_MODEL_TOKENS,
            "tokenizer_sha256": TOKENIZER_SHA256,
            "model_config_sha256": MODEL_CONFIG_SHA256,
            "model_weights_sha256": MODEL_WEIGHTS_SHA256,
            "pooling": "last_non_padding_token",
            "normalization": "l2",
            "runtime_dtype": RUNTIME_DTYPE,
            "text_sha256": sha256_text(text),
        }
    )


class ExactEmbeddingCache:
    def __init__(self, root: Path) -> None:
        self.root = root / "skillrouter-embedding" / REVISION / RUNTIME_DTYPE
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, text: str) -> Path:
        return self.root / f"{cache_key(text)}.json"

    def load(self, text: str) -> list[float] | None:
        path = self.path(text)
        if not path.exists():
            return None
        value = read_json(path)
        require(value.get("schema_version") == "rq2b-skillrouter-embedding-cache-v1", f"Cache schema mismatch: {path}")
        require(value.get("cache_key") == cache_key(text), f"Cache key mismatch: {path}")
        require(value.get("text_sha256") == sha256_text(text), f"Cache text mismatch: {path}")
        require(value.get("model") == MODEL and value.get("revision") == REVISION, f"Cache model mismatch: {path}")
        vector = [float(item) for item in value.get("embedding", [])]
        require(len(vector) == DIMENSIONS, f"Cache vector dimension mismatch: {path}")
        require(all(math.isfinite(item) for item in vector), f"Cache has non-finite vector: {path}")
        return vector

    def store(self, text: str, vector: list[float], *, model_tokens: int) -> None:
        path = self.path(text)
        require(not path.exists(), f"Refusing to overwrite SkillRouter embedding cache: {path}")
        normalized = l2_normalize(vector)
        write_json_new(
            path,
            {
                "schema_version": "rq2b-skillrouter-embedding-cache-v1",
                "cache_key": cache_key(text),
                "model": MODEL,
                "revision": REVISION,
                "dimensions": DIMENSIONS,
                "maximum_model_tokens": MAX_MODEL_TOKENS,
                "tokenizer_sha256": TOKENIZER_SHA256,
                "model_config_sha256": MODEL_CONFIG_SHA256,
                "model_weights_sha256": MODEL_WEIGHTS_SHA256,
                "pooling": "last_non_padding_token",
                "normalization": "l2",
                "runtime_dtype": RUNTIME_DTYPE,
                "text_sha256": sha256_text(text),
                "model_tokens": model_tokens,
                "embedding": normalized,
            },
        )


def verify_model_snapshot(snapshot: Path) -> dict[str, Any]:
    expected = {
        "tokenizer.json": TOKENIZER_SHA256,
        "config.json": MODEL_CONFIG_SHA256,
        "model.safetensors": MODEL_WEIGHTS_SHA256,
    }
    for filename, digest in expected.items():
        path = snapshot / filename
        require(path.is_file(), f"SkillRouter embedding model file missing: {path}")
        require(sha256_file(path) == digest, f"SkillRouter embedding model file drift: {filename}")
    return {
        "path": str(snapshot),
        "revision": REVISION,
        "files": expected,
    }


def validate_authorisation(
    path: Path,
    payload_path: Path,
    *,
    root: Path,
    output_dir: Path,
    run_id: str,
    batch_size: int,
) -> dict[str, Any]:
    require(path.is_file(), f"SkillRouter embedding execution authorisation missing: {path}")
    value = read_json(path)
    require(value.get("schema_version") == "rq2b-skillrouter-embedding-execution-authorisation-v1", "Authorisation schema mismatch")
    require(value.get("state") == "explicitly_authorised_for_one_execution", "SkillRouter embedding run is not authorised")
    require(value.get("b0f_a1_amendment_sha256") == B0F_A1_AMENDMENT_SHA256, "Authorisation amendment mismatch")
    require(value.get("payload_manifest_sha256") == sha256_file(payload_path), "Authorisation payload mismatch")
    require(value.get("model") == MODEL and value.get("revision") == REVISION, "Authorisation model mismatch")
    require(value.get("dimensions") == DIMENSIONS, "Authorisation dimensions mismatch")
    require(value.get("maximum_model_tokens") == MAX_MODEL_TOKENS, "Authorisation token ceiling mismatch")
    require(value.get("runtime_dtype") == RUNTIME_DTYPE and value.get("runtime_device") == RUNTIME_DEVICE, "Authorisation runtime mismatch")
    require(value.get("batch_size") == batch_size and batch_size > 0, "Authorisation batch-size mismatch")
    require(value.get("run_id") == run_id, "Authorisation run-ID mismatch")
    require(value.get("output_dir") == relative(output_dir, root), "Authorisation output mismatch")
    require(value.get("automatic_retries") == 0, "Automatic retries are forbidden")
    require(value.get("scientific_execution_authorized") is True, "Scientific execution is not authorised")
    environment = value.get("execution_environment")
    require(environment in {"local_cuda", "approved_hosted_cuda"}, "Unknown execution environment")
    if environment == "approved_hosted_cuda":
        require(value.get("external_text_transfer_authorized") is True, "Hosted transfer is not authorised")
    for key in (
        "maximum_new_cache_entries",
        "maximum_model_input_instances",
        "maximum_model_forward_batches",
        "maximum_model_input_tokens",
        "maximum_cold_query_forwards",
    ):
        require(isinstance(value.get(key), int) and value[key] >= 0, f"Authorisation lacks {key}")
    return value


def last_token_pool(last_hidden_states: Any, attention_mask: Any) -> Any:
    import torch

    left_padding = bool(attention_mask[:, -1].sum().item() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    sequence_lengths = attention_mask.sum(dim=1) - 1
    batch_size = last_hidden_states.shape[0]
    return last_hidden_states[
        torch.arange(batch_size, device=last_hidden_states.device),
        sequence_lengths,
    ]


def encode_batch(tokenizer: Any, model: Any, batch: list[dict[str, Any]]) -> list[list[float]]:
    import torch
    import torch.nn.functional as functional

    encoded = tokenizer(
        [row["text"] for row in batch],
        padding=True,
        truncation=False,
        return_tensors="pt",
    )
    lengths = [int(value) for value in encoded["attention_mask"].sum(dim=1).tolist()]
    expected = [int(row["model_tokens"]) for row in batch]
    require(lengths == expected, "Runtime SkillRouter token counts differ from sealed payload")
    require(max(lengths) <= MAX_MODEL_TOKENS, "Runtime SkillRouter input exceeds full context")
    encoded = {key: value.to(model.device) for key, value in encoded.items()}
    with torch.inference_mode():
        outputs = model(**encoded)
        pooled = last_token_pool(outputs.last_hidden_state, encoded["attention_mask"])
        embeddings = functional.normalize(pooled.float(), p=2, dim=1)
    return [[float(item) for item in row] for row in embeddings.cpu().tolist()]


def embed_payload(
    text_rows: list[dict[str, Any]],
    *,
    tokenizer: Any,
    model: Any,
    cache: ExactEmbeddingCache,
    authorisation: dict[str, Any],
    batch_size: int,
    progress_root: Path,
) -> tuple[dict[str, list[float]], dict[str, Any]]:
    rows_by_id = {row["text_id"]: row for row in text_rows}
    require(len(rows_by_id) == len(text_rows), "SkillRouter embedding text IDs are not unique")
    document_rows = [row for row in text_rows if any(role["kind"] == "document" for role in row["roles"])]
    query_rows = [row for row in text_rows if any(role["kind"] == "query" for role in row["roles"])]
    require(len(query_rows) > 0, "SkillRouter embedding payload has no queries")
    cached = {row["text_id"]: cache.load(row["text"]) for row in text_rows}
    missing_documents = [row for row in document_rows if cached[row["text_id"]] is None]
    new_cache_ids = {
        row["text_id"]
        for row in [*missing_documents, *query_rows]
        if cached[row["text_id"]] is None
    }
    batches = [
        missing_documents[start : start + batch_size]
        for start in range(0, len(missing_documents), batch_size)
    ] + [[row] for row in query_rows]
    input_instances = sum(len(batch) for batch in batches)
    input_tokens = sum(int(row["model_tokens"]) for batch in batches for row in batch)
    require(len(new_cache_ids) <= authorisation["maximum_new_cache_entries"], "Cache misses exceed authorised ceiling")
    require(input_instances <= authorisation["maximum_model_input_instances"], "Model inputs exceed authorised ceiling")
    require(len(batches) <= authorisation["maximum_model_forward_batches"], "Model batches exceed authorised ceiling")
    require(input_tokens <= authorisation["maximum_model_input_tokens"], "Model tokens exceed authorised ceiling")
    require(len(query_rows) <= authorisation["maximum_cold_query_forwards"], "Cold query forwards exceed authorised ceiling")

    vectors = {
        row["text_id"]: cached[row["text_id"]]
        for row in document_rows
        if cached[row["text_id"]] is not None
    }
    records: list[dict[str, Any]] = []
    model_forward_seconds = 0.0
    started = time.perf_counter()
    document_batch_count = len(batches) - len(query_rows)
    for batch_index, batch in enumerate(batches):
        role = "document_batch" if batch_index < document_batch_count else "cold_query_single"
        base = {
            "schema_version": "rq2b-skillrouter-embedding-forward-record-v1",
            "batch_index": batch_index,
            "role": role,
            "text_ids": [row["text_id"] for row in batch],
            "text_count": len(batch),
            "model_input_tokens": sum(int(row["model_tokens"]) for row in batch),
            "automatic_retry": False,
        }
        attempt_path = progress_root / f"batch_{batch_index:05d}_attempt.json"
        write_json_new(attempt_path, {**base, "state": "forward_started"})
        print(f"SkillRouter embedding: {role} {batch_index + 1}/{len(batches)}, texts {len(batch)}", flush=True)
        batch_started = time.perf_counter()
        batch_vectors = encode_batch(tokenizer, model, batch)
        elapsed = time.perf_counter() - batch_started
        model_forward_seconds += elapsed
        require(len(batch_vectors) == len(batch), "SkillRouter embedding batch output count mismatch")
        cache_entries_written = 0
        for row, vector in zip(batch, batch_vectors, strict=True):
            vector = l2_normalize(vector)
            previous = cached[row["text_id"]]
            if previous is None:
                cache.store(row["text"], vector, model_tokens=int(row["model_tokens"]))
                cached[row["text_id"]] = vector
                cache_entries_written += 1
            else:
                require(
                    max(abs(left - right) for left, right in zip(vector, previous, strict=True)) <= 1e-4,
                    "Cold query forward differs from its persisted embedding",
                )
            vectors[row["text_id"]] = vector
        success_path = progress_root / f"batch_{batch_index:05d}_success.json"
        write_json_new(
            success_path,
            {
                **base,
                "state": "cache_commit_complete",
                "elapsed_seconds": elapsed,
                "cache_entries_written": cache_entries_written,
                "attempt_sha256": sha256_file(attempt_path),
            },
        )
        records.append(
            {
                **base,
                "elapsed_seconds": elapsed,
                "cache_entries_written": cache_entries_written,
                "attempt_path": attempt_path.name,
                "attempt_sha256": sha256_file(attempt_path),
                "success_path": success_path.name,
                "success_sha256": sha256_file(success_path),
            }
        )
    require(len(vectors) == len(text_rows), "SkillRouter embedding vector coverage is incomplete")
    return vectors, {
        "text_rows": len(text_rows),
        "cache_hits": len(text_rows) - len(new_cache_ids),
        "cache_misses": len(new_cache_ids),
        "document_cache_hits": len(document_rows) - len(missing_documents),
        "document_cache_misses": len(missing_documents),
        "cold_query_forwards": len(query_rows),
        "model_input_instances": input_instances,
        "model_input_tokens": input_tokens,
        "model_forward_batches": len(batches),
        "model_forward_seconds": model_forward_seconds,
        "elapsed_seconds": time.perf_counter() - started,
        "automatic_retries": 0,
        "batch_records": records,
    }


def score_payload(
    payload: dict[str, Any],
    vectors: dict[str, list[float]],
    prompts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    import numpy as np

    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    query_vectors = {
        prompt_id: np.asarray(l2_normalize(vectors[text_id]), dtype=np.float64)
        for prompt_id, text_id in payload["query_text_ids"].items()
    }
    rows: list[dict[str, Any]] = []
    for representation, documents in payload["documents"].items():
        skill_ids = [row["skill_id"] for row in documents]
        skill_index = {skill_id: index for index, skill_id in enumerate(skill_ids)}
        matrix = np.asarray(
            [l2_normalize(vectors[row["text_id"]]) for row in documents],
            dtype=np.float64,
        )
        require(matrix.shape == (len(documents), DIMENSIONS), "SkillRouter embedding score matrix mismatch")
        for prompt_id, query in query_vectors.items():
            started = time.perf_counter()
            scores = matrix @ query
            ranking = list(zip(skill_ids, (float(value) for value in scores), strict=True))
            ranking.sort(key=lambda item: (-item[1], item[0]))
            query_seconds = time.perf_counter() - started
            prompt = prompt_by_id[prompt_id]
            result = rank_row(
                prompt,
                ranking,
                representation=representation,
                query_seconds=query_seconds,
                retriever="skillrouter-embedding",
                runner_version=RUNNER_VERSION,
                aggregation="single_full_context_cosine",
            )
            gold = documents[skill_index[prompt["gold_skill"]]]
            result.update(
                {
                    "strict_gold_document_model_tokens": gold["model_tokens"],
                    "strict_gold_selector_utf8_bytes": gold["selector_utf8_bytes"],
                    "strict_gold_source_length_quartile": gold["source_length_quartile"],
                }
            )
            rows.append(result)
    return rows


def run(
    root: Path,
    payload_path: Path,
    authorisation_path: Path,
    model_snapshot: Path,
    output_dir: Path,
    run_id: str,
    batch_size: int,
) -> dict[str, Any]:
    import torch
    from transformers import AutoModel, AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    verify_frozen_manifest(root)
    verify_b0f_a1_amendment(root, require_approval=True)
    verify_b1s_implementation_seal(root)
    require(torch.cuda.is_available(), "Scientific SkillRouter embedding run requires CUDA")
    require(not output_dir.exists(), f"Refusing to overwrite SkillRouter embedding run: {output_dir}")
    staging = output_dir.parent / f".{output_dir.name}.staging"
    require(not staging.exists(), f"Stale SkillRouter embedding staging root: {staging}")
    payload = read_json(payload_path)
    require(payload.get("schema_version") == "rq2b-skillrouter-embedding-payload-manifest-v1", "Payload schema mismatch")
    require(payload.get("state") == "sealed_not_executed", "Payload state mismatch")
    require(payload.get("model") == MODEL and payload.get("revision") == REVISION, "Payload model mismatch")
    require(payload.get("maximum_model_tokens") == MAX_MODEL_TOKENS, "Payload context mismatch")
    authorisation = validate_authorisation(
        authorisation_path,
        payload_path,
        root=root,
        output_dir=output_dir,
        run_id=run_id,
        batch_size=batch_size,
    )
    snapshot_audit = verify_model_snapshot(model_snapshot)
    text_path = root / payload["text_inventory"]["path"]
    require(sha256_file(text_path) == payload["text_inventory"]["sha256"], "Payload text inventory drift")
    text_rows = read_jsonl(text_path)
    staging.mkdir(parents=True, exist_ok=False)
    progress_root = staging / "forward_records"
    progress_root.mkdir(parents=False, exist_ok=False)
    write_json_new(
        staging / "run_started.json",
        {
            "schema_version": "rq2b-skillrouter-embedding-run-start-v1",
            "version_id": VERSION_ID,
            "run_id": run_id,
            "payload_manifest_sha256": sha256_file(payload_path),
            "authorisation_sha256": sha256_file(authorisation_path),
            "batch_size": batch_size,
            "automatic_retries": 0,
        },
    )
    load_started = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(
        model_snapshot,
        local_files_only=True,
        trust_remote_code=True,
        padding_side="left",
    )
    model = AutoModel.from_pretrained(
        model_snapshot,
        local_files_only=True,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    ).eval().to("cuda")
    model_load_seconds = time.perf_counter() - load_started
    cache = ExactEmbeddingCache(root / "skill_benchmark/cache/rq2b/embeddings")
    vectors, embedding_ledger = embed_payload(
        text_rows,
        tokenizer=tokenizer,
        model=model,
        cache=cache,
        authorisation=authorisation,
        batch_size=batch_size,
        progress_root=progress_root,
    )
    prompts = annotate_unresolved_public_equivalents(
        read_jsonl(version_root(root) / "prompt_manifest.jsonl"),
        read_jsonl(version_root(root) / "source_manifest.jsonl"),
    )
    scoring_started = time.perf_counter()
    result_rows = score_payload(payload, vectors, prompts)
    scoring_seconds = time.perf_counter() - scoring_started
    rows_path = staging / "rows.jsonl"
    ledger_path = staging / "embedding_ledger.json"
    write_jsonl_new(rows_path, result_rows)
    write_json_new(
        ledger_path,
        {
            **embedding_ledger,
            "model_load_seconds": model_load_seconds,
            "vector_search_seconds": scoring_seconds,
        },
    )
    manifest = {
        "schema_version": "rq2b-skillrouter-embedding-run-manifest-v1",
        "version_id": VERSION_ID,
        "state": "complete_scientific_b1_skillrouter_embedding",
        "run_id": run_id,
        "runner_version": RUNNER_VERSION,
        "retriever": "skillrouter-embedding",
        "model": MODEL,
        "revision": REVISION,
        "dimensions": DIMENSIONS,
        "maximum_model_tokens": MAX_MODEL_TOKENS,
        "pooling": "last_non_padding_token",
        "normalization": "l2",
        "aggregation": "single_full_context_cosine",
        "runtime_dtype": RUNTIME_DTYPE,
        "runtime_device": RUNTIME_DEVICE,
        "query_instruction": QUERY_INSTRUCTION,
        "automatic_retries": 0,
        "b0f_a1_amendment_sha256": B0F_A1_AMENDMENT_SHA256,
        "payload_manifest_path": relative(payload_path, root),
        "payload_manifest_sha256": sha256_file(payload_path),
        "authorisation_path": relative(authorisation_path, root),
        "authorisation_sha256": sha256_file(authorisation_path),
        "model_snapshot": snapshot_audit,
        "embedding_ledger": {**embedding_ledger, "model_load_seconds": model_load_seconds, "vector_search_seconds": scoring_seconds},
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
                "path": relative(output_dir / "run_started.json", root),
                "sha256": sha256_file(staging / "run_started.json"),
            },
            "forward_records": [
                {"path": relative(output_dir / "forward_records" / path.name, root), "sha256": sha256_file(path)}
                for path in sorted(progress_root.glob("*.json"))
            ],
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_dir)
    return manifest


def self_test() -> dict[str, Any]:
    def vector(first: float, second: float) -> list[float]:
        return l2_normalize([first, second, *([0.0] * (DIMENSIONS - 2))])

    query = vector(1.0, 0.0)
    with tempfile.TemporaryDirectory() as directory:
        cache = ExactEmbeddingCache(Path(directory))
        text = "synthetic document"
        require(cache.load(text) is None, "Empty SkillRouter embedding cache regression")
        cache.store(text, query, model_tokens=2)
        require(cache.load(text) == query, "SkillRouter embedding cache round-trip regression")
    payload = {
        "query_text_ids": {"p1": "q"},
        "documents": {
            "i1-discovery": [
                {"skill_id": "s0", "text_id": "d0", "model_tokens": 2, "selector_utf8_bytes": 2, "source_length_quartile": "q1"},
                {"skill_id": "s1", "text_id": "d1", "model_tokens": 2, "selector_utf8_bytes": 2, "source_length_quartile": "q1"},
            ]
        },
    }
    vectors = {"q": query, "d0": vector(1.0, 0.0), "d1": vector(0.0, 1.0)}
    prompts = [
        {
            "prompt_id": "p1",
            "stratum": "controlled",
            "group": "g1",
            "prompt_sha256": sha256_text("query"),
            "gold_skill": "s0",
            "valid_skills": ["s0"],
            "closest_alternatives": ["s1"],
        }
    ]
    rows = score_payload(payload, vectors, prompts)
    require(len(rows) == 1 and rows[0]["strict_hit_at_1"] == 1, "SkillRouter embedding scoring regression")
    require(cache_key("x") != cache_key("y"), "SkillRouter embedding cache-key regression")
    return {
        "state": "synthetic_no_model_forward_no_scientific_result",
        "network_calls": 0,
        "cache_roundtrip": True,
        "single_full_context_scoring": True,
        "query_instruction_sha256": sha256_text(QUERY_INSTRUCTION),
        "maximum_model_tokens": MAX_MODEL_TOKENS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--payload-manifest", type=Path)
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--model-snapshot", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.execute, "SkillRouter embedding execution requires --execute")
        require(args.payload_manifest is not None, "--payload-manifest is required")
        require(args.authorisation is not None, "--authorisation is required")
        require(args.model_snapshot is not None, "--model-snapshot is required")
        require(args.output_dir is not None, "--output-dir is required")
        require(args.run_id is not None, "--run-id is required")
        root = args.root.resolve()
        result = run(
            root,
            args.payload_manifest if args.payload_manifest.is_absolute() else root / args.payload_manifest,
            args.authorisation if args.authorisation.is_absolute() else root / args.authorisation,
            args.model_snapshot.expanduser().resolve(),
            args.output_dir if args.output_dir.is_absolute() else root / args.output_dir,
            args.run_id,
            args.batch_size,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
