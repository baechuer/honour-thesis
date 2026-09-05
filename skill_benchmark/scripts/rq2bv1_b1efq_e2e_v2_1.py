#!/usr/bin/env python3
"""Local contracts and execution for the B1E-FQ V2.1 end-to-end amendment.

The method is intentionally distinct from B1E-F.  B1E-F used one raw-query
vector against all candidate fields, then took a target-agnostic top two.  This
module instead (1) asks a constrained parser to quote exact request spans,
(2) embeds only the deterministic field-wise serialisations of those spans,
and (3) compares each query field only with the corresponding candidate field.

The module builds/reviews local preflight artifacts by default.  ``--execute``
requires a separately created exact authorisation and is never called by a
preflight or self-test.  No import-time network activity is permitted.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path
from statistics import mean
from typing import Any

from prepare_rq2bv1_v3_qwen_field_aware_preflight import (
    CACHE_ROOT as CANDIDATE_CACHE_ROOT,
    FIELD_COMPONENT_REPRESENTATION,
    FIELD_ORDER as CANDIDATE_FIELD_ORDER,
    PAYLOAD_NAME as CANDIDATE_PAYLOAD_NAME,
    PREFLIGHT_ROOT as CANDIDATE_PREFLIGHT_ROOT,
    RESULT_ROOT as CANDIDATE_RESULT_ROOT,
)
from rq2b_chunking import tokenizer_ids
from rq2b_common import (
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    sha256_text,
    write_json_new,
    write_jsonl_new,
)
from rq2bv1_fq_parser_v2_runtime import (
    ExactQueryParseCacheV2,
    PARSER_INPUT_USD_PER_MILLION_TOKENS,
    PARSER_OUTPUT_USD_PER_MILLION_TOKENS,
    PARSER_PRICE_DATE,
    PARSER_PRICE_SOURCE_URL,
    post_chat_once,
    provider_input_token_upper_bound,
    provider_usage,
)
from rq2bv1_query_field_parser_v2 import (
    FIELD_ORDER as QUERY_FIELD_ORDER,
    MAX_TOTAL_EXCERPT_CHARS,
    MAX_TOTAL_EXCERPTS,
    PARSER_BASE_URL,
    PARSER_MAX_OUTPUT_TOKENS,
    PARSER_MODEL,
    parser_contract,
    parser_contract_sha256,
    request_payload,
    validate_response,
)
from rq2bv1_field_aligned_scoring import score_candidate
from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight
from run_rq2b_qwen import (
    BASE_URL as EMBEDDING_BASE_URL,
    DIMENSIONS,
    MODEL as EMBEDDING_MODEL,
    ExactEmbeddingCache,
    post_embedding_once,
)


METHOD_VERSION = "rq2bv1-v3-b1e-fq-e2e-v2-1"
PREFLIGHT_ROOT = "skill_benchmark/rq2bv1/preflight/qwen_field_aligned_e2e_v2_1_full"
RESULT_ROOT = "skill_benchmark/rq2bv1/results/qwen_field_aligned_e2e_v2_1_full"
PARSER_CACHE_ROOT = "skill_benchmark/cache/rq2bv1/query_parses_v2_1_e2e_full"
QUERY_FIELD_CACHE_ROOT = "skill_benchmark/cache/rq2bv1/query_field_embeddings_v2_1"
RUN_ID = "rq2bv1-v3-qwen-field-aligned-e2e-v2-1-full-001"
PAYLOAD_NAME = "payload_manifest.json"
PACKET_NAME = "execution_approval_packet.json"
REVIEW_NAME = "local_protocol_review.json"
INVENTORY_NAME = "parser_request_inventory.jsonl"
REPORT_NAME = "preflight_report.json"
AUTHORISATION_CONSUMPTION_ROOT = "skill_benchmark/rq2bv1/approvals/consumed"
DEFAULT_AUTHORISATION = "skill_benchmark/rq2bv1/approvals/qwen_field_aligned_e2e_v2_1_execution_authorisation.json"
TIMEOUT_SECONDS = 120
EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS = 0.07
EMBEDDING_PRICE_DATE = "2026-08-22"
EMBEDDING_PRICE_SOURCE_URL = "https://www.alibabacloud.com/help/en/model-studio/embedding-interfaces-compatible-with-openai"

QUERY_TO_CANDIDATE_FIELD = {
    "use_condition": "use_conditions",
    "input_precondition": "input_preconditions",
    "output_artifact": "output_artifacts",
    "workflow_procedure": "workflow_steps",
    "dependency_resource": "dependencies_resources",
    "boundary_not_for": "constraints_boundaries",
    "success_verification": "success_criteria",
}
require(tuple(QUERY_TO_CANDIDATE_FIELD) == QUERY_FIELD_ORDER, "FQ query field map order drift")
require(tuple(QUERY_TO_CANDIDATE_FIELD.values()) == CANDIDATE_FIELD_ORDER, "FQ candidate field map order drift")

RUNNER_DEPENDENCIES = (
    "skill_benchmark/scripts/rq2bv1_b1efq_e2e_v2_1.py",
    "skill_benchmark/scripts/rq2bv1_query_field_parser_v2.py",
    "skill_benchmark/scripts/rq2bv1_fq_parser_v2_runtime.py",
    "skill_benchmark/scripts/rq2bv1_field_aligned_scoring.py",
    "skill_benchmark/scripts/prepare_rq2bv1_v3_qwen_field_aware_preflight.py",
    "skill_benchmark/scripts/run_rq2b_qwen.py",
    "skill_benchmark/scripts/rq2b_chunking.py",
    "skill_benchmark/scripts/rq2b_common.py",
)


def _path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _binding(root: Path, path: Path) -> dict[str, str]:
    require(path.is_file(), f"Missing bound artifact: {path}")
    return {"path": relative(path, root), "sha256": sha256_file(path)}


def _read_bound(root: Path, binding: dict[str, str], label: str) -> Path:
    require(set(binding).issuperset({"path", "sha256"}) and set(binding).issubset({"path", "sha256", "rows"}), f"{label} binding schema drift")
    path = _path(root, binding["path"])
    require(path.is_file() and sha256_file(path) == binding["sha256"], f"{label} binding drift")
    return path


def _strict_prompts(root: Path) -> tuple[Path, list[dict[str, Any]]]:
    _, _, prompts = verify_preflight(root)
    prompt_path = root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
    require(prompt_path.is_file(), "FQ strict-prompt artifact is missing")
    require(len(prompts) == 381 and len({str(row["prompt_id"]) for row in prompts}) == 381, "FQ strict prompt coverage drift")
    prompts = sorted(prompts, key=lambda row: str(row["prompt_id"]))
    return prompt_path, prompts


def _tokenizer(root: Path) -> tuple[Any, dict[str, Any]]:
    from transformers import AutoTokenizer

    token_audit_path = root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"
    audit = read_json(token_audit_path)["qwen"]
    snapshot = Path(audit["local_proxy_tokenizer_snapshot"])
    tokenizer_file = snapshot / "tokenizer.json"
    require(tokenizer_file.is_file(), "Qwen proxy tokenizer is unavailable")
    require(sha256_file(tokenizer_file) == audit["local_proxy_tokenizer_sha256"], "Qwen proxy tokenizer drift")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    return AutoTokenizer.from_pretrained(snapshot, local_files_only=True), audit


def _candidate_context(root: Path) -> tuple[dict[str, Any], dict[str, str], dict[str, dict[str, str]], ExactEmbeddingCache]:
    """Validate and bind completed candidate vectors without contacting Qwen."""
    payload_path = root / CANDIDATE_PREFLIGHT_ROOT / CANDIDATE_PAYLOAD_NAME
    result_manifest_path = root / CANDIDATE_RESULT_ROOT / "manifest.json"
    verification_path = root / CANDIDATE_RESULT_ROOT / "post_run_verification.json"
    require(payload_path.is_file() and result_manifest_path.is_file() and verification_path.is_file(), "Completed B1E-F candidate artifacts are missing")
    payload, result_manifest, verification = read_json(payload_path), read_json(result_manifest_path), read_json(verification_path)
    require(payload.get("schema_version") == "rq2bv1-v3-qwen-field-aware-payload-v1" and payload.get("state") == "sealed_not_executed", "B1E-F candidate payload drift")
    require(verification.get("state") == "passed_local_post_run_integrity_verification", "B1E-F candidate verification is not passed")
    require(result_manifest.get("state") == "qwen_field_aware_completed_pending_user_result_review", "B1E-F candidate run state drift")
    require(result_manifest.get("payload") == _binding(root, payload_path), "B1E-F candidate payload/result binding drift")
    inventory_path = _read_bound(root, payload["text_inventory"], "B1E-F candidate inventory")
    inventory = read_jsonl(inventory_path)
    by_text_id = {str(row["text_id"]): str(row["text"]) for row in inventory}
    require(len(inventory) == 3786 and len(by_text_id) == len(inventory), "B1E-F candidate inventory coverage drift")
    cache = ExactEmbeddingCache(root / CANDIDATE_CACHE_ROOT)
    candidate_components: dict[str, dict[str, str]] = {}
    for document in payload["documents"]:
        skill_id = str(document["skill_id"])
        components = document["components"]
        require(len(components) == 7 and [item["field_key"] for item in components] == list(CANDIDATE_FIELD_ORDER), "B1E-F candidate component order drift")
        candidate_components[skill_id] = {str(item["field_key"]): str(item["text_id"]) for item in components}
    require(len(candidate_components) == 2433, "B1E-F candidate library size drift")
    for text_id, text in by_text_id.items():
        require(sha256_text(text) == text_id and cache.load(text) is not None, f"B1E-F candidate cache coverage drift: {text_id}")
    return payload, by_text_id, candidate_components, cache


def _fallback_rows(root: Path, prompts: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    result_path = root / "skill_benchmark/rq2bv1/results/qwen_primary_v3/qwen_primary_strict_results.jsonl"
    verification_path = root / "skill_benchmark/rq2bv1/results/qwen_primary_v3/post_run_verification.json"
    require(result_path.is_file() and verification_path.is_file(), "Completed Qwen primary fallback artifacts are missing")
    verification = read_json(verification_path)
    require(verification.get("state") == "passed_local_post_run_integrity_verification", "Qwen primary fallback verification is not passed")
    rows = [row for row in read_jsonl(result_path) if row.get("representation") == "i3c-fielded-evidence" and row.get("retriever") == "qwen-text-embedding-v4"]
    by_id = {str(row["prompt_id"]): row for row in rows}
    expected = {str(row["prompt_id"]) for row in prompts}
    require(len(rows) == len(by_id) == len(expected) and set(by_id) == expected, "Qwen primary I3C fallback coverage drift")
    return by_id, {"primary_rows": _binding(root, result_path), "primary_verification": _binding(root, verification_path)}


def _serialize_query_fields(parsed: dict[str, Any], tokenizer: Any, token_audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Turn validated exact spans into deterministic field-specific embedding texts.

    Joining multiple verbatim spans with a newline does not add a rewritten
    requirement.  The newline is an explicit local serialisation delimiter and
    each non-newline character is an exact raw-request substring.
    """
    fields = parsed["fields"]
    active = tuple(parsed["active_fields"])
    require(active and all(field in QUERY_FIELD_ORDER for field in active), "FQ active field drift")
    values: dict[str, dict[str, Any]] = {}
    for field in active:
        spans = fields[field]
        text = "\n".join(str(span["text"]) for span in spans)
        require(bool(text), f"FQ empty serialised field: {field}")
        local_tokens = len(tokenizer_ids(tokenizer, text))
        require(local_tokens <= int(token_audit["provider_documented_per_text_limit"]), f"FQ serialised field exceeds Qwen per-text limit: {field}")
        values[field] = {
            "field": field,
            "candidate_field": QUERY_TO_CANDIDATE_FIELD[field],
            "text": text,
            "text_sha256": sha256_text(text),
            "utf8_bytes": len(text.encode("utf-8")),
            "local_proxy_tokens": local_tokens,
            "span_count": len(spans),
            "serialisation": "newline_join_exact_validated_raw_prompt_spans_no_field_label",
        }
    require(tuple(values) == active, "FQ serialised field ordering drift")
    return values


