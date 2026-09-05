#!/usr/bin/env python3
"""Record the completed source-only C0 Wave 003 triage decision ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave003-finaliser-v1"
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "A vacuum-bloat implementation is a specialised component beside broad PostgreSQL troubleshooting and general PostgreSQL guidance."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "Image selection is a pre-deployment component, while the general vLLM and CPU-specific vLLM sources substantially overlap."),
    "003": ("REJECT_NO_COMMON_ENVELOPE", "Blockchain/Web3, HR recruiting, and security work do not form one bounded operational envelope."),
    "004": ("REJECT_NO_COMMON_ENVELOPE", "Catalog use, MLflow handoff, and production-default guidance do not establish one peer operational envelope."),
    "005": ("REJECT_NO_COMMON_ENVELOPE", "The three sources share only broad AI/architecture vocabulary rather than one bounded task envelope."),
    "006": ("ADVANCE_C1_SOURCE_EVIDENCE", "Covenant extraction with page citations, negotiated legal credit review, and borrower underwriting use distinct source-visible inputs and outputs within credit analysis."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "The chaos candidates are an implementation or specialised component of broader operational sources, not peer alternatives."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "The MariaDB sources mix broad database guidance with specialised implementation or interface material."),
    "009": ("REJECT_NONPARALLEL_OR_COMPONENT", "Interval operations are a method-level component, while hosted inference does not form a clean peer role with genomic annotation."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "The broad digest candidates subsume the Hacker News-specific digest, and the CLI form is an interface distinction rather than a peer operational role."),
    "011": ("REJECT_NONPARALLEL_OR_COMPONENT", "The SaaS metrics sources contain direct broad-to-specialised overlap rather than three peer first-route skills."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "The Firebase candidates mix setup, implementation, and broad container roles rather than parallel operations."),
    "013": ("REJECT_NONPARALLEL_OR_COMPONENT", "The Hugging Face candidates are reference, interface, and broader container material rather than peer task alternatives."),
    "014": ("REJECT_NONPARALLEL_OR_COMPONENT", "The Hacker News candidates mix interface/container forms and do not supply three parallel first-route operations."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "The HubSpot candidates mix broad operational containers with specialised components."),
    "016": ("REJECT_NONPARALLEL_OR_COMPONENT", "The general quantisation/deployment sources materially overlap the AWQ-specific method and retain strong product-method cues."),
    "017": ("REJECT_NONPARALLEL_OR_COMPONENT", "The Terraform candidates combine broad infrastructure workflow with narrower components or platform variants."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "The CloudWatch candidates combine broad monitoring workflows with specialised implementation or interface roles."),
    "019": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The software-composition analysis, audit, and Black Duck scan sources overlap too substantially; the latter is implementation-bound."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "The UGC candidates contain broad strategy or creator-marketing containers that overlap the remaining candidate."),
    "021": ("REJECT_NO_COMMON_ENVELOPE", "Sentry, routing, and Zoom do not form a coherent common operational envelope."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "Multi-provider integration is a broad container and the finder is interface-like beside the narrower Pexels operation."),
    "023": ("REJECT_NONPARALLEL_OR_COMPONENT", "The GKE candidates combine broad operations with specialised components or interfaces rather than peer roles."),
    "024": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The AEO candidates substantially overlap on optimisation/readiness guidance and do not expose three distinct first-route operations."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "The tax sources combine broad optimisation and specialised tax-loss workflows with material overlap."),
    "026": ("REJECT_NONPARALLEL_OR_COMPONENT", "The redline candidates mix a broad template/container, a sentry workflow, and document-specific execution rather than peers."),
    "027": ("REJECT_NONPARALLEL_OR_COMPONENT", "The dbt candidates are broad/container or overlapping analytics-engineering material rather than parallel first-route skills."),
    "028": ("REJECT_NONPARALLEL_OR_COMPONENT", "The governance candidates are broad containers that substantially subsume catalogue, lineage, and PII operations."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "The Outlook candidates are overlapping connector/interface forms rather than distinct peer operations."),
    "030": ("ADVANCE_C1_SOURCE_EVIDENCE", "Prepared Socratic sequence generation, live adaptive never-answer questioning, and corrective guided questioning expose distinct source-visible interaction procedures."),
}
AGENT_ADVANCES = {"002", "006", "009", "010", "016", "019", "020", "022", "030"}
PRINCIPAL_OVERRIDES = {"002", "009", "010", "016", "019", "020", "022"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    args = parser.parse_args()
    roster_path = args.wave_dir / "c0_review_roster.jsonl"
    manifest_path = args.wave_dir / "c0_review_manifest.json"
    audit_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_AUDIT.json"
    ledger_path = args.wave_dir / "c0_review_final_ledger.jsonl"
    checkpoint_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_003_CHECKPOINT.md"
    finaliser_audit_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_003_FINALISER_AUDIT.json"
    if ledger_path.exists() or checkpoint_path.exists() or finaliser_audit_path.exists():
        raise ValueError("refusing to overwrite final C0 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    records = []
    for row in roster:
        suffix = row["c0_review_id"].rsplit("-", 1)[1]
        outcome, reason = DECISIONS[suffix]
        records.append(
            {
                "c0_review_id": row["c0_review_id"],
                "lexical_draft_id": row["lexical_draft_id"],
                "member_source_ids": [member["source_id"] for member in row["members"]],
                "member_titles": [member["title"] for member in row["members"]],
                "review_mode": "source-only independent model-assisted reviewers plus principal source recheck for all agent advances",
                "agent_recommendation": "ADVANCE_C1_SOURCE_EVIDENCE" if suffix in AGENT_ADVANCES else outcome,
                "final_c0_outcome": outcome,
                "principal_override": suffix in PRINCIPAL_OVERRIDES,
                "reason": reason,
                "claim_boundary": "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, field annotation, selector input, metric, semantic-fidelity claim, or strict routing result.",
            }
        )

    expected = {f"{index:03d}" for index in range(1, 31)}
    observed = {record["c0_review_id"].rsplit("-", 1)[1] for record in records}
    if len(records) != 30 or set(DECISIONS) != expected or observed != expected:
        raise ValueError("incomplete C0 roster binding")

    counts = Counter(record["final_c0_outcome"] for record in records)
    ledger_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    c1_ids = [record["c0_review_id"] for record in records if record["final_c0_outcome"] == "ADVANCE_C1_SOURCE_EVIDENCE"]
    checkpoint_path.write_text(
        "# RQ1b V3 C0 Source-Only Review Wave 003\n\n"
        "Status: `COMPLETE / FEASIBILITY CALIBRATION ONLY / NO GOLD OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Roster: `c0_review_roster.jsonl` (30 triads, 90 unique canonical sources).\n"
        "- Mechanical source-binding audit: `C0_SOURCE_REVIEW_WAVE_AUDIT.json` (`PASS`; no source reuse or hash drift).\n"
        "- Review constraint: reviewers read only assigned original source artifacts; no prompts, labels, representations, selector outputs, or online sources.\n"
        "- Distinct-title and non-contained-title settings ordered local review only; neither is a scientific inclusion/exclusion criterion or a field result.\n\n"
        "## Final C0 Disposition\n\n"
        "| Outcome | Triads |\n|---|---:|\n"
        f"| Advance to C1 source evidence | {counts['ADVANCE_C1_SOURCE_EVIDENCE']} |\n"
        f"| Reject: nonparallel/component/container | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: copy/derivative | {counts['REJECT_COPY_OR_DERIVATIVE']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n"
        f"| Reject: no common envelope | {counts['REJECT_NO_COMMON_ENVELOPE']} |\n\n"
        f"C1 triage advances: {', '.join(f'`{item}`' for item in c1_ids)}. They remain source-evidence candidates, not strict clusters.\n\n"
        "## Interpretation And Claim Boundary\n\n"
        "Wave 003 again shows that a broad, cross-origin lexical queue contains a high rate of containers, specialised components, and overlapping operational material. Seven agent suggestions were conservatively rejected after principal source recheck. The two surviving source-evidence candidates still require C1 source cards, cue control, and two independent strict selection-only reviews before they could form strict public clusters. This is not a prevalence/yield estimate or routing result.\n\n"
        "The final ledger is `c0_review_final_ledger.jsonl`. It records source-only feasibility dispositions and no prompt, gold label, selector input, metric, field prevalence, semantic-fidelity, or strict routing outcome.\n"
    )
    result = {
        "status": "PASS",
        "records": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "agent_advance_count": len(AGENT_ADVANCES),
        "principal_override_count": len(PRINCIPAL_OVERRIDES),
        "ledger_sha256": sha256_file(ledger_path),
        "roster_sha256": sha256_file(roster_path),
        "manifest_sha256": sha256_file(manifest_path),
        "audit_sha256": sha256_file(audit_path),
        "network_calls": 0,
        "texts_transmitted": 0,
    }
    finaliser_audit_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
