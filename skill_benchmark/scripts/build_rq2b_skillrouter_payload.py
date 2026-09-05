#!/usr/bin/env python3
"""Build immutable-candidate SkillRouter window payloads for separate approval."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

from rq2b_chunking import CHUNKER_VERSION, exact_text_chunks
from rq2b_common import (
    B0F_A1_AMENDMENT_SHA256,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    sha256_text,
    source_length_quartiles,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    verify_i3c_retrieval_ready,
    version_root,
    write_json_new,
    write_jsonl_new,
)
from run_rq2b_skillrouter import (
    MAX_PAIR_TOKENS,
    MODEL,
    MODEL_CONFIG_SHA256,
    MODEL_WEIGHTS_SHA256,
    PRIMARY_K,
    PROMPT_SHA256,
    PROMPT_VERSION,
    REVISION,
    TOKENIZER_SHA256,
    build_input_ids,
)
from run_rq2b_bm25 import (
    B as BM25_B,
    K1 as BM25_K1,
    RUNNER_VERSION as BM25_RUNNER_VERSION,
    TOP_PERSISTED as BM25_TOP_PERSISTED,
)
from run_rq2b_qwen import (
    BASE_URL as QWEN_BASE_URL,
    DIMENSIONS as QWEN_DIMENSIONS,
    MODEL as QWEN_MODEL,
    RUNNER_VERSION as QWEN_RUNNER_VERSION,
)
from run_rq2b_skillrouter_embedding import (
    DIMENSIONS as SKILLROUTER_EMBEDDING_DIMENSIONS,
    MAX_MODEL_TOKENS as SKILLROUTER_EMBEDDING_MAX_TOKENS,
    MODEL as SKILLROUTER_EMBEDDING_MODEL,
    MODEL_CONFIG_SHA256 as SKILLROUTER_EMBEDDING_CONFIG_SHA256,
    MODEL_WEIGHTS_SHA256 as SKILLROUTER_EMBEDDING_WEIGHTS_SHA256,
    QUERY_INSTRUCTION as SKILLROUTER_EMBEDDING_QUERY_INSTRUCTION,
    REVISION as SKILLROUTER_EMBEDDING_REVISION,
    RUNNER_VERSION as SKILLROUTER_EMBEDDING_RUNNER_VERSION,
    TOKENIZER_SHA256 as SKILLROUTER_EMBEDDING_TOKENIZER_SHA256,
)


REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
)
FIRST_STAGE_RETRIEVERS = ("bm25", "qwen-max-chunk", "skillrouter-embedding")


def require_current_b1_version(manifest: dict[str, Any], label: str) -> None:
    require(
        manifest.get("version_id") == VERSION_ID,
        f"B1 manifest version mismatch: {label}",
    )


def current_input_bindings(
    root: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    verify_i3c_retrieval_ready(root)
    frozen_root = version_root(root)
    prompt_path = frozen_root / "prompt_manifest.jsonl"
    prompt_rows = read_jsonl(prompt_path)
    prompt_binding = {
        "path": relative(prompt_path, root),
        "sha256": sha256_file(prompt_path),
        "rows": len(prompt_rows),
    }
    base_manifest = read_json(frozen_root / "representations" / "manifest.json")
    i3_manifest = read_json(frozen_root / "i3c_merged" / "manifest.json")
    representation_bindings: dict[str, dict[str, Any]] = {}
    for representation in REPRESENTATIONS:
        source_manifest = base_manifest if representation in base_manifest["artifacts"] else i3_manifest
        artifact = source_manifest["artifacts"][representation]
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], f"Representation drift: {representation}")
        representation_bindings[representation] = {
            "path": relative(path, root),
            "sha256": artifact["sha256"],
            "rows": int(artifact["rows"]),
        }
    return prompt_binding, representation_bindings


def validate_b1_manifest_binding(
    manifest: dict[str, Any],
    label: str,
    *,
    prompt_binding: dict[str, Any],
    representation_bindings: dict[str, dict[str, Any]],
    qwen_payload: dict[str, Any] | None = None,
    skillrouter_embedding_payload: dict[str, Any] | None = None,
) -> None:
    require_current_b1_version(manifest, label)
    schema = manifest.get("schema_version")
    if schema == "rq2b-bm25-run-manifest-v1":
        representation = manifest.get("representation")
        require(representation in representation_bindings, f"Unknown BM25 representation: {label}")
        require(manifest.get("runner_version") == BM25_RUNNER_VERSION, f"BM25 runner mismatch: {label}")
        require(manifest.get("network_calls") == 0, f"BM25 network boundary mismatch: {label}")
        require(manifest.get("retriever") == "bm25", f"BM25 retriever mismatch: {label}")
        require(
            manifest.get("configuration")
            == {
                "tokenizer": "lowercase_[a-z0-9]+",
                "query_term_frequency": "multiplicative",
                "k1": BM25_K1,
                "b": BM25_B,
                "corpus_documents": representation_bindings[representation]["rows"],
                "persisted_top_k": BM25_TOP_PERSISTED,
                "tie_break": "skill_id_ascending",
            },
            f"BM25 configuration mismatch: {label}",
        )
        inputs = manifest.get("inputs", {})
        expected_representation = representation_bindings[representation]
        require(
            inputs.get("representation_path") == expected_representation["path"]
            and inputs.get("representation_sha256") == expected_representation["sha256"],
            f"BM25 representation binding mismatch: {label}",
        )
        require(
            inputs.get("prompt_manifest_path") == prompt_binding["path"]
            and inputs.get("prompt_manifest_sha256") == prompt_binding["sha256"],
            f"BM25 prompt-manifest binding mismatch: {label}",
        )
        require(
            manifest.get("counts")
            == {
                "documents": expected_representation["rows"],
                "prompts": prompt_binding["rows"],
                "rows": prompt_binding["rows"],
            },
            f"BM25 manifest-count mismatch: {label}",
        )
        return
    if schema == "rq2b-qwen-run-manifest-v1":
        require(qwen_payload is not None, f"Missing Qwen payload for manifest validation: {label}")
        require(manifest.get("runner_version") == QWEN_RUNNER_VERSION, f"Qwen runner mismatch: {label}")
        require(manifest.get("base_url") == QWEN_BASE_URL, f"Qwen endpoint mismatch: {label}")
        require(manifest.get("model") == QWEN_MODEL, f"Qwen model mismatch: {label}")
        require(manifest.get("dimensions") == QWEN_DIMENSIONS, f"Qwen dimensions mismatch: {label}")
        require(manifest.get("automatic_retries") == 0, f"Qwen retry-policy mismatch: {label}")
        require(
            qwen_payload.get("schema_version") == "rq2b-qwen-payload-manifest-v1"
            and qwen_payload.get("version_id") == VERSION_ID
            and qwen_payload.get("state") == "sealed_not_executed",
            f"Qwen payload identity mismatch: {label}",
        )
        require(qwen_payload.get("base_url") == QWEN_BASE_URL, f"Qwen payload endpoint mismatch: {label}")
        require(qwen_payload.get("model") == QWEN_MODEL, f"Qwen payload model mismatch: {label}")
        require(qwen_payload.get("dimensions") == QWEN_DIMENSIONS, f"Qwen payload dimensions mismatch: {label}")
        require(qwen_payload.get("chunker_version") == CHUNKER_VERSION, f"Qwen payload chunker mismatch: {label}")
        require(qwen_payload.get("prompt_manifest") == prompt_binding, f"Qwen prompt-manifest binding mismatch: {label}")
        require(qwen_payload.get("representation_inputs") == representation_bindings, f"Qwen representation binding mismatch: {label}")
        return

    require(
        schema == "rq2b-skillrouter-embedding-run-manifest-v1",
        f"Unsupported B1 manifest schema: {label}",
    )
    require(skillrouter_embedding_payload is not None, f"Missing SkillRouter embedding payload: {label}")
    require(manifest.get("runner_version") == SKILLROUTER_EMBEDDING_RUNNER_VERSION, f"SkillRouter embedding runner mismatch: {label}")
    require(manifest.get("retriever") == "skillrouter-embedding", f"SkillRouter embedding retriever mismatch: {label}")
    require(manifest.get("model") == SKILLROUTER_EMBEDDING_MODEL, f"SkillRouter embedding model mismatch: {label}")
    require(manifest.get("revision") == SKILLROUTER_EMBEDDING_REVISION, f"SkillRouter embedding revision mismatch: {label}")
    require(manifest.get("dimensions") == SKILLROUTER_EMBEDDING_DIMENSIONS, f"SkillRouter embedding dimensions mismatch: {label}")
    require(manifest.get("maximum_model_tokens") == SKILLROUTER_EMBEDDING_MAX_TOKENS, f"SkillRouter embedding context mismatch: {label}")
    require(manifest.get("aggregation") == "single_full_context_cosine", f"SkillRouter embedding aggregation mismatch: {label}")
    require(manifest.get("pooling") == "last_non_padding_token", f"SkillRouter embedding pooling mismatch: {label}")
    require(manifest.get("normalization") == "l2", f"SkillRouter embedding normalization mismatch: {label}")
    require(manifest.get("query_instruction") == SKILLROUTER_EMBEDDING_QUERY_INSTRUCTION, f"SkillRouter embedding query instruction mismatch: {label}")
    require(manifest.get("automatic_retries") == 0, f"SkillRouter embedding retry-policy mismatch: {label}")
    require(
        manifest.get("b0f_a1_amendment_sha256") == B0F_A1_AMENDMENT_SHA256,
        f"SkillRouter embedding amendment mismatch: {label}",
    )
    require(
        manifest.get("model_snapshot", {}).get("revision")
        == SKILLROUTER_EMBEDDING_REVISION
        and manifest.get("model_snapshot", {}).get("files")
        == {
            "tokenizer.json": SKILLROUTER_EMBEDDING_TOKENIZER_SHA256,
            "config.json": SKILLROUTER_EMBEDDING_CONFIG_SHA256,
            "model.safetensors": SKILLROUTER_EMBEDDING_WEIGHTS_SHA256,
        },
        f"SkillRouter embedding model-snapshot mismatch: {label}",
    )
    require(
        skillrouter_embedding_payload.get("schema_version")
        == "rq2b-skillrouter-embedding-payload-manifest-v1"
        and skillrouter_embedding_payload.get("version_id") == VERSION_ID
        and skillrouter_embedding_payload.get("state") == "sealed_not_executed",
        f"SkillRouter embedding payload identity mismatch: {label}",
    )
    require(skillrouter_embedding_payload.get("model") == SKILLROUTER_EMBEDDING_MODEL, f"SkillRouter embedding payload model mismatch: {label}")
    require(skillrouter_embedding_payload.get("revision") == SKILLROUTER_EMBEDDING_REVISION, f"SkillRouter embedding payload revision mismatch: {label}")
    require(skillrouter_embedding_payload.get("dimensions") == SKILLROUTER_EMBEDDING_DIMENSIONS, f"SkillRouter embedding payload dimensions mismatch: {label}")
    require(skillrouter_embedding_payload.get("maximum_model_tokens") == SKILLROUTER_EMBEDDING_MAX_TOKENS, f"SkillRouter embedding payload context mismatch: {label}")
    require(skillrouter_embedding_payload.get("query_instruction") == SKILLROUTER_EMBEDDING_QUERY_INSTRUCTION, f"SkillRouter embedding query contract mismatch: {label}")
    require(
        skillrouter_embedding_payload.get("b0f_a1_amendment_sha256")
        == B0F_A1_AMENDMENT_SHA256,
        f"SkillRouter embedding payload amendment mismatch: {label}",
    )
    require(skillrouter_embedding_payload.get("document_serialization") == "exact_representation_selector_text", f"SkillRouter embedding document serialization mismatch: {label}")
    require(skillrouter_embedding_payload.get("truncation") == "forbidden", f"SkillRouter embedding truncation contract mismatch: {label}")
    require(skillrouter_embedding_payload.get("pooling") == "last_non_padding_token", f"SkillRouter embedding payload pooling mismatch: {label}")
    require(skillrouter_embedding_payload.get("normalization") == "l2", f"SkillRouter embedding payload normalization mismatch: {label}")
    require(skillrouter_embedding_payload.get("score") == "cosine", f"SkillRouter embedding payload score mismatch: {label}")
    require(
        skillrouter_embedding_payload.get("snapshot_audit")
        == {
            "path": "synthetic-or-bound-at-runtime",
            "tokenizer_sha256": SKILLROUTER_EMBEDDING_TOKENIZER_SHA256,
            "config_sha256": SKILLROUTER_EMBEDDING_CONFIG_SHA256,
            "weights_expected_sha256": SKILLROUTER_EMBEDDING_WEIGHTS_SHA256,
            "weights_present_and_verified": True,
        }
        or (
            skillrouter_embedding_payload.get("snapshot_audit", {}).get("tokenizer_sha256")
            == SKILLROUTER_EMBEDDING_TOKENIZER_SHA256
            and skillrouter_embedding_payload.get("snapshot_audit", {}).get("config_sha256")
            == SKILLROUTER_EMBEDDING_CONFIG_SHA256
            and skillrouter_embedding_payload.get("snapshot_audit", {}).get("weights_expected_sha256")
            == SKILLROUTER_EMBEDDING_WEIGHTS_SHA256
        ),
        f"SkillRouter embedding payload snapshot mismatch: {label}",
    )
    require(skillrouter_embedding_payload.get("prompt_manifest") == prompt_binding, f"SkillRouter embedding prompt binding mismatch: {label}")
    require(skillrouter_embedding_payload.get("representation_inputs") == representation_bindings, f"SkillRouter embedding representation binding mismatch: {label}")


def validate_b1_row_against_prompt(
    row: dict[str, Any],
    prompt: dict[str, Any],
    label: str,
) -> None:
    require(row.get("schema_version") == "rq2b-b1-result-row-v1", f"B1 row schema mismatch: {label}")
    require(row.get("version_id") == VERSION_ID, f"B1 row version mismatch: {label}")
    for field in ("prompt_id", "prompt_sha256", "stratum", "group", "gold_skill", "valid_skills"):
        require(row.get(field) == prompt.get(field), f"B1 row {field} mismatch: {label}")
    retriever = row.get("retriever")
    if retriever == "bm25":
        require(row.get("runner_version") == BM25_RUNNER_VERSION, f"BM25 row runner mismatch: {label}")
        require("aggregation" not in row, f"Unexpected BM25 row aggregation: {label}")
    elif retriever == "qwen-max-chunk":
        require(row.get("runner_version") == QWEN_RUNNER_VERSION, f"Qwen row runner mismatch: {label}")
        require(row.get("aggregation") == "maximum_chunk_cosine", f"Qwen row aggregation mismatch: {label}")
    elif retriever == "skillrouter-embedding":
        require(row.get("runner_version") == SKILLROUTER_EMBEDDING_RUNNER_VERSION, f"SkillRouter embedding row runner mismatch: {label}")
        require(row.get("aggregation") == "single_full_context_cosine", f"SkillRouter embedding row aggregation mismatch: {label}")
    else:
        raise ValueError(f"Unsupported B1 row retriever: {label}")
    candidates = row.get("top_20_skill_ids")
    require(
        isinstance(candidates, list)
        and len(candidates) == PRIMARY_K
        and len(set(candidates)) == PRIMARY_K,
        f"Invalid persisted top-20: {label}",
    )
    top_100 = row.get("top_100")
    require(isinstance(top_100, list) and len(top_100) == 100, f"Invalid persisted top-100: {label}")
    require(
        [entry.get("rank") for entry in top_100] == list(range(1, 101)),
        f"Persisted top-100 rank mismatch: {label}",
    )
    top_100_skill_ids = [entry.get("skill_id") for entry in top_100]
    require(len(set(top_100_skill_ids)) == 100, f"Persisted top-100 duplicate skill: {label}")
    require(top_100_skill_ids[:PRIMARY_K] == candidates, f"Persisted top-20/top-100 mismatch: {label}")


def load_b1_rows(root: Path, b1_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    prompt_binding, representation_bindings = current_input_bindings(root)
    manifests: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    manifest_paths = sorted(b1_root.glob("*/manifest.json"))
    require(bool(manifest_paths), f"No B1 manifests found under {b1_root}")
    for manifest_path in manifest_paths:
        manifest = read_json(manifest_path)
        retriever = manifest.get("retriever")
        if manifest.get("schema_version") == "rq2b-bm25-run-manifest-v1":
            validate_b1_manifest_binding(
                manifest,
                str(manifest_path),
                prompt_binding=prompt_binding,
                representation_bindings=representation_bindings,
            )
            require(manifest.get("state") == "complete_scientific_b1_local", f"Incomplete BM25 run: {manifest_path}")
            rows_path = root / manifest["artifacts"]["rows"]["path"]
        elif manifest.get("schema_version") == "rq2b-qwen-run-manifest-v1":
            require(manifest.get("state") == "complete_scientific_b1_external", f"Incomplete Qwen run: {manifest_path}")
            payload_path = root / manifest["payload_manifest_path"]
            require(
                sha256_file(payload_path) == manifest.get("payload_manifest_sha256"),
                f"Qwen payload-manifest drift: {manifest_path}",
            )
            validate_b1_manifest_binding(
                manifest,
                str(manifest_path),
                prompt_binding=prompt_binding,
                representation_bindings=representation_bindings,
                qwen_payload=read_json(payload_path),
            )
            retriever = "qwen-max-chunk"
            rows_path = root / manifest["artifacts"]["rows"]["path"]
        elif manifest.get("schema_version") == "rq2b-skillrouter-embedding-run-manifest-v1":
            require(
                manifest.get("state") == "complete_scientific_b1_skillrouter_embedding",
                f"Incomplete SkillRouter embedding run: {manifest_path}",
            )
            payload_path = root / manifest["payload_manifest_path"]
            require(
                sha256_file(payload_path) == manifest.get("payload_manifest_sha256"),
                f"SkillRouter embedding payload drift: {manifest_path}",
            )
            validate_b1_manifest_binding(
                manifest,
                str(manifest_path),
                prompt_binding=prompt_binding,
                representation_bindings=representation_bindings,
                skillrouter_embedding_payload=read_json(payload_path),
            )
            retriever = "skillrouter-embedding"
            rows_path = root / manifest["artifacts"]["rows"]["path"]
        else:
            continue
        require(sha256_file(rows_path) == manifest["artifacts"]["rows"]["sha256"], f"B1 rows drift: {rows_path}")
        source_rows = read_jsonl(rows_path)
        require(
            len(source_rows) == int(manifest["artifacts"]["rows"]["rows"]),
            f"B1 manifest/result-row count mismatch: {rows_path}",
        )
        if manifest.get("schema_version") == "rq2b-qwen-run-manifest-v1":
            require(
                len(source_rows) == prompt_binding["rows"] * len(REPRESENTATIONS) * 2,
                f"Qwen B1 complete-matrix row count mismatch: {rows_path}",
            )
        elif manifest.get("schema_version") == "rq2b-skillrouter-embedding-run-manifest-v1":
            require(
                len(source_rows) == prompt_binding["rows"] * len(REPRESENTATIONS),
                f"SkillRouter embedding B1 complete-matrix row count mismatch: {rows_path}",
            )
        require(
            all(row.get("version_id") == VERSION_ID for row in source_rows),
            f"B1 result-row version mismatch: {rows_path}",
        )
        if retriever == "qwen-max-chunk":
            source_rows = [row for row in source_rows if row["retriever"] == "qwen-max-chunk"]
        rows.extend(source_rows)
        manifests.append(
            {
                "path": relative(manifest_path, root),
                "sha256": sha256_file(manifest_path),
                "rows_path": relative(rows_path, root),
                "rows_sha256": sha256_file(rows_path),
                "selected_rows": len(source_rows),
            }
        )
    return rows, manifests


def load_representation_texts(root: Path) -> dict[str, dict[str, dict[str, Any]]]:
    frozen_root = version_root(root)
    base_manifest = read_json(frozen_root / "representations" / "manifest.json")
    i3_manifest = read_json(frozen_root / "i3c_merged" / "manifest.json")
    verify_i3c_retrieval_ready(root)
    output: dict[str, dict[str, dict[str, Any]]] = {}
    for representation in REPRESENTATIONS:
        manifest = base_manifest if representation in base_manifest["artifacts"] else i3_manifest
        artifact = manifest["artifacts"][representation]
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], f"Representation drift: {representation}")
        rows = read_jsonl(path)
        require(len(rows) == 2433, f"Representation row count mismatch: {representation}")
        quartiles = source_length_quartiles(rows)
        output[representation] = {
            row["skill_id"]: {
                **row,
                "source_length_quartile": quartiles[row["skill_id"]],
            }
            for row in rows
        }
    return output


def build_payload_data(
    *,
    tokenizer: Any,
    b1_rows: list[dict[str, Any]],
    prompts: dict[str, dict[str, Any]],
    representations: dict[str, dict[str, dict[str, Any]]],
    budgets: dict[str, int],
    overlap_tokens: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_condition: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in b1_rows:
        retriever = row["retriever"]
        if retriever not in FIRST_STAGE_RETRIEVERS:
            continue
        prompt_id = row["prompt_id"]
        require(prompt_id in prompts, f"Unknown B1 prompt: {prompt_id}")
        validate_b1_row_against_prompt(
            row,
            prompts[prompt_id],
            f"{retriever}/{row['representation']}/{prompt_id}",
        )
        key = (retriever, row["representation"], row["prompt_id"])
        require(key not in by_condition, f"Duplicate B1 condition row: {key}")
        by_condition[key] = row
    expected = {
        (retriever, representation, prompt_id)
        for retriever in FIRST_STAGE_RETRIEVERS
        for representation in REPRESENTATIONS
        for prompt_id in prompts
    }
    require(set(by_condition) == expected, f"B1 condition matrix mismatch: expected {len(expected)}, found {len(by_condition)}")

    pair_rows: dict[str, dict[str, Any]] = {}
    window_rows: dict[str, dict[str, Any]] = {}
    condition_rows: list[dict[str, Any]] = []
    for key in sorted(by_condition):
        retriever, representation, prompt_id = key
        b1 = by_condition[key]
        candidates = list(b1["top_20_skill_ids"])
        prompt = prompts[prompt_id]
        pair_ids: dict[str, str] = {}
        for skill_id in candidates:
            require(skill_id in representations[representation], f"Unknown candidate skill: {key}/{skill_id}")
            document = representations[representation][skill_id]
            pair_id = sha256_json(
                {
                    "prompt_id": prompt_id,
                    "prompt_sha256": prompt["prompt_sha256"],
                    "representation": representation,
                    "skill_id": skill_id,
                    "selector_text_sha256": document["selector_text_sha256"],
                    "model": MODEL,
                    "revision": REVISION,
                    "prompt_contract_sha256": PROMPT_SHA256,
                    "tokenizer_sha256": TOKENIZER_SHA256,
                    "chunker_version": CHUNKER_VERSION,
                    "document_budget": budgets[prompt_id],
                    "overlap_tokens": overlap_tokens,
                }
            )
            pair_ids[skill_id] = pair_id
            if pair_id in pair_rows:
                continue
            chunks = exact_text_chunks(
                tokenizer,
                document["selector_text"],
                maximum_tokens=budgets[prompt_id],
                overlap_tokens=overlap_tokens,
            )
            window_ids: list[str] = []
            for chunk in chunks:
                window_id = sha256_json(
                    {
                        "pair_id": pair_id,
                        "chunk_index": chunk.chunk_index,
                        "document_window_sha256": chunk.text_sha256,
                    }
                )
                window_ids.append(window_id)
                model_input_tokens = len(
                    build_input_ids(tokenizer, prompt["prompt"], chunk.text)
                )
                window_row = {
                    "schema_version": "rq2b-skillrouter-window-payload-v1",
                    "window_id": window_id,
                    "pair_id": pair_id,
                    "prompt_id": prompt_id,
                    "representation": representation,
                    "skill_id": skill_id,
                    "query": prompt["prompt"],
                    "query_sha256": prompt["prompt_sha256"],
                    "document_window": chunk.text,
                    "document_window_sha256": chunk.text_sha256,
                    "chunk_index": chunk.chunk_index,
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char,
                    "document_window_tokens": chunk.token_count,
                    "model_input_tokens": model_input_tokens,
                    "document_budget": budgets[prompt_id],
                }
                existing_window = window_rows.get(window_id)
                require(existing_window is None or existing_window == window_row, "SkillRouter window-ID collision")
                window_rows[window_id] = window_row
            pair_rows[pair_id] = {
                "schema_version": "rq2b-skillrouter-pair-payload-v1",
                "pair_id": pair_id,
                "prompt_id": prompt_id,
                "representation": representation,
                "skill_id": skill_id,
                "query_sha256": prompt["prompt_sha256"],
                "selector_text_sha256": document["selector_text_sha256"],
                "selector_utf8_bytes": document["selector_visible_counts"]["utf8_bytes"],
                "source_length_quartile": document["source_length_quartile"],
                "window_ids": window_ids,
            }
        strict_gold_document = representations[representation][prompt["gold_skill"]]
        strict_gold_windows = exact_text_chunks(
            tokenizer,
            strict_gold_document["selector_text"],
            maximum_tokens=budgets[prompt_id],
            overlap_tokens=overlap_tokens,
        )
        condition_rows.append(
            {
                "schema_version": "rq2b-skillrouter-condition-payload-v1",
                "condition_id": sha256_json(
                    {
                        "first_stage_retriever": retriever,
                        "representation": representation,
                        "prompt_id": prompt_id,
                        "candidate_skill_ids": candidates,
                    }
                ),
                "first_stage_retriever": retriever,
                "representation": representation,
                "prompt_id": prompt_id,
                "stratum": prompt["stratum"],
                "group": prompt["group"],
                "candidate_skill_ids": candidates,
                "candidate_list_sha256": sha256_json(candidates),
                "pair_ids_by_skill": pair_ids,
                "b1_strict_gold_rank": b1["strict_gold_rank"],
                "b1_acceptable_gold_rank": b1["acceptable_gold_rank"],
                "b1_first_stage_top1": candidates[0],
                "strict_gold_document_window_count": len(strict_gold_windows),
                "strict_gold_document_window_class": (
                    "one_window" if len(strict_gold_windows) == 1 else "multi_window"
                ),
                "strict_gold_selector_utf8_bytes": strict_gold_document["selector_visible_counts"]["utf8_bytes"],
                "strict_gold_source_length_quartile": strict_gold_document["source_length_quartile"],
            }
        )
    return (
        [window_rows[key] for key in sorted(window_rows)],
        [pair_rows[key] for key in sorted(pair_rows)],
        condition_rows,
    )


def build(root: Path, b1_root: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    frozen_root = version_root(root)
    b1_rows, b1_manifests = load_b1_rows(root, b1_root)
    prompt_manifest_path = frozen_root / "prompt_manifest.jsonl"
    prompt_rows = read_jsonl(prompt_manifest_path)
    prompts = {row["prompt_id"]: row for row in prompt_rows}
    representations = load_representation_texts(root)
    token_audit_path = root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"
    token_audit = read_json(token_audit_path)
    skillrouter = token_audit["skillrouter"]
    tokenizer_path = Path(skillrouter["tokenizer_snapshot"])
    require(sha256_file(tokenizer_path / "tokenizer.json") == TOKENIZER_SHA256, "SkillRouter tokenizer drift")
    require(sha256_file(tokenizer_path / "model.safetensors") == MODEL_WEIGHTS_SHA256, "SkillRouter model-weight drift")
    require(sha256_file(tokenizer_path / "config.json") == MODEL_CONFIG_SHA256, "SkillRouter model-config drift")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    budgets = {
        row["prompt_id"]: int(row["document_window_budget"])
        for row in token_audit["prompt_overhead_rows"]
    }
    payload_started = time.perf_counter()
    windows, pairs, conditions = build_payload_data(
        tokenizer=tokenizer,
        b1_rows=b1_rows,
        prompts=prompts,
        representations=representations,
        budgets=budgets,
        overlap_tokens=int(skillrouter["overlap_tokens"]),
    )
    payload_serialization_seconds = time.perf_counter() - payload_started
    output_root = frozen_root / "skillrouter_payload"
    staging = frozen_root / ".skillrouter_payload.staging"
    require(not output_root.exists(), f"SkillRouter payload root exists: {output_root}")
    require(not staging.exists(), f"Stale SkillRouter payload staging root: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    window_path = staging / "window_inventory.jsonl"
    pair_path = staging / "pair_inventory.jsonl"
    condition_path = staging / "condition_inventory.jsonl"
    write_jsonl_new(window_path, windows)
    write_jsonl_new(pair_path, pairs)
    write_jsonl_new(condition_path, conditions)
    artifacts = {
        "window_inventory": (window_path, len(windows)),
        "pair_inventory": (pair_path, len(pairs)),
        "condition_inventory": (condition_path, len(conditions)),
    }
    manifest = {
        "schema_version": "rq2b-skillrouter-payload-manifest-v1",
        "version_id": VERSION_ID,
        "state": "sealed_not_executed",
        "network_calls": 0,
        "model_forwards": 0,
        "model": MODEL,
        "revision": REVISION,
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": PROMPT_SHA256,
        "tokenizer_sha256": TOKENIZER_SHA256,
        "model_weights_sha256": MODEL_WEIGHTS_SHA256,
        "model_config_sha256": MODEL_CONFIG_SHA256,
        "maximum_pair_tokens": MAX_PAIR_TOKENS,
        "primary_k": PRIMARY_K,
        "chunker_version": CHUNKER_VERSION,
        "b1_manifests": b1_manifests,
        "prompt_manifest": {
            "path": relative(prompt_manifest_path, root),
            "sha256": sha256_file(prompt_manifest_path),
            "rows": len(prompt_rows),
        },
        "counts": {
            "conditions": len(conditions),
            "unique_pairs": len(pairs),
            "unique_windows": len(windows),
            "visible_window_tokens": sum(row["document_window_tokens"] for row in windows),
            "model_input_tokens": sum(row["model_input_tokens"] for row in windows),
        },
        "preparation_timing": {
            "payload_serialization_seconds": payload_serialization_seconds,
        },
        "authorization_boundary": {
            "model_forward_authorized": False,
            "hosted_text_transfer_authorized": False,
            "execution_authorisation_required": True,
        },
        **{
            name: {
                "path": relative(output_root / path.name, root),
                "sha256": sha256_file(path),
                "rows": count,
            }
            for name, (path, count) in artifacts.items()
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

    skill_ids = [f"s{index:02d}" for index in range(PRIMARY_K)]
    representations = {
        representation: {
            skill_id: {
                "selector_text": f"{representation} {skill_id} document",
                "selector_text_sha256": sha256_text(f"{representation} {skill_id} document"),
                "selector_visible_counts": {
                    "utf8_bytes": len(f"{representation} {skill_id} document".encode("utf-8")),
                },
                "source_length_quartile": "q1",
            }
            for skill_id in skill_ids
        }
        for representation in REPRESENTATIONS
    }
    prompts = {
        "p1": {
            "prompt_id": "p1",
            "prompt": "synthetic query",
            "prompt_sha256": sha256_text("synthetic query"),
            "stratum": "controlled",
            "group": "g1",
            "gold_skill": "s00",
            "valid_skills": ["s00"],
        }
    }
    top_100 = [
        {
            "rank": index + 1,
            "skill_id": f"s{index:02d}",
            "score": float(100 - index),
            "destination_class": "valid" if index == 0 else "background_unrelated",
        }
        for index in range(100)
    ]
    b1_rows = [
        {
            "schema_version": "rq2b-b1-result-row-v1",
            "version_id": VERSION_ID,
            "runner_version": (
                BM25_RUNNER_VERSION
                if retriever == "bm25"
                else QWEN_RUNNER_VERSION
                if retriever == "qwen-max-chunk"
                else SKILLROUTER_EMBEDDING_RUNNER_VERSION
            ),
            "retriever": retriever,
            **(
                {"aggregation": "maximum_chunk_cosine"}
                if retriever == "qwen-max-chunk"
                else {"aggregation": "single_full_context_cosine"}
                if retriever == "skillrouter-embedding"
                else {}
            ),
            "representation": representation,
            "prompt_id": "p1",
            "prompt_sha256": prompts["p1"]["prompt_sha256"],
            "stratum": "controlled",
            "group": "g1",
            "gold_skill": "s00",
            "valid_skills": ["s00"],
            "top_20_skill_ids": skill_ids,
            "top_100": top_100,
            "strict_gold_rank": 1,
            "acceptable_gold_rank": 1,
        }
        for retriever in FIRST_STAGE_RETRIEVERS
        for representation in REPRESENTATIONS
    ]
    windows, pairs, conditions = build_payload_data(
        tokenizer=CharacterTokenizer(),
        b1_rows=b1_rows,
        prompts=prompts,
        representations=representations,
        budgets={"p1": 40},
        overlap_tokens=4,
    )
    require(len(conditions) == 12, "SkillRouter payload condition matrix self-test failed")
    require(len(pairs) == len(REPRESENTATIONS) * PRIMARY_K, "SkillRouter pair deduplication self-test failed")
    require(len(windows) >= len(pairs), "SkillRouter window construction self-test failed")
    stale_version_rejected = False
    try:
        require_current_b1_version(
            {"version_id": "rq2b-stale-version"},
            "synthetic-stale-manifest",
        )
    except ValueError:
        stale_version_rejected = True
    require(stale_version_rejected, "SkillRouter stale B1 manifest self-test failed")
    prompt_binding = {"path": "prompt_manifest.jsonl", "sha256": "prompt-sha256", "rows": 1}
    representation_bindings = {
        representation: {
            "path": f"representations/{representation}.jsonl",
            "sha256": f"{representation}-sha256",
            "rows": 2433,
        }
        for representation in REPRESENTATIONS
    }
    bm25_manifest = {
        "schema_version": "rq2b-bm25-run-manifest-v1",
        "version_id": VERSION_ID,
        "runner_version": BM25_RUNNER_VERSION,
        "network_calls": 0,
        "retriever": "bm25",
        "representation": "i1-discovery",
        "configuration": {
            "tokenizer": "lowercase_[a-z0-9]+",
            "query_term_frequency": "multiplicative",
            "k1": BM25_K1,
            "b": BM25_B,
            "corpus_documents": 2433,
            "persisted_top_k": BM25_TOP_PERSISTED,
            "tie_break": "skill_id_ascending",
        },
        "counts": {"documents": 2433, "prompts": 1, "rows": 1},
        "inputs": {
            "representation_path": representation_bindings["i1-discovery"]["path"],
            "representation_sha256": representation_bindings["i1-discovery"]["sha256"],
            "prompt_manifest_path": prompt_binding["path"],
            "prompt_manifest_sha256": prompt_binding["sha256"],
        },
    }
    validate_b1_manifest_binding(
        bm25_manifest,
        "synthetic-current-bm25",
        prompt_binding=prompt_binding,
        representation_bindings=representation_bindings,
    )
    stale_prompt_binding_rejected = False
    try:
        validate_b1_manifest_binding(
            {
                **bm25_manifest,
                "inputs": {
                    **bm25_manifest["inputs"],
                    "prompt_manifest_sha256": "stale-prompt-sha256",
                },
            },
            "synthetic-stale-prompt-binding",
            prompt_binding=prompt_binding,
            representation_bindings=representation_bindings,
        )
    except ValueError:
        stale_prompt_binding_rejected = True
    require(stale_prompt_binding_rejected, "SkillRouter stale prompt-binding self-test failed")
    wrong_retriever_configuration_rejected = False
    try:
        validate_b1_manifest_binding(
            {
                **bm25_manifest,
                "configuration": {**bm25_manifest["configuration"], "k1": 9.0},
            },
            "synthetic-wrong-bm25-configuration",
            prompt_binding=prompt_binding,
            representation_bindings=representation_bindings,
        )
    except ValueError:
        wrong_retriever_configuration_rejected = True
    require(
        wrong_retriever_configuration_rejected,
        "SkillRouter wrong retriever-configuration self-test failed",
    )
    qwen_manifest = {
        "schema_version": "rq2b-qwen-run-manifest-v1",
        "version_id": VERSION_ID,
        "runner_version": QWEN_RUNNER_VERSION,
        "base_url": QWEN_BASE_URL,
        "model": QWEN_MODEL,
        "dimensions": QWEN_DIMENSIONS,
        "automatic_retries": 0,
    }
    qwen_payload = {
        "schema_version": "rq2b-qwen-payload-manifest-v1",
        "version_id": VERSION_ID,
        "state": "sealed_not_executed",
        "base_url": QWEN_BASE_URL,
        "model": QWEN_MODEL,
        "dimensions": QWEN_DIMENSIONS,
        "chunker_version": CHUNKER_VERSION,
        "prompt_manifest": prompt_binding,
        "representation_inputs": representation_bindings,
    }
    validate_b1_manifest_binding(
        qwen_manifest,
        "synthetic-current-qwen",
        prompt_binding=prompt_binding,
        representation_bindings=representation_bindings,
        qwen_payload=qwen_payload,
    )
    stale_representation_binding_rejected = False
    try:
        validate_b1_manifest_binding(
            qwen_manifest,
            "synthetic-stale-qwen-representation",
            prompt_binding=prompt_binding,
            representation_bindings=representation_bindings,
            qwen_payload={
                **qwen_payload,
                "representation_inputs": {
                    **representation_bindings,
                    "i1-discovery": {
                        **representation_bindings["i1-discovery"],
                        "sha256": "stale-representation-sha256",
                    },
                },
            },
        )
    except ValueError:
        stale_representation_binding_rejected = True
    require(
        stale_representation_binding_rejected,
        "SkillRouter stale representation-binding self-test failed",
    )
    skillrouter_embedding_manifest = {
        "schema_version": "rq2b-skillrouter-embedding-run-manifest-v1",
        "version_id": VERSION_ID,
        "runner_version": SKILLROUTER_EMBEDDING_RUNNER_VERSION,
        "retriever": "skillrouter-embedding",
        "model": SKILLROUTER_EMBEDDING_MODEL,
        "revision": SKILLROUTER_EMBEDDING_REVISION,
        "dimensions": SKILLROUTER_EMBEDDING_DIMENSIONS,
        "maximum_model_tokens": SKILLROUTER_EMBEDDING_MAX_TOKENS,
        "pooling": "last_non_padding_token",
        "normalization": "l2",
        "aggregation": "single_full_context_cosine",
        "query_instruction": SKILLROUTER_EMBEDDING_QUERY_INSTRUCTION,
        "automatic_retries": 0,
        "b0f_a1_amendment_sha256": B0F_A1_AMENDMENT_SHA256,
        "model_snapshot": {
            "path": "synthetic-snapshot",
            "revision": SKILLROUTER_EMBEDDING_REVISION,
            "files": {
                "tokenizer.json": SKILLROUTER_EMBEDDING_TOKENIZER_SHA256,
                "config.json": SKILLROUTER_EMBEDDING_CONFIG_SHA256,
                "model.safetensors": SKILLROUTER_EMBEDDING_WEIGHTS_SHA256,
            },
        },
    }
    skillrouter_embedding_payload = {
        "schema_version": "rq2b-skillrouter-embedding-payload-manifest-v1",
        "version_id": VERSION_ID,
        "state": "sealed_not_executed",
        "b0f_a1_amendment_sha256": B0F_A1_AMENDMENT_SHA256,
        "model": SKILLROUTER_EMBEDDING_MODEL,
        "revision": SKILLROUTER_EMBEDDING_REVISION,
        "dimensions": SKILLROUTER_EMBEDDING_DIMENSIONS,
        "maximum_model_tokens": SKILLROUTER_EMBEDDING_MAX_TOKENS,
        "query_instruction": SKILLROUTER_EMBEDDING_QUERY_INSTRUCTION,
        "document_serialization": "exact_representation_selector_text",
        "truncation": "forbidden",
        "pooling": "last_non_padding_token",
        "normalization": "l2",
        "score": "cosine",
        "snapshot_audit": {
            "path": "synthetic-or-bound-at-runtime",
            "tokenizer_sha256": SKILLROUTER_EMBEDDING_TOKENIZER_SHA256,
            "config_sha256": SKILLROUTER_EMBEDDING_CONFIG_SHA256,
            "weights_expected_sha256": SKILLROUTER_EMBEDDING_WEIGHTS_SHA256,
            "weights_present_and_verified": True,
        },
        "prompt_manifest": prompt_binding,
        "representation_inputs": representation_bindings,
    }
    validate_b1_manifest_binding(
        skillrouter_embedding_manifest,
        "synthetic-current-skillrouter-embedding",
        prompt_binding=prompt_binding,
        representation_bindings=representation_bindings,
        skillrouter_embedding_payload=skillrouter_embedding_payload,
    )
    stale_skillrouter_embedding_contract_rejected = False
    try:
        validate_b1_manifest_binding(
            skillrouter_embedding_manifest,
            "synthetic-stale-skillrouter-embedding-contract",
            prompt_binding=prompt_binding,
            representation_bindings=representation_bindings,
            skillrouter_embedding_payload={
                **skillrouter_embedding_payload,
                "truncation": "longest_first",
            },
        )
    except ValueError:
        stale_skillrouter_embedding_contract_rejected = True
    require(
        stale_skillrouter_embedding_contract_rejected,
        "SkillRouter embedding stale-contract self-test failed",
    )
    stale_prompt_row_rejected = False
    try:
        validate_b1_row_against_prompt(
            {**b1_rows[0], "prompt_sha256": "stale-prompt-sha256"},
            prompts["p1"],
            "synthetic-stale-prompt-row",
        )
    except ValueError:
        stale_prompt_row_rejected = True
    require(stale_prompt_row_rejected, "SkillRouter stale prompt-row self-test failed")
    qwen_sensitivity_row_rejected = False
    qwen_primary_row = next(
        row for row in b1_rows if row["retriever"] == "qwen-max-chunk"
    )
    try:
        validate_b1_row_against_prompt(
            {
                **qwen_primary_row,
                "retriever": "qwen-mean-chunk-sensitivity",
                "aggregation": "cosine_of_l2_normalized_chunk_mean",
            },
            prompts["p1"],
            "synthetic-qwen-sensitivity-row",
        )
    except ValueError:
        qwen_sensitivity_row_rejected = True
    require(qwen_sensitivity_row_rejected, "SkillRouter Qwen sensitivity-row self-test failed")
    return {
        "state": "synthetic_payload_no_model_forward_no_transfer",
        "network_calls": 0,
        "conditions": len(conditions),
        "unique_pairs": len(pairs),
        "unique_windows": len(windows),
        "stale_b1_version_rejected": stale_version_rejected,
        "stale_prompt_binding_rejected": stale_prompt_binding_rejected,
        "stale_representation_binding_rejected": stale_representation_binding_rejected,
        "stale_prompt_row_rejected": stale_prompt_row_rejected,
        "skillrouter_embedding_manifest_validated": True,
        "stale_skillrouter_embedding_contract_rejected": stale_skillrouter_embedding_contract_rejected,
        "wrong_retriever_configuration_rejected": wrong_retriever_configuration_rejected,
        "qwen_sensitivity_row_rejected": qwen_sensitivity_row_rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--b1-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b1"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        root = args.root.resolve()
        b1_root = args.b1_root if args.b1_root.is_absolute() else root / args.b1_root
        result = build(root, b1_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
