#!/usr/bin/env python3
"""Freeze the V3 native-SkillRouter B1 payload without network or scoring.

This preparation gate binds the final V3/B1L representations and strict prompt
population to the pinned SkillRouter tokenizer.  It does not download model
weights, transfer text, load an embedding model, rank a prompt, or write thesis
material.  A later hosted-CUDA execution must use the emitted exact inventory
and obtain a separate user approval receipt.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight
from rq2bv1_v3_skillrouter_primary_constants import (
    CACHE_ROOT,
    CHECKPOINT_NAME,
    DIMENSIONS,
    EXECUTION_PACKET_NAME,
    HF_CHECKPOINT_EVERY_FORWARDS,
    HF_CHECKPOINT_REPOSITORY,
    HF_INPUT_BUNDLE_PATH,
    HF_JOB_IMAGE,
    HF_JOB_FLAVOR,
    HF_JOB_TIMEOUT,
    HF_MAXIMUM_HARDWARE_COST_USD,
    HF_MAX_CHECKPOINT_ARCHIVES,
    HF_OUTPUT_PREFIX,
    MAX_BATCH_SIZE,
    MAX_MODEL_TOKENS,
    MAX_PADDED_MODEL_TOKENS_PER_FORWARD,
    MODEL,
    MODEL_CONFIG_SHA256,
    MODEL_FILE_SHA256,
    MODEL_WEIGHTS_SHA256,
    PAYLOAD_NAME,
    PREFLIGHT_ROOT,
    PREFLIGHT_VERSION,
    QUERY_INSTRUCTION,
    REPORT_NAME,
    REPRESENTATIONS,
    RESULT_ROOT,
    REVISION,
    RUN_ID,
    TEXT_INVENTORY_NAME,
    TOKENIZER_BLOB,
    TOKENIZER_SHA256,
)
from rq2b_common import (
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    source_length_quartiles,
    write_json_new,
    write_jsonl_new,
)


RUNNER_PATH = "skill_benchmark/scripts/run_rq2bv1_v3_skillrouter_primary.py"
RUNNER_DEPENDENCIES = (
    RUNNER_PATH,
    "skill_benchmark/scripts/rq2bv1_v3_skillrouter_primary_constants.py",
    "skill_benchmark/scripts/finalize_rq2bv1_v3_skillrouter_primary.py",
    "skill_benchmark/scripts/hf_rq2bv1_v3_skillrouter_primary_job.py",
    "skill_benchmark/scripts/materialize_rq2bv1_v3_skillrouter_primary_hf_bundle.py",
    "skill_benchmark/scripts/upload_rq2bv1_v3_skillrouter_primary_hf_bundle.py",
    "skill_benchmark/scripts/recover_rq2bv1_v3_skillrouter_primary_hf_outputs.py",
    "skill_benchmark/scripts/prepare_rq2bv1_v3_skillrouter_primary_preflight.py",
    "skill_benchmark/scripts/rq2b_common.py",
    "skill_benchmark/scripts/rq2b_v11_execution_contract.py",
)


def load_exact_tokenizer() -> Any:
    from tokenizers import Tokenizer

    require(TOKENIZER_BLOB.is_file(), f"Pinned SkillRouter tokenizer is missing: {TOKENIZER_BLOB}")
    require(sha256_file(TOKENIZER_BLOB) == TOKENIZER_SHA256, "Pinned SkillRouter tokenizer hash drift")
    return Tokenizer.from_file(str(TOKENIZER_BLOB))


def model_token_count(tokenizer: Any, text: str) -> int:
    token_count = len(tokenizer.encode(text, add_special_tokens=True).ids)
    require(token_count > 0, "SkillRouter payload text tokenised to zero tokens")
    require(token_count <= MAX_MODEL_TOKENS, "SkillRouter full-context limit exceeded; truncation is forbidden")
    return token_count


def register_text(
    texts: dict[str, dict[str, Any]],
    *,
    text: str,
    model_tokens: int,
    role: dict[str, Any],
) -> str:
    require(bool(text), "Cannot register empty SkillRouter text")
    text_id = sha256_text(text)
    existing = texts.get(text_id)
    if existing is None:
        texts[text_id] = {
            "schema_version": "rq2bv1-v3-skillrouter-primary-text-v1",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "model_tokens": int(model_tokens),
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "SHA-256 collision in SkillRouter text inventory")
        require(int(existing["model_tokens"]) == int(model_tokens), "SkillRouter token-count drift for shared text")
        existing["roles"].append(role)
    return text_id


def schedule_document_forwards(text_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create a deterministic CUDA-safe schedule under padded-token bounds."""

    documents = [
        row
        for row in text_rows
        if any(role["kind"] == "document" for role in row["roles"])
    ]
    ordered = sorted(documents, key=lambda row: (-int(row["model_tokens"]), str(row["text_id"])))
    batches: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_max = 0
    for row in ordered:
        proposed_max = max(current_max, int(row["model_tokens"]))
        fits = (
            len(current) < MAX_BATCH_SIZE
            and (len(current) + 1) * proposed_max <= MAX_PADDED_MODEL_TOKENS_PER_FORWARD
        )
        if current and not fits:
            batches.append(
                {
                    "kind": "document",
                    "text_ids": [str(item["text_id"]) for item in current],
                    "items": len(current),
                    "maximum_model_tokens": current_max,
                    "padded_model_tokens": len(current) * current_max,
                }
            )
            current = []
            current_max = 0
        current.append(row)
        current_max = max(current_max, int(row["model_tokens"]))
    if current:
        batches.append(
            {
                "kind": "document",
                "text_ids": [str(item["text_id"]) for item in current],
                "items": len(current),
                "maximum_model_tokens": current_max,
                "padded_model_tokens": len(current) * current_max,
            }
        )
    require(all(0 < batch["items"] <= MAX_BATCH_SIZE for batch in batches), "Invalid SkillRouter document batch")
    require(
        all(batch["padded_model_tokens"] <= MAX_PADDED_MODEL_TOKENS_PER_FORWARD for batch in batches),
        "SkillRouter document schedule exceeds padded-token ceiling",
    )
    require(
        {text_id for batch in batches for text_id in batch["text_ids"]}
        == {str(row["text_id"]) for row in documents},
        "SkillRouter document schedule coverage drift",
    )
    return batches


