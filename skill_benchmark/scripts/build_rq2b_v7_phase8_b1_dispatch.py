#!/usr/bin/env python3
"""Materialise the three V7 Phase-8 B1 payloads and one-use releases.

This builder is deliberately inert until it receives a completed Phase-8
readiness receipt.  It performs no selector inference and no provider call.
The only comparatively expensive work is deterministic local tokenisation for
the Qwen and SkillRouter embedding preflights.

The output package binds one explicit user-approval record to three separate
one-use releases: BM25, Qwen embedding, and SkillRouter embedding.  Executing
those releases remains a separate command after this builder exits.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any


BUILDER_VERSION = "rq2b-v7-phase8-b1-dispatch-builder-v1"
APPROVAL_SCHEMA = "rq2b-v7-b36-c6-user-execution-approval-v1"
DISPATCH_SCHEMA = "rq2b-v7-phase8-b1-dispatch-manifest-v1"
LEDGER_SCHEMA = "rq2b-v7-phase8-b1-one-use-release-ledger-v1"
INTEGRITY_SCHEMA = "rq2b-v7-phase8-b1-dispatch-integrity-v1"
PHASE8_ROOT_SCHEMA = "rq2b-v7-phase8-final-execution-root-v1"
PHASE8_RECEIPT_SCHEMA = "rq2b-v7-phase8-readiness-receipt-v1"
PHASE8_READY = "READY_FOR_FORMAL_EXPERIMENT"

EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
EXPECTED_CONDITIONS = 36
EXPECTED_B1_ROWS = 4 * EXPECTED_QUERIES
TOP_K = 100
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"

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
VALIDATOR_REL = Path("skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py")
CHUNKER_REL = Path("skill_benchmark/scripts/rq2b_v7_exact_chunking_v2.py")
QWEN_PREFLIGHT_BUILDER_REL = Path(
    "skill_benchmark/scripts/build_rq2b_v7_qwen_b1_phase8_v3_preflight.py"
)
WINDOW_AMENDMENT_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_skillrouter_embedding_window_amendment_2026_09_09_v1/method_amendment.json"
)

FIXED_INPUTS = {
    "runtime": {
        "path": RUNTIME_REL.as_posix(),
        "sha256": "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
        "rows": EXPECTED_QUERIES,
    },
    "source_manifest": {
        "path": SOURCE_REL.as_posix(),
        "sha256": "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
        "rows": EXPECTED_SOURCES,
    },
    "conditions": {
        "path": CONDITIONS_REL.as_posix(),
        "sha256": "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
        "rows": EXPECTED_CONDITIONS,
    },
}

I1_I2_ROOT_ROLES = {
    "I1-discovery": ("i1_discovery_v2", "SOURCE_NATIVE_PHASE7_V2"),
    "I2-original": ("i2_original_v2", "SOURCE_NATIVE_PHASE7_V2"),
}
I3_ROOT_ROLES = {
    "I3C-fielded": ("i3c_fielded", "I3C_SUBAGENT_EXTRACTION_V4_1"),
    "I3-flat": ("i3_flat", "I3C_SUBAGENT_EXTRACTION_V4_1"),
}

RUNNER_SPECS = {
    "bm25_b1": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1_v2.py",
        "runner_version": "rq2b-v7-first-matrix-bm25-b1-runner-v2",
        "payload_schema": "rq2b-v7-bm25-b1-phase8-payload-v2",
        "authorisation_schema": "rq2b-v7-bm25-b1-root-release-v2",
    },
    "qwen_embedding_b1": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_qwen_b1_phase8_v3.py",
        "runner_version": "rq2b-v7-qwen-b1-phase8-runner-v3",
        "payload_schema": "rq2b-v7-qwen-b1-phase8-payload-v3",
        "authorisation_schema": "rq2b-v7-qwen-b1-phase8-root-release-v3",
    },
    "skillrouter_embedding_b1": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_skillrouter_embedding_b1.py",
        "runner_version": "rq2b-v7-skillrouter-embedding-b1-runner-v1",
        "payload_schema": "rq2b-v7-skillrouter-embedding-b1-phase8-payload-v1",
        "authorisation_schema": "rq2b-v7-skillrouter-embedding-b1-root-release-v1",
    },
}

BM25_WALL_SECONDS = 6 * 60 * 60
QWEN_WALL_SECONDS = 72 * 60 * 60
SKILLROUTER_WALL_SECONDS = 72 * 60 * 60
QWEN_PROVIDER_TOKEN_MULTIPLIER = 2


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected object: {path}:{line_number}")
            rows.append(value)
    return rows


def write_json_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text_new(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        handle.write(value)


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def root_path(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: relative path required")
    supplied = Path(value)
    require(not supplied.is_absolute(), f"{field}: absolute path forbidden")
    path = (root / supplied).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def bound_file(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, dict), f"{field}: object required")
    require(isinstance(value.get("path"), str), f"{field}: path missing")
    require(is_sha256(value.get("sha256")), f"{field}: SHA-256 missing")
    path = root_path(root, value["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: file missing")
    require(file_sha256(path) == value["sha256"], f"{field}: hash drift")
    return path


def jsonl_count(path: Path) -> int:
    with path.open("rb") as handle:
        return sum(1 for line in handle if line.strip())


def literal_constants(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    wanted = {"RUNNER_VERSION", "PAYLOAD_SCHEMA", "AUTHORISATION_SCHEMA"}
    result: dict[str, Any] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                try:
                    result[target.id] = ast.literal_eval(node.value)
                except (TypeError, ValueError):
                    pass
    return result


def validate_approval(root: Path, path: Path) -> dict[str, Any]:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Approval record must be inside repository root") from error
    value = read_json(path)
    require(value.get("schema_version") == APPROVAL_SCHEMA, "Approval schema drift")
    require(value.get("decision") == "APPROVED", "Execution has not been explicitly approved")
    scope = value.get("scope", {})
    require(scope.get("frozen_library") == "V7_3798_SOURCES_1077_QUERIES", "Approval library scope drift")
    require(scope.get("experiment") == "B36_CORE_PLUS_C6_DIAGNOSTIC", "Approval experiment scope drift")
    require(scope.get("phase8_b1_prerequisite") is True, "Approval does not cover B1")
    require(scope.get("external_qwen_embedding") is True, "Approval does not cover external embeddings")
    require(scope.get("local_skillrouter_embedding") is True, "Approval does not cover local embedding")
    require(value.get("secrets_recorded") is False, "Approval record must not contain secrets")
    quoted = value.get("user_instruction", {}).get("verbatim")
    require(isinstance(quoted, str) and "36个核心配置+6个诊断" in quoted, "Approval verbatim scope missing")
    return value


def validate_runner_root_binding(root: Path, root_manifest: dict[str, Any], role: str) -> None:
    expected = RUNNER_SPECS[role]
    actual = root_manifest.get("runners", {}).get(role)
    require(isinstance(actual, dict), f"Phase-8 root missing runner: {role}")
    runner_path = root_path(root, expected["path"], field=f"runner.{role}")
    require(runner_path.is_file(), f"Runner missing: {role}")
    constants = literal_constants(runner_path)
    require(constants.get("RUNNER_VERSION") == expected["runner_version"], f"{role}: runner literal drift")
    require(constants.get("PAYLOAD_SCHEMA") == expected["payload_schema"], f"{role}: payload literal drift")
    require(constants.get("AUTHORISATION_SCHEMA") == expected["authorisation_schema"], f"{role}: release literal drift")
    for key in ("path", "runner_version", "payload_schema", "authorisation_schema"):
        require(actual.get(key) == expected[key], f"{role}: Phase-8 root {key} drift")
    require(actual.get("sha256") == file_sha256(runner_path), f"{role}: Phase-8 root runner hash drift")


def validate_phase8(
    root: Path, receipt_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, dict[str, dict[str, Any]]]:
    try:
        receipt_path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Phase-8 receipt must be inside repository root") from error
    require(receipt_path.is_file(), "Final Phase-8 receipt is missing")
    receipt = read_json(receipt_path)
    require(receipt.get("schema_version") == PHASE8_RECEIPT_SCHEMA, "Phase-8 receipt schema drift")
    require(
        receipt.get("status") == "PASS_PHASE8_ROOT_READY_PENDING_EXPLICIT_PER_RUN_AUTHORISATION",
        "Phase-8 receipt is not a final PASS",
    )
    require(receipt.get("execution_authorised") is False, "Readiness receipt cannot itself authorise execution")
    require(receipt.get("label_provenance_access") == "HASH_ONLY_NO_CONTENT_PARSE", "Phase-8 receipt label-provenance boundary drift")
    root_binding = receipt.get("root_manifest")
    root_manifest_path = bound_file(root, root_binding, field="phase8.root_manifest")
    root_manifest = read_json(root_manifest_path)
    require(root_manifest.get("schema_version") == PHASE8_ROOT_SCHEMA, "Phase-8 root schema drift")
    require(root_manifest.get("status") == PHASE8_READY, "Phase-8 root is not READY")
    require(root_manifest.get("execution_authorised") is False, "Phase-8 root cannot itself authorise execution")
    require(root_manifest.get("selector_provider_or_model_runs") == 0, "Phase-8 root observed selector work")
    require(root_manifest.get("labels_or_results_content_read") is False, "Phase-8 root label/result isolation drift")
    scope = root_manifest.get("scope", {})
    require(scope.get("queries") == EXPECTED_QUERIES, "Phase-8 query scope drift")
    require(scope.get("sources") == EXPECTED_SOURCES, "Phase-8 source scope drift")
    require(scope.get("core_conditions") == 36 and scope.get("bridge_conditions") == 6, "Phase-8 matrix scope drift")
    require(scope.get("source_union_sha256") == SOURCE_UNION_SHA256, "Phase-8 source-union drift")
    require(scope.get("prompt_manifest_sha256") == PROMPT_MANIFEST_SHA256, "Phase-8 prompt-manifest drift")
    require(scope.get("u0323_excluded") is True, "U0323 exclusion drift")
    for role in RUNNER_SPECS:
        validate_runner_root_binding(root, root_manifest, role)

    representations: dict[str, dict[str, Any]] = {}
    for representation, (role, protocol) in {**I1_I2_ROOT_ROLES, **I3_ROOT_ROLES}.items():
        section = "fixed_artifacts" if representation in I1_I2_ROOT_ROLES else "final_phase7_artifacts"
        item = root_manifest.get(section, {}).get(role)
        path = bound_file(root, item, field=f"phase8.{section}.{role}")
        require(jsonl_count(path) == EXPECTED_SOURCES, f"{representation}: expected 3,798 rows")
        representations[representation] = {
            "path": relative(path, root),
            "sha256": item["sha256"],
            "rows": EXPECTED_SOURCES,
            "phase8_final": True,
            "extraction_protocol": protocol,
        }
    return receipt, root_manifest, root_manifest_path, representations


def implementation_binding(root: Path, rel_path: Path) -> dict[str, str]:
    path = root / rel_path
    require(path.is_file(), f"Implementation missing: {rel_path}")
    return {"path": rel_path.as_posix(), "sha256": file_sha256(path)}


def phase8_payload_binding(receipt_path: Path, root: Path) -> dict[str, Any]:
    return {
        "status": "PASS",
        "receipt": {"path": relative(receipt_path, root), "sha256": file_sha256(receipt_path)},
        "final_v4_1_i3_hashes_bound": True,
    }


def build_bm25_payload(
    *, root: Path, receipt_path: Path, representations: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": RUNNER_SPECS["bm25_b1"]["payload_schema"],
        "state": "SEALED_LABEL_FREE_PHASE8_PAYLOAD",
        "runner_version": RUNNER_SPECS["bm25_b1"]["runner_version"],
        "implementation": {
            "runner": implementation_binding(root, Path(RUNNER_SPECS["bm25_b1"]["path"])),
            "official_output_validator": implementation_binding(root, VALIDATOR_REL),
        },
        "phase8": phase8_payload_binding(receipt_path, root),
        "inputs": {**FIXED_INPUTS, "representations": representations},
        "counts": {
            "queries": EXPECTED_QUERIES,
            "sources": EXPECTED_SOURCES,
            "representations": 4,
            "b1_cells": 4,
            "b1_output_rows": EXPECTED_B1_ROWS,
        },
        "method": {
            "retriever": "BM25",
            "tokenizer": "lowercase_[a-z0-9]+",
            "query_term_frequency": "multiplicative",
            "idf": "ln(1+(N-df+0.5)/(df+0.5))",
            "k1": 1.5,
            "b": 0.75,
            "stable_tie_break": "source_sha256_ascending",
            "top_k": TOP_K,
        },
        "isolation": {
            "labels_or_results_read": False,
            "selector_inputs_are_source_only": True,
            "offline_scorer_run": False,
        },
    }


def build_skillrouter_payload(
    *, root: Path, receipt_path: Path, representations: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    from run_rq2b_v7_skillrouter_embedding_b1 import (
        DIMENSIONS,
        MODEL,
        MODEL_MAX_TOKENS,
        OVERLAP_TOKENS,
        QUERY_INSTRUCTION,
        REVISION,
        WINDOW_TOKENS,
    )

    return {
        "schema_version": RUNNER_SPECS["skillrouter_embedding_b1"]["payload_schema"],
        "state": "SEALED_LABEL_FREE_PHASE8_PAYLOAD",
        "runner_version": RUNNER_SPECS["skillrouter_embedding_b1"]["runner_version"],
        "implementation": {
            "runner": implementation_binding(root, Path(RUNNER_SPECS["skillrouter_embedding_b1"]["path"])),
            "chunker": implementation_binding(root, CHUNKER_REL),
        },
        "phase8": phase8_payload_binding(receipt_path, root),
        "inputs": {**FIXED_INPUTS, "representations": representations},
        "counts": {
            "queries": EXPECTED_QUERIES,
            "sources": EXPECTED_SOURCES,
            "representations": 4,
            "b1_cells": 4,
            "b1_output_rows": EXPECTED_B1_ROWS,
        },
        "method": {
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
        },
        "label_isolation": {
            "labels_or_results_read": False,
            "selector_inputs_are_source_only": True,
            "offline_scorer_run": False,
        },
    }


def deterministic_ids(root_sha256: str, role: str) -> dict[str, str]:
    require(is_sha256(root_sha256), "Invalid root SHA-256")
    require(role in RUNNER_SPECS, f"Unknown B1 role: {role}")
    stem = role.replace("_", "-").upper()
    suffix = root_sha256[:16]
    return {
        "root_release_id": f"RQ2B-V7-P8-{stem}-{suffix}-R1",
        "run_id": f"RQ2B-V7-P8-{stem}-{suffix}",
        "attempt_id": f"RQ2B-V7-P8-{stem}-{suffix}-A1",
    }


def cache_prefix(root_sha256: str) -> str:
    require(is_sha256(root_sha256), "Invalid root SHA-256")
    return f"skill_benchmark/cache/rq2b_v7_phase8_b1_{root_sha256[:16]}"


def skillrouter_preflight(
    *, root: Path, payload: dict[str, Any], snapshot_path: Path, cache_dir: Path,
) -> dict[str, Any]:
    from transformers import AutoTokenizer
    import run_rq2b_v7_skillrouter_embedding_b1 as runner

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    tokenizer = AutoTokenizer.from_pretrained(
        snapshot_path,
        local_files_only=True,
        trust_remote_code=False,
    )
    prompts, _, _, representations = runner.load_authority(root, payload)
    inventory, documents, query_text_ids, summary = runner.build_work_inventory(
        tokenizer, prompts, representations
    )
    cache = runner.ExactEmbeddingCache(cache_dir)
    initial_hits = {text_id: cache.load(item) is not None for text_id, item in inventory.items()}
    document_ids = sorted({
        text_id
        for rows in documents.values()
        for document in rows
        for text_id in document["chunk_text_ids"]
    })
    query_ids = sorted(set(query_text_ids.values()))
    missing_document = [inventory[text_id] for text_id in document_ids if not initial_hits[text_id]]
    missing_query = [inventory[text_id] for text_id in query_ids if not initial_hits[text_id]]
    batches = [
        *runner.exact_length_batches(missing_document),
        *runner.exact_length_batches(missing_query),
    ]
    missing = [*missing_document, *missing_query]
    ceilings = {
        "maximum_new_cache_entries": len(missing),
        "maximum_model_input_instances": len(missing),
        "maximum_model_input_tokens": sum(item["model_input_tokens"] for item in missing),
        "maximum_model_forward_batches": len(batches),
        "maximum_wall_time_seconds": SKILLROUTER_WALL_SECONDS,
    }
    return {
        "schema_version": "rq2b-v7-skillrouter-embedding-b1-zero-inference-preflight-v1",
        "status": "PASS_EXACT_LOCAL_TOKENISATION_NO_MODEL_FORWARD",
        "counts": {
            "unique_work_items": len(inventory),
            "unique_document_windows": len(document_ids),
            "unique_queries": len(query_ids),
            "initial_cache_hits": sum(initial_hits.values()),
            "initial_cache_misses": len(missing),
            "model_forward_batches_if_cache_unchanged": len(batches),
        },
        "ceilings": ceilings,
        "representation_window_summary": summary,
        "network_calls": 0,
        "provider_calls": 0,
        "model_forwards": 0,
    }


def build_bm25_release(
    *, payload_path: Path, payload: dict[str, Any], root: Path, root_sha256: str,
) -> dict[str, Any]:
    ids = deterministic_ids(root_sha256, "bm25_b1")
    prefix = cache_prefix(root_sha256)
    return {
        "schema_version": RUNNER_SPECS["bm25_b1"]["authorisation_schema"],
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_ROOT_RELEASED_EXECUTION",
        "one_use": True,
        "consumed": False,
        **ids,
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "phase8": {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]},
        "destinations": {
            "output_dir": f"{prefix}/bm25/output",
            "attempt_dir": f"{prefix}/bm25/attempt",
        },
        "ceilings": {
            "maximum_queries": EXPECTED_QUERIES,
            "maximum_sources": EXPECTED_SOURCES,
            "maximum_output_rows": EXPECTED_B1_ROWS,
            "maximum_ranked_candidates": EXPECTED_B1_ROWS * TOP_K,
            "maximum_wall_time_seconds": BM25_WALL_SECONDS,
        },
    }


def build_qwen_release(
    *, root: Path, root_sha256: str, payload_path: Path,
    preflight_path: Path, payload: dict[str, Any], timeout_seconds: int,
) -> dict[str, Any]:
    from build_rq2b_v7_qwen_b1_phase8_v3_preflight import (
        BASE_URL, CLEAN_CACHE_REL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL,
    )

    ids = deterministic_ids(root_sha256, "qwen_embedding_b1")
    prefix = cache_prefix(root_sha256)
    predictable = payload["predictable_ceilings"]
    provider_ceiling = max(
        1,
        QWEN_PROVIDER_TOKEN_MULTIPLIER
        * predictable["maximum_external_model_input_proxy_tokens"],
    )
    return {
        "schema_version": RUNNER_SPECS["qwen_embedding_b1"]["authorisation_schema"],
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_QWEN_B1_EXECUTION",
        "one_use": True,
        "consumed": False,
        **ids,
        "runner_version": RUNNER_SPECS["qwen_embedding_b1"]["runner_version"],
        "payload_schema": RUNNER_SPECS["qwen_embedding_b1"]["payload_schema"],
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "preflight": {"path": relative(preflight_path, root), "sha256": file_sha256(preflight_path)},
        "phase8": {
            "receipt_sha256": payload["phase8"]["receipt"]["sha256"],
            "root_manifest_sha256": payload["phase8"]["root_manifest"]["sha256"],
        },
        "provider": {
            "base_url": BASE_URL,
            "endpoint": "/embeddings",
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "api_key_env": "DASHSCOPE_API_KEY",
            "timeout_seconds": timeout_seconds,
            "maximum_batch_texts": MAX_BATCH_TEXTS,
            "automatic_retries": 0,
            "cold_query_batch_size": 1,
        },
        "destinations": {
            "output_dir": f"{prefix}/qwen/output",
            "attempt_dir": f"{prefix}/qwen/attempt",
            "clean_cache_root": CLEAN_CACHE_REL.as_posix(),
        },
        "ceilings": {
            **predictable,
            "maximum_provider_reported_total_tokens": provider_ceiling,
            "maximum_wall_time_seconds": QWEN_WALL_SECONDS,
        },
    }


def build_skillrouter_release(
    *, root: Path, root_manifest: dict[str, Any], root_sha256: str,
    payload_path: Path, payload: dict[str, Any], preflight: dict[str, Any],
) -> dict[str, Any]:
    import run_rq2b_v7_skillrouter_embedding_b1 as runner

    ids = deterministic_ids(root_sha256, "skillrouter_embedding_b1")
    prefix = cache_prefix(root_sha256)
    snapshot = root_manifest.get("models", {}).get("skillrouter_embedding")
    require(isinstance(snapshot, dict), "Phase-8 root lacks SkillRouter embedding snapshot")
    require(snapshot.get("repository") == runner.MODEL, "SkillRouter snapshot repository drift")
    require(snapshot.get("revision") == runner.REVISION, "SkillRouter snapshot revision drift")
    require(snapshot.get("files") == runner.MODEL_FILE_SHA256, "SkillRouter snapshot files drift")
    snapshot_path = root_path(root, snapshot.get("snapshot_path"), field="models.skillrouter_embedding.snapshot_path")
    require(snapshot_path.is_dir(), "SkillRouter snapshot directory missing")
    for name, expected in runner.MODEL_FILE_SHA256.items():
        path = snapshot_path / name
        require(path.is_file() and file_sha256(path) == expected, f"SkillRouter model file drift: {name}")

    amendment = root_manifest.get("final_phase7_artifacts", {}).get("window_method_amendment")
    amendment_path = bound_file(root, amendment, field="phase8.final_phase7_artifacts.window_method_amendment")
    require(relative(amendment_path, root) == WINDOW_AMENDMENT_REL.as_posix(), "Window amendment path drift")
    return {
        "schema_version": RUNNER_SPECS["skillrouter_embedding_b1"]["authorisation_schema"],
        "state": "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_ROOT_RELEASED_EXECUTION",
        **ids,
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "phase8": {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]},
        "window_amendment": {
            "status": "APPROVED_FOR_THIS_ROOT_RELEASE",
            "method_path": relative(amendment_path, root),
            "method_sha256": file_sha256(amendment_path),
            "window_tokens": runner.WINDOW_TOKENS,
            "overlap_tokens": runner.OVERLAP_TOKENS,
            "aggregation": "maximum_query_to_window_cosine",
        },
        "model_snapshot": {
            "path": relative(snapshot_path, root),
            "repository": runner.MODEL,
            "revision": runner.REVISION,
            "files": runner.MODEL_FILE_SHA256,
        },
        "runtime": {
            "device": "mps",
            "dtype": "bfloat16",
            "attention_implementation": "default_sdpa",
            "exact_model_input_token_length_batches": True,
            "padding": False,
            "maximum_batch_size": runner.MAX_BATCH_SIZE,
            "automatic_retries": 0,
            "local_files_only": True,
            "trust_remote_code": False,
        },
        "destinations": {
            "output_dir": f"{prefix}/skillrouter/output",
            "cache_dir": "skill_benchmark/cache/rq2b_v7_skillrouter_embedding_b1_v1/embeddings",
            "attempt_dir": f"{prefix}/skillrouter/attempt",
        },
        "ceilings": preflight["ceilings"],
    }


def render_readme(manifest: dict[str, Any]) -> str:
    commands = manifest["execution_commands"]
    return f"""# V7 Phase-8 B1 dispatch

