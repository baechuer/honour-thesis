#!/usr/bin/env python3
"""Reword the one Round 19 C3 literal-cue prompt without changing its target."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGET = "r18m1-michaelboeding-skills-skills-copywriter-agent"
OLD = "Create a coordinated launch set for a refillable water bottle aimed at university students. Include several headline options, a short product story, a longer sales message with benefits and credibility, a small set of social and search advertisements, button text options, and email subject lines. The campaign goal is online purchases; the voice is upbeat but not childish."
NEW = "Create a coordinated launch set for a refillable water bottle aimed at university students. Include several headline options, a short product story, a longer sales message with benefits and credibility, a small set of social and search advertisements, button text alternatives, and opening lines for the announcement emails. The desired commercial outcome is online purchases; the voice is upbeat but not childish."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    count = 0
    for row in rows:
        if row.get("intended_candidate_skill_id") == TARGET and row.get("variant") == "direct":
            if row.get("prompt") != OLD:
                raise SystemExit("unexpected_prompt_text")
            row["prompt"] = NEW
            count += 1
    if count != 1:
        raise SystemExit(f"repair_count:{count}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "status": "C3_PROMPT_CUE_REWORD_COMPLETE_NOT_A_LABEL_OR_RESULT",
        "target_candidate": TARGET,
        "variant": "direct",
        "old_prompt": OLD,
        "new_prompt": NEW,
        "boundary": "Only literal cue wording changed; proposal and construction target remain identical.",
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "repair_count": count}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
