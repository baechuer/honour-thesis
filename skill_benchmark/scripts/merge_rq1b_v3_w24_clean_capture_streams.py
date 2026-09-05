#!/usr/bin/env python3
"""Merge only integrity-cleared W24 capture streams for source deduplication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line:
            item = json.loads(line)
            if not isinstance(item, dict):
                raise SystemExit(f"jsonl_row_not_object:{path}:{number}")
            values.append(item)
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--single-attempt-manifest", type=Path, required=True)
    parser.add_argument("--never-attempted-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--expected-status", required=True)
    args = parser.parse_args()

    streams = [
        ("INCIDENT_SINGLE_ATTEMPT", read_jsonl(args.single_attempt_manifest)),
        ("NEVER_ATTEMPTED_ONE_SHOT", read_jsonl(args.never_attempted_manifest)),
    ]
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for stream_name, records in streams:
        for record in records:
            url = record.get("raw_artifact_url")
            if not isinstance(url, str) or not url or url in seen:
                raise SystemExit(f"invalid_or_duplicate_url:{stream_name}:{url}")
            if record.get("status") != args.expected_status:
                raise SystemExit(f"unexpected_status:{stream_name}:{url}:{record.get('status')}")
            seen.add(url)
            merged.append(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in merged), encoding="utf-8")
    summary = {
        "status": "RQ1B_V3_W24_CLEAN_CAPTURE_STREAMS_MERGED_NOT_A_SOURCE_OR_CLUSTER",
        "expected_status": args.expected_status,
        "incident_single_attempt_record_count": len(streams[0][1]),
        "never_attempted_one_shot_record_count": len(streams[1][1]),
        "merged_unique_one_attempt_url_count": len(merged),
        "boundary": [
            "The raw concurrent manifest remains preserved separately and is not rewritten.",
            "This merged manifest contains only URLs verified as exactly one attempt across the incident audit or newly attempted once in a separate stream.",
            "Duplicate-attempt URLs remain quarantined and cannot be admitted by this merged manifest.",
            "This is capture-integrity consolidation only, not source admission, D1/C1 eligibility, a cluster, prompt, label, selector, metric or result.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
