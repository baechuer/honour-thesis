#!/usr/bin/env python3
"""Seal a zero-network V2 B1E-FQ parser smoke or full request inventory."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from rq2b_common import relative, repo_root, require, sha256_file, sha256_text, write_json_new, write_jsonl_new
from rq2bv1_fq_parser_v2_runtime import (
    INVENTORY_NAME,
    PACKET_NAME,
    PARSER_INPUT_USD_PER_MILLION_TOKENS,
    PARSER_MODEL,
    PARSER_OUTPUT_USD_PER_MILLION_TOKENS,
    PARSER_PRICE_DATE,
    PARSER_PRICE_SOURCE_URL,
    PAYLOAD_NAME,
    REPORT_NAME,
    TIMEOUT_SECONDS,
    contains_forbidden_routing_metadata,
    profile,
    provider_input_token_upper_bound,
)
from rq2bv1_query_field_parser_v2 import PARSER_BASE_URL, PARSER_ENABLE_THINKING, PARSER_MAX_OUTPUT_TOKENS, parser_contract, parser_contract_sha256, request_payload
from run_rq2b_i3c_v3_b1l_bm25 import verify_preflight
from test_rq2bv1_b1efq_v2_local_recovery import run as run_local_recovery_test


PREFLIGHT_VERSION = "rq2bv1-v3-b1e-fq-parser-v2-preflight-v1"
RUNNER_DEPENDENCIES = (
    "skill_benchmark/scripts/rq2bv1_query_field_parser_v2.py",
    "skill_benchmark/scripts/rq2bv1_fq_parser_v2_runtime.py",
    "skill_benchmark/scripts/rq2bv1_b1efq_v2_cost_ledger.py",
    "skill_benchmark/scripts/prepare_rq2bv1_v3_qwen_field_aligned_parser_v2_preflight.py",
    "skill_benchmark/scripts/review_rq2bv1_v3_qwen_field_aligned_parser_v2_preflight.py",
    "skill_benchmark/scripts/run_rq2bv1_v3_qwen_field_aligned_parser_v2.py",
    "skill_benchmark/scripts/verify_rq2bv1_v3_qwen_field_aligned_parser_v2.py",
    "skill_benchmark/scripts/test_rq2bv1_b1efq_v2_local_recovery.py",
    "skill_benchmark/scripts/rq2b_common.py",
)


def _selected_prompts(root: Path, profile_name: str) -> tuple[Path, list[dict[str, Any]]]:
    _, _, prompts = verify_preflight(root)
    require(len(prompts) == 381, "B1E-FQ V2 strict prompt population drift")
    prompt_path = root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl"
    require(prompt_path.is_file(), "B1E-FQ V2 strict prompt artifact missing")
    if profile_name == "smoke":
        selected = sorted(prompts, key=lambda item: sha256_text(str(item["prompt_id"])))[:20]
    else:
        selected = sorted(prompts, key=lambda item: str(item["prompt_id"]))
    require(len(selected) == profile(profile_name)["expected_prompts"], "B1E-FQ V2 profile selection drift")
    return prompt_path, selected


def _require_smoke_verified(root: Path) -> None:
    smoke = profile("smoke")
    output_root = root / smoke["result_root"]
    manifest_path, receipt_path = output_root / "manifest.json", output_root / "independent_verification.json"
    require(manifest_path.is_file() and receipt_path.is_file(), "B1E-FQ V2 full preflight requires a verified V2 smoke result")
    value = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(value.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-verification-receipt-v1", "B1E-FQ V2 smoke verification schema drift")
    require(value.get("state") == "verified_complete_with_documented_fallbacks" and value.get("profile") == "smoke", "B1E-FQ V2 smoke verification state drift")
    require(value.get("result_manifest") == {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)}, "B1E-FQ V2 smoke verification manifest binding drift")


def build(root: Path, profile_name: str) -> dict[str, Any]:
    spec = profile(profile_name)
    local_recovery = run_local_recovery_test(root)
    require(local_recovery.get("state") == "passed_zero_network" and local_recovery.get("network_calls") == 0, "B1E-FQ V2.1 local recovery regression failed")
    if profile_name == "full":
        _require_smoke_verified(root)
    preflight_root = root / spec["preflight_root"]
    staging = preflight_root.with_name(f".{preflight_root.name}.staging")
    require(not preflight_root.exists() and not staging.exists(), "Refusing to overwrite B1E-FQ V2 preflight")
    prompt_path, prompts = _selected_prompts(root, profile_name)

    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        raw_query = str(prompt["prompt"])
        require(sha256_text(raw_query) == str(prompt["prompt_sha256"]), f"B1E-FQ V2 prompt hash drift: {prompt['prompt_id']}")
        outbound = request_payload(raw_query)
        require(outbound["enable_thinking"] is PARSER_ENABLE_THINKING is False, "B1E-FQ V2 non-thinking mode drift")
        rows.append({
            "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-request-v1",
            "prompt_id": str(prompt["prompt_id"]),
            "prompt_sha256": str(prompt["prompt_sha256"]),
            "raw_query": raw_query,
            "raw_query_utf8_bytes": len(raw_query.encode("utf-8")),
            "provider_input_token_upper_bound": provider_input_token_upper_bound(raw_query),
            "request": outbound,
        })
    require(len(rows) == spec["expected_prompts"] and len({row["prompt_id"] for row in rows}) == len(rows), "B1E-FQ V2 request identity drift")
    require(not contains_forbidden_routing_metadata(rows), "B1E-FQ V2 request inventory leaks routing metadata")

    preflight_root.parent.mkdir(parents=True, exist_ok=True)
    staging.mkdir(parents=False, exist_ok=False)
    inventory_path = staging / INVENTORY_NAME
    final_inventory_path = preflight_root / INVENTORY_NAME
    write_jsonl_new(inventory_path, rows)
    input_cap = sum(row["provider_input_token_upper_bound"] for row in rows)
    output_cap = len(rows) * PARSER_MAX_OUTPUT_TOKENS
    price_cap = math.ceil((input_cap * PARSER_INPUT_USD_PER_MILLION_TOKENS + output_cap * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000 * 1_000_000) / 1_000_000
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
        "maximum_external_raw_query_utf8_bytes": sum(row["raw_query_utf8_bytes"] for row in rows),
    }
    payload = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-payload-v1",
        "state": "sealed_not_executed",
        "network_calls": 0,
        "profile": profile_name,
        "profile_spec": spec,
        "base_url": PARSER_BASE_URL,
        "model": PARSER_MODEL,
        "parser_contract": {
            "path": "skill_benchmark/scripts/rq2bv1_query_field_parser_v2.py",
            "sha256": sha256_file(root / "skill_benchmark/scripts/rq2bv1_query_field_parser_v2.py"),
            "contract_sha256": parser_contract_sha256(),
            "contract": parser_contract(),
        },
        "strict_population": {"source_strict_prompts": 381, "parser_requests": len(rows), "candidate_library_skills_visible_to_parser": 0},
        "local_recovery_regression": local_recovery,
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
        "fallback_policy": "record_fallback_per_unvalidated_parser_response_continue_batch_do_not_materialize_ranking_until_fq_e_provenance_gate",
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
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-execution-approval-packet-v1",
        "state": "awaiting_independent_review_then_explicit_parser_transfer_authorisation",
        "profile": profile_name,
        "payload": {"path": relative(final_payload_path, root), "sha256": sha256_file(payload_path)},
        "execution_scripts": scripts,
        "run_id": spec["run_id"],
        "output_dir": spec["result_root"],
        "cache_root": spec["cache_root"],
        "authorisation_consumption_root": "skill_benchmark/rq2bv1/approvals/consumed",
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
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-preflight-report-v1",
        "state": "preflight_passed_no_network_no_parser_execution_external_authorisation_required",
        "profile": profile_name,
        "payload": {"path": relative(final_payload_path, root), "sha256": sha256_file(payload_path)},
        "execution_packet": {"path": relative(final_packet_path, root), "sha256": sha256_file(packet_path)},
        "counts": counts,
        "validation": {"raw_prompt_hashes_validated": len(rows), "parser_request_rows_without_candidate_or_gold_metadata": len(rows), "local_recovery_regression": "passed_zero_network", "network_calls": 0},
        "next_gate": "independent_local_review_then_exact_parser_transfer_authorisation",
    }
    write_json_new(staging / REPORT_NAME, report)
    staging.rename(preflight_root)
    return report


def self_test() -> dict[str, Any]:
    payload = request_payload("Convert scanned invoices into JSON.")
    require(payload["response_format"] == {"type": "json_object"} and payload["enable_thinking"] is False, "B1E-FQ V2 preflight request drift")
    require(profile("smoke")["expected_prompts"] == 20 and profile("full")["expected_prompts"] == 381, "B1E-FQ V2 profile self-test drift")
    return {"schema_version": "rq2bv1-v3-b1e-fq-parser-v2-preflight-self-test-v1", "state": "passed_zero_network", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--profile", choices=tuple(profile_name for profile_name in ("smoke", "full")))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.self_test != bool(args.profile), "Choose exactly one of --self-test or --profile")
    result = self_test() if args.self_test else build(args.root.resolve(), str(args.profile))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
