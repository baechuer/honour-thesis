#!/usr/bin/env python3
"""Freeze the zero-network FQ-P Qwen query-parser request inventory.

This stage prepares parser requests only. It does not call a provider, parse a
query, embed a query field, score a candidate, or write thesis material.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from rq2b_common import read_json, relative, repo_root, require, sha256_file, sha256_text, write_json_new, write_jsonl_new
from rq2bv1_query_field_parser import (
    PARSER_BASE_URL,
    PARSER_ENABLE_THINKING,
    PARSER_MAX_OUTPUT_TOKENS,
    PARSER_MODEL,
    parser_contract,
    parser_contract_sha256,
    request_payload,
)
from rq2bv1_fq_parser_execution_contract import (
    AUTHORISATION_CONSUMPTION_ROOT,
    CACHE_ROOT,
    CHECKPOINT_NAME,
    INVENTORY_NAME,
    PACKET_NAME,
    PARSER_INPUT_USD_PER_MILLION_TOKENS,
    PARSER_OUTPUT_USD_PER_MILLION_TOKENS,
    PARSER_PRICE_DATE,
    PARSER_PRICE_SOURCE_URL,
    PAYLOAD_NAME,
    PREFLIGHT_ROOT,
    REPORT_NAME,
    RESULT_ROOT,
    RUN_ID,
    TIMEOUT_SECONDS,
    provider_input_token_upper_bound,
)
from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight


PREFLIGHT_VERSION = "rq2bv1-v3-b1e-fq-parser-preflight-v2"
RUNNER_DEPENDENCIES = (
    "skill_benchmark/scripts/rq2bv1_query_field_parser.py",
    "skill_benchmark/scripts/rq2bv1_fq_parser_execution_contract.py",
    "skill_benchmark/scripts/rq2bv1_b1efq_cost_ledger.py",
    "skill_benchmark/scripts/run_rq2bv1_v3_qwen_field_aligned_parser.py",
    "skill_benchmark/scripts/verify_rq2bv1_v3_qwen_field_aligned_parser.py",
    "skill_benchmark/scripts/rq2b_common.py",
)


def build(root: Path) -> dict[str, Any]:
    preflight_root = root / PREFLIGHT_ROOT
    staging = preflight_root.with_name(f".{preflight_root.name}.staging")
    require(not preflight_root.exists() and not staging.exists(), "Refusing to overwrite FQ-P parser preflight")
    _, _, prompts = verify_preflight(root)
    require(len(prompts) == 381, "FQ-P strict prompt population drift")
    prompt_path = root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
    require(prompt_path.is_file(), "FQ-P strict prompt artifact is missing")

    rows: list[dict[str, Any]] = []
    for prompt in sorted(prompts, key=lambda value: str(value["prompt_id"])):
        raw_query = str(prompt["prompt"])
        require(sha256_text(raw_query) == str(prompt["prompt_sha256"]), f"FQ-P prompt hash drift: {prompt['prompt_id']}")
        outbound = request_payload(raw_query)
        require(set(outbound) == {"model", "temperature", "max_tokens", "enable_thinking", "response_format", "messages"}, "FQ-P outbound request shape drift")
        require(outbound["enable_thinking"] is PARSER_ENABLE_THINKING is False, "FQ-P non-thinking mode drift")
        rows.append(
            {
                "schema_version": "rq2bv1-v3-b1e-fq-parser-request-v1",
                "prompt_id": str(prompt["prompt_id"]),
                "prompt_sha256": str(prompt["prompt_sha256"]),
                "raw_query": raw_query,
                "raw_query_utf8_bytes": len(raw_query.encode("utf-8")),
                "provider_input_token_upper_bound": provider_input_token_upper_bound(raw_query),
                "request": outbound,
            }
        )
    require(len(rows) == 381 and len({row["prompt_id"] for row in rows}) == 381, "FQ-P request identity drift")
    require(all("gold_skill" not in row and "candidate" not in row and "target_field" not in row for row in rows), "FQ-P request inventory leaks routing metadata")

    preflight_root.parent.mkdir(parents=True, exist_ok=True)
    staging.mkdir(parents=False, exist_ok=False)
    inventory_path = staging / INVENTORY_NAME
    final_inventory_path = preflight_root / INVENTORY_NAME
    write_jsonl_new(inventory_path, rows)
    input_cap = sum(int(row["provider_input_token_upper_bound"]) for row in rows)
    output_cap = len(rows) * PARSER_MAX_OUTPUT_TOKENS
    input_price = input_cap * PARSER_INPUT_USD_PER_MILLION_TOKENS / 1_000_000
    output_price = output_cap * PARSER_OUTPUT_USD_PER_MILLION_TOKENS / 1_000_000
    price_cap = math.ceil((input_price + output_price) * 1_000_000) / 1_000_000
    counts = {
        "parser_requests": len(rows),
        "unique_raw_query_texts": len({row["prompt_sha256"] for row in rows}),
        "maximum_external_raw_query_submissions": len(rows),
        "maximum_request_attempts": len(rows),
        "maximum_successful_api_calls": len(rows),
        "maximum_parser_input_tokens": input_cap,
        "maximum_parser_output_tokens": output_cap,
        "maximum_parser_total_tokens": input_cap + output_cap,
        "maximum_standard_list_price_usd": price_cap,
        "maximum_external_raw_query_utf8_bytes": sum(int(row["raw_query_utf8_bytes"]) for row in rows),
    }
    payload = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-payload-v1",
        "state": "sealed_not_executed",
        "network_calls": 0,
        "run_id": RUN_ID,
        "base_url": PARSER_BASE_URL,
        "model": PARSER_MODEL,
        "parser_contract": {
            "path": "skill_benchmark/scripts/rq2bv1_query_field_parser.py",
            "sha256": sha256_file(root / "skill_benchmark/scripts/rq2bv1_query_field_parser.py"),
            "contract_sha256": parser_contract_sha256(),
            "contract": parser_contract(),
        },
        "strict_population": {"strict_prompts": 381, "candidate_library_skills_visible_to_parser": 0},
        "prompt_artifact": {"path": relative(prompt_path, root), "sha256": sha256_file(prompt_path)},
        "request_inventory": {"path": relative(final_inventory_path, root), "sha256": sha256_file(inventory_path), "rows": len(rows)},
        "counts": counts,
        "authorisation_boundary": {
            "external_transfer_authorised": False,
            "paid_api_authorised": False,
            "automatic_retries": 0,
            "candidate_text_submissions": 0,
            "embedding_calls": 0,
            "retrieval_scoring": False,
            "reranking": False,
            "thesis_result_writing_authorised": False,
        },
        "pricing_snapshot": {
            "date": PARSER_PRICE_DATE,
            "source_url": PARSER_PRICE_SOURCE_URL,
            "input_usd_per_million_tokens": PARSER_INPUT_USD_PER_MILLION_TOKENS,
            "output_usd_per_million_tokens": PARSER_OUTPUT_USD_PER_MILLION_TOKENS,
            "ceiling_basis": "conservative_input_byte_upper_bound_plus_max_output_tokens",
        },
    }
    payload_path = staging / PAYLOAD_NAME
    final_payload_path = preflight_root / PAYLOAD_NAME
    write_json_new(payload_path, payload)
    scripts = [{"path": path, "sha256": sha256_file(root / path)} for path in RUNNER_DEPENDENCIES]
    packet = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-execution-approval-packet-v1",
        "state": "awaiting_independent_review_then_explicit_parser_transfer_authorisation",
        "payload": {"path": relative(final_payload_path, root), "sha256": sha256_file(payload_path)},
        "execution_scripts": scripts,
        "run_id": RUN_ID,
        "output_dir": RESULT_ROOT,
        "cache_root": CACHE_ROOT,
        "authorisation_consumption_root": AUTHORISATION_CONSUMPTION_ROOT,
        "base_url": PARSER_BASE_URL,
        "model": PARSER_MODEL,
        "timeout_seconds": TIMEOUT_SECONDS,
        "automatic_retries": 0,
        **{key: value for key, value in counts.items() if key.startswith("maximum_")},
        "excluded_actions": [
            "no automatic retry",
            "one-time authorisation consumption before the first provider attempt",
            "no candidate or gold-label text sent to parser",
            "no query-field embedding",
            "no candidate embedding",
            "no retrieval scoring or reranking",
            "no thesis LaTeX or PDF result writing",
        ],
    }
    packet_path = staging / PACKET_NAME
    final_packet_path = preflight_root / PACKET_NAME
    write_json_new(packet_path, packet)
    report = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-preflight-report-v1",
        "state": "preflight_passed_no_network_no_parser_execution_external_authorisation_required",
        "payload": {"path": relative(final_payload_path, root), "sha256": sha256_file(payload_path)},
        "execution_packet": {"path": relative(final_packet_path, root), "sha256": sha256_file(packet_path)},
        "counts": counts,
        "validation": {
            "b1l_preflight_replayed": True,
            "raw_prompt_hashes_validated": len(rows),
            "parser_request_rows_without_candidate_or_gold_metadata": len(rows),
            "network_calls": 0,
            "scientific_retrieval_or_reranking": False,
        },
        "next_gate": "independent_local_review_then_exact_parser_transfer_authorisation",
    }
    report_path = staging / REPORT_NAME
    final_report_path = preflight_root / REPORT_NAME
    write_json_new(report_path, report)
    write_json_new(staging / CHECKPOINT_NAME, {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-preflight-checkpoint-v1",
        "state": "parser_preflight_frozen_independent_review_required",
        "report": {"path": relative(final_report_path, root), "sha256": sha256_file(report_path)},
        "payload": report["payload"],
        "execution_packet": report["execution_packet"],
        "network_calls": 0,
    })
    staging.rename(preflight_root)
    return report


def self_test() -> dict[str, Any]:
    payload = request_payload("Convert scanned invoices into JSON.")
    require(payload["response_format"] == {"type": "json_object"}, "FQ-P JSON mode drift")
    require("JSON" in str(payload["messages"][0]["content"]), "FQ-P JSON instruction drift")
    require(provider_input_token_upper_bound("x") > 1, "FQ-P input token upper bound drift")
    return {"schema_version": "rq2bv1-v3-b1e-fq-parser-preflight-self-test-v1", "state": "self_test_passed_zero_network", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    print(json.dumps(self_test() if args.self_test else build(args.root.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
