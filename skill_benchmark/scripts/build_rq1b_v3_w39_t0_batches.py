#!/usr/bin/env python3
"""Split a Wave 039 source-only T0 roster into disjoint review batches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--triads-per-batch", type=int, default=3)
    args = parser.parse_args()
    if args.triads_per_batch <= 0:
        raise SystemExit("triads_per_batch_must_be_positive")
    rows = [json.loads(line) for line in args.roster.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise SystemExit("empty_t0_roster")
    all_sources: set[str] = set()
    batches = []
    for offset in range(0, len(rows), args.triads_per_batch):
        triads = rows[offset:offset + args.triads_per_batch]
        source_ids = [member["source_id"] for triad in triads for member in triad["members"]]
        if len(source_ids) != len(set(source_ids)):
            raise SystemExit(f"within_batch_source_reuse:{offset // args.triads_per_batch + 1}")
        if all_sources.intersection(source_ids):
            raise SystemExit(f"cross_batch_source_reuse:{offset // args.triads_per_batch + 1}")
        all_sources.update(source_ids)
        batches.append({
            "batch_id": f"RQ1B-V3-W39-T0-B{offset // args.triads_per_batch + 1:02d}",
            "status": "RQ1B_V3_W39_T0_SOURCE_ONLY_READING_ASSIGNED_NOT_A_CLUSTER",
            "triad_count": len(triads),
            "source_count": len(source_ids),
            "triads": triads,
            "boundary": triads[0]["claim_boundary"],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(batch, sort_keys=True) + "\n" for batch in batches), encoding="utf-8")
    print(json.dumps({
        "status": "RQ1B_V3_W39_T0_BATCH_ASSIGNMENT_PASS_NOT_A_CLUSTER",
        "batch_count": len(batches),
        "source_count": len(all_sources),
        "triad_count": len(rows),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
