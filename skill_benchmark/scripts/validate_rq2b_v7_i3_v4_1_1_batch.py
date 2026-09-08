#!/usr/bin/env python3
"""Validate V7 I3 V4.1 outputs with the V4.1.1 polarity correction."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import validate_rq2b_v7_i3_v4_1_batch as base


# V4.1 rejected every occurrence of the word ``unsupported`` under a positive
# use condition. V4.1.1 rejects it only when the source says that an operation,
# input, platform, or similar object is unsupported. Outcome-label enumerations
# such as "supported, partially supported, or unsupported" remain valid.
NOT_FOR_USE = re.compile(
    r"\b(?:do\s+not\s+use|don't\s+use|not\s+for|when\s+not\s+to\s+use|"
    r"must\s+not\s+use|never\s+use|cannot\s+be\s+used|can't\s+be\s+used|"
    r"does\s+not\s+support|doesn't\s+support|does\s+not\s+work|doesn't\s+work|"
    r"(?:is|are|be|remains?)\s+unsupported|"
    r"unsupported\s+(?:format|platform|input|file|task|workflow|operation|feature|case)s?)\b",
    re.I,
)

ROOT = base.ROOT
PREP = base.PREP


def validate_v4_1_1_semantics(input_row: dict, output_row: dict) -> tuple[int, int]:
    previous = base.NOT_FOR_USE
    base.NOT_FOR_USE = NOT_FOR_USE
    try:
        return base.validate_v4_1_semantics(input_row, output_row)
    finally:
        base.NOT_FOR_USE = previous


def validate(batch_id: str, output_override: Path | None = None) -> dict:
    previous = base.NOT_FOR_USE
    base.NOT_FOR_USE = NOT_FOR_USE
    try:
        result = base.validate(batch_id, output_override)
    finally:
        base.NOT_FOR_USE = previous
    result["status"] = "PASS_I3_V4_1_1_BATCH_VALIDATION"
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
