#!/usr/bin/env python3
"""Build the label-free V7 Qwen B1 payload and its zero-network preflight.

The only scientific-data inputs are the frozen label-free query runtime, source
manifest, four representation artifacts, and first-matrix conditions.  An old
exact-text cache may be inspected read-only, one expected key at a time; cache
writes are reserved for the clean V7 cache used by the separately authorised
runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import time
from pathlib import Path
from typing import Any, Iterable

from rq2b_chunking import CHUNKER_VERSION as LEGACY_CHUNKER_VERSION, tokenizer_ids
from rq2b_v7_exact_chunking_v2 import CHUNKER_VERSION, exact_text_chunks
from run_rq2b_qwen import (
    BASE_URL,
    DIMENSIONS,
    MAX_BATCH_TEXTS,
    MODEL,
    ExactEmbeddingCache,
    cache_key as legacy_cache_key,
)


VERSION = "2026_09_09_v2"
BUILDER_VERSION = "rq2b-v7-qwen-b1-preflight-builder-v2"
RUNNER_VERSION = "rq2b-v7-qwen-b1-label-free-runner-v2"
PACKAGE_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_qwen_b1_preflight_2026_09_09_v2"
)
PAYLOAD_REL = Path("skill_benchmark/cache/rq2b_v7_qwen_b1_2026_09_09_v2/payload")
CLEAN_CACHE_REL = Path("skill_benchmark/cache/rq2b_v7_qwen_b1_2026_09_09_v2/embeddings")
DEFAULT_LEGACY_CACHE = Path(
    "/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/cache/rq2bv1/embeddings"
)

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
REPRESENTATION_PATHS = {
    "I1-discovery": Path(
        "skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1/"
        "i1-discovery.jsonl"
    ),
    "I2-original": Path(
        "skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1/"
        "i2-original.jsonl"
    ),
    "I3C-fielded": Path(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase7_i3_merged_2026_09_08_v1/i3c_fielded.jsonl"
    ),
    "I3-flat": Path(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase7_i3_merged_2026_09_08_v1/i3_flat.jsonl"
    ),
}
REPRESENTATION_CELLS = {
    "I1-discovery": "B02",
    "I2-original": "B05",
    "I3C-fielded": "B08",
    "I3-flat": "B11",
}
EXPECTED_SHA256 = {
    RUNTIME_REL: "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    SOURCE_REL: "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    CONDITIONS_REL: "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
    REPRESENTATION_PATHS["I1-discovery"]: "672928a98f31cf65aa90be752191495a9bebefec929b1d2b8b804afe66b3744e",
    REPRESENTATION_PATHS["I2-original"]: "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
    REPRESENTATION_PATHS["I3C-fielded"]: "cb1fd58e61b97d1c21fa41a995f508a7e323127d3f14542ca8ed3f736a291595",
    REPRESENTATION_PATHS["I3-flat"]: "3697e15a308774ec97ed8df2cb4a108e32f2e049fadfcee3d2efcf671d088b74",
}
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
IMPLEMENTATION_FILES = {
    "builder": Path("skill_benchmark/scripts/build_rq2b_v7_qwen_b1_preflight.py"),
    "runner": Path("skill_benchmark/scripts/run_rq2b_v7_qwen_b1.py"),
    "chunker_v2": Path("skill_benchmark/scripts/rq2b_v7_exact_chunking_v2.py"),
    "legacy_cache_contract": Path("skill_benchmark/scripts/run_rq2b_qwen.py"),
    "legacy_chunker_contract": Path("skill_benchmark/scripts/rq2b_chunking.py"),
    "gzip_shard_validator": Path("skill_benchmark/scripts/validate_rq2b_v7_qwen_b1_shards.py"),
    "tests": Path("skill_benchmark/scripts/test_rq2b_v7_qwen_b1.py"),
}

HEX = set("0123456789abcdef")
PROHIBITED_KEY_TOKENS = {
    "target", "gold", "label", "acceptable", "adequacy", "judged",
    "unjudged", "metric", "hit", "mrr", "recall", "ground_truth",
    "correctness", "a_q", "j_q", "d_q",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


def cache_key(text: str) -> str:
    return canonical_sha256({
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "chunker_version": CHUNKER_VERSION,
        "text_sha256": text_sha256(text),
    })


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected object at {path}:{line_number}")
            rows.append(value)
    return rows


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def normalized_key_tokens(key: str) -> set[str]:
    normalized = key.lower().replace("-", "_").replace(" ", "_")
    tokens = set(normalized.split("_")) | {normalized}
    for phrase in ("ground_truth", "a_q", "j_q", "d_q"):
        if phrase in normalized:
            tokens.add(phrase)
    return tokens


def reject_label_keys(value: Any, location: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            # I3's source-only representation schema legitimately names its
            # human-readable serialization heading ``field_label``.  It is not
            # an evaluation label and is frozen inside the representation.
            allowed_representation_key = str(key) == "field_label"
            require(
                allowed_representation_key
                or not (normalized_key_tokens(str(key)) & PROHIBITED_KEY_TOKENS),
                f"Prohibited label/outcome key at {location}: {key}",
            )
            reject_label_keys(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_label_keys(child, f"{location}[{index}]")


def verify_input_hashes(root: Path) -> None:
    for rel_path, expected in EXPECTED_SHA256.items():
        path = root / rel_path
        require(path.is_file(), f"Frozen input missing: {rel_path}")
        actual = file_sha256(path)
        require(actual == expected, f"Frozen input drift: {rel_path}: {actual} != {expected}")
    tokenizer_json = root / TOKENIZER_REL / "tokenizer.json"
    require(tokenizer_json.is_file(), f"Frozen proxy tokenizer missing: {tokenizer_json}")
    require(
        file_sha256(tokenizer_json) == TOKENIZER_JSON_SHA256,
        "Frozen proxy tokenizer hash drift",
    )


def load_authority(root: Path) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
]:
    """Load and validate only the frozen label-free scientific inputs."""
    verify_input_hashes(root)
    prompts = read_jsonl(root / RUNTIME_REL)
    require(len(prompts) == 1077, "Expected 1,077 label-free runtime queries")
    require(len({row.get("prompt_id") for row in prompts}) == len(prompts), "Duplicate prompt IDs")
    for index, row in enumerate(prompts):
        reject_label_keys(row, f"runtime[{index}]")
        require(
            set(row) == {"schema_version", "prompt_id", "prompt", "prompt_sha256"},
            f"Unexpected label-free runtime fields at row {index}",
        )
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", "Runtime schema drift")
        require(text_sha256(row["prompt"]) == row["prompt_sha256"], "Runtime prompt hash drift")

    sources = read_jsonl(root / SOURCE_REL)
    require(len(sources) == 3798, "Expected 3,798 frozen sources")
    source_ids = {row.get("sha256") for row in sources}
    require(len(source_ids) == len(sources) and all(is_sha256(value) for value in source_ids), "Source identity drift")
    for index, row in enumerate(sources):
        reject_label_keys(row, f"sources[{index}]")
        require(set(row) == {"path", "sha256", "bytes"}, f"Unexpected source fields at row {index}")
        require(isinstance(row["bytes"], int) and row["bytes"] > 0, "Invalid source byte count")

    conditions = read_jsonl(root / CONDITIONS_REL)
    require(len(conditions) == 36, "Expected 36 first-matrix conditions")
    for index, row in enumerate(conditions):
        reject_label_keys(row, f"conditions[{index}]")
    selected = {
        row["persisted_candidate_source"]: row
        for row in conditions
        if row["reranker"] == "NONE" and row["retriever"] == "Qwen-text-embedding-v4"
    }
    require(set(selected) == set(REPRESENTATION_CELLS.values()), "Qwen B1 condition set drift")
    for representation, cell in REPRESENTATION_CELLS.items():
        row = selected[cell]
        require(row["condition_id"] == f"{cell}-G0", f"Condition ID drift: {cell}")
        require(row["representation"] == representation, f"Representation condition drift: {cell}")
        require(row["source_union_sha256"] == SOURCE_UNION_SHA256, f"Source union drift: {cell}")
        require(row["query_count"] == 1077, f"Query count drift: {cell}")
        require(row["execution_authorised"] is False, f"Preparation condition unexpectedly authorises execution: {cell}")

    representation_rows: dict[str, list[dict[str, Any]]] = {}
    for representation, rel_path in REPRESENTATION_PATHS.items():
        rows = read_jsonl(root / rel_path)
        require(len(rows) == 3798, f"Representation row count drift: {representation}")
        seen: set[str] = set()
        for index, row in enumerate(rows):
            reject_label_keys(row, f"{representation}[{index}]")
            source_sha = row.get("source_sha256")
            selector_text = row.get("selector_text")
            require(is_sha256(source_sha) and source_sha in source_ids, f"Unknown source in {representation}")
            require(source_sha not in seen, f"Duplicate source in {representation}: {source_sha}")
            seen.add(source_sha)
            require(isinstance(selector_text, str) and selector_text, f"Empty selector text in {representation}")
            require(text_sha256(selector_text) == row.get("selector_text_sha256"), f"Selector hash drift in {representation}")
            require(row.get("representation") == representation, f"Representation tag drift: {representation}")
        require(seen == source_ids, f"Representation source coverage drift: {representation}")
        representation_rows[representation] = rows
    return prompts, sources, selected, representation_rows


def register_text(
    inventory: dict[str, dict[str, Any]],
    *,
    text: str,
    local_proxy_tokens: int,
    role: dict[str, Any],
) -> str:
    text_id = text_sha256(text)
    existing = inventory.get(text_id)
    if existing is None:
        inventory[text_id] = {
            "schema_version": "rq2b-v7-qwen-b1-payload-text-v2",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "local_proxy_tokens": local_proxy_tokens,
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "SHA-256 collision in payload text inventory")
        require(existing["local_proxy_tokens"] == local_proxy_tokens, "Token count drift for identical text")
        existing["roles"].append(role)
    return text_id


def build_payload_data(
    tokenizer: Any,
    prompts: list[dict[str, Any]],
    representations: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str], dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    document_rows: list[dict[str, Any]] = []
    representation_summary: dict[str, dict[str, Any]] = {}
    for representation in REPRESENTATION_PATHS:
        started = time.perf_counter()
        windowed_documents = 0
        document_windows = 0
        maximum_source_tokens = 0
        maximum_adjacent_overlap_tokens = 0
        short_boundary_direct_advances = 0
        for source_index, row in enumerate(representations[representation]):
            source_tokens = len(tokenizer_ids(tokenizer, row["selector_text"]))
            maximum_source_tokens = max(maximum_source_tokens, source_tokens)
            chunks = exact_text_chunks(
                tokenizer,
                row["selector_text"],
                maximum_tokens=CHUNK_TOKENS,
                overlap_tokens=OVERLAP_TOKENS,
            )
            if len(chunks) > 1:
                windowed_documents += 1
            for previous, current in zip(chunks, chunks[1:]):
                overlap_count = len(tokenizer_ids(
                    tokenizer,
                    row["selector_text"][current.start_char:previous.end_char],
                ))
                maximum_adjacent_overlap_tokens = max(
                    maximum_adjacent_overlap_tokens, overlap_count
                )
                require(overlap_count <= OVERLAP_TOKENS, "V2 payload overlap ceiling drift")
                if previous.token_count <= OVERLAP_TOKENS:
                    require(current.start_char == previous.end_char, "V2 short-boundary progress drift")
                    short_boundary_direct_advances += 1
            chunk_text_ids: list[str] = []
            chunk_metadata: list[dict[str, Any]] = []
            for chunk in chunks:
                chunk_text_ids.append(register_text(
                    inventory,
                    text=chunk.text,
                    local_proxy_tokens=chunk.token_count,
                    role={
                        "kind": "document_chunk",
                        "representation": representation,
                        "first_stage_cell_id": REPRESENTATION_CELLS[representation],
                        "source_sha256": row["source_sha256"],
                        "chunk_index": chunk.chunk_index,
                    },
                ))
                chunk_metadata.append({
                    "chunk_index": chunk.chunk_index,
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char,
                    "token_count": chunk.token_count,
                    "text_sha256": chunk.text_sha256,
                    "token_ids_sha256": chunk.token_ids_sha256,
                    "ended_at_preferred_boundary": chunk.ended_at_preferred_boundary,
                })
            document_windows += len(chunks)
            document_rows.append({
                "schema_version": "rq2b-v7-qwen-b1-document-map-v2",
                "representation": representation,
                "first_stage_cell_id": REPRESENTATION_CELLS[representation],
                "source_row_index": source_index,
                "source_sha256": row["source_sha256"],
                "selector_text_sha256": row["selector_text_sha256"],
                "selector_local_proxy_tokens": source_tokens,
                "chunk_text_ids": chunk_text_ids,
                "chunks": chunk_metadata,
            })
        representation_summary[representation] = {
            "first_stage_cell_id": REPRESENTATION_CELLS[representation],
            "documents": len(representations[representation]),
            "document_windows": document_windows,
            "windowed_documents": windowed_documents,
            "maximum_source_proxy_tokens": maximum_source_tokens,
            "maximum_adjacent_overlap_proxy_tokens": maximum_adjacent_overlap_tokens,
            "short_boundary_direct_advances": short_boundary_direct_advances,
            "chunking_seconds": time.perf_counter() - started,
        }

    query_text_ids: dict[str, str] = {}
    for prompt in prompts:
        token_count = len(tokenizer_ids(tokenizer, prompt["prompt"]))
        require(token_count <= QUERY_PROVIDER_LIMIT, f"Query exceeds provider limit: {prompt['prompt_id']}")
        query_text_ids[prompt["prompt_id"]] = register_text(
            inventory,
            text=prompt["prompt"],
            local_proxy_tokens=token_count,
            role={
                "kind": "query",
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
            },
        )
    text_rows = [inventory[text_id] for text_id in sorted(inventory)]
    document_rows.sort(key=lambda row: (row["representation"], row["source_sha256"]))
    return text_rows, document_rows, query_text_ids, representation_summary


class ReadOnlyExactEmbeddingCache(ExactEmbeddingCache):
    """Old exact cache contract without creating or mutating its directory."""

    def __init__(self, root: Path) -> None:
        self.root = root / "qwen" / MODEL / str(DIMENSIONS)

    def store(self, *_: Any, **__: Any) -> None:
        raise ValueError("Legacy exact cache is read-only")


class V2ExactEmbeddingCache:
    """Exact-text clean cache under the corrected V7 chunker namespace."""

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
        require(
            payload.get("schema_version") == "rq2b-v7-qwen-embedding-cache-v2",
            f"Clean cache schema mismatch: {path}",
        )
        require(payload.get("base_url") == BASE_URL, f"Clean cache endpoint mismatch: {path}")
        require(payload.get("model") == MODEL, f"Clean cache model mismatch: {path}")
        require(payload.get("dimensions") == DIMENSIONS, f"Clean cache dimensions mismatch: {path}")
        require(payload.get("chunker_version") == CHUNKER_VERSION, f"Clean cache chunker mismatch: {path}")
        require(payload.get("text_sha256") == text_sha256(text), f"Clean cache text mismatch: {path}")
        vector = [float(value) for value in payload.get("embedding", [])]
        require(len(vector) == DIMENSIONS, f"Clean cache vector dimension mismatch: {path}")
        require(all(math.isfinite(value) for value in vector), f"Clean cache non-finite vector: {path}")
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
        require(not path.exists(), f"Refusing to overwrite clean cache entry: {path}")
        write_json(path, {
            "schema_version": "rq2b-v7-qwen-embedding-cache-v2",
            "base_url": BASE_URL,
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "chunker_version": CHUNKER_VERSION,
            "text_sha256": text_sha256(text),
            "local_proxy_tokens": local_proxy_tokens,
            "provider_usage": provider_usage,
            "embedding": vector,
        })


def cache_inventory(
    text_rows: list[dict[str, Any]],
    *,
    clean_cache: V2ExactEmbeddingCache,
    legacy_cache: ReadOnlyExactEmbeddingCache,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for text_row in text_rows:
        text = text_row["text"]
        clean_path = clean_cache.path(text)
        legacy_path = legacy_cache.path(text)
        clean_hit = clean_path.is_file()
        legacy_hit = legacy_path.is_file()
        if clean_hit:
            require(clean_cache.load(text) is not None, f"Invalid clean exact cache entry: {clean_path}")
        if legacy_hit:
            require(legacy_cache.load(text) is not None, f"Invalid legacy exact cache entry: {legacy_path}")
        roles = {role["kind"] for role in text_row["roles"]}
        rows.append({
            "schema_version": "rq2b-v7-qwen-b1-cache-inventory-row-v2",
            "text_id": text_row["text_id"],
            "clean_cache_key": cache_key(text),
            "legacy_cache_key": legacy_cache_key(text),
            "role_kinds": sorted(roles),
            "local_proxy_tokens": text_row["local_proxy_tokens"],
            "utf8_bytes": text_row["utf8_bytes"],
            "clean_cache_hit": clean_hit,
            "clean_cache_entry_sha256": file_sha256(clean_path) if clean_hit else None,
            "legacy_cache_hit": legacy_hit,
            "legacy_cache_entry_sha256": file_sha256(legacy_path) if legacy_hit else None,
        })

    by_id = {row["text_id"]: row for row in rows}
    document_texts = [row for row in text_rows if any(role["kind"] == "document_chunk" for role in row["roles"])]
    query_texts = [row for row in text_rows if any(role["kind"] == "query" for role in row["roles"])]

    def available(row: dict[str, Any]) -> bool:
        item = by_id[row["text_id"]]
        return bool(item["clean_cache_hit"] or item["legacy_cache_hit"])

    document_misses = [row for row in document_texts if not available(row)]
    query_entry_misses = [row for row in query_texts if not available(row)]
    new_ids = {row["text_id"] for row in [*document_misses, *query_entry_misses]}
    external_rows = [*document_misses, *query_texts]
    summary = {
        "unique_texts": len(text_rows),
        "unique_document_texts": len(document_texts),
        "unique_query_texts": len(query_texts),
        "document_cache_hits": len(document_texts) - len(document_misses),
        "document_cache_misses": len(document_misses),
        "query_cache_entries_preexisting": len(query_texts) - len(query_entry_misses),
        "query_cache_entry_misses": len(query_entry_misses),
        "clean_cache_hits": sum(row["clean_cache_hit"] for row in rows),
        "legacy_cache_hits": sum(row["legacy_cache_hit"] for row in rows),
        "maximum_new_cache_entries": len(new_ids),
        "maximum_new_cache_proxy_tokens": sum(
            int(by_id[text_id]["local_proxy_tokens"]) for text_id in new_ids
        ),
        "maximum_new_cache_utf8_bytes": sum(
            int(by_id[text_id]["utf8_bytes"]) for text_id in new_ids
        ),
        "maximum_external_text_submissions": len(external_rows),
        "maximum_external_submission_proxy_tokens": sum(int(row["local_proxy_tokens"]) for row in external_rows),
        "maximum_external_submission_utf8_bytes": sum(int(row["utf8_bytes"]) for row in external_rows),
        "cold_query_requests": len(query_texts),
        "maximum_document_batch_requests": math.ceil(len(document_misses) / MAX_BATCH_TEXTS),
        "maximum_request_attempts": math.ceil(len(document_misses) / MAX_BATCH_TEXTS) + len(query_texts),
        "maximum_successful_calls": math.ceil(len(document_misses) / MAX_BATCH_TEXTS) + len(query_texts),
        "automatic_retries": 0,
    }
    return rows, summary


def payload_artifact(
    staging_path: Path,
    final_path: Path,
    root: Path,
    rows: int | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": relative(final_path, root),
        "sha256": file_sha256(staging_path),
        "utf8_bytes": staging_path.stat().st_size,
    }
    if rows is not None:
        result["rows"] = rows
    return result


def build(root: Path, legacy_cache_root: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    package_root = root / PACKAGE_REL
    payload_root = root / PAYLOAD_REL
    require(not package_root.exists(), f"Refusing to overwrite preflight package: {package_root}")
    require(not payload_root.exists(), f"Refusing to overwrite payload: {payload_root}")

    prompts, sources, conditions, representations = load_authority(root)
    tokenizer = AutoTokenizer.from_pretrained(root / TOKENIZER_REL, local_files_only=True)
    started = time.perf_counter()
    text_rows, document_rows, query_text_ids, representation_summary = build_payload_data(
        tokenizer, prompts, representations
    )

    payload_staging = payload_root.parent / f".{payload_root.name}.staging-{os.getpid()}"
    package_staging = package_root.parent / f".{package_root.name}.staging-{os.getpid()}"
    require(not payload_staging.exists() and not package_staging.exists(), "Stale Qwen preflight staging path")
    payload_staging.mkdir(parents=True, exist_ok=False)
    try:
        text_path = payload_staging / "text_inventory.jsonl"
        document_path = payload_staging / "document_map.jsonl"
        write_jsonl(text_path, text_rows)
        write_jsonl(document_path, document_rows)

        clean_cache = V2ExactEmbeddingCache(root / CLEAN_CACHE_REL)
        legacy_cache = ReadOnlyExactEmbeddingCache(legacy_cache_root)
        inventory_rows, cache_summary = cache_inventory(
            text_rows, clean_cache=clean_cache, legacy_cache=legacy_cache
        )
        cache_inventory_path = payload_staging / "cache_hit_inventory.jsonl"
        write_jsonl(cache_inventory_path, inventory_rows)

        final_text_path = payload_root / text_path.name
        final_document_path = payload_root / document_path.name
        final_inventory_path = payload_root / cache_inventory_path.name
        input_artifacts = {
            rel_path.as_posix(): {"sha256": expected, "rows": (
                1077 if rel_path == RUNTIME_REL else 36 if rel_path == CONDITIONS_REL else 3798
            )}
            for rel_path, expected in EXPECTED_SHA256.items()
        }
        implementation = {
            name: {"path": path.as_posix(), "sha256": file_sha256(root / path)}
            for name, path in IMPLEMENTATION_FILES.items()
        }
        payload_manifest = {
            "schema_version": "rq2b-v7-qwen-b1-payload-manifest-v2",
            "version": VERSION,
            "state": "SEALED_LABEL_FREE_NOT_AUTHORISED",
            "builder_version": BUILDER_VERSION,
            "runner_version": RUNNER_VERSION,
            "implementation": implementation,
            "supersedes": {
                "package": "v7_qwen_b1_preflight_2026_09_09_v1",
                "disposition": "EXPLORATORY_SUPERSEDED_BEFORE_PROVIDER_REQUEST",
                "reason": "v1 exact chunker can advance one character after a short preferred-boundary chunk already fits inside the overlap budget",
                "method_intent_changed": False,
            },
            "network_calls": 0,
            "selector_runs": 0,
            "model": MODEL,
            "base_url": BASE_URL,
            "dimensions": DIMENSIONS,
            "encoding_format": "float",
            "chunker_version": CHUNKER_VERSION,
            "chunk_tokens": CHUNK_TOKENS,
            "overlap_tokens": OVERLAP_TOKENS,
            "document_score_aggregation": "maximum_window_cosine",
            "noncore_sensitivity_aggregation": "cosine_of_l2_normalized_window_mean",
            "stable_tie_break": "source_sha256_ascending",
            "top_k": TOP_K,
            "maximum_batch_texts": MAX_BATCH_TEXTS,
            "query_latency_contract": {
                "cold": True,
                "batch_size": 1,
                "one_request_per_unique_query_text": True,
                "preexisting_query_cache_never_skips_request": True,
            },
            "input_artifacts": input_artifacts,
            "tokenizer": {
                "path": TOKENIZER_REL.as_posix(),
                "model": TOKENIZER_MODEL,
                "revision": TOKENIZER_REVISION,
                "tokenizer_json_sha256": TOKENIZER_JSON_SHA256,
            },
            "conditions": {
                cell: {
                    "condition_id": row["condition_id"],
                    "representation": row["representation"],
                    "retriever": row["retriever"],
                    "persisted_candidate_source": row["persisted_candidate_source"],
                    "source_union_sha256": row["source_union_sha256"],
                }
                for cell, row in sorted(conditions.items())
            },
            "artifacts": {
                "text_inventory": payload_artifact(text_path, final_text_path, root, len(text_rows)),
                "document_map": payload_artifact(document_path, final_document_path, root, len(document_rows)),
                "cache_hit_inventory": payload_artifact(
                    cache_inventory_path, final_inventory_path, root, len(inventory_rows)
                ),
            },
            "query_text_ids": query_text_ids,
            "representation_summary": representation_summary,
            "counts": {
                "queries": len(prompts),
                "sources": len(sources),
                "representations": len(representations),
                "b1_cells": len(conditions),
                "b1_output_rows": len(prompts) * len(conditions),
                "document_instances": len(document_rows),
                "document_windows": sum(len(row["chunk_text_ids"]) for row in document_rows),
                **cache_summary,
            },
            "cache_contract": {
                "clean_cache_root": CLEAN_CACHE_REL.as_posix(),
                "clean_cache_schema": "rq2b-v7-qwen-embedding-cache-v2",
                "clean_cache_chunker_version": CHUNKER_VERSION,
                "legacy_cache_root_recorded_at_preflight": str(legacy_cache_root.resolve()),
                "legacy_cache_schema": "rq2b-qwen-embedding-cache-v1",
                "legacy_cache_chunker_version": LEGACY_CHUNKER_VERSION,
                "legacy_cache_mode": "READ_ONLY_EXPECTED_KEYS_ONLY",
                "clean_cache_mode": "READ_WRITE_NO_OVERWRITE",
                "each_hit_schema_hash_model_dimension_chunker_text_and_vector_validated": True,
            },
            "authorisation_boundary": {
                "external_transfer_authorised": False,
                "provider_requests_authorised": False,
                "phase7_qa_pass_required": True,
                "root_release_required": True,
                "exact_payload_hash_authorisation_required": True,
                "exact_request_ceilings_required": True,
                "automatic_retries": 0,
            },
            "label_isolation": {
                "labels_or_results_read": False,
                "allowed_scientific_inputs": [
                    RUNTIME_REL.as_posix(), SOURCE_REL.as_posix(), CONDITIONS_REL.as_posix(),
                    *(path.as_posix() for path in REPRESENTATION_PATHS.values()),
                ],
                "prohibited_inputs": [
                    "offline_label_adapter", "reviewed_confusable_neighbour_ledger",
                    "targets", "gold", "A_q", "J_q", "D_q", "results",
                ],
            },
            "preflight_seconds": time.perf_counter() - started,
        }
        payload_manifest_path = payload_staging / "payload_manifest.json"
        write_json(payload_manifest_path, payload_manifest)
        payload_staging.replace(payload_root)

        package_staging.mkdir(parents=True, exist_ok=False)
        final_payload_manifest_path = payload_root / "payload_manifest.json"
        pending_authorisation = {
            "schema_version": "rq2b-v7-qwen-b1-execution-authorisation-v2",
            "state": "PENDING_PHASE7_QA_PASS_AND_ROOT_RELEASE",
            "payload_manifest_path": relative(final_payload_manifest_path, root),
            "payload_manifest_sha256": file_sha256(final_payload_manifest_path),
            "base_url": BASE_URL,
            "model": MODEL,
            "dimensions": DIMENSIONS,
            "automatic_retries": 0,
            "cold_query_latency_measurement": True,
            "cold_query_batch_size": 1,
            "phase7_qa_status": "PENDING",
            "phase7_qa_receipt_sha256": None,
            "root_release_id": None,
            "run_id": None,
            "output_dir": None,
            "timeout_seconds": None,
            "legacy_cache_root": str(legacy_cache_root.resolve()),
            "clean_cache_root": CLEAN_CACHE_REL.as_posix(),
            "ceilings": {
                key: cache_summary[key]
                for key in (
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
            },
            "note": "This pending record is not executable authorisation.",
        }
        write_json(package_staging / "pending_authorisation.json", pending_authorisation)
        report = {
            "schema_version": "rq2b-v7-qwen-b1-preflight-report-v2",
            "status": "PASS_LABEL_FREE_PAYLOAD_AND_CACHE_PREFLIGHT_AWAITING_PHASE7_QA_AND_ROOT_RELEASE",
            "network_calls": 0,
            "provider_requests": 0,
            "selector_runs": 0,
            "labels_or_results_read": False,
            "payload_manifest": {
                "path": relative(final_payload_manifest_path, root),
                "sha256": file_sha256(final_payload_manifest_path),
            },
            "cache_summary": cache_summary,
            "representation_summary": representation_summary,
            "implementation": implementation,
            "blocked_by": ["PHASE7_QA_PASS_RECEIPT", "ROOT_EXECUTION_RELEASE"],
        }
        write_json(package_staging / "preflight_report.json", report)
        readme = f"""# V7 Qwen label-free B1 preflight {VERSION}

