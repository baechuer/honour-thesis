#!/usr/bin/env python3
"""Shared zero-network/runtime helpers for the separately versioned B1E-FQ V2 parser."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any

from rq2b_common import read_json, require, sha256_json, sha256_text, write_json_new
from rq2bv1_query_field_parser_v2 import (
    FIELD_ORDER,
    PARSER_BASE_URL,
    PARSER_MODEL,
    parser_contract_sha256,
    validate_response,
)


PROFILES: dict[str, dict[str, Any]] = {
    "smoke": {
        "run_id": "rq2bv1-v3-qwen-field-aligned-parser-v2-1-smoke-001",
        "preflight_root": "skill_benchmark/rq2bv1/preflight/qwen_field_aligned_v3_parser_v2_1_smoke",
        "result_root": "skill_benchmark/rq2bv1/results/qwen_field_aligned_v3_parser_v2_1_smoke",
        "cache_root": "skill_benchmark/cache/rq2bv1/query_parses_v2_1_smoke",
        "prompt_selection": "sha256_prompt_id_ascending_first_20",
        "expected_prompts": 20,
    },
    "full": {
        "run_id": "rq2bv1-v3-qwen-field-aligned-parser-v2-1-full-001",
        "preflight_root": "skill_benchmark/rq2bv1/preflight/qwen_field_aligned_v3_parser_v2_1_full",
        "result_root": "skill_benchmark/rq2bv1/results/qwen_field_aligned_v3_parser_v2_1_full",
        "cache_root": "skill_benchmark/cache/rq2bv1/query_parses_v2_1_full",
        "prompt_selection": "all_strict_prompts_by_prompt_id",
        "expected_prompts": 381,
    },
}
INVENTORY_NAME = "parser_request_inventory.jsonl"
PAYLOAD_NAME = "payload_manifest.json"
PACKET_NAME = "execution_approval_packet.json"
REPORT_NAME = "preflight_report.json"
REVIEW_NAME = "local_protocol_review.json"
AUTHORISATION_CONSUMPTION_ROOT = "skill_benchmark/rq2bv1/approvals/consumed"
TIMEOUT_SECONDS = 120
PARSER_INPUT_OVERHEAD_TOKEN_UPPER_BOUND = 512
PARSER_PRICE_DATE = "2026-08-22"
PARSER_PRICE_SOURCE_URL = "https://www.alibabacloud.com/help/en/model-studio/model-pricing"
PARSER_INPUT_USD_PER_MILLION_TOKENS = 0.40
PARSER_OUTPUT_USD_PER_MILLION_TOKENS = 1.60
FORBIDDEN_ROUTING_METADATA = {"gold_skill", "candidate", "target_field", "skill_id", "cluster_id", "outcome", "rank", "label"}


def profile(name: str) -> dict[str, Any]:
    require(name in PROFILES, f"Unknown B1E-FQ V2 profile: {name}")
    return dict(PROFILES[name])


def provider_input_token_upper_bound(raw_query: str) -> int:
    from rq2bv1_query_field_parser_v2 import parser_contract

    return len(parser_contract()["system_prompt"].encode("utf-8")) + len(raw_query.encode("utf-8")) + PARSER_INPUT_OVERHEAD_TOKEN_UPPER_BOUND


def contains_forbidden_routing_metadata(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(FORBIDDEN_ROUTING_METADATA & set(value)) or any(contains_forbidden_routing_metadata(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_forbidden_routing_metadata(child) for child in value)
    return False


class ExactQueryParseCacheV2:
    """Run-namespace cache. Smoke and full responses can never be shared."""

    def __init__(self, root: Path, run_id: str) -> None:
        self.root = root / "qwen" / PARSER_MODEL / parser_contract_sha256() / run_id
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, raw_query: str) -> Path:
        key = sha256_json({
            "base_url": PARSER_BASE_URL,
            "model": PARSER_MODEL,
            "parser_contract_sha256": parser_contract_sha256(),
            "run_id": self.root.name,
            "query_sha256": sha256_text(raw_query),
        })
        return self.root / f"{key}.json"

    def load(self, raw_query: str) -> dict[str, Any] | None:
        path = self.path(raw_query)
        if not path.exists():
            return None
        value = read_json(path)
        require(value.get("schema_version") == "rq2bv1-v3-b1e-fq-parser-v2-cache-v1", "FQ-P V2 cache schema drift")
        require(value.get("base_url") == PARSER_BASE_URL and value.get("model") == PARSER_MODEL, "FQ-P V2 cache provider drift")
        require(value.get("parser_contract_sha256") == parser_contract_sha256(), "FQ-P V2 cache contract drift")
        require(value.get("query_sha256") == sha256_text(raw_query), "FQ-P V2 cache query drift")
        require(value.get("status") in {"valid", "fallback"}, "FQ-P V2 cache status drift")
        require(isinstance(value.get("request_seconds"), (int, float)) and value["request_seconds"] >= 0, "FQ-P V2 cache time drift")
        usage = value.get("provider_usage")
        require(isinstance(usage, dict) and set(usage) == {"prompt_tokens", "completion_tokens"}, "FQ-P V2 cache usage drift")
        require(all(type(count) is int and count >= 0 for count in usage.values()), "FQ-P V2 cache usage invalid")
        if value["status"] == "valid":
            require(value.get("failure_class") is None and isinstance(value.get("parsed"), dict), "FQ-P V2 valid cache drift")
            # Stored parses contain local audit locations, whereas the parser
            # contract accepts provider-style lists of text strings. Rebuild
            # that contract payload before revalidating a cache entry.
            cached_texts = {
                field: [str(span["text"]) for span in value["parsed"]["fields"][field]]
                for field in FIELD_ORDER
            }
            validated = validate_response(raw_query, {"fields": cached_texts})
            require(value["parsed"] == validated.as_dict(), "FQ-P V2 valid cache parse drift")
        else:
            require(value.get("parsed") is None and isinstance(value.get("failure_class"), str), "FQ-P V2 fallback cache drift")
        return value

    def store(self, raw_query: str, entry: dict[str, Any]) -> Path:
        path = self.path(raw_query)
        require(not path.exists(), "Refusing to overwrite FQ-P V2 parser cache")
        write_json_new(path, {
            "schema_version": "rq2bv1-v3-b1e-fq-parser-v2-cache-v1",
            "base_url": PARSER_BASE_URL,
            "model": PARSER_MODEL,
            "parser_contract_sha256": parser_contract_sha256(),
            "query_sha256": sha256_text(raw_query),
            **entry,
        })
        return path


def post_chat_once(api_key: str, payload: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{PARSER_BASE_URL}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        value = json.loads(response.read().decode("utf-8"))
    require(isinstance(value, dict), "FQ-P V2 provider response is not an object")
    return value


def provider_usage(response: dict[str, Any]) -> dict[str, int]:
    usage = response.get("usage")
    require(isinstance(usage, dict), "FQ-P V2 provider response lacks usage")
    prompt_tokens, completion_tokens = usage.get("prompt_tokens"), usage.get("completion_tokens")
    require(type(prompt_tokens) is int and type(completion_tokens) is int and prompt_tokens >= 0 and completion_tokens >= 0, "FQ-P V2 provider usage drift")
    return {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}


def parse_provider_response(raw_query: str, response: dict[str, Any]) -> dict[str, Any]:
    """Turn one successful HTTP response into either a validated parse or fallback."""
    try:
        choice = response["choices"][0]
        # A JSON-looking prefix from a length-truncated answer is not a
        # complete parser decision. Treat every non-stop completion as a
        # documented fallback before attempting local validation.
        if choice.get("finish_reason") != "stop":
            return {
                "status": "fallback",
                "parsed": None,
                "failure_class": f"provider_finish_reason_{choice.get('finish_reason') or 'missing'}",
                "response_content_sha256": sha256_text(str(response)),
            }
        content = choice["message"]["content"]
        require(isinstance(content, str), "FQ-P V2 provider content is not text")
        parsed = validate_response(raw_query, json.loads(content))
        return {
            "status": "valid",
            "parsed": parsed.as_dict(),
            "failure_class": None,
            "response_content_sha256": sha256_text(content),
        }
    except json.JSONDecodeError:
        return {"status": "fallback", "parsed": None, "failure_class": "invalid_json", "response_content_sha256": sha256_text(str(response))}
    except ValueError as exc:
        message = str(exc).lower()
        failure_class = "empty_fields" if "no active fields" in message else "span_grounding" if any(token in message for token in ("absent", "ambiguous", "overlap")) else "schema"
        return {"status": "fallback", "parsed": None, "failure_class": failure_class, "response_content_sha256": sha256_text(str(response))}
    except (KeyError, IndexError, TypeError):
        return {"status": "fallback", "parsed": None, "failure_class": "provider_response_schema", "response_content_sha256": sha256_text(str(response))}
