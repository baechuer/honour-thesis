#!/usr/bin/env python3
"""Author and packetise RQ2-native business Wave 001 prompts.

The private authoring file retains the intended source hash so that a later
controller can reconcile target-blinded adequacy judgments.  The review packet
withholds that target and deterministically rotates candidate aliases.  This
script creates curation inputs only; it does not admit a cluster, freeze a gold
label, or run a selector.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
LEADS = ROOT / "rq2b_naturalistic_confusability/candidates/rq2_native_discovery_wave_001_business_2026-08-31.jsonl"
PROMPT_OUT = ROOT / "rq2b_naturalistic_confusability/prompts/rq2_native_business_wave_001_authoring_private_2026-08-31.jsonl"
PACKET_OUT = ROOT / "rq2b_naturalistic_confusability/review/rq2_native_business_wave_001_target_blinded_packets_2026-08-31.jsonl"
SUMMARY_OUT = ROOT / "rq2b_naturalistic_confusability/review/rq2_native_business_wave_001_authoring_summary_2026-08-31.json"


PROMPTS: dict[str, str] = {
    "public-skillme-ab-test-analyzer": (
        "A signup change was randomly assigned between a control and a variant for two weeks. "
        "Using the per-arm visitor and completion counts, estimate the lift and uncertainty, check "
        "whether the experiment was adequately powered, and recommend ship, iterate, or stop."
    ),
    "public-skillme-funnel-analysis": (
        "A product team has weekly counts for landing, account creation, verification, first project, "
        "and first successful export. Identify where the largest losses occur, segment the weak steps, "
        "and recommend the next diagnostic or product change."
    ),
    "public-skillme-growth-accounting": (
        "For each of the last twelve months, a SaaS team has beginning and ending active accounts plus "
        "accounts that were new, retained, returned after inactivity, or lost. Reconcile the movements "
        "and explain which component is driving net growth."
    ),
    "public-skillme-research-synthesis": (
        "A product decision is supported by industry reports, published studies, support analyses, and "
        "prior internal research. Combine the evidence into defensible themes, record contradictions and "
        "evidence strength, and state what remains uncertain."
    ),
    "public-skillme-interview-synthesis": (
        "The team has transcripts from eighteen participant interviews with speaker attribution. Derive "
        "cross-participant themes, show how widely each theme appeared, preserve representative quotations, "
        "and flag whether new interviews were still adding themes."
    ),
    "public-skillme-market-sizing": (
        "Estimate the opportunity for a new compliance service from the number of eligible organisations, "
        "the geographies and segments the team can actually serve, expected annual price, and a defensible "
        "share it could reach. Show assumptions and sensitivity ranges."
    ),
    "public-skillme-revenue-modeling": (
        "Build a twelve-month recurring-revenue forecast from the current book of business and historical "
        "new sales, upgrades, downgrades, renewals, and losses. Provide base, upside, and downside cases and "
        "make every assumption auditable."
    ),
    "public-skillme-unit-economics": (
        "Using acquisition spend, new customers, revenue per account, gross margin, service cost, and loss "
        "rate, determine whether acquiring one more customer creates value. Report contribution, payback "
        "period, and the assumptions most likely to reverse the conclusion."
    ),
    "public-skillme-survey-designer": (
        "Before a roadmap decision, collect comparable estimates of feature-use frequency and satisfaction "
        "from roughly 500 customers. Design the questions, response scales, sampling and analysis plan so "
        "the results can be compared across customer segments."
    ),
    "public-skillme-expert-interview": (
        "The team needs to understand why a specialised procurement process stalls. Plan conversations with "
        "people who recently owned that process, using probes that reveal mechanisms, decision criteria, and "
        "exceptions rather than population-level frequencies."
    ),
    "public-skillme-usability-test-plan": (
        "A clickable prototype now supports three critical account-recovery tasks. Plan sessions in which "
        "representative users attempt those tasks, defining scenarios, observations, success measures, and "
        "a consistent way to record breakdowns."
    ),
    "public-skillme-competitive-intelligence": (
        "Sales teams keep losing a current deal to two named rivals. Verify those rivals' present features, "
        "prices, positioning, and sales claims from traceable evidence, then turn the findings into a near-term "
        "response for this sales cycle."
    ),
    "public-skillme-competitive-moat": (
        "Investors ask what remains defensible if a well-funded rival copies the product's visible features "
        "within a year. Test each claimed advantage against imitation, incumbent response, and durability, "
        "then identify which protections are real and which are temporary."
    ),
    "public-skillme-help-documentation": (
        "Customers repeatedly ask how to recover a locked account in the current interface. Produce a concise "
        "self-service article using the exact visible labels, ordered actions, prerequisites, and an observable "
        "confirmation that recovery succeeded."
    ),
    "public-skillme-process-doc": (
        "New operations staff must execute the normal monthly supplier-onboarding workflow without asking its "
        "author. Document owners, inputs, ordered actions, decision branches, handoffs, exceptions, and the "
        "record that proves completion."
    ),
    "public-skillme-runbook-writer": (
        "During a live service incident, the on-call engineer needs a short operational guide for this alert. "
        "Organise symptoms, immediate safety checks, diagnostics, reversible mitigations, escalation conditions, "
        "and post-recovery verification."
    ),
    "public-skillme-churn-reduction": (
        "Several currently paying accounts have opened cancellation flows or shown an abrupt fall in use. "
        "Diagnose the immediate loss reasons, prioritise the at-risk accounts, and design interventions that can "
        "be tested before those subscriptions end."
    ),
    "public-skillme-win-back-campaign": (
        "A cohort of former customers has been inactive for six months after cancelling. Segment them by prior "
        "value and departure reason, then design a bounded reactivation sequence with an offer, timing, holdout, "
        "and success measure."
    ),
    "public-skillme-expansion-revenue": (
        "Healthy accounts with strong adoption are approaching seat limits, and several have a second team that "
        "could use the product. Identify qualified expansion signals and create an account-level plan for adding "
        "seats or use cases without treating the accounts as retention risks."
    ),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_recorded_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return WORKSPACE / path


def main() -> int:
    leads = [
        row
        for row in read_jsonl(LEADS)
        if row["screen_disposition"] == "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW"
    ]
    if len(leads) != 7:
        raise SystemExit(f"Expected seven promoted business leads, found {len(leads)}")

    all_skill_ids = {candidate["skill_id"] for lead in leads for candidate in lead["candidates"]}
    if all_skill_ids != set(PROMPTS):
        raise SystemExit(
            f"Prompt/lead mismatch: missing={sorted(all_skill_ids - set(PROMPTS))}, "
            f"extra={sorted(set(PROMPTS) - all_skill_ids)}"
        )

    author_rows: list[dict[str, Any]] = []
    packet_rows: list[dict[str, Any]] = []
    prompt_number = 1
    for lead_number, lead in enumerate(leads, start=1):
        candidates = list(lead["candidates"])
        for candidate in candidates:
            source_path = resolve_recorded_path(candidate["source_path"])
            if not source_path.is_file():
                raise SystemExit(f"Missing source: {source_path}")
            if sha256_file(source_path) != candidate["source_sha256"]:
                raise SystemExit(f"Source hash mismatch: {source_path}")

        for within_cluster_index, intended in enumerate(candidates):
            prompt_id = f"NC-NATIVE-BIZ-W001-{prompt_number:03d}"
            prompt = PROMPTS[intended["skill_id"]]
            author_rows.append(
                {
                    "prompt_id": prompt_id,
                    "cluster_lead_id": lead["cluster_lead_id"],
                    "author_intended_candidate_source_sha256": intended["source_sha256"],
                    "prompt": prompt,
                    "authoring_basis": "NATURAL_TASK_WITH_NECESSARY_PRECONDITION_NOT_SKILL_TITLE",
                    "initial_cue_audit": (
                        "No candidate title, repository, provider, package, or source path is named. "
                        "The discriminating facts are necessary input, operating-state, audience, or "
                        "decision-horizon conditions and still require independent cue review."
                    ),
                    "status": "AUTHORING_DRAFT_NOT_A_GOLD_LABEL_OR_ADMITTED_RQ2_CASE",
                }
            )

            rotation = (lead_number + within_cluster_index) % len(candidates)
            rotated = candidates[rotation:] + candidates[:rotation]
            packet_candidates = [
                {
                    "alias": chr(ord("A") + index),
                    "source_sha256": item["source_sha256"],
                    "source_path": item["source_path"],
                }
                for index, item in enumerate(rotated)
            ]
            packet_rows.append(
                {
                    "packet_id": f"NC-TARGET-BLIND-{prompt_id}",
                    "prompt_id": prompt_id,
                    "cluster_lead_id": lead["cluster_lead_id"],
                    "prompt": prompt,
                    "candidates": packet_candidates,
                    "reviewer_instruction": (
                        "Read each preserved source independently. The author target is withheld. Classify "
                        "every candidate as fully_adequate, partially_adequate, inadequate, or unclear; "
                        "identify source overlap, necessary-versus-gratuitous cueing, composition risk, and "
                        "multi-acceptable risk. Do not infer or request the intended target. This is "
                        "target-blinded, not candidate-identity-blinded, review."
                    ),
                    "status": "TARGET_BLINDED_REVIEW_INPUT_NOT_A_LABEL_OR_RESULT",
                }
            )
            prompt_number += 1

    if len(author_rows) != 19 or len(packet_rows) != 19:
        raise SystemExit(f"Expected 19 prompts/packets, found {len(author_rows)}/{len(packet_rows)}")
    write_jsonl(PROMPT_OUT, author_rows)
    write_jsonl(PACKET_OUT, packet_rows)

    summary = {
        "status": "PASS_NATIVE_BUSINESS_WAVE_001_AUTHORING_NOT_A_GOLD_FREEZE",
        "promoted_lead_count": len(leads),
        "authoring_prompt_count": len(author_rows),
        "target_blinded_packet_count": len(packet_rows),
        "unique_candidate_source_count": len({
            candidate["source_sha256"] for lead in leads for candidate in lead["candidates"]
        }),
        "input_sha256": {str(LEADS.relative_to(ROOT)): sha256_file(LEADS)},
        "artifacts": {
            str(PROMPT_OUT.relative_to(ROOT)): sha256_file(PROMPT_OUT),
            str(PACKET_OUT.relative_to(ROOT)): sha256_file(PACKET_OUT),
        },
        "claim_boundary": [
            "Prompts were authored after source-grounded lead screening and do not reuse RQ1 prompts or labels.",
            "The review packet withholds the author-intended target but exposes candidate sources; it is target-blinded, not candidate-identity-blinded.",
            "No prompt or source mapping is admitted until independent candidate-by-candidate adequacy and cue review passes.",
            "No selector, retrieval, embedding, reranking, metric, or thesis result is produced.",
        ],
    }
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
