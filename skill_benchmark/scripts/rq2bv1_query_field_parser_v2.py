#!/usr/bin/env python3
"""Zero-network V2.1 contract for grounded B1E-FQ query parsing.

V1 asked the provider to calculate character offsets as well as quote request
text. The observed provider output quoted useful text but frequently miscounted
offsets. This contract keeps the evidence requirement while assigning offsets
to a deterministic local aligner: the provider returns only exact substrings,
and the validator confirms each occurs in the raw request. Repeated occurrences
and cross-field reuse are legitimate grounding cases, not parser failures.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

from rq2b_common import require, sha256_json, sha256_text


PARSER_CONTRACT_VERSION = "rq2bv1-v3-b1e-fq-span-parser-v2-1-grounded-text-only"
PARSER_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
PARSER_MODEL = "qwen3.7-plus-2026-05-26"
PARSER_MODE = "non_thinking_json_object"
PARSER_TEMPERATURE = 0
PARSER_MAX_OUTPUT_TOKENS = 768
PARSER_ENABLE_THINKING = False
MAX_TOTAL_EXCERPTS = 14
MAX_TOTAL_EXCERPT_CHARS = 1200
FIELD_ORDER = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "dependency_resource",
    "boundary_not_for",
    "success_verification",
)

SYSTEM_PROMPT = """You are a grounded routing-request parser. Return JSON only.
For each field, quote only exact, verbatim substrings from the user's request.
Do not paraphrase, infer missing requirements, add synonyms, invent steps, name
a skill, mention a candidate, or use outside knowledge. Do not calculate
character offsets. A field with no directly evidenced substring must be an empty
list. Prefer the shortest informative phrase rather than a generic single word.
The same exact phrase may appear in more than one field when it genuinely
evidences both. A phrase may also occur more than once in the request.

Return this exact JSON object shape:
{"fields":{"use_condition":[],"input_precondition":[],"output_artifact":[],"workflow_procedure":[],"dependency_resource":[],"boundary_not_for":[],"success_verification":[]}}