def build_payload_data(
    tokenizer: Any,
    representations: dict[str, list[dict[str, Any]]],
    prompts: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    texts: dict[str, dict[str, Any]] = {}
    documents_by_representation: dict[str, list[dict[str, Any]]] = {}
    tokenisation_seconds: dict[str, float] = {}
    for representation in REPRESENTATIONS:
        rows = representations[representation]
        require(len(rows) == 2433, f"Candidate-library count drift: {representation}")
        started = time.perf_counter()
        quartiles = source_length_quartiles(rows)
        documents: list[dict[str, Any]] = []
        for row in rows:
            selector_text = str(row["selector_text"])
            documents.append(
                {
                    "source_row_index": int(row["source_row_index"]),
                    "skill_id": str(row["skill_id"]),
                    "selector_text_sha256": str(row["selector_text_sha256"]),
                    "selector_utf8_bytes": int(row["selector_visible_counts"]["utf8_bytes"]),
                    "source_length_quartile": quartiles[str(row["skill_id"])],
                    "text_id": register_text(
                        texts,
                        text=selector_text,
                        model_tokens=model_token_count(tokenizer, selector_text),
                        role={
                            "kind": "document",
                            "representation": representation,
                            "skill_id": str(row["skill_id"]),
                        },
                    ),
                }
            )
        require(
            [document["skill_id"] for document in documents] == [row["skill_id"] for row in rows],
            f"Candidate ordering drift while serialising {representation}",
        )
        documents_by_representation[representation] = documents
        tokenisation_seconds[representation] = time.perf_counter() - started

    query_started = time.perf_counter()
    query_text_ids: dict[str, str] = {}
    for prompt in prompts:
        query_text = QUERY_INSTRUCTION + str(prompt["prompt"])
        query_text_ids[str(prompt["prompt_id"])] = register_text(
            texts,
            text=query_text,
            model_tokens=model_token_count(tokenizer, query_text),
            role={
                "kind": "query",
                "prompt_id": str(prompt["prompt_id"]),
                "raw_prompt_sha256": str(prompt["prompt_sha256"]),
            },
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
                str(role.get("prompt_id", "")),
            ),
        )
    return rows, {
        "documents": documents_by_representation,
        "query_text_ids": query_text_ids,
        "preparation_timing": {
            "representation_tokenisation_seconds": tokenisation_seconds,
            "query_tokenisation_seconds": query_seconds,
            "total_payload_serialisation_seconds": sum(tokenisation_seconds.values()) + query_seconds,
        },
    }


