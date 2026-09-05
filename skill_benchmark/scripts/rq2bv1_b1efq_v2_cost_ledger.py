#!/usr/bin/env python3
"""Zero-network ledger schema for B1E-FQ V2 parser stages."""

from __future__ import annotations

import math
from typing import Any

from rq2b_common import require


LEDGER_SCHEMA = "rq2bv1-v3-b1e-fq-parser-v2-cost-ledger-v1"
STAGES = ("query_parsing",)
RELIABILITY_KEYS = {
    "queries_total", "parser_valid", "parser_schema_failures",
    "parser_span_grounding_failures", "parser_empty_field_failures",
    "parser_invalid_json_failures", "parser_provider_response_failures",
    "parser_transport_failures", "fallback_queries", "active_field_count_total",
}


def stage_template() -> dict[str, float | int]:
    return {
        "external_text_submissions": 0,
        "external_raw_query_utf8_bytes": 0,
        "request_attempts": 0,
        "successful_api_calls": 0,
        "attempt_failures": 0,
        "automatic_retries": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "provider_input_token_upper_bound": 0,
        "provider_input_tokens": 0,
        "provider_output_tokens": 0,
        "wall_seconds": 0.0,
    }


def empty_ledger() -> dict[str, Any]:
    return {
        "schema_version": LEDGER_SCHEMA,
        "state": "template_not_a_scientific_result",
        "per_query": {stage: stage_template() for stage in STAGES},
        "reliability": {key: 0 for key in RELIABILITY_KEYS},
        "comparability": {
            "parser_only_not_a_retrieval_result": True,
            "automatic_retries": 0,
            "fallback_ranking_materialized": False,
        },
    }


def validate_ledger(ledger: dict[str, Any]) -> None:
    require(ledger.get("schema_version") == LEDGER_SCHEMA, "B1E-FQ V2 ledger schema drift")
    stages = ledger.get("per_query")
    require(isinstance(stages, dict) and set(stages) == set(STAGES), "B1E-FQ V2 ledger stages drift")
    for values in stages.values():
        require(isinstance(values, dict) and set(values) == set(stage_template()), "B1E-FQ V2 ledger fields drift")
        for value in values.values():
            require(isinstance(value, (int, float)) and math.isfinite(float(value)) and value >= 0, "B1E-FQ V2 ledger value invalid")
        require(values["automatic_retries"] == 0 and values["successful_api_calls"] <= values["request_attempts"], "B1E-FQ V2 ledger call counts drift")
    reliability = ledger.get("reliability")
    require(isinstance(reliability, dict) and set(reliability) == RELIABILITY_KEYS, "B1E-FQ V2 reliability schema drift")
    require(all(type(value) is int and value >= 0 for value in reliability.values()), "B1E-FQ V2 reliability value invalid")
    require(reliability["parser_valid"] + reliability["fallback_queries"] == reliability["queries_total"], "B1E-FQ V2 parse coverage drift")


def self_test() -> dict[str, Any]:
    ledger = empty_ledger()
    validate_ledger(ledger)
    ledger["reliability"]["queries_total"] = 1
    ledger["reliability"]["fallback_queries"] = 1
    validate_ledger(ledger)
    return {"schema_version": "rq2bv1-v3-b1e-fq-parser-v2-ledger-self-test-v1", "state": "passed_zero_network", "network_calls": 0}
