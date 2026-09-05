#!/usr/bin/env python3
"""Validate Round 35 source-informed C3 semantic-cue records locally."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DISPOSITIONS = {
    "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT",
    "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT",
}
METHOD = "model_assisted_source_informed_c3_semantic_cue_review_not_human"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")), str(row.get("variant", "")))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--manual", type=Path, action="append", required=True)
    parser.add_argument("--c1", type=Path, required=True)
    parser.add_argument("--source-pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--round-label", default="R35")
    args = parser.parse_args()

    prompt_rows = read_jsonl(args.prompts)
    expected = {key(row) for row in prompt_rows}
    c1 = {str(row["proposal_id"]): row for row in read_jsonl(args.c1)}
    pool = {str(row["skill_id"]): row for row in read_jsonl(args.source_pool)}
    rows = [row for path in args.manual for row in read_jsonl(path)]
    observed = Counter(key(row) for row in rows)
    failures: list[str] = []

    for expected_key in sorted(expected):
        if observed[expected_key] != 1:
            failures.append(f"coverage:{':'.join(expected_key)}:{observed[expected_key]}")
    for row in rows:
        proposal_id, intended_id, variant = key(row)
        row_ref = f"{proposal_id}:{intended_id}:{variant}"
        if row.get("review_method") != METHOD:
            failures.append(f"invalid_review_method:{row_ref}")
        if row.get("c3_disposition") not in DISPOSITIONS:
            failures.append(f"invalid_disposition:{row_ref}")
        if row.get("residual_cue_risk") not in {"low", "medium", "high"}:
            failures.append(f"invalid_risk:{row_ref}")
        if not str(row.get("rationale", "")).strip():
            failures.append(f"missing_rationale:{row_ref}")
        if not isinstance(row.get("source_evidence_substrings"), list):
            failures.append(f"invalid_evidence_shape:{row_ref}")
            continue
        proposal = c1.get(proposal_id)
        candidate_ids = set(map(str, proposal.get("candidate_skill_ids", []))) if proposal else set()
        if intended_id not in candidate_ids:
            failures.append(f"unexpected_intended_candidate:{row_ref}")
            continue
        original_texts: list[str] = []
        for candidate_id in candidate_ids:
            source = pool.get(candidate_id)
            if source is None:
                failures.append(f"missing_pool_candidate:{row_ref}:{candidate_id}")
                continue
            path = Path(str(source.get("local_original_path", "")))
            if not path.is_file():
                failures.append(f"missing_original:{row_ref}:{candidate_id}")
                continue
            original_texts.append(path.read_text(encoding="utf-8"))
        for excerpt in row["source_evidence_substrings"]:
            if not isinstance(excerpt, str) or not excerpt:
                failures.append(f"invalid_evidence:{row_ref}")
            elif not any(excerpt in text for text in original_texts):
                failures.append(f"non_exact_source_evidence:{row_ref}:{excerpt}")
    if len(rows) != len(expected):
        failures.append(f"row_count:{len(rows)}:expected:{len(expected)}")
    rows.sort(key=key)
    write_jsonl(args.output, rows)
    summary = {
        "status": f"C3_{args.round_label}_SOURCE_INFORMED_MANUAL_EVIDENCE_PASS_NOT_A_LABEL_OR_RESULT" if not failures else f"C3_{args.round_label}_SOURCE_INFORMED_MANUAL_EVIDENCE_INVALID_NOT_A_LABEL_OR_RESULT",
        "review_method": METHOD,
        "prompt_count": len(expected),
        "returned_row_count": len(rows),
        "allowed_explicit_context_count": sum(row.get("c3_disposition") == "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT" for row in rows),
        "reworded_for_literal_cue_count": sum(row.get("c3_disposition") == "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT" for row in rows),
        "risk_counts": {risk: sum(row.get("residual_cue_risk") == risk for row in rows) for risk in ("low", "medium", "high")},
        "failures": sorted(set(failures)),
        "exclusions": ["C3 semantic-cue records are not adequacy, gold labels, C4/C5/C6 decisions, retrieval inputs, model results, or metrics."],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
