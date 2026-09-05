#!/usr/bin/env python3
"""Apply complete, identity-locked Round 40 C3 source-cue prompt rewrites."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict) -> tuple[str, str, str]:
    return (
        str(row.get("proposal_id", "")),
        str(row.get("intended_candidate_skill_id", "")),
        str(row.get("variant", "")),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--rewrites", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prompts = read_jsonl(args.prompts)
    rewrites = read_jsonl(args.rewrites)
    prompt_by_key = {key(row): row for row in prompts}
    rewrite_by_key = {key(row): row for row in rewrites}
    if len(prompt_by_key) != len(prompts):
        raise SystemExit("duplicate_prompt_identity")
    if len(rewrite_by_key) != len(rewrites):
        raise SystemExit("duplicate_rewrite_identity")
    if set(prompt_by_key) != set(rewrite_by_key):
        missing = sorted(set(prompt_by_key) - set(rewrite_by_key))
        extra = sorted(set(rewrite_by_key) - set(prompt_by_key))
        raise SystemExit(f"coverage_mismatch:missing={missing}:extra={extra}")

    audit_rows: list[dict] = []
    for row_key, prompt_row in prompt_by_key.items():
        rewrite = rewrite_by_key[row_key]
        if str(rewrite.get("old_prompt", "")) != str(prompt_row.get("prompt", "")):
            raise SystemExit(f"old_prompt_mismatch:{':'.join(row_key)}")
        revised = str(rewrite.get("revised_prompt", "")).strip()
        if not revised or revised == str(prompt_row.get("prompt", "")):
            raise SystemExit(f"invalid_revised_prompt:{':'.join(row_key)}")
        old_prompt = str(prompt_row["prompt"])
        prompt_row["prompt"] = revised
        prompt_row["c3_source_informed_rewrite_status"] = (
            "C3_SOURCE_INFORMED_REWRITE_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT"
        )
        audit_rows.append({
            "proposal_id": row_key[0],
            "intended_candidate_skill_id": row_key[1],
            "variant": row_key[2],
            "old_prompt": old_prompt,
            "revised_prompt": revised,
            "removed_cue_categories": rewrite.get("removed_cue_categories", []),
            "preserved_general_need": rewrite.get("preserved_general_need", ""),
            "rationale": rewrite.get("rationale", ""),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in sorted(
            prompts,
            key=key,
        )),
        encoding="utf-8",
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps({
        "status": "C3_SOURCE_INFORMED_REWRITES_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(prompts),
        "identity_locked_rewrite_count": len(audit_rows),
        "rewrites": audit_rows,
        "invalidated_by_new_prompt_text": [
            "all prior C3 source-informed dispositions",
            "all prior C4 blind reviews",
            "all prior C5/C6 eligibility assumptions",
        ],
        "preserved": [
            "proposal identity",
            "candidate composition",
            "intended candidate identity",
            "prompt variant coverage",
        ],
        "exclusions": ["No gold label, adequacy decision, retrieval input, model result, metric, or frozen benchmark packet was created."],
    }, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"prompt_count": len(prompts), "rewrite_count": len(audit_rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
