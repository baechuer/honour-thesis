#!/usr/bin/env python3
"""Replace the one remaining Round 40 source-shaped lead-generation prompt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGET = (
    "R40-C0A-web_commerce_automation-06",
    "r40m1-exa-labs-agent-skills-skills-lead-generation",
    "direct",
)
OLD = (
    "Prepare a CSV of 100 potential business customers for our inventory-planning service. "
    "For each, list its website, what it offers, approximate company size, a recent sign of growth, "
    "and a brief explanation of its fit. Leave out companies we already serve and direct rivals, "
    "remove repeats, and put the strongest prospects first."
)
NEW = (
    "Identify businesses whose current operations might benefit from our inventory-planning service. "
    "Provide a short prioritised list with a brief public reason for each likely fit. "
    "Leave out businesses already known to us or evidently competing with us."
)


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
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    matches = [row for row in rows if key(row) == TARGET]
    if len(matches) != 1:
        raise SystemExit(f"target_coverage:{len(matches)}")
    row = matches[0]
    if str(row.get("prompt", "")) != OLD:
        raise SystemExit("unexpected_input_prompt")
    row["prompt"] = NEW
    row["c3_source_informed_rewrite_status"] = (
        "C3_LEADGEN_MICRO_REWRITE_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT"
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(item, ensure_ascii=True, sort_keys=True) + "\n" for item in sorted(rows, key=key)),
        encoding="utf-8",
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps({
        "status": "C3_ROUND40_LEADGEN_MICRO_REWRITE_APPLIED_REQUIRES_FRESH_C3_C4_NOT_A_LABEL_OR_RESULT",
        "target_identity": {
            "proposal_id": TARGET[0],
            "intended_candidate_skill_id": TARGET[1],
            "variant": TARGET[2],
        },
        "old_prompt": OLD,
        "new_prompt": NEW,
        "reason": "Remove exact count, multi-field enrichment schema, deduplication, and ordered-output bundle retained by the source-informed audit.",
        "preserved": ["candidate composition", "intended candidate identity", "all other prompt texts"],
        "invalidated": ["the prior C3 source-informed disposition for this prompt", "all prior C4 reviews"],
        "exclusions": ["No gold label, adequacy decision, retrieval input, model result, metric, or frozen benchmark packet was created."],
    }, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rewritten_prompt_count": 1}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
