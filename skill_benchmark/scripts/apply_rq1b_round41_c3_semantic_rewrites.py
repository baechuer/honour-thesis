#!/usr/bin/env python3
"""Apply the declared Round 41 C3 semantic-cue prompt rewrites only."""

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
        "Assess our telehealth product's treatment of patient records and recommend prioritised organisational, physical, and technical protections for access, audit trails, and encryption.",
        "Our remote clinic will begin storing patient records online. What practical protection work should we plan before launch?",
    ),
    (
        "R41-C0A-business_operations-01",
        "r35m1-The-AIOS-aios-skills-aios-pci-compliance",
        "paraphrase",
    ): (
        "We need to prepare our payment system for a card-security assessment. Identify the required network, access, monitoring, and data-protection controls, including what must never be retained.",
        "Our online shop is about to take card payments. What security work should we plan before launch?",
    ),
    (
        "R41-C0A-content_productivity-01",
        "r20m1-0xF4ng-aether-growth-fieldwork-pmm-content-review",
        "direct",
    ): (
        "Evaluate this launch email for audience fit, channel conventions, defensible claims, and inflated language; give concrete revisions and a publication recommendation.",
        "Could you review this launch email before we send it and point out what should be improved?",
    ),
    (
        "R41-C0A-content_productivity-01",
        "r20m1-0xF4ng-aether-growth-fieldwork-pmm-content-review",
        "paraphrase",
    ): (
        "Before we publish this page, score its messaging against a consistent rubric, point out weak sections with concrete revisions, and recommend whether release is appropriate.",
        "Please look over this draft page before it goes live and tell us whether it needs any changes.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "r21m1-superamped-ai-marketing-skills-skills-research-competitor-content-analysis",
        "paraphrase",
    ): (
        "Prepare an intelligence brief on one competing brand's articles and resource pages, showing how it attracts organic visitors and which useful themes or formats we have not addressed.",
        "Give us a short comparison of our content with one competitor's, so we know what to investigate next.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "wave003mc-rampstack-seo-content-gap-audit",
        "direct",
    ): (
        "Use our site inventory, traffic history, and peer domains to choose new topics and decide whether current material should be expanded, updated, combined, forwarded, or retired.",
        "We need to decide what to do with an established website's content. Help us work out the next priorities.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "wave003mc-rampstack-seo-content-gap-audit",
        "paraphrase",
    ): (
        "Build a quarterly organic-content roadmap from site-level traffic and ranking data, diagnosing stale, weak, overlapping, and declining pages alongside worthwhile uncovered subjects.",
        "Our website's search traffic has become uneven. Help us decide what content work to tackle next.",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-ShaishavMaisuria-research-paper-lifecycle-skills-skills-make-slides",
        "direct",
    ): (
        "Create a five-minute lightning talk from my LaTeX manuscript, reuse its figures, make every slide advance a single clear point, and verify it can be delivered within the allotted window.",
        "Turn my research paper into a brief talk that fits a five-minute academic session.",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-ShaishavMaisuria-research-paper-lifecycle-skills-skills-make-slides",
        "paraphrase",
    ): (
        "Create a concise Marp or Beamer talk from this near-final paper for a fixed short slot: extract usable visuals from the manuscript, plan the story around the problem, and flag overcrowded or badly paced slides.",
        "Could you turn this manuscript into a short presentation for a research audience?",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-omnitric-agent-skills-nature-paper2ppt",
        "direct",
    ): (
        "Turn my research article and its figures into a Chinese PowerPoint deck for a lab presentation, with concise speaker notes and a final visual quality check.",
        "Make a Chinese-language slide presentation from my research paper for a group meeting.",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-omnitric-agent-skills-nature-paper2ppt",
        "paraphrase",
    ): (
        "I need a polished Chinese slide presentation based on this scientific paper for a group meeting; select the supporting visuals, keep the scientific terms consistent, and check that the finished slides are readable.",
        "I need to present this scientific article in Chinese to colleagues.",
    ),
    (
        "R41-C0A-document_research-01",
        "r35m1-LARi-UQAC-ResearchTools-claude-skills-paper2talk",
        "direct",
    ): (
        "Prepare a 16:9 PowerPoint presentation from my newly accepted article for a 12-minute conference session, using our lab template, with narration notes paced to the allotted time and a printable PDF.",
        "Create a presentation from my accepted paper for an upcoming conference.",
    ),
    (
        "R41-C0A-document_research-01",
        "r35m1-LARi-UQAC-ResearchTools-claude-skills-paper2talk",
        "paraphrase",
    ): (
        "My publication has a conference slot. After confirming the audience, duration, ending format, and presentation medium, produce the event-ready deck with a time-budgeted speaking script and handout version.",
        "I need a talk based on my paper for a conference audience.",
    ),
    (
        "R41-C0A-systems_data_security-01",
        "r16m1-github-awesome-copilot-skills-spring-boot-testing",
        "direct",
    ): (
        "Add focused MVC tests for my Spring Boot controller, including HTTP status, JSON response, validation failures, and mocked service dependencies using fluent assertions.",
        "I need focused automated tests for an endpoint in a Java web application.",
    ),
    (
        "R41-C0A-systems_data_security-01",
        "r16m1-github-awesome-copilot-skills-spring-boot-testing",
        "paraphrase",
    ): (
        "For this Java backend, write the narrowest automated checks for a REST endpoint so its request handling and response contract are verified without starting the full application.",
        "For a Java service, help me check an HTTP route after a small change.",
    ),
    (
        "R41-C0A-systems_data_security-01",
        "r20m1-DeerHide-agent_skills-skills-python-test",
        "paraphrase",
    ): (
        "Set up multilayered automated checks for a CPython service: keep rapid verification free of external systems, exercise data storage through a disposable service, and support concurrent checks.",
        "I need automated tests for a Python service that uses a database.",
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
        replacement = REWRITES.get(key)
        if replacement is None:
            continue
        old_prompt, new_prompt = replacement
        if row.get("prompt") != old_prompt:
            raise SystemExit(f"unexpected_original_prompt:{key}")
        row["prompt"] = new_prompt
        seen.add(key)
    if seen != set(REWRITES):
        raise SystemExit(f"rewrite_coverage_mismatch:missing={sorted(set(REWRITES) - seen)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    audit = {
        "status": "C3_ROUND41_SEMANTIC_CUE_REWRITES_APPLIED_REQUIRES_FRESH_C3_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "rewrite_count": len(seen),
        "rewrites": [
            {
                "proposal_id": proposal_id,
                "intended_candidate_skill_id": skill_id,
                "variant": variant,
                "old_prompt": old_prompt,
                "new_prompt": new_prompt,
            }
            for (proposal_id, skill_id, variant), (old_prompt, new_prompt) in sorted(REWRITES.items())
        ],
        "invariants": [
            "Only the 16 declared prompt strings changed.",
            "The original C3 source-informed dispositions remain historical records and are not overwritten.",
            "No candidate membership, source content, C0B judgment, C1 integrity decision, C4 adequacy review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result changed.",
        ],
    }
    args.audit.write_text(json.dumps(audit, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"rewrite_count": len(seen), "status": audit["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