def _upper_query_field_budget(prompts: list[dict[str, Any]], tokenizer: Any) -> dict[str, int]:
    """Conservative pre-parser envelope for dynamically generated field texts."""
    maximum_texts = len(prompts) * len(QUERY_FIELD_ORDER)
    maximum_utf8_bytes = len(prompts) * (MAX_TOTAL_EXCERPT_CHARS * 4 + MAX_TOTAL_EXCERPTS - 1)
    maximum_proxy_tokens = 0
    for prompt in prompts:
        raw_tokens = len(tokenizer_ids(tokenizer, str(prompt["prompt"])))
        maximum_proxy_tokens += min(MAX_TOTAL_EXCERPT_CHARS * 4, raw_tokens * MAX_TOTAL_EXCERPTS)
    return {
        "maximum_query_field_texts": maximum_texts,
        "maximum_query_field_embedding_requests": len(prompts),
        "maximum_query_field_external_submissions": maximum_texts,
        "maximum_query_field_utf8_bytes": maximum_utf8_bytes,
        "maximum_query_field_local_proxy_tokens": maximum_proxy_tokens,
        "maximum_query_field_provider_input_tokens": math.ceil(maximum_proxy_tokens * 1.10),
    }


def _execution_script_bindings(root: Path) -> list[dict[str, str]]:
    return [_binding(root, root / path) for path in RUNNER_DEPENDENCIES]


