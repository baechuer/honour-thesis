#!/usr/bin/env python3
"""Materialise B045 Reviewer A packets and the sole Reviewer A return.

This bounded source review consumes only the immutable B045 full-original
packets. It produces no second-reviewer, reconciliation, provenance, prompt,
adequacy, admission, selector, or metric material.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_collaboration_project_management_meeting_notes_email_calendar_crm_customer_support_workflow_automation_b045_2026-09-04"
INPUT = ROOT / "b045_source_native_three_skill_full_original_packets.jsonl"
LEDGER = ROOT / "source_native_reciprocal_family_ledger.jsonl"
PACKET_DIR = ROOT / "batch_045_full_source_review_packets"
PACKET = PACKET_DIR / "reviewer_a_packet.jsonl"
RETURN = PACKET_DIR / "reviewer_a_return.jsonl"

# Each tuple is (decision, evidence phrase for S-1/S-2/S-3, source-grounded
# rationale). Every phrase must replay literally in the immutable full source.
DECISIONS: dict[int, tuple[str, tuple[str, str, str], str]] = {
    1: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Plan and prioritize product roadmaps", "Product roadmap frameworks", "Build a Now / Next / Later prioritized roadmap"), "All three deliver a product roadmap and prioritisation route; framework or format wording does not establish three materially distinct first routes."),
    2: ("PASS_TO_PROMPT_AUTHORING", ("Self-host customer support with Chatwoot", "Add customer messaging and support with Intercom", "Add live chat and customer support with Crisp"), "The bounded task is establishing customer-facing support and messaging. Chatwoot is explicitly self-hosted/open-source, Intercom adds onboarding and product-tour capability, and Crisp is scoped to chat/help-desk/knowledge-base deployment; these are independent platform routes with source-stated operational differences."),
    3: ("REJECT_TOPIC_ONLY", ("Run outbound GTM email", "Triage, reply, escalate, follow up, and close support email", "Book time, check calendar availability, and handle scheduling email"), "A shared Mermail mailbox is topical infrastructure only. The sources serve outbound GTM, support resolution, and calendar booking respectively, with different objectives and outputs."),
    4: ("REJECT_TOPIC_ONLY", ("create, find, update, and delete contacts", "read and search mail, send/reply/forward", "send transactional email, manage contacts and segments"), "Contact management, a general Outlook suite, and transactional delivery do not define one concrete common task envelope."),
    5: ("REJECT_COMPONENT_OR_COMPOSITION", ("Monitor and protect your email sender reputation", "Process email bounces and protect sender reputation", "Implement email rate limiting and volume controls"), "Reputation monitoring, bounce handling, and rate limiting are linked controls within sender-health operations rather than alternative first routes for one bounded task."),
    6: ("PASS_TO_PROMPT_AUTHORING", ("Automate Monday.com workflows, board management", "Automate Asana project management workflows", "Automate Trello board management, card workflows"), "The bounded task is configuring automated collaborative work management. The complete sources establish independent platform-specific routes: Monday boards/cross-board integrations, Asana task tracking/reporting, and Trello cards/power-ups."),
    7: ("REJECT_GENERIC_SPECIALIST", ("Daily inbox triage", "Email triage that summarizes unread email", "Quick inbox scan"), "The first two are the same inbox-triage route, while the third is only a lightweight recent-message scan; this is duplicate/generic coverage rather than three balanced routes."),
    8: ("REJECT_NO_BOUNDED_ENVELOPE", ("Create recurring focus time blocks", "Time-block planner", "Designs a daily schedule that protects deep work"), "Calendar blocking, assigning pasted tasks to slots, and a broader daily-routine design do not share one sufficiently concrete input/output envelope."),
    9: ("REJECT_TOPIC_ONLY", ("Send emails through SMTP", "building Laravel emails", "Compose unsent email drafts"), "SMTP delivery, Laravel implementation work, and mailbox-native draft staging are different tasks; email is only the lexical topic."),
    10: ("REJECT_TOPIC_ONLY", ("CRM enrichment", "buyer persona", "prospect research"), "Record enrichment, persona definition, and account research have distinct inputs and deliverables despite all being adjacent to CRM work."),
    11: ("REJECT_GENERIC_SPECIALIST", ("Write clear, searchable help center articles", "Handles customer support efficiently", "customer support lead for drafting support responses"), "The latter two are broad support containers that subsume the specialised help-centre article route, not distinct alternatives of equal scope."),
    12: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Converts raw meeting notes or transcripts", "Turn raw meeting/call notes or a transcript into clean minutes", "Turn raw meeting transcripts into structured notes"), "All members transform a meeting transcript into the same summary/decisions/actions record; the source texts do not establish operationally distinct routes."),
    13: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Himalaya CLI: IMAP/SMTP email from terminal", "SMTP send, IMAP read", "CLI to manage emails via IMAP/SMTP"), "Two members are explicitly Himalaya terminal IMAP/SMTP clients and the remaining member supplies the same read/send protocol surface, so the sources do not provide three distinct routes."),
    14: ("REJECT_GENERIC_SPECIALIST", ("fresh email composed from scratch", "Draft a professional, audience-aware email or reply", "Drafts a reply message or email from conversation context"), "The middle source is a broad email-drafting container over the fresh-outbound and reply-specific members."),
    15: ("REJECT_GENERIC_SPECIALIST", ("personalized outreach messages by pulling context from Dataverse records", "Draft professional emails for various business scenarios", "Draft clear, well-structured emails and messages"), "The latter two are generic professional-email drafting; the Dataverse member is a context-bound outreach specialist, producing a generic-specialist set."),
    16: ("REJECT_COMPONENT_OR_COMPOSITION", ("Plan a strategic roadmap across prioritization", "Facilitates strategic planning sessions", "orchestrating prioritization, epic definition, stakeholder alignment"), "Business strategy facilitation is upstream of a roadmap, while the third member explicitly orchestrates the roadmap subskills; the packet mixes lifecycle/composition relations."),
    17: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Extracts decisions, action items, owners", "Analyze meeting transcripts to extract decisions, action items", "Extracts action items from meeting notes or transcripts"), "The sources share the same transcript-to-actions route; sentiment and follow-up additions do not create three materially distinct first routes."),
    18: ("REJECT_COMPONENT_OR_COMPOSITION", ("Add a list of attendees to an existing Google Calendar event", "meeting preparation with gog, including attendees", "Share Google Drive files with all attendees"), "Adding attendees, preparing an event, and sharing files with its attendees are dependent operations in one meeting workflow rather than alternatives."),
    19: ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Check a piece of writing for grammar, spelling, punctuation", "reviewing written content for grammar, spelling, punctuation", "Advisory copy-edit of prose"), "The first two are materially the same proofreading route; the advisory no-rewrite boundary of the third does not establish three independent roles."),
    20: ("REJECT_NO_BOUNDED_ENVELOPE", ("adding real-time collaboration features to web applications", "building collaborative applications", "add live features to applications using pub/sub channels"), "The full sources span collaboration UI features, CRDT document synchronisation, and general real-time messaging infrastructure; there is no single concrete task/input/output envelope beyond a broad technical topic."),
    21: ("REJECT_COMPONENT_OR_COMPOSITION", ("Generate closure-grade HE eval and drift proof", "Convert approved HE cognition into small live-ready Linear execution tracking", "Create bounded, evidence-backed Harness Engineering specs"), "Evidence/validation, execution tracking, and specification are distinct lifecycle stages that may compose; they are not alternative first routes."),
    22: ("REJECT_GENERIC_SPECIALIST", ("Turns product strategy into a themed Now/Next/Later roadmap", "Communicate roadmaps with now/next/later horizons", "Build product roadmap"), "The generic roadmap builder subsumes the specialised Now/Next/Later planning and communication members, which themselves target different outputs."),
    23: ("REJECT_GENERIC_SPECIALIST", ("personalized cold email sequences", "professional email templates for various business scenarios", "Writes personalized cold emails"), "The email-template member is a broad container around two cold-outreach specialists, not a balanced three-route family."),
    24: ("REJECT_TOPIC_ONLY", ("Promote existing research into a stable-status canonical article", "Investigate a topic against preserved sources and write a draft-status research article", "work in a Codebase Wiki project"), "Canonicalisation after a decision, research drafting, and codebase-wiki maintenance have different lifecycle states and outputs; a knowledge-base topic is insufficient."),
    25: ("REJECT_COMPONENT_OR_COMPOSITION", ("Protect email pipelines from injection attacks", "Maintain email conversation context across messages", "Receive, parse, and process incoming email"), "Security hardening, thread reconstruction, and inbound parsing are components of an email-processing system, not three alternative first routes."),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def line_anchor(source: str, phrase: str) -> str:
    for line_number, line in enumerate(source.splitlines(), 1):
        if phrase in line:
            return f"L{line_number}: {line.strip()}"
    raise SystemExit(f"literal evidence phrase not found: {phrase!r}")


def main() -> int:
    if PACKET.exists() or RETURN.exists() or PACKET_DIR.exists():
        raise SystemExit(f"refusing to overwrite B045 Reviewer A material: {PACKET_DIR}")
    rows = read_jsonl(INPUT)
    ledger = read_jsonl(LEDGER)
    if len(rows) != len(ledger) != 25 or set(DECISIONS) != set(range(1, 26)):
        raise SystemExit("B045 reviewer input cardinality/decision map mismatch")
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != "10825077479accfd8323e84fd1b2ab72121e078a5b668303d67e8b8420ca5d40":
        raise SystemExit("immutable B045 full-original packet hash mismatch")
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest() != "229b700717b00ec51812c8ab72932c683f4aa9a389f3b02210d876ca1a28edd8":
        raise SystemExit("immutable B045 family-ledger hash mismatch")

    packets: list[dict[str, Any]] = []
    returns: list[dict[str, Any]] = []
    for row in rows:
        rank = int(row["batch_rank"])
        if row["family_id"] != ledger[rank - 1]["family_id"]:
            raise SystemExit(f"ledger family mismatch at B045 rank {rank}")
        family_token = "F-" + str(row["family_id"]).removeprefix("SN-LEX-")
        members = []
        sources = []
        for position, member in enumerate(row["members"], 1):
            originals = member["preserved_complete_original_sources"]
            if not originals:
                raise SystemExit(f"missing complete source at B045 rank {rank}, member {position}")
            source = originals[0]["preserved_original_skill_utf8"]
            expected_hash = str(member["canonical_source_sha256"])
            if any(hashlib.sha256(item["preserved_original_skill_utf8"].encode("utf-8")).hexdigest() != expected_hash for item in originals):
                raise SystemExit(f"complete-source hash mismatch at B045 rank {rank}, member {position}")
            sources.append(source)
            members.append({
                "member_token": f"S-{position}",
                "source_byte_sha256": expected_hash,
                "complete_original_skill": source,
                "review_instruction": "Read the complete original skill. Cite literal excerpts or line locations; do not infer missing capability from topic familiarity.",
            })
        packets.append({
            "record_type": "source_native_full_source_reviewer_a_packet",
            "family_token": family_token,
            "members": members,
            "rubric": {
                "pass": "Three independent first-route skills share a bounded objective/input/output envelope, present plausible natural confusion, and have source-supported distinct roles or tools.",
                "reject_codes": ["REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION", "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE"],
                "rule": "The complete original source is authoritative. Do not use discovery rank, source path, origin, prior outcomes, or another reviewer's judgement.",
            },
        })
        decision, phrases, rationale = DECISIONS[rank]
        evidence = {f"S-{position}": [line_anchor(source, phrase)] for position, (source, phrase) in enumerate(zip(sources, phrases), 1)}
        returns.append({
            "record_type": "source_native_full_source_reviewer_a_return",
            "family_token": family_token,
            "decision": decision,
            "common_envelope_evidence": [item for values in evidence.values() for item in values],
            "member_contrast_evidence": evidence,
            "rationale": rationale,
            "review_boundary": "Reviewer A full-source family assessment only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision.",
        })
    if len({member["source_byte_sha256"] for packet in packets for member in packet["members"]}) != 75:
        raise SystemExit("B045 Reviewer A packet source cardinality mismatch")
    PACKET_DIR.mkdir(parents=True)
    write_jsonl(PACKET, packets)
    write_jsonl(RETURN, returns)
    print(json.dumps({
        "packet_sha256": hashlib.sha256(PACKET.read_bytes()).hexdigest(),
        "return_sha256": hashlib.sha256(RETURN.read_bytes()).hexdigest(),
        "families": len(returns),
        "source_hashes": 75,
        "decision_counts": {decision: sum(row["decision"] == decision for row in returns) for decision in sorted({row["decision"] for row in returns})},
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