Status: `READY_THREE_ONE_USE_RELEASES_NOT_YET_CONSUMED`.

This package was derived from one final Phase-8 root and one explicit user
approval record. It contains label-free payload/release bindings for the four
BM25 cells, four Qwen embedding cells, and four SkillRouter embedding cells.
It performs no target join, scoring, model inference, or provider call.

The Qwen payload and its exact request/cache preflight live under ignored
`skill_benchmark/cache/`; their paths and SHA-256 values are frozen in the
release ledger. Do not rebuild them after execution starts.

Run each command at most once, from the repository root, with the same frozen
checkout. The Qwen command requires `DASHSCOPE_API_KEY` in the environment; no
secret is stored in this package.

## BM25 B1

```sh
{commands['bm25_b1']}
```

## Qwen embedding B1

```sh
{commands['qwen_embedding_b1']}
```

## SkillRouter embedding B1

```sh
{commands['skillrouter_embedding_b1']}
```

After all three complete, combine the 12 B1 cells and run the official output
validator before any B2 payload is materialised. A B1 release authorises only
its named runner, destinations, and ceilings; it does not authorise B2 or
offline scoring by itself.
"""


def materialize(
    *, root: Path, phase8_receipt_path: Path, approval_path: Path,
    output_dir: Path, qwen_payload_dir: Path, qwen_preflight_path: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    root = root.resolve()
    for label, path in (
        ("dispatch output", output_dir),
        ("Qwen payload", qwen_payload_dir),
        ("Qwen preflight receipt", qwen_preflight_path),
    ):
        try:
            path.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError(f"{label} must be inside repository root") from error
    require(not output_dir.exists(), "Dispatch output already exists; overwrite forbidden")
    require(relative(qwen_payload_dir, root).startswith("skill_benchmark/cache/"), "Qwen payload must be under cache")
    require(relative(qwen_preflight_path, root).startswith("skill_benchmark/cache/"), "Qwen preflight must be under cache")
    require(isinstance(timeout_seconds, int) and timeout_seconds > 0, "Timeout must be a positive integer")

    approval = validate_approval(root, approval_path)
    receipt, root_manifest, root_manifest_path, representations = validate_phase8(
        root, phase8_receipt_path
    )
    root_sha = file_sha256(root_manifest_path)
    expected_prefix = Path(cache_prefix(root_sha))
    require(
        qwen_payload_dir == root / expected_prefix / "qwen/payload",
        "Qwen payload path must use the deterministic root-SHA cache prefix",
    )
    require(
        qwen_preflight_path == root / expected_prefix / "qwen/preflight_receipt.json",
        "Qwen preflight path must use the deterministic root-SHA cache prefix",
    )

    bm25_payload = build_bm25_payload(
        root=root, receipt_path=phase8_receipt_path, representations=representations
    )
    skillrouter_payload = build_skillrouter_payload(
        root=root, receipt_path=phase8_receipt_path, representations=representations
    )

    # The existing Qwen preflight is the single authority for its exact
    # label-free text, request, and cache inventory. It contains no provider
    # call and fails closed on an incomplete/stale Phase-8 root.
    from build_rq2b_v7_qwen_b1_phase8_v3_preflight import run_preflight

    run_preflight(
        root=root,
        phase8_receipt_path=phase8_receipt_path,
        payload_dir=qwen_payload_dir,
        preflight_receipt_path=qwen_preflight_path,
    )
    qwen_payload_path = qwen_payload_dir / "payload_manifest.json"
    qwen_payload = read_json(qwen_payload_path)

    staging = output_dir.parent / f".{output_dir.name}.staging-{os.getpid()}"
    require(not staging.exists(), f"Stale dispatch staging path: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    bm25_payload_final = output_dir / "payloads/bm25_b1_payload.json"
    skillrouter_payload_final = output_dir / "payloads/skillrouter_embedding_b1_payload.json"
    write_json_new(staging / "payloads/bm25_b1_payload.json", bm25_payload)
    write_json_new(staging / "payloads/skillrouter_embedding_b1_payload.json", skillrouter_payload)
    staging.replace(output_dir)

    # Validate runner payloads after publication because their own validators
    # require the final repository-relative paths and hashes.
    import run_rq2b_v7_first_matrix_bm25_b1_v2 as bm25_runner
    import run_rq2b_v7_qwen_b1_phase8_v3 as qwen_runner
    import run_rq2b_v7_skillrouter_embedding_b1 as skillrouter_runner

    bm25_runner.validate_payload(root, bm25_payload_final)
    skillrouter_runner.validate_payload(root, skillrouter_payload_final)
    sr_snapshot = root_path(
        root,
        root_manifest["models"]["skillrouter_embedding"]["snapshot_path"],
        field="models.skillrouter_embedding.snapshot_path",
    )
    sr_cache = root / "skill_benchmark/cache/rq2b_v7_skillrouter_embedding_b1_v1/embeddings"
    sr_preflight = skillrouter_preflight(
        root=root,
        payload=skillrouter_payload,
        snapshot_path=sr_snapshot,
        cache_dir=sr_cache,
    )
    write_json_new(output_dir / "skillrouter_zero_inference_preflight.json", sr_preflight)

    bm25_release = build_bm25_release(
        payload_path=bm25_payload_final,
        payload=bm25_payload,
        root=root,
        root_sha256=root_sha,
    )
    qwen_release = build_qwen_release(
        root=root,
        root_sha256=root_sha,
        payload_path=qwen_payload_path,
        preflight_path=qwen_preflight_path,
        payload=qwen_payload,
        timeout_seconds=timeout_seconds,
    )
    skillrouter_release = build_skillrouter_release(
        root=root,
        root_manifest=root_manifest,
        root_sha256=root_sha,
        payload_path=skillrouter_payload_final,
        payload=skillrouter_payload,
        preflight=sr_preflight,
    )
    release_paths = {
        "bm25_b1": output_dir / "authorisations/bm25_b1.one_use.json",
        "qwen_embedding_b1": output_dir / "authorisations/qwen_embedding_b1.one_use.json",
        "skillrouter_embedding_b1": output_dir / "authorisations/skillrouter_embedding_b1.one_use.json",
    }
    releases = {
        "bm25_b1": bm25_release,
        "qwen_embedding_b1": qwen_release,
        "skillrouter_embedding_b1": skillrouter_release,
    }
    for role, path in release_paths.items():
        write_json_new(path, releases[role])

    bm25_runner.validate_root_release(root, release_paths["bm25_b1"])
    qwen_runner.validate_root_release(
        root=root,
        release_path=release_paths["qwen_embedding_b1"],
        payload_path=qwen_payload_path,
        preflight_path=qwen_preflight_path,
        payload=qwen_payload,
        run_id=qwen_release["run_id"],
        output_dir=root / qwen_release["destinations"]["output_dir"],
        attempt_dir=root / qwen_release["destinations"]["attempt_dir"],
        api_key_env="DASHSCOPE_API_KEY",
        timeout_seconds=timeout_seconds,
    )
    skillrouter_runner.validate_root_release(root, release_paths["skillrouter_embedding_b1"])

    commands = {
        "bm25_b1": (
            "python3 -B skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1_v2.py "
            f"--execute --authorisation {relative(release_paths['bm25_b1'], root)}"
        ),
        "qwen_embedding_b1": (
            ".venv-rq2b-v7/bin/python3 -B skill_benchmark/scripts/run_rq2b_v7_qwen_b1_phase8_v3.py --execute "
            f"--payload {relative(qwen_payload_path, root)} "
            f"--preflight-receipt {relative(qwen_preflight_path, root)} "
            f"--root-release {relative(release_paths['qwen_embedding_b1'], root)} "
            f"--output-dir {qwen_release['destinations']['output_dir']} "
            f"--attempt-dir {qwen_release['destinations']['attempt_dir']} "
            f"--run-id {qwen_release['run_id']} --api-key-env DASHSCOPE_API_KEY "
            f"--timeout-seconds {timeout_seconds}"
        ),
        "skillrouter_embedding_b1": (
            ".venv-rq2b-v7/bin/python3 -B skill_benchmark/scripts/run_rq2b_v7_skillrouter_embedding_b1.py "
            f"--execute --authorisation {relative(release_paths['skillrouter_embedding_b1'], root)}"
        ),
    }
    ledger = {
        "schema_version": LEDGER_SCHEMA,
        "status": "READY_THREE_UNUSED_ONE_USE_RELEASES",
        "approval_record": {
            "path": relative(approval_path, root),
            "sha256": file_sha256(approval_path),
            "decision": approval["decision"],
        },
        "phase8": {
            "receipt": {"path": relative(phase8_receipt_path, root), "sha256": file_sha256(phase8_receipt_path)},
            "root_manifest": {"path": relative(root_manifest_path, root), "sha256": root_sha},
            "package_id": root_manifest["package_id"],
        },
        "releases": {
            role: {
                "path": relative(path, root),
                "sha256": file_sha256(path),
                "root_release_id": releases[role]["root_release_id"],
                "run_id": releases[role]["run_id"],
                "attempt_id": releases[role]["attempt_id"],
                "one_use": True,
                "consumed": False,
                "ceilings": releases[role]["ceilings"],
            }
            for role, path in release_paths.items()
        },
        "label_isolation": {
            "label_files_read": False,
            "acceptable_sets_read": False,
            "results_read": False,
            "offline_scoring_run": False,
        },
        "external_activity_during_build": {
            "network_calls": 0,
            "provider_calls": 0,
            "model_forwards": 0,
        },
    }
    write_json_new(output_dir / "one_use_release_ledger.json", ledger)
    manifest = {
        "schema_version": DISPATCH_SCHEMA,
        "status": "READY_THREE_ONE_USE_RELEASES_NOT_YET_CONSUMED",
        "builder": implementation_binding(root, Path(__file__).resolve().relative_to(root)),
        "approval_record": ledger["approval_record"],
        "phase8": ledger["phase8"],
        "payloads": {
            "bm25_b1": {"path": relative(bm25_payload_final, root), "sha256": file_sha256(bm25_payload_final)},
            "qwen_embedding_b1": {"path": relative(qwen_payload_path, root), "sha256": file_sha256(qwen_payload_path)},
            "skillrouter_embedding_b1": {"path": relative(skillrouter_payload_final, root), "sha256": file_sha256(skillrouter_payload_final)},
        },
        "preflights": {
            "qwen_embedding_b1": {"path": relative(qwen_preflight_path, root), "sha256": file_sha256(qwen_preflight_path)},
            "skillrouter_embedding_b1": {
                "path": relative(output_dir / "skillrouter_zero_inference_preflight.json", root),
                "sha256": file_sha256(output_dir / "skillrouter_zero_inference_preflight.json"),
            },
        },
        "release_ledger": {
            "path": relative(output_dir / "one_use_release_ledger.json", root),
            "sha256": file_sha256(output_dir / "one_use_release_ledger.json"),
        },
        "execution_commands": commands,
        "next_gate": "COMPLETE_AND_OFFICIALLY_VALIDATE_ALL_12_B1_CELLS_BEFORE_B2",
    }
    write_json_new(output_dir / "dispatch_manifest.json", manifest)
    write_text_new(output_dir / "README.md", render_readme(manifest))

    artifact_paths = [
        output_dir / "payloads/bm25_b1_payload.json",
        output_dir / "payloads/skillrouter_embedding_b1_payload.json",
        output_dir / "skillrouter_zero_inference_preflight.json",
        *release_paths.values(),
        output_dir / "one_use_release_ledger.json",
        output_dir / "dispatch_manifest.json",
        output_dir / "README.md",
        qwen_payload_path,
        qwen_preflight_path,
    ]
    integrity = {
        "schema_version": INTEGRITY_SCHEMA,
        "status": "PASS_B1_PAYLOADS_AND_UNUSED_ONE_USE_RELEASES_MATERIALISED",
        "phase8_root_sha256": root_sha,
        "approval_record_sha256": file_sha256(approval_path),
        "artifacts": [
            {"path": relative(path, root), "sha256": file_sha256(path), "bytes": path.stat().st_size}
            for path in artifact_paths
        ],
        "assertions": {
            "phase8_root_replayed": "PASS",
            "three_runner_hashes_replayed": "PASS",
            "four_final_representation_hashes_replayed": "PASS",
            "all_payloads_label_free": "PASS",
            "explicit_user_approval_bound": "PASS",
            "three_releases_one_use_and_unconsumed": "PASS",
            "qwen_exact_request_preflight_passed": "PASS",
            "skillrouter_exact_tokenisation_preflight_passed": "PASS",
            "provider_calls_during_build": 0,
            "model_forwards_during_build": 0,
        },
    }
    write_json_new(output_dir / "integrity_report.json", integrity)
    return {
        "status": integrity["status"],
        "output_dir": relative(output_dir, root),
        "phase8_root_sha256": root_sha,
        "release_ledger_sha256": file_sha256(output_dir / "one_use_release_ledger.json"),
        "dispatch_manifest_sha256": file_sha256(output_dir / "dispatch_manifest.json"),
        "provider_calls": 0,
        "model_forwards": 0,
    }


def self_test() -> dict[str, Any]:
    root_sha = "a" * 64
    first = deterministic_ids(root_sha, "bm25_b1")
    second = deterministic_ids(root_sha, "bm25_b1")
    require(first == second, "Deterministic run identities drift")
    require(cache_prefix(root_sha).endswith("a" * 16), "Deterministic cache prefix drift")
    require(EXPECTED_B1_ROWS == 4308, "B1 output cardinality drift")
    require(EXPECTED_B1_ROWS * TOP_K == 430800, "BM25 candidate ceiling drift")
    require(QWEN_PROVIDER_TOKEN_MULTIPLIER == 2, "Qwen provider ceiling policy drift")
    require(BM25_WALL_SECONDS < QWEN_WALL_SECONDS == SKILLROUTER_WALL_SECONDS, "Wall-ceiling policy drift")
    return {
        "status": "PASS_PHASE8_B1_DISPATCH_BUILDER_SELF_TEST_NO_EXECUTION",
        "network_calls": 0,
        "provider_calls": 0,
        "model_forwards": 0,
        "checks": {
            "deterministic_ids": True,
            "deterministic_cache_prefix": True,
            "exact_b1_cardinality": True,
            "bounded_wall_time_policy": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--materialize", action="store_true")
    parser.add_argument("--phase8-receipt", type=Path)
    parser.add_argument("--approval-record", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.phase8_receipt is not None, "--phase8-receipt is required")
        require(args.approval_record is not None, "--approval-record is required")
        require(args.output_dir is not None, "--output-dir is required")
        root = args.root.resolve()
        resolve = lambda path: path if path.is_absolute() else root / path
        phase8 = resolve(args.phase8_receipt)
        approval = resolve(args.approval_record)
        output = resolve(args.output_dir)
        # Read and replay the final root before deriving root-SHA cache paths.
        _, _, root_manifest_path, _ = validate_phase8(root, phase8)
        prefix = root / cache_prefix(file_sha256(root_manifest_path))
        result = materialize(
            root=root,
            phase8_receipt_path=phase8,
            approval_path=approval,
            output_dir=output,
            qwen_payload_dir=prefix / "qwen/payload",
            qwen_preflight_path=prefix / "qwen/preflight_receipt.json",
            timeout_seconds=args.timeout_seconds,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
