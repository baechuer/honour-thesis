#!/usr/bin/env python3
"""Independently review one sealed B1E-FQ V2 parser packet without network use."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, sha256_text, write_json_new
from rq2bv1_fq_parser_v2_runtime import INVENTORY_NAME, PACKET_NAME, PAYLOAD_NAME, REVIEW_NAME, contains_forbidden_routing_metadata, profile, provider_input_token_upper_bound
from rq2bv1_query_field_parser_v2 import PARSER_BASE_URL, PARSER_ENABLE_THINKING, PARSER_MAX_OUTPUT_TOKENS, PARSER_MODEL, PARSER_TEMPERATURE, SYSTEM_PROMPT, parser_contract_sha256, request_payload
from run_rq2bv1_v3_qwen_field_aligned_parser_v2 import _packet, validate_preflight


REVIEW_SCHEMA = "rq2bv1-v3-b1e-fq-parser-v2-local-protocol-review-v1"


def review(root: Path, profile_name: str) -> dict[str, Any]:
    spec = profile(profile_name)
    preflight_root = root / spec["preflight_root"]
    payload_path, packet_path, inventory_path = preflight_root / PAYLOAD_NAME, preflight_root / PACKET_NAME, preflight_root / INVENTORY_NAME
    review_path = preflight_root / REVIEW_NAME
    require(payload_path.is_file() and packet_path.is_file() and inventory_path.is_file(), "B1E-FQ V2 preflight artifacts are incomplete")
    require(not review_path.exists(), "Refusing to overwrite B1E-FQ V2 local protocol review")
    require(not (root / spec["result_root"]).exists(), "B1E-FQ V2 result already exists; review no longer precedes execution")
    payload, packet, rows = read_json(payload_path), read_json(packet_path), read_jsonl(inventory_path)
    runtime_packet_path, runtime_packet = _packet(root, profile_name)
    runtime_payload, runtime_rows = validate_preflight(root, profile_name, runtime_packet)
    require(runtime_packet_path == packet_path and runtime_packet == packet and runtime_payload == payload and runtime_rows == rows, "B1E-FQ V2 runtime binding review drift")
    require(payload.get("state") == "sealed_not_executed" and payload.get("network_calls") == 0, "B1E-FQ V2 payload state drift")
    require(payload.get("profile") == packet.get("profile") == profile_name, "B1E-FQ V2 profile review drift")
    require(len(rows) == spec["expected_prompts"] and not contains_forbidden_routing_metadata(rows), "B1E-FQ V2 outbound boundary drift")
    require(payload["parser_contract"]["contract_sha256"] == parser_contract_sha256(), "B1E-FQ V2 parser-contract drift")
    recovery = payload.get("local_recovery_regression")
    require(isinstance(recovery, dict) and recovery.get("state") == "passed_zero_network" and recovery.get("network_calls") == 0, "B1E-FQ V2.1 local-recovery evidence drift")
    require(recovery.get("historical_replay", {}).get("historical_complete_responses_revalidated") == 150, "B1E-FQ V2.1 historical replay drift")
    require(recovery.get("synthetic_full_inventory", {}).get("synthetic_valid_cache_round_trips") == 381, "B1E-FQ V2.1 synthetic cache replay drift")
    for row in rows:
        require(row["prompt_sha256"] == sha256_text(row["raw_query"]), "B1E-FQ V2 prompt hash drift")
        require(row["raw_query_utf8_bytes"] == len(row["raw_query"].encode("utf-8")), "B1E-FQ V2 byte-count drift")
        require(row["provider_input_token_upper_bound"] == provider_input_token_upper_bound(row["raw_query"]), "B1E-FQ V2 input-cap drift")
        require(row["request"] == request_payload(row["raw_query"]), "B1E-FQ V2 outbound request drift")
        request = row["request"]
        require(request["model"] == PARSER_MODEL and request["temperature"] == PARSER_TEMPERATURE, "B1E-FQ V2 model/temperature drift")
        require(request["enable_thinking"] is PARSER_ENABLE_THINKING is False, "B1E-FQ V2 thinking-mode drift")
        require(request["max_tokens"] == PARSER_MAX_OUTPUT_TOKENS and request["response_format"] == {"type": "json_object"}, "B1E-FQ V2 JSON-mode drift")
        require(request["messages"] == [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": row["raw_query"]}], "B1E-FQ V2 request message boundary drift")
    require(packet["automatic_retries"] == 0 and "no automatic retry" in packet["excluded_actions"], "B1E-FQ V2 retry boundary drift")
    require("no candidate or gold-label text sent to parser" in packet["excluded_actions"], "B1E-FQ V2 candidate/gold exclusion drift")
    require("no query-field embedding" in packet["excluded_actions"] and "no retrieval scoring or reranking" in packet["excluded_actions"], "B1E-FQ V2 parser-only boundary drift")
    for script in packet["execution_scripts"]:
        path = root / script["path"]
        require(path.is_file() and sha256_file(path) == script["sha256"], f"B1E-FQ V2 script hash drift: {script['path']}")
    receipt = {
        "schema_version": REVIEW_SCHEMA,
        "state": "local_protocol_review_passed_no_network_no_external_text_sent",
        "profile": profile_name,
        "preflight": {
            "payload": {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)},
            "execution_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
            "inventory": {"path": relative(inventory_path, root), "rows": len(rows), "sha256": sha256_file(inventory_path)},
        },
        "checks": {
            "network_calls": 0,
            "parser_requests": len(rows),
            "candidate_library_skills_visible_to_parser": 0,
            "forbidden_routing_metadata_absent": True,
            "request_shape_is_system_plus_raw_prompt_only": True,
            "v2_1_exact_string_only_contract": True,
            "local_grounded_alignment_allows_repeated_and_cross_field_text": True,
            "local_recovery_regression": "passed_zero_network",
            "automatic_retries": 0,
            "per_prompt_fallback_continue_batch": True,
            "query_embedding_or_selection_executed": False,
            "thesis_result_writing": False,
        },
        "remaining_gate": "explicit_user_authorisation_for_this_exact_raw_prompt_parser_transfer_only",
    }
    write_json_new(review_path, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--profile", choices=("smoke", "full"), required=True)
    args = parser.parse_args()
    value = review(args.root.resolve(), args.profile)
    print(json.dumps({"state": value["state"], "profile": args.profile, "network_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
