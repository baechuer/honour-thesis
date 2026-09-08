#!/usr/bin/env python3
"""Read-only progress audit for the 95 V7 I3 V4 extraction batches."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from validate_rq2b_v7_i3_v4_batch import ROOT, PREP, validate


def main() -> None:
    assignments = [json.loads(line) for line in (ROOT / PREP / "full_reextraction_assignment_manifest.jsonl").read_bytes().splitlines()]
    status = Counter()
    by_group: dict[str, Counter] = {str(group): Counter() for group in (1, 2, 3)}
    validated_rows = warnings = 0
    pending, invalid = [], []
    for assignment in assignments:
        batch_id = assignment["batch_id"]
        group = str(assignment["extractor_group"])
        output_path = ROOT / assignment["expected_output_path"]
        if not output_path.is_file():
            status["UNSTARTED"] += 1
            by_group[group]["UNSTARTED"] += 1
            pending.append(batch_id)
            continue
        try:
            result = validate(batch_id)
        except Exception as exc:  # the exact message is useful for a traceable reissue
            status["STARTED_INVALID"] += 1
            by_group[group]["STARTED_INVALID"] += 1
            invalid.append({"batch_id": batch_id, "error": str(exc), "output_path": assignment["expected_output_path"]})
            continue
        status["VALIDATED"] += 1
        by_group[group]["VALIDATED"] += 1
        validated_rows += result["rows"]
        warnings += result["warnings_pending_source_only_disposition"]
    report = {
        "state": "ALL_95_VALIDATED_PENDING_MERGE_AND_QA" if status["VALIDATED"] == len(assignments) else "EXTRACTION_IN_PROGRESS",
        "counts": {"batches": len(assignments), **dict(sorted(status.items())), "validated_rows": validated_rows, "warnings_pending_source_only_disposition": warnings},
        "by_extractor_group": {group: dict(sorted(counts.items())) for group, counts in by_group.items()},
        "next_pending_batch_ids": pending[:12],
        "invalid": invalid,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
