#!/usr/bin/env python3
"""Zero-network integration checks for the sealed B1E-FQ V2.1 E2E contract.

This deliberately uses synthetic parser outputs and cached candidate vectors.
It verifies local plumbing only; it is not a provider execution or retrieval
result and it never writes scientific output.
"""

from __future__ import annotations

import json
from pathlib import Path

from rq2b_common import repo_root, require
from rq2bv1_b1efq_e2e_v2_1 import (
    QUERY_FIELD_ORDER,
    _candidate_context,
    _candidate_matrices,
    _fallback_result,
    _field_aligned_result,
    _fallback_rows,
    _run_scoring,
    _serialize_query_fields,
    _strict_prompts,
    _tokenizer,
    _validate_result_row,
)
from rq2bv1_query_field_parser_v2 import validate_response


def run(root: Path) -> dict[str, int | str]:
    root = root.resolve()
    _, prompts = _strict_prompts(root)
    tokenizer, token_audit = _tokenizer(root)
    serialised = 0
    for prompt in prompts:
        raw = str(prompt["prompt"])
        # A short verbatim prefix is a deliberately minimal synthetic parser
        # answer. It exercises grounding and field serialisation without
        # claiming that this is an informative real parse.
        response = {"fields": {field: [] for field in QUERY_FIELD_ORDER}}
        response["fields"]["use_condition"] = [raw[: min(96, len(raw))]]
        parsed = validate_response(raw, response).as_dict()
        fields = _serialize_query_fields(parsed, tokenizer, token_audit)
        require(tuple(fields) == ("use_condition",), "Synthetic field serialisation drift")
        serialised += 1

    _, texts, components, cache = _candidate_context(root)
    skill_ids, matrices = _candidate_matrices(components, texts, cache)
    sample_prompt = prompts[0]
    raw = str(sample_prompt["prompt"])
    response = {"fields": {field: [] for field in QUERY_FIELD_ORDER}}
    response["fields"]["use_condition"] = [raw[: min(96, len(raw))]]
    parsed = validate_response(raw, response).as_dict()
    fields = _serialize_query_fields(parsed, tokenizer, token_audit)
    query_vector = matrices["use_condition"][0].tolist()
    ranking, _ = _run_scoring(skill_ids, matrices, fields, {"use_condition": query_vector})
    result = _field_aligned_result(
        sample_prompt,
        ranking,
        parsed=parsed,
        field_texts=fields,
        parser_seconds=0.0,
        embedding_seconds=0.0,
        alignment_seconds=0.0,
        selector_tokens=1,
    )
    _validate_result_row(result, sample_prompt)
    fallbacks, _ = _fallback_rows(root, prompts)
    fallback = _fallback_result(
        sample_prompt,
        fallbacks[str(sample_prompt["prompt_id"])],
        parser_status="fallback",
        failure_class="synthetic_transport",
        parser_seconds=0.0,
        field_embedding_status="not_attempted_parser_fallback",
    )
    _validate_result_row(fallback, sample_prompt)
    return {
        "schema_version": "rq2bv1-v3-b1e-fq-e2e-v2-1-local-integration-test-v1",
        "state": "passed_zero_network",
        "network_calls": 0,
        "strict_prompts_grounded_and_serialised": serialised,
        "candidate_vectors_loaded_local_only": len(texts),
        "pure_result_schema_validated": 1,
        "fallback_result_schema_validated": 1,
    }


def main() -> int:
    print(json.dumps(run(repo_root()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
