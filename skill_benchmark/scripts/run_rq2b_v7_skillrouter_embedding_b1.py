#!/usr/bin/env python3
"""Run the four Phase-8-released V7 SkillRouter embedding B1 cells.

The runner is deliberately inert unless a separate root-release authorisation
binds an exact Phase-8 payload.  The payload is the only data intake.  It must
name the label-free query runtime, source and condition manifests, and the four
final representation artifacts with exact hashes.  In particular, final V4.1
I3 hashes are supplied by that later payload and are not constants in this
implementation.

Scientific execution is MPS/default-SDPA/bfloat16 only.  It uses exact model-
input-length, unpadded batches, released query instruction, last-token pooling,
1,024-dimensional L2-normalised embeddings, complete 7,500-content-token
windows with at most 256 content-token overlap, and maximum query-to-window
cosine.  Window construction excludes tokenizer special tokens; separately
bound model inputs include them and must fit the 32,768-token checkpoint limit.
There is no automatic retry or device/dtype/attention fallback.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import platform
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from rq2b_v7_exact_chunking_v2 import CHUNKER_VERSION, exact_text_chunks


RUNNER_VERSION = "rq2b-v7-skillrouter-embedding-b1-runner-v1"
PAYLOAD_SCHEMA = "rq2b-v7-skillrouter-embedding-b1-phase8-payload-v1"
AUTHORISATION_SCHEMA = "rq2b-v7-skillrouter-embedding-b1-root-release-v1"
ROW_SCHEMA = "rq2b-v7-b1-runner-output-v1"
MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
REVISION = "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
DIMENSIONS = 1024
WINDOW_TOKENS = 7500
OVERLAP_TOKENS = 256
MODEL_MAX_TOKENS = 32768
MAX_BATCH_SIZE = 16
TOP_K = 100
EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
QUERY_INSTRUCTION = (
    "Instruct: Given a task description, retrieve the most relevant "
    "skill document that would help an agent complete the task\nQuery:"
)

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl"
)
SOURCE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/source_manifest.jsonl"
)
CONDITIONS_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl"
)
WINDOW_AMENDMENT_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_skillrouter_embedding_window_amendment_2026_09_09_v1/"
    "method_amendment.json"
)
FIXED_INPUT_SHA256 = {
    RUNTIME_REL: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    SOURCE_REL: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    CONDITIONS_REL: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
}
FIXED_REPRESENTATION_INPUTS = {
    "I1-discovery": {
        "path": (
            "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/"
            "i1-discovery.jsonl"
        ),
        "sha256": "0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd",
    },
    "I2-original": {
        "path": (
            "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/"
            "i2-original.jsonl"
        ),
        "sha256": "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
    },
}
REPRESENTATION_CELLS = {
    "I1-discovery": "B03",
    "I2-original": "B06",
    "I3C-fielded": "B09",
    "I3-flat": "B12",
}
MODEL_FILE_SHA256 = {
    "added_tokens.json": "c0284b582e14987fbd3d5a2cb2bd139084371ed9acbae488829a1c900833c680",
    "config.json": "02b34f6be10ee6a35304e32b67ac37be4b2b04e327efff49a689136b0913a0e8",
    "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "model.safetensors": "cbab45b8a3c786b8c23aedb24fb22aff74d0e9b62a52369a3090c37f26b00360",
    "special_tokens_map.json": "76862e765266b85aa9459767e33cbaf13970f327a0e88d1c65846c2ddd3a1ecd",
    "tokenizer.json": "def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a",
    "tokenizer_config.json": "7f33cbb21bae9b2ed4a7396d68f9f10d6280d75332d04911cd6c5a0967bd10c9",
    "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
}
HEX = set("0123456789abcdef")
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}
ROW_KEYS = {
    "schema_version", "status", "run_id", "condition_id",
    "first_stage_cell_id", "prompt_id", "prompt_sha256", "representation",
    "retriever", "persisted_candidate_source", "source_union_sha256",
    "top_k", "score_semantics", "top20_binding_sha256",
    "ranked_candidates", "cost",
}
COST_KEYS = {
    "wall_time_ms", "provider_calls", "input_tokens", "output_tokens",
    "window_forwards", "cache_hits", "retry_count", "timeout_count",
    "failure_count",
}
CEILING_KEYS = {
    "maximum_new_cache_entries", "maximum_model_input_instances",
    "maximum_model_input_tokens", "maximum_model_forward_batches",
    "maximum_wall_time_seconds",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def root_path(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: non-empty relative path required")
    raw = Path(value)
    require(not raw.is_absolute(), f"{field}: absolute paths are forbidden")
    resolved = (root / raw).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return resolved


def exact_keys(value: Any, expected: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: object required")
    missing = expected - set(value)
    extra = set(value) - expected
    require(not missing and not extra, f"{field}: missing={sorted(missing)} extra={sorted(extra)}")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path}: JSON object required")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"{path}:{line_number}: blank row")
            value = json.loads(raw)
            require(isinstance(value, dict), f"{path}:{line_number}: object required")
            rows.append(value)
    return rows


def write_json_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_deterministic_jsonl_gzip(
    path: Path, rows: Iterable[dict[str, Any]]
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    uncompressed = hashlib.sha256()
    uncompressed_bytes = 0
    row_count = 0
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            for row in rows:
                encoded = (
                    json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode("utf-8")
                compressed.write(encoded)
                uncompressed.update(encoded)
                uncompressed_bytes += len(encoded)
                row_count += 1
    return {
        "path": str(path),
        "sha256": file_sha256(path),
        "rows": row_count,
        "utf8_bytes_compressed": path.stat().st_size,
        "canonical_jsonl_sha256_uncompressed": uncompressed.hexdigest(),
        "utf8_bytes_uncompressed": uncompressed_bytes,
        "compression": "gzip-mtime-0",
        "jsonl_serialization": "utf8-sort-keys-compact-lf-v1",
    }


def normalized_key_tokens(key: str) -> set[str]:
    normalized = key.lower().replace("-", "_").replace(" ", "_")
    tokens = set(normalized.split("_")) | {normalized}
    for phrase in ("ground_truth", "a_q", "j_q", "d_q"):
        if phrase in normalized:
            tokens.add(phrase)
    return tokens


def reject_outcome_keys(value: Any, location: str = "input") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            # I3 source-only rows legitimately carry the serializer field name.
            if str(key) != "field_label":
                require(
                    not (normalized_key_tokens(str(key)) & PROHIBITED_KEY_TOKENS),
                    f"{location}: prohibited outcome key {key!r}",
                )
            reject_outcome_keys(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_outcome_keys(child, f"{location}[{index}]")


def validate_artifact(
    root: Path, artifact: Any, *, field: str, rows: int | None = None
) -> Path:
    exact_keys(artifact, {"path", "sha256", "rows"}, field)
    require(is_sha256(artifact["sha256"]), f"{field}: invalid SHA-256")
    if rows is not None:
        require(artifact["rows"] == rows, f"{field}: row count binding drift")
    path = root_path(root, artifact["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: missing artifact")
    require(file_sha256(path) == artifact["sha256"], f"{field}: artifact hash drift")
    return path


def validate_payload(root: Path, path: Path) -> dict[str, Any]:
    payload = read_json(path)
    exact_keys(
        payload,
        {"schema_version", "state", "runner_version", "implementation", "phase8",
         "inputs", "counts", "method", "label_isolation"},
        "payload",
    )
    require(payload["schema_version"] == PAYLOAD_SCHEMA, "Payload schema drift")
    require(payload["state"] == "SEALED_LABEL_FREE_PHASE8_PAYLOAD", "Payload is not Phase-8 sealed")
    require(payload["runner_version"] == RUNNER_VERSION, "Payload runner version drift")

    implementation = payload["implementation"]
    exact_keys(implementation, {"runner", "chunker"}, "payload.implementation")
    expected_implementation = {
        "runner": Path(__file__).resolve(),
        "chunker": root / "skill_benchmark/scripts/rq2b_v7_exact_chunking_v2.py",
    }
    for name, expected_path in expected_implementation.items():
        item = implementation[name]
        exact_keys(item, {"path", "sha256"}, f"payload.implementation.{name}")
        require(root_path(root, item["path"], field=f"implementation.{name}.path") == expected_path.resolve(), f"Implementation path drift: {name}")
        require(item["sha256"] == file_sha256(expected_path), f"Implementation hash drift: {name}")

    phase8 = payload["phase8"]
    exact_keys(
        phase8,
        {"status", "receipt", "final_v4_1_i3_hashes_bound"},
        "payload.phase8",
    )
    require(phase8["status"] == "PASS", "Payload Phase-8 status is not PASS")
    require(phase8["final_v4_1_i3_hashes_bound"] is True, "Final V4.1 I3 hashes are not bound")
    validate_artifact(root, {**phase8["receipt"], "rows": 1}, field="payload.phase8.receipt", rows=1)

    inputs = payload["inputs"]
    exact_keys(inputs, {"runtime", "source_manifest", "conditions", "representations"}, "payload.inputs")
    fixed = {
        "runtime": (RUNTIME_REL, EXPECTED_QUERIES),
        "source_manifest": (SOURCE_REL, EXPECTED_SOURCES),
        "conditions": (CONDITIONS_REL, 36),
    }
    for name, (rel_path, rows) in fixed.items():
        item = inputs[name]
        require(item == {"path": rel_path.as_posix(), "sha256": FIXED_INPUT_SHA256[rel_path], "rows": rows}, f"Fixed payload input drift: {name}")
        validate_artifact(root, item, field=f"payload.inputs.{name}", rows=rows)
    representations = inputs["representations"]
    exact_keys(representations, set(REPRESENTATION_CELLS), "payload.inputs.representations")
    for representation, item in representations.items():
        exact_keys(
            item,
            {"path", "sha256", "rows", "phase8_final", "extraction_protocol"},
            f"payload.inputs.representations.{representation}",
        )
        require(item["rows"] == EXPECTED_SOURCES and item["phase8_final"] is True, f"{representation}: representation is not final 3,798-row Phase-8 input")
        if representation in FIXED_REPRESENTATION_INPUTS:
            expected = FIXED_REPRESENTATION_INPUTS[representation]
            require(item["path"] == expected["path"] and item["sha256"] == expected["sha256"], f"{representation}: frozen I1/I2 binding drift")
            require(item["extraction_protocol"] == "SOURCE_NATIVE_PHASE7_V2", f"{representation}: protocol drift")
        else:
            require(item["extraction_protocol"] == "I3C_SUBAGENT_EXTRACTION_V4_1", f"{representation}: final V4.1 protocol binding missing")
        validate_artifact(root, {"path": item["path"], "sha256": item["sha256"], "rows": item["rows"]}, field=f"payload.inputs.representations.{representation}", rows=EXPECTED_SOURCES)

    require(payload["counts"] == {
        "queries": EXPECTED_QUERIES,
        "sources": EXPECTED_SOURCES,
        "representations": 4,
        "b1_cells": 4,
        "b1_output_rows": 4 * EXPECTED_QUERIES,
    }, "Payload counts drift")
    require(payload["method"] == {
        "model": MODEL,
        "revision": REVISION,
        "query_instruction": QUERY_INSTRUCTION,
        "pooling": "last_non_padding_token",
        "dimensions": DIMENSIONS,
        "normalization": "l2",
        "window_tokens": WINDOW_TOKENS,
        "overlap_tokens": OVERLAP_TOKENS,
        "window_token_basis": "content_tokens_add_special_tokens_false",
        "overlap_token_basis": "content_tokens_add_special_tokens_false",
        "model_input_token_basis": "tokenizer_add_special_tokens_true",
        "model_maximum_tokens": MODEL_MAX_TOKENS,
        "exact_batch_length_basis": "model_input_tokens",
        "document_score_aggregation": "maximum_query_to_window_cosine",
        "stable_tie_break": "source_sha256_ascending",
        "top_k": TOP_K,
    }, "Payload method contract drift")
    require(payload["label_isolation"] == {
        "labels_or_results_read": False,
        "selector_inputs_are_source_only": True,
        "offline_scorer_run": False,
    }, "Payload label-isolation contract drift")
    return payload


def validate_root_release(
    root: Path, authorisation_path: Path
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    try:
        authorisation_path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Root-release authorisation must be inside repository root") from error
    require(authorisation_path.is_file(), "Root-release authorisation is missing")
    value = read_json(authorisation_path)
    exact_keys(
        value,
        {"schema_version", "state", "root_release_id", "run_id", "attempt_id",
         "payload", "phase8", "window_amendment", "model_snapshot", "runtime",
         "destinations", "ceilings"},
        "root_release",
    )
    require(value["schema_version"] == AUTHORISATION_SCHEMA, "Root-release schema drift")
    require(value["state"] == "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_ROOT_RELEASED_EXECUTION", "Scientific execution is not root-released")
    for field in ("root_release_id", "run_id", "attempt_id"):
        require(isinstance(value[field], str) and value[field], f"Root-release {field} missing")

    exact_keys(value["payload"], {"path", "sha256"}, "root_release.payload")
    require(is_sha256(value["payload"]["sha256"]), "Root-release payload SHA missing")
    payload_path = root_path(root, value["payload"]["path"], field="root_release.payload.path")
    require(payload_path.is_file(), "Root-release payload is missing")
    require(file_sha256(payload_path) == value["payload"]["sha256"], "Root-release payload hash drift")
    payload = validate_payload(root, payload_path)

    phase8 = value["phase8"]
    exact_keys(phase8, {"status", "receipt_sha256"}, "root_release.phase8")
    require(phase8["status"] == "PASS" and phase8["receipt_sha256"] == payload["phase8"]["receipt"]["sha256"], "Root-release Phase-8 receipt drift")

    amendment = value["window_amendment"]
    exact_keys(
        amendment,
        {"status", "method_path", "method_sha256", "window_tokens",
         "overlap_tokens", "aggregation"},
        "root_release.window_amendment",
    )
    require(amendment["status"] == "APPROVED_FOR_THIS_ROOT_RELEASE", "Window amendment is not approved")
    require(amendment["method_path"] == WINDOW_AMENDMENT_REL.as_posix(), "Window amendment path drift")
    amendment_path = root_path(root, amendment["method_path"], field="window_amendment.method_path")
    require(is_sha256(amendment["method_sha256"]) and file_sha256(amendment_path) == amendment["method_sha256"], "Window amendment hash drift")
    method = read_json(amendment_path)
    require(method["proposal"]["window_tokens"] == WINDOW_TOKENS, "Window token contract drift")
    require(method["proposal"]["overlap_tokens"] == OVERLAP_TOKENS, "Window overlap contract drift")
    require(amendment["window_tokens"] == WINDOW_TOKENS and amendment["overlap_tokens"] == OVERLAP_TOKENS, "Released window parameters drift")
    require(amendment["aggregation"] == "maximum_query_to_window_cosine", "Released aggregation drift")

    snapshot = value["model_snapshot"]
    exact_keys(snapshot, {"path", "repository", "revision", "files"}, "root_release.model_snapshot")
    require(snapshot["repository"] == MODEL and snapshot["revision"] == REVISION, "Root-release model identity drift")
    require(snapshot["files"] == MODEL_FILE_SHA256, "Root-release model file bindings drift")
    snapshot_path = root_path(root, snapshot["path"], field="root_release.model_snapshot.path")
    require(snapshot_path.is_dir(), "Pinned model snapshot is missing")
    for name, expected in MODEL_FILE_SHA256.items():
        model_file = snapshot_path / name
        require(model_file.is_file() and file_sha256(model_file) == expected, f"Pinned model snapshot drift: {name}")

    require(value["runtime"] == {
        "device": "mps",
        "dtype": "bfloat16",
        "attention_implementation": "default_sdpa",
        "exact_model_input_token_length_batches": True,
        "padding": False,
        "maximum_batch_size": MAX_BATCH_SIZE,
        "automatic_retries": 0,
        "local_files_only": True,
        "trust_remote_code": False,
    }, "Root-release runtime contract drift")
    exact_keys(value["destinations"], {"output_dir", "cache_dir", "attempt_dir"}, "root_release.destinations")
    destinations = {
        name: root_path(root, path, field=f"root_release.destinations.{name}")
        for name, path in value["destinations"].items()
    }
    for name, path in destinations.items():
        require(relative(path, root).startswith("skill_benchmark/cache/"), f"{name}: destination must be under skill_benchmark/cache")
    require(len(set(destinations.values())) == 3, "Output/cache/attempt destinations must be distinct")

    exact_keys(value["ceilings"], CEILING_KEYS, "root_release.ceilings")
    for key in CEILING_KEYS - {"maximum_wall_time_seconds"}:
        require(isinstance(value["ceilings"][key], int) and not isinstance(value["ceilings"][key], bool) and value["ceilings"][key] >= 0, f"Invalid ceiling: {key}")
    require(isinstance(value["ceilings"]["maximum_wall_time_seconds"], (int, float)) and value["ceilings"]["maximum_wall_time_seconds"] > 0, "Invalid wall-time ceiling")
    value["_resolved_destinations"] = destinations
    value["_snapshot_path"] = snapshot_path
    return value, payload_path, payload


def load_authority(
    root: Path, payload: dict[str, Any]
) -> tuple[list[dict[str, Any]], set[str], dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    inputs = payload["inputs"]
    prompts = read_jsonl(root_path(root, inputs["runtime"]["path"], field="runtime.path"))
    require(len(prompts) == EXPECTED_QUERIES, "Runtime query count drift")
    require(len({row.get("prompt_id") for row in prompts}) == EXPECTED_QUERIES, "Runtime prompt identities are not unique")
    for index, row in enumerate(prompts):
        reject_outcome_keys(row, f"runtime[{index}]")
        exact_keys(row, {"schema_version", "prompt_id", "prompt", "prompt_sha256"}, f"runtime[{index}]")
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", "Runtime schema drift")
        require(isinstance(row["prompt"], str) and row["prompt"] and text_sha256(row["prompt"]) == row["prompt_sha256"], "Runtime prompt hash drift")

    source_rows = read_jsonl(root_path(root, inputs["source_manifest"]["path"], field="source_manifest.path"))
    sources = {str(row.get("sha256")) for row in source_rows}
    require(len(sources) == len(source_rows) == EXPECTED_SOURCES and all(is_sha256(item) for item in sources), "Source identity drift")
    for index, row in enumerate(source_rows):
        reject_outcome_keys(row, f"sources[{index}]")
        exact_keys(row, {"path", "sha256", "bytes"}, f"sources[{index}]")

    condition_rows = read_jsonl(root_path(root, inputs["conditions"]["path"], field="conditions.path"))
    require(len(condition_rows) == 36, "Condition manifest count drift")
    conditions = {str(row["condition_id"]): row for row in condition_rows}
    require(len(conditions) == 36, "Condition identities are not unique")
    selected: dict[str, dict[str, Any]] = {}
    for representation, cell in REPRESENTATION_CELLS.items():
        condition = conditions.get(f"{cell}-G0")
        require(condition is not None, f"Missing condition: {cell}-G0")
        reject_outcome_keys(condition, f"conditions.{cell}")
        require(condition["representation"] == representation, f"{cell}: representation drift")
        require(condition["retriever"] == "SkillRouter-Embedding-0.6B" and condition["reranker"] == "NONE", f"{cell}: method drift")
        require(condition["persisted_candidate_source"] == cell, f"{cell}: persisted source drift")
        require(condition["source_union_sha256"] == SOURCE_UNION_SHA256, f"{cell}: source union drift")
        require(condition["prompt_manifest_sha256"] == PROMPT_MANIFEST_SHA256, f"{cell}: prompt manifest drift")
        require(condition["query_count"] == EXPECTED_QUERIES and condition["execution_authorised"] is False, f"{cell}: frozen condition state drift")
        selected[representation] = condition

    representation_rows: dict[str, list[dict[str, Any]]] = {}
    for representation, artifact in inputs["representations"].items():
        rows = read_jsonl(root_path(root, artifact["path"], field=f"representations.{representation}.path"))
        require(len(rows) == EXPECTED_SOURCES, f"{representation}: row count drift")
        seen: set[str] = set()
        for index, row in enumerate(rows):
            reject_outcome_keys(row, f"{representation}[{index}]")
            source = row.get("source_sha256")
            selector_text = row.get("selector_text")
            require(source in sources and source not in seen, f"{representation}: source coverage/duplicate drift")
            require(row.get("representation") == representation, f"{representation}: row tag drift")
            require(isinstance(selector_text, str) and selector_text, f"{representation}: empty selector text")
            require(row.get("selector_text_sha256") == text_sha256(selector_text), f"{representation}: selector hash drift")
            seen.add(source)
        require(seen == sources, f"{representation}: source coverage drift")
        representation_rows[representation] = rows
    return prompts, sources, selected, representation_rows


def register_work_item(
    inventory: dict[str, dict[str, Any]], tokenizer: Any, *, text: str, role: dict[str, Any]
) -> str:
    content_token_ids = list(tokenizer.encode(text, add_special_tokens=False))
    model_input_token_ids = list(tokenizer.encode(text, add_special_tokens=True))
    require(bool(content_token_ids), "Work item has no content tokens")
    require(
        bool(model_input_token_ids) and len(model_input_token_ids) <= MODEL_MAX_TOKENS,
        "Model input exceeds the 32,768-token checkpoint limit",
    )
    text_id = text_sha256(text)
    content_token_ids_sha256 = canonical_sha256(content_token_ids)
    model_input_token_ids_sha256 = canonical_sha256(model_input_token_ids)
    existing = inventory.get(text_id)
    if existing is None:
        inventory[text_id] = {
            "text_id": text_id,
            "text": text,
            "text_sha256": text_id,
            "content_token_ids_sha256": content_token_ids_sha256,
            "content_tokens": len(content_token_ids),
            "model_input_token_ids_sha256": model_input_token_ids_sha256,
            "model_input_tokens": len(model_input_token_ids),
            "roles": [role],
        }
    else:
        require(
            existing["text"] == text
            and existing["content_token_ids_sha256"] == content_token_ids_sha256
            and existing["model_input_token_ids_sha256"] == model_input_token_ids_sha256,
            "Text/token identity collision",
        )
        existing["roles"].append(role)
    return text_id


def build_work_inventory(
    tokenizer: Any,
    prompts: list[dict[str, Any]],
    representations: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, str], dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    documents: dict[str, list[dict[str, Any]]] = {}
    summary: dict[str, Any] = {}
    for representation in REPRESENTATION_CELLS:
        documents[representation] = []
        windowed = 0
        windows = 0
        maximum_content_tokens = 0
        maximum_model_input_tokens = 0
        for source_index, row in enumerate(representations[representation]):
            chunks = exact_text_chunks(
                tokenizer,
                row["selector_text"],
                maximum_tokens=WINDOW_TOKENS,
                overlap_tokens=OVERLAP_TOKENS,
            )
            windowed += len(chunks) > 1
            windows += len(chunks)
            chunk_text_ids: list[str] = []
            chunk_metadata: list[dict[str, Any]] = []
            for chunk in chunks:
                text_id = register_work_item(
                    inventory,
                    tokenizer,
                    text=chunk.text,
                    role={
                        "kind": "document_window",
                        "representation": representation,
                        "source_sha256": row["source_sha256"],
                        "chunk_index": chunk.chunk_index,
                    },
                )
                item = inventory[text_id]
                require(item["content_tokens"] == chunk.token_count, "Chunk/content token count drift")
                require(item["content_token_ids_sha256"] == chunk.token_ids_sha256, "Chunk/content token-ID hash drift")
                maximum_content_tokens = max(maximum_content_tokens, item["content_tokens"])
                maximum_model_input_tokens = max(maximum_model_input_tokens, item["model_input_tokens"])
                chunk_text_ids.append(text_id)
                chunk_metadata.append({
                    "chunk_index": chunk.chunk_index,
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char,
                    "content_tokens": chunk.token_count,
                    "content_token_ids_sha256": chunk.token_ids_sha256,
                    "model_input_tokens": item["model_input_tokens"],
                    "model_input_token_ids_sha256": item["model_input_token_ids_sha256"],
                    "text_sha256": chunk.text_sha256,
                    "ended_at_preferred_boundary": chunk.ended_at_preferred_boundary,
                })
            documents[representation].append({
                "source_row_index": source_index,
                "source_sha256": row["source_sha256"],
                "selector_text_sha256": row["selector_text_sha256"],
                "chunk_text_ids": chunk_text_ids,
                "chunks": chunk_metadata,
            })
        summary[representation] = {
            "documents": len(documents[representation]),
            "document_windows": windows,
            "windowed_documents": windowed,
            "maximum_content_tokens_per_window": maximum_content_tokens,
            "maximum_model_input_tokens_per_window": maximum_model_input_tokens,
            "content_window_tokens": WINDOW_TOKENS,
            "content_overlap_tokens": OVERLAP_TOKENS,
            "content_add_special_tokens": False,
            "model_input_add_special_tokens": True,
        }

    query_text_ids: dict[str, str] = {}
    for prompt in prompts:
        query_text = QUERY_INSTRUCTION + prompt["prompt"]
        query_text_ids[prompt["prompt_id"]] = register_work_item(
            inventory,
            tokenizer,
            text=query_text,
            role={"kind": "query", "prompt_id": prompt["prompt_id"], "prompt_sha256": prompt["prompt_sha256"]},
        )
    require(len(query_text_ids) == len(prompts), "Query work inventory drift")
    return inventory, documents, query_text_ids, summary


def exact_length_batches(
    items: Sequence[dict[str, Any]], maximum_batch_size: int = MAX_BATCH_SIZE
) -> list[list[dict[str, Any]]]:
    require(0 < maximum_batch_size <= MAX_BATCH_SIZE, "Invalid exact-length batch ceiling")
    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        length = item.get("model_input_tokens")
        require(isinstance(length, int) and 0 < length <= MODEL_MAX_TOKENS, "Invalid model-input token length")
        buckets[length].append(item)
    batches: list[list[dict[str, Any]]] = []
    for length in sorted(buckets):
        bucket = sorted(buckets[length], key=lambda row: row["text_id"])
        for start in range(0, len(bucket), maximum_batch_size):
            batch = bucket[start:start + maximum_batch_size]
            require(len({row["model_input_tokens"] for row in batch}) == 1, "Heterogeneous batch forbidden")
            batches.append(batch)
    return batches


def cache_key(item: dict[str, Any]) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-skillrouter-embedding-cache-key-v1",
        "model": MODEL,
        "revision": REVISION,
        "dimensions": DIMENSIONS,
        "pooling": "last_non_padding_token",
        "normalization": "l2",
        "device_contract": "mps",
        "dtype_contract": "bfloat16",
        "attention_contract": "default_sdpa",
        "chunker_version": CHUNKER_VERSION,
        "content_window_tokens": WINDOW_TOKENS,
        "content_overlap_tokens": OVERLAP_TOKENS,
        "content_add_special_tokens": False,
        "model_input_add_special_tokens": True,
        "model_maximum_tokens": MODEL_MAX_TOKENS,
        "tokenizer_sha256": MODEL_FILE_SHA256["tokenizer.json"],
        "model_weights_sha256": MODEL_FILE_SHA256["model.safetensors"],
        "text_sha256": item["text_sha256"],
        "content_token_ids_sha256": item["content_token_ids_sha256"],
        "content_tokens": item["content_tokens"],
        "model_input_token_ids_sha256": item["model_input_token_ids_sha256"],
        "model_input_tokens": item["model_input_tokens"],
    })


def normalized_vector(values: Sequence[float]) -> list[float]:
    vector = np.asarray(values, dtype=np.float64)
    require(vector.shape == (DIMENSIONS,) and bool(np.all(np.isfinite(vector))), "Embedding must have 1,024 finite coordinates")
    norm = float(np.linalg.norm(vector))
    require(math.isfinite(norm) and norm > 0.0, "Embedding has invalid norm")
    vector = vector / norm
    require(abs(float(np.linalg.norm(vector)) - 1.0) <= 1e-12, "Embedding L2 normalization failed")
    return [float(value) for value in vector]


class ExactEmbeddingCache:
    def __init__(self, root: Path) -> None:
        self.root = root

    def path(self, item: dict[str, Any]) -> Path:
        return self.root / f"{cache_key(item)}.json"

    def load(self, item: dict[str, Any]) -> list[float] | None:
        path = self.path(item)
        if not path.is_file():
            return None
        value = read_json(path)
        exact_keys(
            value,
            {"schema_version", "cache_key", "model", "revision", "dimensions",
             "pooling", "normalization", "device_contract", "dtype_contract",
             "attention_contract", "chunker_version", "content_window_tokens",
             "content_overlap_tokens", "content_add_special_tokens",
             "model_input_add_special_tokens", "model_maximum_tokens",
             "tokenizer_sha256", "model_weights_sha256", "text_sha256",
             "content_token_ids_sha256", "content_tokens",
             "model_input_token_ids_sha256", "model_input_tokens",
             "embedding_sha256", "embedding"},
            f"cache.{path.name}",
        )
        require(value["schema_version"] == "rq2b-v7-skillrouter-embedding-cache-v1", "Cache schema drift")
        require(value["cache_key"] == cache_key(item), "Cache key drift")
        require(value["model"] == MODEL and value["revision"] == REVISION, "Cache model drift")
        require(value["dimensions"] == DIMENSIONS, "Cache dimensions drift")
        require(value["pooling"] == "last_non_padding_token" and value["normalization"] == "l2", "Cache pooling/normalization drift")
        require(value["device_contract"] == "mps" and value["dtype_contract"] == "bfloat16" and value["attention_contract"] == "default_sdpa", "Cache runtime contract drift")
        require(value["chunker_version"] == CHUNKER_VERSION, "Cache chunker contract drift")
        require(value["content_window_tokens"] == WINDOW_TOKENS and value["content_overlap_tokens"] == OVERLAP_TOKENS, "Cache content-window contract drift")
        require(value["content_add_special_tokens"] is False and value["model_input_add_special_tokens"] is True and value["model_maximum_tokens"] == MODEL_MAX_TOKENS, "Cache content/model token-basis drift")
        require(value["tokenizer_sha256"] == MODEL_FILE_SHA256["tokenizer.json"] and value["model_weights_sha256"] == MODEL_FILE_SHA256["model.safetensors"], "Cache model-file binding drift")
        for field in ("text_sha256", "content_token_ids_sha256", "content_tokens", "model_input_token_ids_sha256", "model_input_tokens"):
            require(value[field] == item[field], f"Cache {field} drift")
        vector = [float(number) for number in value["embedding"]]
        require(value["embedding_sha256"] == canonical_sha256(vector), "Cache embedding hash drift")
        require(len(vector) == DIMENSIONS and all(math.isfinite(number) for number in vector), "Cache vector drift")
        require(abs(math.sqrt(sum(number * number for number in vector)) - 1.0) <= 1e-5, "Cache vector is not L2 normalized")
        return vector

    def store(self, item: dict[str, Any], values: Sequence[float]) -> Path:
        vector = normalized_vector(values)
        path = self.path(item)
        require(not path.exists(), f"Refusing to overwrite cache entry: {path}")
        write_json_new(path, {
            "schema_version": "rq2b-v7-skillrouter-embedding-cache-v1",
            "cache_key": cache_key(item),
            "model": MODEL,
            "revision": REVISION,
            "dimensions": DIMENSIONS,
            "pooling": "last_non_padding_token",
            "normalization": "l2",
            "device_contract": "mps",
            "dtype_contract": "bfloat16",
            "attention_contract": "default_sdpa",
            "chunker_version": CHUNKER_VERSION,
            "content_window_tokens": WINDOW_TOKENS,
            "content_overlap_tokens": OVERLAP_TOKENS,
            "content_add_special_tokens": False,
            "model_input_add_special_tokens": True,
            "model_maximum_tokens": MODEL_MAX_TOKENS,
            "tokenizer_sha256": MODEL_FILE_SHA256["tokenizer.json"],
            "model_weights_sha256": MODEL_FILE_SHA256["model.safetensors"],
            "text_sha256": item["text_sha256"],
            "content_token_ids_sha256": item["content_token_ids_sha256"],
            "content_tokens": item["content_tokens"],
            "model_input_token_ids_sha256": item["model_input_token_ids_sha256"],
            "model_input_tokens": item["model_input_tokens"],
            "embedding_sha256": canonical_sha256(vector),
            "embedding": vector,
        })
        return path


def last_non_padding_positions(attention_mask_rows: Sequence[Sequence[int]]) -> list[int]:
    positions: list[int] = []
    for row in attention_mask_rows:
        require(bool(row) and all(value in (0, 1) for value in row), "Invalid attention mask")
        active = [index for index, value in enumerate(row) if value]
        require(bool(active), "Attention mask has no active token")
        positions.append(active[-1])
    return positions


def _last_token_pool(last_hidden_states: Any, attention_mask: Any) -> Any:
    import torch

    positions = attention_mask.sum(dim=1) - 1
    if bool(torch.all(attention_mask == 1).item()):
        require(bool(torch.all(positions == attention_mask.shape[1] - 1).item()), "Unpadded last-token position drift")
    return last_hidden_states[
        torch.arange(last_hidden_states.shape[0], device=last_hidden_states.device),
        positions,
    ]


def _embed_exact_batch(tokenizer: Any, model: Any, batch: list[dict[str, Any]]) -> list[list[float]]:
    import torch
    import torch.nn.functional as functional

    require(bool(batch) and len(batch) <= MAX_BATCH_SIZE, "Invalid embedding batch size")
    expected_length = batch[0]["model_input_tokens"]
    require(all(item["model_input_tokens"] == expected_length for item in batch), "Heterogeneous token-length batch forbidden")
    encoded = tokenizer(
        [item["text"] for item in batch],
        add_special_tokens=True,
        padding=False,
        truncation=False,
        return_attention_mask=True,
        return_tensors="pt",
    )
    require(tuple(encoded["input_ids"].shape) == (len(batch), expected_length), "Runtime tokenizer length differs from sealed work item")
    require(bool(torch.all(encoded["attention_mask"] == 1).item()), "Padding is forbidden")
    for index, item in enumerate(batch):
        ids = [int(value) for value in encoded["input_ids"][index].tolist()]
        require(canonical_sha256(ids) == item["model_input_token_ids_sha256"], "Runtime model-input token IDs drift")
    encoded = {key: value.to("mps") for key, value in encoded.items()}
    with torch.inference_mode():
        outputs = model(**encoded)
        require(outputs.last_hidden_state.device.type == "mps", "Model output silently left MPS")
        require(bool(torch.isfinite(outputs.last_hidden_state).all().item()), "Non-finite model hidden state")
        pooled = _last_token_pool(outputs.last_hidden_state, encoded["attention_mask"])
        vectors = functional.normalize(pooled.float(), p=2, dim=1)
        require(bool(torch.isfinite(vectors).all().item()), "Non-finite pooled embedding")
        require(tuple(vectors.shape) == (len(batch), DIMENSIONS), "Embedding dimension drift")
        result = vectors.cpu().tolist()
    return [normalized_vector(row) for row in result]


def top20_binding_sha256(
    *, condition_id: str, prompt_id: str, prompt_sha256: str,
    ordered_source_sha256: Iterable[str],
) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-top20-binding-v1",
        "condition_id": condition_id,
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_sha256,
        "ordered_source_sha256": list(ordered_source_sha256),
    })


def stable_top_k(source_ids: list[str], scores: np.ndarray, k: int = TOP_K) -> list[int]:
    require(len(source_ids) == len(scores) and len(source_ids) >= k, "Ranking input size drift")
    require(bool(np.all(np.isfinite(scores))), "Ranking contains non-finite scores")
    source_array = np.asarray(source_ids, dtype=f"U{max(map(len, source_ids))}")
    order = np.lexsort((source_array, -scores))
    return [int(index) for index in order[:k]]


def normalized_matrix(values: Sequence[Sequence[float]]) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    require(matrix.ndim == 2 and matrix.shape[1] == DIMENSIONS, "Embedding matrix shape drift")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), "Embedding matrix norm drift")
    return matrix / norms


def maximum_window_cosine_scores(
    normalized_windows: np.ndarray, document_starts: Sequence[int],
    normalized_query: np.ndarray,
) -> np.ndarray:
    require(
        normalized_windows.ndim == 2
        and normalized_windows.shape[1] == DIMENSIONS
        and normalized_query.shape == (DIMENSIONS,),
        "Maximum-window scoring shape drift",
    )
    starts = np.asarray(document_starts, dtype=np.int64)
    require(
        bool(len(starts)) and starts[0] == 0
        and bool(np.all(starts[1:] > starts[:-1]))
        and starts[-1] < len(normalized_windows),
        "Maximum-window document boundaries drift",
    )
    window_scores = normalized_windows @ normalized_query
    require(bool(np.all(np.isfinite(window_scores))), "Non-finite window cosine")
    return np.maximum.reduceat(window_scores, starts)


def online_row_cost(
    *, query_model_input_tokens: int, query_embedding_ms: float,
    scoring_ms: float, query_initial_cache_hit: bool,
) -> dict[str, Any]:
    """Return one row's online query cost, excluding offline document work.

    ``window_forwards`` is the single logical query-embedding input associated
    with the row.  ``cache_hits`` records whether that query input was already
    cached; document windows and document cache activity belong only in the
    offline cost ledger.
    """
    require(
        isinstance(query_model_input_tokens, int)
        and not isinstance(query_model_input_tokens, bool)
        and query_model_input_tokens > 0,
        "Online query model-input tokens must be positive",
    )
    require(
        all(math.isfinite(value) and value >= 0.0 for value in (query_embedding_ms, scoring_ms)),
        "Online query timing must be finite and non-negative",
    )
    return {
        "wall_time_ms": query_embedding_ms + scoring_ms,
        "provider_calls": 0,
        "input_tokens": query_model_input_tokens,
        "output_tokens": 0,
        "window_forwards": 1,
        "cache_hits": int(query_initial_cache_hit),
        "retry_count": 0,
        "timeout_count": 0,
        "failure_count": 0,
    }


def score_representation(
    *, run_id: str, representation: str, condition: dict[str, Any],
    documents: list[dict[str, Any]], prompts: list[dict[str, Any]],
    query_text_ids: dict[str, str], inventory: dict[str, dict[str, Any]],
    vectors: dict[str, list[float]], initial_cache_hits: dict[str, bool],
    query_embedding_ms: dict[str, float],
) -> tuple[list[dict[str, Any]], float]:
    ordered_documents = sorted(documents, key=lambda row: row["source_sha256"])
    source_ids = [row["source_sha256"] for row in ordered_documents]
    require(len(source_ids) == EXPECTED_SOURCES and len(set(source_ids)) == EXPECTED_SOURCES, "Representation document identity drift")
    starts: list[int] = []
    flat_vectors: list[list[float]] = []
    for document in ordered_documents:
        starts.append(len(flat_vectors))
        require(bool(document["chunk_text_ids"]), "Document has no windows")
        for text_id in document["chunk_text_ids"]:
            flat_vectors.append(vectors[text_id])
    matrix = normalized_matrix(flat_vectors)
    starts_array = np.asarray(starts, dtype=np.int64)
    rows: list[dict[str, Any]] = []
    scoring_ms = 0.0
    for prompt in prompts:
        query_text_id = query_text_ids[prompt["prompt_id"]]
        query = normalized_matrix([vectors[query_text_id]])[0]
        started = time.perf_counter()
        scores = maximum_window_cosine_scores(matrix, starts_array, query)
        indices = stable_top_k(source_ids, scores)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        scoring_ms += elapsed_ms
        candidates = [
            {"rank": rank, "source_sha256": source_ids[index], "score": float(scores[index])}
            for rank, index in enumerate(indices, 1)
        ]
        condition_id = condition["condition_id"]
        rows.append({
            "schema_version": ROW_SCHEMA,
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
                ordered_source_sha256=(item["source_sha256"] for item in candidates[:20]),
            ),
            "ranked_candidates": candidates,
            "cost": online_row_cost(
                query_model_input_tokens=inventory[query_text_id]["model_input_tokens"],
                query_embedding_ms=query_embedding_ms[query_text_id],
                scoring_ms=elapsed_ms,
                query_initial_cache_hit=initial_cache_hits[query_text_id],
            ),
        })
    return rows, scoring_ms


def validate_rows(rows: list[dict[str, Any]], prompts: list[dict[str, Any]]) -> None:
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    expected = {(f"{cell}-G0", prompt_id) for cell in REPRESENTATION_CELLS.values() for prompt_id in prompt_by_id}
    actual: set[tuple[str, str]] = set()
    for row_number, row in enumerate(rows, 1):
        prefix = f"B1 row {row_number}"
        reject_outcome_keys(row, prefix)
        exact_keys(row, ROW_KEYS, prefix)
        require(row["schema_version"] == ROW_SCHEMA and row["status"] == "SUCCESS", f"{prefix}: schema/status drift")
        require(row["top_k"] == TOP_K and row["score_semantics"] == "HIGHER_IS_BETTER", f"{prefix}: ranking contract drift")
        prompt = prompt_by_id.get(row["prompt_id"])
        require(prompt is not None and row["prompt_sha256"] == prompt["prompt_sha256"], f"{prefix}: prompt binding drift")
        candidates = row["ranked_candidates"]
        require(isinstance(candidates, list) and len(candidates) == TOP_K, f"{prefix}: Top-100 required")
        identities: list[str] = []
        previous: tuple[float, str] | None = None
        for rank, candidate in enumerate(candidates, 1):
            exact_keys(candidate, {"rank", "source_sha256", "score"}, f"{prefix}.candidate[{rank - 1}]")
            require(candidate["rank"] == rank and is_sha256(candidate["source_sha256"]), f"{prefix}: candidate identity/rank drift")
            require(isinstance(candidate["score"], (int, float)) and not isinstance(candidate["score"], bool) and math.isfinite(candidate["score"]), f"{prefix}: candidate score drift")
            current = (-float(candidate["score"]), candidate["source_sha256"])
            require(previous is None or previous <= current, f"{prefix}: score/SHA order drift")
            previous = current
            identities.append(candidate["source_sha256"])
        require(len(set(identities)) == TOP_K, f"{prefix}: duplicate candidates")
        require(row["top20_binding_sha256"] == top20_binding_sha256(
            condition_id=row["condition_id"], prompt_id=row["prompt_id"],
            prompt_sha256=row["prompt_sha256"], ordered_source_sha256=identities[:20]
        ), f"{prefix}: Top-20 binding drift")
        exact_keys(row["cost"], COST_KEYS, f"{prefix}.cost")
        require(all(isinstance(row["cost"][key], int) and not isinstance(row["cost"][key], bool) and row["cost"][key] >= 0 for key in COST_KEYS - {"wall_time_ms"}), f"{prefix}: integer cost drift")
        require(isinstance(row["cost"]["wall_time_ms"], (int, float)) and math.isfinite(row["cost"]["wall_time_ms"]) and row["cost"]["wall_time_ms"] >= 0, f"{prefix}: wall-time drift")
        require(row["cost"]["provider_calls"] == 0 and row["cost"]["output_tokens"] == 0, f"{prefix}: local online provider/output cost drift")
        require(row["cost"]["input_tokens"] > 0 and row["cost"]["window_forwards"] == 1, f"{prefix}: row cost must contain exactly one online query input")
        require(row["cost"]["cache_hits"] in {0, 1}, f"{prefix}: row cache hits must be query-only")
        key = (row["condition_id"], row["prompt_id"])
        require(key not in actual, f"{prefix}: duplicate output key")
        actual.add(key)
    require(actual == expected, f"Four-cell output coverage drift: {len(actual)} != {len(expected)}")


def _write_attempt_record(
    attempt_dir: Path, name: str, value: dict[str, Any]
) -> Path:
    path = attempt_dir / name
    write_json_new(path, value)
    return path


def execute(root: Path, authorisation_path: Path) -> dict[str, Any]:
    release, payload_path, payload = validate_root_release(root, authorisation_path)
    destinations = release["_resolved_destinations"]
    output_dir = destinations["output_dir"]
    cache_dir = destinations["cache_dir"]
    attempt_dir = destinations["attempt_dir"]
    require(not output_dir.exists(), f"Refusing to overwrite output: {output_dir}")
    require(not attempt_dir.exists(), f"Refusing to overwrite attempt receipts: {attempt_dir}")
    staging = output_dir.with_name(f".{output_dir.name}.staging-{release['attempt_id']}")
    require(not staging.exists(), f"Stale output staging directory: {staging}")

    prompts, sources, conditions, representations = load_authority(root, payload)
    del sources
    attempt_dir.mkdir(parents=True, exist_ok=False)
    started_at = utc_now()
    run_started_path = _write_attempt_record(attempt_dir, "run_started.json", {
        "schema_version": "rq2b-v7-skillrouter-embedding-b1-run-start-v1",
        "run_id": release["run_id"],
        "attempt_id": release["attempt_id"],
        "root_release_id": release["root_release_id"],
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": file_sha256(authorisation_path)},
        "automatic_retries": 0,
        "started_at_utc": started_at,
    })
    wall_started = time.perf_counter()
    model_load_seconds = 0.0
    scoring_seconds = 0.0
    try:
        require(os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK", "0").lower() not in {"1", "true", "yes"}, "MPS CPU fallback is enabled")
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        import torch
        from transformers import AutoModel, AutoTokenizer

        require(torch.backends.mps.is_built(), "PyTorch is not built with MPS")
        require(torch.backends.mps.is_available(), "MPS is unavailable; CPU fallback is forbidden")
        load_started = time.perf_counter()
        tokenizer = AutoTokenizer.from_pretrained(
            release["_snapshot_path"], local_files_only=True, trust_remote_code=False,
        )
        model = AutoModel.from_pretrained(
            release["_snapshot_path"],
            local_files_only=True,
            trust_remote_code=False,
            torch_dtype=torch.bfloat16,
        ).eval().to("mps")
        model_load_seconds = time.perf_counter() - load_started
        require(getattr(model.config, "_attn_implementation", None) == "sdpa", "Resolved model attention implementation is not SDPA")
        floating_parameters = [parameter for parameter in model.parameters() if parameter.is_floating_point()]
        require(bool(floating_parameters), "Model has no floating parameters")
        require(all(parameter.device.type == "mps" for parameter in floating_parameters), "Model silently left MPS")
        require(all(parameter.dtype == torch.bfloat16 for parameter in floating_parameters), "Model dtype is not bfloat16")

        inventory, documents, query_text_ids, window_summary = build_work_inventory(
            tokenizer, prompts, representations
        )
        cache = ExactEmbeddingCache(cache_dir)
        initial_vectors = {text_id: cache.load(item) for text_id, item in inventory.items()}
        initial_cache_hits = {text_id: vector is not None for text_id, vector in initial_vectors.items()}
        vectors = {text_id: vector for text_id, vector in initial_vectors.items() if vector is not None}
        document_ids = sorted({
            text_id for rows in documents.values() for document in rows
            for text_id in document["chunk_text_ids"]
        })
        query_ids = sorted(set(query_text_ids.values()))
        ordered_stages = [
            ("document", [inventory[text_id] for text_id in document_ids if text_id not in vectors]),
            ("query", [inventory[text_id] for text_id in query_ids if text_id not in vectors]),
        ]
        batches = [(stage, batch) for stage, items in ordered_stages for batch in exact_length_batches(items)]
        planned_new = sum(len(batch) for _, batch in batches)
        planned_tokens = sum(item["model_input_tokens"] for _, batch in batches for item in batch)
        ceilings = release["ceilings"]
        require(planned_new <= ceilings["maximum_new_cache_entries"], "New cache-entry ceiling exceeded before model forward")
        require(planned_new <= ceilings["maximum_model_input_instances"], "Model-input instance ceiling exceeded before model forward")
        require(planned_tokens <= ceilings["maximum_model_input_tokens"], "Model-token ceiling exceeded before model forward")
        require(len(batches) <= ceilings["maximum_model_forward_batches"], "Forward-batch ceiling exceeded before model forward")

        cache_dir.mkdir(parents=True, exist_ok=True)
        query_embedding_ms = {text_id: 0.0 for text_id in query_ids}
        forward_seconds = 0.0
        attempt_records: list[dict[str, Any]] = []
        for batch_number, (stage, batch) in enumerate(batches, 1):
            record_id = f"forward-{batch_number:05d}"
            record_started = _write_attempt_record(attempt_dir, f"{record_id}.started.json", {
                "schema_version": "rq2b-v7-skillrouter-embedding-forward-start-v1",
                "record_id": record_id,
                "stage": stage,
                "text_ids": [item["text_id"] for item in batch],
                "items": len(batch),
                "exact_model_input_tokens": batch[0]["model_input_tokens"],
                "padding": False,
                "device": "mps",
                "dtype": "bfloat16",
                "attention_implementation": "default_sdpa",
                "started_at_utc": utc_now(),
            })
            torch.mps.synchronize()
            forward_started = time.perf_counter()
            embedded = _embed_exact_batch(tokenizer, model, batch)
            torch.mps.synchronize()
            elapsed = time.perf_counter() - forward_started
            forward_seconds += elapsed
            cache_artifacts: list[dict[str, Any]] = []
            for item, vector in zip(batch, embedded, strict=True):
                cache_path = cache.store(item, vector)
                vectors[item["text_id"]] = vector
                cache_artifacts.append({
                    "text_id": item["text_id"],
                    "cache_key": cache_key(item),
                    "path": relative(cache_path, root),
                    "sha256": file_sha256(cache_path),
                })
                if stage == "query":
                    query_embedding_ms[item["text_id"]] = elapsed * 1000.0 / len(batch)
            completed = _write_attempt_record(attempt_dir, f"{record_id}.completed.json", {
                "schema_version": "rq2b-v7-skillrouter-embedding-forward-complete-v1",
                "record_id": record_id,
                "started_receipt_sha256": file_sha256(record_started),
                "items": len(batch),
                "model_input_tokens": sum(item["model_input_tokens"] for item in batch),
                "elapsed_seconds": elapsed,
                "cache_artifacts": cache_artifacts,
                "completed_at_utc": utc_now(),
            })
            attempt_records.append({
                "record_id": record_id,
                "started": {"path": relative(record_started, root), "sha256": file_sha256(record_started)},
                "completed": {"path": relative(completed, root), "sha256": file_sha256(completed)},
            })
            require(time.perf_counter() - wall_started <= ceilings["maximum_wall_time_seconds"], "Wall-time ceiling exceeded after forward; no further model work allowed")

        require(set(vectors) == set(inventory), "Embedding cache coverage is incomplete")
        for text_id, item in inventory.items():
            require(cache.load(item) == vectors[text_id], f"Final cache validation drift: {text_id}")

        rows: list[dict[str, Any]] = []
        per_representation: dict[str, Any] = {}
        for representation, cell in REPRESENTATION_CELLS.items():
            cell_rows, cell_scoring_ms = score_representation(
                run_id=release["run_id"],
                representation=representation,
                condition=conditions[representation],
                documents=documents[representation],
                prompts=prompts,
                query_text_ids=query_text_ids,
                inventory=inventory,
                vectors=vectors,
                initial_cache_hits=initial_cache_hits,
                query_embedding_ms=query_embedding_ms,
            )
            rows.extend(cell_rows)
            scoring_seconds += cell_scoring_ms / 1000.0
            per_representation[representation] = {
                "first_stage_cell_id": cell,
                **window_summary[representation],
                "rows": len(cell_rows),
                "scoring_seconds": cell_scoring_ms / 1000.0,
            }
        validate_rows(rows, prompts)

        staging.mkdir(parents=True, exist_ok=False)
        b1_path = staging / "b1.jsonl.gz"
        b1_artifact = write_deterministic_jsonl_gzip(b1_path, rows)
        b1_artifact["path"] = relative(output_dir / b1_path.name, root)
        cache_inventory_path = staging / "cache_inventory.jsonl.gz"
        cache_rows = []
        for text_id, item in sorted(inventory.items()):
            cache_path = cache.path(item)
            cache_rows.append({
                "schema_version": "rq2b-v7-skillrouter-embedding-cache-inventory-row-v1",
                "text_id": text_id,
                "cache_key": cache_key(item),
                "content_tokens": item["content_tokens"],
                "content_token_ids_sha256": item["content_token_ids_sha256"],
                "model_input_tokens": item["model_input_tokens"],
                "model_input_token_ids_sha256": item["model_input_token_ids_sha256"],
                "role_kinds": sorted({role["kind"] for role in item["roles"]}),
                "initial_cache_hit": initial_cache_hits[text_id],
                "cache_path": relative(cache_path, root),
                "cache_entry_sha256": file_sha256(cache_path),
            })
        cache_artifact = write_deterministic_jsonl_gzip(cache_inventory_path, cache_rows)
        cache_artifact["path"] = relative(output_dir / cache_inventory_path.name, root)
        attempt_index_path = _write_attempt_record(attempt_dir, "attempt_index.json", {
            "schema_version": "rq2b-v7-skillrouter-embedding-attempt-index-v1",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "automatic_retries": 0,
            "forward_records": attempt_records,
        })
        elapsed_seconds = time.perf_counter() - wall_started
        ledger = {
            "schema_version": "rq2b-v7-skillrouter-embedding-b1-cost-ledger-v1",
            "offline": {
                "unique_document_windows": len(document_ids),
                "initial_document_cache_hits": sum(initial_cache_hits[text_id] for text_id in document_ids),
                "new_document_cache_entries": sum(not initial_cache_hits[text_id] for text_id in document_ids),
                "document_model_input_tokens": sum(inventory[text_id]["model_input_tokens"] for text_id in document_ids if not initial_cache_hits[text_id]),
            },
            "online": {
                "unique_queries": len(query_ids),
                "logical_query_inputs": len(query_ids),
                "initial_query_cache_hits": sum(initial_cache_hits[text_id] for text_id in query_ids),
                "new_query_cache_entries": sum(not initial_cache_hits[text_id] for text_id in query_ids),
                "query_model_input_tokens": sum(inventory[text_id]["model_input_tokens"] for text_id in query_ids if not initial_cache_hits[text_id]),
                "logical_query_model_input_tokens": sum(inventory[text_id]["model_input_tokens"] for text_id in query_ids),
                "scoring_seconds": scoring_seconds,
            },
            "execution": {
                "model_load_seconds": model_load_seconds,
                "model_forward_seconds": forward_seconds,
                "model_forward_batches": len(batches),
                "model_input_instances": planned_new,
                "model_input_tokens": planned_tokens,
                "wall_time_seconds": elapsed_seconds,
                "provider_calls": 0,
                "network_calls": 0,
                "automatic_retries": 0,
                "timeout_count": 0,
                "failure_count": 0,
                "monetary_cost_usd": 0.0,
            },
        }
        ledger_path = staging / "cost_ledger.json"
        write_json_new(ledger_path, ledger)
        receipt = {
            "schema_version": "rq2b-v7-skillrouter-embedding-b1-run-receipt-v1",
            "status": "COMPLETE_B03_B06_B09_B12_LABEL_FREE_SKILLROUTER_B1",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "root_release_id": release["root_release_id"],
            "runner": {"version": RUNNER_VERSION, "path": relative(Path(__file__), root), "sha256": file_sha256(Path(__file__))},
            "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
            "authorisation": {"path": relative(authorisation_path, root), "sha256": file_sha256(authorisation_path)},
            "attempt_receipts": {
                "run_started": {"path": relative(run_started_path, root), "sha256": file_sha256(run_started_path)},
                "attempt_index": {"path": relative(attempt_index_path, root), "sha256": file_sha256(attempt_index_path)},
            },
            "method": payload["method"],
            "runtime": release["runtime"],
            "counts": {
                "queries": len(prompts),
                "sources": EXPECTED_SOURCES,
                "cells": 4,
                "rows": len(rows),
                "ranked_candidates": len(rows) * TOP_K,
                "unique_embedding_inputs": len(inventory),
            },
            "per_representation": per_representation,
            "cost": ledger,
            "artifacts": {
                "b1": b1_artifact,
                "cache_inventory": cache_artifact,
                "cost_ledger": {"path": relative(output_dir / ledger_path.name, root), "sha256": file_sha256(ledger_path)},
            },
            "environment": {
                "python": platform.python_version(),
                "implementation": platform.python_implementation(),
                "platform": platform.platform(),
                "torch": torch.__version__,
                "transformers": __import__("transformers").__version__,
            },
            "completed_at_utc": utc_now(),
        }
        receipt_path = staging / "run_receipt.json"
        write_json_new(receipt_path, receipt)
        write_json_new(staging / "manifest.json", {
            "schema_version": "rq2b-v7-skillrouter-embedding-b1-output-manifest-v1",
            "status": receipt["status"],
            "run_receipt": {"path": relative(output_dir / receipt_path.name, root), "sha256": file_sha256(receipt_path)},
            "b1": b1_artifact,
            "cache_inventory": cache_artifact,
        })
        staging.replace(output_dir)
        _write_attempt_record(attempt_dir, "run_completed.json", {
            "schema_version": "rq2b-v7-skillrouter-embedding-b1-run-complete-v1",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "output_manifest": {
                "path": relative(output_dir / "manifest.json", root),
                "sha256": file_sha256(output_dir / "manifest.json"),
            },
            "completed_at_utc": utc_now(),
        })
        return receipt
    except Exception as error:
        if attempt_dir.is_dir() and not (attempt_dir / "run_failed.json").exists():
            _write_attempt_record(attempt_dir, "run_failed.json", {
                "schema_version": "rq2b-v7-skillrouter-embedding-b1-run-failed-v1",
                "run_id": release["run_id"],
                "attempt_id": release["attempt_id"],
                "automatic_retries": 0,
                "failure_type": type(error).__name__,
                "failure_message": str(error),
                "model_load_seconds_before_failure": model_load_seconds,
                "scoring_seconds_before_failure": scoring_seconds,
                "failed_at_utc": utc_now(),
            })
        raise


def self_test() -> dict[str, Any]:
    source_ids = [f"{index:064x}" for index in range(TOP_K)]
    scores = np.ones(TOP_K, dtype=np.float64)
    reversed_sources = list(reversed(source_ids))
    order = stable_top_k(reversed_sources, scores)
    require([reversed_sources[index] for index in order] == source_ids, "SHA tie-break self-test failed")
    batches = exact_length_batches([
        {"text_id": f"t{index:02d}", "model_input_tokens": 3 if index < 17 else 5}
        for index in range(20)
    ])
    require([len(batch) for batch in batches] == [16, 1, 3], "Exact-length batching self-test failed")
    require(all(len({item["model_input_tokens"] for item in batch}) == 1 for batch in batches), "Padding-free batching self-test failed")
    require(last_non_padding_positions([[1, 1, 1], [0, 1, 1]]) == [2, 2], "Last-token position self-test failed")
    require(abs(sum(value * value for value in normalized_vector([1.0, *([0.0] * (DIMENSIONS - 1))])) - 1.0) <= 1e-12, "L2 self-test failed")
    return {
        "status": "PASS_SYNTHETIC_NO_MODEL_LOAD_NO_FORWARD_NO_NETWORK",
        "network_calls": 0,
        "model_loads": 0,
        "model_forwards": 0,
        "checks": {
            "deterministic_sha_tie_break": True,
            "exact_length_no_padding_batches": True,
            "last_non_padding_token_positions": True,
            "l2_1024_dimensions": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--authorisation", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.authorisation is not None, "--authorisation is required for execution")
        root = args.root.resolve()
        authorisation = args.authorisation if args.authorisation.is_absolute() else root / args.authorisation
        result = execute(root, authorisation.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
