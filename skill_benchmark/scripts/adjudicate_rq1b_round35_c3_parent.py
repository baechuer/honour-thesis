#!/usr/bin/env python3
"""Apply the frozen C3 cue rule to Round 35 source-informed risk records.

The source-informed reviewer is intentionally conservative: it may flag a
user's operational constraint merely because it is the fact that distinguishes
one candidate. The frozen RQ1b protocol permits such ordinary input,
environment, constraint, and expected-artifact context. This adjudication
therefore preserves every source-informed warning but treats it as a source
construction risk, not a cue, unless the final literal audit finds candidate
identity or copied wording.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PASS = "C3_LITERAL_CUE_PASS_NOT_A_LABEL_OR_RESULT"
ALLOWED = "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_object:{path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def row_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-informed", type=Path, required=True)
    parser.add_argument("--literal-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    source_rows = read_jsonl(args.source_informed)
    literal = read_json(args.literal_audit)
    if literal.get("status") != "C3_LITERAL_CUE_AUDIT_COMPLETE_NOT_A_LABEL_OR_RESULT":
        raise SystemExit(f"unexpected_literal_status:{literal.get('status')}")
    literal_rows = {
        row_key(row): row
        for row in literal.get("records", [])
    }
    failures: list[str] = []
    adjudicated: list[dict[str, Any]] = []
    for source in source_rows:
        key = row_key(source)
        cue = literal_rows.get(key)
        if cue is None:
            failures.append(f"missing_literal_record:{':'.join(key)}")
            continue
        if cue.get("c3_status") != PASS:
            failures.append(f"literal_cue_not_cleared:{':'.join(key)}")
            continue
        source_risk = str(source.get("residual_cue_risk"))
        if source_risk not in {"low", "medium", "high"}:
            failures.append(f"invalid_source_risk:{':'.join(key)}")
            continue
        # High source-informed risk is retained verbatim below. The parent
        # residual is medium because it records design sensitivity, not a
        # detected source identity/copying cue under the frozen C3 rule.
        parent_risk = "low" if source_risk == "low" else "medium"
        adjudicated.append({
            "adjudication_status": "C3_PARENT_PROTOCOL_ADJUDICATION_NOT_A_LABEL_OR_RESULT",
            "review_method": "parent_protocol_adjudication_not_human",
            "proposal_id": key[0],
            "intended_candidate_skill_id": key[1],
            "variant": key[2],
            "c3_disposition": ALLOWED,
            "residual_cue_risk": parent_risk,
            "literal_audit_status": cue.get("c3_status"),
            "literal_candidate_name_hits": cue.get("candidate_name_hits", []),
            "literal_title_or_short_line_hits": cue.get("title_or_short_line_hits", []),
            "literal_multi_token_phrase_hits": cue.get("multi_token_phrase_hits", []),
            "model_assisted_c3_disposition": source.get("c3_disposition"),
            "model_assisted_c3_residual_cue_risk": source_risk,
            "model_assisted_c3_rationale": source.get("rationale"),
            "model_assisted_c3_source_evidence_substrings": source.get("source_evidence_substrings", []),
            "rationale": (
                "Parent protocol adjudication: final literal C3 found no candidate name, title/short-line, "
                "or copied multi-token source phrase. Under the frozen C2/C3 rule, the prompt's bounded "
                "user-facing operational context is permitted even when that context distinguishes a candidate. "
                "The source-informed warning is retained as a construction-sensitivity audit fact rather than "
                "being relabelled as a human judgment or ignored."
            ),
            "exclusions": [
                "This C3 adjudication does not establish adequacy, a gold label, an acceptable set, C4/C5/C6 outcome, retrieval input, model result, metric, or frozen cluster.",
                "A source-informed model-assisted risk record is preserved below; it is not presented as human review.",
            ],
        })
    source_keys = {row_key(row) for row in source_rows}
    if set(literal_rows) != source_keys:
        failures.append(f"coverage_mismatch:literal={len(literal_rows)}:source={len(source_keys)}")
    adjudicated.sort(key=row_key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in adjudicated), encoding="utf-8")
    summary = {
        "status": "C3_PARENT_PROTOCOL_ADJUDICATION_PASS_NOT_A_LABEL_OR_RESULT" if not failures else "C3_PARENT_PROTOCOL_ADJUDICATION_INVALID_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(adjudicated),
        "allowed_explicit_context_count": len(adjudicated),
        "parent_residual_risk_counts": {risk: sum(row["residual_cue_risk"] == risk for row in adjudicated) for risk in ("low", "medium", "high")},
        "retained_source_informed_risk_counts": {risk: sum(row["model_assisted_c3_residual_cue_risk"] == risk for row in adjudicated) for risk in ("low", "medium", "high")},
        "failures": sorted(set(failures)),
        "exclusions": ["This is a C3 cue adjudication only. It does not replace blinded C4 adequacy review or create benchmark/retrieval results."],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
