#!/usr/bin/env python3
"""Read-only validation of one prepared V7 I3 fresh-extraction batch."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from merge_rq2b_i3c import canonical_extraction

ROOT = Path(__file__).resolve().parents[2]
PREP = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_extraction_2026_09_08_v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_id")
    args = parser.parse_args()
    if re.fullmatch(r"I3-\d{3}", args.batch_id) is None:
        parser.error("batch_id must be I3-NNN")
    manifest = rows(PREP / "fresh_assignment_manifest.jsonl")
    matches = [row for row in manifest if row["batch_id"] == args.batch_id]
    if len(matches) != 1:
        raise ValueError("unknown or duplicated batch ID")
    assignment = matches[0]
    input_path, output_path = ROOT / assignment["input_path"], ROOT / assignment["expected_output_path"]
    if sha(input_path) != assignment["input_sha256"]:
        raise ValueError("input hash mismatch")
    if not output_path.is_file():
        raise ValueError("output missing")
    inputs, outputs = rows(input_path), rows(output_path)
    if len(inputs) != assignment["row_count"] or len(outputs) != len(inputs):
        raise ValueError("input/output row coverage mismatch")
    for input_row, output_row in zip(inputs, outputs, strict=True):
        canonical_extraction(input_row, output_row)
    if [r["source_row_index"] for r in inputs] != sorted(r["source_row_index"] for r in inputs):
        raise ValueError("input order drift")
    print(json.dumps({"status": "PASS_I3_BATCH_VALIDATION", "batch_id": args.batch_id,
                      "rows": len(outputs), "output_path": assignment["expected_output_path"],
                      "output_sha256": sha(output_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
