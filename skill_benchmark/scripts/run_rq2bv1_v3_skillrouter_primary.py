#!/usr/bin/env python3
"""Run one approved hosted-CUDA embedding pass for the frozen RQ2b V3 payload.

The runner intentionally embeds only the sealed text inventory.  It never
loads gold labels or ranks candidates: the local finalizer performs those steps
after the returned cache and forward records have been persisted.  ``--execute``
is fail-closed and requires an exact user approval receipt.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from rq2bv1_v3_skillrouter_primary_constants import (
    CACHE_ROOT,
    DIMENSIONS,
    EXECUTION_PACKET_NAME,
    MAX_MODEL_TOKENS,
    MODEL,
    MODEL_CONFIG_SHA256,
    MODEL_FILE_SHA256,
    MODEL_WEIGHTS_SHA256,
    PREFLIGHT_ROOT,
    QUERY_INSTRUCTION,
    RESULT_ROOT,
    REVISION,
    TOKENIZER_SHA256,
)
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, sha256_json, sha256_text, write_json_new


RUNNER_VERSION = "rq2bv1-v3-skillrouter-primary-hosted-embedding-runner-v1"
AUTHORISATION_DEFAULT = "skill_benchmark/rq2bv1/approvals/skillrouter_primary_v3_execution_authorisation.json"
HOSTED_OUTPUT_ROOT = f"{RESULT_ROOT}/hosted_embedding"


def _path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _normalise(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in values))
    require(math.isfinite(norm) and norm > 0.0, "SkillRouter embedding has invalid norm")
    return [value / norm for value in values]


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
            "normalisation": "l2",
            "runtime_dtype": "bfloat16",
            "text_sha256": sha256_text(text),
        }
    )


class ExactEmbeddingCache:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, text: str) -> Path:
        return self.root / f"{cache_key(text)}.json"

    def load(self, text: str) -> list[float] | None:
        path = self.path(text)
        if not path.is_file():
            return None
        value = read_json(path)
        require(value.get("schema_version") == "rq2bv1-v3-skillrouter-primary-cache-v1", f"Cache schema drift: {path}")
        require(value.get("cache_key") == cache_key(text), f"Cache key drift: {path}")
        require(value.get("text_sha256") == sha256_text(text), f"Cache text drift: {path}")
        require(value.get("model") == MODEL and value.get("revision") == REVISION, f"Cache model drift: {path}")
        vector = [float(item) for item in value.get("embedding", [])]
        require(len(vector) == DIMENSIONS and all(math.isfinite(item) for item in vector), f"Cache vector drift: {path}")
        return vector

    def store(self, text: str, vector: list[float], *, model_tokens: int) -> None:
        path = self.path(text)
        require(not path.exists(), f"Refusing to overwrite embedding cache: {path}")
        write_json_new(
            path,
            {
                "schema_version": "rq2bv1-v3-skillrouter-primary-cache-v1",
                "cache_key": cache_key(text),
                "model": MODEL,
                "revision": REVISION,
                "dimensions": DIMENSIONS,
                "maximum_model_tokens": MAX_MODEL_TOKENS,
                "tokenizer_sha256": TOKENIZER_SHA256,
                "model_config_sha256": MODEL_CONFIG_SHA256,
                "model_weights_sha256": MODEL_WEIGHTS_SHA256,
                "pooling": "last_non_padding_token",
                "normalisation": "l2",
                "runtime_dtype": "bfloat16",
                "text_sha256": sha256_text(text),
                "model_tokens": int(model_tokens),
                "embedding": _normalise(vector),
            },
        )


def _validate_snapshot(snapshot: Path) -> dict[str, Any]:
    expected = MODEL_FILE_SHA256
    for filename, digest in expected.items():
        path = snapshot / filename
        require(path.is_file(), f"SkillRouter model file missing: {path}")
        require(sha256_file(path) == digest, f"SkillRouter model file hash drift: {filename}")
    return {
        "path": str(snapshot),
        "model": MODEL,
        "revision": REVISION,
        "files": expected,
        "trust_remote_code": False,
    }


def _load_packet(root: Path) -> tuple[Path, dict[str, Any]]:
    path = root / PREFLIGHT_ROOT / EXECUTION_PACKET_NAME
    packet = read_json(path)
    require(
        packet.get("schema_version") == "rq2bv1-v3-skillrouter-primary-execution-approval-packet-v1",
        "SkillRouter execution packet schema mismatch",
    )
    require(
        packet.get("state") == "awaiting_explicit_model_download_and_hosted_cuda_transfer_authorisation",
        "SkillRouter execution packet is not awaiting approval",
    )
    return path, packet


def _validate_authorisation(root: Path, path: Path, packet_path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    require(path.is_file(), "SkillRouter execution is not authorised: receipt is absent")
    value = read_json(path)
    require(
        value.get("schema_version") == "rq2bv1-v3-skillrouter-primary-execution-authorisation-v1",
        "SkillRouter execution authorisation schema mismatch",
    )
    require(
        value.get("state") == "explicitly_authorised_for_one_hosted_skillrouter_primary_v3_execution",
        "SkillRouter execution is not authorised",
    )
    require(
        value.get("approved_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "SkillRouter execution packet binding mismatch",
    )
    for key in ("run_id", "output_dir", "cache_root", "execution_environment"):
        require(value.get(key) == packet.get(key), f"SkillRouter authorisation mismatch: {key}")
    for key in (
        "model_download_authorised",
        "external_text_transfer_authorised",
        "hosted_cuda_authorised",
        "hosted_checkpoint_persistence_authorised",
        "scientific_execution_authorised",
    ):
        require(value.get(key) is True, f"SkillRouter authorisation lacks {key}")
    require(value.get("automatic_retries") == 0, "Automatic retries are forbidden")
    for key in (
        "maximum_new_cache_entries",
        "maximum_model_input_instances",
        "maximum_model_input_tokens",
        "maximum_model_forward_batches",
        "maximum_cold_query_forwards",
    ):
        require(value.get(key) == packet["execution_ceiling_without_cache"][key], f"SkillRouter ceiling mismatch: {key}")
    persistence = packet["hosting_and_persistence"]
    for key in (
        "checkpoint_dataset_repository",
        "input_bundle_path",
        "output_prefix",
        "job_image",
        "job_flavor",
        "job_timeout",
        "maximum_hardware_cost_usd",
    ):
        require(value.get(key) == persistence.get(key), f"SkillRouter hosted persistence mismatch: {key}")
    require(
        value.get("checkpoint_every_model_forward_batches")
        == persistence["checkpoint_protocol"]["checkpoint_every_model_forward_batches"],
        "SkillRouter hosted checkpoint cadence mismatch",
    )
    return value


def _validate_payload(root: Path, packet: dict[str, Any]) -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    path = root / str(packet["payload"]["path"])
    require(sha256_file(path) == packet["payload"]["sha256"], "SkillRouter payload hash drift")
    payload = read_json(path)
    require(
        payload.get("schema_version") == "rq2bv1-v3-skillrouter-primary-payload-v1"
        and payload.get("state") == "sealed_not_executed",
        "SkillRouter payload schema/state mismatch",
    )
    require(payload.get("model") == MODEL and payload.get("revision") == REVISION, "SkillRouter payload model drift")
    require(int(payload.get("maximum_model_tokens")) == MAX_MODEL_TOKENS, "SkillRouter payload context limit drift")
    require(payload.get("query_instruction") == QUERY_INSTRUCTION, "SkillRouter query instruction drift")
    require(payload.get("strict_population") == {
        "candidate_library_skills": 2433,
        "strict_prompts": 381,
        "representations": ["i1-discovery", "i2-original", "i3-flat-evidence", "i3c-fielded-evidence"],
        "expected_primary_result_rows": 1524,
    }, "SkillRouter strict population drift")
    inventory_path = root / str(payload["text_inventory"]["path"])
    require(sha256_file(inventory_path) == payload["text_inventory"]["sha256"], "SkillRouter text inventory hash drift")
    rows = read_jsonl(inventory_path)
    require(len(rows) == int(payload["text_inventory"]["rows"]), "SkillRouter text inventory count drift")
    by_id = {str(row["text_id"]): row for row in rows}
    require(len(by_id) == len(rows), "SkillRouter text inventory IDs are not unique")
    for text_id, row in by_id.items():
        require(
            set(row) == {"schema_version", "text_id", "text_sha256", "text", "utf8_bytes", "model_tokens", "roles"},
            f"SkillRouter inventory schema drift: {text_id}",
        )
        require(row["schema_version"] == "rq2bv1-v3-skillrouter-primary-text-v1", f"SkillRouter inventory version drift: {text_id}")
        require(row["text_id"] == text_id == row["text_sha256"] == sha256_text(row["text"]), f"SkillRouter text hash drift: {text_id}")
        require(int(row["utf8_bytes"]) == len(row["text"].encode("utf-8")), f"SkillRouter text byte drift: {text_id}")
        require(0 < int(row["model_tokens"]) <= MAX_MODEL_TOKENS, f"SkillRouter token limit drift: {text_id}")
    scheduled = [
        *payload.get("document_forward_schedule", []),
        *payload.get("cold_query_forward_schedule", []),
    ]
    scheduled_ids = [text_id for batch in scheduled for text_id in batch["text_ids"]]
    require(len(scheduled_ids) == len(set(scheduled_ids)) == len(rows), "SkillRouter schedule identity drift")
    require(set(scheduled_ids) == set(by_id), "SkillRouter schedule coverage drift")
    for batch in scheduled:
        require(set(batch) == {"kind", "text_ids", "items", "maximum_model_tokens", "padded_model_tokens"}, "SkillRouter batch schema drift")
        require(int(batch["items"]) == len(batch["text_ids"]) > 0, "SkillRouter batch count drift")
        lengths = [int(by_id[text_id]["model_tokens"]) for text_id in batch["text_ids"]]
        require(max(lengths) == int(batch["maximum_model_tokens"]), "SkillRouter batch max token drift")
        require(int(batch["padded_model_tokens"]) == len(lengths) * max(lengths), "SkillRouter padded token drift")
    return path, payload, rows


def _last_token_pool(last_hidden_states: Any, attention_mask: Any) -> Any:
    import torch

    if bool(attention_mask[:, -1].sum().item() == attention_mask.shape[0]):
        return last_hidden_states[:, -1]
    positions = attention_mask.sum(dim=1) - 1
    return last_hidden_states[torch.arange(last_hidden_states.shape[0], device=last_hidden_states.device), positions]


def _embed_batch(tokenizer: Any, model: Any, batch: list[dict[str, Any]]) -> list[list[float]]:
    import torch.nn.functional as functional

    encoded = tokenizer(
        [str(row["text"]) for row in batch],
        padding=True,
        truncation=False,
        return_tensors="pt",
    )
    lengths = [int(value) for value in encoded["attention_mask"].sum(dim=1).tolist()]
    expected = [int(row["model_tokens"]) for row in batch]
    require(lengths == expected, "Runtime tokenizer count differs from sealed payload")
    require(max(lengths) <= MAX_MODEL_TOKENS, "Runtime input exceeds full-context limit")
    encoded = {key: value.to(model.device) for key, value in encoded.items()}
    with __import__("torch").inference_mode():
        outputs = model(**encoded)
        pooled = _last_token_pool(outputs.last_hidden_state, encoded["attention_mask"])
        vectors = functional.normalize(pooled, p=2, dim=1).float().cpu().tolist()
    require(len(vectors) == len(batch) and all(len(vector) == DIMENSIONS for vector in vectors), "SkillRouter output dimension drift")
    return [[float(value) for value in vector] for vector in vectors]


def _prepare_staging(output_root: Path, *, resume: bool, run_started: dict[str, Any]) -> Path:
    require(not output_root.exists(), f"Refusing to overwrite hosted embedding output: {output_root}")
    staging = output_root.parent / f".{output_root.name}.staging"
    if staging.exists():
        require(resume, f"Stale hosted embedding staging root: {staging}; pass --resume only after inspection")
        existing = read_json(staging / "run_started.json")
        require(existing == run_started, "Hosted resume binding drift")
    else:
        require(not resume, "Cannot resume absent hosted embedding staging root")
        staging.mkdir(parents=True, exist_ok=False)
        (staging / "forward_records").mkdir(parents=False, exist_ok=False)
        write_json_new(staging / "run_started.json", run_started)
    return staging


def _checkpoint_after_forward(root: Path, record_id: str) -> None:
    """Invoke the bound hosted persistence hook, if this run supplied one.

    The hook is deliberately a synchronous subprocess.  A failed archive upload
    aborts this runner before the next CUDA forward, rather than silently
    creating unpersisted model work that could not be resumed later.
    """

    hook = os.environ.get("RQ2BV1_SKILLROUTER_CHECKPOINT_HOOK")
    if not hook:
        return
    hook_path = Path(hook).expanduser().resolve()
    require(hook_path.is_file(), f"SkillRouter checkpoint hook is missing: {hook_path}")
    subprocess.run(
        [sys.executable, str(hook_path), "--checkpoint-hook", "--root", str(root), "--record-id", record_id],
        check=True,
    )


def run(root: Path, authorisation_path: Path, model_snapshot: Path, *, resume: bool) -> dict[str, Any]:
    import torch
    from transformers import AutoModel, AutoTokenizer

    require(torch.cuda.is_available(), "Native SkillRouter B1 requires CUDA; this machine is not an execution host")
    packet_path, packet = _load_packet(root)
    authorisation = _validate_authorisation(root, authorisation_path, packet_path, packet)
    payload_path, payload, text_rows = _validate_payload(root, packet)
    snapshot = _validate_snapshot(model_snapshot)
    output_root = root / str(packet["output_dir"])
    cache = ExactEmbeddingCache(root / str(packet["cache_root"]))
    run_started = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hosted-run-start-v1",
        "run_id": packet["run_id"],
        "payload": {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
        "model_snapshot": snapshot,
        "automatic_retries": 0,
    }
    staging = _prepare_staging(output_root, resume=resume, run_started=run_started)
    by_id = {str(row["text_id"]): row for row in text_rows}
    schedule = [
        *payload["document_forward_schedule"],
        *payload["cold_query_forward_schedule"],
    ]
    existing_records = {path.stem for path in (staging / "forward_records").glob("*.json")}
    cache_hits = 0
    cache_misses = 0
    document_hits = 0
    document_misses = 0
    query_hits = 0
    query_misses = 0
    model_inputs = 0
    input_tokens = 0
    forward_batches = 0
    load_started = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(model_snapshot, local_files_only=True, trust_remote_code=False, padding_side="left")
    model = AutoModel.from_pretrained(
        model_snapshot,
        local_files_only=True,
        trust_remote_code=False,
        torch_dtype=torch.bfloat16,
    ).eval().to("cuda")
    model_load_seconds = time.perf_counter() - load_started
    for index, batch_spec in enumerate(schedule, start=1):
        record_id = f"forward-{index:05d}"
        batch = [by_id[text_id] for text_id in batch_spec["text_ids"]]
        cached = [cache.load(str(row["text"])) for row in batch]
        kind = str(batch_spec["kind"])
        if all(vector is not None for vector in cached):
            cache_hits += len(batch)
            if kind == "document":
                document_hits += len(batch)
            else:
                query_hits += len(batch)
            continue
        require(all(vector is None for vector in cached), f"Partial-cache batch is forbidden: {record_id}")
        require(record_id not in existing_records, f"Forward record exists but cache is incomplete: {record_id}")
        cache_misses += len(batch)
        model_inputs += len(batch)
        input_tokens += sum(int(row["model_tokens"]) for row in batch)
        forward_batches += 1
        if kind == "document":
            document_misses += len(batch)
        else:
            query_misses += len(batch)
        require(cache_misses <= int(authorisation["maximum_new_cache_entries"]), "New cache-entry ceiling exceeded")
        require(model_inputs <= int(authorisation["maximum_model_input_instances"]), "Model-input ceiling exceeded")
        require(input_tokens <= int(authorisation["maximum_model_input_tokens"]), "Model-token ceiling exceeded")
        require(forward_batches <= int(authorisation["maximum_model_forward_batches"]), "Forward-batch ceiling exceeded")
        require(query_misses <= int(authorisation["maximum_cold_query_forwards"]), "Cold-query ceiling exceeded")
        started = time.perf_counter()
        vectors = _embed_batch(tokenizer, model, batch)
        elapsed = time.perf_counter() - started
        for row, vector in zip(batch, vectors, strict=True):
            cache.store(str(row["text"]), vector, model_tokens=int(row["model_tokens"]))
        write_json_new(
            staging / "forward_records" / f"{record_id}.json",
            {
                "schema_version": "rq2bv1-v3-skillrouter-primary-forward-record-v1",
                "record_id": record_id,
                "kind": kind,
                "text_ids": list(batch_spec["text_ids"]),
                "items": len(batch),
                "model_input_tokens": sum(int(row["model_tokens"]) for row in batch),
                "padded_model_tokens": int(batch_spec["padded_model_tokens"]),
                "elapsed_seconds": elapsed,
            },
        )
        _checkpoint_after_forward(root, record_id)
    require(all(cache.load(str(row["text"])) is not None for row in text_rows), "Hosted cache coverage incomplete")
    ledger = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hosted-embedding-ledger-v1",
        "cache_hits": cache_hits,
        "cache_misses": cache_misses,
        "document_cache_hits": document_hits,
        "document_cache_misses": document_misses,
        "query_cache_hits": query_hits,
        "query_cache_misses": query_misses,
        "model_input_instances": model_inputs,
        "model_input_tokens": input_tokens,
        "model_forward_batches": forward_batches,
        "model_load_seconds": model_load_seconds,
        "automatic_retries": 0,
        "warm_cache_entries_verified": len(text_rows),
    }
    ledger_path = staging / "embedding_ledger.json"
    write_json_new(ledger_path, ledger)
    manifest = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hosted-embedding-manifest-v1",
        "state": "hosted_embedding_complete_pending_local_scoring",
        "run_id": packet["run_id"],
        "runner_version": RUNNER_VERSION,
        "payload": run_started["payload"],
        "authorisation": run_started["authorisation"],
        "model_snapshot": snapshot,
        "cache_root": str(packet["cache_root"]),
        "embedding_ledger": {"path": relative(output_root / ledger_path.name, root), "sha256": sha256_file(ledger_path)},
        "forward_records": [
            {"path": relative(output_root / "forward_records" / path.name, root), "sha256": sha256_file(path)}
            for path in sorted((staging / "forward_records").glob("*.json"))
        ],
        "hosted_scoring": False,
        "gold_labels_transferred": False,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.rename(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    with __import__("tempfile").TemporaryDirectory() as directory:
        cache = ExactEmbeddingCache(Path(directory))
        vector = [1.0, 0.0, *([0.0] * (DIMENSIONS - 2))]
        cache.store("synthetic document", vector, model_tokens=2)
        require(cache.load("synthetic document") == vector, "Cache round-trip regression")
    require(cache_key("a") != cache_key("b"), "Cache-key text isolation regression")
    return {
        "schema_version": "rq2bv1-v3-skillrouter-primary-hosted-runner-self-test-v1",
        "state": "self_test_passed_no_network_no_model_forward",
        "network_calls": 0,
        "scientific_retrieval_or_reranking": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorisation", type=Path, default=Path(AUTHORISATION_DEFAULT))
    parser.add_argument("--model-snapshot", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.execute, "Choose exactly one of --self-test or --execute")
    if args.self_test:
        result = self_test()
    else:
        require(args.model_snapshot is not None, "--model-snapshot is required for hosted execution")
        root = args.root.resolve()
        result = run(root, _path(root, args.authorisation), args.model_snapshot.expanduser().resolve(), resume=args.resume)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
