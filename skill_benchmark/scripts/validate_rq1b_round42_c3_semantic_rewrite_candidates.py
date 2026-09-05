#!/usr/bin/env python3
"""Validate the declared Round 42 C3 semantic rewrite candidates, fail closed."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REWRITTEN = "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"
REQUIRED = {"proposal_id", "intended_candidate_skill_id", "variant", "old_prompt", "new_prompt", "rewrite_rationale"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"non_object_jsonl:{path}:{line_number}")
        rows.append(value)
    return rows


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def sentence_count(text: str) -> int:
    return len(re.findall(r"[.!?](?:\\s|$)", text.strip()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--c3-review", type=Path, required=True)
    parser.add_argument("--rewrite-risk", choices=("low", "medium", "high"))
    parser.add_argument("--rewrite", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prompts_by_key = {key(row): row for row in read_jsonl(args.prompts)}
    expected = {
        key(row)
        for row in read_jsonl(args.c3_review)
        if row.get("c3_disposition") == REWRITTEN
        and (args.rewrite_risk is None or row.get("residual_cue_risk") == args.rewrite_risk)
    }
    rows = [row for path in args.rewrite for row in read_jsonl(path)]
    failures: list[str] = []
    observed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for index, row in enumerate(rows, start=1):
        if set(row) != REQUIRED:
            failures.append(f"schema:{index}")
            continue
        row_key = key(row)
        if row_key in observed:
            failures.append(f"duplicate:{row_key}")
            continue
        observed[row_key] = row
        original = prompts_by_key.get(row_key)
        if original is None:
            failures.append(f"unknown_identity:{row_key}")
            continue
        old_prompt = str(row.get("old_prompt", ""))
        new_prompt = str(row.get("new_prompt", "")).strip()
        if old_prompt != str(original.get("prompt", "")):
            failures.append(f"old_prompt_mismatch:{row_key}")
        if not new_prompt or new_prompt == old_prompt:
            failures.append(f"missing_or_unchanged_new_prompt:{row_key}")
        if len(new_prompt.split()) > 45:
            failures.append(f"word_limit:{row_key}:{len(new_prompt.split())}")
        if sentence_count(new_prompt) > 2:
            failures.append(f"sentence_limit:{row_key}")
        if not str(row.get("rewrite_rationale", "")).strip():
            failures.append(f"missing_rationale:{row_key}")
    if set(observed) != expected:
        failures.append(f"coverage:missing={sorted(expected - set(observed))}:extra={sorted(set(observed) - expected)}")

    ordered = [observed[row_key] for row_key in sorted(observed)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in ordered), encoding="utf-8")
    summary = {
        "status": "C3_ROUND42_SEMANTIC_REWRITE_CANDIDATES_VALID_NOT_A_LABEL_OR_RESULT" if not failures else "C3_ROUND42_SEMANTIC_REWRITE_CANDIDATES_INVALID_NOT_A_LABEL_OR_RESULT",
        "expected_count": len(expected),
        "returned_count": len(rows),
        "unique_returned_count": len(observed),
        "rewrite_risk_filter": args.rewrite_risk,
        "failures": failures,
        "exclusions": ["This validation does not assess adequacy, create labels, or authorize C4/C5/C6/retrieval."],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
