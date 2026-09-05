#!/usr/bin/env python3
"""Repair declared Round 41 C0B citation drift without revising C0B judgments."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


RepairKey = tuple[str, str, int]


REPAIRS: dict[RepairKey, tuple[str, str]] = {
    (
        "R41-C0A-content_productivity-01",
        "r21m1-superamped-ai-marketing-skills-skills-research-competitor-content-analysis",
        0,
    ): (
        '"analyze what a competitor publishes"',
        "Use this skill to analyze what a competitor publishes, which content earns estimated traffic, the SEO plays they use, and where gaps exist. Trigger it before creating or refreshing a content strategy or when investigating a competitor's organic content performance.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "r21m1-superamped-ai-marketing-skills-skills-research-competitor-content-analysis",
        1,
    ): ('"Content Gap Analysis"', "### Step 8: Content Gap Analysis"),
    (
        "R41-C0A-content_productivity-01",
        "wave003mc-rampstack-seo-content-gap-audit",
        0,
    ): (
        '"Audit content gaps and decay using Ahrefs MCP data"',
        "Audit content gaps and decay using Ahrefs MCP data: missing topics, thin coverage, outdated content, and decaying pages. Use this skill when planning a content roadmap, refreshing a stale catalog, building topical authority, or identifying which existing pages need update versus replacement. Triggers on content gap, content audit, content refresh, content roadmap, decaying content, content decay, topical authority, what topics should we cover, where is competitor content stronger. Also triggers when organic traffic is flat despite consistent publishing.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "wave003mc-rampstack-seo-content-gap-audit",
        1,
    ): (
        '"Produces a roadmap of create, update, merge, and prune actions"',
        "Find content gaps and decay using Ahrefs MCP data. Stack-agnostic. Produces a roadmap of create, update, merge, and prune actions across the existing content catalog and identified topic gaps.",
    ),
    (
        "R41-C0A-content_productivity-01",
        "r20m1-0xF4ng-aether-growth-fieldwork-pmm-content-review",
        0,
    ): ('"Scores content pieces and experiment specs before publication or launch."', "Scores content pieces and experiment specs before publication or launch."),
    (
        "R41-C0A-content_productivity-01",
        "r20m1-0xF4ng-aether-growth-fieldwork-pmm-content-review",
        1,
    ): ('"Verdict: APPROVE / REVISE / REJECT."', "sessions. Verdict: APPROVE / REVISE / REJECT."),
    (
        "R41-C0A-document_research-01",
        "r35m1-LARi-UQAC-ResearchTools-claude-skills-paper2talk",
        1,
    ): (
        "This skill covers that step: the deck, the figures at projector resolution, the timed speaker notes, and the printable PDF.",
        "the next deliverable of every accepted paper. This skill covers that step: the deck, the",
    ),
    (
        "R41-C0A-document_research-01",
        "r18m1-ShaishavMaisuria-research-paper-lifecycle-skills-skills-make-slides",
        1,
    ): (
        "Turn an accepted (or nearly-done) paper into a conference talk deck — Beamer `.tex` or Marp markdown — built around a problem-first story, one claim per slide, the paper's own figures, and a slide count the slot can actually afford.",
        "Turn an accepted (or nearly-done) paper into a conference talk deck —",
    ),
    (
        "R41-C0A-document_research-02",
        "r21m1-aniketkrs-research-paper-skills-read-research-paper",
        1,
    ): (
        "It produces a visual, multi-layer rendering: technical depth + plain English + mind maps + method flowcharts + key-finding infographics + comparison tables + related-work timelines.",
        "It produces a visual,",
    ),
    (
        "R41-C0A-product_design-01",
        "r20m1-my-stacks-claude-code-skills-claude-skills-design-qa-lite",
        0,
    ): (
        "Use when reviewing a deployed web URL for responsive layout, accessibility, Core Web Vitals, and SEO basics in any agent that supports markdown skills.",
        "You're reviewing a deployed web URL. Run a multi-pass headless audit and produce a structured report.",
    ),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--packet-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()

    packets = {
        (row["proposal_id"], row["skill_id"]): Path(row["packet_original_path"])
        for row in read_jsonl(args.packet_manifest)
    }
    rows = read_jsonl(args.input)
    repaired: list[dict[str, Any]] = []
    seen: set[RepairKey] = set()
    scalar_risk_repairs: list[str] = []
    for row in rows:
        proposal_id = row["proposal_id"]
        for evidence in row["candidate_evidence"]:
            skill_id = evidence["skill_id"]
            values = evidence["evidence_substrings"]
            for index, value in enumerate(values):
                key = (proposal_id, skill_id, index)
                if key not in REPAIRS:
                    continue
                old, new = REPAIRS[key]
                if value != old:
                    raise SystemExit(f"unexpected_old_evidence:{key}")
                source = packets[key[:2]].read_text(encoding="utf-8")
                if new not in source:
                    raise SystemExit(f"replacement_not_literal:{key}")
                values[index] = new
                seen.add(key)
        if isinstance(row.get("route_out_or_containment_risks"), str):
            row["route_out_or_containment_risks"] = [row["route_out_or_containment_risks"]]
            scalar_risk_repairs.append(proposal_id)
        repaired.append(row)

    if seen != set(REPAIRS):
        raise SystemExit(f"repair_coverage_mismatch:missing={sorted(set(REPAIRS) - seen)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in repaired), encoding="utf-8")
    log = {
        "status": "C0B_ROUND41_LITERAL_EVIDENCE_AND_SCHEMA_REPAIR_PENDING_REVALIDATION_NOT_A_CLUSTER_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "literal_evidence_repairs": [
            {
                "proposal_id": proposal_id,
                "skill_id": skill_id,
                "evidence_index": index,
                "old_nonliteral_evidence": old,
                "replacement_exact_source_substring": new,
            }
            for (proposal_id, skill_id, index), (old, new) in sorted(REPAIRS.items())
        ],
        "scalar_to_singleton_risk_list_repairs": scalar_risk_repairs,
        "invariants": [
            "No C0B status, candidate membership, source-review rationale, or risk text changed.",
            "Every replacement evidence substring was verified against its matching exact packet original before writing.",
            "No prompt, label, acceptable set, retrieval input, model call, metric, or benchmark result was created.",
        ],
    }
    args.repair_log.write_text(json.dumps(log, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"literal_evidence_repairs": len(seen), "scalar_risk_repairs": len(scalar_risk_repairs)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
