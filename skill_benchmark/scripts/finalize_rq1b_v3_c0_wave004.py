#!/usr/bin/env python3
"""Record the completed source-only C0 Wave 004 triage decision ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave004-finaliser-v1"
DECISIONS = {
    "001": ("ADVANCE_C1_SOURCE_EVIDENCE", "Checkout-system architecture, conversion-surface diagnosis, and evidence-bounded checkout-friction audit have distinct source-visible inputs, operations, and deliverables within ecommerce checkout."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "The multi-topic AI/RAG resource router is not a standalone peer procedure beside the two injection-defence sources."),
    "003": ("REJECT_NONPARALLEL_OR_COMPONENT", "Spark migration is a parent router to bundled paths, not a peer operation beside Spark tuning and general Spark guidance."),
    "004": ("REJECT_NONPARALLEL_OR_COMPONENT", "Baseline, sync, and archive are sequential lifecycle stages of one OpenSpec change rather than alternative first-route skills."),
    "005": ("REJECT_NONPARALLEL_OR_COMPONENT", "Adapter authoring, browser operation, and a generic read-only fallback are not parallel OpenCLI candidate roles."),
    "006": ("ADVANCE_C1_SOURCE_EVIDENCE", "Targeted Semgrep scanning, SAST configuration review, and multi-tool finding orchestration expose distinct source-visible input-output chains within static application-security work."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "Full Hono application construction materially overlaps the RPC and scaffolding roles and therefore acts as a broad container."),
    "008": ("REJECT_NO_COMMON_ENVELOPE", "Mac-local agent hosting, remote-Mac fleet operation, and Things task management share only a platform cue."),
    "009": ("REJECT_NONPARALLEL_OR_COMPONENT", "Zoom Meeting SDK integration is a vendor wrapper component beside Blueprint architecture and a broad Unreal Engine umbrella."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "Internal Phoenix OTel development is a component-level role beside application tracing and broad platform operation."),
    "011": ("REJECT_NO_COMMON_ENVELOPE", "Consumer finance planning and engineering technical-debt planning do not share a bounded operational envelope."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "WeChat adapter setup is not a peer workflow beside group-digest creation and Official Account publishing."),
    "013": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All three sources provision or administer AlloyDB clusters and instances without a source-stated routing boundary."),
    "014": ("REJECT_NONPARALLEL_OR_COMPONENT", "The general OSINT-methods source substantially contains the specialised social-profile and CTF OSINT work."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "General GDPR/privacy engineering is a broad container beside breach-notification and jurisdiction-specific diligence workflows."),
    "016": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The SRE/reliability sources substantially overlap on SLO, readiness, incident, and automation work."),
    "017": ("REJECT_NONPARALLEL_OR_COMPONENT", "React component conversion, a Stitch skill collection, and an MCP/CLI integration are not parallel candidate roles."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "Full Spring Boot engineering is a broad container for testing and architecture guidance, rather than a peer operation."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Store onboarding and order reconciliation have different lifecycle roles, and the preview-store source is not parallel to the live-store setup source."),
    "020": ("REJECT_NO_COMMON_ENVELOPE", "Gemini video generation/editing and GitHub skill import share only a title token, not an operational envelope."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "A full webinar funnel and a broad webinar-content umbrella subsume the standalone registration-page task."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "GKE golden-image discovery and storage provisioning are components of the broader GKE operation source."),
    "023": ("REJECT_NO_COMMON_ENVELOPE", "Sports-video, social-carousel, and shell/Makefile scripting use incompatible inputs and outputs."),
    "024": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The three SEO keyword sources all research, expand, and cluster terms for content planning, with overlap exceeding their deliverable differences."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "Generic due diligence materially overlaps the private-equity and real-estate specialised diligence workflows."),
    "026": ("REJECT_NO_COMMON_ENVELOPE", "Crypto tax record intake, accounting, and investment rating do not compete within one bounded first-route task."),
    "027": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "Email nurture-sequence and behaviour-gated drip construction overlap materially; pacing does not restore three distinct peer roles."),
    "028": ("ADVANCE_C1_SOURCE_EVIDENCE", "Cross-platform dbt migration, legacy SQL-to-dbt modularisation, and Dagster-to-Airflow migration have distinct source-to-target inputs, procedures, and validation deliverables."),
    "029": ("REJECT_NO_COMMON_ENVELOPE", "Prime Intellect product navigation, RL environment construction, and repository-context summarisation share no operational envelope."),
    "030": ("REJECT_NONPARALLEL_OR_COMPONENT", "The RDD-specific method is an explicit branch within two umbrella causal-inference workflows."),
}
AGENT_ADVANCES = {"001", "004", "005", "006", "007", "014", "015", "018", "024", "025", "027", "028"}
PRINCIPAL_OVERRIDES = {"004", "005", "007", "014", "015", "018", "024", "025", "027"}


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
    checkpoint_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_004_CHECKPOINT.md"
    finaliser_audit_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_004_FINALISER_AUDIT.json"
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
        "# RQ1b V3 C0 Source-Only Review Wave 004\n\n"
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
        "Wave 004 retained three source-evidence candidates after principal review. Nine otherwise plausible agent advances were rejected because they were sequential lifecycle stages, a generic fallback, a broad container, or materially overlapping variants. The final ledger is feasibility evidence only: every survivor still needs C1 source cards, cue control, and two independent strict selection-only reviews before it could become a strict public cluster.\n\n"
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
