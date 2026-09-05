#!/usr/bin/env python3
"""Build the exact local Qwen payload manifest for later separate approval."""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path
from typing import Any

from rq2b_chunking import CHUNKER_VERSION, exact_text_chunks, tokenizer_ids
from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    source_length_quartiles,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    verify_i3c_retrieval_ready,
    version_root,
    write_json_new,
    write_jsonl_new,
)
from run_rq2b_qwen import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL


REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
)


def load_representations(root: Path) -> dict[str, tuple[Path, list[dict[str, Any]]]]:
    frozen_root = version_root(root)
    base_manifest = read_json(frozen_root / "representations" / "manifest.json")
    i3_manifest = read_json(frozen_root / "i3c_merged" / "manifest.json")
    verify_i3c_retrieval_ready(root)
    loaded: dict[str, tuple[Path, list[dict[str, Any]]]] = {}
    for name in REPRESENTATIONS:
        source_manifest = base_manifest if name in base_manifest["artifacts"] else i3_manifest
        artifact = source_manifest["artifacts"][name]
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], f"Representation drift: {name}")
        rows = read_jsonl(path)
        require(len(rows) == 2433, f"Representation row count mismatch: {name}")
        loaded[name] = (path, rows)
    return loaded


def register_text(
    texts: dict[str, dict[str, Any]],
    *,
    text: str,
    local_proxy_tokens: int,
    role: dict[str, Any],
) -> str:
    text_id = sha256_text(text)
    existing = texts.get(text_id)
    if existing is None:
        texts[text_id] = {
            "schema_version": "rq2b-qwen-payload-text-v1",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "local_proxy_tokens": local_proxy_tokens,
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "SHA-256 collision in Qwen text inventory")
        require(existing["local_proxy_tokens"] == local_proxy_tokens, "Qwen token count drift for identical text")
        existing["roles"].append(role)
    return text_id


