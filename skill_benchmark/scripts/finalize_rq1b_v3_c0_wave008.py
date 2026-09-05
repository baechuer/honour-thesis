#!/usr/bin/env python3
"""Freeze the completed source-only C0 Wave 008 lexical-triage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave008-finaliser-v1"
BOUNDARY = (
    "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, "
    "field annotation, selector input, metric, semantic-fidelity claim, or strict routing result."
)
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "Exa content access, a CLI wrapper, and a general search route are interface/container alternatives rather than peer operational routes."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "Cloud development, setup prerequisites, and CloudFormation deployment are lifecycle or container roles, not peer routes."),
    "003": ("REJECT_COPY_OR_DERIVATIVE", "The Remotion implementation is a wrapper or derivative of a broader route rather than an independently routeable peer."),
    "004": ("REJECT_NONPARALLEL_OR_COMPONENT", "Backlink-gap analysis is a specialised component inside a broader audit/container workflow."),
    "005": ("ADVANCE_C1_SOURCE_EVIDENCE", "Figma component documentation, design-system library construction, and screen construction have explicit, distinct source-grounded input-output roles under a Figma design-work envelope. C1 must still reject the composition if library-to-screen or component-documentation lifecycle dependence makes more than one route fully adequate."),
    "006": ("REJECT_NONPARALLEL_OR_COMPONENT", "Short-form video production, data collection, and broad marketing planning are not three peer routes."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "A data-visualisation specification is an upstream design artifact beside two overlapping infographic-rendering routes."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "Responsive Flutter implementation is a subprocedure beside broad guide/container artifacts."),
    "009": ("REJECT_NONPARALLEL_OR_COMPONENT", "Landing-page execution, category work, and a broad copywriting container do not form peer routes."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "Antitrust-clause analysis is specialised work beside broad contract and transaction-review containers."),
    "011": ("REJECT_NONPARALLEL_OR_COMPONENT", "A monthly budget-variance review is subsumed by broad budget-planning artifacts rather than forming three peer operational routes."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "RFP response drafting and supplier-bid comparison occupy respondent versus evaluator roles; the response writers also overlap materially."),
    "013": ("REJECT_NONPARALLEL_OR_COMPONENT", "Crisis communication is a lifecycle component or router rather than a parallel peer route."),
    "014": ("REJECT_NO_COMMON_ENVELOPE", "The shared miner token is lexical polysemy and does not establish a common task envelope."),
    "015": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The Helm creation artifacts overlap too materially to establish distinct peer routes."),
    "016": ("REJECT_NO_COMMON_ENVELOPE", "Legal cash-collateral issue spotting, financial-statement cash-flow reconciliation, and operating liquidity management do not share a bounded peer envelope."),
    "017": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All three artifacts tailor and emit job-application resumes; their differences are packaging, handoff, or interface details."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "SOC2 criteria mapping and evidence collection are specialised components inside a broad compliance implementation container."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Namespace troubleshooting and network management are specialised paths inside broad Kubernetes debugging."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "Ralph preparation is explicitly upstream of a loop, and the GitHub loop is an interface-specialised loop implementation."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "A meta-description writer is contained by the broad SEO-content writers rather than being a peer alternative."),
    "022": ("REJECT_NO_COMMON_ENVELOPE", "CentOS triage, Linux administration, and Zoom SDK bot work do not share one operational envelope."),
    "023": ("REJECT_NONPARALLEL_OR_COMPONENT", "A campaign-content calendar and affiliate scheduler are specialised planning routes within broad social-media strategy."),
    "024": ("REJECT_NONPARALLEL_OR_COMPONENT", "A coordinate-explicit slide specification is an upstream implementation contract beside overlapping PPTX generation/manipulation routes."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "Curriculum sequencing is a method within curriculum development, while knowledge-architecture diagnosis is an upstream analysis role."),
    "026": ("REJECT_NONPARALLEL_OR_COMPONENT", "Sales hiring and compensation are component procedures inside a broad sales-and-revenue-operations container."),
    "027": ("REJECT_NO_COMMON_ENVELOPE", "SEO backlink outreach targets publishers, whereas the remaining candidates build B2B buyer pipelines."),
    "028": ("REJECT_NONPARALLEL_OR_COMPONENT", "AlloyDB replication exposes a provider-specific script interface rather than a peer diagnosis/remediation route."),
    "029": ("REJECT_NO_COMMON_ENVELOPE", "GCP data-pipeline provisioning, complete IDP rollout, and Compute Engine management share a platform name but not one operation."),
    "030": ("REJECT_NONPARALLEL_OR_COMPONENT", "Generic CSS theming is subsumed by a broad frontend-theming container, while the Shiny artifact is a specialised framework implementation."),
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
    source_audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_AUDIT.json"
    ledger_path = wave_dir / "c0_review_final_ledger.jsonl"
    checkpoint_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_008_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_008_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C0 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    source_audit = json.loads(source_audit_path.read_text())
    if source_audit.get("status") != "PASS":
        raise ValueError("source-binding audit must pass before finalisation")
    expected = {f"{index:03d}" for index in range(1, 31)}
    if len(roster) != 30 or set(DECISIONS) != expected:
        raise ValueError("incomplete C0 Wave 008 decision binding")

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
        "# RQ1b V3 C0 Source-Only Review Wave 008\n\n"
        "Status: `COMPLETE / LEXICAL-QUEUE FEASIBILITY CALIBRATION / NO GOLD OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Roster: `c0_review_roster.jsonl` (30 triads, 90 unique canonical sources).\n"
        "- Mechanical source-binding audit: `C0_SOURCE_REVIEW_WAVE_AUDIT.json` (`PASS`; no source reuse or hash drift).\n"
        "- Review constraint: reviewers read only assigned original source artifacts; no prompts, labels, representations, selector outputs, or online sources.\n\n"
        "## Final C0 Disposition\n\n"
        "| Outcome | Triads |\n|---|---:|\n"
        f"| Advance to C1 source evidence | {counts['ADVANCE_C1_SOURCE_EVIDENCE']} |\n"
        f"| Reject: nonparallel/component/container | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: copy/derivative | {counts['REJECT_COPY_OR_DERIVATIVE']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n"
        f"| Reject: no common envelope | {counts['REJECT_NO_COMMON_ENVELOPE']} |\n\n"
        "## Interpretation And Claim Boundary\n\n"
        "Only `RQ1B-V3-C0-W8-005` may proceed to C1 source-evidence cards. It has distinct Figma component-documentation, design-system-library and screen-construction roles, but C1 must reject it if the sources show lifecycle dependence or more than one fully adequate route. It has no prompt, intended winner, gold label, field card, selector representation, metric, or strict routing result.\n\n"
        "The other 29 lexical drafts were rejected before C1: 20 for nonparallel/component/container structure, two for insufficient operational contrast, one copy/derivative case, and six for no common envelope. This calibrates this local lexical-discovery path; it does not estimate public-cluster prevalence, strict-triad yield, field recoverability, or retrieval performance.\n"
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
        "source_binding_audit_sha256": sha256_file(source_audit_path),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    finaliser_audit_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
