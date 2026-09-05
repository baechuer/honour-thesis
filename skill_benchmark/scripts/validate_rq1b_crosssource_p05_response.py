#!/usr/bin/env python3
"""Validate exact quoted evidence in one blind P0.5 response."""

from __future__ import annotations

import json
import sys
from pathlib import Path


VALID_CODES = {
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
    "MULTI_FIELD_OR_NONCODEABLE",
}


def clause_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("quote"), str):
        return value["quote"]
    raise ValueError(f"Unsupported prompt-clause shape: {value!r}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_rq1b_crosssource_p05_response.py RESPONSE.json")
    response_path = Path(sys.argv[1])
    family_dir = response_path.parents[2] / response_path.stem
    packet_path = family_dir / "field_coding_packet.json"
    response = json.loads(response_path.read_text())
    packet = json.loads(packet_path.read_text())
    if response.get("family_id") != packet.get("family_id"):
        raise SystemExit("family_id mismatch")
    prompt_by_variant = {item["variant"]: item["text"] for item in packet["prompts"]}
    candidate_by_label = {
        item["label"]: (family_dir / item["text_path"]).read_text() for item in packet["candidates"]
    }
    failures = []
    for item in response.get("per_prompt", []):
        variant = item.get("variant")
        if variant not in prompt_by_variant:
            failures.append(f"unknown_variant:{variant}")
            continue
        if item.get("code") not in VALID_CODES:
            failures.append(f"invalid_code:{variant}:{item.get('code')}")
        for raw_clause in item.get("prompt_clauses", []):
            quote = clause_text(raw_clause)
            if quote not in prompt_by_variant[variant]:
                failures.append(f"prompt_quote_not_exact:{variant}:{quote!r}")
        evidence = item.get("candidate_evidence", {})
        for label, quotes in evidence.items():
            text = candidate_by_label.get(label)
            if text is None:
                failures.append(f"unknown_candidate:{variant}:{label}")
                continue
            for quote in quotes:
                if quote not in text:
                    failures.append(f"candidate_quote_not_exact:{variant}:{label}:{quote!r}")
    if len(response.get("per_prompt", [])) != len(prompt_by_variant):
        failures.append("prompt_variant_coverage_mismatch")
    if failures:
        print(json.dumps({"status": "P05_RESPONSE_EVIDENCE_FAIL", "failures": failures}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"status": "P05_RESPONSE_EVIDENCE_PASS", "family_id": response["family_id"]}, sort_keys=True))


if __name__ == "__main__":
    main()
