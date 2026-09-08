#!/usr/bin/env python3
"""Read-only progress audit for the 95 V7 I3 V4.1 extraction batches."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE
from validate_rq2b_v7_i3_v4_1_batch import ROOT, PREP, validate


def main() -> None:
    assignments = [json.loads(line) for line in (ROOT / PREP / "full_reextraction_assignment_manifest.jsonl").read_bytes().splitlines()]
    status = Counter()
    by_group: dict[str, Counter] = {str(group): Counter() for group in (1, 2, 3)}
    validated_rows = warnings = 0
    pending, invalid, selected = [], [], []
    attempts_seen = 0
    for assignment in assignments:
        batch_id = assignment["batch_id"]
        group = str(assignment["extractor_group"])
        output_path = ROOT / assignment["expected_output_path"]
        if not output_path.is_file():
            status["UNSTARTED"] += 1
            by_group[group]["UNSTARTED"] += 1
            pending.append(batch_id)
            continue
        number = batch_id.removeprefix("I3V41-")
        attempt_paths = [output_path, *sorted((ROOT / CACHE / "reissues").glob(f"i3v41_output_{number}_reissue_*.jsonl"))]
        valid_attempts, attempt_errors = [], []
        for path in attempt_paths:
            attempts_seen += 1
            match = re.fullmatch(rf"i3v41_output_{number}_reissue_(\d{{3}})\.jsonl", path.name)
            if path != output_path and match is None:
                continue
            try:
                result = validate(batch_id, path)
                valid_attempts.append((int(match.group(1)) if match else -1, path, result))
            except Exception as exc:
                attempt_errors.append({"path": str(path.relative_to(ROOT)), "error": str(exc)})
        if not valid_attempts:
            status["STARTED_INVALID"] += 1
            by_group[group]["STARTED_INVALID"] += 1
            invalid.append({"batch_id": batch_id, "attempts": attempt_errors})
            continue
        reissue_number, selected_path, result = max(valid_attempts, key=lambda value: value[0])
        status["VALIDATED"] += 1
        by_group[group]["VALIDATED"] += 1
        validated_rows += result["rows"]
        warnings += result["warnings_pending_source_only_disposition"]
        selected.append({"batch_id": batch_id, "selected_path": str(selected_path.relative_to(ROOT)), "reissue_number": None if reissue_number < 0 else reissue_number, "output_sha256": result["output_sha256"]})
    report = {
        "state": "ALL_95_VALIDATED_PENDING_MERGE_AND_QA" if status["VALIDATED"] == len(assignments) else "EXTRACTION_IN_PROGRESS",
        "counts": {"batches": len(assignments), **dict(sorted(status.items())), "validated_rows": validated_rows, "attempts_seen": attempts_seen, "warnings_pending_source_only_disposition": warnings},
        "by_extractor_group": {group: dict(sorted(counts.items())) for group, counts in by_group.items()},
        "next_pending_batch_ids": pending[:12],
        "invalid": invalid,
        "selected_valid_attempts": selected,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
