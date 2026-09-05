#!/usr/bin/env python3
"""Create the protocol-scoped final C3 disposition for Round 34 C2v3.

The retained C3v2 model-assisted ledger is advisory evidence, not an automatic
ban on any operational detail. The frozen protocol prohibits identifying names,
headings, copied source wording, and idiosyncratic workflow chains; it permits
a normal user to state an operational need. This script fail-closes if the
fresh literal audit finds a copied phrase or source short-line overlap.
"""

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
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--literal-audit", type=Path, required=True)
    parser.add_argument("--model-assisted", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prompts = read_jsonl(args.prompts)
    model_rows = {key(row): row for row in read_jsonl(args.model_assisted)}
    audit = json.loads(args.literal_audit.read_text(encoding="utf-8"))
    literal_rows = {key(row): row for row in audit.get("records", [])}
    failures: list[str] = []
    records: list[dict[str, Any]] = []
    for prompt in prompts:
        item_key = key(prompt)
        review = model_rows.get(item_key)
        literal = literal_rows.get(item_key)
        if review is None or literal is None:
            failures.append(f"missing_review_or_literal:{':'.join(item_key)}")
            continue
        copied = list(literal.get("title_or_short_line_hits", [])) + list(literal.get("multi_token_phrase_hits", []))
        if copied:
            failures.append(f"copied_literal_or_short_line:{':'.join(item_key)}")
            continue
        name_hits = list(literal.get("candidate_name_hits", []))
        non_generic_names = [hit for hit in name_hits if str(hit.get("candidate_name_tokens", "")) not in {"review", "code review"}]
        if non_generic_names:
            failures.append(f"non_generic_candidate_name:{':'.join(item_key)}")
            continue
        model_flag = review.get("c3_disposition") == "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"
        rationale = (
            "Parent protocol adjudication: the C2v3 request states a bounded, ordinary user operational need and has no copied source phrase, source short-line, heading, or non-generic candidate name. "
            "Any remaining literal name hit is only the generic task noun 'review' or 'code review'."
        )
        if model_flag:
            rationale += " The retained model-assisted C3v2 reviewer raised a conservative source-specific-context concern; it is recorded below but does not by itself make a normal user constraint a cue under the frozen C3 rule."
        records.append({
            "proposal_id": item_key[0],
            "intended_candidate_skill_id": item_key[1],
            "variant": item_key[2],
            "c3_disposition": "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT",
            "residual_cue_risk": "medium" if model_flag else "low",
            "rationale": rationale,
            "literal_audit_status": literal.get("c3_status"),
            "literal_generic_candidate_name_hits": name_hits,
            "model_assisted_c3v2_disposition": review.get("c3_disposition"),
            "model_assisted_c3v2_residual_cue_risk": review.get("residual_cue_risk"),
            "model_assisted_c3v2_rationale": review.get("rationale"),
            "adjudication_status": "C3_PARENT_PROTOCOL_ADJUDICATION_NOT_A_LABEL_OR_RESULT",
            "exclusions": [
                "This C3 adjudication does not establish adequacy, a gold label, an acceptable set, retrieval input, model result, metric, or frozen cluster.",
                "A model-assisted cue-risk concern is preserved as an audit fact, not relabelled as a human review.",
            ],
        })
    if failures:
        raise SystemExit(";".join(failures))
    records.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    summary = {
        "status": "C3_ROUND34_FINAL_ADJUDICATION_COMPLETE_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(records),
        "allowed_explicit_operational_context_count": len(records),
        "model_assisted_conservative_flag_count": sum(row["model_assisted_c3v2_disposition"] == "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT" for row in records),
        "literal_generic_name_hit_count": sum(bool(row["literal_generic_candidate_name_hits"]) for row in records),
        "failures": [],
        "rule": "Reject copied source wording or identifying cue; retain a normal bounded user operational context.",
        "exclusions": [
            "No C4 adequacy review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "prompt_count", "model_assisted_conservative_flag_count", "literal_generic_name_hit_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
