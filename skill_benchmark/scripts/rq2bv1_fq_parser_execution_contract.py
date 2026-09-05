#!/usr/bin/env python3
"""Hash-bound runtime constants for the separately authorised B1E-FQ FQ-P stage.

This module deliberately has no dependency on preflight construction or B1L
validation. The parser runner imports only this sealed runtime contract plus
the parser, ledger, verifier and common utilities listed in its packet.
"""

from __future__ import annotations

from rq2bv1_query_field_parser import parser_contract


PREFLIGHT_ROOT = "skill_benchmark/rq2bv1/preflight/qwen_field_aligned_v3_parser"
INVENTORY_NAME = "parser_request_inventory.jsonl"
PAYLOAD_NAME = "payload_manifest.json"
REPORT_NAME = "preflight_report.json"
CHECKPOINT_NAME = "preflight_checkpoint.json"
PACKET_NAME = "execution_approval_packet.json"
RUN_ID = "rq2bv1-v3-qwen-field-aligned-parser-002"
RESULT_ROOT = "skill_benchmark/rq2bv1/results/qwen_field_aligned_v3_parser"
CACHE_ROOT = "skill_benchmark/cache/rq2bv1/query_parses"
AUTHORISATION_CONSUMPTION_ROOT = "skill_benchmark/rq2bv1/approvals/consumed"
TIMEOUT_SECONDS = 120
PARSER_INPUT_OVERHEAD_TOKEN_UPPER_BOUND = 512
PARSER_PRICE_DATE = "2026-08-22"
PARSER_PRICE_SOURCE_URL = "https://www.alibabacloud.com/help/en/model-studio/model-pricing"
PARSER_INPUT_USD_PER_MILLION_TOKENS = 0.40
PARSER_OUTPUT_USD_PER_MILLION_TOKENS = 1.60


def provider_input_token_upper_bound(raw_query: str) -> int:
    """Conservative byte-based bound for one fixed-system-plus-raw-query call."""
    return len(parser_contract()["system_prompt"].encode("utf-8")) + len(raw_query.encode("utf-8")) + PARSER_INPUT_OVERHEAD_TOKEN_UPPER_BOUND
