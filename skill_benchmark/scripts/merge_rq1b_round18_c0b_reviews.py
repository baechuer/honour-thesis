#!/usr/bin/env python3
"""Merge reviewer-returned Round 18 C0B rows without changing decisions.

This is a mechanical JSONL merge. Exact-source evidence is checked separately
by validate_rq1b_cross_source_c0b_ledger.py before any draft may reach C1.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for review_input in args.review_input:
        for row in read_jsonl(review_input.resolve()):
            proposal_id = str(row.get("proposal_id", ""))
            if not proposal_id or proposal_id in seen:
                raise SystemExit(f"duplicate_or_missing_proposal:{proposal_id or '<missing>'}")
            seen.add(proposal_id)
            rows.append(row)
    rows.sort(key=lambda row: str(row["proposal_id"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(json.dumps({"status": "C0B_REVIEW_MERGED_NOT_A_CLUSTER_OR_RESULT", "ledger_row_count": len(rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
