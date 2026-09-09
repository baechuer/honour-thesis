#!/usr/bin/env python3
"""Validate V7 I3 V4.1 repair outputs with source-bounded warning evidence.

V4.1.2 changes only the warning-evidence envelope.  The extraction prompt
already permits an empty string or an exact source substring, while the shared
legacy merger imposed an unrelated 500-character cap.  Under this amendment a
warning citation may be any exact contiguous substring of the same frozen
source.  Warning messages remain capped at 500 characters and all V4.1.1
field, polarity, identity and schema checks remain in force.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import merge_rq2b_i3c as shared
import validate_rq2b_v7_i3_v4_1_1_batch as previous


ROOT = previous.ROOT
PREP = previous.PREP


def validate_warning_v4_1_2(
    warning: dict[str, Any],
    *,
    expected_keys: set[str],
    source_text: str,
    path: str,
) -> None:
    """Apply the legacy warning schema without its arbitrary evidence cap."""
    shared.require(isinstance(warning, dict), f"I3C warning must be an object: {path}")
    shared.require(set(warning) == expected_keys, f"I3C warning key mismatch: {path}")
    code = warning["code"]
    message = warning["message"]
    evidence = warning["evidence"]
    shared.require(
        isinstance(code, str) and shared.WARNING_CODE_RE.fullmatch(code) is not None,
        f"Invalid I3C warning code: {path}",
    )
    shared.require(
        isinstance(message, str) and 0 < len(message) <= 500,
        f"Invalid I3C warning message: {path}",
    )
    shared.require(isinstance(evidence, str), f"Invalid I3C warning evidence: {path}")
    shared.require(
        not evidence or evidence in source_text,
        f"Non-substring I3C warning evidence: {path}",
    )
    if "field" in expected_keys:
        field = warning["field"]
        shared.require(
            isinstance(field, str) and (field == "" or field in shared.FIELD_KEYS),
            f"Invalid I3C warning field: {path}",
        )


def canonical_extraction_v4_1_2(input_row: dict, output_row: dict):
    original = shared.validate_warning
    shared.validate_warning = validate_warning_v4_1_2
    try:
        return shared.canonical_extraction(input_row, output_row)
    finally:
        shared.validate_warning = original


def validate_v4_1_2_semantics(input_row: dict, output_row: dict) -> tuple[int, int]:
    return previous.validate_v4_1_1_semantics(input_row, output_row)


def validate(batch_id: str, output_override: Path | None = None) -> dict:
    original = shared.validate_warning
    shared.validate_warning = validate_warning_v4_1_2
    try:
        result = previous.validate(batch_id, output_override)
    finally:
        shared.validate_warning = original
    result["status"] = "PASS_I3_V4_1_2_BATCH_VALIDATION"
    result["warning_evidence_contract"] = "EMPTY_OR_EXACT_FROZEN_SOURCE_SUBSTRING"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_id")
    parser.add_argument("--output-path", type=Path)
    args = parser.parse_args()
    if re.fullmatch(r"I3V41-\d{3}", args.batch_id) is None:
        parser.error("batch_id must be I3V41-NNN")
    print(json.dumps(validate(args.batch_id, args.output_path), sort_keys=True))


if __name__ == "__main__":
    main()
