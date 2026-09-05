#!/usr/bin/env python3
"""Zero-network contract for B1E-FQ query-to-I3C-field parsing.

The future provider adapter may classify only verbatim character spans from a
raw routing request. This module freezes its JSON contract and rejects output
that invents, overlaps, or misquotes query text. It intentionally contains no
network client or credential handling.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

from rq2b_common import require, sha256_json, sha256_text


PARSER_CONTRACT_VERSION = "rq2bv1-v3-b1e-fq-span-parser-v1"
PARSER_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
PARSER_MODEL = "qwen3.7-plus-2026-05-26"
PARSER_MODE = "non_thinking_json_object"
PARSER_TEMPERATURE = 0
PARSER_MAX_OUTPUT_TOKENS = 512
PARSER_ENABLE_THINKING = False
FIELD_ORDER = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "dependency_resource",
    "boundary_not_for",
    "success_verification",
)

SYSTEM_PROMPT = """You are a span-grounded routing-request parser. Return JSON only.
Classify only exact, verbatim character spans from the user's request into the
seven provided fields. Do not paraphrase, infer missing requirements, add
synonyms, invent steps, name a skill, mention a candidate, or use any outside
knowledge. A field with no directly evidenced span must be an empty list.

Return this exact JSON object shape:
{"fields":{"use_condition":[],"input_precondition":[],"output_artifact":[],"workflow_procedure":[],"dependency_resource":[],"boundary_not_for":[],"success_verification":[]}}

