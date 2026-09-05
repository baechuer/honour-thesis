#!/usr/bin/env python3
"""Apply a declared Round 42 C3 semantic-cue rewrite ledger, fail closed."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


Key = tuple[str, str, str]
REWRITTEN = "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> Key:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--c3-review", type=Path, required=True)
    parser.add_argument("--rewrite-risk", choices=("low", "medium", "high"))
    parser.add_argument("--rewrite", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    rows_by_key = {key(row): row for row in rows}
    if len(rows_by_key) != len(rows):
        raise SystemExit("duplicate_input_identity")

    c3 = read_jsonl(args.c3_review)
    c3_by_key = {key(row): row for row in c3}
    if len(c3_by_key) != len(c3):
        raise SystemExit("duplicate_c3_identity")
    expected = {
        row_key
        for row_key, row in c3_by_key.items()
        if row.get("c3_disposition") == REWRITTEN
        and (args.rewrite_risk is None or row.get("residual_cue_risk") == args.rewrite_risk)
    }

    rewrites = [row for path in args.rewrite for row in read_jsonl(path)]
    rewrite_by_key = {key(row): row for row in rewrites}
    if len(rewrite_by_key) != len(rewrites):
        raise SystemExit("duplicate_rewrite_identity")
    if set(rewrite_by_key) != expected:
        raise SystemExit(f"rewrite_coverage_mismatch:missing={sorted(expected - set(rewrite_by_key))}:extra={sorted(set(rewrite_by_key) - expected)}")

    applied: list[dict[str, Any]] = []
    for row_key, rewrite in sorted(rewrite_by_key.items()):
        if row_key not in rows_by_key:
            raise SystemExit(f"missing_input_identity:{row_key}")
        old_prompt = str(rewrite.get("old_prompt", ""))
        new_prompt = str(rewrite.get("new_prompt", "")).strip()
        if not new_prompt or old_prompt != str(rows_by_key[row_key].get("prompt", "")):
            raise SystemExit(f"unexpected_old_or_empty_new_prompt:{row_key}")
        if old_prompt == new_prompt:
            raise SystemExit(f"no_semantic_rewrite:{row_key}")
        rows_by_key[row_key]["prompt"] = new_prompt
        rows_by_key[row_key]["c3_semantic_rewrite_status"] = "C3_SEMANTIC_REWRITE_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT"
        applied.append({
            "proposal_id": row_key[0],
            "intended_candidate_skill_id": row_key[1],
            "variant": row_key[2],
            "old_prompt": old_prompt,
            "new_prompt": new_prompt,
            "rewrite_rationale": str(rewrite.get("rewrite_rationale", "")),
        })

    ordered = [rows_by_key[row_key] for row_key in sorted(rows_by_key)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in ordered), encoding="utf-8")
    audit = {
        "status": "C3_ROUND42_SEMANTIC_CUE_REWRITES_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "c3_review": str(args.c3_review),
        "c3_review_sha256": sha256(args.c3_review),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "rewrite_count": len(applied),
        "rewrite_risk_filter": args.rewrite_risk,
        "rewrites": applied,
        "invariants": [
            "Only the prompt strings for exactly the C3 reworded identities changed.",
            "The pre-rewrite C3 records remain historical evidence and are not overwritten.",
            "No candidate membership, source content, C0B judgment, C1 integrity decision, C4 adequacy review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result changed.",
        ],
    }
    args.audit.write_text(json.dumps(audit, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"rewrite_count": len(applied), "status": audit["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
