#!/usr/bin/env python3
"""Build the exact full-context SkillRouter-embedding payload for RQ2b."""

from __future__ import annotations

import argparse
import json
import os
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
    sha256_text,
    source_length_quartiles,
    verify_b0f_a1_amendment,
    verify_b1s_implementation_seal,
    verify_frozen_manifest,
    verify_i3c_retrieval_ready,
    version_root,
    write_json_new,
    write_jsonl_new,
)
from run_rq2b_skillrouter_embedding import (
    DIMENSIONS,
    MAX_MODEL_TOKENS,
    MODEL,
    MODEL_CONFIG_SHA256,
    MODEL_WEIGHTS_SHA256,
    QUERY_INSTRUCTION,
    REVISION,
    TOKENIZER_SHA256,
)


REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
)
DEFAULT_SNAPSHOT = Path.home() / (
    ".cache/huggingface/hub/models--pipizhao--SkillRouter-Embedding-0.6B/"
    "snapshots/c03c9bcee9fce92ab0262bb6dcf54d174a8ba558"
)


def model_token_count(tokenizer: Any, text: str) -> int:
    token_ids = tokenizer.encode(text, add_special_tokens=True)
    require(isinstance(token_ids, list), "SkillRouter tokenizer returned invalid token IDs")
    return len(token_ids)


def load_representations(root: Path) -> dict[str, tuple[Path, list[dict[str, Any]]]]:
    frozen_root = version_root(root)
    base_manifest = read_json(frozen_root / "representations" / "manifest.json")
    i3_manifest = read_json(frozen_root / "i3c_merged" / "manifest.json")
    verify_i3c_retrieval_ready(root)
    loaded: dict[str, tuple[Path, list[dict[str, Any]]]] = {}
    for representation in REPRESENTATIONS:
        manifest = base_manifest if representation in base_manifest["artifacts"] else i3_manifest
        artifact = manifest["artifacts"][representation]
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], f"Representation drift: {representation}")
        rows = read_jsonl(path)
        require(len(rows) == 2433, f"Representation row count mismatch: {representation}")
        loaded[representation] = (path, rows)
    return loaded


def register_text(
    texts: dict[str, dict[str, Any]],
    *,
    text: str,
    token_count: int,
    role: dict[str, Any],
) -> str:
    require(0 < token_count <= MAX_MODEL_TOKENS, "SkillRouter payload text exceeds full-context limit")
    text_id = sha256_text(text)
    existing = texts.get(text_id)
    if existing is None:
        texts[text_id] = {
            "schema_version": "rq2b-skillrouter-embedding-payload-text-v1",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "model_tokens": token_count,
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "SHA-256 collision in SkillRouter embedding payload")
        require(existing["model_tokens"] == token_count, "Token-count drift for identical payload text")
        existing["roles"].append(role)
    return text_id


