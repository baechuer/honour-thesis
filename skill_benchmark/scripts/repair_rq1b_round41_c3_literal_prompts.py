#!/usr/bin/env python3
"""Apply declared C3 literal-cue rewrites to Round 41 C2 drafts only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


Key = tuple[str, str, str]


REWRITES: dict[Key, tuple[str, str]] = {
    (
        "R41-C0A-business_operations-01",
        "r18m1-CarbeneAI-Forge-claude-skills-hipaacompliance",
        "direct",
    ): (
        "Assess our telehealth application's handling of identifiable health information and give prioritized administrative, physical, and technical safeguards for access, logging, and encryption.",
        "Assess our telehealth product's treatment of patient records and recommend prioritised organisational, physical, and technical protections for access, audit trails, and encryption.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "r20m1-0xF4ng-aether-growth-fieldwork-pmm-content-review",
        "paraphrase",
    ): (
        "Before we release this landing-page copy, assess it against a consistent quality rubric, flag weak sections with specific fixes, and decide whether it is ready to go live.",
        "Before we publish this page, score its messaging against a consistent rubric, point out weak sections with concrete revisions, and recommend whether release is appropriate.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "wave003mc-rampstack-seo-content-gap-audit",
        "direct",
    ): (
        "Use our page inventory, organic performance history, and comparable sites to prioritize which topics to create and which existing pages to deepen, refresh, consolidate, redirect, or remove.",
        "Use our site inventory, traffic history, and peer domains to choose new topics and decide whether current material should be expanded, updated, combined, forwarded, or retired.",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-ShaishavMaisuria-research-paper-lifecycle-skills-skills-make-slides",
        "direct",
    ): (
        "Build a five-minute lightning presentation from my LaTeX manuscript, reusing its figures, limiting each slide to one main takeaway, and checking that the deck fits the speaking time.",
        "Create a five-minute lightning talk from my LaTeX manuscript, reuse its figures, make every slide advance a single clear point, and verify it can be delivered within the allotted window.",
    ),
    (
        "R41-C0A-systems_data_security-01",
        "r20m1-DeerHide-agent_skills-skills-python-test",
        "paraphrase",
    ): (
        "I need a layered Python testing setup that keeps fast tests independent of infrastructure while also validating persistence against a real temporary service and allowing parallel execution.",
        "Set up multilayered automated checks for a CPython service: keep rapid verification free of external systems, exercise data storage through a disposable service, and support concurrent checks.",
    ),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    seen: set[Key] = set()
    for row in rows:
        key = (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))
        if key not in REWRITES:
            continue
        old, new = REWRITES[key]
        if row.get("prompt") != old:
            raise SystemExit(f"unexpected_original_prompt:{key}")
        row["prompt"] = new
        seen.add(key)
    if seen != set(REWRITES):
        raise SystemExit(f"rewrite_coverage_mismatch:missing={sorted(set(REWRITES) - seen)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    audit = {
        "status": "C3_ROUND41_LITERAL_CUE_REWRITE_APPLIED_PENDING_REAUDIT_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "rewrites": [
            {
                "proposal_id": proposal_id,
                "intended_candidate_skill_id": skill_id,
                "variant": variant,
                "old_prompt": old,
                "new_prompt": new,
            }
            for (proposal_id, skill_id, variant), (old, new) in sorted(REWRITES.items())
        ],
        "invariants": [
            "Only the five declared prompt strings changed.",
            "No candidate membership, source content, C0B judgment, C4 adequacy review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result changed.",
        ],
    }
    args.audit.write_text(json.dumps(audit, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"rewrite_count": len(seen), "status": audit["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
