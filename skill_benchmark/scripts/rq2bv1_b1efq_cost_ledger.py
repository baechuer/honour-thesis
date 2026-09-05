#!/usr/bin/env python3
"""Zero-network cost-ledger schema for the prospective B1E-FQ condition."""

from __future__ import annotations

import argparse
import math
from typing import Any

from rq2b_common import require


LEDGER_SCHEMA = "rq2bv1-v3-b1e-fq-cost-ledger-v1"
STAGES = (
    "candidate_preparation",
    "query_parsing",
    "query_field_embedding",
    "local_selection",
    "end_to_end",
)


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
        "one_time": {"candidate_preparation": stage_template()},
        "per_query": {
            "query_parsing": stage_template(),
            "query_field_embedding": stage_template(),
            "local_selection": stage_template(),
            "end_to_end": stage_template(),
        },
        "reliability": {
            "queries_total": 0,
            "parser_valid": 0,
            "parser_schema_failures": 0,
            "parser_span_grounding_failures": 0,
            "parser_empty_field_failures": 0,
            "fallback_queries": 0,
            "active_field_count_total": 0,
        },
        "comparability": {
            "full_reproducibility_cost_includes_candidate_preparation": True,
            "incremental_run_cost_may_reuse_exact_candidate_cache": True,
            "cold_query_includes": ["query_parsing", "query_field_embedding", "local_selection"],
            "warm_query_includes": ["query_parsing", "query_field_embedding", "local_selection"],
        },
    }


def validate_ledger(ledger: dict[str, Any]) -> None:
    require(ledger.get("schema_version") == LEDGER_SCHEMA, "B1E-FQ cost ledger schema drift")
    for location, expected in (("one_time", ("candidate_preparation",)), ("per_query", STAGES[1:])):
        container = ledger.get(location)
        require(isinstance(container, dict) and set(container) == set(expected), f"B1E-FQ ledger stage drift: {location}")
        for stage in expected:
            values = container[stage]
            require(isinstance(values, dict) and set(values) == set(stage_template()), f"B1E-FQ ledger fields drift: {stage}")
            for key, value in values.items():
                require(isinstance(value, (int, float)) and math.isfinite(float(value)) and value >= 0, f"B1E-FQ ledger value invalid: {stage}.{key}")
            require(values["automatic_retries"] == 0, f"B1E-FQ ledger forbids automatic retries: {stage}")
            require(values["successful_api_calls"] <= values["request_attempts"], f"B1E-FQ successful calls exceed attempts: {stage}")

    reliability = ledger.get("reliability")
    require(isinstance(reliability, dict) and set(reliability) == {
        "queries_total", "parser_valid", "parser_schema_failures", "parser_span_grounding_failures",
        "parser_empty_field_failures", "fallback_queries", "active_field_count_total",
    }, "B1E-FQ reliability ledger drift")
    require(all(isinstance(value, int) and value >= 0 for value in reliability.values()), "B1E-FQ reliability value invalid")
    require(reliability["parser_valid"] <= reliability["queries_total"], "B1E-FQ valid parses exceed queries")
    require(reliability["fallback_queries"] <= reliability["queries_total"], "B1E-FQ fallbacks exceed queries")


def self_test() -> dict[str, Any]:
    ledger = empty_ledger()
    validate_ledger(ledger)
    invalid = empty_ledger()
    invalid["per_query"]["query_parsing"]["automatic_retries"] = 1
    try:
        validate_ledger(invalid)
    except ValueError:
        pass
    else:
        raise RuntimeError("Cost-ledger self-test failed to reject automatic retry")
    return {
        "schema_version": "rq2bv1-v3-b1e-fq-cost-ledger-self-test-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate B1E-FQ cost-ledger contract.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.self_test, "Only --self-test is implemented")
    print(self_test())


if __name__ == "__main__":
    main()