Every non-empty list item must be one exact substring as a JSON string. The
substring must appear verbatim in the original user request. Keep the response
concise: at most 14 non-empty strings and at most 1200 characters across all
strings. JSON is required."""


@dataclass(frozen=True)
class ValidatedParse:
    query_sha256: str
    parser_contract_sha256: str
    fields: dict[str, tuple[dict[str, Any], ...]]

    @property
    def active_fields(self) -> tuple[str, ...]:
        return tuple(field for field in FIELD_ORDER if self.fields[field])

    def embedding_texts(self) -> dict[str, str]:
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
        "span_policy": "provider_exact_text_only_local_grounded_alignment_with_repeated_and_cross_field_text_allowed",
        "max_total_excerpts": MAX_TOTAL_EXCERPTS,
        "max_total_excerpt_chars": MAX_TOTAL_EXCERPT_CHARS,
        "fallback_policy": "completed_qwen_i3c_single_vector_ranking_for_unvalidated_parses",
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


def _field_texts(payload: Any) -> dict[str, list[str]]:
    require(isinstance(payload, dict) and set(payload) == {"fields"}, "Parser response must contain only fields")
    fields = payload["fields"]
    require(isinstance(fields, dict) and set(fields) == set(FIELD_ORDER), "Parser fields drift")
    normalized: dict[str, list[str]] = {}
    total_excerpts = 0
    total_chars = 0
    for field in FIELD_ORDER:
        texts = fields[field]
        require(isinstance(texts, list) and all(isinstance(text, str) and bool(text) for text in texts), f"Parser text-list drift: {field}")
        # Repeated identical excerpts within one field carry no additional
        # embedding evidence, so canonicalise them locally without changing
        # cross-field evidence.
        unique_texts = list(dict.fromkeys(texts))
        normalized[field] = unique_texts
        total_excerpts += len(unique_texts)
        total_chars += sum(len(text) for text in unique_texts)
    require(total_excerpts <= MAX_TOTAL_EXCERPTS, "Parser excerpt-count limit exceeded")
    require(total_chars <= MAX_TOTAL_EXCERPT_CHARS, "Parser excerpt-character limit exceeded")
    return normalized


def _first_grounded_start(raw_query: str, text: str) -> tuple[int, int]:
    """Return a deterministic audit location while preserving text-level evidence.

    The downstream embedding uses ``text``, not the character position. A
    phrase repeated in a request, or used for two related fields, is therefore
    still fully grounded. We retain the first position and occurrence count for
    audit only.
    """
    first = raw_query.find(text)
    require(first >= 0, "Parser text is absent from raw request")
    count = raw_query.count(text)
    return first, count


def validate_response(raw_query: str, payload: Any) -> ValidatedParse:
    texts_by_field = _field_texts(payload)
    normalized: dict[str, tuple[dict[str, Any], ...]] = {}
    for field in FIELD_ORDER:
        current: list[dict[str, Any]] = []
        for text in texts_by_field[field]:
            start, occurrence_count = _first_grounded_start(raw_query, text)
            end = start + len(text)
            current.append({"start": start, "end": end, "text": text, "occurrence_count": occurrence_count})
        normalized[field] = tuple(current)
    parsed = ValidatedParse(
        query_sha256=sha256_text(raw_query),
        parser_contract_sha256=parser_contract_sha256(),
        fields=normalized,
    )
    require(bool(parsed.active_fields), "Parser response has no active fields")
    return parsed


def legacy_v1_text_only(payload: Any) -> dict[str, Any]:
    """Discard V1 offsets but retain only its quoted field texts for V2 alignment."""
    require(isinstance(payload, dict) and set(payload) == {"fields"}, "Legacy parser response must contain only fields")
    fields = payload["fields"]
    require(isinstance(fields, dict) and set(fields) == set(FIELD_ORDER), "Legacy parser fields drift")
    converted: dict[str, list[str]] = {}
    for field in FIELD_ORDER:
        spans = fields[field]
        require(isinstance(spans, list), f"Legacy parser field is not a list: {field}")
        texts: list[str] = []
        for span in spans:
            require(isinstance(span, dict) and set(span) == {"start", "end", "text"}, f"Legacy parser span drift: {field}")
            text = span["text"]
            require(isinstance(text, str) and bool(text), f"Legacy parser text drift: {field}")
            texts.append(text)
        converted[field] = texts
    return {"fields": converted}


def validate_legacy_v1_response(raw_query: str, payload: Any) -> ValidatedParse:
    return validate_response(raw_query, legacy_v1_text_only(payload))


def self_test() -> dict[str, Any]:
    query = "Convert scanned invoices into page-anchored JSON. Do not use cloud OCR services."
    payload = {"fields": {field: [] for field in FIELD_ORDER}}
    payload["fields"]["input_precondition"] = ["scanned invoices"]
    payload["fields"]["output_artifact"] = ["page-anchored JSON"]
    payload["fields"]["boundary_not_for"] = ["Do not use cloud OCR services"]
    parsed = validate_response(query, payload)
    require(parsed.active_fields == ("input_precondition", "output_artifact", "boundary_not_for"), "V2 parser field self-test failed")
    require(parsed.fields["input_precondition"][0] == {"start": 8, "end": 24, "text": "scanned invoices", "occurrence_count": 1}, "V2 parser local alignment drift")

    duplicate = {"fields": {field: [] for field in FIELD_ORDER}}
    duplicate["fields"]["use_condition"] = ["PDF"]
    duplicate["fields"]["input_precondition"] = ["PDF"]
    repeated = validate_response("PDF to PDF conversion", duplicate)
    require(repeated.fields["use_condition"][0]["occurrence_count"] == 2, "V2 parser repeated-text grounding drift")
    require(repeated.fields["input_precondition"][0]["start"] == 0, "V2 parser cross-field grounding drift")

    invented = {"fields": {field: [] for field in FIELD_ORDER}}
    invented["fields"]["input_precondition"] = ["DOCX"]
    try:
        validate_response("PDF conversion", invented)
    except ValueError:
        pass
    else:
        raise RuntimeError("V2 parser self-test failed to reject ungrounded text")

    legacy = {"fields": {field: [] for field in FIELD_ORDER}}
    legacy["fields"]["input_precondition"] = [{"start": 999, "end": 1000, "text": "scanned invoices"}]
    recovered = validate_legacy_v1_response(query, legacy)
    require(recovered.fields["input_precondition"][0]["start"] == 8, "V2 legacy offset recovery drift")
    return {
        "schema_version": "rq2bv1-v3-b1e-fq-span-parser-v2-self-test-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
        "parser_contract_sha256": parser_contract_sha256(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the zero-network B1E-FQ V2 parser contract.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.self_test, "Only --self-test is implemented; no provider call is available in this module")
    print(self_test())


if __name__ == "__main__":
    main()
