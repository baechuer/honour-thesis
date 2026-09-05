#!/usr/bin/env python3
"""Cue-only Round 20 C3 rewording that preserves construction targets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROPOSAL = "R20-C0A-AGENT-ECOSYSTEMS-002"
REPAIRS = {
    (
        "r20m1-cobusgreyling-agent-skills-skills-model-routing",
        "direct",
    ): (
        "I am building a support agent with cheap ticket classification, multi-step account actions, and irreversible cancellation decisions. Help me choose an appropriate language-model tier for each call, set escalation rules, and define the tests and per-call cost targets needed before we deploy it.",
        "I am building a support agent with inexpensive ticket classification, multi-step account actions, and irreversible cancellation decisions. Help me assign an appropriate capability tier to each request, set escalation rules, and define the tests and request-level spending thresholds needed before we deploy it.",
    ),
    (
        "r20m1-cobusgreyling-agent-skills-skills-model-routing",
        "paraphrase",
    ): (
        "Our assistant currently uses the same expensive model for every step. Propose a measured routing design that moves simple extraction and summaries to lower-cost models while reserving stronger reasoning for planning and high-consequence actions, with clear verification triggers for promotion.",
        "Our assistant currently uses the same expensive engine for every step. Propose a measured selection scheme that moves simple extraction and summaries to lower-cost options while reserving stronger reasoning for planning and high-consequence actions, with clear verification triggers for promotion.",
    ),
    (
        "r20m1-my-stacks-claude-code-skills-claude-skills-ai-router",
        "paraphrase",
    ): (
        "I want a practical task-routing guide for an AI coding assistant: use an inexpensive option for lightweight edits, a stronger one for complex design work, and extra independent model opinions when reviewing risky changes. Recommend the route for each case and explain the trade-offs.",
        "I want a practical allocation guide for an AI coding assistant: use an inexpensive option for lightweight edits, a stronger one for complex design work, and extra independent opinions when reviewing risky changes. Recommend the assignment for each case and explain the trade-offs.",
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    repairs: list[dict[str, str]] = []
    for row in rows:
        if row.get("proposal_id") != PROPOSAL:
            continue
        key = (str(row.get("intended_candidate_skill_id")), str(row.get("variant")))
        replacement = REPAIRS.get(key)
        if replacement is None:
            continue
        old, new = replacement
        if row.get("prompt") != old:
            raise SystemExit(f"unexpected_prompt_text:{key}")
        row["prompt"] = new
        repairs.append({"candidate": key[0], "variant": key[1], "old_prompt": old, "new_prompt": new})
    if len(repairs) != len(REPAIRS):
        raise SystemExit(f"repair_count:{len(repairs)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "status": "C3_PROMPT_CUE_REWORD_COMPLETE_NOT_A_LABEL_OR_RESULT",
        "proposal_id": PROPOSAL,
        "repairs": repairs,
        "boundary": "Only cue wording changed; intended candidates and direct/paraphrase construction targets are preserved.",
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "repair_count": len(repairs)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
