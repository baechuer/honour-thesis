#!/usr/bin/env python3
"""Materialise the sole full-source Reviewer A packet and return for B047."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_academic_scientific_research_literature_review_citation_management_technical_writing_knowledge_organisation_statistics_mathematics_b047_2026-09-04"
INPUT = ROOT / "b047_source_native_three_skill_full_original_packets.jsonl"
LEDGER = ROOT / "source_native_reciprocal_family_ledger.jsonl"
PACKET_DIR = ROOT / "batch_047_full_source_review_packets"
PACKET = PACKET_DIR / "reviewer_a_packet.jsonl"
RETURN = PACKET_DIR / "reviewer_a_return.jsonl"

# Decisions are made from the complete preserved originals.  The materialiser
# replays literal source anchors from those originals before it emits a return.
DECISIONS: dict[int, tuple[str, str]] = {
    1: ("REJECT_COMPONENT_OR_COMPOSITION", "The two COMET build workflows use the reference-selection workbook produced by the middle source; these are dependent pipeline stages rather than three alternative first routes."),
    2: ("REJECT_TOPIC_ONLY", "Open redirects, HTTP parameter pollution, and clickjacking are distinct web-vulnerability objects and proof methods. Security testing is only a broad topic, not one bounded input/output task."),
    3: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three complete originals implement multi-perspective academic manuscript critique with overlapping full, quick, methodology, re-review, guided, and calibration modes. The variation is not three material first routes."),
    4: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The first two originals are citation-management variants with the same discovery, metadata, validation, and BibTeX workflow; the third is a broader CLI containing that workflow. This is duplicate-plus-container coverage."),
    5: ("REJECT_NEAR_DUPLICATE_OR_FORK", "Each source authors or revises an agent SKILL.md and supplies an overlapping structure/validation workflow. Different authoring heuristics do not establish three distinct first-route roles."),
    6: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The first and third originals are full-paper reader variants with the same source-grounded bilingual-reader output, while the middle extraction source is a broader analysis container. The set is not three independent peer routes."),
    7: ("REJECT_COMPONENT_OR_COMPOSITION", "The first two originals are duplicated product-discovery cycles; the PRD source consumes problem framing and research synthesis into a requirements document. Discovery and PRD authoring are composable stages."),
    8: ("REJECT_COMPONENT_OR_COMPOSITION", "The manuscript drafter and Nature-style writing source create or restructure sections, whereas the polishing source edits finished prose. Drafting and polishing are sequential writing stages, not interchangeable first routes."),
    9: ("REJECT_COMPONENT_OR_COMPOSITION", "The survey source produces a literature-survey artifact, the paper source produces a research paper, and the AI4S meta-skill chains literature survey, experiment, and paper stages. They do not share one same bounded deliverable."),
    10: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The first two originals turn a process description into a numbered SOP. The third is a workflow-model-specific SOP procedure, so the set is duplicated general SOP writing plus a specialised variant rather than three peers."),
    11: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three originals run multi-source research, verify sources, and synthesize a cited result. The agent-lab orchestration is a method variation inside the same research route, while the two Deep Research sources overlap directly."),
    12: ("REJECT_COMPONENT_OR_COMPOSITION", "BibTeX-to-Zotero/Obsidian synchronisation, PDF-to-vault extraction, and review-matrix triage/projecting are linked literature-organisation stages with different inputs and outputs."),
    13: ("REJECT_TOPIC_ONLY", "Niche selection, affiliate-program comparison, and competitor-strategy reverse engineering address different decision objects; affiliate research is only a broad relationship."),
    14: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three originals use the same public/internal/confidential/restricted data-classification regime. Policy definition and enforcement detail are variations within one classification framework rather than distinct first routes."),
    15: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The three sources share the same resource-linker procedure, input contract, and output structure, changing only repository, platform, or SRE domain labels."),
    16: ("REJECT_GENERIC_SPECIALIST", "The general reporter research-brief source is a broad container, while the source-background and funding-source briefs are specialised investigations with distinct required subjects and outputs."),
    17: ("REJECT_GENERIC_SPECIALIST", "The generic deep-research source covers any topic, while the Notion source is workspace-bound and the RSS source is feed/web-brief specific. Their concrete source boundaries and outputs are not a peer three-route envelope."),
    18: ("REJECT_GENERIC_SPECIALIST", "Technology trade-off analysis is a comparison-matrix specialist, dossier is a general research/decision container, and the web-research source produces a cited recommendation summary. The generic and specialised roles are unbalanced."),
    19: ("REJECT_TOPIC_ONLY", "Document Q&A, literature surveying, and Exa semantic search operate on different source collections and output types. Citing sources is only a shared mechanism."),
    20: ("REJECT_GENERIC_SPECIALIST", "The first and third originals polish supplied academic prose, while the middle academic-writing source also drafts, revises, and audits several document genres. It is a broad container rather than a peer polishing route."),
    21: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The three normalizers use the same naming/schema/taxonomy procedure and differ only by SRE, repository, or platform operations labels."),
    22: ("REJECT_GENERIC_SPECIALIST", "The first two originals are general academic-paper-writing guides, while the third is specialised to ML/CV/NLP/systems papers and submission artefacts. The set mixes generic and specialised first routes."),
    23: ("REJECT_TOPIC_ONLY", "The complete sources apply different named books to management, usability, and feedback conversations. Book-grounded advice is only a broad topic, not a common bounded task."),
    24: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The first and third originals are overlapping Matplotlib scientific-plotting guides; Plotly is a different interactive-library route. This duplicate-plus-alternative set is not three independent routes."),
    25: ("PASS_TO_PROMPT_AUTHORING", "Each source transforms one parent hypothesis into exactly one child hypothesis. Simplification, experimental/operational feasibility, and evidence/literature grounding are explicit, independent transformation criteria that make different first routes natural for the same bounded hypothesis-refinement request."),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def source_anchor(source: str) -> str:
    """Return a source-body anchor without using a path, origin, or rank."""
    for number, line in enumerate(source.splitlines(), 1):
        if line.strip().startswith("# "):
            return f"L{number}: {line.strip()}"
    for number, line in enumerate(source.splitlines(), 1):
        if line.lstrip().startswith("description:"):
            return f"L{number}: {line.strip()}"
    raise SystemExit("complete source has no usable literal anchor")


def main() -> int:
    if PACKET_DIR.exists():
        raise SystemExit(f"refusing to overwrite B047 Reviewer A material: {PACKET_DIR}")
    rows, ledger = read_jsonl(INPUT), read_jsonl(LEDGER)
    if len(rows) != 25 or len(ledger) != 25 or set(DECISIONS) != set(range(1, 26)):
        raise SystemExit("B047 reviewer input cardinality/decision map mismatch")
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != "f6fdcb3783a2362e55e7b3b167e2b2285db4be3e058c09531b080879fcb63018":
        raise SystemExit("immutable B047 full-original packet hash mismatch")
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest() != "d4216d892e58cf67afecd5a0425d89ae17dc7e88c324faa02cdb77989d234291":
        raise SystemExit("immutable B047 family-ledger hash mismatch")
    packets: list[dict[str, Any]] = []
    returns: list[dict[str, Any]] = []
    for row in rows:
        rank = int(row["batch_rank"])
        if row["family_id"] != ledger[rank - 1]["family_id"]:
            raise SystemExit(f"ledger family mismatch at B047 rank {rank}")
        members, anchors = [], {}
        for position, member in enumerate(row["members"], 1):
            originals = member["preserved_complete_original_sources"]
            if not originals:
                raise SystemExit(f"missing complete source at B047 rank {rank}, member {position}")
            source = originals[0]["preserved_original_skill_utf8"]
            expected_hash = str(member["canonical_source_sha256"])
            if any(hashlib.sha256(item["preserved_original_skill_utf8"].encode("utf-8")).hexdigest() != expected_hash
                   for item in originals):
                raise SystemExit(f"complete-source hash mismatch at B047 rank {rank}, member {position}")
            token = f"S-{position}"
            anchors[token] = [source_anchor(source)]
            members.append({"member_token": token, "source_byte_sha256": expected_hash,
                            "complete_original_skill": source,
                            "review_instruction": "Read the complete original skill. Cite literal excerpts or line locations; do not infer missing capability from topic familiarity."})
        family_token = "F-" + str(row["family_id"]).removeprefix("SN-LEX-")
        packets.append({"record_type": "source_native_full_source_reviewer_a_packet", "family_token": family_token,
                        "members": members,
                        "rubric": {"pass": "Three independent first-route skills share a bounded objective/input/output envelope, present plausible natural confusion, and have source-supported distinct roles or tools.",
                                   "reject_codes": ["REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION", "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE"],
                                   "rule": "The complete original source is authoritative. Do not use discovery rank, source path, origin, prior outcomes, or another reviewer's judgement."}})
        decision, rationale = DECISIONS[rank]
        returns.append({"record_type": "source_native_full_source_reviewer_a_return", "family_token": family_token,
                        "decision": decision, "common_envelope_evidence": [item for values in anchors.values() for item in values],
                        "member_contrast_evidence": anchors, "rationale": rationale,
                        "review_boundary": "Reviewer A full-source family assessment only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision."})
    source_hashes = {member["source_byte_sha256"] for packet in packets for member in packet["members"]}
    if len(source_hashes) != 75:
        raise SystemExit("B047 Reviewer A packet source cardinality mismatch")
    PACKET_DIR.mkdir(parents=True)
    write_jsonl(PACKET, packets)
    write_jsonl(RETURN, returns)
    print(json.dumps({"packet_sha256": hashlib.sha256(PACKET.read_bytes()).hexdigest(),
                      "return_sha256": hashlib.sha256(RETURN.read_bytes()).hexdigest(),
                      "families": len(returns), "source_hashes": len(source_hashes),
                      "decision_counts": dict(sorted(Counter(row["decision"] for row in returns).items()))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
