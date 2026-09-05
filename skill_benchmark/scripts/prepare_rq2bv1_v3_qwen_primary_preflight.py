#!/usr/bin/env python3
"""Build a local-only, approval-bound Qwen primary payload for RQ2b V3.

This script does not contact DashScope, load a remote model, rank prompts, or
write thesis material.  It replays the final V3/B1L integrity predicates,
losslessly chunks the four frozen representations, and freezes an exact text
inventory plus an execution packet for a later separately authorised run.
"""

from __future__ import annotations

import argparse
import math
import os
import time
from pathlib import Path
from typing import Any

from prepare_rq2b_i3c_v3_b1l_preflight import REPRESENTATIONS
from rq2b_chunking import CHUNKER_VERSION, exact_text_chunks, tokenizer_ids
from rq2b_common import (
    read_json,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    source_length_quartiles,
    write_json_new,
    write_jsonl_new,
)
from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight
from run_rq2b_qwen import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL


PREFLIGHT_VERSION = "rq2bv1-v3-qwen-primary-preflight-v1"
PREFLIGHT_ROOT = "skill_benchmark/rq2bv1/preflight/qwen_primary_v3"
TEXT_INVENTORY_NAME = "text_inventory.jsonl"
PAYLOAD_NAME = "payload_manifest.json"
REPORT_NAME = "preflight_report.json"
CHECKPOINT_NAME = "preflight_checkpoint.json"
EXECUTION_PACKET_NAME = "execution_approval_packet.json"
RUNNER_PATH = "skill_benchmark/scripts/run_rq2bv1_v3_qwen_primary.py"
RUNNER_DEPENDENCIES = (
    RUNNER_PATH,
    "skill_benchmark/scripts/run_rq2b_qwen.py",
    "skill_benchmark/scripts/run_rq2b_bm25.py",
    "skill_benchmark/scripts/rq2b_chunking.py",
    "skill_benchmark/scripts/rq2b_common.py",
    "skill_benchmark/scripts/rq2b_v11_execution_contract.py",
)
CACHE_ROOT = "skill_benchmark/cache/rq2bv1/embeddings"
RESULT_ROOT = "skill_benchmark/rq2bv1/results/qwen_primary_v3"
RUN_ID = "rq2bv1-v3-qwen-primary-001"
TIMEOUT_SECONDS = 120


def register_text(
    texts: dict[str, dict[str, Any]],
    *,
    text: str,
    local_proxy_tokens: int,
    role: dict[str, Any],
) -> str:
    require(bool(text), "Cannot register empty Qwen selector text")
    text_id = sha256_text(text)
    existing = texts.get(text_id)
    if existing is None:
        texts[text_id] = {
            "schema_version": "rq2bv1-qwen-primary-text-v1",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "local_proxy_tokens": int(local_proxy_tokens),
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "SHA-256 collision in Qwen text inventory")
        require(
            int(existing["local_proxy_tokens"]) == int(local_proxy_tokens),
            "Proxy-token count drift for shared Qwen text",
        )
        existing["roles"].append(role)
    return text_id


