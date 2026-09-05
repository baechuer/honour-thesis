#!/usr/bin/env python3
"""Validate one completed RQ2b I3C worker chunk without merging or scoring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from merge_rq2b_i3c import canonical_extraction, is_heading_only


DEFAULT_MANIFEST = Path(
    "skill_benchmark/rq2b_full_library/rq2b-full-library-v1-2026-08-02/"
    "i3c_extraction/manifest.json"
)


def read_strict_jsonl(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8")
    if not raw.endswith("\n"):
        raise ValueError(f"JSONL file must end in newline: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"Blank JSONL line {line_number}: {path}")
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL line {line_number} is not an object: {path}")
        rows.append(value)
    return rows


def validate_chunk(root: Path, manifest_path: Path, chunk_index: int) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    chunks = {int(chunk["chunk_index"]): chunk for chunk in manifest["chunks"]}
    if chunk_index not in chunks:
        raise ValueError(f"Unknown chunk index: {chunk_index}")
    chunk = chunks[chunk_index]
    input_path = root / chunk["input_path"]
    output_path = root / chunk["expected_output_path"]
    if not output_path.is_file():
        raise ValueError(f"Worker output is missing: {output_path}")

    inputs = read_strict_jsonl(input_path)
    outputs = read_strict_jsonl(output_path)
    if len(inputs) != chunk["row_count"] or len(outputs) != chunk["row_count"]:
        raise ValueError(
            f"Row-count mismatch for chunk {chunk_index}: "
            f"expected {chunk['row_count']}, input {len(inputs)}, output {len(outputs)}"
        )
    expected_source_indices = list(range(chunk["first_source_row_index"], chunk["last_source_row_index"] + 1))
    source_indices = [row.get("source_row_index") for row in inputs]
    if source_indices != expected_source_indices:
        raise ValueError(f"Input source_row_index order drift for chunk {chunk_index}")
    skill_ids = [row.get("skill_id") for row in inputs]
    if len(skill_ids) != len(set(skill_ids)) or any(not isinstance(skill_id, str) or not skill_id for skill_id in skill_ids):
        raise ValueError(f"Input skill_id coverage/uniqueness failure for chunk {chunk_index}")

    heading_only_items = 0
    for input_row, output_row in zip(inputs, outputs, strict=True):
        canonical_extraction(input_row, output_row)
        for field_items in output_row["fields"].values():
            for item in field_items:
                if is_heading_only(input_row["text"], item["evidence"]):
                    heading_only_items += 1
    if heading_only_items:
        raise ValueError(f"Heading-only evidence found in chunk {chunk_index}: {heading_only_items}")

    return {
        "chunk_index": chunk_index,
        "input_path": chunk["input_path"],
        "output_path": chunk["expected_output_path"],
        "rows": len(outputs),
        "jsonl_parse_failures": 0,
        "identity_alignment_failures": 0,
        "evidence_substring_failures": 0,
        "heading_only_evidence_items": 0,
        "duplicate_skill_id_failures": 0,
        "missing_skill_id_failures": 0,
        "state": "validated_chunk_automatic_gates_passed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-index", type=int, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
    print(json.dumps(validate_chunk(root, manifest, args.chunk_index), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