def build_payload_data(
    tokenizer: Any,
    representations: dict[str, tuple[Path, list[dict[str, Any]]]],
    prompts: list[dict[str, Any]],
    *,
    chunk_tokens: int,
    overlap_tokens: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    texts: dict[str, dict[str, Any]] = {}
    document_maps: dict[str, list[dict[str, Any]]] = {}
    representation_chunking_seconds: dict[str, float] = {}
    for representation, (_, rows) in representations.items():
        representation_started = time.perf_counter()
        length_quartiles = source_length_quartiles(rows)
        documents: list[dict[str, Any]] = []
        for row in rows:
            chunks = exact_text_chunks(
                tokenizer,
                row["selector_text"],
                maximum_tokens=chunk_tokens,
                overlap_tokens=overlap_tokens,
            )
            chunk_ids: list[str] = []
            chunk_metadata: list[dict[str, Any]] = []
            for chunk in chunks:
                text_id = register_text(
                    texts,
                    text=chunk.text,
                    local_proxy_tokens=chunk.token_count,
                    role={
                        "kind": "document_chunk",
                        "representation": representation,
                        "skill_id": row["skill_id"],
                        "chunk_index": chunk.chunk_index,
                    },
                )
                chunk_ids.append(text_id)
                chunk_metadata.append(
                    {
                        key: value
                        for key, value in chunk.to_dict().items()
                        if key != "text"
                    }
                )
            documents.append(
                {
                    "source_row_index": row["source_row_index"],
                    "skill_id": row["skill_id"],
                    "selector_text_sha256": row["selector_text_sha256"],
                    "selector_utf8_bytes": row["selector_visible_counts"]["utf8_bytes"],
                    "source_length_quartile": length_quartiles[row["skill_id"]],
                    "chunk_text_ids": chunk_ids,
                    "chunks": chunk_metadata,
                }
            )
        document_maps[representation] = documents
        representation_chunking_seconds[representation] = time.perf_counter() - representation_started

    query_text_ids: dict[str, str] = {}
    query_serialization_started = time.perf_counter()
    for prompt in prompts:
        token_count = len(tokenizer_ids(tokenizer, prompt["prompt"]))
        require(token_count <= 8192, f"Qwen query exceeds provider limit: {prompt['prompt_id']}")
        query_text_ids[prompt["prompt_id"]] = register_text(
            texts,
            text=prompt["prompt"],
            local_proxy_tokens=token_count,
            role={"kind": "query", "prompt_id": prompt["prompt_id"]},
        )
    query_serialization_seconds = time.perf_counter() - query_serialization_started
    rows = [texts[text_id] for text_id in sorted(texts)]
    payload = {
        "documents": document_maps,
        "query_text_ids": query_text_ids,
        "preparation_timing": {
            "representation_chunking_seconds": representation_chunking_seconds,
            "query_serialization_seconds": query_serialization_seconds,
            "total_payload_serialization_seconds": (
                sum(representation_chunking_seconds.values())
                + query_serialization_seconds
            ),
        },
    }
    return rows, payload


def build(root: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    frozen_root = version_root(root)
    representations = load_representations(root)
    prompts_path = frozen_root / "prompt_manifest.jsonl"
    prompts = read_jsonl(prompts_path)
    token_audit_path = root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"
    token_audit = read_json(token_audit_path)
    qwen = token_audit["qwen"]
    tokenizer_path = Path(qwen["local_proxy_tokenizer_snapshot"])
    require(sha256_file(tokenizer_path / "tokenizer.json") == qwen["local_proxy_tokenizer_sha256"], "Qwen proxy tokenizer drift")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    text_rows, payload_maps = build_payload_data(
        tokenizer,
        representations,
        prompts,
        chunk_tokens=int(qwen["proposed_chunk_tokens"]),
        overlap_tokens=int(qwen["proposed_overlap_tokens"]),
    )
    document_text_rows = [
        row
        for row in text_rows
        if any(role["kind"] == "document_chunk" for role in row["roles"])
    ]
    query_text_rows = [
        row
        for row in text_rows
        if any(role["kind"] == "query" for role in row["roles"])
    ]
    shared_text_rows = [
        row
        for row in text_rows
        if any(role["kind"] == "document_chunk" for role in row["roles"])
        and any(role["kind"] == "query" for role in row["roles"])
    ]
    output_root = frozen_root / "qwen_payload"
    staging = frozen_root / ".qwen_payload.staging"
    require(not output_root.exists(), f"Qwen payload root already exists: {output_root}")
    require(not staging.exists(), f"Stale Qwen payload staging root: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    text_path = staging / "text_inventory.jsonl"
    write_jsonl_new(text_path, text_rows)
    manifest = {
        "schema_version": "rq2b-qwen-payload-manifest-v1",
        "version_id": VERSION_ID,
        "state": "sealed_not_executed",
        "network_calls": 0,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "chunker_version": CHUNKER_VERSION,
        "chunk_tokens": qwen["proposed_chunk_tokens"],
        "overlap_tokens": qwen["proposed_overlap_tokens"],
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "text_inventory": {
            "path": relative(output_root / text_path.name, root),
            "sha256": sha256_file(text_path),
            "rows": len(text_rows),
        },
        "representation_inputs": {
            name: {
                "path": relative(path, root),
                "sha256": sha256_file(path),
                "rows": len(rows),
            }
            for name, (path, rows) in representations.items()
        },
        "prompt_manifest": {
            "path": relative(prompts_path, root),
            "sha256": sha256_file(prompts_path),
            "rows": len(prompts),
        },
        "counts": {
            "unique_texts": len(text_rows),
            "local_proxy_tokens": sum(int(row["local_proxy_tokens"]) for row in text_rows),
            "utf8_bytes": sum(int(row["utf8_bytes"]) for row in text_rows),
            "unique_document_texts": len(document_text_rows),
            "unique_query_texts": len(query_text_rows),
            "shared_document_query_texts": len(shared_text_rows),
            "query_prompt_instances": len(prompts),
            "cold_query_requests": len(query_text_rows),
            "maximum_external_text_submissions_without_document_cache": len(document_text_rows) + len(query_text_rows),
            "maximum_external_submission_proxy_tokens_without_document_cache": sum(
                int(row["local_proxy_tokens"])
                for row in [*document_text_rows, *query_text_rows]
            ),
            "maximum_external_submission_utf8_bytes_without_document_cache": sum(
                int(row["utf8_bytes"])
                for row in [*document_text_rows, *query_text_rows]
            ),
            "maximum_request_attempts_without_document_cache": (
                math.ceil(len(document_text_rows) / MAX_BATCH_TEXTS)
                + len(query_text_rows)
            ),
            "document_instances": sum(len(rows) for rows in payload_maps["documents"].values()),
            "document_chunks": sum(
                len(row["chunk_text_ids"])
                for rows in payload_maps["documents"].values()
                for row in rows
            ),
        },
        "documents": payload_maps["documents"],
        "query_text_ids": payload_maps["query_text_ids"],
        "preparation_timing": payload_maps["preparation_timing"],
        "authorization_boundary": {
            "external_transfer_authorized": False,
            "paid_api_authorized": False,
            "execution_authorisation_required": True,
            "cold_query_latency_measurement_requires_batch_size_one": True,
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    class CharacterTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
            del add_special_tokens
            return [ord(character) for character in text]

        def __call__(self, text: str, **_: Any) -> dict[str, Any]:
            return {
                "input_ids": self.encode(text),
                "offset_mapping": [(index, index + 1) for index in range(len(text))],
            }

    representations = {
        "i1-discovery": (
            Path("synthetic-i1.jsonl"),
            [
                {
                    "source_row_index": 0,
                    "skill_id": "alpha",
                    "selector_text": "alpha body",
                    "selector_text_sha256": sha256_text("alpha body"),
                    "selector_visible_counts": {"utf8_bytes": len("alpha body".encode("utf-8"))},
                }
            ],
        ),
        "i2-original": (
            Path("synthetic-i2.jsonl"),
            [
                {
                    "source_row_index": 0,
                    "skill_id": "alpha",
                    "selector_text": "alpha body\n\nlong tail",
                    "selector_text_sha256": sha256_text("alpha body\n\nlong tail"),
                    "selector_visible_counts": {"utf8_bytes": len("alpha body\n\nlong tail".encode("utf-8"))},
                }
            ],
        ),
    }
    prompts = [{"prompt_id": "p1", "prompt": "alpha request"}]
    rows, payload = build_payload_data(
        CharacterTokenizer(),
        representations,
        prompts,
        chunk_tokens=12,
        overlap_tokens=2,
    )
    require(len(payload["query_text_ids"]) == 1, "Qwen payload query reuse self-test failed")
    require(sum(len(value) for value in payload["documents"].values()) == 2, "Qwen payload document self-test failed")
    require(all(row["local_proxy_tokens"] <= 12 for row in rows if not any(role["kind"] == "query" for role in row["roles"])), "Qwen payload chunk ceiling self-test failed")
    return {
        "state": "synthetic_payload_not_transmitted",
        "network_calls": 0,
        "unique_texts": len(rows),
        "query_texts": len(payload["query_text_ids"]),
        "document_instances": 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = self_test() if args.self_test else build(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
