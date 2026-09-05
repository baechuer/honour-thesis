#!/usr/bin/env python3
"""Run one explicitly authorised, checkpointed B1E-FQ V2 parser profile."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, sha256_text, write_json_new, write_jsonl_new
from rq2bv1_b1efq_v2_cost_ledger import empty_ledger, validate_ledger
from rq2bv1_fq_parser_v2_runtime import (
    AUTHORISATION_CONSUMPTION_ROOT,
    ExactQueryParseCacheV2,
    INVENTORY_NAME,
    PACKET_NAME,
    PARSER_INPUT_USD_PER_MILLION_TOKENS,
    PARSER_OUTPUT_USD_PER_MILLION_TOKENS,
    PAYLOAD_NAME,
    REVIEW_NAME,
    TIMEOUT_SECONDS,
    contains_forbidden_routing_metadata,
    parse_provider_response,
    post_chat_once,
    profile,
    provider_usage,
)
from rq2bv1_query_field_parser_v2 import PARSER_BASE_URL, PARSER_MODEL, parser_contract, parser_contract_sha256, request_payload


RUNNER_VERSION = "rq2bv1-v3-b1e-fq-parser-v2-runner-v1"
RESULT_SCHEMA = "rq2bv1-v3-b1e-fq-parser-v2-result-row-v1"
DEFAULT_AUTHORISATION = "skill_benchmark/rq2bv1/approvals/qwen_field_aligned_v3_parser_v2_1_smoke_execution_authorisation.json"


def _path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _packet(root: Path, profile_name: str) -> tuple[Path, dict[str, Any]]:
    spec = profile(profile_name)
    path = root / spec["preflight_root"] / PACKET_NAME
    packet = read_json(path)
    require(packet.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-execution-approval-packet-v1", "B1E-FQ V2 packet schema drift")
    require(packet.get("state") == "awaiting_independent_review_then_explicit_parser_transfer_authorisation", "B1E-FQ V2 packet state drift")
    require(packet.get("profile") == profile_name, "B1E-FQ V2 packet profile drift")
    return path, packet


def validate_preflight(root: Path, profile_name: str, packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    spec = profile(profile_name)
    preflight_root = root / spec["preflight_root"]
    payload_path = preflight_root / PAYLOAD_NAME
    payload = read_json(payload_path)
    require(payload.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-payload-v1" and payload.get("state") == "sealed_not_executed", "B1E-FQ V2 payload drift")
    require(payload.get("profile") == profile_name and payload.get("profile_spec") == spec, "B1E-FQ V2 payload profile drift")
    require(packet.get("payload") == {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)}, "B1E-FQ V2 packet payload binding drift")
    require(payload.get("base_url") == packet.get("base_url") == PARSER_BASE_URL, "B1E-FQ V2 endpoint drift")
    require(payload.get("model") == packet.get("model") == PARSER_MODEL, "B1E-FQ V2 model drift")
    require(payload.get("parser_contract") == {
        "path": "skill_benchmark/scripts/rq2bv1_query_field_parser_v2.py",
        "sha256": sha256_file(root / "skill_benchmark/scripts/rq2bv1_query_field_parser_v2.py"),
        "contract_sha256": parser_contract_sha256(),
        "contract": parser_contract(),
    }, "B1E-FQ V2 parser contract drift")
    inventory_path = root / payload["request_inventory"]["path"]
    rows = read_jsonl(inventory_path)
    require(payload.get("request_inventory") == {"path": relative(preflight_root / INVENTORY_NAME, root), "sha256": sha256_file(inventory_path), "rows": len(rows)}, "B1E-FQ V2 inventory binding drift")
    require(len(rows) == spec["expected_prompts"] and len({row["prompt_id"] for row in rows}) == len(rows), "B1E-FQ V2 inventory coverage drift")
    expected_keys = {"schema_version", "prompt_id", "prompt_sha256", "raw_query", "raw_query_utf8_bytes", "provider_input_token_upper_bound", "request"}
    for row in rows:
        require(set(row) == expected_keys and row["schema_version"] == "rq2bv1-v3-b1e-fq-parser-v2-request-v1", "B1E-FQ V2 inventory row schema drift")
        raw_query = row["raw_query"]
        require(isinstance(raw_query, str) and bool(raw_query), "B1E-FQ V2 raw query drift")
        require(row["prompt_sha256"] == sha256_text(raw_query), "B1E-FQ V2 raw query hash drift")
        require(row["raw_query_utf8_bytes"] == len(raw_query.encode("utf-8")), "B1E-FQ V2 raw query bytes drift")
        require(row["request"] == request_payload(raw_query), "B1E-FQ V2 outbound request reconstruction drift")
    require(not contains_forbidden_routing_metadata(rows), "B1E-FQ V2 outbound routing metadata leakage")
    return payload, rows


def _validate_authorisation(root: Path, path: Path, packet_path: Path, packet: dict[str, Any], profile_name: str) -> dict[str, Any]:
    authorisation = read_json(path)
    require(authorisation.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-execution-authorisation-v1", "B1E-FQ V2 authorisation schema drift")
    require(authorisation.get("state") == "explicitly_authorised_for_one_qwen_field_aligned_v2_parser_execution", "B1E-FQ V2 execution is not authorised")
    require(authorisation.get("profile") == profile_name, "B1E-FQ V2 authorisation profile drift")
    require(authorisation.get("approved_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "B1E-FQ V2 authorisation packet drift")
    review_path = root / profile(profile_name)["preflight_root"] / REVIEW_NAME
    require(authorisation.get("local_protocol_review") == {"path": relative(review_path, root), "sha256": sha256_file(review_path)}, "B1E-FQ V2 authorisation review drift")
    for key in ("run_id", "output_dir", "cache_root", "authorisation_consumption_root", "base_url", "model", "timeout_seconds", "automatic_retries"):
        require(authorisation.get(key) == packet.get(key), f"B1E-FQ V2 authorisation mismatch: {key}")
    for key, value in packet.items():
        if key.startswith("maximum_"):
            require(authorisation.get(key) == value, f"B1E-FQ V2 authorisation cap mismatch: {key}")
    require(authorisation.get("thesis_result_writing_authorised") is False, "B1E-FQ V2 cannot write thesis results")
    require(authorisation.get("execution_scripts") == packet.get("execution_scripts"), "B1E-FQ V2 script binding drift")
    for script in packet["execution_scripts"]:
        script_path = _path(root, script["path"])
        require(script_path.is_file() and sha256_file(script_path) == script["sha256"], f"B1E-FQ V2 script hash drift: {script['path']}")
    return authorisation


def _validate_review(root: Path, profile_name: str, packet_path: Path, packet: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    spec = profile(profile_name)
    preflight_root = root / spec["preflight_root"]
    review_path = preflight_root / REVIEW_NAME
    review = read_json(review_path)
    require(review.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-local-protocol-review-v1", "B1E-FQ V2 review schema drift")
    require(review.get("state") == "local_protocol_review_passed_no_network_no_external_text_sent" and review.get("profile") == profile_name, "B1E-FQ V2 review state drift")
    require(review.get("preflight") == {
        "payload": {"path": relative(preflight_root / PAYLOAD_NAME, root), "sha256": sha256_file(preflight_root / PAYLOAD_NAME)},
        "execution_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "inventory": {"path": relative(preflight_root / INVENTORY_NAME, root), "rows": spec["expected_prompts"], "sha256": sha256_file(preflight_root / INVENTORY_NAME)},
    }, "B1E-FQ V2 review preflight binding drift")
    require(review.get("checks", {}).get("network_calls") == 0 and review.get("checks", {}).get("candidate_library_skills_visible_to_parser") == 0, "B1E-FQ V2 review boundary drift")
    return review_path, review


def _consume_authorisation(root: Path, authorisation_path: Path, packet_path: Path, packet: dict[str, Any], profile_name: str) -> Path:
    consumption_root = root / AUTHORISATION_CONSUMPTION_ROOT
    authorisation_sha, packet_sha = sha256_file(authorisation_path), sha256_file(packet_path)
    receipt_path = consumption_root / f"b1e-fq-parser-v2-{profile_name}-{packet_sha}-{authorisation_sha}.json"
    require(not receipt_path.exists(), "B1E-FQ V2 authorisation was already consumed; a new exact authorisation is required")
    consumption_root.mkdir(parents=True, exist_ok=True)
    write_json_new(receipt_path, {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-authorisation-consumption-v1",
        "state": "consumed_before_first_provider_attempt",
        "profile": profile_name,
        "authorisation": {"path": relative(authorisation_path, root), "sha256": authorisation_sha},
        "execution_packet": {"path": relative(packet_path, root), "sha256": packet_sha},
        "network_calls_before_receipt": 0,
        "automatic_retries": 0,
        "thesis_result_writing": False,
    })
    return receipt_path


def _result_row(item: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "prompt_id": item["prompt_id"],
        "prompt_sha256": item["prompt_sha256"],
        "query_sha256": sha256_text(item["raw_query"]),
        "parser_status": entry["status"],
        "parsed": entry.get("parsed"),
        "failure_class": entry.get("failure_class"),
        "response_content_sha256": entry.get("response_content_sha256"),
        "cold_parser_seconds": float(entry["request_seconds"]),
        "provider_usage": entry["provider_usage"],
    }


def _record_reliability(ledger: dict[str, Any], entry: dict[str, Any]) -> None:
    reliability = ledger["reliability"]
    reliability["queries_total"] += 1
    if entry["status"] == "valid":
        reliability["parser_valid"] += 1
        reliability["active_field_count_total"] += len(entry["parsed"]["active_fields"])
        return
    reliability["fallback_queries"] += 1
    failure_class = entry["failure_class"]
    mapping = {
        "schema": "parser_schema_failures",
        "span_grounding": "parser_span_grounding_failures",
        "empty_fields": "parser_empty_field_failures",
        "invalid_json": "parser_invalid_json_failures",
        "provider_response_schema": "parser_provider_response_failures",
        "transport": "parser_transport_failures",
    }
    reliability[mapping[failure_class]] += 1


def run(root: Path, profile_name: str, authorisation_path: Path, api_key_env: str) -> dict[str, Any]:
    packet_path, packet = _packet(root, profile_name)
    payload, inventory = validate_preflight(root, profile_name, packet)
    review_path, review = _validate_review(root, profile_name, packet_path, packet)
    authorisation = _validate_authorisation(root, authorisation_path, packet_path, packet, profile_name)
    output_root = root / packet["output_dir"]
    staging = output_root.with_name(f".{output_root.name}.staging")
    require(not output_root.exists() and not staging.exists(), "Refusing to overwrite or resume B1E-FQ V2 parser scientific output")
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), "B1E-FQ V2 parser API key environment variable is missing")
    cache = ExactQueryParseCacheV2(root / packet["cache_root"], packet["run_id"])
    require(all(cache.load(str(item["raw_query"])) is None for item in inventory), "B1E-FQ V2 cache is not empty; clean run boundary would be violated")
    receipt_path = _consume_authorisation(root, authorisation_path, packet_path, packet, profile_name)

    staging.mkdir(parents=True, exist_ok=False)
    records_root = staging / "request_records"
    records_root.mkdir(parents=False, exist_ok=False)
    ledger, rows = empty_ledger(), []
    ledger["state"] = "parser_stage_running"
    stage = ledger["per_query"]["query_parsing"]
    record_paths: list[Path] = []

    for index, item in enumerate(inventory):
        raw_query = str(item["raw_query"])
        stage["request_attempts"] += 1
        stage["cache_misses"] += 1
        stage["external_text_submissions"] += 1
        stage["external_raw_query_utf8_bytes"] += int(item["raw_query_utf8_bytes"])
        stage["provider_input_token_upper_bound"] += int(item["provider_input_token_upper_bound"])
        attempt_path = records_root / f"request_{index:04d}_attempt.json"
        write_json_new(attempt_path, {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-attempt-v1",
            "state": "persisted_before_provider_call",
            "prompt_id": item["prompt_id"],
            "prompt_sha256": item["prompt_sha256"],
            "request": item["request"],
            "raw_query_utf8_bytes": item["raw_query_utf8_bytes"],
            "provider_input_token_upper_bound": item["provider_input_token_upper_bound"],
            "automatic_retries": 0,
        })
        record_paths.append(attempt_path)
        write_json_new(records_root / f"request_{index:04d}_ledger_before_call.json", ledger)
        record_paths.append(records_root / f"request_{index:04d}_ledger_before_call.json")
        started = time.monotonic()
        try:
            response = post_chat_once(api_key, item["request"], int(packet["timeout_seconds"]))
        except Exception as exc:  # One durable fallback; no automatic retry.
            seconds = time.monotonic() - started
            stage["attempt_failures"] += 1
            stage["wall_seconds"] += seconds
            entry = {
                "status": "fallback", "parsed": None, "failure_class": "transport",
                "response_content_sha256": None, "request_seconds": seconds,
                "provider_usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }
            error_path = records_root / f"request_{index:04d}_transport_fallback.json"
            write_json_new(error_path, {
                "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-transport-fallback-v1",
                "prompt_id": item["prompt_id"], "prompt_sha256": item["prompt_sha256"],
                "error_type": type(exc).__name__, "error_message": str(exc),
                "request_seconds": seconds, "possible_external_submission": True,
                "automatic_retries": 0,
            })
            record_paths.append(error_path)
        else:
            seconds = time.monotonic() - started
            stage["successful_api_calls"] += 1
            stage["wall_seconds"] += seconds
            try:
                usage = provider_usage(response)
                entry = parse_provider_response(raw_query, response)
            except ValueError:
                usage = {"prompt_tokens": 0, "completion_tokens": 0}
                entry = {"status": "fallback", "parsed": None, "failure_class": "provider_response_schema", "response_content_sha256": sha256_text(str(response))}
            entry["request_seconds"] = seconds
            entry["provider_usage"] = usage
            stage["provider_input_tokens"] += usage["prompt_tokens"]
            stage["provider_output_tokens"] += usage["completion_tokens"]
            response_path = records_root / f"request_{index:04d}_response.json"
            write_json_new(response_path, response)
            record_paths.append(response_path)
        _record_reliability(ledger, entry)
        cache_path = cache.store(raw_query, entry)
        commit_path = records_root / f"request_{index:04d}_cache_commit.json"
        write_json_new(commit_path, {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-cache-commit-v1",
            "prompt_id": item["prompt_id"], "query_sha256": sha256_text(raw_query),
            "cache_entry_sha256": sha256_file(cache_path), "parser_status": entry["status"],
            "failure_class": entry["failure_class"], "request_seconds": entry["request_seconds"],
            "provider_usage": entry["provider_usage"],
        })
        record_paths.append(commit_path)
        rows.append(_result_row(item, entry))
        validate_ledger(ledger)

    ledger["state"] = "parser_stage_completed_with_documented_fallbacks_pending_fq_e"
    validate_ledger(ledger)
    rows_path, ledger_path = staging / "parsed_queries.jsonl", staging / "parser_ledger.json"
    write_jsonl_new(rows_path, rows)
    write_json_new(ledger_path, ledger)
    records_manifest_path = staging / "request_records_manifest.json"
    write_json_new(records_manifest_path, {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-request-records-v1",
        "records": [{"path": relative(output_root / "request_records" / path.name, root), "sha256": sha256_file(path)} for path in record_paths],
    })
    actual_price = (stage["provider_input_tokens"] * PARSER_INPUT_USD_PER_MILLION_TOKENS + stage["provider_output_tokens"] * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
    manifest = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-run-manifest-v1",
        "state": "parser_stage_completed_with_documented_fallbacks_pending_fq_e",
        "profile": profile_name, "run_id": packet["run_id"], "runner_version": RUNNER_VERSION,
        "payload": {"path": relative(root / profile(profile_name)["preflight_root"] / PAYLOAD_NAME, root), "sha256": sha256_file(root / profile(profile_name)["preflight_root"] / PAYLOAD_NAME)},
        "execution_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "local_protocol_review": {"path": relative(review_path, root), "sha256": sha256_file(review_path)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
        "authorisation_consumption": {"path": relative(receipt_path, root), "sha256": sha256_file(receipt_path)},
        "parser_contract_sha256": parser_contract_sha256(),
        "artifacts": {
            "rows": {"path": relative(output_root / rows_path.name, root), "rows": len(rows), "sha256": sha256_file(rows_path)},
            "ledger": {"path": relative(output_root / ledger_path.name, root), "sha256": sha256_file(ledger_path)},
            "request_records": {"path": relative(output_root / records_manifest_path.name, root), "sha256": sha256_file(records_manifest_path), "records": len(record_paths)},
        },
        "network_calls_confirmed": stage["successful_api_calls"],
        "possible_external_submissions": stage["external_text_submissions"],
        "parser_standard_list_price_usd": actual_price,
        "fallback_ranking_materialized": False,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.rename(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    query = "Convert scanned invoices into page-anchored JSON."
    response = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps({"fields": {
        "use_condition": [], "input_precondition": ["scanned invoices"], "output_artifact": ["page-anchored JSON"],
        "workflow_procedure": [], "dependency_resource": [], "boundary_not_for": [], "success_verification": [],
    }})}}], "usage": {"prompt_tokens": 3, "completion_tokens": 4}}
    parsed = parse_provider_response(query, response)
    require(parsed["status"] == "valid" and parsed["parsed"]["active_fields"] == ["input_precondition", "output_artifact"], "B1E-FQ V2 runner self-test parse drift")
    truncated = parse_provider_response(query, {"choices": [{"finish_reason": "length", "message": {"content": "{}"}}], "usage": {"prompt_tokens": 3, "completion_tokens": 768}})
    require(truncated["status"] == "fallback" and truncated["failure_class"] == "provider_finish_reason_length", "B1E-FQ V2 runner self-test truncation drift")
    return {"schema_version": "rq2bv1-v3-b1e-fq-parser-v2-runner-self-test-v1", "state": "passed_zero_network", "network_calls": 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--profile", choices=("smoke", "full"))
    parser.add_argument("--authorisation", type=Path, default=Path(DEFAULT_AUTHORISATION))
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.execute and (args.self_test or args.profile is not None), "Choose --self-test or --execute with --profile")
    output = self_test() if args.self_test else run(args.root.resolve(), str(args.profile), _path(args.root.resolve(), args.authorisation), args.api_key_env)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