Status: `PASS_LABEL_FREE_PAYLOAD_AND_CACHE_PREFLIGHT_AWAITING_PHASE7_QA_AND_ROOT_RELEASE`.

This package prepares B02/B05/B08/B11 only. It uses the frozen 1,077 label-free
queries, 3,798-source manifest, four representation artifacts, and first-matrix
conditions. It reads no target/gold/A_q/J_q/D_q/result artifact and performs no
provider request.

The payload uses Qwen `text-embedding-v4` at 1,024 dimensions and the versioned
`{CHUNKER_VERSION}` exact-substring correction with {CHUNK_TOKENS}-proxy-token
windows and at most {OVERLAP_TOKENS} overlap tokens. It preserves lossless
character coverage and fixes the v1 short-boundary one-character-progress bug.
Maximum-window cosine is the B1 outcome, ties use ascending `source_sha256`, and
Top-{TOP_K} is persisted. Mean-window cosine is a separate non-core sensitivity.
Cold query latency requires one single-text request per unique query even when a
query cache entry exists.

Formal B1 and sensitivity outputs are condition-sharded deterministic gzip
(`mtime=0`) containing canonical compact JSONL. Compression changes neither row
semantics nor the Top-20 binding hash, and the Qwen validator reads `.jsonl.gz`
directly.

