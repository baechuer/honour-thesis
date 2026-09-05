#!/usr/bin/env python3
"""Freeze non-overlapping three-source M1 byte-stage batches for Round 32."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EXPECTED = "M1_ROUND32_BOUNDED_DIVERSE_STAGING_SELECTION_NOT_A_CLUSTER_OR_RESULT"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=3)
    args = parser.parse_args()
    if args.batch_size < 1:
        raise SystemExit("invalid_batch_size")
    selection: dict[str, Any] = json.loads(args.selection.read_text(encoding="utf-8"))
    if selection.get("status") != EXPECTED:
        raise SystemExit("unexpected_round32_selection")
    positions = sorted(int(source["plan_position"]) for source in selection.get("sources", []))
    if len(positions) != len(set(positions)):
        raise SystemExit("duplicate_source_position")
    batches = [
        {
            "batch_id": f"R32M1-B{number:02d}",
            "source_positions": positions[start:start + args.batch_size],
            "batch_status": "M1_STAGE_BATCH_DECLARED_NOT_STARTED_NOT_A_CLUSTER_OR_RESULT",
        }
        for number, start in enumerate(range(0, len(positions), args.batch_size), start=1)
    ]
    payload = {
        "status": "M1_ROUND32_NONOVERLAPPING_STAGE_PLAN_DECLARED_NOT_A_CLUSTER_OR_RESULT",
        "selection": str(args.selection),
        "batch_size": args.batch_size,
        "source_position_count": len(positions),
        "batches": batches,
        "exclusions": [
            "The plan declares only source-staging work; it is not a source admission, candidate composition, prompt, label, retrieval input, or result.",
            "Batches are source-position disjoint so concurrent byte staging cannot share a source directory.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "batch_count": len(batches), "source_position_count": len(positions)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
