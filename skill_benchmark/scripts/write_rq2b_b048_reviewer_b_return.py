#!/usr/bin/env python3
"""Write the independent, source-replayed Reviewer B return for B048."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_local_system_administration_desktop_productivity_document_conversion_ocr_pdf_spreadsheets_filesystem_file_organisation_backup_recovery_accessibility_input_b048_2026-09-04"
PACKET = ROOT / "batch_048_full_source_review_packets/reviewer_b_packet.jsonl"
RETURN = ROOT / "batch_048_full_source_review_packets/reviewer_b_return.jsonl"


# decision, one literal phrase per full original, source-grounded rationale.
REVIEWS: dict[int, tuple[str, tuple[str, str, str], str]] = {
    1: ("REJECT_COMPONENT_OR_COMPOSITION", ("speech input or voice", "navigation components", "forms, inputs, selects"), "The originals separately address speech-controlled interaction, navigation patterns, and form/validation flows. They are components of an accessible interface, not three interchangeable first routes to one bounded deliverable."),
    2: ("REJECT_COMPONENT_OR_COMPOSITION", ("workplace memory", "cross-context search", "creates your `work.local.md`"), "Workplace-context maintains memory, workplace-search queries it, and setup establishes the required workspace file. The full sources state a prerequisite-plus-operation sequence rather than peer routes."),
    3: ("PASS_TO_PROMPT_AUTHORING", ("tests whether the platform scans its skills root recursively", "cross-client convention path", "discover SKILL.md files anywhere"), "All three perform a bounded skill-discovery probe and report whether the installation location is discovered. Their source-stated location hypotheses (nested grouping, cross-client convention, and stray project directory) provide operational contrast for natural discovery questions."),
    4: ("REJECT_TOPIC_ONLY", ("民事一审诉讼与破产案件专业流程编排 Skill", "民事、刑事及劳动争议诉讼共用的案件运营管理 Skill", "刑事辩护专业流程编排 Skill"), "The originals concern civil/bankruptcy routing, cross-case operational management, and criminal-defense routing. Litigation is only a broad topic; the staged case objects and outputs are not one shared first-route envelope."),
    5: ("REJECT_GENERIC_SPECIALIST", ("List, get, upload, download, export, organize, and share Google Drive files", "List and download all files from a Google Drive folder", "Share a Google Drive folder and all its contents"), "The complete Drive source is a general command surface that explicitly includes both download and sharing, whereas the other originals are its narrow recipes. They are not three balanced independent routes."),
    6: ("REJECT_COMPONENT_OR_COMPOSITION", ("Implement disaster recovery strategies", "Business continuity and disaster recovery", "Formulates RTO/RPO targets"), "The sources respectively cover a broad DR implementation/runbook, backup policy and restore testing, and DR planning. RTO/RPO planning, backup verification, and failover implementation compose a continuity program rather than alternative routes."),
    7: ("REJECT_COMPONENT_OR_COMPOSITION", ("Route current DOCX, XLSX, PPTX, PDF, and HWPX work", "Dispatch inspected DOCX, XLSX, PPTX, PDF, and HWPX files", "Foundation for any document generation skill"), "S-1 and S-2 are closely overlapping document dispatchers, while S-3 is explicitly a foundation used internally by document skills. The family mixes duplicate routing with its underlying execution component."),
    8: ("REJECT_GENERIC_SPECIALIST", ("Initialize or update the project CLAUDE.md file", "README.md, CLAUDE.md, or AGENTS.md", "Initialize or update the main README.md file"), "The general Markdown-documentation source contains the two specialised context-file tasks. CLAUDE.md and README.md are document targets within the broader documentation workflow, not peer first routes."),
    9: ("REJECT_COMPONENT_OR_COMPOSITION", ("Tie every claim", "Split documents into retrieval units", "Improve RAG answer quality by reranking"), "Citation grounding, chunk construction, and retrieval reranking act at different stages of a retrieval-augmented answering system. They have different input/output contracts and are composable pipeline work."),
    10: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Automatically organizes files in a directory", "# File Organizer", "# File Organizer"), "Each full source organizes files into folders and addresses classification/renaming or safe execution. The different wording and amount of detail do not establish three materially distinct first-route operations."),
    11: ("PASS_TO_PROMPT_AUTHORING", ("Build M&A accretion/dilution workbooks in Excel", "Build discounted cash flow valuation workbooks in Excel", "Build comparable-company valuation workbooks in Excel"), "The sources share a bounded valuation-workbook objective while establishing distinct analytical routes: merger accretion/dilution, intrinsic DCF valuation, and comparable-company multiples. Each supports a source-specific natural modelling request."),
    12: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Turn a PRD into a multi-phase implementation plan", "Turn a spec into a multi-phase implementation plan", "# PRD to Plan"), "All three originals prescribe multi-phase tracer-bullet implementation planning and use substantially the same plan artifact. PRD/spec wording does not provide three independent routes."),
    13: ("REJECT_NO_BOUNDED_ENVELOPE", ("name: stellar-roadmap", "name: looper", "Deprecated compatibility alias"), "The originals are compatibility/delegation stubs for unrelated canonical skills (roadmap, control graph, and codebase structure). They do not establish a common bounded objective, input, or output envelope."),
    14: ("REJECT_TOPIC_ONLY", ("Export a Google Sheets spreadsheet as a CSV", "Export Google Contacts directory to a Google Sheets spreadsheet", "Google Sheets: Append a row"), "A Sheets backup export, Contacts-to-Sheets export, and an append operation have distinct input objects and outputs. Google Sheets is only a tool/topic relation."),
    15: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Compact the current conversation into a handoff document", "Compact the current conversation into a handoff document", "Compact the current conversation into a durable handoff document"), "Each source takes a current conversation and produces a handoff for another agent/session. Additional detail about durability or resuming does not create independent first-route tasks."),
    16: ("REJECT_GENERIC_SPECIALIST", ("Organizes your notes and documents into folders by topic", "Organizes files or folders into a cleaner structure", "organizes your files and folders across your computer"), "The note organiser is a topical specialisation, while the other sources operate at general file/folder or computer-wide scope. The family is generic-versus-specialist coverage rather than three balanced alternatives."),
    17: ("REJECT_TOPIC_ONLY", ("Establish persistence on Windows and Linux systems", "Escalate privileges on Linux systems", "Escalate privileges on Windows systems"), "Persistence and privilege escalation are distinct post-exploitation operations; Linux and Windows escalation are platform-specific variants of only one of them. The family has no shared three-way bounded first-route objective."),
    18: ("REJECT_COMPONENT_OR_COMPOSITION", ("Comprehensive PDF manipulation toolkit", "Comprehensive PDF manipulation toolkit", "Fill out PDF forms programmatically"), "S-1 and S-2 are materially the same broad PDF manipulation guide, while S-3 is the narrower form-filling capability explicitly contained within that surface. This is duplicate-plus-specialist composition."),
    19: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Generate a Product Requirements Document", "Generate comprehensive Product Requirements Documents", "requirements gathering, analysis, and PRD generation"), "All three sources gather requirements and generate a structured PRD. Their differing templates, dialogue style, and save locations do not make them independent operational routes."),
    20: ("REJECT_GENERIC_SPECIALIST", ("Review a document against its SDLC lifecycle context", "Review skill documents and skill-focused changes", "Review project documents such as issues, ADRs, architecture documents"), "The sources combine a lifecycle-context review, a skill-only review, and a broad project-artifact review. The latter two scope review by artifact type, while lifecycle consistency is a different specialised dimension; they are not balanced first routes."),
    21: ("PASS_TO_PROMPT_AUTHORING", ("Inspect, filter, aggregate, and clean CSV/TSV data", "Clean and normalize messy CSV/TSV files", "Clean up messy spreadsheet data"), "The originals share a bounded tabular-data-cleaning outcome but support distinct operational routes: lightweight CSV/TSV inspection, loss-accounted repair of malformed delimited files, and in-sheet/spreadsheet normalization. The contrasts are directly source-stated and promptable."),
    22: ("REJECT_TOPIC_ONLY", ("Parse and generate CSV files", "Parse/write FCS (Flow Cytometry) files", "Parse, transform, and analyze CSV files"), "The FlowIO source operates on specialised flow-cytometry FCS datasets, while the other two operate on CSV. CSV export is an optional interoperability step, not a shared three-skill first-route envelope."),
    23: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("accessibility (a11y) debugging and auditing", "Audits keyboard navigation, focus order", "Checks a web interface for accessibility issues"), "All three inspect web-interface accessibility across labels, focus, keyboard access, ARIA, and contrast. Tooling and prose differences do not establish three independent first-route operations."),
    24: ("REJECT_TOPIC_ONLY", ("prepares a redaction plan", "Answer questions about PDF content", "Answers specific questions from PDF content"), "PDF redaction planning and PDF question answering have different objectives and outputs; S-2 and S-3 overlap QA, but that does not form a three-way shared envelope."),
    25: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Capture a repeatable process from the current session", "create a new LQ.AI skill", "Distill a reusable skill from anything"), "Each original elicits or derives a reusable SKILL.md/folder from user knowledge or source material. Product context and source options do not create three distinct first-route operations."),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def line_anchor(source: str, phrase: str) -> str:
    for number, line in enumerate(source.splitlines(), 1):
        if phrase in line:
            return f"L{number}: {line.strip()}"
    raise SystemExit(f"literal evidence not found: {phrase!r}")


def main() -> int:
    if RETURN.exists():
        raise SystemExit("refusing to overwrite existing B048 Reviewer B return")
    packets = read_jsonl(PACKET)
    if len(packets) != 25 or set(REVIEWS) != set(range(1, 26)):
        raise SystemExit("packet/review cardinality mismatch")
    returns: list[dict[str, Any]] = []
    for rank, packet in enumerate(packets, 1):
        if packet["record_type"] != "source_native_full_source_reviewer_b_packet" or len(packet["members"]) != 3:
            raise SystemExit(f"malformed Reviewer B packet at rank {rank}")
        decision, phrases, rationale = REVIEWS[rank]
        evidence: dict[str, list[str]] = {}
        for member, phrase in zip(packet["members"], phrases):
            source = member["complete_original_skill"]
            if hashlib.sha256(source.encode("utf-8")).hexdigest() != member["source_byte_sha256"]:
                raise SystemExit(f"source hash mismatch at rank {rank}, {member['member_token']}")
            evidence[member["member_token"]] = [line_anchor(source, phrase)]
        returns.append({
            "record_type": "source_native_full_source_reviewer_b_return",
            "family_token": packet["family_token"],
            "decision": decision,
            "common_envelope_evidence": [entry for entries in evidence.values() for entry in entries],
            "member_contrast_evidence": evidence,
            "rationale": rationale,
            "review_boundary": "Reviewer B full-source family assessment only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision.",
        })
    RETURN.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in returns), encoding="utf-8")
    counts = {decision: sum(row["decision"] == decision for row in returns) for decision in sorted({row["decision"] for row in returns})}
    print(json.dumps({"return_sha256": hashlib.sha256(RETURN.read_bytes()).hexdigest(), "families": len(returns), "sources_replayed": 75, "decision_counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
