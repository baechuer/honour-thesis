#!/usr/bin/env python3
"""Verify a completed B1E-FQ V2 parser profile without network access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, sha256_text, write_json_new
from rq2bv1_b1efq_v2_cost_ledger import validate_ledger
from rq2bv1_fq_parser_v2_runtime import ExactQueryParseCacheV2, PACKET_NAME, PARSER_INPUT_USD_PER_MILLION_TOKENS, PARSER_OUTPUT_USD_PER_MILLION_TOKENS, profile
from rq2bv1_query_field_parser_v2 import FIELD_ORDER, parser_contract_sha256, validate_response
from run_rq2bv1_v3_qwen_field_aligned_parser_v2 import RESULT_SCHEMA, _packet, _result_row, _validate_authorisation, _validate_review, validate_preflight


VERIFIER_VERSION = "rq2bv1-v3-b1e-fq-parser-v2-verifier-v1"


def verify(root: Path, profile_name: str) -> dict[str, Any]:
    spec = profile(profile_name)
    packet_path, packet = _packet(root, profile_name)
    payload, inventory = validate_preflight(root, profile_name, packet)
    review_path, review = _validate_review(root, profile_name, packet_path, packet)
    output_root = root / spec["result_root"]
    manifest_path, rows_path, ledger_path = output_root / "manifest.json", output_root / "parsed_queries.jsonl", output_root / "parser_ledger.json"
    receipt_path = output_root / "independent_verification.json"
    require(manifest_path.is_file() and rows_path.is_file() and ledger_path.is_file(), "B1E-FQ V2 output artifacts are incomplete")
    require(not receipt_path.exists(), "Refusing to overwrite B1E-FQ V2 verification receipt")
    manifest, rows, ledger = read_json(manifest_path), read_jsonl(rows_path), read_json(ledger_path)
    require(manifest.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-run-manifest-v1", "B1E-FQ V2 manifest schema drift")
    require(manifest.get("state") == "parser_stage_completed_with_documented_fallbacks_pending_fq_e" and manifest.get("profile") == profile_name, "B1E-FQ V2 manifest state drift")
    require(manifest.get("fallback_ranking_materialized") is False and manifest.get("thesis_result_writing") is False, "B1E-FQ V2 method boundary drift")
    require(manifest.get("parser_contract_sha256") == parser_contract_sha256(), "B1E-FQ V2 parser contract drift")
    require(manifest.get("payload") == {"path": relative(root / spec["preflight_root"] / "payload_manifest.json", root), "sha256": sha256_file(root / spec["preflight_root"] / "payload_manifest.json")}, "B1E-FQ V2 manifest payload drift")
    require(manifest.get("execution_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "B1E-FQ V2 manifest packet drift")
    require(manifest.get("local_protocol_review") == {"path": relative(review_path, root), "sha256": sha256_file(review_path)}, "B1E-FQ V2 manifest review drift")
    for script in packet["execution_scripts"]:
        path = root / script["path"]
        require(path.is_file() and sha256_file(path) == script["sha256"], f"B1E-FQ V2 verifier script hash drift: {script['path']}")
    authorisation = manifest.get("authorisation")
    require(isinstance(authorisation, dict), "B1E-FQ V2 manifest authorisation missing")
    authorisation_path = root / authorisation.get("path", "")
    require(authorisation_path.is_file() and sha256_file(authorisation_path) == authorisation.get("sha256"), "B1E-FQ V2 manifest authorisation binding drift")
    authorisation_value = read_json(authorisation_path)
    require(_validate_authorisation(root, authorisation_path, packet_path, packet, profile_name) == authorisation_value, "B1E-FQ V2 authorisation validation drift")
    require(authorisation_value.get("approved_packet") == manifest["execution_packet"] and authorisation_value.get("local_protocol_review") == manifest["local_protocol_review"], "B1E-FQ V2 authorisation receipt drift")
    consumption = manifest.get("authorisation_consumption")
    require(isinstance(consumption, dict), "B1E-FQ V2 authorisation-consumption missing")
    consumption_path = root / consumption.get("path", "")
    require(consumption_path.is_file() and sha256_file(consumption_path) == consumption.get("sha256"), "B1E-FQ V2 authorisation-consumption binding drift")
    consumption_value = read_json(consumption_path)
    require(consumption_value.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-authorisation-consumption-v1", "B1E-FQ V2 authorisation-consumption schema drift")
    require(consumption_value.get("state") == "consumed_before_first_provider_attempt" and consumption_value.get("profile") == profile_name, "B1E-FQ V2 authorisation-consumption state drift")
    require(consumption_value.get("authorisation") == manifest["authorisation"] and consumption_value.get("execution_packet") == manifest["execution_packet"], "B1E-FQ V2 authorisation-consumption receipt drift")
    require(consumption_value.get("network_calls_before_receipt") == 0 and consumption_value.get("automatic_retries") == 0 and consumption_value.get("thesis_result_writing") is False, "B1E-FQ V2 authorisation-consumption boundary drift")
    require(len(rows) == len(inventory) == spec["expected_prompts"] and all(row.get("schema_version") == RESULT_SCHEMA for row in rows), "B1E-FQ V2 output coverage drift")
    by_id = {row["prompt_id"]: row for row in rows}
    require(len(by_id) == len(rows) and set(by_id) == {row["prompt_id"] for row in inventory}, "B1E-FQ V2 output identity drift")
    cache = ExactQueryParseCacheV2(root / spec["cache_root"], spec["run_id"])
    valid_count, transport_count = 0, 0
    for index, item in enumerate(inventory):
        row = by_id[item["prompt_id"]]
        cached = cache.load(item["raw_query"])
        require(cached is not None, f"B1E-FQ V2 cache missing: {item['prompt_id']}")
        expected = _result_row(item, cached)
        for key in expected:
            require(row.get(key) == expected[key], f"B1E-FQ V2 result/cache drift: {item['prompt_id']}.{key}")
        attempt_path = output_root / "request_records" / f"request_{index:04d}_attempt.json"
        commit_path = output_root / "request_records" / f"request_{index:04d}_cache_commit.json"
        require(attempt_path.is_file() and commit_path.is_file(), f"B1E-FQ V2 request records missing: {item['prompt_id']}")
        attempt, commit = read_json(attempt_path), read_json(commit_path)
        require(attempt.get("state") == "persisted_before_provider_call" and attempt.get("request") == item["request"], f"B1E-FQ V2 attempt record drift: {item['prompt_id']}")
        require(commit.get("cache_entry_sha256") == sha256_file(cache.path(item["raw_query"])) and commit.get("parser_status") == row["parser_status"], f"B1E-FQ V2 cache commit drift: {item['prompt_id']}")
        if row["parser_status"] == "valid":
            cached_texts = {
                field: [str(span["text"]) for span in row["parsed"]["fields"][field]]
                for field in FIELD_ORDER
            }
            validate_response(item["raw_query"], {"fields": cached_texts})
            valid_count += 1
        else:
            require(row["parsed"] is None and isinstance(row["failure_class"], str), f"B1E-FQ V2 fallback row drift: {item['prompt_id']}")
            if row["failure_class"] == "transport":
                transport_count += 1
                require((output_root / "request_records" / f"request_{index:04d}_transport_fallback.json").is_file(), f"B1E-FQ V2 transport evidence missing: {item['prompt_id']}")
            else:
                require((output_root / "request_records" / f"request_{index:04d}_response.json").is_file(), f"B1E-FQ V2 response evidence missing: {item['prompt_id']}")
    validate_ledger(ledger)
    stage, reliability = ledger["per_query"]["query_parsing"], ledger["reliability"]
    require(stage["request_attempts"] == stage["cache_misses"] == stage["external_text_submissions"] == len(rows), "B1E-FQ V2 request ledger drift")
    require(stage["cache_hits"] == 0 and stage["automatic_retries"] == 0, "B1E-FQ V2 cache/retry ledger drift")
    require(stage["successful_api_calls"] == len(rows) - transport_count and stage["attempt_failures"] == transport_count, "B1E-FQ V2 transport ledger drift")
    require(reliability["queries_total"] == len(rows) and reliability["parser_valid"] == valid_count and reliability["fallback_queries"] == len(rows) - valid_count, "B1E-FQ V2 reliability counts drift")
    actual_price = (stage["provider_input_tokens"] * PARSER_INPUT_USD_PER_MILLION_TOKENS + stage["provider_output_tokens"] * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
    require(manifest.get("parser_standard_list_price_usd") == actual_price, "B1E-FQ V2 parser-price drift")
    records_manifest_path = output_root / "request_records_manifest.json"
    records_manifest = read_json(records_manifest_path)
    require(len(records_manifest.get("records", [])) == len(rows) * 4, "B1E-FQ V2 request-record count drift")
    for record in records_manifest["records"]:
        path = root / record["path"]
        require(path.is_file() and sha256_file(path) == record["sha256"], "B1E-FQ V2 request-record hash drift")
    receipt = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-verification-receipt-v1",
        "state": "verified_complete_with_documented_fallbacks",
        "profile": profile_name,
        "verifier_version": VERIFIER_VERSION,
        "network_calls": 0,
        "result_manifest": {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)},
        "checks": {
            "rows": len(rows), "valid_parser_rows": valid_count, "fallback_rows": len(rows) - valid_count,
            "transport_fallback_rows": transport_count, "candidate_or_gold_text_sent": 0,
            "query_embedding_or_selection_executed": False, "fallback_ranking_materialized": False,
        },
        "next_gate": "smoke_only_complete" if profile_name == "smoke" else "fq_e_provenance_and_embedding_preflight",
    }
    write_json_new(receipt_path, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--profile", choices=("smoke", "full"), required=True)
    args = parser.parse_args()
    value = verify(args.root.resolve(), str(args.profile))
    print(json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
