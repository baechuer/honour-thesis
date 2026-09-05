#!/usr/bin/env python3
"""Materialise the source-only RQ1 re-review ledger for queue orders 61--79.

This intentionally produces only a review ledger and private authoring drafts.
It neither reads nor emits historic prompts, gold/acceptable labels, selector
outputs, experiment results, target-blinded packets, admissions, or metrics.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "rq1_frozen_cluster_re_review_queue_2026-08-31/"
    "rq1_frozen_cluster_source_only_re_review_queue.jsonl"
)
REVIEW = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "rq1_frozen_cluster_re_review_batch_004_2026-08-31.jsonl"
)
PROMPTS = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/prompts/"
    "rq1_frozen_cluster_reauthored_batch_004_private_2026-08-31.jsonl"
)
SUMMARY = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "rq1_frozen_cluster_re_review_batch_004_2026-08-31_summary.json"
)


P = "PROMOTE_TO_RQ2_PROMPT_AUTHORING"
R = "REJECT"
D = "DEFER"

# Each boundary reference is deliberately rooted in the preserved source text.
# The review rationale is a semantic source-only judgement, not a transferred RQ1 label.
DECISIONS = {
    61: {
        "d": R,
        "e": "Search-strategy guidance for an information need.",
        "b": [
            "Academic literature, methodology and literature-review support; the source also says it cannot execute database searches.",
            "General web query formulation, source evaluation and information synthesis across source types.",
        ],
        "lines": [["L53-L71", "L75-L99"], ["L52-L70", "L74-L98"]],
        "risk": "HIERARCHY_HIGH: academic literature search is a field-specialised subset of general web search; their query, source-evaluation and synthesis operations overlap.",
        "why": "Reject: no natural singleton survives once academic source-type terms are not treated as a target cue; the academic candidate is a specialised route within the broader web-search workflow.",
    },
    62: {
        "d": P,
        "e": "Improve the operational reliability of a software service using evidence already available or still to be designed.",
        "b": [
            "No adequate telemetry/alert plan exists: define health signals, alert ownership and the smallest visibility slice.",
            "A trace, benchmark, query plan or profiler artefact already exists: isolate one performance bottleneck, make one or two bounded changes, and compare before/after.",
        ],
        "lines": [["L26-L53", "L122-L150"], ["L27-L51", "L111-L164"]],
        "risk": "LOW_SUBSUMPTION: monitoring explicitly routes bottleneck tuning out, and performance explicitly routes telemetry rollout out; existing-measurement state is a natural necessary condition.",
        "why": "Promote: instrumentation/ownership versus evidence-led bottleneck tuning is a non-substitutable boundary that can be expressed without titles or providers.",
    },
    63: {
        "d": P,
        "e": "Improve how a delivery team coordinates and learns from work.",
        "b": [
            "A sprint, release or milestone is complete: review prior actions and delivery evidence, identify themes, and agree a few owned process changes.",
            "Work is in progress: choose a daily or lighter coordination cadence to surface current blockers and handoffs.",
        ],
        "lines": [["L24-L44", "L102-L145"], ["L30-L61", "L120-L145"]],
        "risk": "WORKFLOW_PHASE_RISK_CONTROLLED: both are delivery rituals, but completed-work reflection and in-progress blocker coordination have incompatible evidence and outputs.",
        "why": "Promote: the time-state of the work is necessary and naturally observable; neither candidate is a parent of the other.",
    },
    64: {
        "d": P,
        "e": "Decide how software changes should be validated with credible evidence.",
        "b": [
            "A concrete backend behaviour is known: choose unit/integration/contract/smoke coverage, fixtures and dependency realism for that change.",
            "The team is shaping merge, release or scheduled confidence policy across changes: decide gate truth, layer policy, exceptions and flake handling.",
        ],
        "lines": [["L21-L49", "L52-L62"], ["L25-L58", "L83-L151"]],
        "risk": "ABSTRACTION_RISK_CONTROLLED: implementation planning and organisation-level gate policy are adjacent, but the sources explicitly route each to the other.",
        "why": "Promote: the concrete changed behaviour versus policy/gate decision is a necessary, cue-safe boundary.",
    },
    65: {
        "d": P,
        "e": "Improve the quality and consistency of a web product interface.",
        "b": [
            "Multiple pages/products need shared tokens, visual-language rules, primitive naming and governance before screen work.",
            "A specific existing page or flow needs a broad usability/visual audit, prioritised by user friction and launch risk.",
        ],
        "lines": [["L26-L56", "L90-L115"], ["L28-L53", "L55-L64"]],
        "risk": "SCOPE_RISK_CONTROLLED: system-governance source explicitly routes broad page/flow critique out; audit source routes token governance out.",
        "why": "Promote: cross-surface shared-rule creation versus review of a concrete surface is a natural, non-provider distinction.",
    },
    66: {
        "d": R,
        "e": "Make a production software release safer.",
        "b": [
            "Automate build, test and deployment pipelines, including deployment strategies and rollback workflow mechanics.",
            "Prepare a production launch checklist, staged rollout, monitoring and rollback strategy.",
        ],
        "lines": [["L2-L16", "L193-L269"], ["L2-L18", "L20-L75", "L110-L160"]],
        "risk": "SUBSUMPTION_HIGH: the pipeline source explicitly contains deployment, staged rollout and rollback material; the launch source is a broad release checklist over the same process.",
        "why": "Reject: release-safety prompts would leave both candidates substantially adequate; an artificial pipeline-versus-launch wording split is not enough.",
    },
    67: {
        "d": P,
        "e": "Plan or create email communications for an organisation.",
        "b": [
            "A single message has a specified recipient relationship, situation, purpose and tone; draft that message.",
            "A subscriber programme requires sequence design, segmentation, timing, experimentation or deliverability analysis across multiple sends.",
        ],
        "lines": [["L49-L74", "L76-L105", "L205-L241"], ["L46-L58", "L61-L108", "L278-L374"]],
        "risk": "CONTAINMENT_RISK_LOW: campaign work may draft copy, but the multi-send lifecycle/segmentation evidence is necessary for the second candidate and absent from a single correspondence task.",
        "why": "Promote: single recipient-specific correspondence versus campaign system design is a stable, natural boundary.",
    },
    68: {
        "d": D,
        "e": "Use organisational data to support a business decision.",
        "b": [
            "Curated BigQuery data must become a trustworthy stakeholder reporting/dashboard delivery artefact.",
            "The immediate task is first-pass detection of repeated patterns or suspicious metric anomalies, before explanation or reporting.",
        ],
        "lines": [["L1-L19", "L24-L67"], ["L1-L18", "L21-L44", "L68-L105"]],
        "risk": "COMMON_ENVELOPE_WEAK: dashboard delivery and anomaly detection can co-occur, but natural mixed business prompts would commonly need both or route one out; a strict singleton is not yet demonstrated.",
        "why": "Defer: both sources are semantically coherent individually, but this pair needs a stronger shared natural-artifact setting before authoring.",
    },
    69: {
        "d": P,
        "e": "Make a web or API product safe for real user access.",
        "b": [
            "Choose or migrate the product identity lane, login/session model, provider/app ownership, organisation model or enterprise SSO boundary.",
            "An application already exists and needs a focused hardening layer such as browser policy, CSRF/session protection, abuse control, validation or secrets verification.",
        ],
        "lines": [["L26-L59", "L84-L150"], ["L27-L59", "L63-L108"]],
        "risk": "ADJACENCY_CONTROLLED: both sources explicitly distinguish auth-stack choice from general hardening; user state (identity architecture undecided vs a missing security control) separates them.",
        "why": "Promote: the ownership/architecture decision and the existing-control hardening decision are non-substitutable in natural product work.",
    },
    70: {
        "d": P,
        "e": "Make software delivery repeatable and safe.",
        "b": [
            "The system already builds; decide release promotion, rollout, verification, stop conditions or rollback across environments.",
            "The repository needs a recurring local command surface, hooks, local-CI parity or maintenance automation.",
        ],
        "lines": [["L24-L55", "L79-L130"], ["L24-L60", "L89-L117"]],
        "risk": "BOUNDARY_EXPLICIT: release source routes CI workflow authoring to workflow automation; workflow source routes deployment architecture and rollout out.",
        "why": "Promote: release-state versus repo-command-surface is a necessary, cue-safe distinction.",
    },
    71: {
        "d": R,
        "e": "Give an AI assistant the project context it needs across tasks or sessions.",
        "b": [
            "Curate rules, focused source files, specifications and conversation context for an agent task.",
            "Preserve, search and hand off active project memory through compact packets, manifests and stable links.",
        ],
        "lines": [["L6-L18", "L20-L35", "L121-L178"], ["L25-L57", "L61-L103"]],
        "risk": "HIERARCHY_AND_DUPLICATE_HIGH: generic context curation encompasses the same load/search/handoff activities; OpenContext is a tool-specific operationalisation rather than a peer semantic alternative.",
        "why": "Reject: a singleton would depend on tool/product naming or an artificial artifact cue, not a durable user-task distinction.",
    },
    72: {
        "d": P,
        "e": "Add an AI capability to a product.",
        "b": [
            "Directly integrate a simple user-facing text/chat/multimodal/streaming capability in the client app, with app-side controls.",
            "Own a reusable server-side flow with contracts, tools, retrieval, prompt assets, evaluation, observability or multi-client reuse.",
        ],
        "lines": [["L20-L43", "L60-L88", "L123-L131"], ["L28-L52", "L96-L109", "L132-L159"]],
        "risk": "LAYER_BOUNDARY_EXPLICIT: client integration source routes server-owned orchestration out; server-flow source routes direct client SDK work out.",
        "why": "Promote: client feature ownership versus reusable backend workflow ownership is necessary and naturally observable without naming a provider.",
    },
    73: {
        "d": P,
        "e": "Run a controlled autonomous improvement loop with keep/revert discipline.",
        "b": [
            "Improve train.py in a real ML training repository under the fixed prepare.py/runtime/validation-bits-per-byte experiment contract.",
            "Improve a repo-local skill, SOP, prompt or workflow artifact using representative scenarios and a frozen local benchmark.",
        ],
        "lines": [["L26-L63", "L114-L126", "L160-L181"], ["L24-L53", "L60-L82"]],
        "risk": "SURFACE_AND_EVALUATOR_BOUNDARY_STRONG: the candidates share keep/revert structure but have different mutable artifacts, fixed evaluators and execution substrates.",
        "why": "Promote: real training artefact versus reusable instruction/workflow artefact is a necessary non-substitutable boundary.",
    },
    74: {
        "d": P,
        "e": "Protect email sending reputation and inbox placement.",
        "b": [
            "Send cold outbound to new prospects using separate sending domains, mailbox pools, warm-up and per-mailbox capacity controls.",
            "Audit permissioned marketing/lifecycle sending using authenticated brand identity, list hygiene, complaint thresholds and engagement suppression.",
        ],
        "lines": [["L43-L73", "L75-L93", "L198-L211"], ["L1-L8", "L14-L55", "L99-L117"]],
        "risk": "AUDIENCE_AND_IDENTITY_BOUNDARY_STRONG: the permissioned-send source explicitly routes cold outbound away; different acquisition legitimacy and sender-identity policies are necessary facts.",
        "why": "Promote: cold prospecting versus opted-in lifecycle mail is a natural strict boundary, not a title cue.",
    },
    75: {
        "d": P,
        "e": "Create a sustainable content publishing calendar.",
        "b": [
            "A solo creator needs one primary channel, a worst-week sustainable cadence, pillar rotation, idea bank and personal audit loop.",
            "A brand or social team needs a dated multi-platform grid with per-channel cadence, campaign dates, assets and reactive capacity.",
        ],
        "lines": [["L1-L8", "L14-L46", "L76-L97"], ["L1-L17", "L19-L34"]],
        "risk": "ACTOR_AND_DELIVERY_SHAPE_BOUNDARY_STRONG: creator source explicitly routes brand/team multi-platform grids away; the second source excludes solo single-channel planning.",
        "why": "Promote: creator operating constraint versus team campaign/grid work is a necessary natural distinction.",
    },
    76: {
        "d": P,
        "e": "Increase a local service business's visibility in map-based and local organic search.",
        "b": [
            "Repair and maintain the owned business listing: category, service area, duplicate listing, NAP, services, photos, Q&A and posts.",
            "Create a broader 90-day local ranking plan across website service/city pages, citations, review velocity, links and remeasurement.",
        ],
        "lines": [["L1-L17", "L24-L57", "L146-L180"], ["L1-L16", "L18-L49", "L148-L184"]],
        "risk": "DEPENDENCY_RISK_CONTROLLED: broader local plan requires listing foundation but explicitly routes hands-on listing settings out; the scopes have different deliverables and time horizons.",
        "why": "Promote: owned listing remediation versus wider site/citation strategy is a natural non-substitutable boundary.",
    },
    77: {
        "d": R,
        "e": "Select visual assets for a public or commercial communication.",
        "b": [
            "Find candidate stock images: select a library and search queries from a visual brief.",
            "Clear a specific candidate image for a stated use: inspect its licence, attribution, releases, scale and restrictions.",
        ],
        "lines": [["L1-L18", "L24-L37", "L89-L113"], ["L1-L10", "L16-L64", "L87-L109"]],
        "risk": "COMPOSITION_HIGH: discovery source explicitly requires rights review before commercial shipping; rights review requires a specific candidate and is a necessary next-stage gate.",
        "why": "Reject: the candidates form a sequential workflow rather than competing fully adequate solutions to the same prompt.",
    },
    78: {
        "d": P,
        "e": "Improve the quality, transparency and evidence discipline of a scientific manuscript.",
        "b": [
            "An author team is drafting, revising or preparing its own manuscript, declarations, evidence records and submission materials.",
            "An authorised reviewer is assessing a confidential external manuscript/protocol/preprint and must provide a bounded constructive review without editorial decision-making.",
        ],
        "lines": [["L1-L15", "L213-L276", "L278-L315"], ["L11-L52", "L77-L104", "L209-L263"]],
        "risk": "ROLE_AND_CONFIDENTIALITY_BOUNDARY_STRONG: author-side writing/revision and reviewer-side authorised confidential assessment have incompatible accountability, handling and output constraints.",
        "why": "Promote: author versus authorised reviewer role is a necessary real-world condition, not a provider or title cue.",
    },
    79: {
        "d": P,
        "e": "Improve how a website is found and understood in search-mediated discovery.",
        "b": [
            "Diagnose conventional organic search health: crawlability, indexation, technical foundations, on-page content and ranking changes.",
            "Improve visibility/citation in generative answers and automated-agent discovery through extractability, citable authority, third-party presence and AI-search monitoring.",
        ],
        "lines": [["L1-L10", "L38-L58", "L62-L150", "L423-L458"], ["L1-L12", "L204-L278", "L392-L424", "L428-L461"]],
        "risk": "FOUNDATION_DEPENDENCY_CONTROLLED: AI-search work relies partly on conventional search hygiene, but the sources define distinct evidence surfaces and outcomes; prompts can specify the observed discovery failure.",
        "why": "Promote: conventional crawl/index/on-page diagnosis versus answer-citation/agent-readability visibility can be separated by a natural evidence condition.",
    },
}

PROMPT_TEXT = {
    62: [
        "A newly launched checkout API has no agreed alerts or owner, and users are often the first to report problems. Define the smallest monitoring plan that should notice customer-impacting failures and tell a person what to do.",
        "We have a staging trace showing checkout p95 rose from 180 ms to 850 ms after a filter change. Identify the most likely bottleneck, propose no more than two changes, and state how to verify the result fairly.",
    ],
    63: [
        "Our two-week sprint has ended with late QA handoffs and several unfinished actions from the previous cycle. Facilitate a short review that turns the evidence into a few owned process improvements.",
        "A distributed product team spends 40 minutes every morning reading status updates, yet blockers still surface late. Decide the lightest recurring coordination cadence and show how blockers should be escalated.",
    ],
    64: [
        "A new webhook writes to the database and calls an external billing service. Design the smallest credible test plan, including what should be mocked, what needs realistic data, and how state should be reset.",
        "After an authentication change and database migration, the team disagrees about what must block merge, what belongs before release, and what can run overnight. Produce a risk-based validation policy.",
    ],
    65: [
        "Our marketing site and logged-in dashboard use inconsistent spacing, colours, and button naming. Define shared visual foundations, primitive governance, and the handoff boundaries for implementation work.",
        "Review our completed signup flow for hierarchy, clarity, CTA emphasis, error-state quality, and task friction; prioritise the changes that most affect a first-time user.",
    ],
    67: [
        "Draft a concise, professional email to a prospective partner after yesterday’s meeting, asking them to confirm whether they can review the proposal by Friday.",
        "Plan a two-week welcome programme for new subscribers, including segmentation, timing, subject-line experiment ideas, and the success metrics to watch.",
    ],
    69: [
        "We are building a B2B SaaS product that needs email login, social sign-in, workspace membership, and later customer SSO. Recommend an authentication architecture and clarify what the app versus provider should own.",
        "Our web app already uses cookie sessions, but a launch review found missing CSRF protection, weak rate limits, and unclear secret handling. Prioritise the first security hardening layer and verification steps.",
    ],
    70: [
        "Staging deploys automatically, but production promotion is an undocumented manual ritual. Create a release packet with promotion gates, verification, stop conditions, and a rollback path.",
        "This repository has commands scattered across the README, package scripts, and shell files. Design one repeatable developer command surface for setup, verification, and routine maintenance.",
    ],
    72: [
        "Our existing mobile app needs streaming AI summaries inside its client interface. Keep the capability in the app layer, describe the UX lifecycle, and include the platform-specific production controls it needs.",
        "Our web app and internal support console both need a document-grounded assistant that can retrieve approved material and call one ticket action. Define the smallest reusable server-side AI workflow and how it should be evaluated.",
    ],
    73: [
        "We have a Linux GPU machine and an existing language-model training repository. Set up a bounded experiment loop where each training change is compared under the same fixed runtime and validation metric.",
        "Our reusable workflow guide behaves inconsistently. We have four representative requests and binary checks; set up a frozen local improvement loop that keeps only measured improvements to the guide.",
    ],
    74: [
        "We need to contact about 200 new prospects per business day without damaging our main corporate domain. Design the sending-domain, mailbox, warm-up, and monitoring plan.",
        "Our opted-in newsletter now has falling opens, 2.4% total bounces, and occasional spam complaints. Audit the sending identity, hygiene, engagement, and remediation order.",
    ],
    75: [
        "I am a solo educator with six hours a week and one video channel. Build a sustainable four-week publishing system that I can maintain during a bad week.",
        "A brand team must schedule several social channels and short-form video around next month’s product launch. Build a four-week grid with per-channel cadence, campaign dates, assets, and reactive capacity.",
    ],
    76: [
        "A local plumbing business has a duplicated map listing, an overly broad category, and inconsistent service areas. Produce the exact listing fixes and a weekly owner routine.",
        "A local plumbing company has a verified business listing but still loses map-pack searches to nearby competitors. Create a 90-day plan for service pages, truthful city pages, citation cleanup, and remeasurement.",
    ],
    78: [
        "I am preparing my own scientific manuscript for submission. Help me audit its evidence traceability, reporting coverage, declarations, and internal consistency before the accountable authors approve it.",
        "I am authorised to review a confidential preprint for a journal. Prepare a structured, constructive review plan that checks claims, methods, reproducibility, ethics, and figures without making an editorial decision.",
    ],
    79: [
        "Organic traffic fell after a site migration. We have access to a search-performance console and need a prioritised diagnosis of crawlability, indexation, technical foundations, and on-page issues.",
        "Our traditional rankings are stable, but competitors are cited in generative answers and our product information is difficult for automated assistants to extract. Audit the answer-citation visibility and the highest-value improvements.",
    ],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_bound_ok(path: Path, ref: str) -> bool:
    match = re.fullmatch(r"L(\d+)-L(\d+)", ref)
    if not match:
        return False
    first, last = map(int, match.groups())
    return 1 <= first <= last <= len(path.read_text(encoding="utf-8").splitlines())


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in records), encoding="utf-8")


def main() -> None:
    queue_rows = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line]
    selected = [r for r in queue_rows if 61 <= r["review_order"] <= 79]
    assert len(selected) == 19
    assert set(DECISIONS) == {r["review_order"] for r in selected}

    review_rows: list[dict] = []
    prompt_rows: list[dict] = []
    source_refs = []
    line_refs_ok = 0
    for row in selected:
        order = row["review_order"]
        decision = DECISIONS[order]
        sources = row["candidate_sources"]
        assert len(sources) == 2
        boundaries = []
        for source, boundary, refs in zip(sources, decision["b"], decision["lines"], strict=True):
            source_path = Path(source["source_path"])
            assert source_path.is_file()
            assert sha(source_path) == source["source_sha256"]
            assert all(line_bound_ok(source_path, ref) for ref in refs)
            line_refs_ok += len(refs)
            source_refs.append(source)
            boundaries.append({
                "candidate_skill_id": source["candidate_skill_id"],
                "necessary_boundary": boundary,
                "source_evidence": {
                    "source_path": source["source_path"],
                    "source_sha256": source["source_sha256"],
                    "source_binding": source["source_binding"],
                    "provenance_status": source["provenance_status"],
                    "line_refs": refs,
                },
            })
        review_rows.append({
            "review_order": order,
            "review_queue_id": row["review_queue_id"],
            "parent_rq1_cluster_id": row["parent_rq1_cluster_id"],
            "nc_lead_id": row["nc_lead_id"],
            "nc_intake_arm": row["nc_intake_arm"],
            "primary_field": row["primary_field"],
            "candidate_cardinality": row["candidate_cardinality"],
            "candidate_skill_ids": [s["candidate_skill_id"] for s in sources],
            "bounded_shared_envelope": decision["e"],
            "necessary_candidate_boundaries": boundaries,
            "relation_risks": {
                "assessment": decision["risk"],
                "initial_queue_risk_note": row["initial_risk_note"],
            },
            "disposition": decision["d"],
            "disposition_rationale": decision["why"],
            "review_protocol": "FULL_PRESERVED_SOURCE_ONLY_NO_RQ1_CLUSTER_CARD_PROMPT_GOLD_ACCEPTABLE_LABEL_SELECTOR_OUTPUT_OR_METRIC",
            "status": "SOURCE_ONLY_RQ2_RE_REVIEW_COMPLETE_NOT_A_GOLD_LABEL_OR_ADMISSION_DECISION",
        })
        if decision["d"] == P:
            assert order in PROMPT_TEXT and len(PROMPT_TEXT[order]) == 2
            for index, (source, prompt) in enumerate(zip(sources, PROMPT_TEXT[order], strict=True), start=1):
                prompt_rows.append({
                    "prompt_id": f"RQ2B-NC-RQ1-REAUTH-B004-{order:03d}-{index:02d}",
                    "review_queue_id": row["review_queue_id"],
                    "parent_rq1_cluster_id": row["parent_rq1_cluster_id"],
                    "family_id": None,
                    "candidate_skill_id": source["candidate_skill_id"],
                    "author_intended_candidate_source_sha256": source["source_sha256"],
                    "authoring_basis": "SOURCE_ONLY_RE_REVIEW_OF_PRESERVED_CANDIDATE_SOURCES_WITHOUT_RQ1_CLUSTER_CARDS_PROMPTS_LABELS_SELECTOR_OUTPUTS_OR_METRICS",
                    "initial_cue_audit": "PASS_WITH_INTRINSIC_TASK_STATE_CUES: avoids candidate title, provider identity, and source path; the stated actor, artifact, evidence state, or workflow phase is necessary for the source-derived boundary.",
                    "prompt": prompt,
                    "visibility": "PRIVATE_AUTHORING_ONLY",
                    "status": "AUTHORING_DRAFT_NOT_A_GOLD_LABEL_OR_ADMITTED_RQ2_CASE",
                })
    assert len(prompt_rows) == 28
    assert {r["candidate_skill_id"] for r in prompt_rows} == {
        sid for record in review_rows if record["disposition"] == P for sid in record["candidate_skill_ids"]
    }
    assert not set(PROMPT_TEXT) - {r["review_order"] for r in review_rows if r["disposition"] == P}

    write_jsonl(REVIEW, review_rows)
    write_jsonl(PROMPTS, prompt_rows)
    forbidden = {"SKILL.original.md", "/Users/", "rq1_frozen_cluster", "gold", "selector"}
    assert all(not any(token.casefold() in p["prompt"].casefold() for token in forbidden) for p in prompt_rows)
    summary = {
        "status": "PASS_BATCH_004_SOURCE_ONLY_RE_REVIEW_AND_PRIVATE_AUTHORING_NOT_A_GOLD_FREEZE",
        "date": "2026-08-31",
        "input": {"path": str(QUEUE.relative_to(ROOT)), "sha256": sha(QUEUE), "reviewed_queue_rows": "review_order 61-79"},
        "artifacts": {str(REVIEW.relative_to(ROOT)): sha(REVIEW), str(PROMPTS.relative_to(ROOT)): sha(PROMPTS)},
        "counts": {
            "review_rows": len(review_rows),
            "disposition_counts": dict(Counter(r["disposition"] for r in review_rows)),
            "candidate_source_references": len(source_refs),
            "unique_candidate_source_paths": len({s["source_path"] for s in source_refs}),
            "unique_candidate_source_hashes": len({s["source_sha256"] for s in source_refs}),
            "private_authoring_prompts": len(prompt_rows),
            "unique_prompt_ids": len({p["prompt_id"] for p in prompt_rows}),
            "unique_prompt_candidates": len({p["candidate_skill_id"] for p in prompt_rows}),
            "promoted_family_ids": 0,
        },
        "mechanical_validation": {
            "jsonl_parse": "PASS",
            "review_to_queue_metadata_alignment": "PASS",
            "source_path_readability": "PASS_38_OF_38",
            "source_sha256_match": "PASS_38_OF_38",
            "source_line_ref_bounds": f"PASS_{line_refs_ok}_OF_{line_refs_ok}",
            "promoted_candidate_prompt_coverage": "PASS_ONE_PROMPT_PER_CANDIDATE",
            "prompt_intended_source_hash_alignment": "PASS",
            "prompt_status_and_visibility": "PASS_PRIVATE_AUTHORING_NOT_GOLD",
            "prompt_forbidden_candidate_provider_path_string_scan": "PASS",
            "nonpromoted_prompt_exclusion": "PASS",
            "provenance_status_counts": dict(Counter(s["provenance_status"] for s in source_refs)),
        },
        "family_ids": [],
        "claim_boundary": [
            "The review ledger records source-only semantic dispositions and is not a gold-label, acceptable-set, or admission decision.",
            "The private prompt file preserves author-intended source hashes and is not a target-blinded packet.",
            "No historic RQ1 prompt/gold/acceptable label, selector output, retrieval result, experiment metric, target-blinded review, admission artifact, or thesis result is read or produced.",
            "All source references retain their queue provenance status; semantic promotion does not cure immutable-provenance failure.",
            "No family_id is assigned because these fourteen promoted pairs do not form a demonstrated cross-cluster correlated family in this batch.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