def _candidate_matrices(candidate_components: dict[str, dict[str, str]], candidate_texts: dict[str, str], candidate_cache: ExactEmbeddingCache) -> tuple[list[str], dict[str, Any]]:
    """Load the sealed candidate field vectors once for vectorised local scoring."""
    import numpy as np

    skill_ids = list(candidate_components)
    matrices: dict[str, Any] = {}
    for query_field, candidate_field in QUERY_TO_CANDIDATE_FIELD.items():
        values = [candidate_cache.load(candidate_texts[candidate_components[skill_id][candidate_field]]) for skill_id in skill_ids]
        require(all(value is not None for value in values), f"FQ candidate cache coverage drift: {candidate_field}")
        matrix = np.asarray(values, dtype=np.float64)
        require(matrix.shape == (2433, DIMENSIONS), f"FQ candidate matrix shape drift: {candidate_field}")
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        require(bool(np.all(np.isfinite(norms))) and bool(np.all(norms > 0.0)), f"FQ candidate matrix norm drift: {candidate_field}")
        matrices[query_field] = matrix / norms
    return skill_ids, matrices


def build_preflight(root: Path) -> dict[str, Any]:
    root = root.resolve()
    prompt_path, prompts = _strict_prompts(root)
    tokenizer, token_audit = _tokenizer(root)
    candidate_payload, _, candidate_components, _ = _candidate_context(root)
    fallback_rows, fallback_binding = _fallback_rows(root, prompts)
    require(len(candidate_components) == 2433 and len(fallback_rows) == len(prompts), "FQ local provenance preflight drift")
    preflight_root = root / PREFLIGHT_ROOT
    staging = preflight_root.with_name(f".{preflight_root.name}.staging")
    require(not preflight_root.exists() and not staging.exists(), "Refusing to overwrite FQ E2E preflight")
    inventory: list[dict[str, Any]] = []
    for prompt in prompts:
        raw_query = str(prompt["prompt"])
        inventory.append({
            "schema_version": f"{METHOD_VERSION}-parser-request-v1",
            "prompt_id": str(prompt["prompt_id"]),
            "prompt_sha256": str(prompt["prompt_sha256"]),
            "raw_query": raw_query,
            "raw_query_utf8_bytes": len(raw_query.encode("utf-8")),
            "provider_input_token_upper_bound": provider_input_token_upper_bound(raw_query),
            "request": request_payload(raw_query),
        })
    require(len(inventory) == 381 and len({row["prompt_id"] for row in inventory}) == 381, "FQ parser inventory coverage drift")
    parser_input_cap = sum(int(row["provider_input_token_upper_bound"]) for row in inventory)
    parser_output_cap = len(inventory) * PARSER_MAX_OUTPUT_TOKENS
    parser_price_cap = (parser_input_cap * PARSER_INPUT_USD_PER_MILLION_TOKENS + parser_output_cap * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
    field_budget = _upper_query_field_budget(prompts, tokenizer)
    field_price_cap = field_budget["maximum_query_field_provider_input_tokens"] * EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS / 1_000_000
    counts = {
        "strict_prompts": len(inventory),
        "candidate_library_skills": len(candidate_components),
        "candidate_component_vectors_reused_locally": len(candidate_payload["text_inventory"]["rows"] and range(int(candidate_payload["text_inventory"]["rows"]))),
        "maximum_parser_request_attempts": len(inventory),
        "maximum_parser_successful_calls": len(inventory),
        "maximum_parser_raw_prompt_submissions": len(inventory),
        "maximum_parser_raw_prompt_utf8_bytes": sum(int(row["raw_query_utf8_bytes"]) for row in inventory),
        "maximum_parser_input_tokens": parser_input_cap,
        "maximum_parser_output_tokens": parser_output_cap,
        "maximum_parser_total_tokens": parser_input_cap + parser_output_cap,
        **field_budget,
        "maximum_total_outbound_request_attempts": len(inventory) + field_budget["maximum_query_field_embedding_requests"],
        "maximum_total_successful_calls": len(inventory) + field_budget["maximum_query_field_embedding_requests"],
        "maximum_standard_list_price_usd": math.ceil((parser_price_cap + field_price_cap) * 1_000_000) / 1_000_000,
    }
    staging.mkdir(parents=True, exist_ok=False)
    inventory_path = staging / INVENTORY_NAME
    write_jsonl_new(inventory_path, inventory)
    final_inventory_binding = {"path": relative(preflight_root / INVENTORY_NAME, root), "sha256": sha256_file(inventory_path)}
    final_inventory = preflight_root / INVENTORY_NAME
    payload = {
        "schema_version": f"{METHOD_VERSION}-payload-v1",
        "state": "sealed_not_executed",
        "network_calls": 0,
        "run_id": RUN_ID,
        "method": {
            "name": "query_structured_field_aligned_qwen",
            "parser": "grounded_exact_raw_request_span_parser_v2_1",
            "query_field_serialisation": "newline_join_exact_validated_raw_prompt_spans_no_field_label",
            "candidate_representation": FIELD_COMPONENT_REPRESENTATION,
            "matching": "same_semantic_field_cosine_only",
            "aggregation": "equal_weight_mean_over_parser_active_fields",
            "candidate_tie_break": "skill_id_ascending",
            "fallback": "completed_qwen_i3c_fielded_single_vector_row_only_when_parser_or_field_embedding_is_unavailable",
        },
        "parser": {
            "base_url": PARSER_BASE_URL,
            "model": PARSER_MODEL,
            "contract_sha256": parser_contract_sha256(),
            "contract": parser_contract(),
        },
        "query_field_embedding": {
            "base_url": EMBEDDING_BASE_URL,
            "model": EMBEDDING_MODEL,
            "dimensions": DIMENSIONS,
            "cache_root": QUERY_FIELD_CACHE_ROOT,
            "per_prompt_batching": "one request containing all previously uncached active field texts, maximum seven texts",
            "automatic_retries": 0,
        },
        "strict_population": {"prompts": len(inventory), "candidate_library_skills": len(candidate_components), "candidate_text_submissions": 0},
        "parser_request_inventory": final_inventory_binding,
        "prompt_artifact": _binding(root, prompt_path),
        "candidate_field_payload": _binding(root, root / CANDIDATE_PREFLIGHT_ROOT / CANDIDATE_PAYLOAD_NAME),
        "candidate_field_run_manifest": _binding(root, root / CANDIDATE_RESULT_ROOT / "manifest.json"),
        "candidate_field_verification": _binding(root, root / CANDIDATE_RESULT_ROOT / "post_run_verification.json"),
        "fallback_binding": fallback_binding,
        "token_audit": _binding(root, root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json"),
        "counts": counts,
        "pricing_snapshot": {
            "parser": {"date": PARSER_PRICE_DATE, "source_url": PARSER_PRICE_SOURCE_URL, "input_usd_per_million_tokens": PARSER_INPUT_USD_PER_MILLION_TOKENS, "output_usd_per_million_tokens": PARSER_OUTPUT_USD_PER_MILLION_TOKENS, "ceiling_usd": parser_price_cap},
            "embedding": {"date": EMBEDDING_PRICE_DATE, "source_url": EMBEDDING_PRICE_SOURCE_URL, "input_usd_per_million_tokens": EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS, "ceiling_usd": field_price_cap},
        },
        "execution_boundary": {
            "external_transfer_authorised": False,
            "paid_api_authorised": False,
            "automatic_retries": 0,
            "candidate_text_submissions": 0,
            "query_field_text_origin": "only local serialisations of V2.1 validated exact raw-prompt spans; no candidate, gold, cluster, skill ID, rank, or target-field metadata",
            "parser_raw_prompt_origin": "only the original strict benchmark prompt plus fixed parser instruction",
            "fallback_rows_are_not_pure_field_aligned_results": True,
            "reranking": False,
            "thesis_result_writing_authorised": False,
        },
    }
    payload_path = staging / PAYLOAD_NAME
    write_json_new(payload_path, payload)
    final_payload = preflight_root / PAYLOAD_NAME
    final_payload_binding = {"path": relative(final_payload, root), "sha256": sha256_file(payload_path)}
    packet = {
        "schema_version": f"{METHOD_VERSION}-execution-approval-packet-v1",
        "state": "awaiting_independent_review_then_one_exact_end_to_end_authorisation",
        "run_id": RUN_ID,
        "payload": final_payload_binding,
        "output_dir": RESULT_ROOT,
        "parser_cache_root": PARSER_CACHE_ROOT,
        "query_field_cache_root": QUERY_FIELD_CACHE_ROOT,
        "authorisation_consumption_root": AUTHORISATION_CONSUMPTION_ROOT,
        "parser": payload["parser"],
        "query_field_embedding": payload["query_field_embedding"],
        "counts": counts,
        "execution_scripts": _execution_script_bindings(root),
        "resumption_policy": "one user-authorised serial execution may resume only from durable records; a call with an attempt record but no durable completion is converted to fallback and never resent",
        "excluded_actions": [
            "no automatic retry or hidden request replay",
            "no candidate skill text, gold label, skill_id, cluster, ranking, or target-field metadata sent externally",
            "no candidate embedding; completed B1E-F candidate vectors are read locally only",
            "no reranker or hosted SkillRouter",
            "no thesis LaTeX or PDF result writing",
            "no claim that fallback rows are pure field-aligned retrieval",
        ],
    }
    packet_path = staging / PACKET_NAME
    write_json_new(packet_path, packet)
    report = {
        "schema_version": f"{METHOD_VERSION}-preflight-report-v1",
        "state": "preflight_passed_local_only_no_external_text_sent",
        "network_calls": 0,
        "payload": final_payload_binding,
        "execution_packet": {"path": relative(preflight_root / PACKET_NAME, root), "sha256": sha256_file(packet_path)},
        "counts": counts,
        "checks": {
            "strict_prompt_hashes": len(inventory),
            "candidate_component_vectors_locally_verified": int(candidate_payload["text_inventory"]["rows"]),
            "fallback_i3c_rows_locally_verified": len(fallback_rows),
            "candidate_texts_visible_to_parser": 0,
            "network_calls": 0,
        },
        "next_gate": "independent_local_review_then_one_exact_end_to_end_authorisation",
    }
    write_json_new(staging / REPORT_NAME, report)
    staging.rename(preflight_root)
    return report


def _load_preflight(root: Path) -> tuple[Path, dict[str, Any], Path, dict[str, Any], list[dict[str, Any]]]:
    preflight_root = root / PREFLIGHT_ROOT
    payload_path, packet_path = preflight_root / PAYLOAD_NAME, preflight_root / PACKET_NAME
    payload, packet = read_json(payload_path), read_json(packet_path)
    require(payload.get("schema_version") == f"{METHOD_VERSION}-payload-v1" and payload.get("state") == "sealed_not_executed", "FQ E2E payload state drift")
    require(packet.get("schema_version") == f"{METHOD_VERSION}-execution-approval-packet-v1" and packet.get("state") == "awaiting_independent_review_then_one_exact_end_to_end_authorisation", "FQ E2E packet state drift")
    require(packet.get("payload") == _binding(root, payload_path), "FQ E2E packet/payload drift")
    inventory_path = _read_bound(root, payload["parser_request_inventory"], "FQ parser inventory")
    inventory = read_jsonl(inventory_path)
    require(len(inventory) == 381 and len({row["prompt_id"] for row in inventory}) == 381, "FQ E2E inventory coverage drift")
    for row in inventory:
        require(row["request"] == request_payload(str(row["raw_query"])), f"FQ parser request reconstruction drift: {row['prompt_id']}")
        require(row["prompt_sha256"] == sha256_text(str(row["raw_query"])), f"FQ parser prompt digest drift: {row['prompt_id']}")
    return payload_path, payload, packet_path, packet, inventory


def review_preflight(root: Path) -> dict[str, Any]:
    root = root.resolve()
    payload_path, payload, packet_path, packet, inventory = _load_preflight(root)
    prompt_path, prompts = _strict_prompts(root)
    tokenizer, audit = _tokenizer(root)
    candidate_payload, _, candidates, _ = _candidate_context(root)
    fallbacks, fallback_binding = _fallback_rows(root, prompts)
    require(payload["prompt_artifact"] == _binding(root, prompt_path), "FQ E2E prompt artifact drift")
    require(payload["candidate_field_payload"] == _binding(root, root / CANDIDATE_PREFLIGHT_ROOT / CANDIDATE_PAYLOAD_NAME), "FQ E2E candidate payload drift")
    require(payload["fallback_binding"] == fallback_binding, "FQ E2E fallback binding drift")
    bound = _upper_query_field_budget(prompts, tokenizer)
    require(all(payload["counts"][key] == value for key, value in bound.items()), "FQ E2E dynamic field budget drift")
    require(payload["counts"]["candidate_library_skills"] == len(candidates) == 2433, "FQ E2E candidate count drift")
    require(len(fallbacks) == len(inventory), "FQ E2E fallback count drift")
    review_path = root / PREFLIGHT_ROOT / REVIEW_NAME
    require(not review_path.exists(), "Refusing to overwrite FQ E2E local review")
    review = {
        "schema_version": f"{METHOD_VERSION}-local-protocol-review-v1",
        "state": "local_protocol_review_passed_no_network_no_external_text_sent",
        "network_calls": 0,
        "payload": _binding(root, payload_path),
        "execution_packet": _binding(root, packet_path),
        "checks": {
            "parser_requests": len(inventory),
            "raw_prompt_hashes_reconstructed": len(inventory),
            "candidate_library_skills_visible_to_parser": 0,
            "candidate_component_vectors_reused_local_only": int(candidate_payload["text_inventory"]["rows"]),
            "fallback_i3c_rows": len(fallbacks),
            "query_field_serialisation": payload["method"]["query_field_serialisation"],
            "query_field_per_text_limit": int(audit["provider_documented_per_text_limit"]),
            "automatic_retries": 0,
            "thesis_result_writing_authorised": False,
        },
        "next_gate": "one_exact_end_to_end_user_authorisation_using_execution_packet_sha256",
    }
    write_json_new(review_path, review)
    return review


def _validate_authorisation(root: Path, authorisation_path: Path, packet_path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    authorisation = read_json(authorisation_path)
    require(authorisation.get("schema_version") == f"{METHOD_VERSION}-execution-authorisation-v1", "FQ E2E authorisation schema drift")
    require(authorisation.get("state") == "explicitly_authorised_for_one_resumable_qwen_field_aligned_e2e_v2_1_execution", "FQ E2E execution is not authorised")
    require(authorisation.get("approved_packet") == _binding(root, packet_path), "FQ E2E authorisation packet drift")
    review_path = root / PREFLIGHT_ROOT / REVIEW_NAME
    require(authorisation.get("local_protocol_review") == _binding(root, review_path), "FQ E2E authorisation review drift")
    for key in ("run_id", "output_dir", "parser_cache_root", "query_field_cache_root", "authorisation_consumption_root", "resumption_policy"):
        require(authorisation.get(key) == packet.get(key), f"FQ E2E authorisation mismatch: {key}")
    require(authorisation.get("counts") == packet.get("counts"), "FQ E2E authorisation count ceiling drift")
    require(authorisation.get("execution_scripts") == packet.get("execution_scripts"), "FQ E2E authorisation script binding drift")
    require(authorisation.get("thesis_result_writing_authorised") is False and authorisation.get("automatic_retries") == 0, "FQ E2E authorisation boundary drift")
    for binding in packet["execution_scripts"]:
        _read_bound(root, binding, "FQ E2E execution script")
    return authorisation


def _consume_or_resume_authorisation(root: Path, authorisation_path: Path, packet_path: Path, packet: dict[str, Any], staging: Path) -> Path:
    receipt_root = root / AUTHORISATION_CONSUMPTION_ROOT
    receipt = receipt_root / f"{RUN_ID}-{sha256_file(packet_path)}-{sha256_file(authorisation_path)}.json"
    if receipt.exists():
        value = read_json(receipt)
        require(value.get("state") == "consumed_before_first_provider_attempt" and value.get("packet") == _binding(root, packet_path), "FQ E2E authorisation consumption drift")
        return receipt
    require(not staging.exists(), "FQ E2E staging exists without an authorisation receipt")
    receipt_root.mkdir(parents=True, exist_ok=True)
    write_json_new(receipt, {
        "schema_version": f"{METHOD_VERSION}-authorisation-consumption-v1",
        "state": "consumed_before_first_provider_attempt",
        "packet": _binding(root, packet_path),
        "authorisation": _binding(root, authorisation_path),
        "automatic_retries": 0,
        "network_calls_before_receipt": 0,
        "resumption_policy": packet["resumption_policy"],
        "thesis_result_writing": False,
    })
    return receipt


def _fallback_result(prompt: dict[str, Any], fallback: dict[str, Any], *, parser_status: str, failure_class: str, parser_seconds: float, field_embedding_status: str) -> dict[str, Any]:
    return {
        "schema_version": f"{METHOD_VERSION}-result-row-v1",
        "method_source": "fallback_i3c_single_vector",
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": fallback["strict_gold_rank"],
        "strict_hit_at_1": fallback["strict_hit_at_1"],
        "strict_recall_at_5": fallback["strict_recall_at_5"],
        "strict_recall_at_20": fallback["strict_recall_at_20"],
        "strict_recall_at_50": fallback["strict_recall_at_50"],
        "strict_recall_at_100": fallback["strict_recall_at_100"],
        "strict_mrr_at_10": fallback["strict_mrr_at_10"],
        "top_5_skill_ids": fallback["top_5_skill_ids"],
        "top_20_skill_ids": fallback["top_20_skill_ids"],
        "top_50_skill_ids": fallback["top_50_skill_ids"],
        "top_100": fallback["top_100"],
        "selector_visible_tokens": fallback["selector_visible_tokens"],
        "timing": {
            "cold_parser_seconds": parser_seconds,
            "cold_query_field_embedding_seconds": 0.0,
            "local_field_alignment_seconds": 0.0,
            "reused_primary_i3c_query_embedding_seconds_not_reexecuted": float(fallback["retriever_metadata"]["cold_query_embedding_seconds"]),
        },
        "parser": {"status": parser_status, "failure_class": failure_class},
        "query_field_embedding": {"status": field_embedding_status, "active_fields": [], "external_text_submissions": 0},
        "retriever_metadata": {
            "retriever": "qwen-text-embedding-v4-i3c-single-vector-fallback",
            "fallback_source_representation": "i3c-fielded-evidence",
            "fallback_is_not_pure_field_aligned": True,
        },
    }


def _field_aligned_result(prompt: dict[str, Any], ranking: list[tuple[str, float]], *, parsed: dict[str, Any], field_texts: dict[str, dict[str, Any]], parser_seconds: float, embedding_seconds: float, alignment_seconds: float, selector_tokens: int) -> dict[str, Any]:
    ranks = {skill_id: index for index, (skill_id, _) in enumerate(ranking, start=1)}
    gold_rank = int(ranks[prompt["gold_skill"]])
    top100 = ranking[:100]
    return {
        "schema_version": f"{METHOD_VERSION}-result-row-v1",
        "method_source": "pure_query_structured_field_aligned",
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": gold_rank,
        "strict_hit_at_1": int(gold_rank == 1),
        "strict_recall_at_5": int(gold_rank <= 5),
        "strict_recall_at_20": int(gold_rank <= 20),
        "strict_recall_at_50": int(gold_rank <= 50),
        "strict_recall_at_100": int(gold_rank <= 100),
        "strict_mrr_at_10": 0.0 if gold_rank > 10 else 1.0 / gold_rank,
        "top_5_skill_ids": [skill_id for skill_id, _ in ranking[:5]],
        "top_20_skill_ids": [skill_id for skill_id, _ in ranking[:20]],
        "top_50_skill_ids": [skill_id for skill_id, _ in ranking[:50]],
        "top_100": [{"rank": index, "skill_id": skill_id, "score": score} for index, (skill_id, score) in enumerate(top100, start=1)],
        "selector_visible_tokens": selector_tokens,
        "timing": {"cold_parser_seconds": parser_seconds, "cold_query_field_embedding_seconds": embedding_seconds, "local_field_alignment_seconds": alignment_seconds, "reused_primary_i3c_query_embedding_seconds_not_reexecuted": 0.0},
        "parser": {"status": "valid", "failure_class": None, "active_fields": parsed["active_fields"], "query_field_text_sha256": parsed["query_field_text_sha256"]},
        "query_field_embedding": {
            "status": "valid",
            "active_fields": list(field_texts),
            "external_text_submissions": None,
            "field_texts": [{key: value[key] for key in ("field", "candidate_field", "text_sha256", "utf8_bytes", "local_proxy_tokens", "span_count", "serialisation")} for value in field_texts.values()],
        },
        "retriever_metadata": {
            "retriever": "qwen-text-embedding-v4-query-structured-field-aligned",
            "candidate_representation": FIELD_COMPONENT_REPRESENTATION,
            "same_field_mapping": QUERY_TO_CANDIDATE_FIELD,
            "aggregation": "equal_weight_mean_over_parser_active_fields",
            "candidate_tie_break": "skill_id_ascending",
            "fallback_is_not_pure_field_aligned": False,
        },
    }


def _validate_result_row(row: dict[str, Any], prompt: dict[str, Any]) -> None:
    require(row["prompt_id"] == prompt["prompt_id"] and row["prompt_sha256"] == prompt["prompt_sha256"], "FQ result prompt identity drift")
    require(row["gold_skill"] == prompt["gold_skill"] and 1 <= int(row["strict_gold_rank"]) <= 2433, "FQ result gold drift")
    top100 = row["top_100"]
    require(len(top100) == 100 and [item["rank"] for item in top100] == list(range(1, 101)), "FQ result top-100 drift")
    ids = [item["skill_id"] for item in top100]
    require(len(ids) == len(set(ids)) and row["top_5_skill_ids"] == ids[:5] and row["top_20_skill_ids"] == ids[:20] and row["top_50_skill_ids"] == ids[:50], "FQ result ranking prefix drift")
    rank = int(row["strict_gold_rank"])
    require(row["strict_hit_at_1"] == int(rank == 1) and row["strict_recall_at_20"] == int(rank <= 20), "FQ result metric drift")
    require(row["method_source"] in {"pure_query_structured_field_aligned", "fallback_i3c_single_vector"}, "FQ method source drift")


def _run_scoring(skill_ids: list[str], candidate_matrices: dict[str, Any], field_texts: dict[str, dict[str, Any]], query_vectors: dict[str, list[float]]) -> tuple[list[tuple[str, float]], float]:
    """Vectorised equivalent of equal-weight same-field ``score_candidate`` calls."""
    import numpy as np

    started = time.perf_counter()
    active = tuple(field_texts)
    scores = np.zeros(len(skill_ids), dtype=np.float64)
    for field in active:
        query = np.asarray(query_vectors[field], dtype=np.float64)
        require(query.shape == (DIMENSIONS,), f"FQ query vector shape drift: {field}")
        norm = float(np.linalg.norm(query))
        require(math.isfinite(norm) and norm > 0.0, f"FQ query vector norm drift: {field}")
        scores += candidate_matrices[field] @ (query / norm)
    scores /= len(active)
    ranking = list(zip(skill_ids, (float(value) for value in scores), strict=True))
    ranking.sort(key=lambda item: (-item[1], item[0]))
    return ranking, time.perf_counter() - started


def _parse_entry(raw_query: str, response: dict[str, Any] | None, seconds: float, failure: str | None) -> dict[str, Any]:
    if failure is not None:
        return {"status": "fallback", "parsed": None, "failure_class": failure, "request_seconds": seconds, "provider_usage": {"prompt_tokens": 0, "completion_tokens": 0}}
    try:
        usage = provider_usage(response or {})
        choice = (response or {})["choices"][0]
        if choice.get("finish_reason") != "stop":
            return {"status": "fallback", "parsed": None, "failure_class": f"provider_finish_reason_{choice.get('finish_reason') or 'missing'}", "request_seconds": seconds, "provider_usage": usage}
        parsed = validate_response(raw_query, json.loads(choice["message"]["content"]))
        return {"status": "valid", "parsed": parsed.as_dict(), "failure_class": None, "request_seconds": seconds, "provider_usage": usage}
    except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return {"status": "fallback", "parsed": None, "failure_class": "parser_response_invalid", "request_seconds": seconds, "provider_usage": {"prompt_tokens": 0, "completion_tokens": 0}}


def _record_json_once(path: Path, value: dict[str, Any]) -> None:
    require(not path.exists(), f"Refusing to overwrite durable FQ record: {path}")
    write_json_new(path, value)


def execute(root: Path, authorisation_path: Path, api_key_env: str) -> dict[str, Any]:
    """Run one user-authorised serial, resumable E2E pass with no request retries."""
    root = root.resolve()
    payload_path, payload, packet_path, packet, inventory = _load_preflight(root)
    review_path = root / PREFLIGHT_ROOT / REVIEW_NAME
    review = read_json(review_path)
    require(review.get("state") == "local_protocol_review_passed_no_network_no_external_text_sent" and review.get("execution_packet") == _binding(root, packet_path), "FQ E2E local review drift")
    authorisation = _validate_authorisation(root, authorisation_path, packet_path, packet)
    prompts_path, prompts = _strict_prompts(root)
    prompts_by_id = {str(row["prompt_id"]): row for row in prompts}
    require(set(prompts_by_id) == {row["prompt_id"] for row in inventory}, "FQ E2E prompt population drift")
    tokenizer, token_audit = _tokenizer(root)
    _, candidate_texts, candidate_components, candidate_cache = _candidate_context(root)
    candidate_skill_ids, candidate_matrices = _candidate_matrices(candidate_components, candidate_texts, candidate_cache)
    fallback_by_id, _ = _fallback_rows(root, prompts)
    selector_tokens = int(read_json(root / CANDIDATE_PREFLIGHT_ROOT / CANDIDATE_PAYLOAD_NAME)["counts"]["selector_visible_tokens"])
    output_root = root / RESULT_ROOT
    staging = output_root.with_name(f".{output_root.name}.staging")
    receipt = _consume_or_resume_authorisation(root, authorisation_path, packet_path, packet, staging)
    if not staging.exists():
        require(not output_root.exists(), "Refusing to overwrite completed FQ E2E output")
        staging.mkdir(parents=True, exist_ok=False)
        _record_json_once(staging / "run_started.json", {"schema_version": f"{METHOD_VERSION}-run-start-v1", "packet": _binding(root, packet_path), "authorisation": _binding(root, authorisation_path), "authorisation_consumption": _binding(root, receipt), "automatic_retries": 0})
        (staging / "parser_records").mkdir()
        (staging / "embedding_records").mkdir()
        (staging / "rows").mkdir()
    else:
        started = read_json(staging / "run_started.json")
        require(started.get("packet") == _binding(root, packet_path) and started.get("authorisation") == _binding(root, authorisation_path), "FQ E2E resume binding drift")
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), "FQ E2E API key environment variable is missing")
    parser_cache = ExactQueryParseCacheV2(root / PARSER_CACHE_ROOT, RUN_ID)
    query_cache = ExactEmbeddingCache(root / QUERY_FIELD_CACHE_ROOT)
    parser_records, embedding_records, row_root = staging / "parser_records", staging / "embedding_records", staging / "rows"
    parser_attempts = parser_successes = parser_input_tokens = parser_output_tokens = 0
    parser_seconds_total = embedding_attempts = embedding_successes = embedding_input_tokens = embedding_seconds_total = 0.0
    external_field_submissions = 0

    for index, item in enumerate(inventory):
        prompt_id = str(item["prompt_id"])
        prompt = prompts_by_id[prompt_id]
        row_path = row_root / f"{index:04d}.json"
        if row_path.exists():
            continue
        raw_query = str(item["raw_query"])
        parse_cache_entry = parser_cache.load(raw_query)
        parser_record = parser_records / f"{index:04d}.json"
        parser_attempt = parser_records / f"{index:04d}_attempt.json"
        if parse_cache_entry is None:
            if parser_attempt.exists():
                entry = _parse_entry(raw_query, None, 0.0, "interrupted_parser_attempt_unknown_delivery")
                _record_json_once(parser_record, {"state": "interrupted_attempt_converted_to_fallback_without_retry", "entry": entry})
                parser_cache.store(raw_query, entry)
            else:
                _record_json_once(parser_attempt, {"schema_version": f"{METHOD_VERSION}-parser-attempt-v1", "state": "persisted_before_provider_call", "prompt_id": prompt_id, "prompt_sha256": item["prompt_sha256"], "request": item["request"], "automatic_retries": 0})
                parser_attempts += 1
                started = time.monotonic()
                try:
                    response = post_chat_once(api_key, item["request"], TIMEOUT_SECONDS)
                except Exception as exc:
                    entry = _parse_entry(raw_query, None, time.monotonic() - started, "parser_transport")
                    _record_json_once(parser_record, {"state": "transport_fallback_no_retry", "error_type": type(exc).__name__, "error_message": str(exc), "entry": entry})
                else:
                    entry = _parse_entry(raw_query, response, time.monotonic() - started, None)
                    _record_json_once(parser_record, {"state": "provider_response_processed", "entry": entry, "response": response})
                parser_cache.store(raw_query, entry)
            parse_cache_entry = parser_cache.load(raw_query)
        require(parse_cache_entry is not None, "FQ E2E parser cache write drift")
        parser_seconds_total += float(parse_cache_entry["request_seconds"])
        parser_input_tokens += int(parse_cache_entry["provider_usage"]["prompt_tokens"])
        parser_output_tokens += int(parse_cache_entry["provider_usage"]["completion_tokens"])
        if parse_cache_entry["status"] == "valid":
            parser_successes += 1
        else:
            row = _fallback_result(prompt, fallback_by_id[prompt_id], parser_status="fallback", failure_class=str(parse_cache_entry["failure_class"]), parser_seconds=float(parse_cache_entry["request_seconds"]), field_embedding_status="not_attempted_parser_fallback")
            _validate_result_row(row, prompt)
            _record_json_once(row_path, row)
            continue

        field_texts = _serialize_query_fields(parse_cache_entry["parsed"], tokenizer, token_audit)
        embedding_record = embedding_records / f"{index:04d}.json"
        embedding_attempt = embedding_records / f"{index:04d}_attempt.json"
        field_vectors: dict[str, list[float]] = {}
        field_embedding_seconds = 0.0
        embedding_failure: str | None = None
        if embedding_record.exists():
            saved = read_json(embedding_record)
            require(saved.get("field_texts") == {field: {key: value[key] for key in ("text_sha256", "text", "local_proxy_tokens", "utf8_bytes")} for field, value in field_texts.items()}, "FQ E2E field embedding resume content drift")
            if saved.get("status") == "valid":
                for field, value in field_texts.items():
                    vector = query_cache.load(value["text"])
                    require(vector is not None, f"FQ E2E query field cache missing on resume: {prompt_id}:{field}")
                    field_vectors[field] = vector
                field_embedding_seconds = float(saved["request_seconds"])
            else:
                embedding_failure = str(saved["failure_class"])
        elif embedding_attempt.exists():
            embedding_failure = "interrupted_field_embedding_attempt_unknown_delivery"
            _record_json_once(embedding_record, {"state": "interrupted_attempt_converted_to_fallback_without_retry", "status": "fallback", "failure_class": embedding_failure, "request_seconds": 0.0, "field_texts": {field: {key: value[key] for key in ("text_sha256", "text", "local_proxy_tokens", "utf8_bytes")} for field, value in field_texts.items()}})
        else:
            missing = [value for value in field_texts.values() if query_cache.load(value["text"]) is None]
            for field, value in field_texts.items():
                cached = query_cache.load(value["text"])
                if cached is not None:
                    field_vectors[field] = cached
            if missing:
                _record_json_once(embedding_attempt, {"schema_version": f"{METHOD_VERSION}-field-embedding-attempt-v1", "state": "persisted_before_provider_call", "prompt_id": prompt_id, "prompt_sha256": item["prompt_sha256"], "field_texts": [{key: value[key] for key in ("field", "text", "text_sha256", "utf8_bytes", "local_proxy_tokens")} for value in missing], "automatic_retries": 0})
                embedding_attempts += 1
                started = time.monotonic()
                try:
                    response = post_embedding_once(api_key, [str(value["text"]) for value in missing], TIMEOUT_SECONDS)
                    data = response.get("data")
                    require(isinstance(data, list) and len(data) == len(missing), "FQ E2E field embedding row-count drift")
                    ordered = sorted(data, key=lambda row: int(row["index"]))
                    require([int(row["index"]) for row in ordered] == list(range(len(missing))), "FQ E2E field embedding index drift")
                    usage = response.get("usage") or {}
                    require(isinstance(usage, dict), "FQ E2E field embedding usage drift")
                    for value, returned in zip(missing, ordered, strict=True):
                        vector = [float(item) for item in returned["embedding"]]
                        require(len(vector) == DIMENSIONS and all(math.isfinite(item) for item in vector), "FQ E2E field vector drift")
                        query_cache.store(value["text"], vector, local_proxy_tokens=int(value["local_proxy_tokens"]), provider_usage=usage)
                    field_embedding_seconds = time.monotonic() - started
                    external_field_submissions += len(missing)
                    embedding_successes += 1
                    embedding_input_tokens += int(usage.get("prompt_tokens", 0))
                    _record_json_once(embedding_record, {"state": "provider_response_cached", "status": "valid", "failure_class": None, "request_seconds": field_embedding_seconds, "provider_usage": usage, "field_texts": {field: {key: value[key] for key in ("text_sha256", "text", "local_proxy_tokens", "utf8_bytes")} for field, value in field_texts.items()}})
                except Exception as exc:
                    field_embedding_seconds = time.monotonic() - started
                    embedding_failure = "field_embedding_transport_or_response"
                    _record_json_once(embedding_record, {"state": "fallback_no_retry", "status": "fallback", "failure_class": embedding_failure, "request_seconds": field_embedding_seconds, "error_type": type(exc).__name__, "error_message": str(exc), "field_texts": {field: {key: value[key] for key in ("text_sha256", "text", "local_proxy_tokens", "utf8_bytes")} for field, value in field_texts.items()}})
                embedding_seconds_total += field_embedding_seconds
            if embedding_failure is None:
                for field, value in field_texts.items():
                    vector = query_cache.load(value["text"])
                    require(vector is not None, f"FQ E2E query field cache missing after call: {prompt_id}:{field}")
                    field_vectors[field] = vector
        if embedding_failure is not None:
            row = _fallback_result(prompt, fallback_by_id[prompt_id], parser_status="valid", failure_class=embedding_failure, parser_seconds=float(parse_cache_entry["request_seconds"]), field_embedding_status="fallback")
        else:
            ranking, alignment_seconds = _run_scoring(candidate_skill_ids, candidate_matrices, field_texts, field_vectors)
            row = _field_aligned_result(prompt, ranking, parsed=parse_cache_entry["parsed"], field_texts=field_texts, parser_seconds=float(parse_cache_entry["request_seconds"]), embedding_seconds=field_embedding_seconds, alignment_seconds=alignment_seconds, selector_tokens=selector_tokens)
        _validate_result_row(row, prompt)
        _record_json_once(row_path, row)

    row_paths = sorted(row_root.glob("*.json"))
    require(len(row_paths) == len(inventory), "FQ E2E result coverage is incomplete")
    rows = [read_json(path) for path in row_paths]
    rows.sort(key=lambda row: str(row["prompt_id"]))
    for row in rows:
        _validate_result_row(row, prompts_by_id[str(row["prompt_id"])])
    pure = [row for row in rows if row["method_source"] == "pure_query_structured_field_aligned"]
    fallback = [row for row in rows if row["method_source"] == "fallback_i3c_single_vector"]
    metrics = lambda values: {"rows": len(values), "hit_at_1": mean(float(row["strict_hit_at_1"]) for row in values) if values else None, "mrr_at_10": mean(float(row["strict_mrr_at_10"]) for row in values) if values else None, "recall_at_20": mean(float(row["strict_recall_at_20"]) for row in values) if values else None}
    rows_path = staging / "field_aligned_results.jsonl"
    write_jsonl_new(rows_path, rows)
    ledger = {
        "schema_version": f"{METHOD_VERSION}-cost-ledger-v1",
        "automatic_retries": 0,
        "parser": {"request_attempts_observed_this_process": parser_attempts, "successful_calls_observed_this_process": parser_successes, "input_tokens_observed_this_process": parser_input_tokens, "output_tokens_observed_this_process": parser_output_tokens, "wall_seconds_observed_this_process": parser_seconds_total, "standard_list_price_usd_observed_this_process": (parser_input_tokens * PARSER_INPUT_USD_PER_MILLION_TOKENS + parser_output_tokens * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000},
        "query_field_embedding": {"request_attempts_observed_this_process": embedding_attempts, "successful_calls_observed_this_process": embedding_successes, "external_text_submissions_observed_this_process": external_field_submissions, "input_tokens_observed_this_process": embedding_input_tokens, "wall_seconds_observed_this_process": embedding_seconds_total, "standard_list_price_usd_observed_this_process": embedding_input_tokens * EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS / 1_000_000},
        "candidate_field_embeddings": {"external_text_submissions_this_run": 0, "reused_completed_b1e_f_component_vectors": 3786},
        "coverage": {"all_rows": len(rows), "pure_field_aligned_rows": len(pure), "fallback_rows": len(fallback), "pure_metrics": metrics(pure), "hybrid_coverage_metrics": metrics(rows)},
    }
    ledger_path = staging / "cost_ledger.json"
    write_json_new(ledger_path, ledger)
    manifest = {
        "schema_version": f"{METHOD_VERSION}-run-manifest-v1",
        "state": "complete_pending_user_result_review",
        "run_id": RUN_ID,
        "payload": _binding(root, payload_path),
        "execution_packet": _binding(root, packet_path),
        "local_protocol_review": _binding(root, review_path),
        "authorisation": _binding(root, authorisation_path),
        "authorisation_consumption": _binding(root, receipt),
        "method": payload["method"],
        "artifacts": {"rows": _binding(root, rows_path), "cost_ledger": _binding(root, ledger_path), "per_prompt_rows": len(rows)},
        "network_calls_confirmed_this_process": parser_successes + embedding_successes,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.rename(output_root)
    return manifest


def verify_completed(root: Path) -> dict[str, Any]:
    root = root.resolve()
    payload_path, payload, packet_path, _, inventory = _load_preflight(root)
    output_root = root / RESULT_ROOT
    manifest_path, rows_path, ledger_path = output_root / "manifest.json", output_root / "field_aligned_results.jsonl", output_root / "cost_ledger.json"
    receipt_path = output_root / "independent_verification.json"
    require(manifest_path.is_file() and rows_path.is_file() and ledger_path.is_file() and not receipt_path.exists(), "FQ E2E completed artifacts are unavailable or already verified")
    manifest, rows, ledger = read_json(manifest_path), read_jsonl(rows_path), read_json(ledger_path)
    require(manifest.get("state") == "complete_pending_user_result_review" and manifest.get("payload") == _binding(root, payload_path) and manifest.get("execution_packet") == _binding(root, packet_path), "FQ E2E completed manifest drift")
    prompts_path, prompts = _strict_prompts(root)
    prompts_by_id = {str(row["prompt_id"]): row for row in prompts}
    require(len(rows) == len(inventory) == len(prompts_by_id), "FQ E2E completed result coverage drift")
    for row in rows:
        _validate_result_row(row, prompts_by_id[str(row["prompt_id"])])
    pure = [row for row in rows if row["method_source"] == "pure_query_structured_field_aligned"]
    fallback = [row for row in rows if row["method_source"] == "fallback_i3c_single_vector"]
    require(ledger["coverage"]["pure_field_aligned_rows"] == len(pure) and ledger["coverage"]["fallback_rows"] == len(fallback), "FQ E2E ledger coverage drift")
    receipt = {
        "schema_version": f"{METHOD_VERSION}-verification-receipt-v1",
        "state": "verified_complete_with_explicit_pure_and_fallback_subsets",
        "network_calls": 0,
        "result_manifest": _binding(root, manifest_path),
        "checks": {"rows": len(rows), "pure_field_aligned_rows": len(pure), "fallback_rows": len(fallback), "candidate_embedding_calls_this_run": 0, "automatic_retries": 0, "thesis_result_writing": False},
        "next_gate": "user_review_of_results_before_thesis_integration",
    }
    write_json_new(receipt_path, receipt)
    return receipt


def self_test() -> dict[str, Any]:
    query = "Convert scanned invoices into page-anchored JSON without cloud OCR."
    provider_payload = {"fields": {field: [] for field in QUERY_FIELD_ORDER}}
    provider_payload["fields"]["input_precondition"] = ["scanned invoices"]
    provider_payload["fields"]["output_artifact"] = ["page-anchored JSON"]
    provider_payload["fields"]["boundary_not_for"] = ["without cloud OCR"]
    parsed = validate_response(query, provider_payload).as_dict()
    require(parsed["active_fields"] == ["input_precondition", "output_artifact", "boundary_not_for"], "FQ E2E parser self-test drift")
    require(QUERY_TO_CANDIDATE_FIELD["input_precondition"] == "input_preconditions", "FQ E2E field map self-test drift")
    score = score_candidate({"input_precondition": [1.0, 0.0]}, {"input_precondition": [1.0, 0.0]}, ("input_precondition",))
    require(score["score"] == 1.0, "FQ E2E aligned scorer self-test drift")
    return {"schema_version": f"{METHOD_VERSION}-self-test-v1", "state": "passed_zero_network", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--build-preflight", action="store_true")
    parser.add_argument("--review-preflight", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--authorisation", type=Path, default=Path(DEFAULT_AUTHORISATION))
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    args = parser.parse_args()
    choices = [args.self_test, args.build_preflight, args.review_preflight, args.execute, args.verify]
    require(sum(bool(value) for value in choices) == 1, "Choose exactly one FQ E2E action")
    root = args.root.resolve()
    if args.self_test:
        result = self_test()
    elif args.build_preflight:
        result = build_preflight(root)
    elif args.review_preflight:
        result = review_preflight(root)
    elif args.execute:
        result = execute(root, _path(root, args.authorisation), args.api_key_env)
    else:
        result = verify_completed(root)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
