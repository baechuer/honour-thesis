#!/usr/bin/env python3
"""Write B047's independent, full-source disagreement adjudications only."""

from __future__ import annotations

import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
PACKET_DIR = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_academic_scientific_research_literature_review_citation_management_technical_writing_knowledge_organisation_statistics_mathematics_b047_2026-09-04/batch_047_full_source_review_packets"
PACKET = PACKET_DIR / "reconciliation/coordinator_packet.jsonl"
RETURN = PACKET_DIR / "reconciliation/coordinator_return.jsonl"


DECISIONS = {
    "F-1b3e7c01aeaad42c": (
        "REJECT_TOPIC_ONLY",
        ("# Source Research Brief", "# Funding Sources Researcher", "# Research Brief Creator"),
        "The sources produce briefs about a prospective interview source, an organisation's funding, and a reporter's story assignment. A brief is a common document label, not a bounded shared objective, input, and output.",
    ),
    "F-3cf96c92aec292c1": (
        "REJECT_COMPONENT_OR_COMPOSITION",
        ("## Phase 1: Frame the Problem (Day 1-2)", "## Phase 1: Frame the Problem (Day 1-2)", "# [Feature/Product Name] PRD"),
        "S-1 and S-2 duplicate the end-to-end product-discovery cycle, while S-3 turns framed and researched product evidence into a PRD. Discovery and PRD authoring are sequential, composable operations rather than three alternative first routes.",
    ),
    "F-49bc7df459ec0fd3": (
        "REJECT_NEAR_DUPLICATE_OR_FORK",
        ("# Skill Creator", "# Write Skills", "# Writing Skills"),
        "All three complete originals create or revise agent skills and overlap on SKILL.md structure, triggering, concise instruction, resources, and validation. Picoclaw scope, tighter authoring heuristics, and an extended critic loop are variations around the same skill-authoring route, not three independent peer routes.",
    ),
    "F-5f0d2a20e04fc95f": (
        "REJECT_GENERIC_SPECIALIST",
        ("# 学术写作润色", "# Academic Writing: Publication-Grade English Prose", "# SCI/SSCI Academic Polishing"),
        "S-1 and S-3 specialise in polishing supplied academic prose (including Chinese-to-English/manuscript work), whereas S-2 is a broader draft/revise/review container for essays, reports, literature reviews, rubric enforcement, and anti-AI auditing. The generalist versus specialist coverage is unbalanced.",
    ),
    "F-652f0fd56bec2f8a": (
        "REJECT_NEAR_DUPLICATE_OR_FORK",
        ("# Deep research", "# Deep Research", "# Research lab of agents"),
        "Each original independently plans multi-source research, verifies evidence, and synthesises a cited answer. Markdown-report and multi-agent/verification-loop implementation differences do not establish three distinct first routes for that same research operation.",
    ),
    "F-98826bcfe8ea282e": (
        "REJECT_COMPONENT_OR_COMPOSITION",
        ("# Manuscript Drafter — Long-Form Drafting Without the Usual AI Mistakes", "# Nature-Style Academic Polishing", "# Nature-Style Scientific Writing"),
        "S-1 and S-3 draft or rebuild manuscript sections from claims, results, or notes; S-2 polishes or restructures existing prose. Draft/rebuild and finished-prose editing are sequential writing stages, not interchangeable first routes.",
    ),
    "F-c03781eccdc8b28b": (
        "REJECT_NEAR_DUPLICATE_OR_FORK",
        ("# Full-Paper Markdown Reader", "# Sci-Extract — Scientific Extraction", "# Full-Paper Markdown Reader — Router"),
        "S-1 and S-3 are the same named full-paper Chinese-English, source-grounded reader workflow, with S-3 expressly a router. S-2 is a broader scientific-extraction container. This duplicate-plus-container family does not present three independent peer routes.",
    ),
    "F-e150ebd1f0fd1a16": (
        "REJECT_GENERIC_SPECIALIST",
        ("name: trade-off-analysis", "# Dossier", "# Research Topic and Summarize Skill"),
        "S-1 is a bounded scored technology trade-off analysis and S-3 a technology/library web-research comparison, while S-2 is a cross-domain research-or-decision dossier container. The generic dossier is not a peer of the two technology-comparison specialists.",
    ),
    "F-f0a8b7937c3a6cac": (
        "REJECT_COMPONENT_OR_COMPOSITION",
        ("# Literature Sync: Zotero + Obsidian Pipeline", "# Obsidian Paper Vault", "# literature-review — a living review matrix, with optional generated Obsidian views"),
        "The originals own different linked literature-management states: BibTeX-to-Zotero/Obsidian synchronisation, PDF-folder-to-vault extraction, and review-matrix triage/projection. They can compose within one research-organisation workflow but do not share one interchangeable input/output route.",
    ),
    "F-fb8e3ca8833fd0f9": (
        "REJECT_NEAR_DUPLICATE_OR_FORK",
        ("# Citation Management", "# Citation Management", "# OpenCite CLI"),
        "S-1 and S-2 retain the same academic-paper discovery, metadata extraction, citation validation, and BibTeX workflow, with OpenAlex added in S-2. S-3 is a broader paper-retrieval CLI. This is duplicate-plus-container coverage, not three independent first routes.",
    ),
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def anchor(source: str, phrase: str) -> str:
    for line_number, line in enumerate(source.splitlines(), 1):
        if phrase in line:
            return f"L{line_number}: {line.strip()}"
    raise SystemExit(f"literal coordinator evidence not found: {phrase!r}")


def main() -> int:
    if RETURN.exists():
        raise SystemExit(f"refusing to overwrite coordinator return: {RETURN}")
    packets = read_jsonl(PACKET)
    by_token = {row["family_token"]: row for row in packets}
    if len(packets) != len(by_token) or set(by_token) != set(DECISIONS):
        raise SystemExit("B047 disagreement packet does not exactly match coordinator decision map")
    returns = []
    for token in sorted(by_token):
        decision, phrases, rationale = DECISIONS[token]
        members = by_token[token]["members"]
        evidence = {f"S-{index}": [anchor(member["complete_original_skill"], phrase)] for index, (member, phrase) in enumerate(zip(members, phrases), 1)}
        returns.append({
            "record_type": "source_native_full_source_family_review_return",
            "family_token": token,
            "decision": decision,
            "common_envelope_evidence": [item for values in evidence.values() for item in values],
            "member_contrast_evidence": evidence,
            "rationale": rationale,
            "review_boundary": "Independent full-source disagreement adjudication only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision.",
        })
    RETURN.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in returns), encoding="utf-8", newline="\n")
    print(json.dumps({"families": len(returns), "coordinator_return": str(RETURN.relative_to(WORKSPACE))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
