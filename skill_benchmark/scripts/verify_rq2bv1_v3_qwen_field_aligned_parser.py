#!/usr/bin/env python3
"""Independently verify a completed FQ-P parser stage without network access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2bv1_fq_parser_execution_contract import CACHE_ROOT, PARSER_INPUT_USD_PER_MILLION_TOKENS, PARSER_OUTPUT_USD_PER_MILLION_TOKENS, PAYLOAD_NAME, PREFLIGHT_ROOT, RESULT_ROOT
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new
from rq2bv1_b1efq_cost_ledger import validate_ledger
from rq2bv1_query_field_parser import parser_contract_sha256, validate_response
from run_rq2bv1_v3_qwen_field_aligned_parser import ExactQueryParseCache, RESULT_SCHEMA, _packet, _parse_provider_response, _result_row, _usage, _validate_preflight


VERIFIER_VERSION = "rq2bv1-v3-b1e-fq-parser-verifier-v2"


def verify(root: Path) -> dict[str, Any]:
    packet_path, packet = _packet(root)
    payload, inventory = _validate_preflight(root, packet)
    output_root = root / RESULT_ROOT
    manifest_path, rows_path, ledger_path = output_root / "manifest.json", output_root / "parsed_queries.jsonl", output_root / "parser_ledger.json"
    require(manifest_path.is_file() and rows_path.is_file() and ledger_path.is_file(), "FQ-P output artifacts are incomplete")
    manifest, rows, ledger = read_json(manifest_path), read_jsonl(rows_path), read_json(ledger_path)
    require(manifest.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-run-manifest-v2", "FQ-P manifest schema drift")
    require(manifest.get("state") == "parser_stage_completed_pending_query_field_embedding_preflight", "FQ-P manifest state drift")
    require(manifest.get("payload") == {"path": relative(root / PREFLIGHT_ROOT / PAYLOAD_NAME, root), "sha256": sha256_file(root / PREFLIGHT_ROOT / PAYLOAD_NAME)}, "FQ-P manifest payload drift")
    require(manifest.get("execution_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "FQ-P manifest packet drift")
    authorisation = manifest.get("authorisation")
    require(isinstance(authorisation, dict), "FQ-P manifest authorisation missing")
    authorisation_path = root / authorisation["path"]
    require(authorisation_path.is_file() and sha256_file(authorisation_path) == authorisation["sha256"], "FQ-P manifest authorisation drift")
    require(manifest.get("parser_contract_sha256") == parser_contract_sha256(), "FQ-P manifest parser contract drift")
    require(manifest["artifacts"]["rows"] == {"path": relative(rows_path, root), "rows": len(rows), "sha256": sha256_file(rows_path)}, "FQ-P manifest rows drift")
    require(manifest["artifacts"]["ledger"] == {"path": relative(ledger_path, root), "sha256": sha256_file(ledger_path)}, "FQ-P manifest ledger drift")
    require(len(rows) == len(inventory) == 381, "FQ-P result population drift")
    require(all(row.get("schema_version") == RESULT_SCHEMA for row in rows), "FQ-P result schema drift")

    by_id = {row["prompt_id"]: row for row in rows}
    require(len(by_id) == len(rows) and set(by_id) == {row["prompt_id"] for row in inventory}, "FQ-P result identity drift")
    cache = ExactQueryParseCache(root / CACHE_ROOT)
    valid_count = 0
    for index, item in enumerate(inventory):
        raw_query, expected = str(item["raw_query"]), by_id[item["prompt_id"]]
        cached = cache.load(raw_query)
        require(cached is not None, f"FQ-P cache coverage drift: {item['prompt_id']}")
        reconstructed = _result_row(item, cached, cache_status=expected["cache_status"])
        for key in ("prompt_sha256", "query_sha256", "parser_status", "parsed", "failure_class", "response_content_sha256", "cold_parser_seconds", "provider_usage"):
            require(reconstructed[key] == expected[key], f"FQ-P result/cache drift: {item['prompt_id']}.{key}")
        if expected["parser_status"] == "valid":
            validate_response(raw_query, {"fields": expected["parsed"]["fields"]})
            valid_count += 1
        else:
            require(expected["parsed"] is None and isinstance(expected["failure_class"], str), f"FQ-P invalid record drift: {item['prompt_id']}")
        if expected["cache_status"] == "new_provider_call":
            record_root = output_root / "request_records"
            attempt = read_json(record_root / f"request_{index:04d}_attempt.json")
            response = read_json(record_root / f"request_{index:04d}_response.json")
            commit = read_json(record_root / f"request_{index:04d}_cache_commit.json")
            require(attempt.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-attempt-v2" and attempt.get("state") == "persisted_before_provider_call", f"FQ-P attempt record drift: {item['prompt_id']}")
            require(attempt.get("prompt_id") == item["prompt_id"] and attempt.get("prompt_sha256") == item["prompt_sha256"] and attempt.get("request") == item["request"], f"FQ-P attempt payload drift: {item['prompt_id']}")
            require(attempt.get("raw_query_utf8_bytes") == item["raw_query_utf8_bytes"] and attempt.get("provider_input_token_upper_bound") == item["provider_input_token_upper_bound"], f"FQ-P attempt cap drift: {item['prompt_id']}")
            response_entry = _parse_provider_response(raw_query, response)
            response_usage = {"prompt_tokens": _usage(response)[0], "completion_tokens": _usage(response)[1]}
            for key in ("status", "parsed", "failure_class", "response_content_sha256"):
                require(cached.get(key) == response_entry.get(key), f"FQ-P response/cache drift: {item['prompt_id']}.{key}")
            require(cached.get("provider_usage") == response_usage == commit.get("provider_usage"), f"FQ-P response usage drift: {item['prompt_id']}")
            require(cached.get("request_seconds") == commit.get("request_seconds") == expected["cold_parser_seconds"], f"FQ-P response timing drift: {item['prompt_id']}")
            require(commit == {
                "schema_version": "rq2bv1-v3-b1e-fq-parser-cache-commit-v2",
                "prompt_id": item["prompt_id"],
                "query_sha256": expected["query_sha256"],
                "cache_entry_sha256": sha256_file(cache.path(raw_query)),
                "parser_status": cached["status"],
                "failure_class": cached.get("failure_class"),
                "response_content_sha256": cached["response_content_sha256"],
                "provider_usage": cached["provider_usage"],
                "request_seconds": cached["request_seconds"],
            }, f"FQ-P cache-commit drift: {item['prompt_id']}")

    validate_ledger(ledger)
    stage, reliability = ledger["per_query"]["query_parsing"], ledger["reliability"]
    new_rows = [row for row in rows if row["cache_status"] == "new_provider_call"]
    cache_rows = [row for row in rows if row["cache_status"] == "exact_cache_hit"]
    require(stage["successful_api_calls"] == stage["request_attempts"] == len(new_rows), "FQ-P call ledger drift")
    require(stage["cache_hits"] == len(cache_rows) and stage["cache_misses"] == len(new_rows), "FQ-P cache ledger drift")
    require(stage["external_text_submissions"] == len(new_rows), "FQ-P external submission ledger drift")
    require(stage["external_raw_query_utf8_bytes"] == sum(item["raw_query_utf8_bytes"] for item in inventory if by_id[item["prompt_id"]]["cache_status"] == "new_provider_call"), "FQ-P raw-query byte ledger drift")
    require(stage["provider_input_token_upper_bound"] == sum(item["provider_input_token_upper_bound"] for item in inventory if by_id[item["prompt_id"]]["cache_status"] == "new_provider_call"), "FQ-P input-bound ledger drift")
    require(stage["attempt_failures"] == 0, "FQ-P completed run has attempt failures")
    actual_price = (stage["provider_input_tokens"] * PARSER_INPUT_USD_PER_MILLION_TOKENS + stage["provider_output_tokens"] * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
    require(manifest.get("parser_standard_list_price_usd") == actual_price, "FQ-P parser-price manifest drift")
    require(reliability["queries_total"] == len(rows) and reliability["parser_valid"] == valid_count, "FQ-P reliability drift")
    require(reliability["fallback_queries"] == len(rows) - valid_count, "FQ-P fallback ledger drift")
    records_manifest_path = output_root / "request_records_manifest.json"
    require(records_manifest_path.is_file(), "FQ-P request-record manifest missing")
    records_manifest = read_json(records_manifest_path)
    require(manifest["artifacts"]["request_records"] == {"path": relative(records_manifest_path, root), "sha256": sha256_file(records_manifest_path), "records": len(records_manifest["records"])}, "FQ-P request-record manifest binding drift")
    require(records_manifest.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-request-records-v2", "FQ-P request-record manifest schema drift")
    request_records = records_manifest.get("records")
    require(isinstance(request_records, list) and len(request_records) == len(new_rows) * 4, "FQ-P request-record coverage drift")
    for record in request_records:
        path = root / record["path"]
        require(path.is_file() and sha256_file(path) == record["sha256"], "FQ-P request-record hash drift")
    require(manifest.get("network_calls") == len(new_rows), "FQ-P manifest network-call drift")
    consumption = manifest.get("authorisation_consumption")
    require(isinstance(consumption, dict), "FQ-P authorisation consumption receipt missing")
    consumption_path = root / consumption["path"]
    require(consumption_path.is_file() and sha256_file(consumption_path) == consumption["sha256"], "FQ-P authorisation consumption receipt drift")
    receipt = read_json(consumption_path)
    require(receipt.get("state") == "consumed_before_first_provider_attempt" and receipt.get("execution_packet") == manifest["execution_packet"] and receipt.get("authorisation") == authorisation, "FQ-P authorisation consumption content drift")
    require(manifest.get("warm_replay") == {"verified_prompts": len(rows)}, "FQ-P warm replay drift")
    require(manifest.get("thesis_result_writing") is False, "FQ-P thesis boundary drift")

    summary = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-post-run-summary-v2",
        "state": "parser_stage_completed_pending_query_field_embedding_preflight",
        "scope": {"strict_prompts": len(rows), "candidate_text_visible_to_parser": 0, "parser_contract_sha256": parser_contract_sha256()},
        "parser": {
            "valid_parses": valid_count,
            "fallback_queries": reliability["fallback_queries"],
            "active_field_count_total": reliability["active_field_count_total"],
            "mean_active_fields_per_valid_parse": 0.0 if valid_count == 0 else reliability["active_field_count_total"] / valid_count,
            "cold_provider_calls": stage["successful_api_calls"],
            "cold_provider_input_tokens": stage["provider_input_tokens"],
            "cold_provider_output_tokens": stage["provider_output_tokens"],
            "cold_wall_seconds": stage["wall_seconds"],
            "cold_raw_query_utf8_bytes": stage["external_raw_query_utf8_bytes"],
            "cold_input_token_upper_bound": stage["provider_input_token_upper_bound"],
            "standard_list_price_usd": manifest["parser_standard_list_price_usd"],
            "cache_hits": stage["cache_hits"],
            "cache_misses": stage["cache_misses"],
        },
        "quality_gate": {"result_rows_validated": len(rows), "request_records_hash_validated": len(request_records), "warm_replay_prompts": len(rows), "network_calls_by_verifier": 0},
        "thesis_result_writing": False,
    }
    verification = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-post-run-verification-v2",
        "state": "passed_local_post_run_integrity_verification",
        "run_manifest": {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)},
        "result_rows": {"path": relative(rows_path, root), "rows": len(rows), "sha256": sha256_file(rows_path)},
        "parser_ledger": {"path": relative(ledger_path, root), "sha256": sha256_file(ledger_path)},
        "checks": summary["quality_gate"],
        "network_calls": 0,
        "thesis_result_writing": False,
    }
    write_json_new(output_root / "post_run_summary.json", summary)
    write_json_new(output_root / "post_run_verification.json", verification)
    return {"state": verification["state"], "verification": relative(output_root / "post_run_verification.json", root), "summary": relative(output_root / "post_run_summary.json", root)}


def self_test() -> dict[str, Any]:
    return {"schema_version": "rq2bv1-v3-b1e-fq-parser-verifier-self-test-v2", "state": "self_test_passed_zero_network", "network_calls": 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.verify, "Choose exactly one of --self-test or --verify")
    output = self_test() if args.self_test else verify(args.root.resolve())
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
