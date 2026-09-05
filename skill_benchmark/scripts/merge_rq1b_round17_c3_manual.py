#!/usr/bin/env python3
"""Merge and validate the coverage of Round 17 manual C3 dispositions."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKING = ROOT / "rq1b_cross_source_public_benchmark" / "working"
MANIFEST = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
INPUTS = [WORKING / f"c3_round17_manual_{proposal}.jsonl" for proposal in ("201_204", "206_207", "210_212", "215_217", "219_222")]
PROMPTS = MANIFEST / "c2_prompt_drafts_round17_v2_2026-08-27.jsonl"
OUTPUT = MANIFEST / "c3_round17_manual_semantic_disposition_2026-08-27.jsonl"
SUMMARY = MANIFEST / "c3_round17_manual_semantic_disposition_summary_2026-08-27.json"
VALID = {
    "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT",
    "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except json.JSONDecodeError as error:
        raise SystemExit(f"json_parse_error:{path}:{error}") from error


def key(row: dict[str, object]) -> tuple[str, str, str]:
    return (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")), str(row.get("variant", "")))


def main() -> None:
    expected = {key(row) for row in read_jsonl(PROMPTS)}
    rows = [row for path in INPUTS for row in read_jsonl(path)]
    observed = Counter(key(row) for row in rows)
    failures: list[str] = []
    for item in sorted(expected):
        if observed[item] != 1:
            failures.append(f"coverage:{':'.join(item)}:{observed[item]}")
    for row in rows:
        if row.get("c3_disposition") not in VALID:
            failures.append(f"invalid_disposition:{':'.join(key(row))}")
        if row.get("residual_cue_risk") not in {"low", "medium", "high"}:
            failures.append(f"invalid_risk:{':'.join(key(row))}")
        if not str(row.get("rationale", "")).strip():
            failures.append(f"missing_rationale:{':'.join(key(row))}")
    if len(rows) != len(expected):
        failures.append(f"row_count:{len(rows)}:expected:{len(expected)}")
    rows.sort(key=key)
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C3_MANUAL_COVERAGE_VALID_NOT_A_LABEL_OR_RESULT" if not failures else "C3_MANUAL_COVERAGE_INVALID_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(expected),
        "reworded_count": sum(row.get("c3_disposition") == "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT" for row in rows),
        "allowed_explicit_context_count": sum(row.get("c3_disposition") == "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT" for row in rows),
        "risk_counts": {risk: sum(row.get("residual_cue_risk") == risk for row in rows) for risk in ("low", "medium", "high")},
        "failures": failures,
        "exclusions": ["C3 does not establish gold labels, adequacy, strict singleton validity, retrieval inputs, model calls, metrics, or frozen benchmark packets."],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
