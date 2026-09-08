#!/usr/bin/env python3
"""Validate condition-sharded deterministic-gzip V7 Qwen B1 output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_rq2b_v7_qwen_b1_preflight import REPRESENTATION_CELLS, file_sha256, require
from run_rq2b_v7_qwen_b1 import read_jsonl_any
from validate_rq2b_v7_runner_outputs import RunnerAuthority, validate_outputs


EXPECTED_CONDITIONS = {f"{cell}-G0" for cell in REPRESENTATION_CELLS.values()}


def validate_shards(paths: list[Path]) -> dict[str, Any]:
    require(len(paths) == 4, "Exactly four Qwen B1 shards are required")
    all_rows: list[dict[str, Any]] = []
    observed: set[str] = set()
    shard_rows: dict[str, int] = {}
    for path in paths:
        require(path.name.endswith(".jsonl.gz"), f"Expected .jsonl.gz shard: {path}")
        rows = read_jsonl_any(path)
        conditions = {str(row.get("condition_id")) for row in rows}
        require(len(conditions) == 1, f"Shard mixes condition IDs: {path}")
        condition = next(iter(conditions))
        require(condition in EXPECTED_CONDITIONS, f"Unexpected Qwen B1 condition: {condition}")
        require(condition not in observed, f"Duplicate Qwen B1 condition shard: {condition}")
        require(len(rows) == 1077, f"Qwen B1 shard row count drift: {condition}")
        observed.add(condition)
        shard_rows[condition] = len(rows)
        all_rows.extend(rows)
    require(observed == EXPECTED_CONDITIONS, "Qwen B1 shard coverage drift")
    authority = RunnerAuthority.load()
    validate_outputs(all_rows, [], authority, require_complete=False)
    return {
        "status": "PASS_FOUR_QWEN_B1_CONDITION_SHARDS",
        "conditions": sorted(observed),
        "rows": len(all_rows),
        "rows_by_condition": shard_rows,
        "compression": "gzip-mtime-0",
        "label_free_validation": True,
    }


def paths_from_manifest(path: Path) -> tuple[Path, list[Path]]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    require(manifest.get("schema_version") == "rq2b-v7-qwen-b1-run-manifest-v2", "Run manifest schema drift")
    root = Path(__file__).resolve().parents[2]
    paths: list[Path] = []
    for artifact in manifest["artifacts"]["b1_condition_shards"]:
        shard_path = root / artifact["path"]
        require(file_sha256(shard_path) == artifact["sha256"], f"Compressed shard hash drift: {shard_path}")
        paths.append(shard_path)
    return root, paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-manifest", type=Path)
    parser.add_argument("--shard", type=Path, action="append", default=[])
    args = parser.parse_args()
    require(bool(args.run_manifest) != bool(args.shard), "Provide either --run-manifest or four --shard paths")
    if args.run_manifest:
        _, paths = paths_from_manifest(args.run_manifest.resolve())
    else:
        paths = [path.resolve() for path in args.shard]
    print(json.dumps(validate_shards(paths), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
