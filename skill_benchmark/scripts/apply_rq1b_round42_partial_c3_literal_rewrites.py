#!/usr/bin/env python3
"""Apply only the literal-C3 review-required Round 42 prompt rewrites."""

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
    parser.add_argument("--rewrites", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prompts = read_jsonl(args.prompts)
    prompt_by_key = {key(row): row for row in prompts}
    if len(prompt_by_key) != len(prompts):
        raise SystemExit("duplicate_prompt_identity")
    audit = json.loads(args.literal_audit.read_text(encoding="utf-8"))
    review_keys = {
        key(row)
        for row in audit.get("records", [])
        if row.get("c3_status") == "C3_LITERAL_CUE_REVIEW_REQUIRED_NOT_A_LABEL_OR_RESULT"
    }
    rewrites = read_jsonl(args.rewrites)
    rewrite_by_key = {key(row): row for row in rewrites}
    if len(rewrite_by_key) != len(rewrites):
        raise SystemExit("duplicate_rewrite_identity")
    if set(rewrite_by_key) != review_keys:
        raise SystemExit(f"rewrite_coverage_mismatch:expected={len(review_keys)}:actual={len(rewrite_by_key)}")

    audit_rows: list[dict[str, Any]] = []
    for row_key, rewrite in rewrite_by_key.items():
        prompt = prompt_by_key.get(row_key)
        if prompt is None:
            raise SystemExit(f"rewrite_unknown_prompt:{':'.join(row_key)}")
        old = str(rewrite.get("old_prompt", ""))
        revised = str(rewrite.get("revised_prompt", "")).strip()
        if old != str(prompt.get("prompt", "")):
            raise SystemExit(f"old_prompt_mismatch:{':'.join(row_key)}")
        if not revised or revised == old:
            raise SystemExit(f"invalid_revised_prompt:{':'.join(row_key)}")
        prompt["prompt"] = revised
        prompt["c3_literal_rewrite_status"] = "C3_LITERAL_REWRITE_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT"
        audit_rows.append({
            "proposal_id": row_key[0],
            "intended_candidate_skill_id": row_key[1],
            "variant": row_key[2],
            "old_prompt": old,
            "revised_prompt": revised,
            "removed_cue_categories": rewrite.get("removed_cue_categories", []),
            "preserved_general_need": rewrite.get("preserved_general_need", ""),
            "rationale": rewrite.get("rationale", ""),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in sorted(prompts, key=key)), encoding="utf-8")
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps({
        "status": "C3_LITERAL_REWRITES_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT",
        "input_prompt_count": len(prompts),
        "literal_review_required_count": len(review_keys),
        "identity_locked_rewrite_count": len(audit_rows),
        "rewrites": sorted(audit_rows, key=key),
        "preserved": ["proposal identity", "candidate composition", "intended candidate identity", "prompt variant coverage"],
        "invalidated_by_new_prompt_text": ["all prior C3 dispositions", "all later C4/C5/C6 eligibility assumptions"],
        "exclusions": ["No gold label, adequacy decision, retrieval input, model result, metric, or frozen benchmark packet was created."],
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"prompt_count": len(prompts), "rewrite_count": len(audit_rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
