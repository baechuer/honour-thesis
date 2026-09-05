#!/usr/bin/env python3
"""Freeze a local-only payload for RQ2b V3 Qwen field-aware B1E-F.

The script never contacts DashScope or ranks a query.  It binds the final V3
I3C evidence spans to exactly seven labelled candidate blocks, verifies that
the already-completed Qwen-primary run supplies each cached raw-query vector,
and writes an exact payload plus a later execution-approval packet.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
from typing import Any

from prepare_rq2b_i3c_v3_b1l_preflight import REPRESENTATIONS
from rq2b_chunking import tokenizer_ids
from rq2b_common import (
    FIELD_SPECS,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_text,
    write_json_new,
    write_jsonl_new,
)
from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight
from run_rq2b_qwen import BASE_URL, DIMENSIONS, MAX_BATCH_TEXTS, MODEL, ExactEmbeddingCache


PREFLIGHT_VERSION = "rq2bv1-v3-qwen-field-aware-preflight-v1"
PREFLIGHT_ROOT = "skill_benchmark/rq2bv1/preflight/qwen_field_aware_v3"
TEXT_INVENTORY_NAME = "field_component_inventory.jsonl"
PAYLOAD_NAME = "payload_manifest.json"
REPORT_NAME = "preflight_report.json"
CHECKPOINT_NAME = "preflight_checkpoint.json"
PACKET_NAME = "execution_approval_packet.json"
RUNNER_PATH = "skill_benchmark/scripts/run_rq2bv1_v3_qwen_field_aware.py"
VERIFIER_PATH = "skill_benchmark/scripts/verify_rq2bv1_v3_qwen_field_aware.py"
RUNNER_DEPENDENCIES = (
    RUNNER_PATH,
    VERIFIER_PATH,
    "skill_benchmark/scripts/run_rq2bv1_v3_qwen_primary.py",
    "skill_benchmark/scripts/run_rq2b_qwen.py",
    "skill_benchmark/scripts/rq2b_common.py",
    "skill_benchmark/scripts/rq2b_v11_execution_contract.py",
)
CACHE_ROOT = "skill_benchmark/cache/rq2bv1/embeddings"
RESULT_ROOT = "skill_benchmark/rq2bv1/results/qwen_field_aware_v3"
RUN_ID = "rq2bv1-v3-qwen-field-aware-001"
TIMEOUT_SECONDS = 120
FIELD_COMPONENT_REPRESENTATION = "i3c-field-aware-evidence"
FIELD_ORDER = tuple(field for field, _ in FIELD_SPECS)
FIELD_LABELS = dict(FIELD_SPECS)
PRIMARY_OUTPUT_ROOT = "skill_benchmark/rq2bv1/results/qwen_primary_v3"
PRICING_SNAPSHOT_DATE = "2026-08-22"
PRICE_SOURCE_URL = "https://www.alibabacloud.com/help/en/model-studio/embedding-interfaces-compatible-with-openai"
EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS = 0.07


def _register_text(
    texts: dict[str, dict[str, Any]], *, text: str, local_proxy_tokens: int, role: dict[str, Any]
) -> str:
    require(bool(text), "Field component text must be non-empty")
    text_id = sha256_text(text)
    existing = texts.get(text_id)
    if existing is None:
        texts[text_id] = {
            "schema_version": "rq2bv1-qwen-field-aware-component-v1",
            "text_id": text_id,
            "text_sha256": text_id,
            "text": text,
            "utf8_bytes": len(text.encode("utf-8")),
            "local_proxy_tokens": int(local_proxy_tokens),
            "roles": [role],
        }
    else:
        require(existing["text"] == text, "Field-component SHA-256 collision")
        require(int(existing["local_proxy_tokens"]) == int(local_proxy_tokens), "Field-component token drift")
        existing["roles"].append(role)
    return text_id


def _field_block(label: str, spans: list[dict[str, Any]]) -> str:
    # The label-only form is the frozen empty-field representation.
    return f"{label}:\n" + "\n".join(f"- {span['selector_evidence']}" for span in spans)


def _canonical_spans(row: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    spans = row.get("selector_evidence_spans")
    require(isinstance(spans, list), f"I3C spans missing: {row.get('skill_id')}")
    grouped = {field: [] for field in FIELD_ORDER}
    for span in spans:
        require(
            isinstance(span, dict)
            and set(span) == {"field_key", "field_label", "item_id", "selector_evidence", "source_position"},
            f"I3C span schema drift: {row.get('skill_id')}",
        )
        field = str(span["field_key"])
        require(field in grouped, f"Unknown I3C field: {field}")
        require(span["field_label"] == FIELD_LABELS[field], f"Field label drift: {field}")
        require(isinstance(span["selector_evidence"], str) and bool(span["selector_evidence"]), "Empty I3C evidence")
        require(isinstance(span["source_position"], int) and span["source_position"] >= 0, "Invalid source position")
        grouped[field].append(span)
    for field in FIELD_ORDER:
        grouped[field].sort(key=lambda span: (int(span["source_position"]), str(span["item_id"])))
    return grouped


def _primary_query_binding(root: Path, prompts: list[dict[str, Any]], cache: ExactEmbeddingCache) -> dict[str, Any]:
    output_root = root / PRIMARY_OUTPUT_ROOT
    verification_path = output_root / "post_run_verification.json"
    rows_path = output_root / "qwen_primary_strict_results.jsonl"
    require(verification_path.is_file() and rows_path.is_file(), "Completed Qwen-primary artifacts are required")
    verification = read_json(verification_path)
    require(verification.get("state") == "passed_local_post_run_integrity_verification", "Qwen-primary verification is not passed")
    rows = read_jsonl(rows_path)
    by_prompt: dict[str, float] = {}
    for row in rows:
        prompt_id = str(row["prompt_id"])
        seconds = float(row["retriever_metadata"]["cold_query_embedding_seconds"])
        previous = by_prompt.setdefault(prompt_id, seconds)
        require(abs(previous - seconds) <= 1e-12, f"Qwen-primary cold-query timing drift: {prompt_id}")
    require(set(by_prompt) == {str(prompt["prompt_id"]) for prompt in prompts}, "Qwen-primary prompt coverage drift")
    bindings: dict[str, dict[str, Any]] = {}
    for prompt in prompts:
        prompt_id = str(prompt["prompt_id"])
        vector = cache.load(str(prompt["prompt"]))
        require(vector is not None, f"Missing exact cached Qwen query vector: {prompt_id}")
        bindings[prompt_id] = {
            "prompt_sha256": str(prompt["prompt_sha256"]),
            "query_text_sha256": sha256_text(str(prompt["prompt"])),
            "reused_primary_cold_query_embedding_seconds": by_prompt[prompt_id],
        }
    return {
        "primary_post_run_verification": {
            "path": relative(verification_path, root),
            "sha256": sha256_file(verification_path),
        },
        "primary_result_rows": {"path": relative(rows_path, root), "sha256": sha256_file(rows_path)},
        "query_vectors": bindings,
    }


def build(root: Path) -> dict[str, Any]:
    from transformers import AutoTokenizer

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    _, representations, prompts = verify_preflight(root)
    require(set(representations) == set(REPRESENTATIONS) and len(prompts) == 381, "B1L binding drift")
    fielded_rows = representations["i3c-fielded-evidence"]
    require(len(fielded_rows) == 2433, "I3C candidate count drift")

    token_audit = read_json(root / "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json")["qwen"]
    tokenizer_path = Path(token_audit["local_proxy_tokenizer_snapshot"])
    tokenizer_file = tokenizer_path / "tokenizer.json"
    require(tokenizer_file.is_file(), "Qwen proxy tokenizer is unavailable")
    require(sha256_file(tokenizer_file) == token_audit["local_proxy_tokenizer_sha256"], "Proxy tokenizer hash drift")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    cache = ExactEmbeddingCache(root / CACHE_ROOT)
    query_binding = _primary_query_binding(root, prompts, cache)

    texts: dict[str, dict[str, Any]] = {}
    documents: list[dict[str, Any]] = []
    for row in fielded_rows:
        grouped = _canonical_spans(row)
        components: list[dict[str, Any]] = []
        for field in FIELD_ORDER:
            block = _field_block(FIELD_LABELS[field], grouped[field])
            token_count = len(tokenizer_ids(tokenizer, block))
            require(token_count <= int(token_audit["provider_documented_per_text_limit"]), f"Field block exceeds provider limit: {row['skill_id']}:{field}")
            text_id = _register_text(
                texts,
                text=block,
                local_proxy_tokens=token_count,
                role={
                    "kind": "document_chunk",
                    "representation": FIELD_COMPONENT_REPRESENTATION,
                    "skill_id": str(row["skill_id"]),
                    "field_key": field,
                },
            )
            components.append(
                {
                    "field_key": field,
                    "field_label": FIELD_LABELS[field],
                    "text_id": text_id,
                    "text_sha256": sha256_text(block),
                    "local_proxy_tokens": token_count,
                    "evidence_count": len(grouped[field]),
                }
            )
        require(len(components) == 7 and [item["field_key"] for item in components] == list(FIELD_ORDER), "Seven-field component drift")
        documents.append({"source_row_index": int(row["source_row_index"]), "skill_id": str(row["skill_id"]), "components": components})
    require([document["skill_id"] for document in documents] == [row["skill_id"] for row in fielded_rows], "Candidate ordering drift")

    rows = [texts[text_id] for text_id in sorted(texts)]
    for row in rows:
        row["roles"] = sorted(row["roles"], key=lambda role: (str(role["skill_id"]), FIELD_ORDER.index(str(role["field_key"]))))
    cache_misses = [row for row in rows if cache.load(str(row["text"])) is None]
    preflight_root = root / PREFLIGHT_ROOT
    staging = preflight_root.with_name(f".{preflight_root.name}.staging")
    require(not preflight_root.exists() and not staging.exists(), "Refusing to overwrite B1E-F preflight")
    staging.mkdir(parents=True, exist_ok=False)
    text_path = staging / TEXT_INVENTORY_NAME
    write_jsonl_new(text_path, rows)
    selector_tokens = sum(sum(int(component["local_proxy_tokens"]) for component in document["components"]) for document in documents)
    max_new_proxy_tokens = sum(int(row["local_proxy_tokens"]) for row in cache_misses)
    max_new_utf8_bytes = sum(int(row["utf8_bytes"]) for row in cache_misses)
    max_provider_prompt_tokens = math.ceil(max_new_proxy_tokens * 1.10)
    # Round up to a whole mill, rather than down to a precision that could
    # understate the authorised price ceiling.
    max_standard_list_price_usd = math.ceil(
        max_provider_prompt_tokens * EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS / 1_000_000 * 1_000
    ) / 1_000
    payload = {
        "schema_version": "rq2bv1-v3-qwen-field-aware-payload-v1",
        "state": "sealed_not_executed",
        "network_calls": 0,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "strict_population": {"candidate_library_skills": 2433, "strict_prompts": 381, "expected_result_rows": 381},
        "field_components": {
            "representation": FIELD_COMPONENT_REPRESENTATION,
            "field_order": list(FIELD_ORDER),
            "empty_field_serialization": "<field label>:\\n",
            "present_field_serialization": "<field label>:\\n- <exact selector evidence>...",
            "candidate_tie_break": "skill_id_ascending",
            "aggregation": "mean_of_descending_top_two_of_seven_cosines",
            "source_representation": "i3c-fielded-evidence",
        },
        "prompt_artifact": {
            "path": relative(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl", root),
            "sha256": sha256_file(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"),
        },
        "query_cache_binding": query_binding,
        "i3c_fielded_artifact": {
            "path": relative(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_merged_final/i3c-fielded-evidence.jsonl", root),
            "sha256": sha256_file(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_merged_final/i3c-fielded-evidence.jsonl"),
        },
        "text_inventory": {"path": relative(preflight_root / TEXT_INVENTORY_NAME, root), "sha256": sha256_file(text_path), "rows": len(rows)},
        "documents": documents,
        "tokenizer": {
            "snapshot": str(tokenizer_path),
            "tokenizer_json_sha256": token_audit["local_proxy_tokenizer_sha256"],
            "provider_documented_per_text_limit": int(token_audit["provider_documented_per_text_limit"]),
        },
        "counts": {
            "field_component_instances": 2433 * 7,
            "unique_document_component_texts": len(rows),
            "cached_component_texts_at_preflight": len(rows) - len(cache_misses),
            "maximum_new_cache_texts": len(cache_misses),
            "maximum_new_cache_proxy_tokens": max_new_proxy_tokens,
            "maximum_new_cache_utf8_bytes": max_new_utf8_bytes,
            "maximum_external_text_submissions": len(cache_misses),
            "maximum_external_submission_proxy_tokens": max_new_proxy_tokens,
            "maximum_external_submission_utf8_bytes": max_new_utf8_bytes,
            "maximum_request_attempts": math.ceil(len(cache_misses) / MAX_BATCH_TEXTS),
            "maximum_successful_api_calls": math.ceil(len(cache_misses) / MAX_BATCH_TEXTS),
            "maximum_provider_prompt_tokens": max_provider_prompt_tokens,
            "maximum_standard_list_price_usd": max_standard_list_price_usd,
            "reused_query_embeddings": len(prompts),
            "query_external_text_submissions": 0,
            "selector_visible_tokens": selector_tokens,
        },
        "authorisation_boundary": {
            "external_transfer_authorised": False,
            "paid_api_authorised": False,
            "automatic_retries": 0,
            "reranking": False,
            "thesis_result_writing_authorised": False,
        },
        "pricing_snapshot": {
            "date": PRICING_SNAPSHOT_DATE,
            "source_url": PRICE_SOURCE_URL,
            "usd_per_million_input_tokens": EMBEDDING_PRICE_USD_PER_MILLION_INPUT_TOKENS,
            "ceiling_basis": "maximum_provider_prompt_tokens",
        },
    }
    payload_path = staging / PAYLOAD_NAME
    write_json_new(payload_path, payload)
    scripts = [{"path": path, "sha256": sha256_file(root / path)} for path in RUNNER_DEPENDENCIES]
    packet = {
        "schema_version": "rq2bv1-v3-qwen-field-aware-execution-approval-packet-v1",
        "state": "awaiting_explicit_external_transfer_authorisation",
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(payload_path)},
        "execution_scripts": scripts,
        "run_id": RUN_ID,
        "output_dir": RESULT_ROOT,
        "cache_root": CACHE_ROOT,
        "base_url": BASE_URL,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "timeout_seconds": TIMEOUT_SECONDS,
        "automatic_retries": 0,
        **{key: payload["counts"][key] for key in payload["counts"] if key.startswith("maximum_")},
        "query_external_text_submissions": 0,
        "pricing_snapshot": payload["pricing_snapshot"],
        "excluded_actions": [
            "no automatic retry", "no query transmission", "no query-side field prediction or oracle routing",
            "no reranking", "no thesis LaTeX or PDF result writing",
        ],
    }
    packet_path = staging / PACKET_NAME
    write_json_new(packet_path, packet)
    report = {
        "schema_version": "rq2bv1-v3-qwen-field-aware-preflight-report-v1",
        "state": "preflight_passed_no_network_no_scoring_external_authorisation_required",
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(payload_path)},
        "execution_packet": {"path": relative(preflight_root / PACKET_NAME, root), "sha256": sha256_file(packet_path)},
        "counts": payload["counts"],
        "validation": {
            "b1l_preflight_replayed": True,
            "field_components_per_candidate": 7,
            "all_query_vectors_reused_from_verified_qwen_primary_cache": True,
            "network_calls": 0,
            "scientific_retrieval_or_reranking": False,
        },
        "next_gate": "independent_local_review_then_exact_external_transfer_authorisation",
    }
    report_path = staging / REPORT_NAME
    write_json_new(report_path, report)
    write_json_new(staging / CHECKPOINT_NAME, {
        "schema_version": "rq2bv1-v3-qwen-field-aware-preflight-checkpoint-v1",
        "state": "qwen_field_aware_preflight_frozen_external_authorisation_required",
        "report": {"path": relative(preflight_root / REPORT_NAME, root), "sha256": sha256_file(report_path)},
        "payload": report["payload"],
        "execution_packet": report["execution_packet"],
        "network_calls": 0,
    })
    staging.rename(preflight_root)
    return report


def self_test() -> dict[str, Any]:
    spans = {field: [] for field in FIELD_ORDER}
    spans[FIELD_ORDER[0]] = [{"selector_evidence": "exact evidence", "source_position": 2, "item_id": "a"}]
    rendered = [_field_block(FIELD_LABELS[field], spans[field]) for field in FIELD_ORDER]
    require(len(rendered) == 7 and all(rendered), "Seven-field serialization failed")
    require(rendered[0] == f"{FIELD_LABELS[FIELD_ORDER[0]]}:\n- exact evidence", "Present field serialization drift")
    require(rendered[1] == f"{FIELD_LABELS[FIELD_ORDER[1]]}:\n", "Empty field serialization drift")
    return {"schema_version": "rq2bv1-v3-qwen-field-aware-preflight-self-test-v1", "state": "self_test_passed", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    import json

    print(json.dumps(self_test() if args.self_test else build(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
