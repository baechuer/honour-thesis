#!/usr/bin/env python3
"""Create disjoint, local-only Wave 035 T0 source reading batches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BATCHES = {
    "RQ1B-V3-W35-T0-CREATIVE-PROFESSIONAL": list(range(1, 24)) + [24, 60, 61, 62, 63, 66, 67, 68],
    "RQ1B-V3-W35-T0-AUDIO": list(range(25, 36)) + [45, 46, 51, 59, 64, 65],
    "RQ1B-V3-W35-T0-IMAGE-VIDEO": list(range(36, 45)) + list(range(47, 51)) + list(range(52, 59)),
    "RQ1B-V3-W35-T0-DATA-VISION": list(range(69, 88)),
    "RQ1B-V3-W35-T0-DATA-SOFTWARE": list(range(88, 117)),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = [json.loads(line) for line in args.amendment.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_id = {row["amendment_source_id"]: row for row in rows}
    output = []
    assigned = set()
    for batch_id, numbers in BATCHES.items():
        member_ids = [f"RQ1B-V3-W35-SRC-{number:04d}" for number in numbers]
        if any(member_id not in by_id for member_id in member_ids):
            raise SystemExit(f"unknown_member_in_{batch_id}")
        if assigned & set(member_ids):
            raise SystemExit(f"non_disjoint_batch:{batch_id}")
        assigned.update(member_ids)
        output.append({
            "batch_id": batch_id,
            "status": "RQ1B_V3_W35_T0_ASSIGNED_SOURCE_READING_NOT_A_CLUSTER",
            "source_count": len(member_ids),
            "sources": [
                {
                    "source_id": member_id,
                    "local_raw_path": by_id[member_id]["canonical"]["local_raw_path"],
                    "repository_ref": by_id[member_id]["canonical"]["repository_ref"],
                    "artifact_path": by_id[member_id]["canonical"]["artifact_path"],
                }
                for member_id in member_ids
            ],
            "boundary": "Assigned local source reading only; this is not a cluster or a proposal outcome.",
        })
    if assigned != set(by_id):
        raise SystemExit(f"assignment_coverage_mismatch:{len(assigned)}:{len(by_id)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in output), encoding="utf-8")
    print(json.dumps({"status": "RQ1B_V3_W35_T0_BATCH_ASSIGNMENT_PASS_NOT_A_CLUSTER", "batch_count": len(output), "source_count": len(assigned)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
