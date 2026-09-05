#!/usr/bin/env python3
"""Write B045's independent, full-source disagreement adjudications only."""

from __future__ import annotations

import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
PACKET_DIR = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_collaboration_project_management_meeting_notes_email_calendar_crm_customer_support_workflow_automation_b045_2026-09-04/batch_045_full_source_review_packets"
PACKET = PACKET_DIR / "reconciliation/coordinator_packet.jsonl"
RETURN = PACKET_DIR / "reconciliation/coordinator_return.jsonl"


DECISIONS = {
    "F-02f2fe2f0388ab72": ("REJECT_TOPIC_ONLY", ("Send emails through SMTP", "building Laravel emails", "Compose unsent email drafts"), "SMTP delivery, Laravel-specific mail implementation, and staging an unsent IMAP draft have different objectives, inputs, and output states. Email is a topic only, not a bounded shared first-route task."),
    "F-1786fbea80407af8": ("REJECT_NO_BOUNDED_ENVELOPE", ("adding real-time collaboration features to web applications", "building collaborative applications", "add live features to applications using pub/sub channels"), "The complete sources span a collaboration-feature SDK, CRDT document synchronisation, and general hosted pub/sub infrastructure. They do not establish one concrete, equally scoped input/output envelope beyond the broad real-time-collaboration topic."),
    "F-21faaa2747f7f650": ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Plan and prioritize product roadmaps", "Product roadmap frameworks", "Build a Now / Next / Later prioritized roadmap"), "Each original builds and prioritises a product roadmap. Framework, audience-format, and effort-estimation detail are variants within the same route, not three independent first routes."),
    "F-27305d483b26465d": ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Check a piece of writing for grammar, spelling, punctuation", "reviewing written content for grammar, spelling, punctuation", "Advisory copy-edit of prose"), "The first two provide the same proofreading surface, while the third supplies closely adjacent grammar/copy-edit feedback. The no-rewrite distinction does not establish three peer routes for a bounded request."),
    "F-35c0c3a11d9ecada": ("REJECT_GENERIC_SPECIALIST", ("Daily inbox triage", "Email triage that summarizes unread email", "Quick inbox scan"), "The Cowork and Inbox Zero sources overlap on comprehensive inbox triage; the third source is a narrow scan and explicitly defers operations to another skill. This is unbalanced generic-versus-specialist coverage, not three peers."),
    "F-3abf943b0264dcc7": ("REJECT_GENERIC_SPECIALIST", ("Turns product strategy into a themed Now/Next/Later roadmap", "Communicate roadmaps with now/next/later horizons", "Build product roadmap"), "The generic roadmap builder spans the central roadmap task, while the other originals specialise in bounded Now/Next/Later construction and communication. The set is not balanced peer alternatives."),
    "F-52a4d23f0ee5ac1f": ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Extracts decisions, action items, owners", "Analyze meeting transcripts to extract decisions, action items", "Extracts action items from meeting notes or transcripts"), "All three consume meeting notes or transcripts to extract actions, owners, deadlines, and decisions. Sentiment, follow-up, or CRM formatting are additions to the same core route rather than distinct first routes."),
    "F-9029c199faa3efbc": ("REJECT_TOPIC_ONLY", ("Promote existing research into a stable-status canonical article", "Investigate a topic against preserved sources and write a draft-status research article", "work in a Codebase Wiki project"), "Canonical promotion after a decision, provisional research, and codebase-wiki generation are different lifecycle states and artifacts. A knowledge-base label alone does not create a common bounded task."),
    "F-921c3fc2c3cdaa73": ("REJECT_GENERIC_SPECIALIST", ("fresh email composed from scratch", "Draft a professional, audience-aware email or reply", "Drafts a reply message or email from conversation context"), "The middle original is a broad professional-email container over the fresh-outbound and reply-specific routes. The members are not three equally scoped alternatives."),
    "F-98d3511e4b50b49d": ("REJECT_NO_BOUNDED_ENVELOPE", ("Create recurring focus time blocks", "Time-block planner", "Designs a daily schedule that protects deep work"), "The originals respectively mutate recurring Calendar blocks, allocate pasted calendar tasks, and design a wider behavioural routine with rituals and a scorecard. Their inputs and outputs are not one sufficiently narrow shared envelope."),
    "F-9bf3540551e9771d": ("REJECT_NEAR_DUPLICATE_OR_FORK", ("Plan a strategic roadmap across prioritization", "Facilitates strategic planning sessions", "orchestrating prioritization, epic definition, stakeholder alignment"), "The first and third originals describe the same strategic-roadmap orchestration sequence, while the facilitator adds an upstream business-planning session. This is duplicate-plus-broader coverage rather than three peer routes."),
    "F-b9bb45f9640952ee": ("REJECT_COMPONENT_OR_COMPOSITION", ("Add a list of attendees to an existing Google Calendar event", "meeting preparation with gog, including attendees", "Share Google Drive files with all attendees"), "Adding attendees, preparing the selected event, and sharing materials with those attendees are dependent operations in an event-collaboration workflow, not alternative first routes to one output."),
    "F-c4a1efbbfb8e76de": ("REJECT_TOPIC_ONLY", ("create, find, update, and delete contacts", "read and search mail, send/reply/forward", "send transactional email, manage contacts and segments"), "Google Contacts, the general Outlook suite, and Resend transactional delivery have materially different task surfaces. Contacts and email are shared topics, not a common concrete objective."),
    "F-d24bbd4710645abf": ("REJECT_TOPIC_ONLY", ("Run outbound GTM email", "Triage, reply, escalate, follow up, and close support email", "Book time, check calendar availability, and handle scheduling email"), "The shared Mermail infrastructure does not supply a shared task: the originals route outbound GTM, support resolution, and calendar scheduling to different objectives and outputs."),
    "F-eba1acaf91947fca": ("REJECT_COMPONENT_OR_COMPOSITION", ("Monitor and protect your email sender reputation", "Process email bounces and protect sender reputation", "Implement email rate limiting and volume controls"), "Reputation monitoring, bounce remediation, and rate limiting are complementary deliverability controls. The sources describe components that can compose in sender-health operations, not alternatives for the same first route."),
    "F-fa5ae1ab9425dc8b": ("REJECT_TOPIC_ONLY", ("CRM enrichment", "buyer persona", "prospect research"), "CRM record enrichment, ICP/persona development, and individual prospect research have separate inputs and deliverables; the shared GTM/CRM area is topical only."),
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
        raise SystemExit("B045 disagreement packet does not exactly match coordinator decision map")
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
