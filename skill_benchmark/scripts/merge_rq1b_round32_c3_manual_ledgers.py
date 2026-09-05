#!/usr/bin/env python3
"""Merge final Round 32 C3 reviewer ledgers without altering review content."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")), str(row.get("variant", "")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    rows = [row for path in args.input for row in read_jsonl(path)]
    keys = [key(row) for row in rows]
    if any(not all(row_key) for row_key in keys) or len(keys) != len(set(keys)):
        raise SystemExit("missing_or_duplicate_prompt_identity")
    rows.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C3_ROUND32_FINAL_MANUAL_LEDGERS_MERGED_NOT_A_LABEL_OR_RESULT",
        "input_count": len(args.input),
        "row_count": len(rows),
        "allowed_count": sum(row.get("c3_disposition") == "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT" for row in rows),
        "reworded_count": sum(row.get("c3_disposition") == "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT" for row in rows),
        "risk_counts": {risk: sum(row.get("residual_cue_risk") == risk for row in rows) for risk in ("low", "medium", "high")},
        "exclusions": ["The merger does not alter reviewer judgment, create labels, adequacy decisions, retrieval inputs, metrics, or results."],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
