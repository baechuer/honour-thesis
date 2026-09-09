#!/usr/bin/env python3
"""Build the Phase-8-compatible V7 Qwen B1 payload with zero network work.

The preflight accepts only a final Phase-8 readiness receipt/root.  I1/I2 are
pinned to the authoritative 2026-09-09 V2 views; I3C/I3-flat are taken only
from the final V4.1 bindings inside that Phase-8 root.  Missing or stale final
bindings fail closed.  No embedding or provider function is called here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
from pathlib import Path
from typing import Any, Iterable

from rq2b_chunking import tokenizer_ids
from rq2b_v7_exact_chunking_v2 import CHUNKER_VERSION, exact_text_chunks
from run_rq2b_qwen import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL


BUILDER_VERSION = "rq2b-v7-qwen-b1-phase8-preflight-builder-v3"
RUNNER_VERSION = "rq2b-v7-qwen-b1-phase8-runner-v3"
PAYLOAD_SCHEMA = "rq2b-v7-qwen-b1-phase8-payload-v3"
AUTHORISATION_SCHEMA = "rq2b-v7-qwen-b1-phase8-root-release-v3"
PREFLIGHT_SCHEMA = "rq2b-v7-qwen-b1-phase8-preflight-receipt-v3"
PHASE8_ROOT_SCHEMA = "rq2b-v7-phase8-final-execution-root-v1"
PHASE8_RECEIPT_SCHEMA = "rq2b-v7-phase8-readiness-receipt-v1"
PHASE8_READY = "READY_FOR_FORMAL_EXPERIMENT"

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
FIXED_SHA256 = {
    RUNTIME_REL: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    SOURCE_REL: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    CONDITIONS_REL: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
}
I1_I2_BINDINGS = {
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
PHASE8_I3_ROLES = {
    "I3C-fielded": "i3c_fielded",
    "I3-flat": "i3_flat",
}
REPRESENTATION_CELLS = {
    "I1-discovery": "B02",
    "I2-original": "B05",
    "I3C-fielded": "B08",
    "I3-flat": "B11",
}
SKILLROUTER_CELLS = {"B03", "B06", "B09", "B12"}
EXPECTED_QUERIES = 1077
EXPECTED_SOURCES = 3798
EXPECTED_ROWS = 4 * EXPECTED_QUERIES
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
TOKENIZER_REL = Path(
    "skill_benchmark/cache/huggingface/"
    "SkillRouter-Embedding-0.6B-c03c9bcee9fc"
)
TOKENIZER_JSON_SHA256 = "def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a"
TOKENIZER_MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
TOKENIZER_REVISION = "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
CHUNK_TOKENS = 7500
OVERLAP_TOKENS = 256
TOP_K = 100
QUERY_PROVIDER_LIMIT = 8192
DEFAULT_TIMEOUT_SECONDS = 120
CLEAN_CACHE_REL = Path("skill_benchmark/cache/rq2b_v7_qwen_b1_phase8_v3/embeddings")
RUNNER_REL = Path("skill_benchmark/scripts/run_rq2b_v7_qwen_b1_phase8_v3.py")
BUILDER_REL = Path("skill_benchmark/scripts/build_rq2b_v7_qwen_b1_phase8_v3_preflight.py")
CHUNKER_REL = Path("skill_benchmark/scripts/rq2b_v7_exact_chunking_v2.py")
PROVIDER_CONTRACT_REL = Path("skill_benchmark/scripts/run_rq2b_qwen.py")
VALIDATOR_REL = Path("skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py")
TEST_REL = Path("skill_benchmark/scripts/test_rq2b_v7_qwen_b1_phase8_v3.py")
HEX = set("0123456789abcdef")
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}
PREDICTABLE_CEILING_KEYS = {
    "maximum_new_cache_entries",
    "maximum_new_cache_content_proxy_tokens",
    "maximum_new_cache_model_input_proxy_tokens",
    "maximum_new_cache_utf8_bytes",
    "maximum_external_text_submissions",
    "maximum_external_content_proxy_tokens",
    "maximum_external_model_input_proxy_tokens",
    "maximum_external_text_utf8_bytes",
    "maximum_external_request_body_utf8_bytes",
    "cold_query_requests",
    "maximum_request_attempts",
    "maximum_successful_calls",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def exact_keys(value: Any, keys: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: object required")
    missing = keys - set(value)
    extra = set(value) - keys
    require(not missing and not extra, f"{field}: missing={sorted(missing)} extra={sorted(extra)}")


def root_path(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: non-empty path required")
    raw = Path(value)
    require(not raw.is_absolute(), f"{field}: absolute path forbidden")
    path = (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path}: JSON object required")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
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


def write_jsonl_new(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def normalized_key_tokens(key: str) -> set[str]:
    normalized = key.lower().replace("-", "_").replace(" ", "_")
    tokens = set(normalized.split("_")) | {normalized}
    for phrase in ("ground_truth", "a_q", "j_q", "d_q"):
        if phrase in normalized:
            tokens.add(phrase)
    return tokens


def reject_outcome_keys(value: Any, location: str) -> None:
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


def validate_bound_file(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, dict) and "path" in value and "sha256" in value, f"{field}: path/SHA binding required")
    require(is_sha256(value["sha256"]), f"{field}: invalid SHA-256")
    path = root_path(root, value["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: file missing")
    require(file_sha256(path) == value["sha256"], f"{field}: file hash drift")
    return path


def validate_qwen_condition_mapping(selected: dict[str, dict[str, Any]]) -> None:
    """Reject a common but scientifically material Qwen/SkillRouter cell swap."""
    expected = set(REPRESENTATION_CELLS.values())
    observed = set(selected)
    require(not (observed & SKILLROUTER_CELLS), "Qwen B1 cannot bind SkillRouter cells B03/B06/B09/B12")
    require(observed == expected, f"Qwen B1 condition set drift: {sorted(observed)} != {sorted(expected)}")
    for representation, cell in REPRESENTATION_CELLS.items():
        row = selected[cell]
        require(row.get("condition_id") == f"{cell}-G0", f"{cell}: condition identity drift")
        require(row.get("representation") == representation, f"{cell}: representation drift")
        require(row.get("retriever") == "Qwen-text-embedding-v4", f"{cell}: retriever drift")
        require(row.get("persisted_candidate_source") == cell, f"{cell}: persisted source drift")


def validate_representation_manifest_bindings(
    representations: Any, expected: dict[str, dict[str, str]],
) -> None:
    require(isinstance(representations, dict), "Payload representations must be an object")
    require(set(representations) == set(REPRESENTATION_CELLS), "Payload representation set drift")
    for representation, binding in expected.items():
        item = representations[representation]
        require(
            item.get("path") == binding["path"] and item.get("sha256") == binding["sha256"],
            f"{representation}: stale or non-Phase8 representation binding rejected",
        )
        expected_provenance = (
            "AUTHORITATIVE_2026_09_09_V2"
            if representation in I1_I2_BINDINGS else "FINAL_PHASE8_V4_1"
        )
        require(item.get("provenance") == expected_provenance, f"{representation}: provenance drift")
        require(item.get("rows") == EXPECTED_SOURCES, f"{representation}: row-count drift")


def phase8_bindings(root: Path, receipt_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, str]]]:
    try:
        receipt_path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Phase-8 receipt must be inside repository root") from error
    receipt = read_json(receipt_path)
    require(receipt.get("schema_version") == PHASE8_RECEIPT_SCHEMA, "Phase-8 receipt schema drift")
    require(
        receipt.get("status") == "PASS_PHASE8_ROOT_READY_PENDING_EXPLICIT_PER_RUN_AUTHORISATION",
        "Phase-8 receipt is not final PASS",
    )
    require(receipt.get("execution_authorised") is False, "Phase-8 readiness unexpectedly authorises execution")
    root_binding = receipt.get("root_manifest")
    root_manifest_path = validate_bound_file(root, root_binding, field="phase8.root_manifest")
    root_manifest = read_json(root_manifest_path)
    require(root_manifest.get("schema_version") == PHASE8_ROOT_SCHEMA, "Phase-8 root schema drift")
    require(root_manifest.get("status") == PHASE8_READY, "Phase-8 root is not READY")
    require(root_manifest.get("execution_authorised") is False, "Phase-8 root unexpectedly authorises execution")
    scope = root_manifest.get("scope", {})
    require(
        scope.get("queries") == EXPECTED_QUERIES
        and scope.get("sources") == EXPECTED_SOURCES
        and scope.get("source_union_sha256") == SOURCE_UNION_SHA256,
        "Phase-8 root scope drift",
    )
    runner = root_manifest.get("runners", {}).get("qwen_embedding_b1")
    require(isinstance(runner, dict), "Phase-8 root lacks qwen_embedding_b1 runner")
    require(
        runner.get("path") == RUNNER_REL.as_posix()
        and runner.get("runner_version") == RUNNER_VERSION
        and runner.get("payload_schema") == PAYLOAD_SCHEMA
        and runner.get("authorisation_schema") == AUTHORISATION_SCHEMA,
        "Phase-8 root Qwen B1 runner/schema binding drift",
    )
    runner_path = root / RUNNER_REL
    require(runner_path.is_file() and runner.get("sha256") == file_sha256(runner_path), "Phase-8 root Qwen B1 runner hash drift")

    representations: dict[str, dict[str, str]] = {}
    fixed = root_manifest.get("fixed_artifacts", {})
    for representation, expected in I1_I2_BINDINGS.items():
        role = "i1_discovery_v2" if representation == "I1-discovery" else "i2_original_v2"
        item = fixed.get(role)
        require(isinstance(item, dict), f"Phase-8 root lacks {role}")
        require(item.get("path") == expected["path"] and item.get("sha256") == expected["sha256"], f"{representation}: old/non-authoritative V2 binding rejected")
        validate_bound_file(root, item, field=f"phase8.fixed_artifacts.{role}")
        representations[representation] = dict(expected)
    dynamic = root_manifest.get("final_phase7_artifacts", {})
    for representation, role in PHASE8_I3_ROLES.items():
        item = dynamic.get(role)
        require(isinstance(item, dict), f"Phase-8 root lacks final {role}")
        path = validate_bound_file(root, item, field=f"phase8.final_phase7_artifacts.{role}")
        require("2026_09_09_v4_1" in relative(path, root), f"{representation}: final V4.1 path binding missing")
        representations[representation] = {"path": relative(path, root), "sha256": item["sha256"]}
    return receipt, root_manifest, representations


def verify_fixed_authority(root: Path) -> None:
    for rel_path, expected in FIXED_SHA256.items():
        path = root / rel_path
        require(path.is_file(), f"Frozen authority missing: {rel_path}")
        require(file_sha256(path) == expected, f"Frozen authority hash drift: {rel_path}")
    tokenizer_json = root / TOKENIZER_REL / "tokenizer.json"
    require(tokenizer_json.is_file(), "Pinned proxy tokenizer missing")
    require(file_sha256(tokenizer_json) == TOKENIZER_JSON_SHA256, "Pinned proxy tokenizer hash drift")


def load_authority(
    root: Path, representation_bindings: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], set[str], dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    verify_fixed_authority(root)
    prompts = read_jsonl(root / RUNTIME_REL)
    require(len(prompts) == EXPECTED_QUERIES, "Expected 1,077 frozen queries")
    for index, row in enumerate(prompts):
        reject_outcome_keys(row, f"runtime[{index}]")
        exact_keys(row, {"schema_version", "prompt_id", "prompt", "prompt_sha256"}, f"runtime[{index}]")
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", "Runtime schema drift")
        require(row["prompt_sha256"] == text_sha256(row["prompt"]), "Runtime prompt hash drift")
    require(len({row["prompt_id"] for row in prompts}) == EXPECTED_QUERIES, "Duplicate prompt IDs")

    source_rows = read_jsonl(root / SOURCE_REL)
    source_ids = {str(row.get("sha256")) for row in source_rows}
    require(len(source_rows) == len(source_ids) == EXPECTED_SOURCES, "Source identity/coverage drift")
    require(all(is_sha256(value) for value in source_ids), "Invalid source SHA")

    conditions = read_jsonl(root / CONDITIONS_REL)
    selected = {
        row["persisted_candidate_source"]: row
        for row in conditions
        if row.get("reranker") == "NONE" and row.get("retriever") == "Qwen-text-embedding-v4"
    }
    validate_qwen_condition_mapping(selected)
    for representation, cell in REPRESENTATION_CELLS.items():
        condition = selected[cell]
        reject_outcome_keys(condition, f"condition.{cell}")
        require(condition["condition_id"] == f"{cell}-G0", f"{cell}: condition identity drift")
        require(condition["representation"] == representation, f"{cell}: representation drift")
        require(condition["source_union_sha256"] == SOURCE_UNION_SHA256, f"{cell}: source union drift")
        require(condition["query_count"] == EXPECTED_QUERIES, f"{cell}: query-count drift")
        require(condition["execution_authorised"] is False, f"{cell}: authority unexpectedly authorises execution")

    representations: dict[str, list[dict[str, Any]]] = {}
    require(set(representation_bindings) == set(REPRESENTATION_CELLS), "Representation binding set drift")
    for representation, binding in representation_bindings.items():
        path = validate_bound_file(root, binding, field=f"representations.{representation}")
        rows = read_jsonl(path)
        require(len(rows) == EXPECTED_SOURCES, f"{representation}: row-count drift")
        seen: set[str] = set()
        for index, row in enumerate(rows):
            reject_outcome_keys(row, f"{representation}[{index}]")
            source = row.get("source_sha256")
            text = row.get("selector_text")
            require(source in source_ids and source not in seen, f"{representation}: source identity/duplicate drift")
            seen.add(source)
            require(row.get("representation") == representation, f"{representation}: row tag drift")
            require(isinstance(text, str) and text and row.get("selector_text_sha256") == text_sha256(text), f"{representation}: selector bytes/hash drift")
        require(seen == source_ids, f"{representation}: exact source coverage drift")
        representations[representation] = rows
    return prompts, source_ids, selected, representations


def content_and_model_proxy_tokens(tokenizer: Any, text: str) -> tuple[int, int]:
    content = len(tokenizer.encode(text, add_special_tokens=False))
    model_input = len(tokenizer.encode(text, add_special_tokens=True))
    require(model_input >= content > 0, "Proxy tokenizer returned invalid content/model-input counts")
    return content, model_input


def register_text(
    inventory: dict[str, dict[str, Any]], *, text: str,
    content_proxy_tokens: int, model_input_proxy_tokens: int,
    role: dict[str, Any],
) -> str:
    text_id = text_sha256(text)
    existing = inventory.get(text_id)
    if existing is None:
        inventory[text_id] = {
            "schema_version": "rq2b-v7-qwen-b1-phase8-text-v3",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "content_proxy_tokens": content_proxy_tokens,
            "model_input_proxy_tokens": model_input_proxy_tokens,
            "special_token_proxy_tokens": model_input_proxy_tokens - content_proxy_tokens,
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "SHA-256 collision in text inventory")
        require(existing["content_proxy_tokens"] == content_proxy_tokens, "Content proxy-token drift")
        require(existing["model_input_proxy_tokens"] == model_input_proxy_tokens, "Model-input proxy-token drift")
        existing["roles"].append(role)
    return text_id


def build_payload_data(
    tokenizer: Any,
    prompts: list[dict[str, Any]],
    representations: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str], dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    documents: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, Any]] = {}
    for representation in REPRESENTATION_CELLS:
        document_windows = 0
        windowed_documents = 0
        maximum_content = 0
        maximum_model_input = 0
        maximum_overlap = 0
        short_direct_advances = 0
        for source_index, row in enumerate(representations[representation]):
            content_count, model_count = content_and_model_proxy_tokens(tokenizer, row["selector_text"])
            maximum_content = max(maximum_content, content_count)
            maximum_model_input = max(maximum_model_input, model_count)
            chunks = exact_text_chunks(
                tokenizer,
                row["selector_text"],
                maximum_tokens=CHUNK_TOKENS,
                overlap_tokens=OVERLAP_TOKENS,
            )
            if len(chunks) > 1:
                windowed_documents += 1
            chunk_ids: list[str] = []
            metadata: list[dict[str, Any]] = []
            for previous, current in zip(chunks, chunks[1:]):
                overlap = len(tokenizer_ids(
                    tokenizer,
                    row["selector_text"][current.start_char:previous.end_char],
                ))
                maximum_overlap = max(maximum_overlap, overlap)
                require(overlap <= OVERLAP_TOKENS, "V2 chunk overlap ceiling drift")
                if previous.token_count <= OVERLAP_TOKENS:
                    require(current.start_char == previous.end_char, "V2 short-boundary progress drift")
                    short_direct_advances += 1
            for chunk in chunks:
                chunk_content, chunk_model = content_and_model_proxy_tokens(tokenizer, chunk.text)
                require(chunk_content == chunk.token_count <= CHUNK_TOKENS, "Chunk token-count drift")
                chunk_ids.append(register_text(
                    inventory,
                    text=chunk.text,
                    content_proxy_tokens=chunk_content,
                    model_input_proxy_tokens=chunk_model,
                    role={
                        "kind": "document_chunk",
                        "representation": representation,
                        "first_stage_cell_id": REPRESENTATION_CELLS[representation],
                        "source_sha256": row["source_sha256"],
                        "chunk_index": chunk.chunk_index,
                    },
                ))
                metadata.append({
                    "chunk_index": chunk.chunk_index,
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char,
                    "content_proxy_tokens": chunk_content,
                    "model_input_proxy_tokens": chunk_model,
                    "special_token_proxy_tokens": chunk_model - chunk_content,
                    "text_sha256": chunk.text_sha256,
                    "token_ids_sha256": chunk.token_ids_sha256,
                    "ended_at_preferred_boundary": chunk.ended_at_preferred_boundary,
                })
            documents.append({
                "schema_version": "rq2b-v7-qwen-b1-phase8-document-map-v3",
                "representation": representation,
                "first_stage_cell_id": REPRESENTATION_CELLS[representation],
                "source_row_index": source_index,
                "source_sha256": row["source_sha256"],
                "selector_text_sha256": row["selector_text_sha256"],
                "selector_content_proxy_tokens": content_count,
                "selector_model_input_proxy_tokens": model_count,
                "chunk_text_ids": chunk_ids,
                "chunks": metadata,
            })
            document_windows += len(chunks)
        summaries[representation] = {
            "first_stage_cell_id": REPRESENTATION_CELLS[representation],
            "documents": len(representations[representation]),
            "document_windows": document_windows,
            "windowed_documents": windowed_documents,
            "maximum_source_content_proxy_tokens": maximum_content,
            "maximum_source_model_input_proxy_tokens": maximum_model_input,
            "maximum_adjacent_overlap_content_proxy_tokens": maximum_overlap,
            "short_boundary_direct_advances": short_direct_advances,
        }
    query_text_ids: dict[str, str] = {}
    for prompt in prompts:
        content_count, model_count = content_and_model_proxy_tokens(tokenizer, prompt["prompt"])
        require(model_count <= QUERY_PROVIDER_LIMIT, f"Query exceeds frozen model-input proxy limit: {prompt['prompt_id']}")
        query_text_ids[prompt["prompt_id"]] = register_text(
            inventory,
            text=prompt["prompt"],
            content_proxy_tokens=content_count,
            model_input_proxy_tokens=model_count,
            role={
                "kind": "query",
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
            },
        )
    text_rows = [inventory[text_id] for text_id in sorted(inventory)]
    documents.sort(key=lambda row: (row["representation"], row["source_sha256"]))
    return text_rows, documents, query_text_ids, summaries


def cache_key(text: str) -> str:
    return canonical_sha256({
        "schema_version": "rq2b-v7-qwen-b1-phase8-cache-key-v3",
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "chunker_version": CHUNKER_VERSION,
        "text_sha256": text_sha256(text),
    })


class V3ExactEmbeddingCache:
    """Exact V3 cache; preflight reads without creating and runner writes new only."""

    def __init__(self, root: Path, *, create: bool = False) -> None:
        self.root = root / "qwen" / MODEL / str(DIMENSIONS)
        if create:
            self.root.mkdir(parents=True, exist_ok=True)

    def path(self, text: str) -> Path:
        return self.root / f"{cache_key(text)}.json"

    def load(self, text: str) -> list[float] | None:
        path = self.path(text)
        if not path.is_file():
            return None
        value = read_json(path)
        require(value.get("schema_version") == "rq2b-v7-qwen-embedding-cache-v3", f"Cache schema drift: {path}")
        require(value.get("base_url") == BASE_URL and value.get("model") == MODEL, f"Cache provider/model drift: {path}")
        require(value.get("dimensions") == DIMENSIONS, f"Cache dimension drift: {path}")
        require(value.get("chunker_version") == CHUNKER_VERSION, f"Cache chunker drift: {path}")
        require(value.get("text_sha256") == text_sha256(text), f"Cache text drift: {path}")
        vector = [float(item) for item in value.get("embedding", [])]
        require(len(vector) == DIMENSIONS, f"Cache vector dimension drift: {path}")
        require(all(math.isfinite(item) for item in vector), f"Cache vector non-finite: {path}")
        return vector

    def store(
        self, text: str, vector: list[float], *,
        content_proxy_tokens: int, model_input_proxy_tokens: int,
        provider_usage: dict[str, Any],
    ) -> Path:
        require(len(vector) == DIMENSIONS and all(math.isfinite(item) for item in vector), "Invalid cache vector")
        path = self.path(text)
        require(not path.exists(), f"Refusing to overwrite V3 exact cache entry: {path}")
        write_json_new(path, {
            "schema_version": "rq2b-v7-qwen-embedding-cache-v3",
            "base_url": BASE_URL,
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "chunker_version": CHUNKER_VERSION,
            "text_sha256": text_sha256(text),
            "content_proxy_tokens": content_proxy_tokens,
            "model_input_proxy_tokens": model_input_proxy_tokens,
            "provider_usage": provider_usage,
            "embedding": vector,
        })
        return path


def embedding_request_payload(texts: list[str]) -> dict[str, Any]:
    require(1 <= len(texts) <= MAX_BATCH_TEXTS, "Embedding request must contain 1..10 texts")
    return {
        "model": MODEL,
        "input": texts,
        "dimensions": DIMENSIONS,
        "encoding_format": "float",
    }


def embedding_request_bytes(texts: list[str]) -> bytes:
    return json.dumps(
        embedding_request_payload(texts),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def has_role(row: dict[str, Any], kind: str) -> bool:
    return any(role.get("kind") == kind for role in row["roles"])


def cache_inventory_and_counts(
    text_rows: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
    query_text_ids: dict[str, str],
    cache: V3ExactEmbeddingCache,
) -> tuple[list[dict[str, Any]], dict[str, int], list[list[str]]]:
    by_id = {row["text_id"]: row for row in text_rows}
    require(len(by_id) == len(text_rows), "Duplicate text IDs")
    require(set(query_text_ids) == {row["prompt_id"] for row in prompts}, "Query-text map coverage drift")
    require(len(set(query_text_ids.values())) == EXPECTED_QUERIES, "Cold-query contract requires 1,077 unique query texts")
    inventory: list[dict[str, Any]] = []
    available: dict[str, bool] = {}
    for row in text_rows:
        path = cache.path(row["text"])
        hit = path.is_file()
        if hit:
            require(cache.load(row["text"]) is not None, f"Invalid V3 cache hit: {path}")
        available[row["text_id"]] = hit
        inventory.append({
            "schema_version": "rq2b-v7-qwen-b1-phase8-cache-inventory-v3",
            "text_id": row["text_id"],
            "cache_key": cache_key(row["text"]),
            "role_kinds": sorted({role["kind"] for role in row["roles"]}),
            "content_proxy_tokens": row["content_proxy_tokens"],
            "model_input_proxy_tokens": row["model_input_proxy_tokens"],
            "special_token_proxy_tokens": row["special_token_proxy_tokens"],
            "utf8_bytes": row["utf8_bytes"],
            "cache_hit": hit,
            "cache_entry_sha256": file_sha256(path) if hit else None,
        })
    document_rows = [row for row in text_rows if has_role(row, "document_chunk")]
    query_rows = [by_id[query_text_ids[prompt["prompt_id"]]] for prompt in prompts]
    document_misses = [row for row in document_rows if not available[row["text_id"]]]
    all_misses = [row for row in text_rows if not available[row["text_id"]]]
    planned_batches = [
        [row["text_id"] for row in document_misses[start:start + MAX_BATCH_TEXTS]]
        for start in range(0, len(document_misses), MAX_BATCH_TEXTS)
    ] + [[row["text_id"]] for row in query_rows]
    external_rows = [*document_misses, *query_rows]
    request_body_bytes = sum(
        len(embedding_request_bytes([by_id[text_id]["text"] for text_id in batch]))
        for batch in planned_batches
    )
    counts = {
        "unique_texts": len(text_rows),
        "unique_document_texts": len(document_rows),
        "unique_query_texts": len(query_rows),
        "cache_hits": len(text_rows) - len(all_misses),
        "cache_misses": len(all_misses),
        "document_cache_hits": len(document_rows) - len(document_misses),
        "document_cache_misses": len(document_misses),
        "query_cache_entries_preexisting": sum(available[row["text_id"]] for row in query_rows),
        "query_cache_entry_misses": sum(not available[row["text_id"]] for row in query_rows),
        "maximum_new_cache_entries": len(all_misses),
        "maximum_new_cache_content_proxy_tokens": sum(row["content_proxy_tokens"] for row in all_misses),
        "maximum_new_cache_model_input_proxy_tokens": sum(row["model_input_proxy_tokens"] for row in all_misses),
        "maximum_new_cache_utf8_bytes": sum(row["utf8_bytes"] for row in all_misses),
        "maximum_external_text_submissions": len(external_rows),
        "maximum_external_content_proxy_tokens": sum(row["content_proxy_tokens"] for row in external_rows),
        "maximum_external_model_input_proxy_tokens": sum(row["model_input_proxy_tokens"] for row in external_rows),
        "maximum_external_text_utf8_bytes": sum(row["utf8_bytes"] for row in external_rows),
        "maximum_external_request_body_utf8_bytes": request_body_bytes,
        "cold_query_requests": len(query_rows),
        "maximum_request_attempts": len(planned_batches),
        "maximum_successful_calls": len(planned_batches),
    }
    return inventory, counts, planned_batches


def predictable_ceilings(counts: dict[str, int]) -> dict[str, int]:
    return {key: counts[key] for key in sorted(PREDICTABLE_CEILING_KEYS)}


def implementation_bindings(root: Path) -> dict[str, dict[str, str]]:
    files = {
        "builder": BUILDER_REL,
        "runner": RUNNER_REL,
        "chunker_v2": CHUNKER_REL,
        "provider_cache_contract": PROVIDER_CONTRACT_REL,
        "official_validator": VALIDATOR_REL,
        "focused_tests": TEST_REL,
    }
    result: dict[str, dict[str, str]] = {}
    for name, rel_path in files.items():
        path = root / rel_path
        require(path.is_file(), f"Implementation missing: {rel_path}")
        result[name] = {"path": rel_path.as_posix(), "sha256": file_sha256(path)}
    return result


def artifact_binding(staging: Path, final: Path, root: Path, *, rows: int) -> dict[str, Any]:
    return {
        "path": relative(final, root),
        "sha256": file_sha256(staging),
        "rows": rows,
        "utf8_bytes": staging.stat().st_size,
    }


def validate_payload(root: Path, manifest_path: Path) -> dict[str, Any]:
    verify_fixed_authority(root)
    payload = read_json(manifest_path)
    require(payload.get("schema_version") == PAYLOAD_SCHEMA, "Payload schema drift")
    require(payload.get("state") == "SEALED_PHASE8_LABEL_FREE_NOT_AUTHORISED", "Payload state drift")
    require(payload.get("runner_version") == RUNNER_VERSION, "Payload runner version drift")
    require(payload.get("builder_version") == BUILDER_VERSION, "Payload builder version drift")
    reject_outcome_keys(payload, "payload")
    require(payload.get("network_calls") == 0 and payload.get("embedding_calls") == 0, "Payload observed external/model work")
    require(payload.get("model") == MODEL and payload.get("base_url") == BASE_URL, "Payload provider/model drift")
    require(payload.get("dimensions") == DIMENSIONS, "Payload dimensions drift")
    require(payload.get("chunker_version") == CHUNKER_VERSION, "Payload chunker drift")
    require(payload.get("chunk_tokens") == CHUNK_TOKENS and payload.get("overlap_tokens") == OVERLAP_TOKENS, "Payload window-method drift")
    require(payload.get("primary_aggregation") == "maximum_window_cosine", "Payload primary aggregation drift")
    require(payload.get("sensitivity_aggregation") == "cosine_of_l2_normalized_window_mean", "Payload sensitivity aggregation drift")
    require(payload.get("stable_tie_break") == "source_sha256_ascending", "Payload tie-break drift")
    require(payload.get("top_k") == TOP_K, "Payload Top-K drift")
    require(payload.get("conditions") == {
        representation: f"{cell}-G0" for representation, cell in REPRESENTATION_CELLS.items()
    }, "Payload condition scope drift")
    condition_rows = read_jsonl(root / CONDITIONS_REL)
    expected_condition_authority = {
        row["persisted_candidate_source"]: {
            "condition_id": row["condition_id"],
            "representation": row["representation"],
            "retriever": row["retriever"],
            "persisted_candidate_source": row["persisted_candidate_source"],
            "source_union_sha256": row["source_union_sha256"],
        }
        for row in condition_rows
        if row.get("reranker") == "NONE" and row.get("retriever") == "Qwen-text-embedding-v4"
    }
    validate_qwen_condition_mapping({
        cell: next(
            row for row in condition_rows
            if row.get("condition_id") == value["condition_id"]
        )
        for cell, value in expected_condition_authority.items()
    })
    require(payload.get("condition_authority") == expected_condition_authority, "Payload condition authority drift")
    phase8 = payload.get("phase8", {})
    receipt_path = validate_bound_file(root, phase8.get("receipt"), field="payload.phase8.receipt")
    root_manifest_path = validate_bound_file(root, phase8.get("root_manifest"), field="payload.phase8.root_manifest")
    receipt, root_manifest, expected_representations = phase8_bindings(root, receipt_path)
    require(file_sha256(root_manifest_path) == phase8["root_manifest"]["sha256"], "Payload Phase-8 root drift")
    require(root_manifest.get("package_id") == phase8.get("package_id"), "Payload Phase-8 package drift")
    representations = payload.get("representations")
    validate_representation_manifest_bindings(representations, expected_representations)
    for representation, expected in expected_representations.items():
        item = representations[representation]
        validate_bound_file(root, item, field=f"payload.representations.{representation}")
    for rel_path, expected_sha in FIXED_SHA256.items():
        item = payload.get("fixed_inputs", {}).get(rel_path.as_posix())
        require(item == {"sha256": expected_sha, "rows": EXPECTED_QUERIES if rel_path == RUNTIME_REL else 36 if rel_path == CONDITIONS_REL else EXPECTED_SOURCES}, f"Fixed input binding drift: {rel_path}")
    require(payload.get("tokenizer") == {
        "path": TOKENIZER_REL.as_posix(),
        "model": TOKENIZER_MODEL,
        "revision": TOKENIZER_REVISION,
        "tokenizer_json_sha256": TOKENIZER_JSON_SHA256,
    }, "Payload tokenizer binding drift")
    expected_implementation = {"builder", "runner", "chunker_v2", "provider_cache_contract", "official_validator", "focused_tests"}
    require(set(payload.get("implementation", {})) == expected_implementation, "Payload implementation binding set drift")
    for name, binding in payload["implementation"].items():
        validate_bound_file(root, binding, field=f"payload.implementation.{name}")
    artifacts = payload.get("artifacts", {})
    for name in ("text_inventory", "document_map", "cache_inventory", "planned_requests"):
        item = artifacts.get(name)
        path = validate_bound_file(root, item, field=f"payload.artifacts.{name}")
        require(path.stat().st_size == item["utf8_bytes"], f"Payload artifact byte-size drift: {name}")
        require(len(read_jsonl(path)) == item["rows"], f"Payload artifact row-count drift: {name}")
    require(payload.get("counts", {}).get("queries") == EXPECTED_QUERIES, "Payload query count drift")
    require(payload.get("counts", {}).get("sources") == EXPECTED_SOURCES, "Payload source count drift")
    require(payload.get("counts", {}).get("b1_output_rows") == EXPECTED_ROWS, "Payload output row count drift")
    require(payload.get("predictable_ceilings") == predictable_ceilings(payload["counts"]), "Payload predictable ceilings drift")
    require(receipt.get("root_manifest", {}).get("sha256") == phase8["root_manifest"]["sha256"], "Payload Phase-8 receipt/root mismatch")
    return payload


def validate_preflight_receipt(
    root: Path, receipt_path: Path, *, payload_path: Path | None = None,
) -> dict[str, Any]:
    receipt = read_json(receipt_path)
    require(receipt.get("schema_version") == PREFLIGHT_SCHEMA, "Preflight receipt schema drift")
    require(receipt.get("status") == "PASS_EXACT_PHASE8_NO_NETWORK_PREFLIGHT", "Preflight is not PASS")
    require(receipt.get("network_calls") == 0 and receipt.get("embedding_calls") == 0, "Preflight observed network/embedding work")
    manifest_path = validate_bound_file(root, receipt.get("payload_manifest"), field="preflight.payload_manifest")
    if payload_path is not None:
        require(manifest_path.resolve() == payload_path.resolve(), "Preflight payload path is stale")
    payload = validate_payload(root, manifest_path)
    require(receipt.get("runner_version") == RUNNER_VERSION, "Preflight runner version drift")
    require(receipt.get("phase8") == payload["phase8"], "Preflight Phase-8 binding drift")
    require(receipt.get("implementation") == payload["implementation"], "Preflight implementation binding drift")
    require(receipt.get("tokenizer") == payload["tokenizer"], "Preflight tokenizer binding drift")
    require(receipt.get("counts") == payload["counts"], "Preflight counts drift")
    require(receipt.get("predictable_ceilings") == payload["predictable_ceilings"], "Preflight ceilings drift")
    return receipt


def run_preflight(
    *, root: Path, phase8_receipt_path: Path, payload_dir: Path,
    preflight_receipt_path: Path,
) -> dict[str, Any]:
    root = root.resolve()
    for name, path in (
        ("Phase-8 receipt", phase8_receipt_path),
        ("payload directory", payload_dir),
        ("preflight receipt", preflight_receipt_path),
    ):
        try:
            path.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError(f"{name} must be inside repository root") from error
    require(not payload_dir.exists(), "Payload directory already exists; overwrite forbidden")
    require(not preflight_receipt_path.exists(), "Preflight receipt already exists; overwrite forbidden")
    require(relative(payload_dir, root).startswith("skill_benchmark/cache/"), "Payload must be under cache")
    require(relative(preflight_receipt_path, root).startswith("skill_benchmark/cache/"), "Preflight receipt must be under cache")
    staging = payload_dir.with_name(f".{payload_dir.name}.staging-{os.getpid()}")
    require(not staging.exists(), "Preflight staging path already exists")
    started = time.perf_counter()

    phase8_receipt, phase8_root, representation_bindings = phase8_bindings(
        root, phase8_receipt_path.resolve()
    )
    prompts, sources, conditions, representations = load_authority(root, representation_bindings)
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    tokenizer = AutoTokenizer.from_pretrained(
        root / TOKENIZER_REL,
        local_files_only=True,
        trust_remote_code=False,
    )
    text_rows, document_rows, query_text_ids, representation_summary = build_payload_data(
        tokenizer, prompts, representations
    )
    cache = V3ExactEmbeddingCache(root / CLEAN_CACHE_REL, create=False)
    cache_rows, cache_counts, planned_batches = cache_inventory_and_counts(
        text_rows, prompts, query_text_ids, cache
    )
    by_id = {row["text_id"]: row for row in text_rows}
    document_request_count = len(planned_batches) - EXPECTED_QUERIES
    planned_requests: list[dict[str, Any]] = []
    for request_index, batch in enumerate(planned_batches):
        rows = [by_id[text_id] for text_id in batch]
        body = embedding_request_bytes([row["text"] for row in rows])
        role = "document_batch" if request_index < document_request_count else "cold_query_single"
        if role == "cold_query_single":
            require(len(rows) == 1 and has_role(rows[0], "query"), "Cold-query request plan drift")
        planned_requests.append({
            "schema_version": "rq2b-v7-qwen-b1-phase8-planned-request-v3",
            "request_index": request_index,
            "request_role": role,
            "text_ids": batch,
            "text_count": len(rows),
            "content_proxy_tokens": sum(row["content_proxy_tokens"] for row in rows),
            "model_input_proxy_tokens": sum(row["model_input_proxy_tokens"] for row in rows),
            "special_token_proxy_tokens": sum(row["special_token_proxy_tokens"] for row in rows),
            "text_utf8_bytes": sum(row["utf8_bytes"] for row in rows),
            "request_body_utf8_bytes": len(body),
            "request_body_sha256": hashlib.sha256(body).hexdigest(),
        })
    require(len(planned_requests) == cache_counts["maximum_request_attempts"], "Planned request count drift")
    require(sum(row["request_body_utf8_bytes"] for row in planned_requests) == cache_counts["maximum_external_request_body_utf8_bytes"], "Planned request-byte count drift")

    staging.mkdir(parents=True, exist_ok=False)
    text_path = staging / "text_inventory.jsonl"
    documents_path = staging / "document_map.jsonl"
    cache_path = staging / "cache_inventory.jsonl"
    requests_path = staging / "planned_requests.jsonl"
    write_jsonl_new(text_path, text_rows)
    write_jsonl_new(documents_path, document_rows)
    write_jsonl_new(cache_path, cache_rows)
    write_jsonl_new(requests_path, planned_requests)
    implementation = implementation_bindings(root)
    final_manifest = payload_dir / "payload_manifest.json"
    phase8_root_binding = phase8_receipt["root_manifest"]
    phase8 = {
        "package_id": phase8_root["package_id"],
        "receipt": {
            "path": relative(phase8_receipt_path, root),
            "sha256": file_sha256(phase8_receipt_path),
        },
        "root_manifest": {
            "path": phase8_root_binding["path"],
            "sha256": phase8_root_binding["sha256"],
        },
    }
    representation_manifest = {
        representation: {
            **binding,
            "rows": EXPECTED_SOURCES,
            "provenance": (
                "AUTHORITATIVE_2026_09_09_V2"
                if representation in I1_I2_BINDINGS
                else "FINAL_PHASE8_V4_1"
            ),
        }
        for representation, binding in representation_bindings.items()
    }
    counts = {
        "queries": len(prompts),
        "sources": len(sources),
        "representations": len(representations),
        "b1_cells": len(conditions),
        "b1_output_rows": len(prompts) * len(conditions),
        "document_instances": len(document_rows),
        "document_windows": sum(len(row["chunk_text_ids"]) for row in document_rows),
        **cache_counts,
    }
    payload = {
        "schema_version": PAYLOAD_SCHEMA,
        "state": "SEALED_PHASE8_LABEL_FREE_NOT_AUTHORISED",
        "builder_version": BUILDER_VERSION,
        "runner_version": RUNNER_VERSION,
        "network_calls": 0,
        "embedding_calls": 0,
        "model": MODEL,
        "base_url": BASE_URL,
        "dimensions": DIMENSIONS,
        "encoding_format": "float",
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "chunker_version": CHUNKER_VERSION,
        "chunk_tokens": CHUNK_TOKENS,
        "overlap_tokens": OVERLAP_TOKENS,
        "primary_aggregation": "maximum_window_cosine",
        "sensitivity_aggregation": "cosine_of_l2_normalized_window_mean",
        "stable_tie_break": "source_sha256_ascending",
        "top_k": TOP_K,
        "conditions": {
            representation: f"{cell}-G0"
            for representation, cell in REPRESENTATION_CELLS.items()
        },
        "condition_authority": {
            cell: {
                "condition_id": condition["condition_id"],
                "representation": condition["representation"],
                "retriever": condition["retriever"],
                "persisted_candidate_source": condition["persisted_candidate_source"],
                "source_union_sha256": condition["source_union_sha256"],
            }
            for cell, condition in sorted(conditions.items())
        },
        "phase8": phase8,
        "fixed_inputs": {
            rel_path.as_posix(): {
                "sha256": expected,
                "rows": EXPECTED_QUERIES if rel_path == RUNTIME_REL else 36 if rel_path == CONDITIONS_REL else EXPECTED_SOURCES,
            }
            for rel_path, expected in FIXED_SHA256.items()
        },
        "representations": representation_manifest,
        "tokenizer": {
            "path": TOKENIZER_REL.as_posix(),
            "model": TOKENIZER_MODEL,
            "revision": TOKENIZER_REVISION,
            "tokenizer_json_sha256": TOKENIZER_JSON_SHA256,
        },
        "implementation": implementation,
        "artifacts": {
            "text_inventory": artifact_binding(text_path, payload_dir / text_path.name, root, rows=len(text_rows)),
            "document_map": artifact_binding(documents_path, payload_dir / documents_path.name, root, rows=len(document_rows)),
            "cache_inventory": artifact_binding(cache_path, payload_dir / cache_path.name, root, rows=len(cache_rows)),
            "planned_requests": artifact_binding(requests_path, payload_dir / requests_path.name, root, rows=len(planned_requests)),
        },
        "query_text_ids": query_text_ids,
        "representation_summary": representation_summary,
        "counts": counts,
        "predictable_ceilings": predictable_ceilings(counts),
        "cache_contract": {
            "root": CLEAN_CACHE_REL.as_posix(),
            "schema": "rq2b-v7-qwen-embedding-cache-v3",
            "key_schema": "rq2b-v7-qwen-b1-phase8-cache-key-v3",
            "mode": "READ_EXISTING_EXACT_HITS_WRITE_NEW_ONLY_NO_OVERWRITE",
            "old_v2_cache_read": False,
            "old_v2_cache_write": False,
        },
        "query_latency_contract": {
            "cold": True,
            "batch_size": 1,
            "one_request_per_unique_query_text": True,
            "preexisting_query_cache_never_skips_request": True,
        },
        "cost_contract": {
            "official_b1_row": "ONLINE_QUERY_ONLY",
            "offline_document_embedding": "RUN_RECEIPT_LEDGER_ONLY",
            "official_input_tokens": "query_model_input_proxy_tokens_including_special_tokens",
            "provider_reported_usage": "separate_request_and_run_ledgers",
        },
        "authorisation_boundary": {
            "provider_requests_authorised": False,
            "phase8_root_bound": True,
            "preflight_receipt_required": True,
            "one_use_root_release_required": True,
            "automatic_retries": 0,
        },
        "label_isolation": {
            "labels_or_results_read": False,
            "acceptable_sets_read": False,
            "metrics_read": False,
        },
    }
    manifest_path = staging / "payload_manifest.json"
    write_json_new(manifest_path, payload)
    staging.replace(payload_dir)
    manifest_sha = file_sha256(final_manifest)
    elapsed = time.perf_counter() - started
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "status": "PASS_EXACT_PHASE8_NO_NETWORK_PREFLIGHT",
        "runner_version": RUNNER_VERSION,
        "payload_manifest": {
            "path": relative(final_manifest, root),
            "sha256": manifest_sha,
        },
        "phase8": phase8,
        "implementation": implementation,
        "tokenizer": payload["tokenizer"],
        "counts": counts,
        "predictable_ceilings": payload["predictable_ceilings"],
        "network_calls": 0,
        "embedding_calls": 0,
        "preflight_seconds": elapsed,
        "completed_at_utc": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat().replace("+00:00", "Z"),
    }
    validate_payload(root, final_manifest)
    write_json_new(preflight_receipt_path, receipt)
    validate_preflight_receipt(root, preflight_receipt_path, payload_path=final_manifest)
    return receipt


class CharacterTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        values = [ord(character) + 1 for character in text]
        return [100, *values, 101] if add_special_tokens else values

    def __call__(self, text: str, *, add_special_tokens: bool, return_offsets_mapping: bool) -> dict[str, Any]:
        require(add_special_tokens is False and return_offsets_mapping is True, "Synthetic tokenizer mode drift")
        return {
            "input_ids": self.encode(text, add_special_tokens=False),
            "offset_mapping": [(index, index + 1) for index in range(len(text))],
        }


def self_test() -> dict[str, Any]:
    tokenizer = CharacterTokenizer()
    representations = {
        representation: [{
            "source_sha256": "1" * 64,
            "selector_text": f"{representation}\n\n" + "x" * 8000,
            "selector_text_sha256": text_sha256(f"{representation}\n\n" + "x" * 8000),
        }]
        for representation in REPRESENTATION_CELLS
    }
    prompts = [{"prompt_id": "p", "prompt": "query", "prompt_sha256": text_sha256("query")}]
    texts, documents, query_map, summaries = build_payload_data(tokenizer, prompts, representations)
    require(len(documents) == 4 and query_map == {"p": text_sha256("query")}, "Synthetic payload coverage drift")
    require(all(row["model_input_proxy_tokens"] == row["content_proxy_tokens"] + 2 for row in texts), "Synthetic special-token counts drift")
    require(all(summary["document_windows"] >= 2 for summary in summaries.values()), "Synthetic V2 windowing not exercised")
    payload = embedding_request_payload(["a", "b"])
    require(payload == {
        "model": MODEL,
        "input": ["a", "b"],
        "dimensions": DIMENSIONS,
        "encoding_format": "float",
    }, "Synthetic provider request contract drift")
    return {
        "status": "PASS_SYNTHETIC_PHASE8_PREFLIGHT_NO_NETWORK_NO_EMBEDDING",
        "network_calls": 0,
        "embedding_calls": 0,
        "checks": {
            "v2_exact_chunking": True,
            "content_and_model_input_proxy_counts_separate": True,
            "provider_request_contract": True,
            "four_representations": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--phase8-receipt", type=Path)
    parser.add_argument("--payload-dir", type=Path)
    parser.add_argument("--preflight-receipt", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.phase8_receipt is not None, "--preflight requires --phase8-receipt")
        require(args.payload_dir is not None, "--preflight requires --payload-dir")
        require(args.preflight_receipt is not None, "--preflight requires --preflight-receipt")
        root = args.root.resolve()
        phase8 = args.phase8_receipt if args.phase8_receipt.is_absolute() else root / args.phase8_receipt
        payload = args.payload_dir if args.payload_dir.is_absolute() else root / args.payload_dir
        receipt = args.preflight_receipt if args.preflight_receipt.is_absolute() else root / args.preflight_receipt
        result = run_preflight(
            root=root,
            phase8_receipt_path=phase8,
            payload_dir=payload,
            preflight_receipt_path=receipt,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
