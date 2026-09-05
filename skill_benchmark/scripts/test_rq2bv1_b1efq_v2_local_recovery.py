#!/usr/bin/env python3
"""Zero-network regression checks for the B1E-FQ V2.1 parser recovery.

This is deliberately a contract test, not a parser-quality evaluation. It
replays only already persisted V1 responses locally, then exercises the fresh
V2.1 validation and cache paths with synthetic grounded responses for the
entire strict-prompt inventory. It never calls a provider.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from rq2b_common import repo_root, require
from rq2bv1_fq_parser_v2_runtime import ExactQueryParseCacheV2, parse_provider_response
from rq2bv1_query_field_parser_v2 import FIELD_ORDER, self_test, validate_legacy_v1_response


HISTORICAL_RECORDS = Path(
    "skill_benchmark/rq2bv1/results/qwen_field_aligned_v3_parser_failed_timeout_attempt_002/request_records"
)
HISTORICAL_INVENTORY = Path(
    "skill_benchmark/rq2bv1/preflight/qwen_field_aligned_v3_parser/parser_request_inventory.jsonl"
)


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected object: {path}")
    return value


def _historical_replay(root: Path) -> dict[str, int]:
    inventory = {
        str(row["prompt_id"]): row
        for row in (json.loads(line) for line in (root / HISTORICAL_INVENTORY).read_text(encoding="utf-8").splitlines())
    }
    records = root / HISTORICAL_RECORDS
    valid = 0
    length_truncated = 0
    for response_path in sorted(records.glob("*_response.json")):
        response = _read_json(response_path)
        choice = response["choices"][0]
        require(isinstance(choice, dict), f"Historical choice drift: {response_path.name}")
        if choice.get("finish_reason") == "length":
            length_truncated += 1
            continue
        request_index = int(response_path.name.split("_")[1])
        attempt = _read_json(records / f"request_{request_index:04d}_attempt.json")
        prompt_id = str(attempt["prompt_id"])
        content = choice["message"]["content"]
        require(isinstance(content, str), f"Historical content drift: {response_path.name}")
        validate_legacy_v1_response(str(inventory[prompt_id]["raw_query"]), json.loads(content))
        valid += 1
    return {"historical_complete_responses_revalidated": valid, "historical_length_truncated_responses": length_truncated}


def _synthetic_full_inventory(root: Path) -> dict[str, int]:
    rows = [
        json.loads(line)
        for line in (root / HISTORICAL_INVENTORY).read_text(encoding="utf-8").splitlines()
    ]
    require(len(rows) == 381, "Strict prompt population drift")
    with tempfile.TemporaryDirectory() as directory:
        cache = ExactQueryParseCacheV2(Path(directory), "zero-network-full-contract-test")
        for row in rows:
            raw_query = str(row["raw_query"])
            payload = {"fields": {field: [] for field in FIELD_ORDER}}
            payload["fields"]["use_condition"] = [raw_query[: min(180, len(raw_query))]]
            response = {
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(payload)}}],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }
            entry = parse_provider_response(raw_query, response)
            require(entry["status"] == "valid", f"Synthetic grounded parse failed: {row['prompt_id']}")
            entry.update({"request_seconds": 0.0, "provider_usage": {"prompt_tokens": 0, "completion_tokens": 0}})
            cache.store(raw_query, entry)
            loaded = cache.load(raw_query)
            require(loaded is not None and loaded["parsed"] == entry["parsed"], f"Cache round-trip drift: {row['prompt_id']}")
        require(len(list(cache.root.glob("*.json"))) == len(rows), "Synthetic cache coverage drift")
    return {"synthetic_full_inventory_rows": len(rows), "synthetic_valid_cache_round_trips": len(rows)}


def run(root: Path) -> dict[str, object]:
    malformed = parse_provider_response(
        "route this",
        {"choices": [{"finish_reason": "stop", "message": {"content": "not-json"}}], "usage": {"prompt_tokens": 0, "completion_tokens": 0}},
    )
    truncated = parse_provider_response(
        "route this",
        {"choices": [{"finish_reason": "length", "message": {"content": "{}"}}], "usage": {"prompt_tokens": 0, "completion_tokens": 768}},
    )
    require(malformed["status"] == "fallback" and malformed["failure_class"] == "invalid_json", "Malformed JSON fallback drift")
    require(truncated["status"] == "fallback" and truncated["failure_class"] == "provider_finish_reason_length", "Truncation fallback drift")
    return {
        "schema_version": "rq2bv1-b1e-fq-v2-1-local-recovery-test-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
        "parser_self_test": self_test()["state"],
        "historical_replay": _historical_replay(root),
        "synthetic_full_inventory": _synthetic_full_inventory(root),
        "fallback_contract": {"invalid_json": malformed["failure_class"], "truncation": truncated["failure_class"]},
        "scientific_result": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(repo_root()), indent=2, sort_keys=True))
