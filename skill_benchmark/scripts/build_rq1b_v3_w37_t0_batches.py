#!/usr/bin/env python3
"""Split the Wave 037 local T0 roster into six disjoint three-triad batches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.roster.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 18:
        raise SystemExit(f"expected_18_triads:{len(rows)}")
    batches = []
    all_sources = set()
    for batch_number in range(6):
        triads = rows[batch_number * 3:(batch_number + 1) * 3]
        source_ids = [member["source_id"] for triad in triads for member in triad["members"]]
        if len(source_ids) != len(set(source_ids)):
            raise SystemExit(f"within_batch_source_reuse:{batch_number + 1}")
        if all_sources.intersection(source_ids):
            raise SystemExit(f"cross_batch_source_reuse:{batch_number + 1}")
        all_sources.update(source_ids)
        batches.append({
            "batch_id": f"RQ1B-V3-W37-T0-B{batch_number + 1:02d}",
            "status": "RQ1B_V3_W37_T0_SOURCE_ONLY_READING_ASSIGNED_NOT_A_CLUSTER",
            "triad_count": len(triads),
            "source_count": len(source_ids),
            "triads": triads,
            "boundary": triads[0]["claim_boundary"],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(batch, sort_keys=True) + "\n" for batch in batches), encoding="utf-8")
    print(json.dumps({"status": "RQ1B_V3_W37_T0_BATCH_ASSIGNMENT_PASS_NOT_A_CLUSTER", "batch_count": len(batches), "source_count": len(all_sources)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