def build_payload_data(
    tokenizer: Any,
    representations: dict[str, list[dict[str, Any]]],
    prompts: list[dict[str, Any]],
    *,
    chunk_tokens: int,
    overlap_tokens: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    texts: dict[str, dict[str, Any]] = {}
    documents_by_representation: dict[str, list[dict[str, Any]]] = {}
    chunking_seconds: dict[str, float] = {}
    for representation in REPRESENTATIONS:
        rows = representations[representation]
        require(len(rows) == 2433, f"Candidate count drift: {representation}")
        started = time.perf_counter()
        quartiles = source_length_quartiles(rows)
        documents: list[dict[str, Any]] = []
        for row in rows:
            selector_text = str(row["selector_text"])
            selector_tokens = len(tokenizer_ids(tokenizer, selector_text))
            chunks = exact_text_chunks(
                tokenizer,
                selector_text,
                maximum_tokens=chunk_tokens,
                overlap_tokens=overlap_tokens,
            )
            chunk_ids: list[str] = []
            chunk_metadata: list[dict[str, Any]] = []
            for chunk in chunks:
                chunk_ids.append(
                    register_text(
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
                )
                chunk_metadata.append(
                    {key: value for key, value in chunk.to_dict().items() if key != "text"}
                )
            documents.append(
                {
                    "source_row_index": int(row["source_row_index"]),
                    "skill_id": str(row["skill_id"]),
                    "selector_text_sha256": str(row["selector_text_sha256"]),
                    "selector_utf8_bytes": int(row["selector_visible_counts"]["utf8_bytes"]),
                    "selector_local_proxy_tokens": selector_tokens,
                    "source_length_quartile": quartiles[str(row["skill_id"])],
                    "chunk_text_ids": chunk_ids,
                    "chunks": chunk_metadata,
                }
            )
        require(
            [document["skill_id"] for document in documents]
            == [row["skill_id"] for row in rows],
            f"Candidate ordering drift while chunking {representation}",
        )
        documents_by_representation[representation] = documents
        chunking_seconds[representation] = time.perf_counter() - started

    query_started = time.perf_counter()
    query_text_ids: dict[str, str] = {}
    for prompt in prompts:
        prompt_text = str(prompt["prompt"])
        token_count = len(tokenizer_ids(tokenizer, prompt_text))
        require(token_count <= 8192, f"Query exceeds Qwen limit: {prompt['prompt_id']}")
        query_text_ids[str(prompt["prompt_id"])] = register_text(
            texts,
            text=prompt_text,
            local_proxy_tokens=token_count,
            role={"kind": "query", "prompt_id": str(prompt["prompt_id"])},
        )
    query_seconds = time.perf_counter() - query_started
    rows = [texts[text_id] for text_id in sorted(texts)]
    for row in rows:
        row["roles"] = sorted(
            row["roles"],
            key=lambda role: (
                str(role["kind"]),
                str(role.get("representation", "")),
                str(role.get("skill_id", "")),
                int(role.get("chunk_index", -1)),
                str(role.get("prompt_id", "")),
            ),
        )
    return rows, {
        "documents": documents_by_representation,
        "query_text_ids": query_text_ids,
        "preparation_timing": {
            "representation_chunking_seconds": chunking_seconds,
            "query_serialization_seconds": query_seconds,
            "total_payload_serialization_seconds": sum(chunking_seconds.values()) + query_seconds,
        },
    }


def build(root: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    # `verify_preflight` replays the automatic V3 source/I3C predicates and
    # binds the 381 strict prompts and all four representation artefacts.
    b1l_report, representations, prompts = verify_preflight(root)
    require(len(prompts) == 381, "Strict prompt population drift")
    require(set(representations) == set(REPRESENTATIONS), "Representation set drift")

    token_audit_path = root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"
    token_audit = read_json(token_audit_path)
    qwen = token_audit["qwen"]
    tokenizer_path = Path(qwen["local_proxy_tokenizer_snapshot"])
    tokenizer_file = tokenizer_path / "tokenizer.json"
    require(tokenizer_file.is_file(), f"Qwen proxy tokenizer missing: {tokenizer_file}")
    require(
        sha256_file(tokenizer_file) == qwen["local_proxy_tokenizer_sha256"],
        "Qwen proxy tokenizer hash drift",
    )
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)

    text_rows, payload_maps = build_payload_data(
        tokenizer,
        representations,
        prompts,
        chunk_tokens=int(qwen["proposed_chunk_tokens"]),
        overlap_tokens=int(qwen["proposed_overlap_tokens"]),
    )
    document_text_rows = [
        row for row in text_rows if any(role["kind"] == "document_chunk" for role in row["roles"])
    ]
    query_text_rows = [
        row for row in text_rows if any(role["kind"] == "query" for role in row["roles"])
    ]
    require(len(query_text_rows) == len(set(payload_maps["query_text_ids"].values())), "Query inventory drift")

    preflight_root = root / PREFLIGHT_ROOT
    staging = preflight_root.with_name(f".{preflight_root.name}.staging")
    require(not preflight_root.exists() and not staging.exists(), "Refusing to overwrite Qwen V3 preflight")
    staging.mkdir(parents=True, exist_ok=False)
    text_path = staging / TEXT_INVENTORY_NAME
    write_jsonl_new(text_path, text_rows)

    document_chunks = sum(
        len(document["chunk_text_ids"])
        for documents in payload_maps["documents"].values()
        for document in documents
    )
    selector_tokens_by_representation = {
        representation: sum(int(document["selector_local_proxy_tokens"]) for document in documents)
        for representation, documents in payload_maps["documents"].items()
    }
    payload = {
        "schema_version": "rq2bv1-v3-qwen-primary-payload-v1",
        "state": "sealed_not_executed",
        "network_calls": 0,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "chunker_version": CHUNKER_VERSION,
        "chunk_tokens": int(qwen["proposed_chunk_tokens"]),
        "overlap_tokens": int(qwen["proposed_overlap_tokens"]),
        "maximum_batch_texts": MAX_BATCH_TEXTS,
        "strict_population": {
            "candidate_library_skills": 2433,
            "strict_prompts": 381,
            "representations": list(REPRESENTATIONS),
            "expected_primary_result_rows": 381 * len(REPRESENTATIONS),
        },
        "b1l_preflight": {
            "path": b1l_report["strict_endpoint_contract"]["path"],
            "sha256": b1l_report["strict_endpoint_contract"]["sha256"],
            "source_preflight_report": {
                "path": relative(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/b1l_preflight_report.json", root),
                "sha256": sha256_file(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/b1l_preflight_report.json"),
            },
        },
        "text_inventory": {
            "path": relative(preflight_root / TEXT_INVENTORY_NAME, root),
            "sha256": sha256_file(text_path),
            "rows": len(text_rows),
        },
        "prompt_artifact": b1l_report["strict_scored_prompts"],
        "representation_inputs": b1l_report["representations"],
        "tokenizer": {
            "model": qwen["local_proxy_tokenizer_model"],
            "revision": qwen["local_proxy_tokenizer_revision"],
            "snapshot": str(tokenizer_path),
            "tokenizer_json_sha256": qwen["local_proxy_tokenizer_sha256"],
            "provider_documented_per_text_limit": int(qwen["provider_documented_per_text_limit"]),
        },
        "counts": {
            "unique_texts": len(text_rows),
            "unique_document_texts": len(document_text_rows),
            "unique_query_texts": len(query_text_rows),
            "document_instances": sum(len(rows) for rows in payload_maps["documents"].values()),
            "document_chunks": document_chunks,
            "selector_local_proxy_tokens_by_representation": selector_tokens_by_representation,
            "cold_query_requests": len(query_text_rows),
            "maximum_external_text_submissions_without_document_cache": len(document_text_rows) + len(query_text_rows),
            "maximum_external_submission_proxy_tokens_without_document_cache": sum(
                int(row["local_proxy_tokens"]) for row in [*document_text_rows, *query_text_rows]
            ),
            "maximum_external_submission_utf8_bytes_without_document_cache": sum(
                int(row["utf8_bytes"]) for row in [*document_text_rows, *query_text_rows]
            ),
            "maximum_new_cache_texts_without_document_cache": len(text_rows),
            "maximum_new_cache_proxy_tokens_without_document_cache": sum(
                int(row["local_proxy_tokens"]) for row in text_rows
            ),
            "maximum_new_cache_utf8_bytes_without_document_cache": sum(
                int(row["utf8_bytes"]) for row in text_rows
            ),
            "maximum_request_attempts_without_document_cache": (
                math.ceil(len(document_text_rows) / MAX_BATCH_TEXTS) + len(query_text_rows)
            ),
        },
        "documents": payload_maps["documents"],
        "query_text_ids": payload_maps["query_text_ids"],
        "preparation_timing": payload_maps["preparation_timing"],
        "execution_method": {
            "retriever": "qwen-text-embedding-v4",
            "document_aggregation": "maximum_chunk_cosine",
            "candidate_tie_break": "skill_id_ascending",
            "persisted_ranks": [1, 5, 20, 50, 100],
            "query_embedding_measurement": "one cold provider request per unique raw query text, batch size one",
            "document_embedding_cache": CACHE_ROOT,
            "automatic_retries": 0,
        },
        "authorisation_boundary": {
            "external_transfer_authorised": False,
            "paid_api_authorised": False,
            "execution_authorisation_required": True,
            "thesis_result_writing_authorised": False,
        },
    }
    payload_path = staging / PAYLOAD_NAME
    write_json_new(payload_path, payload)

    execution_scripts = [
        {"path": path, "sha256": sha256_file(root / path)} for path in RUNNER_DEPENDENCIES
    ]
    packet = {
        "schema_version": "rq2bv1-v3-qwen-primary-execution-approval-packet-v1",
        "state": "awaiting_explicit_external_transfer_authorisation",
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(payload_path)},
        "execution_scripts": execution_scripts,
        "run_id": RUN_ID,
        "output_dir": RESULT_ROOT,
        "cache_root": CACHE_ROOT,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "timeout_seconds": TIMEOUT_SECONDS,
        "automatic_retries": 0,
        "maximum_new_cache_texts": payload["counts"]["maximum_new_cache_texts_without_document_cache"],
        "maximum_new_cache_proxy_tokens": payload["counts"]["maximum_new_cache_proxy_tokens_without_document_cache"],
        "maximum_new_cache_utf8_bytes": payload["counts"]["maximum_new_cache_utf8_bytes_without_document_cache"],
        "maximum_external_text_submissions": payload["counts"]["maximum_external_text_submissions_without_document_cache"],
        "maximum_external_submission_proxy_tokens": payload["counts"]["maximum_external_submission_proxy_tokens_without_document_cache"],
        "maximum_external_submission_utf8_bytes": payload["counts"]["maximum_external_submission_utf8_bytes_without_document_cache"],
        "maximum_request_attempts": payload["counts"]["maximum_request_attempts_without_document_cache"],
        "maximum_successful_api_calls": payload["counts"]["maximum_request_attempts_without_document_cache"],
        "cold_query_requests": payload["counts"]["cold_query_requests"],
        "excluded_actions": [
            "no automatic retry",
            "no query-side field prediction or oracle routing",
            "no field-aware scoring in this primary execution",
            "no reranking",
            "no thesis LaTeX or PDF result writing",
        ],
    }
    packet_path = staging / EXECUTION_PACKET_NAME
    write_json_new(packet_path, packet)
    report = {
        "schema_version": "rq2bv1-v3-qwen-primary-preflight-report-v1",
        "state": "preflight_passed_no_network_no_scoring_external_authorisation_required",
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(payload_path)},
        "execution_packet": {"path": relative(preflight_root / EXECUTION_PACKET_NAME, root), "sha256": sha256_file(packet_path)},
        "strict_population": payload["strict_population"],
        "counts": payload["counts"],
        "validation": {
            "b1l_preflight_replayed": True,
            "tokenizer_hash_verified": True,
            "lossless_chunking_verified": True,
            "document_chunks_at_or_below_limit": document_chunks,
            "network_calls": 0,
            "scientific_retrieval_or_reranking": False,
        },
        "next_gate": "user_review_of_exact_packet_then_separate_external_transfer_authorisation",
    }
    report_path = staging / REPORT_NAME
    write_json_new(report_path, report)
    checkpoint = {
        "schema_version": "rq2bv1-v3-qwen-primary-preflight-checkpoint-v1",
        "state": "qwen_primary_preflight_frozen_external_authorisation_required",
        "report": {"path": relative(preflight_root / REPORT_NAME, root), "sha256": sha256_file(report_path)},
        "payload": report["payload"],
        "execution_packet": report["execution_packet"],
        "network_calls": 0,
    }
    write_json_new(staging / CHECKPOINT_NAME, checkpoint)
    staging.rename(preflight_root)
    return report


def self_test() -> dict[str, Any]:
    class CharacterTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
            del add_special_tokens
            return [ord(character) for character in text]

        def __call__(self, text: str, **_: Any) -> dict[str, Any]:
            return {"input_ids": self.encode(text), "offset_mapping": [(index, index + 1) for index in range(len(text))]}

    rows = [
        {
            "source_row_index": index,
            "skill_id": f"skill-{index:04d}",
            "selector_text": "alpha body\n\nlong tail",
            "selector_text_sha256": sha256_text("alpha body\n\nlong tail"),
            "selector_visible_counts": {"utf8_bytes": len("alpha body\n\nlong tail".encode("utf-8"))},
        }
        for index in range(2433)
    ]
    representations = {representation: [dict(row) for row in rows] for representation in REPRESENTATIONS}
    prompts = [
        {
            "prompt_id": "p1",
            "prompt": "alpha request",
            "prompt_sha256": sha256_text("alpha request"),
            "stratum": "controlled",
            "group": "synthetic",
            "gold_skill": "skill-0000",
        }
    ]
    text_rows, payload = build_payload_data(
        CharacterTokenizer(), representations, prompts, chunk_tokens=12, overlap_tokens=2
    )
    require(len(payload["documents"]) == 4, "Synthetic representation matrix mismatch")
    require(len(payload["query_text_ids"]) == 1, "Synthetic query map mismatch")
    require(all(int(row["local_proxy_tokens"]) <= 12 for row in text_rows if any(role["kind"] == "document_chunk" for role in row["roles"])), "Synthetic chunk limit mismatch")
    return {
        "schema_version": "rq2bv1-v3-qwen-primary-preflight-self-test-v1",
        "state": "self_test_passed",
        "network_calls": 0,
        "scientific_retrieval_or_reranking": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = self_test() if args.self_test else build(args.root.resolve())
    import json

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