def build(root: Path) -> dict[str, Any]:
    b1l_report, representations, prompts = verify_preflight(root)
    require(len(prompts) == 381, "Strict prompt population drift")
    require(set(representations) == set(REPRESENTATIONS), "Representation coverage drift")
    tokenizer = load_exact_tokenizer()
    text_rows, payload_maps = build_payload_data(tokenizer, representations, prompts)
    document_rows = [row for row in text_rows if any(role["kind"] == "document" for role in row["roles"])]
    query_rows = [row for row in text_rows if any(role["kind"] == "query" for role in row["roles"])]
    document_schedule = schedule_document_forwards(text_rows)
    query_schedule = [
        {
            "kind": "query",
            "text_ids": [str(row["text_id"])],
            "items": 1,
            "maximum_model_tokens": int(row["model_tokens"]),
            "padded_model_tokens": int(row["model_tokens"]),
        }
        for row in sorted(query_rows, key=lambda row: str(row["text_id"]))
    ]
    require(len(query_schedule) == len(query_rows), "SkillRouter query schedule drift")

    preflight_root = root / PREFLIGHT_ROOT
    staging = preflight_root.with_name(f".{preflight_root.name}.staging")
    require(not preflight_root.exists() and not staging.exists(), "Refusing to overwrite SkillRouter V3 preflight")
    staging.mkdir(parents=True, exist_ok=False)
    inventory_path = staging / TEXT_INVENTORY_NAME
    write_jsonl_new(inventory_path, text_rows)

    selector_tokens_by_representation = {
        representation: sum(
            int(next(row for row in text_rows if row["text_id"] == document["text_id"])["model_tokens"])
            for document in documents
        )
        for representation, documents in payload_maps["documents"].items()
    }
    payload = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-payload-v1",
        "state": "sealed_not_executed",
        "network_calls": 0,
        "model": MODEL,
        "revision": REVISION,
        "dimensions": DIMENSIONS,
        "maximum_model_tokens": MAX_MODEL_TOKENS,
        "pooling": "last_non_padding_token",
        "normalisation": "l2",
        "score": "cosine",
        "query_instruction": QUERY_INSTRUCTION,
        "document_serialisation": "exact_representation_selector_text",
        "truncation": "forbidden",
        "strict_population": {
            "candidate_library_skills": 2433,
            "strict_prompts": 381,
            "representations": list(REPRESENTATIONS),
            "expected_primary_result_rows": 1524,
        },
        "b1l_preflight": {
            "strict_endpoint_contract": b1l_report["strict_endpoint_contract"],
            "source_preflight_report": {
                "path": "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/b1l_preflight_report.json",
                "sha256": sha256_file(
                    root
                    / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/b1l_preflight_report.json"
                ),
            },
        },
        "text_inventory": {
            "path": relative(preflight_root / TEXT_INVENTORY_NAME, root),
            "sha256": sha256_file(inventory_path),
            "rows": len(text_rows),
        },
        "prompt_artifact": b1l_report["strict_scored_prompts"],
        "representation_inputs": b1l_report["representations"],
        "tokenizer": {
            "source": "local pinned tokenizer blob only",
            "tokenizer_json_sha256": TOKENIZER_SHA256,
            "model_config_sha256": MODEL_CONFIG_SHA256,
            "model_weights_sha256_expected": MODEL_WEIGHTS_SHA256,
        },
        "counts": {
            "unique_texts": len(text_rows),
            "unique_document_texts": len(document_rows),
            "unique_query_texts": len(query_rows),
            "document_instances": sum(len(documents) for documents in payload_maps["documents"].values()),
            "query_instances": len(prompts),
            "model_input_tokens_without_cache": sum(int(row["model_tokens"]) for row in text_rows),
            "document_model_tokens_by_representation": selector_tokens_by_representation,
            "document_forward_batches": len(document_schedule),
            "cold_query_forward_batches": len(query_schedule),
            "total_forward_batches_without_cache": len(document_schedule) + len(query_schedule),
            "padded_model_tokens_across_document_forwards": sum(
                int(batch["padded_model_tokens"]) for batch in document_schedule
            ),
            "padded_model_tokens_across_cold_query_forwards": sum(
                int(batch["padded_model_tokens"]) for batch in query_schedule
            ),
            "utf8_bytes_without_cache": sum(int(row["utf8_bytes"]) for row in text_rows),
            "maximum_document_model_tokens": max(int(row["model_tokens"]) for row in document_rows),
            "maximum_query_model_tokens": max(int(row["model_tokens"]) for row in query_rows),
        },
        "documents": payload_maps["documents"],
        "query_text_ids": payload_maps["query_text_ids"],
        "document_forward_schedule": document_schedule,
        "cold_query_forward_schedule": query_schedule,
        "execution_method": {
            "retriever": "skillrouter-embedding-single-vector",
            "document_aggregation": "single_full_context_cosine",
            "candidate_tie_break": "skill_id_ascending",
            "persisted_ranks": [1, 5, 20, 50, 100],
            "query_embedding_measurement": "one cold local forward per unique serialised query text",
            "cache_root": CACHE_ROOT,
            "runtime_dtype": "bfloat16",
            "runtime_device": "cuda",
            "maximum_batch_size": MAX_BATCH_SIZE,
            "maximum_padded_model_tokens_per_forward": MAX_PADDED_MODEL_TOKENS_PER_FORWARD,
        },
        "authorisation_boundary": {
            "model_download_authorised": False,
            "external_text_transfer_authorised": False,
            "hosted_cuda_authorised": False,
            "scientific_execution_authorised": False,
            "thesis_result_writing_authorised": False,
        },
    }
    payload_path = staging / PAYLOAD_NAME
    write_json_new(payload_path, payload)
    packet = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-execution-approval-packet-v1",
        "state": "awaiting_explicit_model_download_and_hosted_cuda_transfer_authorisation",
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(payload_path)},
        "execution_scripts": [
            {"path": path, "sha256": sha256_file(root / path)} for path in RUNNER_DEPENDENCIES
        ],
        "run_id": RUN_ID,
        "output_dir": RESULT_ROOT,
        "cache_root": CACHE_ROOT,
        "execution_environment": "approved_hosted_cuda",
        "minimum_compute": {
            "device": "CUDA GPU",
            "minimum_vram_gib": 24,
            "runtime_dtype": "bfloat16",
            "maximum_padded_model_tokens_per_forward": MAX_PADDED_MODEL_TOKENS_PER_FORWARD,
        },
        "model_download": {
            "authorised": False,
            "model": MODEL,
            "revision": REVISION,
            "required_sha256": MODEL_FILE_SHA256,
            "trust_remote_code": False,
        },
        "hosting_and_persistence": {
            "authorised": False,
            "platform": "Hugging Face Jobs",
            "job_image": HF_JOB_IMAGE,
            "job_flavor": HF_JOB_FLAVOR,
            "job_timeout": HF_JOB_TIMEOUT,
            "maximum_hardware_cost_usd": HF_MAXIMUM_HARDWARE_COST_USD,
            "checkpoint_dataset_repository": HF_CHECKPOINT_REPOSITORY,
            "input_bundle_path": HF_INPUT_BUNDLE_PATH,
            "output_prefix": HF_OUTPUT_PREFIX,
            "checkpoint_protocol": {
                "format": "immutable gzip tar archives with JSON manifests",
                "checkpoint_every_model_forward_batches": HF_CHECKPOINT_EVERY_FORWARDS,
                "maximum_checkpoint_archives": HF_MAX_CHECKPOINT_ARCHIVES,
                "maximum_completion_archives": 1,
                "maximum_hub_write_attempts": 64,
                "write_budget": "at most one dataset creation, one input-bundle upload, 61 checkpoint archives, and one completion archive",
                "upload_failure_policy": "fail closed; no automatic retry and no further model forwards",
                "resume_policy": "restore and verify all immutable checkpoint archives before executing missing forward batches",
            },
            "local_finalisation": "download verified checkpoint and completion archives, then score locally with gold labels retained locally",
        },
        "hosted_text_transfer": {
            "authorised": False,
            "only_text_artifact": payload["text_inventory"],
            "unique_texts": payload["counts"]["unique_texts"],
            "utf8_bytes": payload["counts"]["utf8_bytes_without_cache"],
            "model_input_tokens": payload["counts"]["model_input_tokens_without_cache"],
            "excluded_source_data": [
                "unselected source files outside the frozen selector representations",
                "gold labels, alternative-label metadata, and B0G audit material",
                "thesis LaTeX/PDF files",
            ],
        },
        "execution_ceiling_without_cache": {
            "maximum_new_cache_entries": payload["counts"]["unique_texts"],
            "maximum_model_input_instances": payload["counts"]["unique_texts"],
            "maximum_model_input_tokens": payload["counts"]["model_input_tokens_without_cache"],
            "maximum_model_forward_batches": payload["counts"]["total_forward_batches_without_cache"],
            "maximum_cold_query_forwards": payload["counts"]["unique_query_texts"],
            "automatic_retries": 0,
        },
        "expected_outputs": [
            "exact-key local embedding cache",
            "per-forward records for recovery",
            "1,524 strict B1 result rows",
            "zero-forward warm replay verification",
            "post-run integrity summary",
        ],
        "excluded_actions": [
            "no truncation or chunking",
            "no field-aware scoring",
            "no reranking",
            "no B2 candidate recomputation",
            "no query rewrite or target-label access",
            "no thesis LaTeX or PDF result writing",
        ],
    }
    packet_path = staging / EXECUTION_PACKET_NAME
    write_json_new(packet_path, packet)
    report = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-preflight-report-v1",
        "state": "preflight_passed_no_network_no_scoring_hosted_cuda_authorisation_required",
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(payload_path)},
        "execution_packet": {"path": relative(preflight_root / EXECUTION_PACKET_NAME, root), "sha256": sha256_file(packet_path)},
        "strict_population": payload["strict_population"],
        "counts": payload["counts"],
        "validation": {
            "b1l_preflight_replayed": True,
            "pinned_tokenizer_hash_verified": True,
            "all_texts_within_32768_token_limit": len(text_rows),
            "document_schedule_coverage": len(document_rows),
            "query_schedule_coverage": len(query_rows),
            "network_calls": 0,
            "scientific_retrieval_or_reranking": False,
        },
        "next_gate": "user_review_of_exact_packet_then_separate_model_download_and_hosted_cuda_transfer_authorisation",
    }
    report_path = staging / REPORT_NAME
    write_json_new(report_path, report)
    checkpoint = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-preflight-checkpoint-v1",
        "state": "skillrouter_primary_preflight_frozen_hosted_cuda_authorisation_required",
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
        def encode(self, text: str, add_special_tokens: bool = True) -> Any:
            del add_special_tokens
            return type("Encoded", (), {"ids": [ord(character) for character in text]})()

    rows = [
        {
            "source_row_index": index,
            "skill_id": f"skill-{index:04d}",
            "selector_text": "alpha body",
            "selector_text_sha256": sha256_text("alpha body"),
            "selector_visible_counts": {"utf8_bytes": len("alpha body".encode("utf-8"))},
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
    text_rows, payload = build_payload_data(CharacterTokenizer(), representations, prompts)
    schedule = schedule_document_forwards(text_rows)
    require(len(payload["documents"]) == 4, "Synthetic representation matrix mismatch")
    require(len(payload["query_text_ids"]) == 1, "Synthetic query map mismatch")
    require(len(schedule) > 0, "Synthetic document schedule missing")
    require(
        all(int(batch["padded_model_tokens"]) <= MAX_PADDED_MODEL_TOKENS_PER_FORWARD for batch in schedule),
        "Synthetic padded-token bound failure",
    )
    return {
        "schema_version": "rq2bv1-v3-skillrouter-primary-preflight-self-test-v1",
        "state": "self_test_passed_no_network_no_scoring",
        "network_calls": 0,
        "scientific_retrieval_or_reranking": False,
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
