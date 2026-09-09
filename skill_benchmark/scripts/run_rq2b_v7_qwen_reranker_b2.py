#!/usr/bin/env python3
"""Run the 15 materialised V7 Qwen qwen3-rerank B2 conditions.

The runner is fail-closed and label-free.  It consumes only an explicitly
root-released, Phase-8/hash-bound set of source representations plus already
persisted and officially validated B1 Top-20 rows.  It never regenerates a
candidate list.  B01-GQ..B12-GQ and C1-Q/C3-Q/C4-Q are materialised for all
1,077 frozen queries; C2-Q remains the exact B05-GQ alias and is not emitted.

Provider execution has no automatic retry.  Each attempted request gets an
immutable start receipt before network I/O and either a completion or failure
receipt afterwards.  Incomplete runs retain their attempt directory and never
publish a completed output directory.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import platform
import socket
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from rq2b_chunking import CHUNKER_VERSION as CHUNKER_V1_VERSION
from rq2b_chunking import exact_text_chunks
from rq2b_v7_exact_chunking_v2 import CHUNKER_VERSION as CHUNKER_V2_VERSION
from rq2b_v7_exact_chunking_v2 import exact_text_chunks as exact_text_chunks_v2
from rq2b_qwen_reranker import (
    ANCHOR_SCORE_ABS_TOLERANCE,
    ENDPOINT,
    INSTRUCTION,
    MAX_DOCUMENTS_PER_REQUEST,
    MAX_REQUEST_PROXY_TOKENS,
    MAX_TOKENS_PER_DOCUMENT,
    MODEL,
    REQUEST_FIXED_PROXY_TOKENS,
    RUNNER_CONTRACT_VERSION,
    WINDOW_OVERLAP_PROXY_TOKENS,
    WINDOW_PROXY_TOKENS,
    build_request_batches,
    parse_response_scores,
    trusted_binding_from_sources,
    validate_condition,
    verify_duplicate_anchor_scores,
)


RUNNER_VERSION = "rq2b-v7-qwen-reranker-b2-runner-v1"
PAYLOAD_SCHEMA = "rq2b-v7-qwen-reranker-b2-phase8-payload-v1"
AUTHORISATION_SCHEMA = "rq2b-v7-qwen-reranker-b2-root-release-v1"
PENDING_RELEASE_SCHEMA = "rq2b-v7-qwen-reranker-b2-pending-release-v1"
PREFLIGHT_SCHEMA = "rq2b-v7-qwen-reranker-b2-no-provider-preflight-v1"
B1_SCHEMA = "rq2b-v7-b1-runner-output-v1"
B2_SCHEMA = "rq2b-v7-b2-runner-output-v1"
B1_VALIDATION_RECEIPT_SCHEMA = "rq2b-v7-phase8-b1-official-validation-receipt-v1"
EXECUTION_APPROVAL_SCHEMA = "rq2b-v7-b36-c6-b2-user-execution-approval-v1"
TOP_K = 20
EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
EXPECTED_B1_ROWS = 12 * EXPECTED_QUERIES
EXPECTED_B2_ROWS = 15 * EXPECTED_QUERIES
DEFAULT_TIMEOUT_SECONDS = 120
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
API_KEY_ENV = "DASHSCOPE_API_KEY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl"
)
SOURCE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/source_manifest.jsonl"
)
CORE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl"
)
BRIDGE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_first_matrix_2026_09_08_v1/fixed_candidate_bridge_conditions.jsonl"
)
HELPER_REL = Path("skill_benchmark/scripts/rq2b_qwen_reranker.py")
CHUNKER_V1_REL = Path("skill_benchmark/scripts/rq2b_chunking.py")
CHUNKER_V2_REL = Path("skill_benchmark/scripts/rq2b_v7_exact_chunking_v2.py")
VALIDATOR_REL = Path("skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py")

FIXED_INPUT_SHA256 = {
    RUNTIME_REL: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    SOURCE_REL: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    CORE_REL: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
    BRIDGE_REL: "d659ff98a5a2534478f68ab44794e4df7d89b23eb3a44a2fbf335cdca42366f7",
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
PROXY_TOKENIZER = {
    "repository": "pipizhao/SkillRouter-Embedding-0.6B",
    "revision": "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558",
    "path": "skill_benchmark/cache/huggingface/SkillRouter-Embedding-0.6B-c03c9bcee9fc",
    "tokenizer_json_sha256": "def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a",
}
REPRESENTATIONS = ("I1-discovery", "I2-original", "I3C-fielded", "I3-flat")
CORE_GQ_CONDITIONS = tuple(f"B{index:02d}-GQ" for index in range(1, 13))
BRIDGE_GQ_CONDITIONS = ("C1-Q", "C3-Q", "C4-Q")
MATERIALISED_CONDITIONS = CORE_GQ_CONDITIONS + BRIDGE_GQ_CONDITIONS
B1_CONDITIONS = tuple(f"B{index:02d}-G0" for index in range(1, 13))
HEX = set("0123456789abcdef")
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}
CEILING_KEYS = {
    "maximum_request_attempts",
    "maximum_successful_calls",
    "maximum_external_documents",
    "maximum_external_submission_proxy_tokens",
    "maximum_external_submission_utf8_bytes",
    "maximum_provider_total_tokens",
    "maximum_wall_time_seconds",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def exact_keys(value: Any, expected: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: object required")
    missing = expected - set(value)
    extra = set(value) - expected
    require(not missing and not extra, f"{field}: missing={sorted(missing)} extra={sorted(extra)}")


def root_path(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: non-empty relative path required")
    raw = Path(value)
    require(not raw.is_absolute(), f"{field}: absolute path forbidden")
    resolved = (root / raw).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return resolved


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path}: JSON object required")
    return value


def read_jsonl_any(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    context = (
        gzip.open(path, "rt", encoding="utf-8", newline="")
        if path.suffix == ".gz"
        else path.open("r", encoding="utf-8", newline="")
    )
    with context as handle:
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
    digest = hashlib.sha256()
    row_count = 0
    raw_bytes = 0
    with path.open("xb") as raw_handle:
        with gzip.GzipFile(fileobj=raw_handle, mode="wb", mtime=0) as gz_handle:
            for row in rows:
                encoded = (
                    json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode("utf-8")
                digest.update(encoded)
                raw_bytes += len(encoded)
                row_count += 1
                gz_handle.write(encoded)
    return {
        "path": path.as_posix(),
        "sha256": file_sha256(path),
        "rows": row_count,
        "utf8_bytes_compressed": path.stat().st_size,
        "canonical_jsonl_sha256_uncompressed": digest.hexdigest(),
        "utf8_bytes_uncompressed": raw_bytes,
        "compression": "gzip-mtime-0",
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
    root: Path, item: Any, *, field: str, rows: int | None = None
) -> Path:
    exact_keys(item, {"path", "sha256", "rows"}, field)
    require(is_sha256(item["sha256"]), f"{field}: invalid SHA-256")
    if rows is not None:
        require(item["rows"] == rows, f"{field}: row binding drift")
    path = root_path(root, item["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: artifact missing")
    require(file_sha256(path) == item["sha256"], f"{field}: artifact hash drift")
    return path


def validate_file_binding(root: Path, item: Any, *, field: str) -> Path:
    exact_keys(item, {"path", "sha256"}, field)
    require(is_sha256(item["sha256"]), f"{field}: invalid SHA-256")
    path = root_path(root, item["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: file missing")
    require(file_sha256(path) == item["sha256"], f"{field}: file hash drift")
    return path


def method_contract() -> dict[str, Any]:
    return {
        "helper_contract_version": RUNNER_CONTRACT_VERSION,
        "endpoint": ENDPOINT,
        "model": MODEL,
        "instruction": INSTRUCTION,
        "request_contract": {
            "input": ["query", "documents"],
            "parameters": {
                "instruct": INSTRUCTION,
                "return_documents": False,
                "top_n": "requested_document_count",
            },
        },
        "response_contract": "output.results exact unique index coverage plus finite relevance_score",
        "maximum_documents_per_request": MAX_DOCUMENTS_PER_REQUEST,
        "maximum_tokens_per_document": MAX_TOKENS_PER_DOCUMENT,
        "maximum_request_proxy_tokens": MAX_REQUEST_PROXY_TOKENS,
        "request_fixed_proxy_tokens": REQUEST_FIXED_PROXY_TOKENS,
        "document_window_proxy_tokens": WINDOW_PROXY_TOKENS,
        "document_window_overlap_proxy_tokens": WINDOW_OVERLAP_PROXY_TOKENS,
        "primary_chunker": CHUNKER_V1_VERSION,
        "pre_execution_chunker_parity_gate": CHUNKER_V2_VERSION,
        "cross_request_anchor": "complete_first_candidate_duplicated_after_each_split",
        "cross_request_anchor_absolute_tolerance": ANCHOR_SCORE_ABS_TOLERANCE,
        "document_score_aggregation": "maximum_window_score",
        "stable_tie_break": "source_sha256_ascending",
        "top_k": TOP_K,
        "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
        "automatic_retries": 0,
        "official_cost_input_tokens": "local_proxy_submission_tokens_including_fixed_overhead_and_duplicate_anchors",
        "official_cost_output_tokens": "provider_reported_output_tokens_or_zero_when_absent",
        "monetary_cost": "not_estimated; provider response does not freeze a price contract",
    }


def validate_payload(root: Path, path: Path) -> dict[str, Any]:
    payload = read_json(path)
    exact_keys(
        payload,
        {"schema_version", "state", "runner_version", "implementation", "phase8",
         "inputs", "b1_validation", "counts", "method", "label_isolation"},
        "payload",
    )
    require(payload["schema_version"] == PAYLOAD_SCHEMA, "Payload schema drift")
    require(
        payload["state"] == "SEALED_LABEL_FREE_PHASE8_B1_BOUND_PAYLOAD",
        "Payload is not Phase-8/B1 sealed",
    )
    require(payload["runner_version"] == RUNNER_VERSION, "Payload runner version drift")
    implementation = payload["implementation"]
    exact_keys(
        implementation,
        {"runner", "qwen_contract_helper", "exact_chunker_v1", "exact_chunker_v2",
         "official_output_validator"},
        "payload.implementation",
    )
    expected = {
        "runner": Path(__file__).resolve(),
        "qwen_contract_helper": (root / HELPER_REL).resolve(),
        "exact_chunker_v1": (root / CHUNKER_V1_REL).resolve(),
        "exact_chunker_v2": (root / CHUNKER_V2_REL).resolve(),
        "official_output_validator": (root / VALIDATOR_REL).resolve(),
    }
    for name, expected_path in expected.items():
        binding = implementation[name]
        exact_keys(binding, {"path", "sha256"}, f"payload.implementation.{name}")
        require(
            root_path(root, binding["path"], field=f"implementation.{name}.path")
            == expected_path,
            f"Implementation path drift: {name}",
        )
        require(binding["sha256"] == file_sha256(expected_path), f"Implementation hash drift: {name}")

    phase8 = payload["phase8"]
    exact_keys(phase8, {"status", "receipt", "final_v4_1_i3_hashes_bound"}, "payload.phase8")
    require(
        phase8["status"] == "PASS" and phase8["final_v4_1_i3_hashes_bound"] is True,
        "Phase-8 final representation gate is not PASS",
    )
    validate_artifact(root, {**phase8["receipt"], "rows": 1}, field="payload.phase8.receipt", rows=1)

    inputs = payload["inputs"]
    exact_keys(
        inputs,
        {"runtime", "source_manifest", "core_conditions", "bridge_conditions",
         "proxy_tokenizer", "representations", "b1_artifacts"},
        "payload.inputs",
    )
    fixed = {
        "runtime": (RUNTIME_REL, EXPECTED_QUERIES),
        "source_manifest": (SOURCE_REL, EXPECTED_SOURCES),
        "core_conditions": (CORE_REL, 36),
        "bridge_conditions": (BRIDGE_REL, 6),
    }
    for name, (rel_path, rows) in fixed.items():
        item = inputs[name]
        expected_item = {
            "path": rel_path.as_posix(),
            "sha256": FIXED_INPUT_SHA256[rel_path],
            "rows": rows,
        }
        require(item == expected_item, f"Fixed payload input drift: {name}")
        validate_artifact(root, item, field=f"payload.inputs.{name}", rows=rows)
    exact_keys(
        inputs["proxy_tokenizer"],
        {"repository", "revision", "path", "tokenizer_json_sha256"},
        "payload.inputs.proxy_tokenizer",
    )
    require(inputs["proxy_tokenizer"] == PROXY_TOKENIZER, "Proxy-tokenizer binding drift")
    tokenizer_path = root_path(root, PROXY_TOKENIZER["path"], field="proxy_tokenizer.path")
    tokenizer_json = tokenizer_path / "tokenizer.json"
    require(tokenizer_json.is_file(), "Pinned proxy tokenizer is absent")
    require(
        file_sha256(tokenizer_json) == PROXY_TOKENIZER["tokenizer_json_sha256"],
        "Pinned proxy tokenizer hash drift",
    )

    representations = inputs["representations"]
    exact_keys(representations, set(REPRESENTATIONS), "payload.inputs.representations")
    for representation, item in representations.items():
        exact_keys(
            item,
            {"path", "sha256", "rows", "phase8_final", "extraction_protocol"},
            f"representations.{representation}",
        )
        require(
            item["rows"] == EXPECTED_SOURCES and item["phase8_final"] is True,
            f"{representation}: final Phase-8 binding missing",
        )
        if representation in FIXED_REPRESENTATION_INPUTS:
            frozen = FIXED_REPRESENTATION_INPUTS[representation]
            require(
                item["path"] == frozen["path"] and item["sha256"] == frozen["sha256"],
                f"{representation}: authoritative V2 I1/I2 binding drift",
            )
            require(
                item["extraction_protocol"] == "SOURCE_NATIVE_PHASE7_V2",
                f"{representation}: extraction protocol drift",
            )
        else:
            require(
                item["extraction_protocol"] == "I3C_SUBAGENT_EXTRACTION_V4_1",
                f"{representation}: final V4.1 protocol missing",
            )
        validate_artifact(
            root,
            {"path": item["path"], "sha256": item["sha256"], "rows": item["rows"]},
            field=f"representations.{representation}",
            rows=EXPECTED_SOURCES,
        )

    artifacts = inputs["b1_artifacts"]
    require(isinstance(artifacts, list) and artifacts, "Persisted B1 artifacts are required")
    for index, artifact in enumerate(artifacts):
        validate_artifact(root, artifact, field=f"payload.inputs.b1_artifacts[{index}]")
    b1_validation = payload["b1_validation"]
    exact_keys(b1_validation, {"status", "receipt", "condition_ids", "rows"}, "payload.b1_validation")
    require(
        b1_validation["status"] == "PASS_12_PERSISTED_B1_CELLS",
        "Persisted B1 validation is not PASS",
    )
    require(
        b1_validation["condition_ids"] == list(B1_CONDITIONS)
        and b1_validation["rows"] == EXPECTED_B1_ROWS,
        "Persisted B1 validation scope drift",
    )
    receipt_path = validate_artifact(
        root,
        {**b1_validation["receipt"], "rows": 1},
        field="payload.b1_validation.receipt",
        rows=1,
    )
    receipt = read_json(receipt_path)
    validate_b1_validation_receipt(receipt)
    require(
        receipt.get("b1_cells") == 12 and receipt.get("b1_rows") == EXPECTED_B1_ROWS,
        "Official B1 validation receipt coverage drift",
    )
    require(
        payload["counts"] == {
            "queries": EXPECTED_QUERIES,
            "sources": EXPECTED_SOURCES,
            "persisted_b1_cells": 12,
            "persisted_b1_rows": EXPECTED_B1_ROWS,
            "materialised_b2_conditions": 15,
            "materialised_b2_rows": EXPECTED_B2_ROWS,
            "c2_q_alias_rows": 0,
        },
        "Payload count contract drift",
    )
    require(payload["method"] == method_contract(), "Payload method contract drift")
    require(
        payload["label_isolation"] == {
            "labels_or_results_read": False,
            "b1_candidates_regenerated": False,
            "offline_scorer_run": False,
        },
        "Payload label-isolation contract drift",
    )
    reject_outcome_keys(payload, "payload")
    return payload


def validate_b1_validation_receipt(receipt: dict[str, Any]) -> None:
    require(
        receipt.get("schema_version") == B1_VALIDATION_RECEIPT_SCHEMA
        and receipt.get("status") == "PASS_FRESH_OFFICIAL_LABEL_FREE_B1_VALIDATION"
        and receipt.get("official_report", {}).get("status") == "PASS_LABEL_FREE_RUNNER_OUTPUT_VALIDATION",
        "Official B1 validation receipt status drift",
    )


def validate_root_release(
    root: Path, authorisation_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        authorisation_path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Root release must be inside repository root") from error
    require(authorisation_path.is_file(), "Root-release authorisation is missing")
    release = read_json(authorisation_path)
    exact_keys(
        release,
        {"schema_version", "state", "root_release_id", "run_id", "attempt_id",
         "payload", "phase8", "b1_validation_receipt_sha256", "approval", "provider",
         "preflight", "destinations", "ceilings"},
        "root_release",
    )
    require(release["schema_version"] == AUTHORISATION_SCHEMA, "Root-release schema drift")
    require(
        release["state"] == "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_B1_BOUND_EXECUTION",
        "Scientific B2 execution is not root-released",
    )
    for name in ("root_release_id", "run_id", "attempt_id"):
        require(isinstance(release[name], str) and release[name], f"Root-release {name} missing")
    exact_keys(release["payload"], {"path", "sha256"}, "root_release.payload")
    payload_path = root_path(root, release["payload"]["path"], field="root_release.payload.path")
    require(
        payload_path.is_file() and file_sha256(payload_path) == release["payload"]["sha256"],
        "Root-release payload hash drift",
    )
    payload = validate_payload(root, payload_path)
    require(
        release["phase8"]
        == {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]},
        "Root-release Phase-8 binding drift",
    )
    require(
        release["b1_validation_receipt_sha256"]
        == payload["b1_validation"]["receipt"]["sha256"],
        "Root-release B1-validation binding drift",
    )
    approval_binding = release["approval"]
    exact_keys(approval_binding, {"path", "sha256", "decision", "scope"}, "root_release.approval")
    approval_path = root_path(root, approval_binding["path"], field="root_release.approval.path")
    require(approval_path.is_file() and file_sha256(approval_path) == approval_binding["sha256"], "Execution approval hash drift")
    approval = read_json(approval_path)
    require(approval.get("schema_version") == EXECUTION_APPROVAL_SCHEMA and approval.get("decision") == "APPROVED", "Execution approval is not a valid B2 approval")
    require(approval_binding["decision"] == approval["decision"] and approval_binding["scope"] == approval.get("scope"), "Execution approval binding drift")
    scope = approval_binding["scope"]
    require(scope.get("frozen_library") == "V7_3798_SOURCES_1077_QUERIES" and scope.get("experiment") == "B36_CORE_PLUS_C6_DIAGNOSTIC", "Execution approval experiment scope drift")
    require(scope.get("phase8_b2_prerequisite") is True and scope.get("external_qwen_reranker") is True, "Execution approval does not cover Qwen B2")
    require(approval.get("secrets_recorded") is False, "Execution approval must not contain secrets")
    require(
        release["provider"] == {
            "endpoint": ENDPOINT,
            "model": MODEL,
            "api_key_env": API_KEY_ENV,
            "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
            "automatic_retries": 0,
        },
        "Provider endpoint/model/timeout/retry contract drift",
    )
    exact_keys(release["destinations"], {"output_dir", "attempt_dir"}, "root_release.destinations")
    destinations = {
        name: root_path(root, value, field=f"root_release.destinations.{name}")
        for name, value in release["destinations"].items()
    }
    require(
        len(set(destinations.values())) == 2,
        "Output and attempt destinations must be distinct",
    )
    for name, path in destinations.items():
        require(
            relative(path, root).startswith("skill_benchmark/cache/"),
            f"{name}: destination must be under skill_benchmark/cache",
        )
        require(not path.exists(), f"{name}: destination already exists; overwrite forbidden")
    exact_keys(release["ceilings"], CEILING_KEYS, "root_release.ceilings")
    for name in CEILING_KEYS - {"maximum_wall_time_seconds"}:
        value = release["ceilings"][name]
        require(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0,
            f"Invalid ceiling: {name}",
        )
    wall = release["ceilings"]["maximum_wall_time_seconds"]
    require(
        isinstance(wall, (int, float)) and not isinstance(wall, bool)
        and math.isfinite(float(wall)) and wall > 0,
        "Invalid maximum_wall_time_seconds",
    )
    preflight = release["preflight"]
    exact_keys(preflight, {"pending_release", "receipt"}, "root_release.preflight")
    pending_path = validate_file_binding(root, preflight["pending_release"], field="root_release.preflight.pending_release")
    pending = read_json(pending_path)
    exact_keys(
        pending,
        {"schema_version", "state", "payload", "provider", "planned_destinations", "ceilings"},
        "pending_release",
    )
    require(pending["schema_version"] == PENDING_RELEASE_SCHEMA, "Pending-release schema drift")
    require(
        pending["state"] == "PENDING_NO_PROVIDER_PREFLIGHT_NOT_EXECUTABLE",
        "Pending-release state is not fail-closed",
    )
    require(pending["payload"] == release["payload"], "Pending-release payload binding drift")
    require(pending["provider"] == release["provider"], "Pending-release provider binding drift")
    require(pending["planned_destinations"] == release["destinations"], "Pending-release destination binding drift")
    require(pending["ceilings"] == release["ceilings"], "Pending-release ceiling binding drift")
    receipt_path = validate_file_binding(root, preflight["receipt"], field="root_release.preflight.receipt")
    receipt = read_json(receipt_path)
    validate_preflight_receipt(
        receipt,
        payload_sha256=file_sha256(payload_path),
        pending_release_sha256=file_sha256(pending_path),
        ceilings=release["ceilings"],
        root=root,
    )
    release["_destinations"] = destinations
    release["_payload_path"] = payload_path
    return release, payload


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


def reranker_input_sha256(
    *, condition_id: str, prompt_id: str, prompt_sha256: str,
    input_top20_binding_sha256: str, input_candidates: list[dict[str, Any]],
) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-reranker-input-binding-v1",
        "condition_id": condition_id,
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_sha256,
        "input_top20_binding_sha256": input_top20_binding_sha256,
        "input_candidates": input_candidates,
    })


def load_official_validator(root: Path) -> Any:
    scripts = str((root / "skill_benchmark/scripts").resolve())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import validate_rq2b_v7_runner_outputs as validator
    return validator


def load_authority(
    root: Path, payload: dict[str, Any]
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, dict[str, Any]]],
    dict[tuple[str, str], dict[str, Any]],
    Any,
]:
    validator = load_official_validator(root)
    official = validator.RunnerAuthority.load()
    inputs = payload["inputs"]
    prompts = read_jsonl_any(root_path(root, inputs["runtime"]["path"], field="runtime.path"))
    require(len(prompts) == EXPECTED_QUERIES, "Runtime query count drift")
    for index, row in enumerate(prompts):
        reject_outcome_keys(row, f"runtime[{index}]")
        exact_keys(row, {"schema_version", "prompt_id", "prompt", "prompt_sha256"}, f"runtime[{index}]")
        require(
            row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1"
            and row["prompt_sha256"] == text_sha256(row["prompt"]),
            f"runtime[{index}]: schema/hash drift",
        )
    require(
        {row["prompt_id"] for row in prompts} == set(official.prompts),
        "Runtime prompt identities drift from official authority",
    )

    core = read_jsonl_any(root_path(root, inputs["core_conditions"]["path"], field="core.path"))
    bridge = read_jsonl_any(root_path(root, inputs["bridge_conditions"]["path"], field="bridge.path"))
    all_conditions = {row["condition_id"]: row for row in [*core, *bridge]}
    conditions: dict[str, dict[str, Any]] = {}
    for condition_id in MATERIALISED_CONDITIONS:
        condition = all_conditions.get(condition_id)
        require(condition is not None, f"Missing materialised condition: {condition_id}")
        reject_outcome_keys(condition, f"condition.{condition_id}")
        require(condition["reranker"] == "Qwen-qwen3-rerank", f"{condition_id}: reranker drift")
        require(condition["source_union_sha256"] == SOURCE_UNION_SHA256, f"{condition_id}: source union drift")
        require(condition["prompt_manifest_sha256"] == PROMPT_MANIFEST_SHA256, f"{condition_id}: prompt manifest drift")
        require(condition["runtime_rerank_k"] == TOP_K, f"{condition_id}: rerank-k drift")
        require(condition["query_count"] == EXPECTED_QUERIES, f"{condition_id}: query count drift")
        require(condition["execution_authorised"] is False, f"{condition_id}: manifest unexpectedly authorises execution")
        require(condition_id in official.b2_conditions, f"{condition_id}: absent from official authority")
        conditions[condition_id] = condition
    require("C2-Q" not in all_conditions, "C2-Q must remain an alias and not be materialised")

    views: dict[str, dict[str, dict[str, Any]]] = {}
    for representation, artifact in inputs["representations"].items():
        rows = read_jsonl_any(root_path(root, artifact["path"], field=f"representations.{representation}.path"))
        indexed: dict[str, dict[str, Any]] = {}
        for index, row in enumerate(rows):
            reject_outcome_keys(row, f"representations.{representation}[{index}]")
            source = row.get("source_sha256")
            selector_text = row.get("selector_text")
            require(source in official.sources and source not in indexed, f"{representation}: source identity/duplicate drift")
            require(row.get("representation") == representation, f"{representation}: row tag drift")
            require(
                isinstance(selector_text, str) and bool(selector_text)
                and row.get("selector_text_sha256") == text_sha256(selector_text),
                f"{representation}: selector-text bytes/hash drift",
            )
            indexed[str(source)] = row
        require(
            len(indexed) == EXPECTED_SOURCES and set(indexed) == official.sources,
            f"{representation}: source coverage drift",
        )
        views[representation] = indexed

    b1_rows: list[dict[str, Any]] = []
    for index, artifact in enumerate(inputs["b1_artifacts"]):
        artifact_path = root_path(root, artifact["path"], field=f"b1_artifacts[{index}].path")
        rows = read_jsonl_any(artifact_path)
        require(len(rows) == artifact["rows"], f"B1 artifact row count drift: {artifact_path}")
        b1_rows.extend(rows)
    b1_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for row_number, row in enumerate(b1_rows, 1):
        reject_outcome_keys(row, f"B1[{row_number}]")
        validator.validate_b1_row(row, official, row_number)
        key = (row["condition_id"], row["prompt_id"])
        require(key not in b1_by_key, f"Duplicate B1 row: {key}")
        b1_by_key[key] = row
    expected_keys = {
        (condition_id, prompt["prompt_id"])
        for condition_id in B1_CONDITIONS
        for prompt in prompts
    }
    require(set(b1_by_key) == expected_keys, "Persisted B1 coverage is not exact 12 x 1,077")
    return prompts, conditions, views, b1_by_key, official


def b1_condition_id(condition: dict[str, Any]) -> str:
    source = condition["persisted_candidate_source"]
    require(
        isinstance(source, str) and len(source) == 3 and source.startswith("B"),
        f"{condition['condition_id']}: invalid persisted candidate source",
    )
    value = f"{source}-G0"
    require(value in B1_CONDITIONS, f"{condition['condition_id']}: unknown B1 source")
    return value


def load_proxy_tokenizer(root: Path) -> Any:
    from transformers import AutoTokenizer

    path = root_path(root, PROXY_TOKENIZER["path"], field="proxy_tokenizer.path")
    tokenizer = AutoTokenizer.from_pretrained(
        path,
        local_files_only=True,
        trust_remote_code=False,
    )
    return tokenizer


def source_windows(
    tokenizer: Any, source_sha256: str, selector_text: str,
    *, chunker: Callable[..., list[Any]] = exact_text_chunks,
) -> list[dict[str, Any]]:
    chunks = chunker(
        tokenizer,
        selector_text,
        maximum_tokens=WINDOW_PROXY_TOKENS,
        overlap_tokens=WINDOW_OVERLAP_PROXY_TOKENS,
    )
    return [
        {
            "skill_id": source_sha256,
            "window_index": chunk.chunk_index,
            "text": chunk.text,
            "text_sha256": chunk.text_sha256,
            "proxy_tokens": chunk.token_count,
        }
        for chunk in chunks
    ]


def build_condition_work(
    tokenizer: Any,
    condition: dict[str, Any],
    prompt: dict[str, Any],
    b1_row: dict[str, Any],
    representation_rows: dict[str, dict[str, Any]],
    *,
    chunker: Callable[..., list[Any]] = exact_text_chunks,
    window_cache: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    candidate_sources = [row["source_sha256"] for row in b1_row["ranked_candidates"][:TOP_K]]
    require(len(candidate_sources) == TOP_K and len(set(candidate_sources)) == TOP_K, "B1 Top-20 identity drift")
    input_candidates = [
        {
            "input_rank": rank,
            "source_sha256": source,
            "candidate_view_sha256": representation_rows[source]["selector_text_sha256"],
        }
        for rank, source in enumerate(candidate_sources, 1)
    ]
    windows: list[dict[str, Any]] = []
    for source in candidate_sources:
        cached = window_cache.get(source) if window_cache is not None else None
        if cached is None:
            cached = source_windows(
                tokenizer,
                source,
                representation_rows[source]["selector_text"],
                chunker=chunker,
            )
            if window_cache is not None:
                window_cache[source] = cached
        windows.extend(cached)
    b1_adapter = {
        "retriever": b1_row["retriever"],
        "representation": condition["representation"],
        "prompt_id": b1_row["prompt_id"],
        "prompt_sha256": b1_row["prompt_sha256"],
        "top_20_skill_ids": candidate_sources,
    }
    trusted = trusted_binding_from_sources(
        condition_id=condition["condition_id"],
        prompt=prompt,
        b1_row=b1_adapter,
        candidate_windows=windows,
    )
    qwen_condition = {
        "schema_version": "rq2b-qwen-reranker-condition-payload-v1",
        "condition_id": condition["condition_id"],
        "first_stage_retriever": condition["retriever"],
        "representation": condition["representation"],
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "query": prompt["prompt"],
        "query_sha256": text_sha256(prompt["prompt"]),
        "candidate_skill_ids": candidate_sources,
        "candidate_list_sha256": canonical_sha256(candidate_sources),
        "candidate_windows": windows,
    }
    validate_condition(qwen_condition, trusted)
    batches = build_request_batches(qwen_condition, trusted)
    return {
        "condition": qwen_condition,
        "trusted_binding": trusted,
        "batches": batches,
        "input_candidates": input_candidates,
        "input_top20_binding_sha256": b1_row["top20_binding_sha256"],
    }


def workload_signature(work: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_windows": work["trusted_binding"]["candidate_windows"],
        "requests": [
            {
                "batch_index": batch["batch_index"],
                "request_proxy_tokens": batch["request_proxy_tokens"],
                "request_utf8_bytes": request_utf8_bytes(batch["payload"]),
                "entries": [
                    {
                        "skill_id": entry["window"]["skill_id"],
                        "window_index": entry["window"]["window_index"],
                        "text_sha256": entry["window"]["text_sha256"],
                        "proxy_tokens": entry["window"]["proxy_tokens"],
                        "is_anchor_duplicate": entry["is_anchor_duplicate"],
                    }
                    for entry in batch["entries"]
                ],
            }
            for batch in work["batches"]
        ],
    }


def empty_workload_counts() -> dict[str, int]:
    return {
        "rows": 0,
        "requests": 0,
        "documents": 0,
        "proxy_tokens": 0,
        "utf8_bytes": 0,
        "candidate_windows": 0,
        "duplicate_anchor_documents": 0,
        "split_rows": 0,
        "maximum_documents_in_one_request": 0,
        "maximum_proxy_tokens_in_one_request": 0,
        "maximum_utf8_bytes_in_one_request": 0,
    }


def add_workload_counts(counts: dict[str, int], work: dict[str, Any]) -> None:
    counts["rows"] += 1
    counts["candidate_windows"] += len(work["condition"]["candidate_windows"])
    if len(work["batches"]) > 1:
        counts["split_rows"] += 1
    for batch in work["batches"]:
        documents = len(batch["entries"])
        utf8_bytes = request_utf8_bytes(batch["payload"])
        counts["requests"] += 1
        counts["documents"] += documents
        counts["proxy_tokens"] += batch["request_proxy_tokens"]
        counts["utf8_bytes"] += utf8_bytes
        counts["duplicate_anchor_documents"] += batch["anchor_duplicate_window_count"]
        counts["maximum_documents_in_one_request"] = max(
            counts["maximum_documents_in_one_request"], documents
        )
        counts["maximum_proxy_tokens_in_one_request"] = max(
            counts["maximum_proxy_tokens_in_one_request"], batch["request_proxy_tokens"]
        )
        counts["maximum_utf8_bytes_in_one_request"] = max(
            counts["maximum_utf8_bytes_in_one_request"], utf8_bytes
        )


def ceiling_headroom(
    counts: dict[str, int], ceilings: dict[str, Any], *, preflight_seconds: float,
) -> dict[str, dict[str, Any]]:
    required = {
        "maximum_request_attempts": counts["requests"],
        "maximum_successful_calls": counts["requests"],
        "maximum_external_documents": counts["documents"],
        "maximum_external_submission_proxy_tokens": counts["proxy_tokens"],
        "maximum_external_submission_utf8_bytes": counts["utf8_bytes"],
    }
    output: dict[str, dict[str, Any]] = {}
    for key, value in required.items():
        output[key] = {
            "required": value,
            "authorised": ceilings[key],
            "headroom": ceilings[key] - value,
            "sufficient": value <= ceilings[key],
            "predictability": "EXACT_BEFORE_PROVIDER_EXECUTION",
        }
    output["maximum_provider_total_tokens"] = {
        "required": None,
        "observed_before_execution": 0,
        "authorised": ceilings["maximum_provider_total_tokens"],
        "headroom_before_execution": ceilings["maximum_provider_total_tokens"],
        "sufficient": None,
        "predictability": "PROVIDER_RESPONSE_ONLY_RUNTIME_FAIL_CLOSED",
    }
    output["maximum_wall_time_seconds"] = {
        "required": None,
        "preflight_observed_seconds": preflight_seconds,
        "authorised": ceilings["maximum_wall_time_seconds"],
        "headroom_at_execution_start": ceilings["maximum_wall_time_seconds"],
        "sufficient": None,
        "predictability": "RUNTIME_ONLY_FAIL_CLOSED_BEFORE_EACH_REQUEST_AND_PUBLICATION",
    }
    return output


def validate_pending_release(root: Path, path: Path) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Pending release must be inside repository root") from error
    require(path.is_file(), "Pending-release input is missing")
    pending = read_json(path)
    exact_keys(
        pending,
        {"schema_version", "state", "payload", "provider", "planned_destinations", "ceilings"},
        "pending_release",
    )
    require(pending["schema_version"] == PENDING_RELEASE_SCHEMA, "Pending-release schema drift")
    require(
        pending["state"] == "PENDING_NO_PROVIDER_PREFLIGHT_NOT_EXECUTABLE",
        "Pending release must remain non-executable",
    )
    exact_keys(pending["payload"], {"path", "sha256"}, "pending_release.payload")
    payload_path = root_path(root, pending["payload"]["path"], field="pending_release.payload.path")
    require(
        payload_path.is_file() and file_sha256(payload_path) == pending["payload"]["sha256"],
        "Pending-release payload hash drift",
    )
    payload = validate_payload(root, payload_path)
    require(
        pending["provider"] == {
            "endpoint": ENDPOINT,
            "model": MODEL,
            "api_key_env": API_KEY_ENV,
            "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
            "automatic_retries": 0,
        },
        "Pending-release provider contract drift",
    )
    exact_keys(pending["planned_destinations"], {"output_dir", "attempt_dir"}, "pending_release.planned_destinations")
    for name, value in pending["planned_destinations"].items():
        planned = root_path(root, value, field=f"pending_release.planned_destinations.{name}")
        require(relative(planned, root).startswith("skill_benchmark/cache/"), f"{name}: planned destination outside cache")
        require(not planned.exists(), f"{name}: planned destination already exists")
    require(
        len(set(pending["planned_destinations"].values())) == 2,
        "Pending output and attempt destinations must be distinct",
    )
    exact_keys(pending["ceilings"], CEILING_KEYS, "pending_release.ceilings")
    for key in CEILING_KEYS - {"maximum_wall_time_seconds"}:
        value = pending["ceilings"][key]
        require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"Invalid ceiling: {key}")
    wall = pending["ceilings"]["maximum_wall_time_seconds"]
    require(isinstance(wall, (int, float)) and not isinstance(wall, bool) and wall > 0, "Invalid wall-time ceiling")
    return pending, payload_path, payload


def validate_preflight_receipt(
    receipt: dict[str, Any], *, payload_sha256: str, pending_release_sha256: str,
    ceilings: dict[str, Any], root: Path,
) -> None:
    exact_keys(
        receipt,
        {"schema_version", "status", "runner_version", "payload_sha256",
         "pending_release_sha256", "implementation", "proxy_tokenizer", "method_sha256",
         "scope", "counts", "chunker_parity", "ceilings", "ceiling_headroom",
         "all_pre_execution_predictable_ceilings_sufficient", "provider_calls",
         "network_calls", "preflight_wall_time_seconds", "completed_at_utc"},
        "preflight_receipt",
    )
    require(receipt["schema_version"] == PREFLIGHT_SCHEMA, "Preflight receipt schema drift")
    require(receipt["status"] == "PASS_EXACT_NO_PROVIDER_PREFLIGHT", "Preflight receipt is not PASS")
    require(receipt["runner_version"] == RUNNER_VERSION, "Preflight runner version drift")
    require(receipt["payload_sha256"] == payload_sha256, "Preflight payload binding is stale")
    require(receipt["pending_release_sha256"] == pending_release_sha256, "Preflight pending-release binding is stale")
    require(
        receipt["implementation"] == {
            "runner_sha256": file_sha256(Path(__file__).resolve()),
            "qwen_contract_helper_sha256": file_sha256(root / HELPER_REL),
            "exact_chunker_v1_sha256": file_sha256(root / CHUNKER_V1_REL),
            "exact_chunker_v2_sha256": file_sha256(root / CHUNKER_V2_REL),
            "official_output_validator_sha256": file_sha256(root / VALIDATOR_REL),
        },
        "Preflight implementation binding is stale",
    )
    require(receipt["proxy_tokenizer"] == PROXY_TOKENIZER, "Preflight proxy-tokenizer binding drift")
    require(receipt["method_sha256"] == canonical_sha256(method_contract()), "Preflight method binding drift")
    require(receipt["scope"] == {
        "conditions": list(MATERIALISED_CONDITIONS),
        "condition_count": 15,
        "queries": EXPECTED_QUERIES,
        "rows": EXPECTED_B2_ROWS,
        "candidate_pairs_per_row": TOP_K,
        "c2_q_alias_rows": 0,
    }, "Preflight scope drift")
    exact_keys(receipt["counts"], set(empty_workload_counts()), "preflight_receipt.counts")
    require(receipt["counts"]["rows"] == EXPECTED_B2_ROWS, "Preflight row-count drift")
    parity = receipt["chunker_parity"]
    exact_keys(
        parity,
        {"status", "v1", "v2", "compared_rows", "different_rows",
         "same_window_boundaries", "same_request_partitioning",
         "differences_sha256", "difference_samples", "decision"},
        "preflight_receipt.chunker_parity",
    )
    for name, rel_path, version in (
        ("v1", CHUNKER_V1_REL, CHUNKER_V1_VERSION),
        ("v2", CHUNKER_V2_REL, CHUNKER_V2_VERSION),
    ):
        binding = parity[name]
        exact_keys(binding, {"version", "path", "sha256", "counts_sha256"}, f"chunker_parity.{name}")
        require(
            binding["version"] == version
            and binding["path"] == rel_path.as_posix()
            and binding["sha256"] == file_sha256(root / rel_path),
            f"Preflight {name} chunker binding drift",
        )
    require(
        parity["status"] == "PASS_EXACT_V1_V2_PARITY"
        and parity["different_rows"] == 0
        and parity["compared_rows"] == EXPECTED_B2_ROWS
        and parity["same_window_boundaries"] is True
        and parity["same_request_partitioning"] is True,
        "Preflight v1/v2 chunker parity is not PASS",
    )
    require(
        parity["v1"]["counts_sha256"] == canonical_sha256(receipt["counts"])
        and parity["v2"]["counts_sha256"] == canonical_sha256(receipt["counts"])
        and parity["differences_sha256"] == canonical_sha256([])
        and parity["difference_samples"] == []
        and parity["decision"] == "V1_FROZEN_METHOD_SAFE_TO_EXECUTE",
        "Preflight v1/v2 parity audit details drift",
    )
    require(receipt["ceilings"] == ceilings, "Preflight ceiling binding drift")
    exact_keys(receipt["ceiling_headroom"], CEILING_KEYS, "preflight_receipt.ceiling_headroom")
    require(receipt["provider_calls"] == 0 and receipt["network_calls"] == 0, "Preflight performed provider/network work")
    require(receipt["all_pre_execution_predictable_ceilings_sufficient"] is True, "Preflight predictable ceilings are insufficient")
    for key in (
        "maximum_request_attempts", "maximum_successful_calls", "maximum_external_documents",
        "maximum_external_submission_proxy_tokens", "maximum_external_submission_utf8_bytes",
    ):
        item = receipt["ceiling_headroom"][key]
        require(item["headroom"] >= 0 and item["sufficient"] is True, f"Preflight insufficient ceiling: {key}")


def run_preflight(root: Path, pending_release_path: Path, receipt_path: Path) -> dict[str, Any]:
    root = root.resolve()
    try:
        receipt_path.resolve().relative_to(root)
    except ValueError as error:
        raise ValueError("Preflight receipt must be inside repository root") from error
    require(not receipt_path.exists(), "Preflight receipt overwrite forbidden")
    require(relative(receipt_path, root).startswith("skill_benchmark/cache/"), "Preflight receipt must be under cache")
    started = time.monotonic()
    pending, payload_path, payload = validate_pending_release(root, pending_release_path.resolve())
    prompts, conditions, views, b1_by_key, _official = load_authority(root, payload)
    tokenizer = load_proxy_tokenizer(root)
    counts = empty_workload_counts()
    v2_counts = empty_workload_counts()
    v1_window_caches: dict[str, dict[str, list[dict[str, Any]]]] = {
        representation: {} for representation in REPRESENTATIONS
    }
    v2_window_caches: dict[str, dict[str, list[dict[str, Any]]]] = {
        representation: {} for representation in REPRESENTATIONS
    }
    parity_differences: list[dict[str, Any]] = []
    same_window_boundaries = True
    same_request_partitioning = True
    for condition_id in MATERIALISED_CONDITIONS:
        condition = conditions[condition_id]
        representation_rows = views[condition["representation"]]
        source_b1_condition = b1_condition_id(condition)
        for prompt in prompts:
            work = build_condition_work(
                tokenizer,
                condition,
                prompt,
                b1_by_key[(source_b1_condition, prompt["prompt_id"])],
                representation_rows,
                window_cache=v1_window_caches[condition["representation"]],
            )
            v2_work = build_condition_work(
                tokenizer,
                condition,
                prompt,
                b1_by_key[(source_b1_condition, prompt["prompt_id"])],
                representation_rows,
                chunker=exact_text_chunks_v2,
                window_cache=v2_window_caches[condition["representation"]],
            )
            add_workload_counts(counts, work)
            add_workload_counts(v2_counts, v2_work)
            v1_signature = workload_signature(work)
            v2_signature = workload_signature(v2_work)
            windows_equal = v1_signature["candidate_windows"] == v2_signature["candidate_windows"]
            requests_equal = v1_signature["requests"] == v2_signature["requests"]
            same_window_boundaries = same_window_boundaries and windows_equal
            same_request_partitioning = same_request_partitioning and requests_equal
            if not (windows_equal and requests_equal):
                parity_differences.append({
                    "condition_id": condition_id,
                    "prompt_id": prompt["prompt_id"],
                    "representation": condition["representation"],
                    "window_boundaries_equal": windows_equal,
                    "request_partitioning_equal": requests_equal,
                    "v1_signature_sha256": canonical_sha256(v1_signature),
                    "v2_signature_sha256": canonical_sha256(v2_signature),
                    "v1_candidate_windows": len(work["condition"]["candidate_windows"]),
                    "v2_candidate_windows": len(v2_work["condition"]["candidate_windows"]),
                    "v1_requests": len(work["batches"]),
                    "v2_requests": len(v2_work["batches"]),
                })
    elapsed = time.monotonic() - started
    headroom = ceiling_headroom(counts, pending["ceilings"], preflight_seconds=elapsed)
    predictable_sufficient = all(
        headroom[key]["sufficient"] is True
        for key in (
            "maximum_request_attempts", "maximum_successful_calls", "maximum_external_documents",
            "maximum_external_submission_proxy_tokens", "maximum_external_submission_utf8_bytes",
        )
    )
    parity_pass = not parity_differences
    if not parity_pass:
        status = "FAIL_METHOD_PARITY_REVIEW_REQUIRED"
    elif not predictable_sufficient:
        status = "FAIL_INSUFFICIENT_PREDICTABLE_CEILING"
    else:
        status = "PASS_EXACT_NO_PROVIDER_PREFLIGHT"
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "status": status,
        "runner_version": RUNNER_VERSION,
        "payload_sha256": file_sha256(payload_path),
        "pending_release_sha256": file_sha256(pending_release_path),
        "implementation": {
            "runner_sha256": file_sha256(Path(__file__).resolve()),
            "qwen_contract_helper_sha256": file_sha256(root / HELPER_REL),
            "exact_chunker_v1_sha256": file_sha256(root / CHUNKER_V1_REL),
            "exact_chunker_v2_sha256": file_sha256(root / CHUNKER_V2_REL),
            "official_output_validator_sha256": file_sha256(root / VALIDATOR_REL),
        },
        "proxy_tokenizer": PROXY_TOKENIZER,
        "method_sha256": canonical_sha256(method_contract()),
        "scope": {
            "conditions": list(MATERIALISED_CONDITIONS),
            "condition_count": 15,
            "queries": EXPECTED_QUERIES,
            "rows": EXPECTED_B2_ROWS,
            "candidate_pairs_per_row": TOP_K,
            "c2_q_alias_rows": 0,
        },
        "counts": counts,
        "chunker_parity": {
            "status": "PASS_EXACT_V1_V2_PARITY" if parity_pass else "FAIL_METHOD_DOCKET_REQUIRED",
            "v1": {
                "version": CHUNKER_V1_VERSION,
                "path": CHUNKER_V1_REL.as_posix(),
                "sha256": file_sha256(root / CHUNKER_V1_REL),
                "counts_sha256": canonical_sha256(counts),
            },
            "v2": {
                "version": CHUNKER_V2_VERSION,
                "path": CHUNKER_V2_REL.as_posix(),
                "sha256": file_sha256(root / CHUNKER_V2_REL),
                "counts_sha256": canonical_sha256(v2_counts),
            },
            "compared_rows": counts["rows"],
            "different_rows": len(parity_differences),
            "same_window_boundaries": same_window_boundaries,
            "same_request_partitioning": same_request_partitioning,
            "differences_sha256": canonical_sha256(parity_differences),
            "difference_samples": parity_differences[:25],
            "decision": (
                "V1_FROZEN_METHOD_SAFE_TO_EXECUTE"
                if parity_pass
                else "FAIL_CLOSED_DO_NOT_EXECUTE_OPEN_METHOD_DOCKET_NO_AUTOMATIC_CHUNKER_SWAP"
            ),
        },
        "ceilings": pending["ceilings"],
        "ceiling_headroom": headroom,
        "all_pre_execution_predictable_ceilings_sufficient": predictable_sufficient,
        "provider_calls": 0,
        "network_calls": 0,
        "preflight_wall_time_seconds": elapsed,
        "completed_at_utc": utc_now(),
    }
    if status != "PASS_EXACT_NO_PROVIDER_PREFLIGHT":
        write_json_new(receipt_path, receipt)
        raise ValueError(
            "No-provider preflight failed closed; preserved receipt contains exact ceiling/parity method docket"
        )
    validate_preflight_receipt(
        receipt,
        payload_sha256=file_sha256(payload_path),
        pending_release_sha256=file_sha256(pending_release_path),
        ceilings=pending["ceilings"],
        root=root,
    )
    write_json_new(receipt_path, receipt)
    return receipt


class ProviderRequestError(RuntimeError):
    def __init__(self, message: str, *, timed_out: bool, status_code: int | None = None) -> None:
        super().__init__(message)
        self.timed_out = timed_out
        self.status_code = status_code


def request_once(payload: dict[str, Any], api_key: str, timeout_seconds: int) -> dict[str, Any]:
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=encoded,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        body = error.read(4096).decode("utf-8", errors="replace")
        raise ProviderRequestError(
            f"DashScope HTTP {error.code}: {body}",
            timed_out=False,
            status_code=error.code,
        ) from error
    except (urllib.error.URLError, TimeoutError, socket.timeout) as error:
        reason = getattr(error, "reason", error)
        timed_out = isinstance(reason, (TimeoutError, socket.timeout)) or "timed out" in str(reason).lower()
        raise ProviderRequestError(
            f"DashScope transport failure: {reason}",
            timed_out=timed_out,
        ) from error
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProviderRequestError("DashScope returned non-JSON response bytes", timed_out=False) from error
    require(isinstance(value, dict), "DashScope response must be a JSON object")
    return value


def parse_provider_usage(response: dict[str, Any]) -> dict[str, int]:
    usage = response.get("usage")
    if usage is None:
        return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    require(isinstance(usage, dict), "DashScope usage must be an object when present")

    def token_value(*names: str) -> int | None:
        for name in names:
            if name in usage:
                value = usage[name]
                require(
                    isinstance(value, int) and not isinstance(value, bool) and value >= 0,
                    f"DashScope usage.{name} must be a non-negative integer",
                )
                return value
        return None

    total = token_value("total_tokens")
    input_tokens = token_value("input_tokens", "prompt_tokens")
    output_tokens = token_value("output_tokens", "completion_tokens")
    if total is None:
        total = (input_tokens or 0) + (output_tokens or 0)
    if input_tokens is None:
        input_tokens = total
    if output_tokens is None:
        output_tokens = max(0, total - input_tokens)
    require(input_tokens + output_tokens <= total, "DashScope usage token fields are inconsistent")
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total,
    }


def request_utf8_bytes(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def empty_ledger() -> dict[str, int]:
    return {
        "request_attempts": 0,
        "successful_calls": 0,
        "external_documents": 0,
        "external_submission_proxy_tokens": 0,
        "external_submission_utf8_bytes": 0,
        "provider_reported_input_tokens": 0,
        "provider_reported_output_tokens": 0,
        "provider_reported_total_tokens": 0,
        "timeouts": 0,
        "failures": 0,
    }


def enforce_next_request_ceilings(
    ledger: dict[str, int], batch: dict[str, Any], ceilings: dict[str, Any],
    *, started_at: float,
) -> None:
    proposed = {
        "maximum_request_attempts": ledger["request_attempts"] + 1,
        "maximum_successful_calls": ledger["successful_calls"] + 1,
        "maximum_external_documents": ledger["external_documents"] + len(batch["entries"]),
        "maximum_external_submission_proxy_tokens": (
            ledger["external_submission_proxy_tokens"] + batch["request_proxy_tokens"]
        ),
        "maximum_external_submission_utf8_bytes": (
            ledger["external_submission_utf8_bytes"] + request_utf8_bytes(batch["payload"])
        ),
    }
    for ceiling_name, value in proposed.items():
        require(value <= ceilings[ceiling_name], f"Root-release ceiling would be exceeded: {ceiling_name}")
    require(
        time.monotonic() - started_at < ceilings["maximum_wall_time_seconds"],
        "Root-release wall-time ceiling reached before next request",
    )


def rank_candidate_scores(
    candidate_sources: list[str],
    windows: list[dict[str, Any]],
    scores_by_window: dict[tuple[str, int, str], float],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    input_rank = {source: rank for rank, source in enumerate(candidate_sources, 1)}
    by_source: dict[str, list[float]] = defaultdict(list)
    for window in windows:
        key = (window["skill_id"], window["window_index"], window["text_sha256"])
        require(key in scores_by_window, f"Missing canonical window score: {key}")
        score = scores_by_window[key]
        require(isinstance(score, (int, float)) and math.isfinite(float(score)), "Non-finite window score")
        by_source[window["skill_id"]].append(float(score))
    require(set(by_source) == set(candidate_sources), "Candidate-score coverage drift")
    ranked = sorted(
        [
            {
                "source_sha256": source,
                "input_rank": input_rank[source],
                "score": max(by_source[source]),
                "mean_window_score": sum(by_source[source]) / len(by_source[source]),
                "window_count": len(by_source[source]),
            }
            for source in candidate_sources
        ],
        key=lambda row: (-row["score"], row["source_sha256"]),
    )
    ties_by_score: dict[float, list[str]] = defaultdict(list)
    for row in ranked:
        ties_by_score[row["score"]].append(row["source_sha256"])
    ties = [
        {"score": score, "source_sha256": sorted(sources)}
        for score, sources in sorted(ties_by_score.items(), key=lambda item: -item[0])
        if len(sources) > 1
    ]
    return ranked, ties


def score_work(
    work: dict[str, Any],
    *,
    request_fn: Callable[[dict[str, Any], str, int], dict[str, Any]],
    api_key: str,
    timeout_seconds: int,
    ceilings: dict[str, Any],
    ledger: dict[str, int],
    attempt_dir: Path,
    request_index: list[dict[str, Any]],
    started_at: float,
    root: Path = ROOT,
) -> tuple[dict[tuple[str, int, str], float], int, dict[str, int]]:
    before = dict(ledger)
    score_batches: list[list[float]] = []
    batches = work["batches"]
    for batch in batches:
        enforce_next_request_ceilings(ledger, batch, ceilings, started_at=started_at)
        serial = ledger["request_attempts"] + 1
        payload = batch["payload"]
        request_bytes = request_utf8_bytes(payload)
        request_sha = canonical_sha256(payload)
        prefix = f"request-{serial:06d}"
        started_path = attempt_dir / f"{prefix}-started.json"
        started_receipt = {
            "schema_version": "rq2b-v7-qwen-reranker-b2-request-start-v1",
            "request_attempt": serial,
            "condition_id": work["condition"]["condition_id"],
            "prompt_id": work["condition"]["prompt_id"],
            "batch_index": batch["batch_index"],
            "endpoint": ENDPOINT,
            "model": MODEL,
            "automatic_retries": 0,
            "timeout_seconds": timeout_seconds,
            "request_sha256": request_sha,
            "query_sha256": work["condition"]["query_sha256"],
            "document_count": len(batch["entries"]),
            "document_text_sha256": [entry["window"]["text_sha256"] for entry in batch["entries"]],
            "request_proxy_tokens": batch["request_proxy_tokens"],
            "request_utf8_bytes": request_bytes,
            "started_at_utc": utc_now(),
        }
        write_json_new(started_path, started_receipt)
        ledger["request_attempts"] += 1
        ledger["external_documents"] += len(batch["entries"])
        ledger["external_submission_proxy_tokens"] += batch["request_proxy_tokens"]
        ledger["external_submission_utf8_bytes"] += request_bytes
        call_started = time.monotonic()
        try:
            response = request_fn(payload, api_key, timeout_seconds)
            scores = parse_response_scores(response, len(batch["entries"]))
            usage = parse_provider_usage(response)
            prospective_total = ledger["provider_reported_total_tokens"] + usage["total_tokens"]
            require(
                prospective_total <= ceilings["maximum_provider_total_tokens"],
                "Root-release provider-total-token ceiling exceeded by completed response",
            )
            ledger["successful_calls"] += 1
            ledger["provider_reported_input_tokens"] += usage["input_tokens"]
            ledger["provider_reported_output_tokens"] += usage["output_tokens"]
            ledger["provider_reported_total_tokens"] = prospective_total
            completed_path = attempt_dir / f"{prefix}-completed.json"
            completed_receipt = {
                "schema_version": "rq2b-v7-qwen-reranker-b2-request-complete-v1",
                "request_attempt": serial,
                "request_sha256": request_sha,
                "response_sha256": canonical_sha256(response),
                "score_count": len(scores),
                "scores_in_request_index_order": scores,
                "provider_usage": usage,
                "wall_time_ms": (time.monotonic() - call_started) * 1000,
                "completed_at_utc": utc_now(),
            }
            write_json_new(completed_path, completed_receipt)
            request_index.append({
                "request_attempt": serial,
                "status": "SUCCESS",
                "started_receipt": {"path": relative(started_path, root), "sha256": file_sha256(started_path)},
                "terminal_receipt": {"path": relative(completed_path, root), "sha256": file_sha256(completed_path)},
            })
            score_batches.append(scores)
        except Exception as error:
            ledger["failures"] += 1
            timed_out = isinstance(error, ProviderRequestError) and error.timed_out
            if timed_out:
                ledger["timeouts"] += 1
            failure_path = attempt_dir / f"{prefix}-failed.json"
            failure_receipt = {
                "schema_version": "rq2b-v7-qwen-reranker-b2-request-failure-v1",
                "request_attempt": serial,
                "request_sha256": request_sha,
                "automatic_retries": 0,
                "timed_out": timed_out,
                "failure_type": type(error).__name__,
                "failure_message": str(error),
                "wall_time_ms": (time.monotonic() - call_started) * 1000,
                "failed_at_utc": utc_now(),
            }
            write_json_new(failure_path, failure_receipt)
            request_index.append({
                "request_attempt": serial,
                "status": "FAILED",
                "started_receipt": {"path": relative(started_path, root), "sha256": file_sha256(started_path)},
                "terminal_receipt": {"path": relative(failure_path, root), "sha256": file_sha256(failure_path)},
            })
            raise
    anchor_comparisons = verify_duplicate_anchor_scores(batches, score_batches)
    canonical: dict[tuple[str, int, str], float] = {}
    for batch, scores in zip(batches, score_batches, strict=True):
        for entry, score in zip(batch["entries"], scores, strict=True):
            window = entry["window"]
            key = (window["skill_id"], window["window_index"], window["text_sha256"])
            if not entry["is_anchor_duplicate"]:
                require(key not in canonical, "Canonical candidate window was submitted twice")
                canonical[key] = float(score)
    delta = {key: ledger[key] - before[key] for key in ledger}
    return canonical, anchor_comparisons, delta


def make_b2_row(
    *, run_id: str, condition_authority: dict[str, Any], prompt: dict[str, Any],
    work: dict[str, Any], ranked: list[dict[str, Any]], delta: dict[str, int],
    wall_time_ms: float,
) -> dict[str, Any]:
    inputs = work["input_candidates"]
    outputs = [
        {
            "rank": rank,
            "input_rank": row["input_rank"],
            "source_sha256": row["source_sha256"],
            "score": row["score"],
        }
        for rank, row in enumerate(ranked, 1)
    ]
    return {
        "schema_version": B2_SCHEMA,
        "status": "SUCCESS",
        "run_id": run_id,
        "condition_id": condition_authority["condition_id"],
        "phase": condition_authority["phase"],
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "representation": condition_authority["representation"],
        "first_stage_retriever": condition_authority["retriever"],
        "reranker": condition_authority["reranker"],
        "persisted_candidate_source": condition_authority["persisted_candidate_source"],
        "source_union_sha256": condition_authority["source_union_sha256"],
        "input_top20_binding_sha256": work["input_top20_binding_sha256"],
        "reranker_input_sha256": reranker_input_sha256(
            condition_id=condition_authority["condition_id"],
            prompt_id=prompt["prompt_id"],
            prompt_sha256=prompt["prompt_sha256"],
            input_top20_binding_sha256=work["input_top20_binding_sha256"],
            input_candidates=inputs,
        ),
        "score_semantics": "HIGHER_IS_BETTER",
        "input_candidates": inputs,
        "reranked_candidates": outputs,
        "cost": {
            "wall_time_ms": wall_time_ms,
            "provider_calls": delta["successful_calls"],
            "input_tokens": delta["external_submission_proxy_tokens"],
            "output_tokens": delta["provider_reported_output_tokens"],
            "window_forwards": delta["external_documents"],
            "cache_hits": 0,
            "retry_count": 0,
            "timeout_count": 0,
            "failure_count": 0,
            "candidate_pairs": TOP_K,
        },
    }


def execute(root: Path, authorisation_path: Path) -> dict[str, Any]:
    root = root.resolve()
    release, payload = validate_root_release(root, authorisation_path.resolve())
    attempt_dir = release["_destinations"]["attempt_dir"]
    output_dir = release["_destinations"]["output_dir"]
    staging_dir = output_dir.with_name(f"{output_dir.name}.staging-{release['attempt_id']}")
    require(not staging_dir.exists(), "Output staging destination already exists")
    attempt_dir.mkdir(parents=True, exist_ok=False)
    ledger = empty_ledger()
    request_index: list[dict[str, Any]] = []
    run_started = time.monotonic()
    write_json_new(attempt_dir / "run_started.json", {
        "schema_version": "rq2b-v7-qwen-reranker-b2-run-start-v1",
        "runner_version": RUNNER_VERSION,
        "run_id": release["run_id"],
        "attempt_id": release["attempt_id"],
        "root_release_id": release["root_release_id"],
        "root_release_sha256": file_sha256(authorisation_path),
        "payload": {
            "path": relative(release["_payload_path"], root),
            "sha256": file_sha256(release["_payload_path"]),
        },
        "provider": release["provider"],
        "ceilings": release["ceilings"],
        "started_at_utc": utc_now(),
    })
    try:
        api_key = os.environ.get(API_KEY_ENV)
        require(isinstance(api_key, str) and bool(api_key.strip()), f"{API_KEY_ENV} is absent")
        prompts, conditions, views, b1_by_key, official = load_authority(root, payload)
        official_validator = load_official_validator(root)
        tokenizer = load_proxy_tokenizer(root)
        b2_rows: list[dict[str, Any]] = []
        tie_rows: list[dict[str, Any]] = []
        window_audit_rows: list[dict[str, Any]] = []
        window_caches: dict[str, dict[str, list[dict[str, Any]]]] = {
            representation: {} for representation in REPRESENTATIONS
        }
        for condition_id in MATERIALISED_CONDITIONS:
            condition = conditions[condition_id]
            representation_rows = views[condition["representation"]]
            source_b1_condition = b1_condition_id(condition)
            for prompt in prompts:
                condition_started = time.monotonic()
                b1_row = b1_by_key[(source_b1_condition, prompt["prompt_id"])]
                work = build_condition_work(
                    tokenizer,
                    condition,
                    prompt,
                    b1_row,
                    representation_rows,
                    window_cache=window_caches[condition["representation"]],
                )
                canonical, anchor_comparisons, delta = score_work(
                    work,
                    request_fn=request_once,
                    api_key=api_key,
                    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
                    ceilings=release["ceilings"],
                    ledger=ledger,
                    attempt_dir=attempt_dir,
                    request_index=request_index,
                    started_at=run_started,
                    root=root,
                )
                candidates = work["condition"]["candidate_skill_ids"]
                ranked, ties = rank_candidate_scores(
                    candidates,
                    work["condition"]["candidate_windows"],
                    canonical,
                )
                row = make_b2_row(
                    run_id=release["run_id"],
                    condition_authority=condition,
                    prompt=prompt,
                    work=work,
                    ranked=ranked,
                    delta=delta,
                    wall_time_ms=(time.monotonic() - condition_started) * 1000,
                )
                validator_row_number = len(b2_rows) + 1
                official_validator.validate_b2_row(row, official, b1_by_key, validator_row_number)
                b2_rows.append(row)
                if ties:
                    tie_rows.append({
                        "schema_version": "rq2b-v7-qwen-reranker-b2-exact-ties-v1",
                        "condition_id": condition_id,
                        "prompt_id": prompt["prompt_id"],
                        "stable_tie_break": "source_sha256_ascending",
                        "ties": ties,
                    })
                window_audit_rows.append({
                    "schema_version": "rq2b-v7-qwen-reranker-b2-window-audit-v1",
                    "condition_id": condition_id,
                    "prompt_id": prompt["prompt_id"],
                    "input_top20_binding_sha256": work["input_top20_binding_sha256"],
                    "reranker_input_sha256": row["reranker_input_sha256"],
                    "candidate_list_sha256": work["condition"]["candidate_list_sha256"],
                    "window_count": len(work["condition"]["candidate_windows"]),
                    "window_binding_sha256": canonical_sha256(work["trusted_binding"]["candidate_windows"]),
                    "request_batch_count": len(work["batches"]),
                    "duplicate_anchor_comparisons": anchor_comparisons,
                    "provider_reported_input_tokens": delta["provider_reported_input_tokens"],
                    "provider_reported_output_tokens": delta["provider_reported_output_tokens"],
                    "provider_reported_total_tokens": delta["provider_reported_total_tokens"],
                })
        require(len(b2_rows) == EXPECTED_B2_ROWS, "B2 row coverage drift before publication")
        require(
            {(row["condition_id"], row["prompt_id"]) for row in b2_rows}
            == {
                (condition_id, prompt["prompt_id"])
                for condition_id in MATERIALISED_CONDITIONS
                for prompt in prompts
            },
            "B2 condition/prompt coverage drift before publication",
        )
        require("C2-Q" not in {row["condition_id"] for row in b2_rows}, "C2-Q was incorrectly materialised")
        require(ledger["request_attempts"] == ledger["successful_calls"], "Successful run contains a failed request attempt")
        require(ledger["failures"] == 0 and ledger["timeouts"] == 0, "Successful run contains failures/timeouts")
        require(
            time.monotonic() - run_started <= release["ceilings"]["maximum_wall_time_seconds"],
            "Root-release wall-time ceiling exceeded",
        )

        staging_dir.mkdir(parents=True, exist_ok=False)
        b2_path = staging_dir / "qwen_b2.jsonl.gz"
        ties_path = staging_dir / "exact_ties.jsonl.gz"
        window_path = staging_dir / "window_audit.jsonl.gz"
        index_path = staging_dir / "request_receipt_index.jsonl.gz"
        b2_artifact = write_deterministic_jsonl_gzip(b2_path, b2_rows)
        ties_artifact = write_deterministic_jsonl_gzip(ties_path, tie_rows)
        window_artifact = write_deterministic_jsonl_gzip(window_path, window_audit_rows)
        index_artifact = write_deterministic_jsonl_gzip(index_path, request_index)
        for artifact in (b2_artifact, ties_artifact, window_artifact, index_artifact):
            artifact["path"] = relative(output_dir / Path(artifact["path"]).name, root)

        cost_ledger = {
            "schema_version": "rq2b-v7-qwen-reranker-b2-cost-ledger-v1",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "provider": {"endpoint": ENDPOINT, "model": MODEL},
            "logical_cost": {
                "candidate_pairs": EXPECTED_B2_ROWS * TOP_K,
                "window_forwards": ledger["external_documents"],
                "local_proxy_submission_tokens": ledger["external_submission_proxy_tokens"],
            },
            "provider_cost": {
                "request_attempts": ledger["request_attempts"],
                "successful_calls": ledger["successful_calls"],
                "timeouts": ledger["timeouts"],
                "failures": ledger["failures"],
                "provider_reported_input_tokens": ledger["provider_reported_input_tokens"],
                "provider_reported_output_tokens": ledger["provider_reported_output_tokens"],
                "provider_reported_total_tokens": ledger["provider_reported_total_tokens"],
                "external_submission_utf8_bytes": ledger["external_submission_utf8_bytes"],
                "monetary_amount": None,
                "currency": None,
                "monetary_status": "NOT_RETURNED_BY_FROZEN_RERANK_RESPONSE_CONTRACT_NOT_ESTIMATED",
            },
            "automatic_retries": 0,
            "ceilings": release["ceilings"],
        }
        cost_path = staging_dir / "cost_ledger.json"
        write_json_new(cost_path, cost_ledger)
        cost_artifact = {"path": relative(output_dir / cost_path.name, root), "sha256": file_sha256(cost_path)}
        receipt = {
            "schema_version": "rq2b-v7-qwen-reranker-b2-run-receipt-v1",
            "status": "PASS_PHASE8_B1_BOUND_QWEN_B2_OUTPUT",
            "runner_version": RUNNER_VERSION,
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "root_release_id": release["root_release_id"],
            "root_release_sha256": file_sha256(authorisation_path),
            "payload_sha256": file_sha256(release["_payload_path"]),
            "phase8_receipt_sha256": payload["phase8"]["receipt"]["sha256"],
            "b1_validation_receipt_sha256": payload["b1_validation"]["receipt"]["sha256"],
            "rows": len(b2_rows),
            "conditions": list(MATERIALISED_CONDITIONS),
            "c2_q_alias_materialised": False,
            "artifacts": {
                "b2": b2_artifact,
                "exact_ties": ties_artifact,
                "window_audit": window_artifact,
                "request_receipt_index": index_artifact,
                "cost_ledger": cost_artifact,
            },
            "runtime": {
                "python": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "platform": platform.platform(),
            },
            "wall_time_seconds": time.monotonic() - run_started,
            "completed_at_utc": utc_now(),
        }
        receipt_path = staging_dir / "run_receipt.json"
        write_json_new(receipt_path, receipt)
        manifest_path = staging_dir / "manifest.json"
        write_json_new(manifest_path, {
            "schema_version": "rq2b-v7-qwen-reranker-b2-output-manifest-v1",
            "status": receipt["status"],
            "run_receipt": {
                "path": relative(output_dir / receipt_path.name, root),
                "sha256": file_sha256(receipt_path),
            },
            **receipt["artifacts"],
        })
        staging_dir.replace(output_dir)
        write_json_new(attempt_dir / "run_completed.json", {
            "schema_version": "rq2b-v7-qwen-reranker-b2-run-complete-v1",
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
            write_json_new(attempt_dir / "run_failed.json", {
                "schema_version": "rq2b-v7-qwen-reranker-b2-run-failed-v1",
                "run_id": release["run_id"],
                "attempt_id": release["attempt_id"],
                "automatic_retries": 0,
                "failure_type": type(error).__name__,
                "failure_message": str(error),
                "ledger_at_failure": ledger,
                "staging_path": relative(staging_dir, root),
                "staging_exists": staging_dir.exists(),
                "failed_at_utc": utc_now(),
            })
        raise


class CharacterTokenizer:
    """Small deterministic tokenizer used only by --self-test."""

    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        require(add_special_tokens is False, "Self-test tokenizer unexpected special tokens")
        return [ord(character) + 1 for character in text]

    def __call__(
        self, text: str, *, add_special_tokens: bool, return_offsets_mapping: bool,
    ) -> dict[str, Any]:
        require(add_special_tokens is False and return_offsets_mapping is True, "Self-test tokenizer mode drift")
        return {
            "input_ids": self.encode(text),
            "offset_mapping": [(index, index + 1) for index in range(len(text))],
        }


def synthetic_work() -> dict[str, Any]:
    tokenizer = CharacterTokenizer()
    sources = [f"{index:064x}" for index in range(1, TOP_K + 1)]
    prompt = {
        "prompt_id": "synthetic-prompt",
        "prompt": "Route this synthetic request.",
        "prompt_sha256": text_sha256("Route this synthetic request."),
    }
    condition = {
        "condition_id": "B01-GQ",
        "phase": "FIRST_CORE_MATRIX",
        "representation": "I1-discovery",
        "retriever": "BM25",
        "reranker": "Qwen-qwen3-rerank",
        "persisted_candidate_source": "B01",
        "source_union_sha256": SOURCE_UNION_SHA256,
    }
    b1 = {
        "retriever": "BM25",
        "representation": "I1-discovery",
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "top20_binding_sha256": "f" * 64,
        "ranked_candidates": [
            {"rank": rank, "source_sha256": source, "score": float(TOP_K - rank)}
            for rank, source in enumerate(sources, 1)
        ],
    }
    views = {
        source: {
            "selector_text": f"Synthetic exact source bytes for {source}.",
            "selector_text_sha256": text_sha256(f"Synthetic exact source bytes for {source}."),
        }
        for source in sources
    }
    return build_condition_work(tokenizer, condition, prompt, b1, views)


def self_test() -> dict[str, Any]:
    work = synthetic_work()
    validate_condition(work["condition"], work["trusted_binding"])
    windows = work["condition"]["candidate_windows"]
    drifted = {**work["condition"], "candidate_windows": [dict(row) for row in windows]}
    drifted["candidate_windows"][0]["text"] += " drift"
    drifted["candidate_windows"][0]["text_sha256"] = text_sha256(drifted["candidate_windows"][0]["text"])
    binding_drift_rejected = False
    try:
        validate_condition(drifted, work["trusted_binding"])
    except ValueError:
        binding_drift_rejected = True
    require(binding_drift_rejected, "Source-window binding drift was not rejected")

    canonical = {
        (window["skill_id"], window["window_index"], window["text_sha256"]): 1.0
        for window in windows
    }
    ranked, ties = rank_candidate_scores(work["condition"]["candidate_skill_ids"], windows, canonical)
    require(
        [row["source_sha256"] for row in ranked] == sorted(work["condition"]["candidate_skill_ids"]),
        "Stable source-SHA tie break failed",
    )
    incomplete_rejected = False
    try:
        parse_response_scores({"output": {"results": [{"index": 0, "relevance_score": 1.0}]}}, 2)
    except ValueError:
        incomplete_rejected = True
    require(incomplete_rejected, "Incomplete provider response was accepted")
    require("C2-Q" not in MATERIALISED_CONDITIONS, "C2-Q alias was materialised")
    return {
        "status": "PASS_SYNTHETIC_NO_PROVIDER_NO_NETWORK",
        "network_calls": 0,
        "provider_calls": 0,
        "conditions": len(MATERIALISED_CONDITIONS),
        "expected_rows": EXPECTED_B2_ROWS,
        "checks": {
            "exact_source_window_binding": True,
            "stable_source_sha_tie_break": bool(ties),
            "incomplete_response_rejected": True,
            "c2_q_not_materialised": True,
            "frozen_request_contract": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--pending-release", type=Path)
    parser.add_argument("--preflight-receipt", type=Path)
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.preflight:
        require(args.pending_release is not None, "--preflight requires --pending-release")
        require(args.preflight_receipt is not None, "--preflight requires --preflight-receipt")
        root = args.root.resolve()
        pending = args.pending_release if args.pending_release.is_absolute() else root / args.pending_release
        receipt_path = args.preflight_receipt if args.preflight_receipt.is_absolute() else root / args.preflight_receipt
        receipt = run_preflight(root, pending, receipt_path)
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    require(args.authorisation is not None, "--execute requires --authorisation")
    root = args.root.resolve()
    authorisation = args.authorisation if args.authorisation.is_absolute() else root / args.authorisation
    receipt = execute(root, authorisation)
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
