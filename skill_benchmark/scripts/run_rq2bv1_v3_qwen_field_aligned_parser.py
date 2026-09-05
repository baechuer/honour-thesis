#!/usr/bin/env python3
"""Run one separately authorised FQ-P span-grounded Qwen parser stage."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

from rq2bv1_fq_parser_execution_contract import (
    AUTHORISATION_CONSUMPTION_ROOT,
    CACHE_ROOT,
    INVENTORY_NAME,
    PACKET_NAME,
    PARSER_INPUT_USD_PER_MILLION_TOKENS,
    PARSER_OUTPUT_USD_PER_MILLION_TOKENS,
    PAYLOAD_NAME,
    PREFLIGHT_ROOT,
    RESULT_ROOT,
    RUN_ID,
    TIMEOUT_SECONDS,
    provider_input_token_upper_bound,
)
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, sha256_json, sha256_text, write_json_new, write_jsonl_new
from rq2bv1_b1efq_cost_ledger import empty_ledger, validate_ledger
from rq2bv1_query_field_parser import PARSER_BASE_URL, PARSER_MODEL, parser_contract, parser_contract_sha256, request_payload, validate_response


RUNNER_VERSION = "rq2bv1-v3-b1e-fq-parser-runner-v2"
RESULT_SCHEMA = "rq2bv1-v3-b1e-fq-parser-result-row-v2"
DEFAULT_AUTHORISATION = "skill_benchmark/rq2bv1/approvals/qwen_field_aligned_v3_parser_execution_authorisation.json"
FORBIDDEN_ROUTING_METADATA = {"gold_skill", "candidate", "target_field", "skill_id", "cluster_id", "outcome", "rank", "label"}
INVALID_FAILURE_CLASSES = {"invalid_json", "schema", "span_grounding", "empty_fields", "provider_response_schema"}


def _path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in "0123456789abcdef" for character in value)


class ExactQueryParseCache:
    def __init__(self, root: Path) -> None:
        self.root = root / "qwen" / PARSER_MODEL / parser_contract_sha256()
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, raw_query: str) -> Path:
        key = sha256_json({"base_url": PARSER_BASE_URL, "model": PARSER_MODEL, "parser_contract_sha256": parser_contract_sha256(), "query_sha256": sha256_text(raw_query)})
        return self.root / f"{key}.json"

    def load(self, raw_query: str) -> dict[str, Any] | None:
        path = self.path(raw_query)
        if not path.exists():
            return None
        value = read_json(path)
        require(value.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-cache-v1", "FQ-P cache schema drift")
        require(value.get("base_url") == PARSER_BASE_URL and value.get("model") == PARSER_MODEL, "FQ-P parser cache provider drift")
        require(value.get("parser_contract_sha256") == parser_contract_sha256(), "FQ-P parser cache contract drift")
        require(value.get("query_sha256") == sha256_text(raw_query), "FQ-P parser cache query drift")
        require(value.get("status") in {"valid", "invalid"}, "FQ-P parser cache status drift")
        if value["status"] == "valid":
            validated = validate_response(raw_query, {"fields": value["parsed"]["fields"]})
            require(value["parsed"] == validated.as_dict(), "FQ-P validated cache content drift")
            require(value.get("failure_class") is None, "FQ-P valid cache failure-class drift")
        else:
            require(value.get("parsed") is None, "FQ-P invalid cache parsed-content drift")
            require(value.get("failure_class") in INVALID_FAILURE_CLASSES, "FQ-P invalid cache failure-class drift")
        require(_is_sha256(value.get("response_content_sha256")), "FQ-P cache response hash drift")
        require(isinstance(value.get("request_seconds"), (int, float)) and float(value["request_seconds"]) >= 0.0, "FQ-P cache request-time drift")
        usage = value.get("provider_usage")
        require(isinstance(usage, dict) and set(usage) == {"prompt_tokens", "completion_tokens"}, "FQ-P cache usage schema drift")
        require(all(type(token_count) is int and token_count >= 0 for token_count in usage.values()), "FQ-P cache usage value drift")
        return value

    def store(self, raw_query: str, entry: dict[str, Any]) -> None:
        path = self.path(raw_query)
        require(not path.exists(), "Refusing to overwrite FQ-P parser cache")
        payload = {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-cache-v1",
            "base_url": PARSER_BASE_URL,
            "model": PARSER_MODEL,
            "parser_contract_sha256": parser_contract_sha256(),
            "query_sha256": sha256_text(raw_query),
            **entry,
        }
        write_json_new(path, payload)


def _packet(root: Path) -> tuple[Path, dict[str, Any]]:
    path = root / PREFLIGHT_ROOT / PACKET_NAME
    packet = read_json(path)
    require(packet.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-execution-approval-packet-v1", "FQ-P packet schema drift")
    require(packet.get("state") == "awaiting_independent_review_then_explicit_parser_transfer_authorisation", "FQ-P packet state drift")
    return path, packet


def _contains_forbidden_routing_metadata(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(FORBIDDEN_ROUTING_METADATA & set(value)) or any(_contains_forbidden_routing_metadata(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_routing_metadata(child) for child in value)
    return False


def _validate_preflight(root: Path, packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    preflight_root = root / PREFLIGHT_ROOT
    payload_path = preflight_root / PAYLOAD_NAME
    payload = read_json(payload_path)
    require(payload.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-payload-v1" and payload.get("state") == "sealed_not_executed", "FQ-P payload drift")
    require(packet.get("payload") == {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)}, "FQ-P packet payload binding drift")
    require(payload.get("run_id") == packet.get("run_id") == RUN_ID, "FQ-P run identifier drift")
    require(payload.get("base_url") == packet.get("base_url") == PARSER_BASE_URL, "FQ-P endpoint drift")
    require(payload.get("model") == packet.get("model") == PARSER_MODEL, "FQ-P model drift")
    require(payload.get("parser_contract") == {
        "path": "skill_benchmark/scripts/rq2bv1_query_field_parser.py",
        "sha256": sha256_file(root / "skill_benchmark/scripts/rq2bv1_query_field_parser.py"),
        "contract_sha256": parser_contract_sha256(),
        "contract": parser_contract(),
    }, "FQ-P parser contract payload drift")
    require(payload.get("strict_population") == {"strict_prompts": 381, "candidate_library_skills_visible_to_parser": 0}, "FQ-P strict population drift")
    inventory_path = root / payload["request_inventory"]["path"]
    require(sha256_file(inventory_path) == payload["request_inventory"]["sha256"], "FQ-P request inventory drift")
    rows = read_jsonl(inventory_path)
    require(len(rows) == 381 and len({row["prompt_id"] for row in rows}) == 381, "FQ-P inventory coverage drift")
    require(payload.get("request_inventory") == {"path": relative(preflight_root / INVENTORY_NAME, root), "sha256": sha256_file(inventory_path), "rows": len(rows)}, "FQ-P inventory manifest drift")
    expected_keys = {"schema_version", "prompt_id", "prompt_sha256", "raw_query", "raw_query_utf8_bytes", "provider_input_token_upper_bound", "request"}
    for row in rows:
        require(set(row) == expected_keys and row["schema_version"] == "rq2bv1-v3-b1e-fq-parser-request-v1", "FQ-P inventory schema drift")
        raw_query = row["raw_query"]
        require(isinstance(raw_query, str) and bool(raw_query), "FQ-P raw query drift")
        require(row["prompt_sha256"] == sha256_text(raw_query), "FQ-P prompt hash drift")
        require(row["raw_query_utf8_bytes"] == len(raw_query.encode("utf-8")), "FQ-P raw-query byte drift")
        require(row["provider_input_token_upper_bound"] == provider_input_token_upper_bound(raw_query), "FQ-P parser input-bound drift")
        require(row["request"] == request_payload(raw_query), "FQ-P outbound request reconstruction drift")
    require(not _contains_forbidden_routing_metadata(rows), "FQ-P inventory routing-metadata leakage")
    require(payload.get("counts", {}).get("maximum_external_raw_query_utf8_bytes") == sum(row["raw_query_utf8_bytes"] for row in rows), "FQ-P raw-query byte cap drift")
    return payload, rows


def _validate_authorisation(root: Path, path: Path, packet_path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    authorisation = read_json(path)
    require(authorisation.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-execution-authorisation-v1", "FQ-P authorisation schema drift")
    require(authorisation.get("state") == "explicitly_authorised_for_one_qwen_field_aligned_parser_execution", "FQ-P execution is not authorised")
    require(authorisation.get("approved_packet") == {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)}, "FQ-P packet/authorisation drift")
    for key in ("run_id", "output_dir", "cache_root", "authorisation_consumption_root", "base_url", "model", "timeout_seconds", "automatic_retries"):
        require(authorisation.get(key) == packet.get(key), f"FQ-P authorisation mismatch: {key}")
    for key, value in packet.items():
        if key.startswith("maximum_"):
            require(authorisation.get(key) == value, f"FQ-P authorisation cap mismatch: {key}")
    require(authorisation.get("thesis_result_writing_authorised") is False, "FQ-P cannot write thesis results")
    require(authorisation.get("execution_scripts") == packet.get("execution_scripts"), "FQ-P script binding drift")
    for script in packet["execution_scripts"]:
        script_path = _path(root, script["path"])
        require(script_path.is_file() and sha256_file(script_path) == script["sha256"], f"FQ-P script hash drift: {script['path']}")
    return authorisation


def _consume_authorisation(root: Path, authorisation_path: Path, packet_path: Path, packet: dict[str, Any]) -> Path:
    consumption_root = root / str(packet["authorisation_consumption_root"])
    authorisation_sha, packet_sha = sha256_file(authorisation_path), sha256_file(packet_path)
    receipt_path = consumption_root / f"b1e-fq-parser-{packet_sha}-{authorisation_sha}.json"
    require(not receipt_path.exists(), "FQ-P authorisation was already consumed; a new exact authorisation is required")
    consumption_root.mkdir(parents=True, exist_ok=True)
    write_json_new(receipt_path, {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-authorisation-consumption-v1",
        "state": "consumed_before_first_provider_attempt",
        "authorisation": {"path": relative(authorisation_path, root), "sha256": authorisation_sha},
        "execution_packet": {"path": relative(packet_path, root), "sha256": packet_sha},
        "network_calls_before_receipt": 0,
        "automatic_retries": 0,
        "thesis_result_writing": False,
    })
    return receipt_path


def _post_chat_once(api_key: str, request_payload: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{PARSER_BASE_URL}/chat/completions",
        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        value = json.loads(response.read().decode("utf-8"))
    require(isinstance(value, dict), "FQ-P provider response is not an object")
    return value


def _parse_provider_response(raw_query: str, response: dict[str, Any]) -> dict[str, Any]:
    try:
        content = response["choices"][0]["message"]["content"]
        require(isinstance(content, str), "FQ-P provider content is not text")
        candidate = json.loads(content)
        parsed = validate_response(raw_query, candidate)
        return {"status": "valid", "parsed": parsed.as_dict(), "response_content_sha256": sha256_text(content)}
    except json.JSONDecodeError:
        return {"status": "invalid", "failure_class": "invalid_json", "response_content_sha256": sha256_text(str(response))}
    except ValueError as exc:
        message = str(exc).lower()
        failure_class = "empty_fields" if "no active fields" in message else "span_grounding" if "span" in message or "overlap" in message else "schema"
        return {"status": "invalid", "failure_class": failure_class, "response_content_sha256": sha256_text(str(response))}
    except (KeyError, IndexError, TypeError):
        return {"status": "invalid", "failure_class": "provider_response_schema", "response_content_sha256": sha256_text(str(response))}


def _usage(response: dict[str, Any]) -> tuple[int, int]:
    usage = response.get("usage")
    require(isinstance(usage, dict), "FQ-P provider response lacks usage")
    prompt_tokens, completion_tokens = usage.get("prompt_tokens"), usage.get("completion_tokens")
    require(type(prompt_tokens) is int and type(completion_tokens) is int and prompt_tokens >= 0 and completion_tokens >= 0, "FQ-P provider usage drift")
    return prompt_tokens, completion_tokens


def _result_row(inventory: dict[str, Any], entry: dict[str, Any], *, cache_status: str) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "prompt_id": inventory["prompt_id"],
        "prompt_sha256": inventory["prompt_sha256"],
        "query_sha256": sha256_text(str(inventory["raw_query"])),
        "cache_status": cache_status,
        "parser_status": entry["status"],
        "parsed": entry.get("parsed"),
        "failure_class": entry.get("failure_class"),
        "response_content_sha256": entry["response_content_sha256"],
        "cold_parser_seconds": float(entry.get("request_seconds", 0.0)),
        "provider_usage": entry.get("provider_usage", {"prompt_tokens": 0, "completion_tokens": 0}),
    }


def _warm_replay(rows: list[dict[str, Any]], inventory: list[dict[str, Any]], cache: ExactQueryParseCache) -> dict[str, Any]:
    expected = {row["prompt_id"]: row for row in rows}
    require(set(expected) == {row["prompt_id"] for row in inventory}, "FQ-P warm replay coverage drift")
    for row in inventory:
        cached = cache.load(str(row["raw_query"]))
        require(cached is not None, f"FQ-P warm cache missing: {row['prompt_id']}")
        actual = _result_row(row, cached, cache_status="warm_replay")
        prior = expected[row["prompt_id"]]
        for key in ("parser_status", "parsed", "failure_class", "query_sha256"):
            require(actual[key] == prior[key], f"FQ-P warm replay drift: {row['prompt_id']}.{key}")
    return {"verified_prompts": len(rows)}


def run(root: Path, authorisation_path: Path, api_key_env: str) -> dict[str, Any]:
    packet_path, packet = _packet(root)
    payload, inventory = _validate_preflight(root, packet)
    authorisation = _validate_authorisation(root, authorisation_path, packet_path, packet)
    output_root = root / str(packet["output_dir"])
    staging = output_root.with_name(f".{output_root.name}.staging")
    require(not output_root.exists() and not staging.exists(), "Refusing to overwrite or resume FQ-P parser scientific output")
    api_key = os.environ.get(api_key_env)
    require(bool(api_key), "FQ-P parser API key environment variable is missing")
    cache = ExactQueryParseCache(root / str(packet["cache_root"]))
    consumption_receipt = _consume_authorisation(root, authorisation_path, packet_path, packet)

    staging.mkdir(parents=True, exist_ok=False)
    records_root = staging / "request_records"
    records_root.mkdir(parents=False, exist_ok=False)
    ledger = empty_ledger()
    ledger["state"] = "parser_stage_running"
    stage = ledger["per_query"]["query_parsing"]
    rows: list[dict[str, Any]] = []

    def abort_after_attempt(index: int, item: dict[str, Any], failure_type: str, error: Exception, request_seconds: float) -> None:
        stage["attempt_failures"] += 1
        stage["wall_seconds"] += request_seconds
        ledger["state"] = "failed_after_persisted_provider_attempt"
        validate_ledger(ledger)
        write_json_new(records_root / f"request_{index:04d}_fatal_failure.json", {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-attempt-failure-v1",
            "prompt_id": item["prompt_id"],
            "prompt_sha256": item["prompt_sha256"],
            "failure_type": failure_type,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "request_seconds": request_seconds,
            "possible_external_submission": True,
            "automatic_retries": 0,
        })
        write_json_new(staging / "failure_ledger.json", ledger)
        write_json_new(staging / "failure_manifest.json", {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-failure-manifest-v1",
            "state": "failed_after_persisted_provider_attempt_authorisation_consumed_no_automatic_retry",
            "payload": {"path": relative(root / PREFLIGHT_ROOT / PAYLOAD_NAME, root), "sha256": sha256_file(root / PREFLIGHT_ROOT / PAYLOAD_NAME)},
            "execution_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
            "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
            "authorisation_consumption": None if consumption_receipt is None else {"path": relative(consumption_receipt, root), "sha256": sha256_file(consumption_receipt)},
            "failed_prompt_id": item["prompt_id"],
            "network_calls_confirmed": stage["successful_api_calls"],
            "possible_external_submissions": stage["external_text_submissions"],
            "automatic_retries": 0,
            "thesis_result_writing": False,
        })
        raise RuntimeError("FQ-P parser attempt failed after durable receipt; authorisation is consumed and no automatic retry is permitted") from error

    for index, item in enumerate(inventory):
        raw_query = str(item["raw_query"])
        cached = cache.load(raw_query)
        if cached is not None:
            stage["cache_hits"] += 1
            rows.append(_result_row(item, cached, cache_status="exact_cache_hit"))
            continue

        stage["cache_misses"] += 1
        projected_attempts = stage["request_attempts"] + 1
        projected_submissions = stage["external_text_submissions"] + 1
        projected_bytes = stage["external_raw_query_utf8_bytes"] + int(item["raw_query_utf8_bytes"])
        projected_input_bound = stage["provider_input_token_upper_bound"] + int(item["provider_input_token_upper_bound"])
        projected_output_bound = stage["provider_output_tokens"] + int(item["request"]["max_tokens"])
        projected_price = (projected_input_bound * PARSER_INPUT_USD_PER_MILLION_TOKENS + projected_output_bound * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
        require(projected_attempts <= int(authorisation["maximum_request_attempts"]), "FQ-P request-attempt cap would be exceeded")
        require(projected_submissions <= int(authorisation["maximum_external_raw_query_submissions"]), "FQ-P raw-query submission cap would be exceeded")
        require(projected_bytes <= int(authorisation["maximum_external_raw_query_utf8_bytes"]), "FQ-P raw-query byte cap would be exceeded")
        require(projected_input_bound <= int(authorisation["maximum_parser_input_tokens"]), "FQ-P parser input-token bound would be exceeded")
        require(projected_output_bound <= int(authorisation["maximum_parser_output_tokens"]), "FQ-P parser output-token bound would be exceeded")
        require(projected_price <= float(authorisation["maximum_standard_list_price_usd"]), "FQ-P price ceiling would be exceeded")
        stage["request_attempts"] = projected_attempts
        stage["external_text_submissions"] = projected_submissions
        stage["external_raw_query_utf8_bytes"] = projected_bytes
        stage["provider_input_token_upper_bound"] = projected_input_bound
        validate_ledger(ledger)
        write_json_new(records_root / f"request_{index:04d}_attempt.json", {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-attempt-v2",
            "state": "persisted_before_provider_call",
            "prompt_id": item["prompt_id"],
            "prompt_sha256": item["prompt_sha256"],
            "raw_query_utf8_bytes": item["raw_query_utf8_bytes"],
            "provider_input_token_upper_bound": item["provider_input_token_upper_bound"],
            "request": item["request"],
            "automatic_retries": 0,
        })
        write_json_new(records_root / f"request_{index:04d}_ledger_before_call.json", ledger)
        started = time.perf_counter()
        try:
            response = _post_chat_once(api_key, item["request"], int(authorisation["timeout_seconds"]))
        except Exception as error:
            abort_after_attempt(index, item, "provider_transport_or_response_decode_failure", error, time.perf_counter() - started)
        request_seconds = time.perf_counter() - started
        stage["successful_api_calls"] += 1
        stage["wall_seconds"] += request_seconds
        write_json_new(records_root / f"request_{index:04d}_response.json", response)
        try:
            prompt_tokens, completion_tokens = _usage(response)
            stage["provider_input_tokens"] += prompt_tokens
            stage["provider_output_tokens"] += completion_tokens
            actual_price = (stage["provider_input_tokens"] * PARSER_INPUT_USD_PER_MILLION_TOKENS + stage["provider_output_tokens"] * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
            require(stage["successful_api_calls"] <= int(authorisation["maximum_successful_api_calls"]), "FQ-P successful-call cap exceeded")
            require(stage["provider_input_tokens"] <= int(authorisation["maximum_parser_input_tokens"]), "FQ-P parser input-token cap exceeded")
            require(stage["provider_output_tokens"] <= int(authorisation["maximum_parser_output_tokens"]), "FQ-P parser output-token cap exceeded")
            require(actual_price <= float(authorisation["maximum_standard_list_price_usd"]), "FQ-P actual price ceiling exceeded")
            entry = _parse_provider_response(raw_query, response)
            entry["request_seconds"] = request_seconds
            entry["provider_usage"] = {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}
            cache.store(raw_query, entry)
            write_json_new(records_root / f"request_{index:04d}_cache_commit.json", {
                "schema_version": "rq2bv1-v3-b1e-fq-parser-cache-commit-v2",
                "prompt_id": item["prompt_id"],
                "query_sha256": sha256_text(raw_query),
                "cache_entry_sha256": sha256_file(cache.path(raw_query)),
                "parser_status": entry["status"],
                "failure_class": entry.get("failure_class"),
                "response_content_sha256": entry["response_content_sha256"],
                "provider_usage": entry["provider_usage"],
                "request_seconds": entry["request_seconds"],
            })
            rows.append(_result_row(item, entry, cache_status="new_provider_call"))
        except Exception as error:
            abort_after_attempt(index, item, "provider_usage_or_local_response_processing_failure", error, 0.0)

    reliability = ledger["reliability"]
    reliability["queries_total"] = len(rows)
    reliability["parser_valid"] = sum(row["parser_status"] == "valid" for row in rows)
    reliability["parser_schema_failures"] = sum(row["parser_status"] == "invalid" and row["failure_class"] in {"schema", "invalid_json", "provider_response_schema"} for row in rows)
    reliability["parser_span_grounding_failures"] = sum(row["parser_status"] == "invalid" and row["failure_class"] == "span_grounding" for row in rows)
    reliability["parser_empty_field_failures"] = sum(row["parser_status"] == "invalid" and row["failure_class"] == "empty_fields" for row in rows)
    reliability["fallback_queries"] = len(rows) - reliability["parser_valid"]
    reliability["active_field_count_total"] = sum(len(row["parsed"]["active_fields"]) for row in rows if row["parsed"] is not None)
    ledger["state"] = "parser_stage_completed_pending_query_field_embedding_preflight"
    validate_ledger(ledger)
    warm = _warm_replay(rows, inventory, cache)
    rows_path, ledger_path = staging / "parsed_queries.jsonl", staging / "parser_ledger.json"
    final_rows_path, final_ledger_path = output_root / "parsed_queries.jsonl", output_root / "parser_ledger.json"
    write_jsonl_new(rows_path, rows)
    write_json_new(ledger_path, ledger)
    record_paths = sorted(records_root.glob("*.json"))
    request_records_manifest = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-request-records-v2",
        "records": [{"path": relative(output_root / "request_records" / path.name, root), "sha256": sha256_file(path)} for path in record_paths],
    }
    request_records_manifest_path = staging / "request_records_manifest.json"
    final_request_records_manifest_path = output_root / "request_records_manifest.json"
    write_json_new(request_records_manifest_path, request_records_manifest)
    actual_price = (stage["provider_input_tokens"] * PARSER_INPUT_USD_PER_MILLION_TOKENS + stage["provider_output_tokens"] * PARSER_OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
    manifest = {
        "schema_version": "rq2bv1-v3-b1e-fq-parser-run-manifest-v2",
        "state": "parser_stage_completed_pending_query_field_embedding_preflight",
        "run_id": packet["run_id"],
        "runner_version": RUNNER_VERSION,
        "payload": {"path": relative(root / PREFLIGHT_ROOT / PAYLOAD_NAME, root), "sha256": sha256_file(root / PREFLIGHT_ROOT / PAYLOAD_NAME)},
        "execution_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
        "authorisation": {"path": relative(authorisation_path, root), "sha256": sha256_file(authorisation_path)},
        "authorisation_consumption": None if consumption_receipt is None else {"path": relative(consumption_receipt, root), "sha256": sha256_file(consumption_receipt)},
        "parser_contract_sha256": parser_contract_sha256(),
        "artifacts": {
            "rows": {"path": relative(final_rows_path, root), "rows": len(rows), "sha256": sha256_file(rows_path)},
            "ledger": {"path": relative(final_ledger_path, root), "sha256": sha256_file(ledger_path)},
            "request_records": {"path": relative(final_request_records_manifest_path, root), "sha256": sha256_file(request_records_manifest_path), "records": len(record_paths)},
        },
        "network_calls": int(stage["successful_api_calls"]),
        "parser_standard_list_price_usd": actual_price,
        "warm_replay": warm,
        "thesis_result_writing": False,
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.rename(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    query = "Convert scanned invoices into page-anchored JSON."
    input_start, output_start = query.index("scanned invoices"), query.index("page-anchored JSON")
    fields = {field: [] for field in ("use_condition", "input_precondition", "output_artifact", "workflow_procedure", "dependency_resource", "boundary_not_for", "success_verification")}
    fields["input_precondition"] = [{"start": input_start, "end": input_start + len("scanned invoices"), "text": "scanned invoices"}]
    fields["output_artifact"] = [{"start": output_start, "end": output_start + len("page-anchored JSON"), "text": "page-anchored JSON"}]
    response = {"choices": [{"message": {"content": json.dumps({"fields": fields})}}]}
    parsed = _parse_provider_response(query, response)
    require(parsed["status"] == "valid" and parsed["parsed"]["active_fields"] == ["input_precondition", "output_artifact"], "FQ-P runner self-test failed")
    require(request_payload(query)["enable_thinking"] is False, "FQ-P runner self-test non-thinking drift")
    return {"schema_version": "rq2bv1-v3-b1e-fq-parser-runner-self-test-v2", "state": "self_test_passed_zero_network", "network_calls": 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--authorisation", type=Path, default=Path(DEFAULT_AUTHORISATION))
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.execute, "Choose exactly one of --self-test or --execute")
    output = self_test() if args.self_test else run(args.root.resolve(), _path(args.root.resolve(), args.authorisation), args.api_key_env)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
