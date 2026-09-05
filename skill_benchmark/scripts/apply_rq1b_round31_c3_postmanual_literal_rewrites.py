#!/usr/bin/env python3
"""Remove two literal overlaps introduced by Round 31 C3 manual amendments."""

from __future__ import annotations

import json
from pathlib import Path


INPUT = Path(
    "skill_benchmark/rq1b_cross_source_public_benchmark/working/"
    "c2_round31_final_prompt_drafts_after_c3_manual_rewrite_2026-08-28.jsonl"
)
OUTPUT = Path(
    "skill_benchmark/rq1b_cross_source_public_benchmark/working/"
    "c2_round31_final_prompt_drafts_after_c3_postmanual_literal_rewrite_2026-08-28.jsonl"
)
TARGET = "r31m1-posit-dev-skills-posit-dev-critical-code-reviewer"
REWRITES = {
    "direct": (
        "Review this feature change and prepare implementer-facing feedback. Check expected behavior and the user experience, and clearly distinguish confirmed issues from questions.",
        "Review this feature change and prepare actionable notes for the developer. Check expected behavior and the user experience, and clearly distinguish confirmed issues from questions.",
    ),
    "paraphrase": (
        "Review this submitted change in context. Identify concrete problems in the relevant flow and turn confirmed concerns into professional, implementer-facing feedback.",
        "Review this submitted change in context. Identify concrete problems in the relevant flow and turn confirmed concerns into professional comments the author can act on.",
    ),
}


def main() -> int:
    rows = [json.loads(line) for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed: set[str] = set()
    for row in rows:
        if row.get("intended_candidate_skill_id") != TARGET:
            continue
        variant = str(row.get("variant", ""))
        if variant not in REWRITES:
            continue
        old, new = REWRITES[variant]
        if str(row.get("prompt", "")).count(old) != 1:
            raise SystemExit(f"unexpected_prompt:{variant}")
        row["prompt"] = new
        changed.add(variant)
    if changed != set(REWRITES):
        raise SystemExit(f"rewrite_coverage:{sorted(set(REWRITES) - changed)}")
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    print(json.dumps({"changed_prompt_count": len(changed), "output": str(OUTPUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