def build_payload_data(
    tokenizer: Any,
    representations: dict[str, tuple[Path, list[dict[str, Any]]]],
    prompts: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    texts: dict[str, dict[str, Any]] = {}
    documents: dict[str, list[dict[str, Any]]] = {}
    representation_seconds: dict[str, float] = {}
    for representation, (_, rows) in representations.items():
        started = time.perf_counter()
        quartiles = source_length_quartiles(rows)
        documents[representation] = []
        for row in rows:
            text = row["selector_text"]
            token_count = model_token_count(tokenizer, text)
            text_id = register_text(
                texts,
                text=text,
                token_count=token_count,
                role={
                    "kind": "document",
                    "representation": representation,
                    "skill_id": row["skill_id"],
                },
            )
            documents[representation].append(
                {
                    "source_row_index": row["source_row_index"],
                    "skill_id": row["skill_id"],
                    "selector_text_sha256": row["selector_text_sha256"],
                    "selector_utf8_bytes": row["selector_visible_counts"]["utf8_bytes"],
                    "source_length_quartile": quartiles[row["skill_id"]],
                    "text_id": text_id,
                    "model_tokens": token_count,
                }
            )
        representation_seconds[representation] = time.perf_counter() - started

    query_text_ids: dict[str, str] = {}
    query_started = time.perf_counter()
    for prompt in prompts:
        query_text = QUERY_INSTRUCTION + prompt["prompt"]
        token_count = model_token_count(tokenizer, query_text)
        query_text_ids[prompt["prompt_id"]] = register_text(
            texts,
            text=query_text,
            token_count=token_count,
            role={
                "kind": "query",
                "prompt_id": prompt["prompt_id"],
                "raw_prompt_sha256": prompt["prompt_sha256"],
            },
        )
    query_seconds = time.perf_counter() - query_started
    return [texts[text_id] for text_id in sorted(texts)], {
        "documents": documents,
        "query_text_ids": query_text_ids,
        "preparation_timing": {
            "representation_tokenization_seconds": representation_seconds,
            "query_tokenization_seconds": query_seconds,
            "total_payload_serialization_seconds": sum(representation_seconds.values()) + query_seconds,
        },
    }


def verify_snapshot_for_payload(snapshot: Path) -> dict[str, Any]:
    tokenizer_path = snapshot / "tokenizer.json"
    config_path = snapshot / "config.json"
    require(tokenizer_path.is_file(), f"SkillRouter embedding tokenizer missing: {tokenizer_path}")
    require(config_path.is_file(), f"SkillRouter embedding config missing: {config_path}")
    require(sha256_file(tokenizer_path) == TOKENIZER_SHA256, "SkillRouter embedding tokenizer drift")
    require(sha256_file(config_path) == MODEL_CONFIG_SHA256, "SkillRouter embedding config drift")
    weights_path = snapshot / "model.safetensors"
    return {
        "path": str(snapshot),
        "tokenizer_sha256": TOKENIZER_SHA256,
        "config_sha256": MODEL_CONFIG_SHA256,
        "weights_expected_sha256": MODEL_WEIGHTS_SHA256,
        "weights_present_and_verified": (
            weights_path.is_file() and sha256_file(weights_path) == MODEL_WEIGHTS_SHA256
        ),
    }


def build(root: Path, snapshot: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    verify_frozen_manifest(root)
    verify_b0f_a1_amendment(root)
    verify_b1s_implementation_seal(root)
    snapshot_audit = verify_snapshot_for_payload(snapshot)
    tokenizer = AutoTokenizer.from_pretrained(
        snapshot,
        local_files_only=True,
        trust_remote_code=True,
        padding_side="left",
    )
    representations = load_representations(root)
    frozen_root = version_root(root)
    prompt_path = frozen_root / "prompt_manifest.jsonl"
    prompts = read_jsonl(prompt_path)
    text_rows, maps = build_payload_data(tokenizer, representations, prompts)
    document_rows = [row for row in text_rows if any(role["kind"] == "document" for role in row["roles"])]
    query_rows = [row for row in text_rows if any(role["kind"] == "query" for role in row["roles"])]
    output_root = frozen_root / "skillrouter_embedding_payload"
    staging = frozen_root / ".skillrouter_embedding_payload.staging"
    require(not output_root.exists(), f"SkillRouter embedding payload exists: {output_root}")
    require(not staging.exists(), f"Stale SkillRouter embedding payload staging root: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    inventory_path = staging / "text_inventory.jsonl"
    write_jsonl_new(inventory_path, text_rows)
    manifest = {
        "schema_version": "rq2b-skillrouter-embedding-payload-manifest-v1",
        "version_id": VERSION_ID,
        "state": "sealed_not_executed",
        "network_calls": 0,
        "b0f_a1_amendment_sha256": B0F_A1_AMENDMENT_SHA256,
        "model": MODEL,
        "revision": REVISION,
        "dimensions": DIMENSIONS,
        "maximum_model_tokens": MAX_MODEL_TOKENS,
        "pooling": "last_non_padding_token",
        "normalization": "l2",
        "score": "cosine",
        "query_instruction": QUERY_INSTRUCTION,
        "document_serialization": "exact_representation_selector_text",
        "truncation": "forbidden",
        "snapshot_audit": snapshot_audit,
        "text_inventory": {
            "path": relative(output_root / inventory_path.name, root),
            "sha256": sha256_file(inventory_path),
            "rows": len(text_rows),
        },
        "representation_inputs": {
            name: {"path": relative(path, root), "sha256": sha256_file(path), "rows": len(rows)}
            for name, (path, rows) in representations.items()
        },
        "prompt_manifest": {
            "path": relative(prompt_path, root),
            "sha256": sha256_file(prompt_path),
            "rows": len(prompts),
        },
        "documents": maps["documents"],
        "query_text_ids": maps["query_text_ids"],
        "preparation_timing": maps["preparation_timing"],
        "counts": {
            "unique_texts": len(text_rows),
            "unique_document_texts": len(document_rows),
            "unique_query_texts": len(query_rows),
            "document_instances": sum(len(rows) for rows in maps["documents"].values()),
            "query_instances": len(prompts),
            "model_tokens": sum(int(row["model_tokens"]) for row in text_rows),
            "utf8_bytes": sum(int(row["utf8_bytes"]) for row in text_rows),
            "maximum_text_tokens": max(int(row["model_tokens"]) for row in text_rows),
        },
        "authorization_boundary": {
            "scientific_execution_authorized": False,
            "hosted_transfer_authorized": False,
            "model_download_authorized": False,
            "execution_authorisation_required": True,
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    class CharacterTokenizer:
        def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
            del add_special_tokens
            return [ord(character) for character in text]

    representations = {
        representation: (
            Path(f"{representation}.jsonl"),
            [
                {
                    "source_row_index": index,
                    "skill_id": f"s{index}",
                    "selector_text": f"{representation} document {index}",
                    "selector_text_sha256": sha256_text(f"{representation} document {index}"),
                    "selector_visible_counts": {"utf8_bytes": len(f"{representation} document {index}")},
                }
                for index in range(2)
            ],
        )
        for representation in REPRESENTATIONS
    }
    prompts = [
        {
            "prompt_id": "p1",
            "prompt": "route this task",
            "prompt_sha256": sha256_text("route this task"),
        }
    ]
    rows, payload = build_payload_data(CharacterTokenizer(), representations, prompts)
    require(sum(len(values) for values in payload["documents"].values()) == 8, "Document matrix regression")
    query_id = payload["query_text_ids"]["p1"]
    query_row = next(row for row in rows if row["text_id"] == query_id)
    require(query_row["text"].startswith(QUERY_INSTRUCTION), "Query instruction regression")
    require(all(int(row["model_tokens"]) <= MAX_MODEL_TOKENS for row in rows), "Token ceiling regression")
    return {
        "state": "synthetic_payload_no_model_forward_no_transfer",
        "network_calls": 0,
        "document_instances": 8,
        "query_instances": 1,
        "query_instruction_bound": True,
        "no_truncation": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--model-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = self_test() if args.self_test else build(args.root.resolve(), args.model_snapshot.expanduser().resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
