#!/usr/bin/env python3
"""Validate complete C3 manual dispositions against final C2 prompts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


VALID_DISPOSITIONS = {
    "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT",
    "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def row_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")), str(row.get("variant", "")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--manual", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    expected = {row_key(row) for row in read_jsonl(args.prompts)}
    rows = read_jsonl(args.manual)
    observed = Counter(row_key(row) for row in rows)
    failures: list[str] = []
    for key in sorted(expected):
        if observed[key] != 1:
            failures.append(f"coverage:{':'.join(key)}:{observed[key]}")
    for row in rows:
        key = row_key(row)
        if row.get("c3_disposition") not in VALID_DISPOSITIONS:
            failures.append(f"invalid_disposition:{':'.join(key)}")
        if row.get("residual_cue_risk") not in {"low", "medium", "high"}:
            failures.append(f"invalid_risk:{':'.join(key)}")
        if not str(row.get("rationale", "")).strip():
            failures.append(f"missing_rationale:{':'.join(key)}")
    if len(rows) != len(expected):
        failures.append(f"row_count:{len(rows)}:expected:{len(expected)}")
    rows.sort(key=row_key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C3_MANUAL_COVERAGE_VALID_NOT_A_LABEL_OR_RESULT" if not failures else "C3_MANUAL_COVERAGE_INVALID_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(expected),
        "reworded_count": sum(row.get("c3_disposition") == "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT" for row in rows),
        "allowed_explicit_context_count": sum(row.get("c3_disposition") == "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT" for row in rows),
        "risk_counts": {risk: sum(row.get("residual_cue_risk") == risk for row in rows) for risk in ("low", "medium", "high")},
        "failures": failures,
        "exclusions": ["C3 does not establish gold labels, adequacy, strict singleton validity, retrieval inputs, model calls, metrics, or frozen benchmark packets."],
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
