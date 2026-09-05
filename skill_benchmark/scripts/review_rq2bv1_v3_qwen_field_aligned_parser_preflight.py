#!/usr/bin/env python3
"""Locally review the sealed B1E-FQ parser-transfer packet without network use."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from rq2bv1_fq_parser_execution_contract import (
    AUTHORISATION_CONSUMPTION_ROOT,
    INVENTORY_NAME,
    PACKET_NAME,
    PAYLOAD_NAME,
    PREFLIGHT_ROOT,
    RESULT_ROOT,
    provider_input_token_upper_bound,
)
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, sha256_text, write_json_new
from rq2bv1_query_field_parser import (
    PARSER_BASE_URL,
    PARSER_ENABLE_THINKING,
    PARSER_MAX_OUTPUT_TOKENS,
    PARSER_MODEL,
    PARSER_TEMPERATURE,
    SYSTEM_PROMPT,
    parser_contract_sha256,
    request_payload,
)
from run_rq2bv1_v3_qwen_field_aligned_parser import _packet, _validate_preflight


REVIEW_SCHEMA = "rq2bv1-v3-b1e-fq-parser-local-protocol-review-v2"
FORBIDDEN_METADATA_KEYS = {"gold_skill", "candidate", "target_field", "skill_id", "cluster_id", "outcome", "rank", "label"}


def _contains_forbidden_metadata(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(FORBIDDEN_METADATA_KEYS & set(value)) or any(_contains_forbidden_metadata(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_metadata(child) for child in value)
    return False


def review(root: Path) -> dict[str, Any]:
    preflight_root = root / PREFLIGHT_ROOT
    payload_path = preflight_root / PAYLOAD_NAME
    packet_path = preflight_root / PACKET_NAME
    inventory_path = preflight_root / INVENTORY_NAME
    review_path = preflight_root / "local_protocol_review.json"
    require(payload_path.is_file() and packet_path.is_file() and inventory_path.is_file(), "FQ-P preflight artifacts are incomplete")
    require(not review_path.exists(), "Refusing to overwrite FQ-P local protocol review")
    require(not (root / RESULT_ROOT).exists(), "FQ-P parser result directory already exists; review no longer precedes execution")

    payload, packet, rows = read_json(payload_path), read_json(packet_path), read_jsonl(inventory_path)
    runtime_packet_path, runtime_packet = _packet(root)
    runtime_payload, runtime_rows = _validate_preflight(root, runtime_packet)
    require(payload.get("state") == "sealed_not_executed" and payload.get("network_calls") == 0, "FQ-P payload state drift")
    require(packet.get("state") == "awaiting_independent_review_then_explicit_parser_transfer_authorisation", "FQ-P packet state drift")
    require(packet.get("automatic_retries") == 0, "FQ-P packet permits automatic retry")
    require(payload.get("base_url") == packet.get("base_url") == PARSER_BASE_URL, "FQ-P endpoint drift")
    require(payload.get("model") == packet.get("model") == PARSER_MODEL, "FQ-P model drift")
    require(packet.get("authorisation_consumption_root") == AUTHORISATION_CONSUMPTION_ROOT, "FQ-P authorisation-consumption drift")
    require(payload["parser_contract"]["contract_sha256"] == parser_contract_sha256(), "FQ-P parser contract drift")
    require(payload["strict_population"] == {"strict_prompts": 381, "candidate_library_skills_visible_to_parser": 0}, "FQ-P population boundary drift")
    require(len(rows) == 381 and len({row["prompt_id"] for row in rows}) == 381, "FQ-P inventory population drift")
    require(runtime_packet_path == packet_path and runtime_packet == packet and runtime_payload == payload and runtime_rows == rows, "FQ-P runtime binding review drift")
    require(not _contains_forbidden_metadata(rows), "FQ-P request inventory contains candidate or routing metadata")

    request_shapes: set[tuple[str, ...]] = set()
    for row in rows:
        require(set(row) == {
            "schema_version", "prompt_id", "prompt_sha256", "raw_query", "raw_query_utf8_bytes",
            "provider_input_token_upper_bound", "request",
        }, "FQ-P inventory row schema drift")
        require(row["prompt_sha256"] == sha256_text(row["raw_query"]), "FQ-P prompt hash drift")
        require(row["raw_query_utf8_bytes"] == len(row["raw_query"].encode("utf-8")), "FQ-P raw-query byte count drift")
        require(row["provider_input_token_upper_bound"] == provider_input_token_upper_bound(row["raw_query"]), "FQ-P parser input-cap drift")
        request = row["request"]
        request_shapes.add(tuple(sorted(request)))
        require(request["model"] == PARSER_MODEL and request["temperature"] == PARSER_TEMPERATURE, "FQ-P request model drift")
        require(request["enable_thinking"] is PARSER_ENABLE_THINKING is False, "FQ-P request thinking-mode drift")
        require(request["max_tokens"] == PARSER_MAX_OUTPUT_TOKENS and request["response_format"] == {"type": "json_object"}, "FQ-P request generation drift")
        require(request == request_payload(row["raw_query"]), "FQ-P runtime request reconstruction drift")
        messages = request["messages"]
        require(isinstance(messages, list) and len(messages) == 2, "FQ-P request message count drift")
        require(messages[0] == {"role": "system", "content": SYSTEM_PROMPT}, "FQ-P system prompt drift")
        require(messages[1] == {"role": "user", "content": row["raw_query"]}, "FQ-P raw-query binding drift")
    require(request_shapes == {("enable_thinking", "max_tokens", "messages", "model", "response_format", "temperature")}, "FQ-P request shape drift")

    expected_packet_limits = {key: value for key, value in payload["counts"].items() if key.startswith("maximum_")}
    require({key: packet[key] for key in expected_packet_limits} == expected_packet_limits, "FQ-P packet cap drift")
    require(packet["payload"] == {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)}, "FQ-P packet payload binding drift")
    for script in packet["execution_scripts"]:
        path = root / script["path"]
        require(path.is_file() and sha256_file(path) == script["sha256"], f"FQ-P execution script drift: {script['path']}")
    excluded = set(packet["excluded_actions"])
    require({
        "no automatic retry",
        "one-time authorisation consumption before the first provider attempt",
        "no candidate or gold-label text sent to parser",
        "no query-field embedding",
        "no candidate embedding",
        "no retrieval scoring or reranking",
        "no thesis LaTeX or PDF result writing",
    } <= excluded, "FQ-P excluded-action boundary drift")

    receipt = {
        "schema_version": REVIEW_SCHEMA,
        "state": "local_protocol_review_passed_no_network_no_external_text_sent",
        "preflight": {
            "payload": {"path": relative(payload_path, root), "sha256": sha256_file(payload_path)},
            "execution_packet": {"path": relative(packet_path, root), "sha256": sha256_file(packet_path)},
            "inventory": {"path": relative(inventory_path, root), "rows": len(rows), "sha256": sha256_file(inventory_path)},
        },
        "checks": {
            "network_calls": 0,
            "strict_prompt_count": len(rows),
            "candidate_library_skills_visible_to_parser": 0,
            "forbidden_routing_metadata_absent": True,
            "request_shape_is_system_plus_raw_prompt_only": True,
            "raw_prompt_binding_validated": True,
            "runtime_payload_and_request_reconstruction_validated": True,
            "explicit_non_thinking_mode": True,
            "parser_contract_sha256": parser_contract_sha256(),
            "execution_script_hashes_validated": len(packet["execution_scripts"]),
            "automatic_retries": 0,
            "one_time_authorisation_consumption_before_provider_attempt": True,
            "query_embedding_or_selection_executed": False,
            "thesis_result_writing": False,
        },
        "remaining_gate": "explicit_user_authorisation_for_raw_prompt_parser_transfer_only",
    }
    write_json_new(review_path, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args()
    receipt = review(args.root.resolve())
    print({"state": receipt["state"], "network_calls": 0, "review": receipt["preflight"]["execution_packet"]})


if __name__ == "__main__":
    main()
