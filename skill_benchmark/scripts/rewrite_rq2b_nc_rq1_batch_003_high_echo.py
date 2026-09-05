#!/usr/bin/env python3
"""Rewrite every batch-003 prompt after strong source/body-echo review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
AUTHORS_IN = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_003_private_2026-08-31.jsonl"
PACKETS_IN = BASE / "review/rq1_frozen_cluster_reauthored_batch_003_target_blinded_packets_2026-08-31.jsonl"
REVIEW_IN = BASE / "review/rq1_frozen_cluster_reauthored_batch_003_target_blinded_results_2026-08-31.jsonl"
AUTHORS_OUT = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_003_rewrite_private_2026-08-31.jsonl"
PACKETS_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_003_rewrite_target_blinded_packets_2026-08-31.jsonl"
SUMMARY_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_003_rewrite_packet_summary_2026-08-31.json"


REWRITES = {
    "RQ2B-NC-RQ1-REAUTH-B003-041-01": "I am the recipient under the attached confidentiality agreement and need to decide what to negotiate before signing. Identify the provisions that materially expose us, explain the practical consequence, cite the wording, and suggest a workable change.",
    "RQ2B-NC-RQ1-REAUTH-B003-041-02": "Our portfolio team has sixty confidentiality agreements and an existing workbook with the facts it tracks for every deal. Populate one row per document from the agreement itself and preserve a link back to where each recorded value came from.",
    "RQ2B-NC-RQ1-REAUTH-B003-042-01": "I am the employee named in this offer and employment contract. Before I sign, explain which terms deserve attention, what they could mean for me in practice, and which changes I should ask the employer to consider, with references to the supplied text.",
    "RQ2B-NC-RQ1-REAUTH-B003-042-02": "HR has a fixed workbook used to compare employment contracts across the group. Fill its existing columns for each supplied contract using the document text and make every populated value traceable to its source passage.",
    "RQ2B-NC-RQ1-REAUTH-B003-043-01": "Our company would occupy the premises under this lease. Tell us which terms could create the largest cost or operational surprise, show where they appear, and propose the points we should negotiate before committing.",
    "RQ2B-NC-RQ1-REAUTH-B003-043-02": "The property team maintains a standard workbook for its lease portfolio. For each uploaded lease, complete the existing fields from the agreement and attach enough location evidence for another analyst to verify every entry.",
    "RQ2B-NC-RQ1-REAUTH-B003-044-01": "We would be the borrower under this facility. Explain the terms most likely to restrict the business or cause an unexpected default or cost, cite the relevant wording, and propose a realistic negotiation position before signing.",
    "RQ2B-NC-RQ1-REAUTH-B003-044-02": "Treasury has an established workbook for comparing lending facilities. Populate its defined fields for each uploaded agreement from the documents themselves and keep each value tied to the supporting passage.",
    "RQ2B-NC-RQ1-REAUTH-B003-045-01": "I would hold a small minority stake under this shareholders' agreement. Assess where my influence, economics or exit could be weakened, point to the operative language, and suggest the protections worth negotiating.",
    "RQ2B-NC-RQ1-REAUTH-B003-045-02": "The investment team uses one fixed workbook to compare shareholders' agreements. Complete its existing columns for each document using only supported values, and retain the location needed to check each entry later.",
    "RQ2B-NC-RQ1-REAUTH-B003-046-01": "A pilot repeatedly found that patients with the exposure had fewer readmissions, but selection and adherence could explain the pattern. Turn this observation into a small next study whose predictions would distinguish the leading explanations and state the decisions that must be fixed before new outcomes are seen.",
    "RQ2B-NC-RQ1-REAUTH-B003-046-02": "Our respiratory-research group has no agreed project for next winter. Design a 90-minute session that gets quieter and senior members contributing independently, develops several distinct directions, and ends with a recorded shortlist the team can investigate.",
    "RQ2B-NC-RQ1-REAUTH-B003-047-01": "Build a verified reading list of recent primary studies on the topic. For each paper, give the stable identifier, citation and a lawful route to the full text where one exists, and leave enough search detail for another researcher to update the list later.",
    "RQ2B-NC-RQ1-REAUTH-B003-047-02": "I have supplied the full texts selected for a scoping review. Build an evidence matrix that lets us compare what each study did and found, with every entry grounded in the paper and unsupported fields visibly unresolved.",
    "RQ2B-NC-RQ1-REAUTH-B003-048-01": "Here are thirty days of spend, qualified leads and revenue by campaign and audience. Decide how next month's paid budget should move, including what to stop, protect or test, and tie each recommendation to the observed evidence.",
    "RQ2B-NC-RQ1-REAUTH-B003-048-02": "Here are our strongest customer comments, approved brand assets and examples of ads that have worked. Develop a set of new static-ad directions for the next campaign, showing the proposed message and visual idea and which supplied evidence inspired it.",
    "RQ2B-NC-RQ1-REAUTH-B003-050-01": "Four teachers will mark the same Year 9 persuasive speeches and currently disagree about quality. Create a shared marking guide that distinguishes performance across the important dimensions clearly enough for moderation and for students to understand expectations.",
    "RQ2B-NC-RQ1-REAUTH-B003-050-02": "Year 9 students are revising one aspect of a persuasive speech. Create a simple feedback sheet that states the success criterion once and leaves open space to record evidence of what works and what should change, without turning the activity into a score.",
    "RQ2B-NC-RQ1-REAUTH-B003-056-01": "The attached fantasy scene is complete but reads slowly and repeats itself. Give it a clean second-draft edit while keeping the narrator's voice, viewpoint and events intact, and flag any continuity question that cannot be solved from the page.",
    "RQ2B-NC-RQ1-REAUTH-B003-056-02": "My mystery has a premise, protagonist and ending, but the middle loses momentum. Rebuild the story's major turns and causal sequence across the novel so I can see what each section must accomplish and where setups need later payoffs.",
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
    if set(REWRITES) != set(authors) or set(REWRITES) != set(packets) or set(REWRITES) != set(reviews):
        raise SystemExit("The rewrite must cover the complete reviewed batch-003 prompt set")

    author_rows: list[dict[str, Any]] = []
    packet_rows: list[dict[str, Any]] = []
    for old_id, prompt in REWRITES.items():
        new_id = old_id.replace("REAUTH-B003", "REAUTH-B003-R1")
        author_rows.append({
            **authors[old_id],
            "prompt_id": new_id,
            "supersedes_prompt_id": old_id,
            "prompt": prompt,
            "initial_cue_audit": (
                "REWRITE_AFTER_STRONG_SOURCE_BODY_ECHO_REVIEW: removes copied output schemas, exhaustive source checklists, "
                "and explicit sibling exclusions while preserving the necessary document state, audience, evidence object, "
                "or lifecycle boundary."
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

    write_jsonl(AUTHORS_OUT, author_rows)
    write_jsonl(PACKETS_OUT, packet_rows)
    summary = {
        "status": "PASS_RQ1_BATCH_003_FULL_HIGH_ECHO_REWRITE_PACKETISATION_NOT_A_LABEL_OR_ADMISSION",
        "rewritten_prompt_count": len(author_rows),
        "target_blinded_packet_count": len(packet_rows),
        "candidate_judgment_slot_count": sum(len(row["candidates"]) for row in packet_rows),
        "input_sha256": {
            str(AUTHORS_IN.relative_to(ROOT)): sha256_file(AUTHORS_IN),
            str(PACKETS_IN.relative_to(ROOT)): sha256_file(PACKETS_IN),
            str(REVIEW_IN.relative_to(ROOT)): sha256_file(REVIEW_IN),
        },
        "artifacts": {
            str(AUTHORS_OUT.relative_to(ROOT)): sha256_file(AUTHORS_OUT),
            str(PACKETS_OUT.relative_to(ROOT)): sha256_file(PACKETS_OUT),
        },
        "claim_boundary": [
            "All twenty original prompts were discriminable but rejected for strong source/body echo.",
            "These complete-batch rewrites are new review inputs, not labels or admissions.",
            "Every rewrite requires a fresh independent full-source adequacy and cue review."
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
