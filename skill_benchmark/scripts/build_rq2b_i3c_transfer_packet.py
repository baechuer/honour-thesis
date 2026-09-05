#!/usr/bin/env python3
"""Build and verify the local RQ2b I3C extraction packet without transfer."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from rq2b_common import (
    FIELD_SPECS,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    verify_frozen_manifest,
    version_root,
    write_json_new,
    write_jsonl_new,
)


PACKET_VERSION = "rq2b-i3c-transfer-packet-v2"
MAX_ROWS_PER_CHUNK = 50
MAX_PROXY_TOKENS_PER_CHUNK = 60_000
ALLOWED_INPUT_KEYS = {
    "source_row_index",
    "skill_id",
    "name",
    "description",
    "family",
    "source",
    "source_sha256",
    "text",
}
PROHIBITED_KEYS = {
    "prompt",
    "prompt_id",
    "gold_skill",
    "acceptable_skills",
    "valid_skills",
    "closest_alternatives",
    "stratum",
    "group",
    "role",
    "retrieval_result",
}


def chunks_by_limits(
    rows: list[dict[str, Any]],
    token_counts: dict[str, int],
) -> list[list[dict[str, Any]]]:
    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_tokens = 0
    for row in rows:
        tokens = token_counts[row["skill_id"]]
        require(tokens <= MAX_PROXY_TOKENS_PER_CHUNK, f"Single source exceeds chunk token ceiling: {row['skill_id']}")
        if current and (
            len(current) >= MAX_ROWS_PER_CHUNK
            or current_tokens + tokens > MAX_PROXY_TOKENS_PER_CHUNK
        ):
            chunks.append(current)
            current = []
            current_tokens = 0
        current.append(row)
        current_tokens += tokens
    if current:
        chunks.append(current)
    return chunks


def input_row(source: dict[str, Any], i2: dict[str, Any]) -> dict[str, Any]:
    require(source["skill_id"] == i2["skill_id"], "I3C packet source/I2 identity mismatch")
    require(source["source_row_index"] == i2["source_row_index"], "I3C packet row-index mismatch")
    require(i2["selector_text_sha256"] == source["source_sha256"], "I3C packet I2 hash mismatch")
    return {
        "source_row_index": source["source_row_index"],
        "skill_id": source["skill_id"],
        "name": source["source_name"],
        "description": source["source_description"],
        "family": source["family"],
        "source": source["source_path"],
        "source_sha256": source["source_sha256"],
        "text": i2["selector_text"],
    }


def build(root: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    verify_frozen_manifest(root)
    frozen_root = version_root(root)
    representation_manifest = read_json(frozen_root / "representations" / "manifest.json")
    require(
        representation_manifest.get("state") == "local_i1_i2_built_no_scientific_run",
        "I1/I2 representations are not ready",
    )
    source_manifest_path = frozen_root / "source_manifest.jsonl"
    i2_path = root / representation_manifest["artifacts"]["i2-original"]["path"]
    token_audit_path = root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"
    extraction_prompt_path = root / "skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md"
    sources = read_jsonl(source_manifest_path)
    i2_rows = read_jsonl(i2_path)
    token_audit = read_json(token_audit_path)
    require(token_audit.get("network_calls") == 0, "Token audit is not zero-network")
    qwen = token_audit["qwen"]
    tokenizer_path = Path(qwen["local_proxy_tokenizer_snapshot"])
    require(
        sha256_file(tokenizer_path / "tokenizer.json")
        == qwen["local_proxy_tokenizer_sha256"],
        "I3C packet proxy tokenizer drift",
    )
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    token_counts = {
        row["skill_id"]: len(
            tokenizer.encode(row["selector_text"], add_special_tokens=False)
        )
        for row in i2_rows
    }
    require(len(token_counts) == 2433, "Token audit identity count mismatch")
    packet_rows = [
        input_row(source, i2)
        for source, i2 in zip(sources, i2_rows, strict=True)
    ]
    chunks = chunks_by_limits(packet_rows, token_counts)

    output_root = frozen_root / "i3c_extraction"
    staging_root = frozen_root / ".i3c_extraction.staging"
    require(not output_root.exists(), f"I3C extraction root already exists: {output_root}")
    require(not staging_root.exists(), f"Stale I3C staging root: {staging_root}")
    input_root = staging_root / "inputs"
    input_root.mkdir(parents=True, exist_ok=False)
    chunk_records: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    for chunk_index, chunk in enumerate(chunks):
        first_index = chunk[0]["source_row_index"]
        last_index = chunk[-1]["source_row_index"]
        filename = f"i3c_input_{chunk_index:04d}_{first_index:04d}_{last_index:04d}.jsonl"
        path = input_root / filename
        write_jsonl_new(path, chunk)
        proxy_tokens = sum(token_counts[row["skill_id"]] for row in chunk)
        chunk_records.append(
            {
                "chunk_index": chunk_index,
                "input_path": relative(output_root / "inputs" / filename, root),
                "input_sha256": sha256_file(path),
                "expected_output_path": relative(
                    output_root / "outputs" / filename.replace("i3c_input_", "i3c_output_"),
                    root,
                ),
                "row_count": len(chunk),
                "first_source_row_index": first_index,
                "last_source_row_index": last_index,
                "qwen_proxy_tokens": proxy_tokens,
                "utf8_bytes": path.stat().st_size,
            }
        )
        for chunk_row_index, row in enumerate(chunk):
            identity_rows.append(
                {
                    "source_row_index": row["source_row_index"],
                    "skill_id": row["skill_id"],
                    "source": row["source"],
                    "source_sha256": row["source_sha256"],
                    "text_sha256": sha256_text(row["text"]),
                    "chunk_index": chunk_index,
                    "chunk_row_index": chunk_row_index,
                    "qwen_proxy_tokens": token_counts[row["skill_id"]],
                }
            )

    identity_path = staging_root / "identity_manifest.jsonl"
    write_jsonl_new(identity_path, identity_rows)
    manifest = {
        "schema_version": PACKET_VERSION,
        "version_id": VERSION_ID,
        "state": "built_not_transmitted",
        "network_calls": 0,
        "external_texts_transmitted": 0,
        "worker_count": 0,
        "source_manifest": {
            "path": relative(source_manifest_path, root),
            "sha256": sha256_file(source_manifest_path),
        },
        "i2_representation": {
            "path": relative(i2_path, root),
            "sha256": sha256_file(i2_path),
        },
        "extraction_prompt": {
            "path": relative(extraction_prompt_path, root),
            "sha256": sha256_file(extraction_prompt_path),
        },
        "token_audit": {
            "path": relative(token_audit_path, root),
            "sha256": sha256_file(token_audit_path),
        },
        "packet_token_counting": {
            "policy": "tokenize_exact_i2_decoded_text_without_universal_newline_conversion",
            "tokenizer_snapshot": str(tokenizer_path),
            "tokenizer_sha256": qwen["local_proxy_tokenizer_sha256"],
        },
        "fields": [field for field, _ in FIELD_SPECS],
        "chunk_policy": {
            "maximum_rows": MAX_ROWS_PER_CHUNK,
            "maximum_qwen_proxy_tokens": MAX_PROXY_TOKENS_PER_CHUNK,
            "ordering": "frozen_source_row_index_ascending",
        },
        "counts": {
            "input_rows": len(packet_rows),
            "chunks": len(chunk_records),
            "total_qwen_proxy_tokens": sum(token_counts.values()),
            "total_source_utf8_bytes": sum(
                len(row["text"].encode("utf-8")) for row in packet_rows
            ),
        },
        "identity_manifest": {
            "path": relative(output_root / identity_path.name, root),
            "sha256": sha256_file(identity_path),
            "rows": len(identity_rows),
        },
        "chunks": chunk_records,
        "authorization_boundary": {
            "packet_build_authorized": True,
            "source_transfer_authorized": False,
            "paid_api_authorized": False,
            "hosted_compute_authorized": False,
        },
    }
    write_json_new(staging_root / "manifest.json", manifest)
    staging_root.replace(output_root)
    return verify(root)


def verify(root: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    frozen_root = version_root(root)
    output_root = frozen_root / "i3c_extraction"
    manifest_path = output_root / "manifest.json"
    require(manifest_path.exists(), f"I3C extraction manifest missing: {manifest_path}")
    manifest = read_json(manifest_path)
    require(manifest.get("schema_version") == PACKET_VERSION, "I3C packet schema mismatch")
    require(manifest.get("version_id") == VERSION_ID, "I3C packet version mismatch")
    require(manifest.get("state") == "built_not_transmitted", "Unsafe I3C packet state")
    require(manifest.get("network_calls") == 0, "I3C packet used network")
    require(manifest.get("external_texts_transmitted") == 0, "I3C packet was transmitted")
    require(manifest.get("worker_count") == 0, "I3C extraction workers were started")
    require(manifest["authorization_boundary"]["source_transfer_authorized"] is False, "I3C transfer boundary missing")

    identity_path = root / manifest["identity_manifest"]["path"]
    require(sha256_file(identity_path) == manifest["identity_manifest"]["sha256"], "I3C identity manifest drift")
    identities = read_jsonl(identity_path)
    require(len(identities) == 2433, "I3C identity manifest row count mismatch")
    seen: set[str] = set()
    total_rows = 0
    total_tokens = 0
    total_source_bytes = 0
    for chunk in manifest["chunks"]:
        path = root / chunk["input_path"]
        require(path.exists(), f"I3C input chunk missing: {path}")
        require(sha256_file(path) == chunk["input_sha256"], f"I3C chunk drift: {path}")
        rows = read_jsonl(path)
        require(len(rows) == chunk["row_count"], f"I3C chunk row count drift: {path}")
        require(len(rows) <= MAX_ROWS_PER_CHUNK, f"I3C chunk row ceiling exceeded: {path}")
        chunk_tokens = 0
        for row in rows:
            require(set(row) == ALLOWED_INPUT_KEYS, f"I3C input key mismatch: {row.get('skill_id')}")
            require(not (set(row) & PROHIBITED_KEYS), f"I3C role leakage: {row.get('skill_id')}")
            skill_id = row["skill_id"]
            require(skill_id not in seen, f"Duplicate I3C input skill: {skill_id}")
            seen.add(skill_id)
            require(sha256_text(row["text"]) == row["source_sha256"], f"I3C source hash mismatch: {skill_id}")
            identity = identities[row["source_row_index"]]
            require(identity["skill_id"] == skill_id, f"I3C identity alignment mismatch: {skill_id}")
            require(identity["chunk_index"] == chunk["chunk_index"], f"I3C chunk alignment mismatch: {skill_id}")
            chunk_tokens += int(identity["qwen_proxy_tokens"])
            total_source_bytes += len(row["text"].encode("utf-8"))
        require(chunk_tokens == chunk["qwen_proxy_tokens"], f"I3C chunk token drift: {path}")
        require(chunk_tokens <= MAX_PROXY_TOKENS_PER_CHUNK, f"I3C chunk token ceiling exceeded: {path}")
        total_rows += len(rows)
        total_tokens += chunk_tokens
    require(len(seen) == 2433, "I3C input identity coverage mismatch")
    require(total_rows == manifest["counts"]["input_rows"], "I3C total row drift")
    require(total_tokens == manifest["counts"]["total_qwen_proxy_tokens"], "I3C total token drift")
    require(total_source_bytes == manifest["counts"]["total_source_utf8_bytes"], "I3C total byte drift")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = verify(root) if args.verify_only else build(root)
    print(
        json.dumps(
            {
                "version_id": manifest["version_id"],
                "state": manifest["state"],
                "counts": manifest["counts"],
                "maximum_chunk_rows": max(row["row_count"] for row in manifest["chunks"]),
                "maximum_chunk_proxy_tokens": max(row["qwen_proxy_tokens"] for row in manifest["chunks"]),
                "external_texts_transmitted": manifest["external_texts_transmitted"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
