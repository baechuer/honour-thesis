#!/usr/bin/env python3
"""Apply only recorded Round 31 C3 manual cue amendments to C2 drafts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REWORDED = "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--manual", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    amendments: dict[tuple[str, str, str], str] = {}
    for path in args.manual:
        for row in read_jsonl(path):
            if row.get("c3_disposition") != REWORDED:
                continue
            replacement = str(row.get("proposed_replacement_prompt", "")).strip()
            if not replacement:
                raise SystemExit(f"missing_replacement:{':'.join(key(row))}")
            row_key = key(row)
            if row_key in amendments:
                raise SystemExit(f"duplicate_amendment:{':'.join(row_key)}")
            amendments[row_key] = replacement

    rows = read_jsonl(args.prompts)
    prompt_keys = {key(row) for row in rows}
    unknown = sorted(set(amendments) - prompt_keys)
    if unknown:
        raise SystemExit(f"unknown_amendment:{unknown}")
    applied: list[tuple[str, str, str]] = []
    for row in rows:
        row_key = key(row)
        if row_key in amendments:
            row["prompt"] = amendments[row_key]
            applied.append(row_key)
    if set(applied) != set(amendments):
        raise SystemExit("amendment_application_incomplete")

    rows.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C3_MANUAL_REWRITES_APPLIED_PENDING_REAUDIT_NOT_A_LABEL_OR_RESULT",
        "input_prompt_count": len(rows),
        "applied_rewrite_count": len(applied),
        "applied_keys": [": ".join(row_key) for row_key in sorted(applied)],
        "source_manual_ledgers": [str(path) for path in args.manual],
        "exclusions": [
            "Only recorded C3 replacement prompts were applied.",
            "No label, adequacy decision, retrieval input, metric, result, or frozen cluster was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "applied_rewrite_count": len(applied)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
