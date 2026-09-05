#!/usr/bin/env python3
"""Rewrite viable batch-002 prompts and defer the platform-specific guard pair."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
AUTHORS_IN = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_002_private_2026-08-31.jsonl"
PACKETS_IN = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_target_blinded_packets_2026-08-31.jsonl"
REVIEW_IN = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_target_blinded_results_2026-08-31.jsonl"
AUTHORS_OUT = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_002_rewrite_private_2026-08-31.jsonl"
PACKETS_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_packets_2026-08-31.jsonl"
DEFERRED_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_deferred_after_blind_review_2026-08-31.jsonl"
SUMMARY_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_packet_summary_2026-08-31.json"


REWRITES = {
    "RQ2B-NC-RQ1-REAUTH-B002-021-01": "The attached transcript is the only record of yesterday's project review. Produce a durable account of what the group decided and who agreed to do what, and make uncertainty in the transcript visible rather than filling it in.",
    "RQ2B-NC-RQ1-REAUTH-B002-021-02": "My manager was away this week. Turn the attached work updates into a short account of where my projects now stand, what changed, what needs help, and what I intend to move next week.",
    "RQ2B-NC-RQ1-REAUTH-B002-023-01": "The board wants to understand why recurring revenue rose while cash collection and active accounts weakened. Use the monthly customer and billing records to reconcile the movement and show the trends that matter for the next investor update.",
    "RQ2B-NC-RQ1-REAUTH-B002-023-02": "Our subscription product handles sign-up, plan changes and failed payments inconsistently across teams. Define how each customer state should move, what event triggers an action, and who owns exceptions so the process can be implemented reliably.",
    "RQ2B-NC-RQ1-REAUTH-B002-030-01": "The attached policy exists only as a PDF, but the legal team must edit it in Word next week. Create an editable version that keeps its hierarchy and tables usable, and identify places where conversion could not preserve the original reliably.",
    "RQ2B-NC-RQ1-REAUTH-B002-030-02": "Before this report is sent outside the company, place a visible confidentiality mark across every page and add consistent company and page information in the margins while keeping the underlying PDF readable.",
    "RQ2B-NC-RQ1-REAUTH-B002-032-01": "We are the buyer under the attached supplier agreement. Before signature, tell us which provisions create the most meaningful commercial or legal exposure, why they matter in practice, and what we should seek to change.",
    "RQ2B-NC-RQ1-REAUTH-B002-032-02": "Our sales team repeatedly prepares the same service agreement with different customer and deal facts. Create a reusable machine-populated form with stable boilerplate and clearly defined variables for the changing terms.",
    "RQ2B-NC-RQ1-REAUTH-B002-033-01": "We need the substance of this slide deck in the repository so engineers can search it, review changes and link to sections. Convert its narrative and tables into a clean text-based document with a sensible heading structure.",
    "RQ2B-NC-RQ1-REAUTH-B002-033-02": "The first twelve pages of this report must become an editable Word deliverable for a client revision. Recreate the pages so their visual organization, tables and images remain usable after editing.",
    "RQ2B-NC-RQ1-REAUTH-B002-034-01": "A document-processing model needs the geometry and reading sequence of this scanned page rather than its prose alone. Identify the page regions and classify their structural roles so downstream code can reconstruct the layout.",
    "RQ2B-NC-RQ1-REAUTH-B002-034-02": "Recover the bilingual text from these scanned pages for search and translation. Keep the text in reading order and retain enough position and confidence information to send uncertain regions for manual checking.",
    "RQ2B-NC-RQ1-REAUTH-B002-035-01": "Our design library and frontend repository evolved separately. For each selected published component, identify the existing coded component that represents it and record an approved link that preserves the relevant property mapping.",
    "RQ2B-NC-RQ1-REAUTH-B002-035-02": "The selected interface is approved and now needs to work in this repository. Build it using the project's current component and token conventions, include the supplied assets, and compare the result with the design across its visible states.",
    "RQ2B-NC-RQ1-REAUTH-B002-036-01": "I am posting a written account of how our support team halved response time. Propose several genuinely different opening lines that make a professional reader want to expand the post without inventing details.",
    "RQ2B-NC-RQ1-REAUTH-B002-036-02": "The first moments of a short video must introduce how a small team halved support response time. Propose several alternative openings, pairing what the viewer hears with what appears on screen.",
    "RQ2B-NC-RQ1-REAUTH-B002-038-01": "This evaluation report says the programme reduced emergency visits, saved public money and improved health. Determine which parts of that conclusion the cited evidence actually supports, where the chain of reasoning breaks, and how confident we should be in the overall claim.",
    "RQ2B-NC-RQ1-REAUTH-B002-038-02": "A council brief says the city's first public electric-bus route opened in 2018. Check that one statement against reliable records and tell me whether it is accurate, with the qualification needed to avoid misleading readers.",
    "RQ2B-NC-RQ1-REAUTH-B002-040-01": "The books are closed and the trial balance, prior balance sheet and adjustment details are attached. Prepare the complete period-end financial statements and show that the statements reconcile with one another without inserting an unexplained balancing amount.",
    "RQ2B-NC-RQ1-REAUTH-B002-040-02": "The founders need to know when cash could fall below the operating reserve. Use receivables, expected payment dates and planned spending to project near-term weekly liquidity and the following year's monthly runway under realistic alternatives.",
}
DEFERRED_PROMPT_IDS = {
    "RQ2B-NC-RQ1-REAUTH-B002-027-01",
    "RQ2B-NC-RQ1-REAUTH-B002-027-02",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    authors = {str(row["prompt_id"]): row for row in read_jsonl(AUTHORS_IN)}
    packets = {str(row["prompt_id"]): row for row in read_jsonl(PACKETS_IN)}
    reviews = {str(row["prompt_id"]): row for row in read_jsonl(REVIEW_IN)}
    if set(authors) != set(REWRITES) | DEFERRED_PROMPT_IDS or set(packets) != set(authors) or set(reviews) != set(authors):
        raise SystemExit("Rewrite plus deferred sets must cover the complete reviewed batch")

    author_rows: list[dict[str, Any]] = []
    packet_rows: list[dict[str, Any]] = []
    for old_id, prompt in REWRITES.items():
        new_id = old_id.replace("REAUTH-B002", "REAUTH-B002-R1")
        author_rows.append({
            **authors[old_id],
            "prompt_id": new_id,
            "supersedes_prompt_id": old_id,
            "prompt": prompt,
            "initial_cue_audit": (
                "REWRITE_AFTER_SOURCE_BODY_ECHO_REVIEW: removes source-template field sequences and explicit sibling "
                "exclusions while preserving the necessary input artifact, audience, lifecycle state, or output medium."
            ),
            "status": "REWRITTEN_PRIVATE_AUTHORING_ONLY_NOT_A_GOLD_LABEL_OR_ADMITTED_RQ2_CASE",
        })
        packet_rows.append({
            **packets[old_id],
            "packet_id": f"RQ2B-NC-TARGET-BLIND-{new_id}",
            "prompt_id": new_id,
            "supersedes_prompt_id": old_id,
            "prompt": prompt,
            "status": "REWRITE_TARGET_BLINDED_REVIEW_INPUT_NOT_A_LABEL_OR_RESULT",
        })

    deferred = [{
        "review_queue_id": authors[next(iter(DEFERRED_PROMPT_IDS))]["review_queue_id"],
        "parent_rq1_cluster_id": authors[next(iter(DEFERRED_PROMPT_IDS))]["parent_rq1_cluster_id"],
        "prompt_ids": sorted(DEFERRED_PROMPT_IDS),
        "disposition": "DEFER_CLUSTER_AFTER_TARGET_BLINDED_REVIEW",
        "reason": (
            "The guardrail source is tied to one coding-assistant platform. The generic assistant prompt was only "
            "partially adequate, while adding the product name would create a provider cue rather than a semantic task distinction."
        ),
        "status": "NOT_ADMITTED_NOT_GOLD_NOT_EXPERIMENT_INPUT",
    }]
    write_jsonl(AUTHORS_OUT, author_rows)
    write_jsonl(PACKETS_OUT, packet_rows)
    write_jsonl(DEFERRED_OUT, deferred)
    summary = {
        "status": "PASS_RQ1_BATCH_002_REWRITE_AND_FAIL_CLOSED_DEFER_NOT_A_LABEL_OR_ADMISSION",
        "rewritten_prompt_count": len(author_rows),
        "target_blinded_packet_count": len(packet_rows),
        "deferred_cluster_count": 1,
        "deferred_prompt_count": len(DEFERRED_PROMPT_IDS),
        "input_sha256": {
            str(AUTHORS_IN.relative_to(ROOT)): sha256_file(AUTHORS_IN),
            str(PACKETS_IN.relative_to(ROOT)): sha256_file(PACKETS_IN),
            str(REVIEW_IN.relative_to(ROOT)): sha256_file(REVIEW_IN),
        },
        "artifacts": {
            str(AUTHORS_OUT.relative_to(ROOT)): sha256_file(AUTHORS_OUT),
            str(PACKETS_OUT.relative_to(ROOT)): sha256_file(PACKETS_OUT),
            str(DEFERRED_OUT.relative_to(ROOT)): sha256_file(DEFERRED_OUT),
        },
        "claim_boundary": [
            "Twenty prompts are naturalistic rewrites requiring fresh independent review.",
            "The platform-specific guardrail pair is deferred rather than repaired with a provider-name cue.",
            "No prompt, cluster, source, label, or result is admitted by this step."
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
