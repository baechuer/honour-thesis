#!/usr/bin/env python3
"""Create a cue-repaired C2 Round 35 draft without changing its coverage keys.

This maps the ten C3 literal-cue findings to cue-safe natural-language prompt
rewrites.  The script changes only ``prompt`` at an explicitly enumerated
``(proposal, intended candidate, variant)`` key and fails closed for every
other condition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REWRITES = {
    ("R35-C0A-BROAD_AGENT_SKILLS-02", "r35m1-ai-ecoverse-slicc-packages-vfs-root-workspace-skills-playwright-cli", "direct"): "I have several concurrent interactive sessions for separate tasks. In the one displaying our checkout, fill in the test details, submit the form, and confirm the order confirmation appears without affecting the other sessions.",
    ("R35-C0A-BROAD_AGENT_SKILLS-02", "r35m1-faisal-shah-agent-skills-skills-playwright-cli", "direct"): "A sign-up flow works locally but fails in CI. Use a command-line web session to reproduce it, inspect the page after each step, and collect evidence showing where the flow breaks.",
    ("R35-C0A-BROAD_AGENT_SKILLS-02", "r35m1-faisal-shah-agent-skills-skills-playwright-cli", "paraphrase"): "Please diagnose the failing registration journey in our automated page check: navigate through the form, verify the visible outcome and relevant requests, then report the failure with supporting artifacts.",
    ("R35-C0A-BROAD_AGENT_SKILLS-02", "r35m1-iii-hq-workers-browser-skills", "direct"): "Our deployed web app shows a blank results area after a search. Open an interactive web session, reproduce the issue, and inspect the page console and failed requests to identify what is going wrong.",
    ("R35-C0A-BROAD_AGENT_SKILLS-03", "r35m1-cgfixit-CyClaw-codex-skills-doc-sync", "paraphrase"): "I changed how this project is configured and operated. Bring the user-facing instructions into line with the code, including command and setup material; do not alter behavior merely to accommodate inaccurate instructions, and confirm the documentation checks pass.",
    ("R35-C0A-CLAUDE_CODE_SKILLS-01", "r35m1-Kevin-hDev-Beaver-src-tauri-default-skills-review", "direct"): "Assess the changes in my branch before we ship. Check for bugs, security risks, regressions, missing requirements, and unjustified changes; return prioritized findings with file-and-line evidence, but do not edit anything.",
    ("R35-C0A-CLAUDE_CODE_SKILLS-01", "r35m1-rodriguezyanez-eco-team-brain-commands-code-review-expert", "direct"): "Before assessing our payment API module, ask me for the product context, technology stack, architecture expectations, team conventions, requirements, and scope. Then examine robustness, protection concerns, runtime behaviour, test coverage, configuration, monitoring, and documentation, with actionable findings.",
    ("R35-C0A-CLAUDE_CODE_SKILLS-01", "r35m1-rodriguezyanez-eco-team-brain-commands-code-review-expert", "paraphrase"): "I need a comprehensive health assessment of this project rather than a patch check. Start by collecting the business and technical background, then scrutinize the selected components for structural, reliability, security, test, operational, and documentation gaps and deliver a prioritized remediation report.",
    ("R35-C0A-CODEX_SKILLS-02", "r35m1-ArcaneArts-Cantrip-cantrip-codex-upstream-codex-rs-skills-src-assets-samples-skill-creator", "direct"): "Package a reusable agent capability for handling customer-support escalations. Keep the instructions tightly scoped and add supporting resources only where they are genuinely needed.",
    ("R35-C0A-CODEX_SKILLS-02", "r35m1-ArcaneArts-Cantrip-cantrip-codex-upstream-codex-rs-skills-src-assets-samples-skill-creator", "paraphrase"): "I want to package our support-escalation process as an agent capability. Design the guidance so it stays focused on that work, with extra materials where they materially improve the workflow's reliability.",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    pending = set(REWRITES)
    repairs: list[dict[str, object]] = []
    for row in rows:
        key = (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")), str(row.get("variant", "")))
        replacement = REWRITES.get(key)
        if replacement is None:
            continue
        old = row.get("prompt")
        if not isinstance(old, str) or not old.strip() or old == replacement:
            raise SystemExit(f"unexpected_prompt_at_repair_location:{key}")
        row["prompt"] = replacement
        repairs.append({"proposal_id": key[0], "intended_candidate_skill_id": key[1], "variant": key[2], "old_prompt": old, "replacement_prompt": replacement})
        pending.remove(key)
    if pending or len(repairs) != len(REWRITES):
        raise SystemExit(f"repair_locations_missing:{sorted(pending)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    args.repair_log.parent.mkdir(parents=True, exist_ok=True)
    args.repair_log.write_text(json.dumps({
        "status": "C3_LITERAL_CUE_REWRITE_PENDING_REAUDIT_NOT_A_LABEL_OR_RESULT",
        "input_drafts": str(args.input),
        "input_sha256": sha256(args.input),
        "output_drafts": str(args.output),
        "output_sha256": sha256(args.output),
        "repair_count": len(repairs),
        "repairs": repairs,
        "invariant": "Only the ten declared prompt strings changed; proposal, intended candidate, variant, coverage, source records, labels, acceptable sets, retrieval inputs, model calls, metrics, and results did not change.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "cue_rewrites_written", "repair_count": len(repairs)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