The old V3 exact cache is inspected read-only for expected payload keys. Each hit
is schema/model/dimension/chunker/text/vector checked and byte-hash bound in the
ignored payload inventory. Only the clean V7-v2 cache may receive new entries.

No execution command is valid yet. `pending_authorisation.json` deliberately has
a non-executable state. After Phase-7 QA passes, a separate root release must bind
the exact payload hash, ceilings, run ID, output directory, timeout and QA receipt.

Offline replay:

```bash
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/build_rq2b_v7_qwen_b1_preflight.py --verify
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_qwen_b1.py
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/validate_rq2b_v7_qwen_b1_shards.py --run-manifest /ABSOLUTE/PATH/manifest.json
```
"""
        readme_path = package_staging / "README.md"
        readme_path.write_text(readme, encoding="utf-8")
        integrity = {
            "schema_version": "rq2b-v7-qwen-b1-preflight-integrity-v2",
            "status": "PASS_ZERO_NETWORK_LABEL_FREE_PREFLIGHT_EXECUTION_NOT_AUTHORISED",
            "artifacts": {
                "README.md": {"sha256": file_sha256(readme_path)},
                "pending_authorisation.json": {"sha256": file_sha256(package_staging / "pending_authorisation.json")},
                "preflight_report.json": {"sha256": file_sha256(package_staging / "preflight_report.json")},
            },
            "payload_manifest_sha256": file_sha256(final_payload_manifest_path),
            "implementation": implementation,
            "checks": {
                "label_free_input_hashes": True,
                "all_representation_sources_exactly_match_source_manifest": True,
                "exact_lossless_chunks_verified": True,
                "legacy_cache_hits_validated_read_only": True,
                "cold_query_request_ceiling_exact": True,
                "zero_retries": True,
                "zero_network": True,
                "execution_authorised": False,
            },
        }
        write_json(package_staging / "integrity_report.json", integrity)
        package_staging.replace(package_root)
        return report
    except Exception:
        if payload_staging.exists():
            shutil.rmtree(payload_staging)
        if package_staging.exists():
            shutil.rmtree(package_staging)
        raise


def verify(root: Path, legacy_cache_root: Path) -> dict[str, Any]:
    package_root = root / PACKAGE_REL
    payload_root = root / PAYLOAD_REL
    require(package_root.is_dir(), f"Preflight package missing: {package_root}")
    require(payload_root.is_dir(), f"Payload missing: {payload_root}")
    integrity = read_json(package_root / "integrity_report.json")
    require(integrity["status"] == "PASS_ZERO_NETWORK_LABEL_FREE_PREFLIGHT_EXECUTION_NOT_AUTHORISED", "Preflight status drift")
    for name, artifact in integrity["artifacts"].items():
        require(file_sha256(package_root / name) == artifact["sha256"], f"Package artifact drift: {name}")
    manifest_path = payload_root / "payload_manifest.json"
    require(file_sha256(manifest_path) == integrity["payload_manifest_sha256"], "Payload manifest drift")
    manifest = read_json(manifest_path)
    require(manifest["state"] == "SEALED_LABEL_FREE_NOT_AUTHORISED", "Payload state drift")
    require(manifest["network_calls"] == 0 and manifest["selector_runs"] == 0, "Preflight execution boundary drift")
    for name, implementation in manifest["implementation"].items():
        path = root / implementation["path"]
        require(file_sha256(path) == implementation["sha256"], f"Implementation drift: {name}")
    verify_input_hashes(root)
    for artifact in manifest["artifacts"].values():
        path = root / artifact["path"]
        require(file_sha256(path) == artifact["sha256"], f"Payload artifact drift: {path}")
        require(path.stat().st_size == artifact["utf8_bytes"], f"Payload artifact size drift: {path}")

    text_rows = read_jsonl(root / manifest["artifacts"]["text_inventory"]["path"])
    inventory_rows = read_jsonl(root / manifest["artifacts"]["cache_hit_inventory"]["path"])
    require(len(text_rows) == len(inventory_rows) == manifest["counts"]["unique_texts"], "Payload inventory count drift")
    by_id = {row["text_id"]: row for row in text_rows}
    require(len(by_id) == len(text_rows), "Duplicate payload text IDs")
    legacy_cache = ReadOnlyExactEmbeddingCache(legacy_cache_root)
    clean_cache = V2ExactEmbeddingCache(root / CLEAN_CACHE_REL)
    for row in inventory_rows:
        text = by_id[row["text_id"]]["text"]
        require(row["clean_cache_key"] == cache_key(text), "Clean cache inventory key drift")
        require(row["legacy_cache_key"] == legacy_cache_key(text), "Legacy cache inventory key drift")
        for prefix, cache in (("clean", clean_cache), ("legacy", legacy_cache)):
            if row[f"{prefix}_cache_hit"]:
                path = cache.path(text)
                require(path.is_file(), f"Recorded cache hit missing: {path}")
                require(file_sha256(path) == row[f"{prefix}_cache_entry_sha256"], f"Recorded cache entry drift: {path}")
                require(cache.load(text) is not None, f"Recorded cache entry invalid: {path}")
    pending = read_json(package_root / "pending_authorisation.json")
    require(pending["state"] == "PENDING_PHASE7_QA_PASS_AND_ROOT_RELEASE", "Pending authorisation became executable")
    require(pending["payload_manifest_sha256"] == file_sha256(manifest_path), "Pending authorisation payload drift")
    return {
        "status": "PASS_ZERO_NETWORK_LABEL_FREE_PREFLIGHT_REPLAY",
        "network_calls": 0,
        "provider_requests": 0,
        "counts": manifest["counts"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--legacy-cache-root", type=Path, default=DEFAULT_LEGACY_CACHE)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    legacy = args.legacy_cache_root.resolve()
    result = verify(root, legacy) if args.verify else build(root, legacy)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
