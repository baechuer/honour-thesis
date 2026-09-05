#!/usr/bin/env python3
"""Freeze the completed source-only C0 Wave 007 lexical-triage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave007-finaliser-v1"
BOUNDARY = (
    "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, "
    "field annotation, selector input, metric, semantic-fidelity claim, or strict routing result."
)
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "AgentCore lifecycle setup and a product-specific deployment route are containers or lifecycle steps rather than peer operational routes."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "Authority-mark checking is a specialised research subprocedure beside a broad keyword-research route."),
    "003": ("REJECT_NO_COMMON_ENVELOPE", "The shared Airflow title signal does not establish one bounded peer task across the three artifacts."),
    "004": ("REJECT_NONPARALLEL_OR_COMPONENT", "Defect diagnosis, testing, and reference material are nonparallel stages or support artifacts."),
    "005": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The OKR artifacts overlap materially and do not expose three independently routeable operational roles."),
    "006": ("ADVANCE_C1_SOURCE_EVIDENCE", "Traffic decline, blog-content decay, and ad-creative fatigue are source-grounded diagnostic routes under a performance-decay envelope; C1 must still test overlap between SEO traffic and content-decay routes."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "Telegram installation and bridge components are not peer routes to a broad Telegram bot/API workflow."),
    "008": ("REJECT_NO_COMMON_ENVELOPE", "Affiliate-program design, directory submission, and referral-program strategy are different lifecycle purposes, not three peer routes."),
    "009": ("REJECT_NONPARALLEL_OR_COMPONENT", "Prompt authoring is a component beside hosted image-generation and platform-specific design containers."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "A reflected-XSS check is contained by broad XSS approaches and does not form a peer route."),
    "011": ("REJECT_NO_COMMON_ENVELOPE", "The shared term spike is lexical polysemy rather than a bounded common operation."),
    "012": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The code-complexity scanner artifacts overlap too strongly to justify distinct peer routes."),
    "013": ("REJECT_NONPARALLEL_OR_COMPONENT", "UTM operations are an execution component within broader campaign or attribution strategy."),
    "014": ("REJECT_NONPARALLEL_OR_COMPONENT", "Pseudolocalisation is an implementation component, not a peer route to the broader internationalisation work."),
    "015": ("REJECT_NO_COMMON_ENVELOPE", "Privacy legal analysis and vendor-oriented work do not form one bounded three-way peer envelope."),
    "016": ("REJECT_NO_COMMON_ENVELOPE", "The culture-labelled artifacts concern incompatible settings and do not share one operational envelope."),
    "017": ("REJECT_NONPARALLEL_OR_COMPONENT", "A generic CRM integration container subsumes the specialised ingest and cross-CRM synchronization routes."),
    "018": ("ADVANCE_C1_SOURCE_EVIDENCE", "Threat-intelligence enrichment, intelligence-product production, and actor-focused SIEM hunting are distinct source-grounded routes under a threat-intelligence workflow envelope; C1 must reject them if the source cards reveal merely producer-consumer lifecycle containment."),
    "019": ("REJECT_NO_COMMON_ENVELOPE", "Gitea runner material, CI coordination, and GitHub Actions work do not define a common three-way task."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "The SLA artifact is a lifecycle component rather than a peer operational route."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "A2A containers and interface-specific implementations are not peer routes."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "Pitch creation, general speech support, and discovery are different communication lifecycle stages."),
    "023": ("REJECT_NONPARALLEL_OR_COMPONENT", "Six-hats reasoning is a component or meta-method beside assessment and history workflows."),
    "024": ("REJECT_NO_COMMON_ENVELOPE", "The financial artifacts are too broad and heterogeneous to establish a bounded peer operation."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "Crisis workflow handling and public-statement production occupy different operational stages."),
    "026": ("REJECT_NONPARALLEL_OR_COMPONENT", "A broad WhatsApp Cloud API bot route contains business-automation use cases, while the NanoClaw member is an implementation adapter."),
    "027": ("REJECT_NONPARALLEL_OR_COMPONENT", "Broad Hebrew SEO/GEO and workflow-router artifacts contain the specialised hreflang audit."),
    "028": ("REJECT_NONPARALLEL_OR_COMPONENT", "General C# development contains LINQ optimisation and MSTest verification as component concerns."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "Generic prompt refinement contains the pipeline-specific refiner, while repository-wide skill refinement has a different artifact lifecycle."),
    "030": ("REJECT_NO_COMMON_ENVELOPE", "Two container-registry routes and a local Azure SQL runtime share an incidental registry prerequisite, not a common task."),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    args = parser.parse_args()
    wave_dir = args.wave_dir
    roster_path = wave_dir / "c0_review_roster.jsonl"
    manifest_path = wave_dir / "c0_review_manifest.json"
    audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_AUDIT.json"
    ledger_path = wave_dir / "c0_review_final_ledger.jsonl"
    checkpoint_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_007_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_007_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C0 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    mechanical_audit = json.loads(audit_path.read_text())
    if mechanical_audit.get("status") != "PASS":
        raise ValueError("source-binding audit must pass before finalisation")
    expected = {f"{index:03d}" for index in range(1, 31)}
    if len(roster) != 30 or set(DECISIONS) != expected:
        raise ValueError("incomplete C0 Wave 007 decision binding")

    records = []
    for row in roster:
        suffix = row["c0_review_id"].rsplit("-", 1)[1]
        outcome, reason = DECISIONS[suffix]
        records.append({
            "c0_review_id": row["c0_review_id"],
            "lexical_draft_id": row["lexical_draft_id"],
            "member_source_ids": [member["source_id"] for member in row["members"]],
            "member_titles": [member["title"] for member in row["members"]],
            "review_mode": "source-only independent review plus principal source recheck",
            "final_c0_outcome": outcome,
            "reason": reason,
            "claim_boundary": BOUNDARY,
        })
    observed = {record["c0_review_id"].rsplit("-", 1)[1] for record in records}
    if observed != expected:
        raise ValueError("roster identifiers do not match frozen decision mapping")
    counts = Counter(record["final_c0_outcome"] for record in records)
    ledger_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    checkpoint_path.write_text(
        "# RQ1b V3 C0 Source-Only Review Wave 007\n\n"
        "Status: `COMPLETE / LEXICAL-QUEUE FEASIBILITY CALIBRATION / NO GOLD OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Roster: `c0_review_roster.jsonl` (30 triads, 90 unique canonical sources).\n"
        "- Mechanical source-binding audit: `C0_SOURCE_REVIEW_WAVE_AUDIT.json` (`PASS`; no source reuse or hash drift).\n"
        "- Review constraint: reviewers read only assigned original source artifacts; no prompts, labels, representations, selector outputs, or online sources.\n\n"
        "## Final C0 Disposition\n\n"
        "| Outcome | Triads |\n|---|---:|\n"
        f"| Advance to C1 source evidence | {counts['ADVANCE_C1_SOURCE_EVIDENCE']} |\n"
        f"| Reject: nonparallel/component/container | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n"
        f"| Reject: no common envelope | {counts['REJECT_NO_COMMON_ENVELOPE']} |\n\n"
        "## Interpretation And Claim Boundary\n\n"
        "Two triads may proceed only to C1 source-evidence cards. The performance-decay triad requires C1 to test whether traffic and content decay are overlapping routes; the threat-intelligence triad requires C1 to test whether enrichment, product production, and hunting are merely a producer-consumer lifecycle. Neither has a prompt, intended winner, gold label, acceptable set, field card, selector representation, metric, or strict routing result.\n\n"
        "The other 28 lexical-title/local-FTS drafts were rejected before C1, principally because a broad container subsumed a specialised component or the title overlap did not imply one competing task envelope. This calibrates this particular discovery method; it is not a prevalence estimate, public-cluster yield, or retrieval result.\n"
    )
    result = {
        "status": "PASS",
        "version": VERSION,
        "records": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "c1_advance_count": counts["ADVANCE_C1_SOURCE_EVIDENCE"],
        "ledger_sha256": sha256_file(ledger_path),
        "roster_sha256": sha256_file(roster_path),
        "manifest_sha256": sha256_file(manifest_path),
        "source_binding_audit_sha256": sha256_file(audit_path),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    finaliser_audit_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
