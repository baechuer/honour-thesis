#!/usr/bin/env python3
"""Persist the returned C2 Wave 002 source-informed prompt drafts locally.

The three C2 workers returned their records in their final messages rather than
writing files.  This script transcribes those source-informed drafts verbatim
into JSONL, preserving their original non-schema ``variant`` token and their
non-unique per-target packet IDs.  A separate normaliser makes the mechanical
schema-only changes needed before validation.

This creates C2 drafts only.  It does not decide cue safety, adequacy, labels,
cluster validity, retrieval inputs, model calls, metrics, or results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BASE = "RQ1B-V3-D1-C2-W5"


def pair(
    c1: str,
    source_id: str,
    direct: str,
    paraphrase: str,
    constraints: str,
) -> list[dict[str, object]]:
    """Return the literal direct/paraphrase pair supplied by a C2 worker."""
    packet_id = f"{BASE}-{c1[-3:]}-{source_id.rsplit('-', 1)[-1]}"
    common = {
        "c1_review_id": c1,
        "sealed_target_source_id": source_id,
        "c2_packet_id": packet_id,
        "c2_disposition": "C2_DRAFT_FOR_C3",
        "intended_operational_constraints": constraints,
        "construction_rationale": (
            "Source-informed C2 wording transcribed from the assigned worker "
            "return. It states operational constraints without a skill title, "
            "source identifier, or source-family cue."
        ),
        "avoided_source_cues": [
            "skill title", "source identifier", "repository or source family",
        ],
        "raw_transcription_boundary": (
            "Transcribed after the worker completed; original worker token and "
            "packet-ID shape are intentionally retained in this raw file."
        ),
    }
    return [
        {**common, "variant": "direct", "prompt_text": direct},
        {
            **common,
            "variant": "intent-preserving paraphrase",
            "prompt_text": paraphrase,
        },
    ]


DRAFTS = [
    *pair(
        "RQ1B-V3-D1-C1-W5-001", "RQ1B-V3-SRC-009012",
        "Review the images in my supplied site content for missing or unhelpful text alternatives. Return a remediation list ranked by severity, with the issue and a suggested replacement for each image.",
        "Audit the provided website images for absent or weak descriptions used by assistive technology. Prioritise the fixes from most serious to least serious, and give improved wording for every flagged image.",
        "Supplied website images; assess image text alternatives; return a severity-ranked remediation list with suggested wording.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-001", "RQ1B-V3-SRC-005779",
        "I have the hexadecimal codes for an interface's brand, status, and neutral colours. Check every planned foreground-background pairing, record whether it meets the relevant readability threshold, and return a contrast report.",
        "Using the supplied hex values for our interface palette, test all intended text-and-background combinations. For each combination, state whether it passes the appropriate legibility criterion and provide the results as a colour-pair report.",
        "Supplied hexadecimal interface colours; evaluate planned foreground-background pairs; return threshold pass/fail contrast report.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-001", "RQ1B-V3-SRC-016652",
        "From the supplied video, first establish the spoken languages and whether on-screen information or non-speech audio needs representation. Then create separate files by language or locale and purpose: translation-only subtitle text, same-language captions that include material sounds, subtitles for narrative information otherwise unavailable, a spoken-description script for visual action, and a transcript.",
        "Prepare an accessibility-ready text package for this video. Determine its languages and the important visual and audio content first, then issue distinct files for each locale and audience need: translated dialogue, captions that retain meaningful sounds, subtitle material carrying otherwise missed story information, narration for visual events, and a full transcript.",
        "Supplied video; determine languages and material visual/audio content; create separate locale- and purpose-specific accessibility text files plus transcript.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-002", "RQ1B-V3-SRC-000021",
        "Evaluate every page in an existing website for how well it supports discovery through search. Use the complete page list or the access needed to enumerate it, rate each page against the same criteria, and deliver a spreadsheet with one row per page plus a concise written summary.",
        "Review a complete website, not an individual page. Given a list of page addresses or permission to map them, assess each page for its search-discovery readiness and return a tabular page-by-page assessment together with a short overview report.",
        "Whole website and page list or enumeration access; apply one rating scheme to every page; return per-page spreadsheet and concise summary.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-002", "RQ1B-V3-SRC-002223",
        "Using the supplied website pages, documents, folders, or pasted copy, examine the organisation's writing across all relevant dimensions. Cite representative examples for each finding and produce a complete reusable style guide, noting lower confidence wherever the corpus is too small.",
        "I need a documented house style built from real material. Take the files, pages, folders, or pasted samples I provide; identify recurring choices in tone, terminology, structure, and related aspects; anchor every conclusion in examples from that corpus; then deliver a thorough guide and flag conclusions based on too little evidence.",
        "Supplied multi-document content corpus; inspect recurring writing choices; cite examples; deliver reusable style guide and flag insufficient-evidence conclusions.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-002", "RQ1B-V3-SRC-008486",
        "Review every supplied product-interface string, each with its screen location and the moment it appears. Mark each item as acceptable, needing revision, or needing replacement; do not alter legal or regulated wording, but flag it. Return a findings table with the original text, location, issue lens, decision, and suggested replacement, a location-level tally, a terminology-conflict glossary, and a concise reusable style reference.",
        "Assess the in-product messages I provide, together with their component types and user moments. Categorise each as fit to keep, needing editing, or requiring new copy. Preserve any legally controlled language exactly and list it for follow-up. Produce a row-level review of the source text, surface, criterion, outcome, and replacement; counts of issues by surface; a glossary resolving inconsistent terms; and a brief editorial reference for future interface copy.",
        "Supplied product-interface strings with screen locations and moments; preserve legal language; deliver row-level review, surface tally, terminology glossary, and short style reference.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-004", "RQ1B-V3-SRC-007645",
        "Review this expense population against the supplied expense policy. Return a concise exception workpaper that identifies policy breaches, transactions split to bypass limits, and likely duplicate claims.",
        "Using the provided spending rules, examine the submitted expense records and prepare a short exceptions report. Flag non-compliant items, claims divided to evade approval thresholds, and apparent repeat reimbursements.",
        "Supplied expense policy and expense population; find policy breaches, threshold-bypass splits, and likely duplicate claims; return exception workpaper.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-004", "RQ1B-V3-SRC-009717",
        "Match every line on this supplier invoice to the corresponding supporting records. Return a reconciliation table with the invoice number, vendor, matched details, and any unmatched or inconsistent line items.",
        "Compare the details of this vendor bill, item by item, with its supplied evidence. Produce a structured match report showing the bill reference, supplier, matching results, and discrepancies that need follow-up.",
        "Supplier invoice plus supporting records; line-item matching; return reconciliation with invoice reference, supplier, matches, and discrepancies.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-004", "RQ1B-V3-SRC-000296",
        "For the requested period, summarize the billing history into invoiced amounts, cash collected, and amounts that appear uncollectible. Report cash results rather than recurring subscription revenue.",
        "Create a time-bounded overview from these customer billing records. Show amounts billed, money actually received, and balances likely to remain unpaid; base the revenue view on collections, not subscription run-rate figures.",
        "Customer billing history and requested period; report invoiced, cash-collected, and likely uncollectible amounts; use collections rather than subscription run-rate.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-005", "RQ1B-V3-SRC-011722",
        "Review this one-way commercial confidentiality agreement clause by clause. Produce an issue log with risk analysis, preferred redlines, fallback positions, and negotiation guidance; do not treat it as a mutual agreement.",
        "Assess the provisions of this unilateral business confidentiality contract in sequence. Deliver a clause-level risks register that recommends edits, acceptable compromises, and negotiation points, while keeping mutual forms out of scope.",
        "One-way commercial confidentiality agreement; clause-level review; issue/risk log, redlines, fallback positions and negotiation guidance; exclude mutual forms.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-005", "RQ1B-V3-SRC-018791",
        "Review this credit agreement for the represented party. Return an issues table that identifies each concern, explains its effect, and recommends a change; ask which party is represented before reviewing if that has not been provided.",
        "Assess the attached lending contract from the client's position. If the client side is not stated, obtain that first; then produce a list of material issues, their implications, and proposed revisions.",
        "Credit agreement and represented party; obtain party position if absent; return material issues, implications and recommended revisions.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-005", "RQ1B-V3-SRC-013580",
        "Review this investor rights agreement for the client's actual role. Produce a term-by-term risk matrix and identify conflicts between the agreement and any related side letters, including changes needed before approval.",
        "From the client's position, evaluate this shareholders' rights instrument and its associated side letters. Provide a matrix of term-level risks, flag inconsistencies across the documents, and recommend amendments required for sign-off.",
        "Investor rights agreement, client role, and related side letters; term-level risk matrix; identify conflicts and changes required before approval.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-007", "RQ1B-V3-SRC-008722",
        "Using the supplied business and workflow requirements for a multi-user order-management application, design a normalized relational data store. Return implementation SQL covering tables, record links, indexes, integrity rules, per-user record access, and the schema changes needed to introduce it.",
        "I need to turn the attached requirements for an operational order system into a normalized transactional data design. Please provide SQL that defines its data structures and associations, protects access to individual records, adds necessary performance indexes and validation rules, and includes a rollout path for the initial schema.",
        "Multi-user order-management requirements; normalized transactional relational design; SQL for tables, links, indexes, integrity, access control and migration.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-007", "RQ1B-V3-SRC-010816",
        "Given documentation for customer purchasing, stock handling, order fulfilment, and invoicing, design a model for reporting and analysis. Deliver a cross-process reporting plan, a star-style arrangement of measure records and descriptive records, rules for retaining history when business attributes change, and database-definition statements.",
        "I need an analytics-ready design from our commercial process material covering demand, stock, fulfilment, and billing. Specify the shared reporting structure, the event-measure tables and their linked descriptive records, how changing reference information keeps its history, and the implementation DDL.",
        "Commercial process documentation covering purchasing, stock, fulfilment and invoicing; analytics model; shared reporting plan, star schema, history rules and DDL.",
    ),
    *pair(
        "RQ1B-V3-D1-C1-W5-007", "RQ1B-V3-SRC-021375",
        "From a collection of unstructured policy and procedure documents, extract the entities and their connections into a query-ready graph data set, and also provide a readable diagram of the resulting network.",
        "I will supply free-form documents. Identify the important things they mention and the relationships between them, then return both a machine-usable node-and-link representation and a visual map for inspection.",
        "Unstructured policy and procedure documents; extract entities and relationships; return query-ready node-link data and a readable network diagram.",
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n" for record in DRAFTS),
        encoding="utf-8",
    )
    print(json.dumps({"records": len(DRAFTS), "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
