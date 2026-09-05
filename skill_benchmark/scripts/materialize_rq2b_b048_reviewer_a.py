#!/usr/bin/env python3
"""Materialise the sole full-source Reviewer A packet and return for B048."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_local_system_administration_desktop_productivity_document_conversion_ocr_pdf_spreadsheets_filesystem_file_organisation_backup_recovery_accessibility_input_b048_2026-09-04"
INPUT = ROOT / "b048_source_native_three_skill_full_original_packets.jsonl"
LEDGER = ROOT / "source_native_reciprocal_family_ledger.jsonl"
PACKET_DIR = ROOT / "batch_048_full_source_review_packets"
PACKET = PACKET_DIR / "reviewer_a_packet.jsonl"
RETURN = PACKET_DIR / "reviewer_a_return.jsonl"

# Decisions are made from the complete preserved originals. The materialiser
# replays literal source anchors from those originals before it emits a return.
DECISIONS: dict[int, tuple[str, str]] = {
    1: ("REJECT_COMPONENT_OR_COMPOSITION", "Speech input, navigation, and forms are separate interface components with different accessibility checks; a page can require them in sequence rather than choosing one as an alternative first route."),
    2: ("REJECT_COMPONENT_OR_COMPOSITION", "The sources respectively maintain workplace memory, search it, and install/configure the office system. Search and setup consume or enable the memory workflow rather than offering peer routes."),
    3: ("REJECT_TOPIC_ONLY", "The three probes test distinct installation locations: a grouping directory, a cross-client convention, and an unrecognised stray path. They share skill-discovery testing only at a broad topic level."),
    4: ("REJECT_GENERIC_SPECIALIST", "The generic litigation-case manager is mixed with civil/bankruptcy and criminal-defence stage dispatchers. Their legal case-type boundaries and routing roles are not a balanced peer first-route envelope."),
    5: ("REJECT_COMPONENT_OR_COMPOSITION", "The general Drive CLI includes finding, downloading, and sharing, while the other two sources are its specific folder-download and team-sharing operations. The specialised actions are components of the general route."),
    6: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three complete sources formulate RTO/RPO, failover, backup, and recovery procedures. Their policy, strategy, and template presentation varies, but the operational continuity route overlaps directly."),
    7: ("REJECT_COMPONENT_OR_COMPOSITION", "The first two sources are nearly identical document-type dispatchers, while the Python sandbox source supplies the document-generation execution environment they route to. This is duplicate-plus-foundation coverage."),
    8: ("REJECT_GENERIC_SPECIALIST", "The CLAUDE.md and README sources initialise individual project files, while the markdown-management source is the broader multi-file documentation container. The generic and file-specialist roles are unbalanced."),
    9: ("REJECT_COMPONENT_OR_COMPOSITION", "Citation grounding, semantic chunking, and retrieval reranking are successive retrieval-system stages with different inputs and outputs. They are composable mechanisms, not alternative first routes."),
    10: ("REJECT_NEAR_DUPLICATE_OR_FORK", "Each complete original organises a directory into folders by type or rules, with overlapping duplicate handling and cleanup. Content analysis, configurable rules, and dry-run/undo are variants inside the same organisation route."),
    11: ("REJECT_TOPIC_ONLY", "The merger, DCF, and comparable-company workbooks answer distinct valuation and transaction questions. Excel is a shared tool, not a common bounded objective or deliverable."),
    12: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three sources turn a PRD or specification into a phased tracer-bullet implementation plan, and the first and third replicate the same six-step process. Their variation does not create three distinct routes."),
    13: ("REJECT_NO_BOUNDED_ENVELOPE", "Each source is an explicit deprecated compatibility alias that delegates to a different canonical skill. The aliases contain no independent common objective, input contract, or deliverable."),
    14: ("REJECT_TOPIC_ONLY", "Exporting a sheet to CSV, exporting contacts to a sheet, and appending a row have different source objects and outputs. Spreadsheet use alone is too broad to be a shared task envelope."),
    15: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The first two sources contain the same conversation-compaction instruction, and the third provides the same durable handoff artifact with additional pickup guidance. This is duplicate-plus-expanded coverage."),
    16: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three sources organise notes or files into folders and include context- or duplicate-aware cleanup variants. The scope and output overlap directly rather than establishing distinct first-route roles."),
    17: ("REJECT_COMPONENT_OR_COMPOSITION", "The persistence source maintains access after compromise, whereas the Linux and Windows sources escalate privileges through platform-specific methods. Privilege escalation can precede persistence, so the workflows are composable stages."),
    18: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The first two originals are overlapping PDF processing guides for extraction and manipulation, while the third is a form-filling subset in the same PDF tool domain. This is duplicate-plus-specialised coverage."),
    19: ("REJECT_NEAR_DUPLICATE_OR_FORK", "The three sources all gather requirements through questions and produce a PRD; the third's scoring and iterative refinement are workflow variations rather than a distinct first-route role."),
    20: ("REJECT_GENERIC_SPECIALIST", "The skill-document reviewer is specialised to SKILL.md changes, the lifecycle review is SDLC-context-bound, and artifact review is the broader project-document container. The source boundaries do not form peer alternatives."),
    21: ("REJECT_GENERIC_SPECIALIST", "CSV Tools combines inspection, filtering, aggregation, and cleanup, whereas CSV Cleaner and Clean Data focus on repair/normalisation. The broader analysis container is not balanced with the cleaning specialists."),
    22: ("REJECT_TOPIC_ONLY", "The two CSV sources parse or transform CSV records, but FlowIO reads and writes flow-cytometry FCS data with domain-specific events and metadata. File processing is only a broad shared topic."),
    23: ("REJECT_NEAR_DUPLICATE_OR_FORK", "All three sources audit the same web-interface accessibility concerns: labels, keyboard/focus, semantics, contrast, and screen-reader usability. Chrome DevTools/Lighthouse is a tooling variant within that same audit route."),
    24: ("REJECT_TOPIC_ONLY", "PDF redaction planning, general PDF question answering/extraction, and specific question answering produce different outputs and have different safety goals. PDF input alone is not a bounded common envelope."),
    25: ("REJECT_NEAR_DUPLICATE_OR_FORK", "Each complete original interviews or distils a reusable procedure and writes a SKILL.md. The source material and platform conventions vary, but the skill-authoring route overlaps directly."),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def source_anchor(source: str) -> str:
    """Return a source-body anchor without using a path, origin, or rank."""
    for number, line in enumerate(source.splitlines(), 1):
        title = line.strip()
        if title.startswith("# ") and set(title[2:]) != {"="}:
            return f"L{number}: {title}"
    for number, line in enumerate(source.splitlines(), 1):
        if line.lstrip().startswith("description:"):
            return f"L{number}: {line.strip()}"
    raise SystemExit("complete source has no usable literal anchor")


def main() -> int:
    if PACKET_DIR.exists():
        raise SystemExit(f"refusing to overwrite B048 Reviewer A material: {PACKET_DIR}")
    rows, ledger = read_jsonl(INPUT), read_jsonl(LEDGER)
    if len(rows) != 25 or len(ledger) != 25 or set(DECISIONS) != set(range(1, 26)):
        raise SystemExit("B048 reviewer input cardinality/decision map mismatch")
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != "137fb6490f536a59e1a6db5b302ec2af1af4fb418f8bbef2018e3f8c81006993":
        raise SystemExit("immutable B048 full-original packet hash mismatch")
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest() != "5333e3adc2f99fda780fd4f6e6fe4580713ab404013d1526faaee379b868d166":
        raise SystemExit("immutable B048 family-ledger hash mismatch")
    packets: list[dict[str, Any]] = []
    returns: list[dict[str, Any]] = []
    for row in rows:
        rank = int(row["batch_rank"])
        if row["family_id"] != ledger[rank - 1]["family_id"]:
            raise SystemExit(f"ledger family mismatch at B048 rank {rank}")
        members, anchors = [], {}
        for position, member in enumerate(row["members"], 1):
            originals = member["preserved_complete_original_sources"]
            if not originals:
                raise SystemExit(f"missing complete source at B048 rank {rank}, member {position}")
            source = originals[0]["preserved_original_skill_utf8"]
            expected_hash = str(member["canonical_source_sha256"])
            if any(hashlib.sha256(item["preserved_original_skill_utf8"].encode("utf-8")).hexdigest() != expected_hash
                   for item in originals):
                raise SystemExit(f"complete-source hash mismatch at B048 rank {rank}, member {position}")
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
        raise SystemExit("B048 Reviewer A packet source cardinality mismatch")
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
