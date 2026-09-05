#!/usr/bin/env python3
"""Prepare full SkillRouter-Eval-Core I3C V2 extraction chunks.

This keeps the full-library I3C extraction resumable and avoids re-parsing
skills that already passed the I3C V2 top-20 pool QA gate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


FIELDS = [
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "constraints_boundaries",
    "dependencies_resources",
    "success_criteria",
]


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all-i2",
        type=Path,
        default=Path(
            "skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl"
        ),
    )
    parser.add_argument(
        "--seed-i3c",
        type=Path,
        default=Path(
            "skill_benchmark/external/skillrouter_eval_core/derived/representations/"
            "i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl"
        ),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(
            "skill_benchmark/external/skillrouter_eval_core/derived/representations/"
            "i3c_v2_full_all"
        ),
    )
    parser.add_argument("--chunk-size", type=int, default=100)
    args = parser.parse_args()

    all_rows = read_jsonl(args.all_i2)
    seed_rows = read_jsonl(args.seed_i3c) if args.seed_i3c.exists() else []

    all_ids = [row["skill_id"] for row in all_rows]
    counts = {}
    for sid in all_ids:
        counts[sid] = counts.get(sid, 0) + 1
    duplicate_all_ids = sorted(sid for sid, count in counts.items() if count > 1)
    if duplicate_all_ids:
        raise SystemExit(f"Duplicate skill_id values in all_I2: {duplicate_all_ids[:10]}")

    all_id_set = set(all_ids)
    seed_by_id = {row["skill_id"]: row for row in seed_rows}
    seed_ids_in_all = sorted(set(seed_by_id) & all_id_set)
    seed_ids_not_in_all = sorted(set(seed_by_id) - all_id_set)

    missing_rows: list[dict] = []
    for source_index, row in enumerate(all_rows):
        if row["skill_id"] in seed_by_id:
            continue
        chunk_row = dict(row)
        chunk_row["source_row_index"] = source_index
        chunk_row["i3c_full_extraction_status"] = "missing_from_seed"
        missing_rows.append(chunk_row)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    input_dir = args.out_dir / "inputs"
    output_dir = args.out_dir / "outputs"
    cached_dir = args.out_dir / "cached"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    cached_dir.mkdir(parents=True, exist_ok=True)

    seeded_rows: list[dict] = []
    for row in all_rows:
        cached = seed_by_id.get(row["skill_id"])
        if cached:
            cached_row = dict(cached)
            cached_row["i3c_full_extraction_status"] = "seeded_from_top20_cleaned"
            seeded_rows.append(cached_row)
    seed_cache_path = cached_dir / "I3C_V2_full_all_seed_top20_cleaned.jsonl"
    write_jsonl(seed_cache_path, seeded_rows)

    chunk_records = []
    for chunk_number, start in enumerate(range(0, len(missing_rows), args.chunk_size)):
        chunk = missing_rows[start : start + args.chunk_size]
        end = start + len(chunk) - 1
        input_path = input_dir / f"i3c_v2_full_missing_input_{start:05d}_{end:05d}.jsonl"
        output_path = output_dir / f"i3c_v2_full_missing_output_{start:05d}_{end:05d}.jsonl"
        write_jsonl(input_path, chunk)
        chunk_records.append(
            {
                "chunk_number": chunk_number,
                "start_missing_index": start,
                "end_missing_index": end,
                "row_count": len(chunk),
                "input_jsonl": str(input_path),
                "output_jsonl": str(output_path),
            }
        )

    manifest = {
        "schema_version": "I3C_V2_FULL_ALL_EXTRACTION_MANIFEST_V1",
        "source_all_i2": str(args.all_i2),
        "seed_i3c": str(args.seed_i3c),
        "seed_cache_jsonl": str(seed_cache_path),
        "out_dir": str(args.out_dir),
        "chunk_size": args.chunk_size,
        "total_all_i2_rows": len(all_rows),
        "seed_rows_input": len(seed_rows),
        "seed_rows_in_all_i2": len(seed_ids_in_all),
        "seed_rows_not_in_all_i2": len(seed_ids_not_in_all),
        "remaining_rows_to_extract": len(missing_rows),
        "missing_chunk_count": len(chunk_records),
        "fields": FIELDS,
        "prompt": "skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md",
        "notes": [
            "Do not mix older I3M/I3C slices into this V2 full-all extraction.",
            "The cleaned top-20 task-relevant pool is reused because it already passed I3C V2 QA.",
            "Outputs should be merged with the seed cache only after all missing chunks pass validation.",
        ],
        "chunks": chunk_records,
    }
    manifest_path = args.out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in manifest if k != "chunks"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
