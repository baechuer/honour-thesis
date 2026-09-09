#!/usr/bin/env python3
"""Run the 15 materialised V7 SkillRouter reranker B2 conditions.

The runner consumes only Phase-8/hash-bound representation views and already
persisted, independently validated B1 rows.  It never regenerates candidates.
Twelve core ``*-GS`` conditions plus C1-S/C3-S/C4-S are materialised for all
1,077 queries; C2-S remains the exact B05-GS alias required by the plan.

Execution requires a one-use root release.  The scientific runtime is pinned
MPS/default-SDPA/bfloat16, exact-token-length unpadded batches of at most 16,
zero automatic retries, the released SkillRouter prompt and yes-minus-no final
token score, complete query-specific 2,048-token windows with 128-token source
overlap, maximum-window aggregation, and ascending source-SHA tie breaks.
"""

from __future__ import annotations

import argparse
import bisect
import gzip
import hashlib
import json
import math
import os
import platform
import re
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


RUNNER_VERSION = "rq2b-v7-skillrouter-reranker-b2-runner-v1"
PAYLOAD_SCHEMA = "rq2b-v7-skillrouter-reranker-b2-phase8-payload-v1"
AUTHORISATION_SCHEMA = "rq2b-v7-skillrouter-reranker-b2-root-release-v1"
B1_SCHEMA = "rq2b-v7-b1-runner-output-v1"
B2_SCHEMA = "rq2b-v7-b2-runner-output-v1"
B1_VALIDATION_RECEIPT_SCHEMA = "rq2b-v7-phase8-b1-official-validation-receipt-v1"
EXECUTION_APPROVAL_SCHEMA = "rq2b-v7-b36-c6-b2-user-execution-approval-v1"
MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
INSTRUCTION = (
    "Given a task description, judge whether the skill document "
    "is relevant and useful for completing the task"
)
BODY_FORMAT = "<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {document}"
PREFIX = (
    "<|im_start|>system\nJudge whether the Document meets the requirements "
    "based on the Query and the Instruct provided. Note that the answer can "
    'only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
)
SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
PROMPT_CONTRACT_SHA256 = "face140f238119fc19ba12de90131d1031ada388f08f73e641d0dffd6a00817e"
MAX_PAIR_TOKENS = 2048
PAIR_SAFETY_TOKENS = 16
PAIR_OVERLAP_TOKENS = 128
MAX_BATCH_SIZE = 16
TOP_K = 20
EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
EXPECTED_B1_ROWS = 12 * EXPECTED_QUERIES
EXPECTED_B2_ROWS = 15 * EXPECTED_QUERIES
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
CPU_SELECTION_NAMESPACE = "rq2b-v7-b36-c6-runtime-cpu-audit-v1"

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
REPRESENTATIONS = ("I1-discovery", "I2-original", "I3C-fielded", "I3-flat")
CORE_GS_CONDITIONS = tuple(f"B{index:02d}-GS" for index in range(1, 13))
BRIDGE_GS_CONDITIONS = ("C1-S", "C3-S", "C4-S")
MATERIALISED_CONDITIONS = CORE_GS_CONDITIONS + BRIDGE_GS_CONDITIONS
B1_CONDITIONS = tuple(f"B{index:02d}-G0" for index in range(1, 13))
MODEL_FILE_SHA256 = {
    "added_tokens.json": "c0284b582e14987fbd3d5a2cb2bd139084371ed9acbae488829a1c900833c680",
    "config.json": "17f3b5063350823bfda01f740ac14b9d1cd9cb80c738cbe0d9939c4988ac6b39",
    "generation_config.json": "b015f739ce02d6f51f0fbd1fbd6bfd22436983139cfb51514c86fa1ffe5dfef5",
    "merges.txt": "8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
    "model.safetensors": "34064850b1b512168309481a9cebe4ecaf55d0821bf22608f657b40033ed36d7",
    "special_tokens_map.json": "76862e765266b85aa9459767e33cbaf13970f327a0e88d1c65846c2ddd3a1ecd",
    "tokenizer.json": "ab19c66299579df20542864f9e27b79898ca05f35acc97fd9259aee385a07d4a",
    "tokenizer_config.json": "7f33cbb21bae9b2ed4a7396d68f9f10d6280d75332d04911cd6c5a0967bd10c9",
    "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
}
HEX = set("0123456789abcdef")
BLANK_BREAK_RE = re.compile(r"\n(?:[ \t]*\n)+")
HEADING_RE = re.compile(r"(?m)^(?:#{1,6}[ \t]+|[^\n]+\n(?:=+|-+)[ \t]*\n)")
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}
B1_KEYS = {
    "schema_version", "status", "run_id", "condition_id",
    "first_stage_cell_id", "prompt_id", "prompt_sha256", "representation",
    "retriever", "persisted_candidate_source", "source_union_sha256",
    "top_k", "score_semantics", "top20_binding_sha256",
    "ranked_candidates", "cost",
}
B2_KEYS = {
    "schema_version", "status", "run_id", "condition_id", "phase",
    "prompt_id", "prompt_sha256", "representation", "first_stage_retriever",
    "reranker", "persisted_candidate_source", "source_union_sha256",
    "input_top20_binding_sha256", "reranker_input_sha256", "score_semantics",
    "input_candidates", "reranked_candidates", "cost",
}
B1_COST_KEYS = {
    "wall_time_ms", "provider_calls", "input_tokens", "output_tokens",
    "window_forwards", "cache_hits", "retry_count", "timeout_count",
    "failure_count",
}
B2_COST_KEYS = B1_COST_KEYS | {"candidate_pairs"}
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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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
    if path.suffix == ".gz":
        context = gzip.open(path, "rt", encoding="utf-8", newline="")
    else:
        context = path.open("r", encoding="utf-8", newline="")
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
    raw_bytes = 0
    count = 0
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                encoded = (
                    json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode("utf-8")
                zipped.write(encoded)
                digest.update(encoded)
                raw_bytes += len(encoded)
                count += 1
    return {
        "sha256": file_sha256(path),
        "rows": count,
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


def validate_artifact(root: Path, item: Any, *, field: str, rows: int | None = None) -> Path:
    exact_keys(item, {"path", "sha256", "rows"}, field)
    require(is_sha256(item["sha256"]), f"{field}: invalid SHA-256")
    if rows is not None:
        require(item["rows"] == rows, f"{field}: row binding drift")
    path = root_path(root, item["path"], field=f"{field}.path")
    require(path.is_file() and file_sha256(path) == item["sha256"], f"{field}: artifact missing or hash drift")
    return path


def method_contract() -> dict[str, Any]:
    return {
        "model": MODEL,
        "revision": REVISION,
        "instruction": INSTRUCTION,
        "body_format": BODY_FORMAT,
        "prefix": PREFIX,
        "suffix": SUFFIX,
        "prompt_contract_sha256": PROMPT_CONTRACT_SHA256,
        "score": "final_token_yes_logit_minus_no_logit",
        "maximum_pair_tokens": MAX_PAIR_TOKENS,
        "pair_safety_tokens": PAIR_SAFETY_TOKENS,
        "document_overlap_tokens": PAIR_OVERLAP_TOKENS,
        "document_score_aggregation": "maximum_window_score",
        "stable_tie_break": "source_sha256_ascending",
        "top_k": TOP_K,
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
    require(payload["state"] == "SEALED_LABEL_FREE_PHASE8_B1_BOUND_PAYLOAD", "Payload is not Phase-8/B1 sealed")
    require(payload["runner_version"] == RUNNER_VERSION, "Payload runner version drift")
    implementation = payload["implementation"]
    exact_keys(implementation, {"runner", "official_output_validator"}, "payload.implementation")
    expected = {
        "runner": Path(__file__).resolve(),
        "official_output_validator": (root / VALIDATOR_REL).resolve(),
    }
    for name, expected_path in expected.items():
        binding = implementation[name]
        exact_keys(binding, {"path", "sha256"}, f"payload.implementation.{name}")
        require(root_path(root, binding["path"], field=f"implementation.{name}.path") == expected_path, f"Implementation path drift: {name}")
        require(binding["sha256"] == file_sha256(expected_path), f"Implementation hash drift: {name}")

    phase8 = payload["phase8"]
    exact_keys(phase8, {"status", "receipt", "final_v4_1_i3_hashes_bound"}, "payload.phase8")
    require(phase8["status"] == "PASS" and phase8["final_v4_1_i3_hashes_bound"] is True, "Phase-8 final representation gate is not PASS")
    validate_artifact(root, {**phase8["receipt"], "rows": 1}, field="payload.phase8.receipt", rows=1)

    inputs = payload["inputs"]
    exact_keys(inputs, {"runtime", "source_manifest", "core_conditions", "bridge_conditions", "representations", "b1_artifacts"}, "payload.inputs")
    fixed = {
        "runtime": (RUNTIME_REL, EXPECTED_QUERIES),
        "source_manifest": (SOURCE_REL, EXPECTED_SOURCES),
        "core_conditions": (CORE_REL, 36),
        "bridge_conditions": (BRIDGE_REL, 6),
    }
    for name, (rel_path, rows) in fixed.items():
        item = inputs[name]
        require(item == {"path": rel_path.as_posix(), "sha256": FIXED_INPUT_SHA256[rel_path], "rows": rows}, f"Fixed payload input drift: {name}")
        validate_artifact(root, item, field=f"payload.inputs.{name}", rows=rows)
    representations = inputs["representations"]
    exact_keys(representations, set(REPRESENTATIONS), "payload.inputs.representations")
    for representation, item in representations.items():
        exact_keys(item, {"path", "sha256", "rows", "phase8_final", "extraction_protocol"}, f"representations.{representation}")
        require(item["rows"] == EXPECTED_SOURCES and item["phase8_final"] is True, f"{representation}: final Phase-8 binding missing")
        if representation in FIXED_REPRESENTATION_INPUTS:
            frozen = FIXED_REPRESENTATION_INPUTS[representation]
            require(item["path"] == frozen["path"] and item["sha256"] == frozen["sha256"], f"{representation}: authoritative V2 I1/I2 binding drift")
            require(item["extraction_protocol"] == "SOURCE_NATIVE_PHASE7_V2", f"{representation}: protocol drift")
        else:
            require(item["extraction_protocol"] == "I3C_SUBAGENT_EXTRACTION_V4_1", f"{representation}: final V4.1 protocol missing")
        validate_artifact(root, {"path": item["path"], "sha256": item["sha256"], "rows": item["rows"]}, field=f"representations.{representation}", rows=EXPECTED_SOURCES)

    artifacts = inputs["b1_artifacts"]
    require(isinstance(artifacts, list) and artifacts, "At least one persisted B1 artifact is required")
    for index, artifact in enumerate(artifacts):
        validate_artifact(root, artifact, field=f"payload.inputs.b1_artifacts[{index}]")
    b1_validation = payload["b1_validation"]
    exact_keys(b1_validation, {"status", "receipt", "condition_ids", "rows"}, "payload.b1_validation")
    require(b1_validation["status"] == "PASS_12_PERSISTED_B1_CELLS", "Persisted B1 validation is not PASS")
    require(b1_validation["condition_ids"] == list(B1_CONDITIONS) and b1_validation["rows"] == EXPECTED_B1_ROWS, "Persisted B1 validation scope drift")
    receipt_path = validate_artifact(root, {**b1_validation["receipt"], "rows": 1}, field="payload.b1_validation.receipt", rows=1)
    receipt = read_json(receipt_path)
    validate_b1_validation_receipt(receipt)
    require(receipt.get("b1_cells") == 12 and receipt.get("b1_rows") == EXPECTED_B1_ROWS, "Official B1 validation receipt coverage drift")

    require(payload["counts"] == {
        "queries": EXPECTED_QUERIES,
        "sources": EXPECTED_SOURCES,
        "persisted_b1_cells": 12,
        "persisted_b1_rows": EXPECTED_B1_ROWS,
        "materialised_b2_conditions": 15,
        "materialised_b2_rows": EXPECTED_B2_ROWS,
        "c2_s_alias_rows": 0,
    }, "Payload count contract drift")
    require(payload["method"] == method_contract(), "Payload method contract drift")
    require(payload["label_isolation"] == {
        "labels_or_results_read": False,
        "b1_candidates_regenerated": False,
        "offline_scorer_run": False,
    }, "Payload label-isolation contract drift")
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
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    try:
        authorisation_path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Root release must be inside repository root") from error
    require(authorisation_path.is_file(), "Root-release authorisation is missing")
    release = read_json(authorisation_path)
    exact_keys(
        release,
        {"schema_version", "state", "root_release_id", "run_id", "attempt_id",
         "payload", "phase8", "b1_validation_receipt_sha256", "approval", "model_snapshot",
         "runtime", "cpu_fp32_sensitivity", "destinations", "ceilings"},
        "root_release",
    )
    require(release["schema_version"] == AUTHORISATION_SCHEMA, "Root-release schema drift")
    require(release["state"] == "EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_B1_BOUND_EXECUTION", "Scientific B2 execution is not root-released")
    for name in ("root_release_id", "run_id", "attempt_id"):
        require(isinstance(release[name], str) and release[name], f"Root-release {name} missing")
    exact_keys(release["payload"], {"path", "sha256"}, "root_release.payload")
    require(is_sha256(release["payload"]["sha256"]), "Payload SHA is absent")
    payload_path = root_path(root, release["payload"]["path"], field="root_release.payload.path")
    require(payload_path.is_file() and file_sha256(payload_path) == release["payload"]["sha256"], "Root-release payload drift")
    payload = validate_payload(root, payload_path)
    require(release["phase8"] == {"status": "PASS", "receipt_sha256": payload["phase8"]["receipt"]["sha256"]}, "Root-release Phase-8 binding drift")
    require(release["b1_validation_receipt_sha256"] == payload["b1_validation"]["receipt"]["sha256"], "Root-release B1 validation binding drift")
    approval_binding = release["approval"]
    exact_keys(approval_binding, {"path", "sha256", "decision", "scope"}, "root_release.approval")
    approval_path = root_path(root, approval_binding["path"], field="root_release.approval.path")
    require(approval_path.is_file() and file_sha256(approval_path) == approval_binding["sha256"], "Execution approval hash drift")
    approval = read_json(approval_path)
    require(approval.get("schema_version") == EXECUTION_APPROVAL_SCHEMA and approval.get("decision") == "APPROVED", "Execution approval is not a valid B2 approval")
    require(approval_binding["decision"] == approval["decision"] and approval_binding["scope"] == approval.get("scope"), "Execution approval binding drift")
    scope = approval_binding["scope"]
    require(scope.get("frozen_library") == "V7_3798_SOURCES_1077_QUERIES" and scope.get("experiment") == "B36_CORE_PLUS_C6_DIAGNOSTIC", "Execution approval experiment scope drift")
    require(scope.get("phase8_b2_prerequisite") is True and scope.get("local_skillrouter_reranker") is True, "Execution approval does not cover SkillRouter B2")
    require(approval.get("secrets_recorded") is False, "Execution approval must not contain secrets")

    snapshot = release["model_snapshot"]
    exact_keys(snapshot, {"path", "repository", "revision", "files"}, "root_release.model_snapshot")
    require(snapshot["repository"] == MODEL and snapshot["revision"] == REVISION, "Model identity drift")
    require(snapshot["files"] == MODEL_FILE_SHA256, "Model file binding drift")
    snapshot_path = root_path(root, snapshot["path"], field="root_release.model_snapshot.path")
    require(snapshot_path.is_dir(), "Pinned reranker snapshot is absent")
    for name, expected in MODEL_FILE_SHA256.items():
        path = snapshot_path / name
        require(path.is_file() and file_sha256(path) == expected, f"Pinned reranker snapshot drift: {name}")

    runtime = release["runtime"]
    exact_keys(runtime, {"device", "dtype", "attention_implementation", "exact_model_input_token_length_batches", "padding", "batch_size", "maximum_batch_size", "automatic_retries", "local_files_only", "trust_remote_code"}, "root_release.runtime")
    require(runtime["device"] == "mps" and runtime["dtype"] == "bfloat16" and runtime["attention_implementation"] == "default_sdpa", "Primary runtime drift")
    require(runtime["exact_model_input_token_length_batches"] is True and runtime["padding"] is False, "Exact-length no-padding contract drift")
    require(isinstance(runtime["batch_size"], int) and not isinstance(runtime["batch_size"], bool) and 0 < runtime["batch_size"] <= MAX_BATCH_SIZE, "Released batch size must be 1..16")
    require(runtime["maximum_batch_size"] == MAX_BATCH_SIZE and runtime["automatic_retries"] == 0, "Batch/retry contract drift")
    require(runtime["local_files_only"] is True and runtime["trust_remote_code"] is False, "Local model loading contract drift")
    require(release["cpu_fp32_sensitivity"] == {
        "required": True,
        "execute_during_primary": False,
        "samples_per_representation": 8,
        "maximum_samples": 32,
        "selection_namespace": CPU_SELECTION_NAMESPACE,
        "state": "PENDING_SEPARATE_EXPLICIT_AUTHORISATION",
    }, "CPU fp32 sensitivity hook contract drift")
    exact_keys(release["destinations"], {"output_dir", "cache_dir", "attempt_dir"}, "root_release.destinations")
    destinations = {
        name: root_path(root, value, field=f"destinations.{name}")
        for name, value in release["destinations"].items()
    }
    for name, path in destinations.items():
        require(relative(path, root).startswith("skill_benchmark/cache/"), f"{name}: destination must be under skill_benchmark/cache")
    require(len(set(destinations.values())) == 3, "Output/cache/attempt destinations must be distinct")
    require(not destinations["cache_dir"].exists(), "Score-cache namespace must not exist before this one-use execution")
    exact_keys(release["ceilings"], CEILING_KEYS, "root_release.ceilings")
    for name in CEILING_KEYS - {"maximum_wall_time_seconds"}:
        require(isinstance(release["ceilings"][name], int) and not isinstance(release["ceilings"][name], bool) and release["ceilings"][name] >= 0, f"Invalid ceiling: {name}")
    require(isinstance(release["ceilings"]["maximum_wall_time_seconds"], (int, float)) and release["ceilings"]["maximum_wall_time_seconds"] > 0, "Invalid wall-time ceiling")
    release["_snapshot_path"] = snapshot_path
    release["_destinations"] = destinations
    return release, payload_path, payload


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


def load_authority(
    root: Path, payload: dict[str, Any]
) -> tuple[
    list[dict[str, Any]],
    set[str],
    dict[str, dict[str, Any]],
    dict[str, dict[str, dict[str, Any]]],
    dict[tuple[str, str], dict[str, Any]],
]:
    inputs = payload["inputs"]
    prompts = read_jsonl_any(root_path(root, inputs["runtime"]["path"], field="runtime.path"))
    require(len(prompts) == EXPECTED_QUERIES, "Runtime query count drift")
    prompt_by_id = {str(row.get("prompt_id")): row for row in prompts}
    require(len(prompt_by_id) == EXPECTED_QUERIES, "Runtime query identity drift")
    for index, row in enumerate(prompts):
        reject_outcome_keys(row, f"runtime[{index}]")
        exact_keys(row, {"schema_version", "prompt_id", "prompt", "prompt_sha256"}, f"runtime[{index}]")
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1" and text_sha256(row["prompt"]) == row["prompt_sha256"], "Runtime prompt schema/hash drift")

    source_rows = read_jsonl_any(root_path(root, inputs["source_manifest"]["path"], field="source_manifest.path"))
    sources = {str(row.get("sha256")) for row in source_rows}
    require(len(sources) == len(source_rows) == EXPECTED_SOURCES and all(is_sha256(value) for value in sources), "Source identity drift")
    for index, row in enumerate(source_rows):
        reject_outcome_keys(row, f"sources[{index}]")
        exact_keys(row, {"path", "sha256", "bytes"}, f"sources[{index}]")

    core = read_jsonl_any(root_path(root, inputs["core_conditions"]["path"], field="core_conditions.path"))
    bridge = read_jsonl_any(root_path(root, inputs["bridge_conditions"]["path"], field="bridge_conditions.path"))
    all_conditions = {str(row["condition_id"]): row for row in [*core, *bridge]}
    require(len(core) == 36 and len(bridge) == 6 and len(all_conditions) == 42, "Condition authority drift")
    conditions: dict[str, dict[str, Any]] = {}
    for condition_id in MATERIALISED_CONDITIONS:
        condition = all_conditions.get(condition_id)
        require(condition is not None, f"Missing materialised condition: {condition_id}")
        reject_outcome_keys(condition, f"conditions.{condition_id}")
        require(condition["reranker"] == "SkillRouter-Reranker-0.6B", f"{condition_id}: reranker drift")
        require(condition["source_union_sha256"] == SOURCE_UNION_SHA256 and condition["prompt_manifest_sha256"] == PROMPT_MANIFEST_SHA256, f"{condition_id}: authority hash drift")
        require(condition["runtime_rerank_k"] == TOP_K and condition["query_count"] == EXPECTED_QUERIES, f"{condition_id}: scope drift")
        require(condition["execution_authorised"] is False, f"{condition_id}: preparation unexpectedly authorises execution")
        conditions[condition_id] = condition
    require("C2-S" not in all_conditions, "C2-S must not be materialised in condition authority")

    views: dict[str, dict[str, dict[str, Any]]] = {}
    for representation, artifact in inputs["representations"].items():
        rows = read_jsonl_any(root_path(root, artifact["path"], field=f"representations.{representation}.path"))
        indexed: dict[str, dict[str, Any]] = {}
        for index, row in enumerate(rows):
            reject_outcome_keys(row, f"{representation}[{index}]")
            source = row.get("source_sha256")
            text = row.get("selector_text")
            require(source in sources and source not in indexed, f"{representation}: source identity/duplicate drift")
            require(row.get("representation") == representation, f"{representation}: row tag drift")
            require(isinstance(text, str) and text and row.get("selector_text_sha256") == text_sha256(text), f"{representation}: selector text hash drift")
            indexed[str(source)] = row
        require(len(indexed) == EXPECTED_SOURCES and set(indexed) == sources, f"{representation}: source coverage drift")
        views[representation] = indexed

    b1_rows: list[dict[str, Any]] = []
    for index, artifact in enumerate(inputs["b1_artifacts"]):
        path = root_path(root, artifact["path"], field=f"b1_artifacts[{index}].path")
        rows = read_jsonl_any(path)
        require(len(rows) == artifact["rows"], f"B1 artifact row-count drift: {path}")
        b1_rows.extend(rows)
    b1_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    condition_authority = {str(row["condition_id"]): row for row in core if row["reranker"] == "NONE"}
    require(set(condition_authority) == set(B1_CONDITIONS), "B1 condition authority drift")
    for row_number, row in enumerate(b1_rows, 1):
        prefix = f"B1 row {row_number}"
        reject_outcome_keys(row, prefix)
        exact_keys(row, B1_KEYS, prefix)
        require(row["schema_version"] == B1_SCHEMA and row["status"] == "SUCCESS", f"{prefix}: schema/status drift")
        condition = condition_authority.get(row["condition_id"])
        prompt = prompt_by_id.get(row["prompt_id"])
        require(condition is not None and prompt is not None, f"{prefix}: unknown condition/prompt")
        require(row["first_stage_cell_id"] == row["condition_id"].removesuffix("-G0"), f"{prefix}: first-stage cell drift")
        require(row["prompt_sha256"] == prompt["prompt_sha256"], f"{prefix}: prompt hash drift")
        for field in ("representation", "retriever", "persisted_candidate_source", "source_union_sha256"):
            require(row[field] == condition[field], f"{prefix}: {field} authority drift")
        ranked = row["ranked_candidates"]
        require(row["top_k"] == 100 and row["score_semantics"] == "HIGHER_IS_BETTER" and isinstance(ranked, list) and len(ranked) == 100, f"{prefix}: Top-100 contract drift")
        identities: list[str] = []
        for rank, candidate in enumerate(ranked, 1):
            exact_keys(candidate, {"rank", "source_sha256", "score"}, f"{prefix}.candidate[{rank - 1}]")
            require(candidate["rank"] == rank and candidate["source_sha256"] in sources, f"{prefix}: candidate identity/rank drift")
            require(isinstance(candidate["score"], (int, float)) and not isinstance(candidate["score"], bool) and math.isfinite(candidate["score"]), f"{prefix}: non-finite candidate score")
            identities.append(candidate["source_sha256"])
        require(len(set(identities)) == 100, f"{prefix}: duplicate candidate")
        require(row["top20_binding_sha256"] == top20_binding_sha256(
            condition_id=row["condition_id"], prompt_id=row["prompt_id"],
            prompt_sha256=row["prompt_sha256"], ordered_source_sha256=identities[:20]
        ), f"{prefix}: Top-20 binding drift")
        exact_keys(row["cost"], B1_COST_KEYS, f"{prefix}.cost")
        key = (row["condition_id"], row["prompt_id"])
        require(key not in b1_by_key, f"{prefix}: duplicate B1 key")
        b1_by_key[key] = row
    expected_keys = {(condition, prompt_id) for condition in B1_CONDITIONS for prompt_id in prompt_by_id}
    require(set(b1_by_key) == expected_keys and len(b1_rows) == EXPECTED_B1_ROWS, "Persisted B1 12-cell coverage drift")
    return prompts, sources, conditions, views, b1_by_key


def build_pair_ids(tokenizer: Any, query: str, document: str) -> list[int]:
    body = BODY_FORMAT.format(instruction=INSTRUCTION, query=query, document=document)
    return (
        list(tokenizer.encode(PREFIX, add_special_tokens=False))
        + list(tokenizer.encode(body, add_special_tokens=False))
        + list(tokenizer.encode(SUFFIX, add_special_tokens=False))
    )


def lossless_markdown_windows(
    tokenizer: Any, text: str, *, maximum_content_tokens: int,
    overlap_tokens: int,
) -> list[dict[str, Any]]:
    require(bool(text), "Cannot window empty selector text")
    require(0 <= overlap_tokens < maximum_content_tokens, "Invalid reranker overlap")
    encoded_full = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    offsets = [
        tuple(map(int, pair)) for pair in encoded_full["offset_mapping"]
        if int(pair[1]) > int(pair[0])
    ]
    require(bool(offsets), "Selector text has no tokenizer spans")
    token_ends = [end for _, end in offsets]
    preferred = {len(text)}
    preferred.update(match.end() for match in BLANK_BREAK_RE.finditer(text))
    preferred.update(match.start() for match in HEADING_RE.finditer(text) if match.start() > 0)
    boundaries = sorted(value for value in preferred if 0 < value <= len(text))
    windows: list[dict[str, Any]] = []
    start = 0
    while start < len(text):
        first_token = bisect.bisect_right(token_ends, start)
        require(first_token < len(offsets), "Window start exceeded tokenizer spans")
        last_token = min(first_token + maximum_content_tokens - 1, len(offsets) - 1)
        hard_end = len(text) if last_token == len(offsets) - 1 else offsets[last_token][1]
        boundary_index = bisect.bisect_right(boundaries, hard_end) - 1
        end = boundaries[boundary_index] if boundary_index >= 0 and boundaries[boundary_index] > start else hard_end
        while True:
            encoded = tokenizer(text[start:end], add_special_tokens=False, return_offsets_mapping=True)
            token_ids = list(encoded["input_ids"])
            local_offsets = [
                tuple(map(int, pair)) for pair in encoded["offset_mapping"]
                if int(pair[1]) > int(pair[0])
            ]
            if len(token_ids) <= maximum_content_tokens:
                break
            require(len(local_offsets) >= 2, "Cannot reduce over-budget reranker window")
            end = start + local_offsets[-2][1]
        require(start < end <= len(text), "Reranker window cannot advance")
        window_text = text[start:end]
        windows.append({
            "window_index": len(windows),
            "text": window_text,
            "text_sha256": text_sha256(window_text),
            "source_start_char": start,
            "source_end_char": end,
            "content_token_count": len(token_ids),
        })
        if end == len(text):
            break
        next_start = end if len(token_ids) <= overlap_tokens else start + local_offsets[len(token_ids) - overlap_tokens][0]
        require(start < next_start <= end, "Reranker overlap did not advance")
        start = next_start
    require(windows[0]["source_start_char"] == 0 and windows[-1]["source_end_char"] == len(text), "Reranker window endpoint coverage drift")
    reconstructed = ""
    previous_end = 0
    for index, window in enumerate(windows):
        require(window["window_index"] == index and window["source_start_char"] <= previous_end, "Reranker window order/gap drift")
        require(window["text"] == text[window["source_start_char"]:window["source_end_char"]], "Reranker window source drift")
        append_start = max(previous_end, window["source_start_char"])
        reconstructed += text[append_start:window["source_end_char"]]
        previous_end = max(previous_end, window["source_end_char"])
    require(reconstructed == text, "Reranker windows do not reconstruct exact selector text")
    return windows


def pair_cache_key(pair: dict[str, Any]) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-skillrouter-reranker-cache-key-v1",
        "model": MODEL,
        "revision": REVISION,
        "prompt_contract_sha256": PROMPT_CONTRACT_SHA256,
        "score": "final_token_yes_logit_minus_no_logit",
        "maximum_pair_tokens": MAX_PAIR_TOKENS,
        "pair_safety_tokens": PAIR_SAFETY_TOKENS,
        "document_overlap_tokens": PAIR_OVERLAP_TOKENS,
        "device_contract": "mps",
        "dtype_contract": "bfloat16",
        "attention_contract": "default_sdpa",
        "tokenizer_sha256": MODEL_FILE_SHA256["tokenizer.json"],
        "model_weights_sha256": MODEL_FILE_SHA256["model.safetensors"],
        "pair_id": pair["pair_id"],
        "pair_input_ids_sha256": pair["pair_input_ids_sha256"],
        "pair_input_tokens": pair["pair_input_tokens"],
    })


class ExactScoreCache:
    def __init__(self, root: Path) -> None:
        self.root = root

    def path(self, pair: dict[str, Any]) -> Path:
        return self.root / f"{pair_cache_key(pair)}.json"

    def load(self, pair: dict[str, Any]) -> float | None:
        path = self.path(pair)
        if not path.is_file():
            return None
        value = read_json(path)
        exact_keys(value, {"schema_version", "cache_key", "model", "revision", "prompt_contract_sha256", "score_semantics", "maximum_pair_tokens", "pair_safety_tokens", "document_overlap_tokens", "device_contract", "dtype_contract", "attention_contract", "tokenizer_sha256", "model_weights_sha256", "pair_id", "pair_input_ids_sha256", "pair_input_tokens", "score"}, f"cache.{path.name}")
        require(value["schema_version"] == "rq2b-v7-skillrouter-reranker-score-cache-v1" and value["cache_key"] == pair_cache_key(pair), "Score cache schema/key drift")
        require(value["model"] == MODEL and value["revision"] == REVISION and value["prompt_contract_sha256"] == PROMPT_CONTRACT_SHA256, "Score cache model/prompt drift")
        require(value["score_semantics"] == "yes_logit_minus_no_logit", "Score cache semantics drift")
        require(value["maximum_pair_tokens"] == MAX_PAIR_TOKENS and value["pair_safety_tokens"] == PAIR_SAFETY_TOKENS and value["document_overlap_tokens"] == PAIR_OVERLAP_TOKENS, "Score cache window contract drift")
        require(value["device_contract"] == "mps" and value["dtype_contract"] == "bfloat16" and value["attention_contract"] == "default_sdpa", "Score cache runtime drift")
        require(value["tokenizer_sha256"] == MODEL_FILE_SHA256["tokenizer.json"] and value["model_weights_sha256"] == MODEL_FILE_SHA256["model.safetensors"], "Score cache model-file drift")
        for field in ("pair_id", "pair_input_ids_sha256", "pair_input_tokens"):
            require(value[field] == pair[field], f"Score cache {field} drift")
        score = value["score"]
        require(isinstance(score, (int, float)) and not isinstance(score, bool) and math.isfinite(score), "Score cache non-finite value")
        return float(score)

    def store(self, pair: dict[str, Any], score: float) -> Path:
        require(math.isfinite(score), "Cannot cache non-finite score")
        path = self.path(pair)
        require(not path.exists(), f"Refusing to overwrite score cache: {path}")
        write_json_new(path, {
            "schema_version": "rq2b-v7-skillrouter-reranker-score-cache-v1",
            "cache_key": pair_cache_key(pair),
            "model": MODEL,
            "revision": REVISION,
            "prompt_contract_sha256": PROMPT_CONTRACT_SHA256,
            "score_semantics": "yes_logit_minus_no_logit",
            "maximum_pair_tokens": MAX_PAIR_TOKENS,
            "pair_safety_tokens": PAIR_SAFETY_TOKENS,
            "document_overlap_tokens": PAIR_OVERLAP_TOKENS,
            "device_contract": "mps",
            "dtype_contract": "bfloat16",
            "attention_contract": "default_sdpa",
            "tokenizer_sha256": MODEL_FILE_SHA256["tokenizer.json"],
            "model_weights_sha256": MODEL_FILE_SHA256["model.safetensors"],
            "pair_id": pair["pair_id"],
            "pair_input_ids_sha256": pair["pair_input_ids_sha256"],
            "pair_input_tokens": pair["pair_input_tokens"],
            "score": float(score),
        })
        return path


def exact_length_batches(
    pairs: Sequence[dict[str, Any]], batch_size: int
) -> list[list[dict[str, Any]]]:
    require(0 < batch_size <= MAX_BATCH_SIZE, "Batch size must be 1..16")
    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for pair in pairs:
        length = pair.get("pair_input_tokens")
        require(isinstance(length, int) and 0 < length <= MAX_PAIR_TOKENS, "Invalid pair token length")
        buckets[length].append(pair)
    batches: list[list[dict[str, Any]]] = []
    for length in sorted(buckets):
        bucket = sorted(buckets[length], key=lambda row: row["pair_id"])
        for start in range(0, len(bucket), batch_size):
            batch = bucket[start:start + batch_size]
            require(len({row["pair_input_tokens"] for row in batch}) == 1, "Heterogeneous pair batch forbidden")
            batches.append(batch)
    return batches


def build_pair_inventory(
    tokenizer: Any, prompts: list[dict[str, Any]], conditions: dict[str, dict[str, Any]],
    views: dict[str, dict[str, dict[str, Any]]],
    b1_by_key: dict[tuple[str, str], dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    pair_by_id: dict[str, dict[str, Any]] = {}
    condition_work: list[dict[str, Any]] = []
    window_cache: dict[tuple[str, str, str, str, int], list[dict[str, Any]]] = {}
    summary = {"candidate_occurrences": 0, "window_occurrences": 0, "windowed_candidates": 0}
    for condition_id in MATERIALISED_CONDITIONS:
        condition = conditions[condition_id]
        representation = condition["representation"]
        source_condition = f"{condition['persisted_candidate_source']}-G0"
        for prompt in prompts:
            b1 = b1_by_key[(source_condition, prompt["prompt_id"])]
            top20 = b1["ranked_candidates"][:TOP_K]
            input_candidates: list[dict[str, Any]] = []
            candidates: list[dict[str, Any]] = []
            empty_pair_tokens = len(build_pair_ids(tokenizer, prompt["prompt"], ""))
            document_budget = MAX_PAIR_TOKENS - empty_pair_tokens - PAIR_SAFETY_TOKENS
            require(document_budget > PAIR_OVERLAP_TOKENS, f"No safe document budget: {prompt['prompt_id']}")
            for input_rank, candidate in enumerate(top20, 1):
                source = candidate["source_sha256"]
                view = views[representation][source]
                input_candidates.append({
                    "input_rank": input_rank,
                    "source_sha256": source,
                    "candidate_view_sha256": view["selector_text_sha256"],
                })
                cache_key = (
                    representation, prompt["prompt_sha256"], source,
                    view["selector_text_sha256"], document_budget,
                )
                templates = window_cache.get(cache_key)
                if templates is None:
                    content_ids = list(tokenizer.encode(view["selector_text"], add_special_tokens=False))
                    if len(content_ids) <= document_budget:
                        templates = [{
                            "window_index": 0,
                            "text": view["selector_text"],
                            "text_sha256": view["selector_text_sha256"],
                            "source_start_char": 0,
                            "source_end_char": len(view["selector_text"]),
                            "content_token_count": len(content_ids),
                        }]
                    else:
                        templates = lossless_markdown_windows(
                            tokenizer, view["selector_text"],
                            maximum_content_tokens=document_budget,
                            overlap_tokens=PAIR_OVERLAP_TOKENS,
                        )
                    window_cache[cache_key] = templates
                summary["windowed_candidates"] += len(templates) > 1
                pair_ids: list[str] = []
                for template in templates:
                    input_ids = build_pair_ids(tokenizer, prompt["prompt"], template["text"])
                    require(len(input_ids) <= MAX_PAIR_TOKENS, "Pair exceeds sealed 2,048-token ceiling")
                    pair_id = canonical_sha256({
                        "schema_version": "rq2b-v7-skillrouter-reranker-pair-id-v1",
                        "representation": representation,
                        "prompt_sha256": prompt["prompt_sha256"],
                        "source_sha256": source,
                        "candidate_view_sha256": view["selector_text_sha256"],
                        "window_index": template["window_index"],
                        "window_text_sha256": template["text_sha256"],
                        "reranker_prompt_sha256": PROMPT_CONTRACT_SHA256,
                    })
                    pair = {
                        "pair_id": pair_id,
                        "representation": representation,
                        "prompt_id": prompt["prompt_id"],
                        "prompt_sha256": prompt["prompt_sha256"],
                        "source_sha256": source,
                        "candidate_view_sha256": view["selector_text_sha256"],
                        "window_index": template["window_index"],
                        "window_text": template["text"],
                        "window_text_sha256": template["text_sha256"],
                        "source_start_char": template["source_start_char"],
                        "source_end_char": template["source_end_char"],
                        "pair_input_ids_sha256": canonical_sha256(input_ids),
                        "pair_input_tokens": len(input_ids),
                    }
                    existing = pair_by_id.get(pair_id)
                    if existing is None:
                        pair_by_id[pair_id] = pair
                    else:
                        require(existing == pair, "Pair-ID collision")
                    pair_ids.append(pair_id)
                candidates.append({
                    "input_rank": input_rank,
                    "source_sha256": source,
                    "pair_ids": pair_ids,
                })
                summary["candidate_occurrences"] += 1
                summary["window_occurrences"] += len(pair_ids)
            condition_work.append({
                "condition": condition,
                "prompt": prompt_by_id[prompt["prompt_id"]],
                "input_top20_binding_sha256": b1["top20_binding_sha256"],
                "input_candidates": input_candidates,
                "candidates": candidates,
            })
    require(len(condition_work) == EXPECTED_B2_ROWS, "B2 condition work coverage drift")
    summary["unique_pairs"] = len(pair_by_id)
    return pair_by_id, condition_work, summary


def rank_candidate_scores(
    candidates: list[dict[str, Any]], pair_scores: dict[str, float]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scored: list[tuple[str, int, float]] = []
    for candidate in candidates:
        scores = [pair_scores[pair_id] for pair_id in candidate["pair_ids"]]
        require(bool(scores) and all(math.isfinite(score) for score in scores), "Candidate window score coverage drift")
        scored.append((candidate["source_sha256"], candidate["input_rank"], max(scores)))
    ranked = sorted(scored, key=lambda row: (-row[2], row[0]))
    output = [
        {"rank": rank, "input_rank": input_rank, "source_sha256": source, "score": score}
        for rank, (source, input_rank, score) in enumerate(ranked, 1)
    ]
    by_score: dict[float, list[str]] = defaultdict(list)
    for source, _, score in scored:
        by_score[score].append(source)
    ties = [
        {"score": score, "source_sha256": sorted(sources)}
        for score, sources in sorted(by_score.items(), key=lambda item: -item[0])
        if len(sources) > 1
    ]
    return output, ties


def cpu_sensitivity_plan(pair_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_representation: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for pair in pair_by_id.values():
        selection_hash = hashlib.sha256(
            f"{CPU_SELECTION_NAMESPACE}|{MODEL}|{pair['representation']}|{pair['pair_id']}".encode("utf-8")
        ).hexdigest()
        by_representation[pair["representation"]].append((selection_hash, pair))
    selections: dict[str, list[dict[str, Any]]] = {}
    for representation in REPRESENTATIONS:
        ordered = sorted(by_representation[representation], key=lambda value: (value[0], value[1]["pair_id"]))[:8]
        require(len(ordered) == 8, f"CPU sensitivity sample coverage drift: {representation}")
        selections[representation] = [{
            "selection_sha256": selection_hash,
            "pair_id": pair["pair_id"],
            "prompt_id": pair["prompt_id"],
            "source_sha256": pair["source_sha256"],
            "window_index": pair["window_index"],
            "pair_input_ids_sha256": pair["pair_input_ids_sha256"],
            "pair_input_tokens": pair["pair_input_tokens"],
        } for selection_hash, pair in ordered]
    return {
        "schema_version": "rq2b-v7-skillrouter-reranker-cpu-fp32-sensitivity-plan-v1",
        "state": "PENDING_SEPARATE_EXPLICIT_AUTHORISATION_NOT_EXECUTED",
        "selection_namespace": CPU_SELECTION_NAMESPACE,
        "component": MODEL,
        "samples_per_representation": 8,
        "maximum_samples": 32,
        "runtime": {"device": "cpu", "dtype": "float32", "attention_implementation": "eager"},
        "comparison": "primary_mps_bfloat16_yes_minus_no_score_absolute_delta_and_rank_tie_changes",
        "selections": selections,
        "model_loads": 0,
        "model_forwards": 0,
        "network_calls": 0,
    }


def _score_exact_batch(
    torch: Any, tokenizer: Any, model: Any, batch: list[dict[str, Any]],
    yes_token: int, no_token: int,
) -> list[float]:
    require(bool(batch) and len(batch) <= MAX_BATCH_SIZE, "Invalid score batch size")
    length = batch[0]["pair_input_tokens"]
    require(all(pair["pair_input_tokens"] == length for pair in batch), "Heterogeneous pair batch forbidden")
    rows = [build_pair_ids(tokenizer, pair["query"], pair["window_text"]) for pair in batch]
    require(all(len(ids) == length and canonical_sha256(ids) == pair["pair_input_ids_sha256"] for ids, pair in zip(rows, batch, strict=True)), "Runtime pair token drift")
    inputs = torch.tensor(rows, dtype=torch.long, device="mps")
    attention = torch.ones_like(inputs)
    with torch.inference_mode():
        logits = model(input_ids=inputs, attention_mask=attention).logits
        require(logits.device.type == "mps" and bool(torch.isfinite(logits).all().item()), "Non-finite or non-MPS reranker logits")
        final = logits[:, -1, :]
        values = (final[:, yes_token] - final[:, no_token]).float()
        require(bool(torch.isfinite(values).all().item()), "Non-finite yes-minus-no score")
        result = [float(value) for value in values.cpu().tolist()]
    return result


def validate_b2_rows(rows: list[dict[str, Any]], prompts: list[dict[str, Any]]) -> None:
    prompt_by_id = {row["prompt_id"]: row for row in prompts}
    expected = {(condition, prompt_id) for condition in MATERIALISED_CONDITIONS for prompt_id in prompt_by_id}
    actual: set[tuple[str, str]] = set()
    for row_number, row in enumerate(rows, 1):
        prefix = f"B2 row {row_number}"
        reject_outcome_keys(row, prefix)
        exact_keys(row, B2_KEYS, prefix)
        require(row["schema_version"] == B2_SCHEMA and row["status"] == "SUCCESS", f"{prefix}: schema/status drift")
        require(row["condition_id"] in MATERIALISED_CONDITIONS and row["condition_id"] != "C2-S", f"{prefix}: condition drift")
        require(row["prompt_id"] in prompt_by_id and row["prompt_sha256"] == prompt_by_id[row["prompt_id"]]["prompt_sha256"], f"{prefix}: prompt binding drift")
        require(row["score_semantics"] == "HIGHER_IS_BETTER", f"{prefix}: score semantics drift")
        inputs = row["input_candidates"]
        outputs = row["reranked_candidates"]
        require(isinstance(inputs, list) and isinstance(outputs, list) and len(inputs) == len(outputs) == TOP_K, f"{prefix}: Top-20 length drift")
        input_sources: list[str] = []
        for rank, candidate in enumerate(inputs, 1):
            exact_keys(candidate, {"input_rank", "source_sha256", "candidate_view_sha256"}, f"{prefix}.input[{rank - 1}]")
            require(candidate["input_rank"] == rank and is_sha256(candidate["source_sha256"]) and is_sha256(candidate["candidate_view_sha256"]), f"{prefix}: input candidate drift")
            input_sources.append(candidate["source_sha256"])
        expected_input_rank = {source: rank for rank, source in enumerate(input_sources, 1)}
        require(len(expected_input_rank) == TOP_K, f"{prefix}: duplicate input source")
        previous: tuple[float, str] | None = None
        output_sources: list[str] = []
        for rank, candidate in enumerate(outputs, 1):
            exact_keys(candidate, {"rank", "input_rank", "source_sha256", "score"}, f"{prefix}.output[{rank - 1}]")
            require(candidate["rank"] == rank and candidate["source_sha256"] in expected_input_rank and candidate["input_rank"] == expected_input_rank[candidate["source_sha256"]], f"{prefix}: output candidate drift")
            score = candidate["score"]
            require(isinstance(score, (int, float)) and not isinstance(score, bool) and math.isfinite(score), f"{prefix}: non-finite score")
            current = (-float(score), candidate["source_sha256"])
            require(previous is None or previous <= current, f"{prefix}: score/SHA tie order drift")
            previous = current
            output_sources.append(candidate["source_sha256"])
        require(set(output_sources) == set(input_sources), f"{prefix}: reranker is not an exact input permutation")
        require(row["reranker_input_sha256"] == reranker_input_sha256(
            condition_id=row["condition_id"], prompt_id=row["prompt_id"],
            prompt_sha256=row["prompt_sha256"], input_top20_binding_sha256=row["input_top20_binding_sha256"],
            input_candidates=inputs,
        ), f"{prefix}: reranker input hash drift")
        exact_keys(row["cost"], B2_COST_KEYS, f"{prefix}.cost")
        require(row["cost"]["candidate_pairs"] == TOP_K, f"{prefix}: candidate-pair count drift")
        require(isinstance(row["cost"]["wall_time_ms"], (int, float)) and not isinstance(row["cost"]["wall_time_ms"], bool) and math.isfinite(row["cost"]["wall_time_ms"]) and row["cost"]["wall_time_ms"] >= 0, f"{prefix}: wall time drift")
        require(all(isinstance(row["cost"][name], int) and not isinstance(row["cost"][name], bool) and row["cost"][name] >= 0 for name in B2_COST_KEYS - {"wall_time_ms"}), f"{prefix}: integer cost drift")
        key = (row["condition_id"], row["prompt_id"])
        require(key not in actual, f"{prefix}: duplicate output key")
        actual.add(key)
    require(actual == expected and len(rows) == EXPECTED_B2_ROWS, "15-condition B2 coverage drift")


def execute(root: Path, authorisation_path: Path) -> dict[str, Any]:
    release, payload_path, payload = validate_root_release(root, authorisation_path)
    destinations = release["_destinations"]
    output_dir = destinations["output_dir"]
    cache_dir = destinations["cache_dir"]
    attempt_dir = destinations["attempt_dir"]
    require(not output_dir.exists(), f"Refusing to overwrite output: {output_dir}")
    require(not attempt_dir.exists(), f"Refusing to overwrite attempt receipts: {attempt_dir}")
    require(not cache_dir.exists(), f"Refusing pre-existing score cache: {cache_dir}")
    staging = output_dir.with_name(f".{output_dir.name}.staging-{release['attempt_id']}")
    require(not staging.exists(), f"Stale output staging directory: {staging}")
    prompts, sources, conditions, views, b1_by_key = load_authority(root, payload)
    del sources
    attempt_dir.mkdir(parents=True, exist_ok=False)
    run_started = attempt_dir / "run_started.json"
    write_json_new(run_started, {
        "schema_version": "rq2b-v7-skillrouter-reranker-b2-run-start-v1",
        "run_id": release["run_id"],
        "attempt_id": release["attempt_id"],
        "root_release_id": release["root_release_id"],
        "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": file_sha256(authorisation_path)},
        "automatic_retries": 0,
        "started_at_utc": utc_now(),
    })
    wall_started = time.perf_counter()
    model_load_seconds = 0.0
    try:
        require(os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK", "0").lower() not in {"1", "true", "yes"}, "MPS CPU fallback is enabled")
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        require(torch.backends.mps.is_built() and torch.backends.mps.is_available(), "MPS unavailable; fallback is forbidden")
        load_started = time.perf_counter()
        tokenizer = AutoTokenizer.from_pretrained(release["_snapshot_path"], local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(
            release["_snapshot_path"], local_files_only=True, trust_remote_code=False,
            torch_dtype=torch.bfloat16,
        ).eval().to("mps")
        model_load_seconds = time.perf_counter() - load_started
        require(getattr(model.config, "_attn_implementation", None) == "sdpa", "Resolved attention is not SDPA")
        floating = [parameter for parameter in model.parameters() if parameter.is_floating_point()]
        require(bool(floating) and all(parameter.device.type == "mps" and parameter.dtype == torch.bfloat16 for parameter in floating), "Model device/dtype drift")
        yes = list(tokenizer.encode("yes", add_special_tokens=False))
        no = list(tokenizer.encode("no", add_special_tokens=False))
        require(len(yes) == len(no) == 1, "yes/no token contract drift")
        pair_by_id, condition_work, work_summary = build_pair_inventory(
            tokenizer, prompts, conditions, views, b1_by_key
        )
        prompt_text_by_id = {row["prompt_id"]: row["prompt"] for row in prompts}
        cache = ExactScoreCache(cache_dir)
        initial = {pair_id: cache.load(pair) for pair_id, pair in pair_by_id.items()}
        initial_hits = {pair_id: score is not None for pair_id, score in initial.items()}
        scores = {pair_id: float(score) for pair_id, score in initial.items() if score is not None}
        missing = [pair for pair_id, pair in pair_by_id.items() if pair_id not in scores]
        batches = exact_length_batches(missing, release["runtime"]["batch_size"])
        planned_tokens = sum(pair["pair_input_tokens"] for pair in missing)
        ceilings = release["ceilings"]
        require(len(missing) <= ceilings["maximum_new_cache_entries"], "New score-cache ceiling exceeded")
        require(len(missing) <= ceilings["maximum_model_input_instances"], "Model-input instance ceiling exceeded")
        require(planned_tokens <= ceilings["maximum_model_input_tokens"], "Model-token ceiling exceeded")
        require(len(batches) <= ceilings["maximum_model_forward_batches"], "Forward-batch ceiling exceeded")
        cache_dir.mkdir(parents=True, exist_ok=False)
        pair_forward_ms = {pair_id: 0.0 for pair_id in pair_by_id}
        forward_records: list[dict[str, Any]] = []
        forward_seconds = 0.0
        for batch_number, batch in enumerate(batches, 1):
            record_id = f"forward-{batch_number:06d}"
            runtime_batch = [
                {**pair, "query": prompt_text_by_id[pair["prompt_id"]]}
                for pair in batch
            ]
            started_path = attempt_dir / f"{record_id}.started.json"
            write_json_new(started_path, {
                "schema_version": "rq2b-v7-skillrouter-reranker-forward-start-v1",
                "record_id": record_id,
                "pair_ids": [pair["pair_id"] for pair in batch],
                "items": len(batch),
                "exact_pair_input_tokens": batch[0]["pair_input_tokens"],
                "padding": False,
                "device": "mps",
                "dtype": "bfloat16",
                "attention_implementation": "default_sdpa",
                "started_at_utc": utc_now(),
            })
            torch.mps.synchronize()
            batch_started = time.perf_counter()
            values = _score_exact_batch(torch, tokenizer, model, runtime_batch, yes[0], no[0])
            torch.mps.synchronize()
            elapsed = time.perf_counter() - batch_started
            forward_seconds += elapsed
            cache_artifacts: list[dict[str, Any]] = []
            for pair, score in zip(batch, values, strict=True):
                cache_path = cache.store(pair, score)
                scores[pair["pair_id"]] = score
                pair_forward_ms[pair["pair_id"]] = elapsed * 1000.0 / len(batch)
                cache_artifacts.append({
                    "pair_id": pair["pair_id"],
                    "cache_key": pair_cache_key(pair),
                    "path": relative(cache_path, root),
                    "sha256": file_sha256(cache_path),
                })
            completed_path = attempt_dir / f"{record_id}.completed.json"
            write_json_new(completed_path, {
                "schema_version": "rq2b-v7-skillrouter-reranker-forward-complete-v1",
                "record_id": record_id,
                "started_receipt_sha256": file_sha256(started_path),
                "items": len(batch),
                "model_input_tokens": sum(pair["pair_input_tokens"] for pair in batch),
                "elapsed_seconds": elapsed,
                "cache_artifacts": cache_artifacts,
                "completed_at_utc": utc_now(),
            })
            forward_records.append({
                "record_id": record_id,
                "started": {"path": relative(started_path, root), "sha256": file_sha256(started_path)},
                "completed": {"path": relative(completed_path, root), "sha256": file_sha256(completed_path)},
            })
            require(time.perf_counter() - wall_started <= ceilings["maximum_wall_time_seconds"], "Wall-time ceiling exceeded; no further forward allowed")
        require(set(scores) == set(pair_by_id), "Pair score coverage incomplete")
        require(all(cache.load(pair) == scores[pair_id] for pair_id, pair in pair_by_id.items()), "Final score-cache validation drift")

        rows: list[dict[str, Any]] = []
        tie_rows: list[dict[str, Any]] = []
        aggregation_seconds = 0.0
        for work in condition_work:
            condition = work["condition"]
            prompt = work["prompt"]
            aggregate_started = time.perf_counter()
            ranked, ties = rank_candidate_scores(work["candidates"], scores)
            aggregate_ms = (time.perf_counter() - aggregate_started) * 1000.0
            aggregation_seconds += aggregate_ms / 1000.0
            logical_pair_ids = [pair_id for candidate in work["candidates"] for pair_id in candidate["pair_ids"]]
            row = {
                "schema_version": B2_SCHEMA,
                "status": "SUCCESS",
                "run_id": release["run_id"],
                "condition_id": condition["condition_id"],
                "phase": condition["phase"],
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
                "representation": condition["representation"],
                "first_stage_retriever": condition["retriever"],
                "reranker": condition["reranker"],
                "persisted_candidate_source": condition["persisted_candidate_source"],
                "source_union_sha256": condition["source_union_sha256"],
                "input_top20_binding_sha256": work["input_top20_binding_sha256"],
                "reranker_input_sha256": reranker_input_sha256(
                    condition_id=condition["condition_id"],
                    prompt_id=prompt["prompt_id"],
                    prompt_sha256=prompt["prompt_sha256"],
                    input_top20_binding_sha256=work["input_top20_binding_sha256"],
                    input_candidates=work["input_candidates"],
                ),
                "score_semantics": "HIGHER_IS_BETTER",
                "input_candidates": work["input_candidates"],
                "reranked_candidates": ranked,
                "cost": {
                    "wall_time_ms": aggregate_ms + sum(pair_forward_ms[pair_id] for pair_id in logical_pair_ids),
                    "provider_calls": 0,
                    "input_tokens": sum(pair_by_id[pair_id]["pair_input_tokens"] for pair_id in logical_pair_ids),
                    "output_tokens": 0,
                    "window_forwards": len(logical_pair_ids),
                    "cache_hits": sum(initial_hits[pair_id] for pair_id in logical_pair_ids),
                    "retry_count": 0,
                    "timeout_count": 0,
                    "failure_count": 0,
                    "candidate_pairs": TOP_K,
                },
            }
            rows.append(row)
            for tie in ties:
                tie_rows.append({
                    "schema_version": "rq2b-v7-skillrouter-reranker-exact-tie-v1",
                    "condition_id": condition["condition_id"],
                    "prompt_id": prompt["prompt_id"],
                    **tie,
                    "tie_break": "source_sha256_ascending",
                })
        validate_b2_rows(rows, prompts)

        staging.mkdir(parents=True, exist_ok=False)
        b2_path = staging / "b2.jsonl.gz"
        b2_artifact = write_deterministic_jsonl_gzip(b2_path, rows)
        b2_artifact["path"] = relative(output_dir / b2_path.name, root)
        ties_path = staging / "exact_ties.jsonl.gz"
        ties_artifact = write_deterministic_jsonl_gzip(ties_path, tie_rows)
        ties_artifact["path"] = relative(output_dir / ties_path.name, root)
        cache_inventory_path = staging / "score_cache_inventory.jsonl.gz"
        cache_rows = []
        for pair_id, pair in sorted(pair_by_id.items()):
            path = cache.path(pair)
            cache_rows.append({
                "schema_version": "rq2b-v7-skillrouter-reranker-cache-inventory-row-v1",
                "pair_id": pair_id,
                "cache_key": pair_cache_key(pair),
                "representation": pair["representation"],
                "pair_input_tokens": pair["pair_input_tokens"],
                "initial_cache_hit": initial_hits[pair_id],
                "cache_path": relative(path, root),
                "cache_entry_sha256": file_sha256(path),
            })
        cache_artifact = write_deterministic_jsonl_gzip(cache_inventory_path, cache_rows)
        cache_artifact["path"] = relative(output_dir / cache_inventory_path.name, root)
        cpu_plan_path = staging / "cpu_fp32_sensitivity_plan.json"
        write_json_new(cpu_plan_path, cpu_sensitivity_plan(pair_by_id))
        cpu_pending_path = staging / "cpu_fp32_sensitivity_pending_receipt.json"
        write_json_new(cpu_pending_path, {
            "schema_version": "rq2b-v7-skillrouter-reranker-cpu-fp32-sensitivity-receipt-v1",
            "status": "PENDING_SEPARATE_EXPLICIT_AUTHORISATION_NOT_RUN",
            "plan": {"path": relative(output_dir / cpu_plan_path.name, root), "sha256": file_sha256(cpu_plan_path)},
            "primary_runtime": {"device": "mps", "dtype": "bfloat16", "attention_implementation": "default_sdpa"},
            "reference_runtime": {"device": "cpu", "dtype": "float32", "attention_implementation": "eager"},
            "model_loads": 0,
            "model_forwards": 0,
            "network_calls": 0,
        })
        attempt_index_path = attempt_dir / "attempt_index.json"
        write_json_new(attempt_index_path, {
            "schema_version": "rq2b-v7-skillrouter-reranker-attempt-index-v1",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "automatic_retries": 0,
            "forward_records": forward_records,
        })
        cost = {
            "schema_version": "rq2b-v7-skillrouter-reranker-b2-cost-ledger-v1",
            "unique_pairs": len(pair_by_id),
            "logical_candidate_occurrences": work_summary["candidate_occurrences"],
            "logical_window_occurrences": work_summary["window_occurrences"],
            "windowed_candidate_occurrences": work_summary["windowed_candidates"],
            "initial_cache_hits": sum(initial_hits.values()),
            "new_cache_entries": len(missing),
            "new_model_input_tokens": planned_tokens,
            "model_forward_batches": len(batches),
            "model_load_seconds": model_load_seconds,
            "model_forward_seconds": forward_seconds,
            "aggregation_seconds": aggregation_seconds,
            "wall_time_seconds": time.perf_counter() - wall_started,
            "provider_calls": 0,
            "network_calls": 0,
            "automatic_retries": 0,
            "timeout_count": 0,
            "failure_count": 0,
            "monetary_cost_usd": 0.0,
        }
        cost_path = staging / "cost_ledger.json"
        write_json_new(cost_path, cost)
        receipt = {
            "schema_version": "rq2b-v7-skillrouter-reranker-b2-run-receipt-v1",
            "status": "COMPLETE_15_MATERIALISED_SKILLROUTER_B2_CONDITIONS",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "root_release_id": release["root_release_id"],
            "runner": {"version": RUNNER_VERSION, "path": relative(Path(__file__), root), "sha256": file_sha256(Path(__file__))},
            "payload": {"path": relative(payload_path, root), "sha256": file_sha256(payload_path)},
            "authorisation": {"path": relative(authorisation_path, root), "sha256": file_sha256(authorisation_path)},
            "method": method_contract(),
            "runtime": release["runtime"],
            "scope": {
                "materialised_conditions": list(MATERIALISED_CONDITIONS),
                "rows": len(rows),
                "c2_s_alias": {"materialised": False, "exact_alias_of": "B05-GS"},
            },
            "ties": {"exact_tie_groups": len(tie_rows), "preserved_scores": True, "tie_break": "source_sha256_ascending"},
            "cpu_fp32_sensitivity": {
                "status": "PENDING_SEPARATE_EXPLICIT_AUTHORISATION_NOT_RUN",
                "plan": {"path": relative(output_dir / cpu_plan_path.name, root), "sha256": file_sha256(cpu_plan_path)},
                "pending_receipt": {"path": relative(output_dir / cpu_pending_path.name, root), "sha256": file_sha256(cpu_pending_path)},
            },
            "attempt_receipts": {
                "run_started": {"path": relative(run_started, root), "sha256": file_sha256(run_started)},
                "attempt_index": {"path": relative(attempt_index_path, root), "sha256": file_sha256(attempt_index_path)},
            },
            "cost": cost,
            "artifacts": {
                "b2": b2_artifact,
                "exact_ties": ties_artifact,
                "score_cache_inventory": cache_artifact,
                "cost_ledger": {"path": relative(output_dir / cost_path.name, root), "sha256": file_sha256(cost_path)},
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
        manifest_path = staging / "manifest.json"
        write_json_new(manifest_path, {
            "schema_version": "rq2b-v7-skillrouter-reranker-b2-output-manifest-v1",
            "status": receipt["status"],
            "run_receipt": {"path": relative(output_dir / receipt_path.name, root), "sha256": file_sha256(receipt_path)},
            "b2": b2_artifact,
            "exact_ties": ties_artifact,
            "score_cache_inventory": cache_artifact,
        })
        staging.replace(output_dir)
        write_json_new(attempt_dir / "run_completed.json", {
            "schema_version": "rq2b-v7-skillrouter-reranker-b2-run-complete-v1",
            "run_id": release["run_id"],
            "attempt_id": release["attempt_id"],
            "output_manifest": {"path": relative(output_dir / "manifest.json", root), "sha256": file_sha256(output_dir / "manifest.json")},
            "completed_at_utc": utc_now(),
        })
        return receipt
    except Exception as error:
        if attempt_dir.is_dir() and not (attempt_dir / "run_failed.json").exists():
            write_json_new(attempt_dir / "run_failed.json", {
                "schema_version": "rq2b-v7-skillrouter-reranker-b2-run-failed-v1",
                "run_id": release["run_id"],
                "attempt_id": release["attempt_id"],
                "automatic_retries": 0,
                "failure_type": type(error).__name__,
                "failure_message": str(error),
                "model_load_seconds_before_failure": model_load_seconds,
                "failed_at_utc": utc_now(),
            })
        raise


def self_test() -> dict[str, Any]:
    candidates = [
        {"source_sha256": "2" * 64, "input_rank": 1, "pair_ids": ["p1", "p2"]},
        {"source_sha256": "1" * 64, "input_rank": 2, "pair_ids": ["p3"]},
    ]
    ranked, ties = rank_candidate_scores(candidates, {"p1": -1.0, "p2": 0.5, "p3": 0.5})
    require([row["source_sha256"] for row in ranked] == ["1" * 64, "2" * 64], "Maximum-window/SHA-tie self-test failed")
    require(len(ties) == 1 and ties[0]["score"] == 0.5, "Exact-tie preservation self-test failed")
    batches = exact_length_batches([
        {"pair_id": f"p{index:02d}", "pair_input_tokens": 9 if index < 17 else 11}
        for index in range(20)
    ], 16)
    require([len(batch) for batch in batches] == [16, 1, 3], "Exact-length batch self-test failed")
    return {
        "status": "PASS_SYNTHETIC_NO_MODEL_LOAD_NO_FORWARD_NO_NETWORK",
        "network_calls": 0,
        "model_loads": 0,
        "model_forwards": 0,
        "checks": {
            "maximum_window_aggregation": True,
            "exact_ties_preserved": True,
            "source_sha256_tie_break": True,
            "exact_length_no_padding_batches": True,
            "c2_s_not_materialised": "C2-S" not in MATERIALISED_CONDITIONS,
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