Each list item must be {"start":integer,"end":integer,"text":"exact substring"}.
Offsets are zero-based, end-exclusive character offsets into the original user
request. A span may appear in only one field. JSON is required."""


@dataclass(frozen=True)
class ValidatedParse:
    query_sha256: str
    parser_contract_sha256: str
    fields: dict[str, tuple[dict[str, Any], ...]]

    @property
    def active_fields(self) -> tuple[str, ...]:
        return tuple(field for field in FIELD_ORDER if self.fields[field])

    def embedding_texts(self) -> dict[str, str]:
        """Return per-field query text made only of verified source spans."""
        return {
            field: "\n".join(str(span["text"]) for span in self.fields[field])
            for field in self.active_fields
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": PARSER_CONTRACT_VERSION,
            "query_sha256": self.query_sha256,
            "parser_contract_sha256": self.parser_contract_sha256,
            "active_fields": list(self.active_fields),
            "fields": {field: list(self.fields[field]) for field in FIELD_ORDER},
            "query_field_text_sha256": {
                field: sha256_text(text) for field, text in self.embedding_texts().items()
            },
        }


def parser_contract() -> dict[str, Any]:
    return {
        "schema_version": PARSER_CONTRACT_VERSION,
        "base_url": PARSER_BASE_URL,
        "model": PARSER_MODEL,
        "mode": PARSER_MODE,
        "temperature": PARSER_TEMPERATURE,
        "max_output_tokens": PARSER_MAX_OUTPUT_TOKENS,
        "enable_thinking": PARSER_ENABLE_THINKING,
        "response_format": {"type": "json_object"},
        "field_order": list(FIELD_ORDER),
        "system_prompt": SYSTEM_PROMPT,
        "span_policy": "verbatim_zero_based_end_exclusive_non_overlapping_single_field_only",
        "fallback_policy": "not_frozen",
    }


def parser_contract_sha256() -> str:
    return sha256_json(parser_contract())


def request_payload(raw_query: str) -> dict[str, Any]:
    require(bool(raw_query), "Raw query must be non-empty")
    return {
        "model": PARSER_MODEL,
        "temperature": PARSER_TEMPERATURE,
        "enable_thinking": PARSER_ENABLE_THINKING,
        "max_tokens": PARSER_MAX_OUTPUT_TOKENS,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_query},
        ],
    }


def validate_response(raw_query: str, payload: Any) -> ValidatedParse:
    require(isinstance(payload, dict), "Parser response must be a JSON object")
    require(set(payload) == {"fields"}, "Parser response must contain only fields")
    by_field = payload["fields"]
    require(isinstance(by_field, dict) and set(by_field) == set(FIELD_ORDER), "Parser fields drift")

    occupied: list[tuple[int, int]] = []
    normalized: dict[str, tuple[dict[str, Any], ...]] = {}
    for field in FIELD_ORDER:
        spans = by_field[field]
        require(isinstance(spans, list), f"Parser field is not a list: {field}")
        current: list[dict[str, Any]] = []
        previous_end = -1
        for span in spans:
            require(isinstance(span, dict) and set(span) == {"start", "end", "text"}, f"Parser span shape drift: {field}")
            start, end, text = span["start"], span["end"], span["text"]
            require(type(start) is int and type(end) is int and isinstance(text, str), f"Parser span type drift: {field}")
            require(0 <= start < end <= len(raw_query), f"Parser span offsets invalid: {field}")
            require(start >= previous_end, f"Parser spans are not ordered: {field}")
            require(raw_query[start:end] == text, f"Parser span is not verbatim: {field}")
            require(all(end <= other_start or start >= other_end for other_start, other_end in occupied), "Parser spans overlap across fields")
            current.append({"start": start, "end": end, "text": text})
            occupied.append((start, end))
            previous_end = end
        normalized[field] = tuple(current)

    validated = ValidatedParse(
        query_sha256=sha256_text(raw_query),
        parser_contract_sha256=parser_contract_sha256(),
        fields=normalized,
    )
    require(bool(validated.active_fields), "Parser response has no active fields")
    return validated


def _blank_fields() -> dict[str, list[dict[str, Any]]]:
    return {field: [] for field in FIELD_ORDER}


def self_test() -> dict[str, Any]:
    query = "Convert scanned invoices into page-anchored JSON. Do not use cloud OCR services."
    fields = _blank_fields()
    for field, text in (
        ("input_precondition", "scanned invoices"),
        ("output_artifact", "page-anchored JSON"),
        ("boundary_not_for", "Do not use cloud OCR services"),
    ):
        start = query.index(text)
        fields[field].append({"start": start, "end": start + len(text), "text": text})
    parsed = validate_response(query, {"fields": fields})
    require(parsed.active_fields == ("input_precondition", "output_artifact", "boundary_not_for"), "Parser active fields self-test failed")
    require(parsed.embedding_texts()["output_artifact"] == "page-anchored JSON", "Parser field text self-test failed")

    invented = _blank_fields()
    invented["output_artifact"].append({"start": 0, "end": 7, "text": "CSV file"})
    try:
        validate_response(query, {"fields": invented})
    except ValueError:
        pass
    else:
        raise RuntimeError("Parser self-test failed to reject invented text")

    overlap = _blank_fields()
    start = query.index("scanned invoices")
    overlap["input_precondition"].append({"start": start, "end": start + 7, "text": "scanned"})
    overlap["use_condition"].append({"start": start, "end": start + len("scanned invoices"), "text": "scanned invoices"})
    try:
        validate_response(query, {"fields": overlap})
    except ValueError:
        pass
    else:
        raise RuntimeError("Parser self-test failed to reject overlap")

    try:
        validate_response(query, {"fields": _blank_fields()})
    except ValueError:
        pass
    else:
        raise RuntimeError("Parser self-test failed to reject empty extraction")

    boolean_offset = _blank_fields()
    boolean_offset["input_precondition"].append({"start": True, "end": 2, "text": "on"})
    try:
        validate_response(query, {"fields": boolean_offset})
    except ValueError:
        pass
    else:
        raise RuntimeError("Parser self-test failed to reject boolean offsets")

    return {
        "schema_version": "rq2bv1-v3-b1e-fq-span-parser-self-test-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
        "parser_contract_sha256": parser_contract_sha256(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the zero-network B1E-FQ parser contract.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.self_test, "Only --self-test is implemented; no provider call is available in this module")
    print(self_test())


if __name__ == "__main__":
    main()
