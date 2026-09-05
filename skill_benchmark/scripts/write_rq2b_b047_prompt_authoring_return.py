#!/usr/bin/env python3
"""Write B047's three source-bound, cue-safe natural task prompts only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
AUTHORING = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_academic_scientific_research_literature_review_citation_management_technical_writing_knowledge_organisation_statistics_mathematics_b047_2026-09-04/batch_047_full_source_review_packets/reconciliation/prompt_authoring"
PACKET = AUTHORING / "author_packet.jsonl"
RETURN = AUTHORING / "author_return.jsonl"
FAMILY = "F-fd816a343e35c608"


DRAFTS = {
    "S-1": {
        "prompt": "A research team has a project plan, one existing explanatory hypothesis, and review notes saying the proposal relies on too many optional assumptions. Produce one successor hypothesis that keeps its falsifiable causal claim while removing non-essential branches. Return a structured record with a concise statement, causal explanation, and a minimal three-to-six-step test plan that includes controls or measurable readouts. State which review concern the revision addresses.",
        "requirements": [
            "Use the supplied plan, parent hypothesis, and review material.",
            "Preserve a falsifiable causal core while reducing unnecessary assumptions.",
            "Produce one structured successor with a short decisive experiment plan and explicit readouts or controls.",
        ],
    },
    "S-2": {
        "prompt": "A team must revise a parent research hypothesis after review, but the original test depends on unavailable reagents and an instrument booking window that exceeds the eight-week project schedule. Produce one successor hypothesis that retains a testable causal mechanism while replacing impractical requirements with workable alternatives. Return a structured record with the hypothesis, mechanism, and a concrete three-to-six-step experiment using available materials, controls, and measurable decision thresholds.",
        "requirements": [
            "Use the supplied plan, parent hypothesis, and review material.",
            "Address resource, instrumentation, and timeline constraints without reducing the work to implementation notes.",
            "Preserve a testable mechanism and provide one structured successor with a concrete experiment plan.",
        ],
    },
    "S-3": {
        "prompt": "A research team has a parent hypothesis, review notes identifying vague mechanisms and claims with weak support, and research notes containing the available evidence. Produce one successor hypothesis that makes the causal claim more specific and evidence-grounded without expanding its scope. Return a structured record with a two-to-three-sentence statement and mechanism, plus a three-to-six-step experiment with controls or measurable thresholds. Explain how the revision addresses the cited weaknesses and evidence gaps.",
        "requirements": [
            "Use the supplied plan, parent hypothesis, review material, and available research evidence.",
            "Replace vague or weakly supported claims with specific, evidence-grounded causal reasoning.",
            "Produce one structured successor with a bounded experiment plan and explicit measurable checks.",
        ],
    },
}


FORBIDDEN_CUES = (
    "hypothesis-evolve-simplification", "hypothesis-evolve-feasibility", "hypothesis-evolve-grounding",
    "simplification_evolution", "feasibility_evolution", "grounding_evolution", "co-scientist",
    "panjose", "skill.original.md", "research_plan/research_plan.json", "origin.json",
    "hypothesiscontract", "packages/agent_contracts/hypothesis.py",
)


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> int:
    if RETURN.exists():
        raise SystemExit(f"refusing to overwrite B047 author return: {RETURN}")
    packets = rows(PACKET)
    if len(packets) != 1 or packets[0].get("family_token") != FAMILY:
        raise SystemExit("B047 author packet does not contain exactly the eligible family")
    hashes = {member["member_token"]: member["canonical_source_sha256"] for member in packets[0].get("members", [])}
    if set(hashes) != set(DRAFTS):
        raise SystemExit("B047 author packet target bindings are incomplete")
    output = []
    for member_token in ("S-1", "S-2", "S-3"):
        draft = DRAFTS[member_token]
        prompt = draft["prompt"]
        normalized = prompt.casefold()
        leaked = [cue for cue in FORBIDDEN_CUES if cue in normalized]
        if leaked:
            raise SystemExit(f"cue scan failed for {member_token}: {leaked}")
        output.append({
            "family_token": FAMILY,
            "target_member_token": member_token,
            "target_source_sha256": hashes[member_token],
            "prompt": prompt,
            "source_supported_distinguishing_requirements": draft["requirements"],
            "cue_audit": "CUE_SAFE: the prompt uses ordinary research-task inputs, output structure, and material constraints only. It contains no source title, provider, repository, path, hash, file name, strategy label, implementation identifier, or copied distinctive source phrase.",
        })
    RETURN.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in output), encoding="utf-8", newline="\n")
    print(json.dumps({"family": FAMILY, "prompts": len(output), "author_return_sha256": hashlib.sha256(RETURN.read_bytes()).hexdigest(), "cue_scan": "PASS"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
