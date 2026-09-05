#!/usr/bin/env python3
"""Record the completed source-only C0 Wave 005 triage decision ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave005-finaliser-v1"
DECISIONS = {
    "001": ("ADVANCE_C1_SOURCE_EVIDENCE", "Kubernetes manifest generation, readiness audit/remediation, and rollout execution expose distinct source-visible input-output chains within workload delivery."),
    "002": ("REJECT_COPY_OR_DERIVATIVE", "The two HAR sources duplicate the same capture-to-derived-client pipeline; the MITM proxy does not make the triad parallel."),
    "003": ("ADVANCE_C1_SOURCE_EVIDENCE", "Attempted-work error diagnosis, fiction coaching, and IELTS grammar scoring/correction have distinct learner inputs, procedures, and deliverables."),
    "004": ("ADVANCE_C1_SOURCE_EVIDENCE", "Retainer-floor calculation, single-service package recommendation, and per-offering pricing optimisation use distinct source-visible data and outputs."),
    "005": ("REJECT_NO_COMMON_ENVELOPE", "Two target-specific database migrations and day-two MariaDB performance operation do not form one peer operational envelope."),
    "006": ("ADVANCE_C1_SOURCE_EVIDENCE", "Airflow upstream tracing, DataHub entity traversal, and MLOps data-to-model lineage use distinct sources, procedures, and lineage outputs."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "Reel editing, Instagram research, and publishing are upstream, research, and downstream lifecycle components rather than peer first-route skills."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "Practice setup, company-risk monitoring, and jurisdiction-specific bankruptcy procedure are not parallel operational roles."),
    "009": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The sales win/loss sources substantially overlap on deal-outcome analysis and recommendations."),
    "010": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The three churn sources substantially overlap on account risk/churn analysis despite scoring-format differences."),
    "011": ("REJECT_NONPARALLEL_OR_COMPONENT", "Ingestion is explicitly a component beside broad RAG infrastructure and full pipeline construction."),
    "012": ("REJECT_NO_COMMON_ENVELOPE", "dbt lineage visualisation, Cosmos orchestration, and BigQuery dbt modification do not form one operational envelope."),
    "013": ("REJECT_NONPARALLEL_OR_COMPONENT", "DORA measurement is a specialised component beside overlapping broad DevOps/SRE delivery roles."),
    "014": ("ADVANCE_C1_SOURCE_EVIDENCE", "Direct-open HTML deck production, constrained branded PowerPoint production, and visual-only deck specification have distinct source-visible output modes and boundaries."),
    "015": ("ADVANCE_C1_SOURCE_EVIDENCE", "AzureRM plan-diff analysis, Azure infrastructure provisioning, and general Terraform HCL generation expose distinct input and validation chains."),
    "016": ("REJECT_NO_COMMON_ENVELOPE", "Three.js scene composition, a fixed Earth-route renderer, and screenshot-led game graphics enhancement do not supply one peer task envelope."),
    "017": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The two current-MSK operational sources overlap materially; migration does not restore three distinct peer operations."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "Spark engineering and broad job optimisation substantially overlap the plan-specific diagnostic role."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Broad customer-journey strategy and analysis materially contain the specialised CSV gap analysis."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "Template authoring is a component beside end-to-end Nuclei/DAST scanning workflows."),
    "021": ("REJECT_NO_COMMON_ENVELOPE", "Downstream-dependency circuit breaking and agent tool-loop diagnosis do not compete within a bounded task envelope."),
    "022": ("ADVANCE_C1_SOURCE_EVIDENCE", "Negative-keyword draft analysis, shared-list execution, and performance diagnostics provide distinct source-visible Google Ads operations."),
    "023": ("ADVANCE_C1_SOURCE_EVIDENCE", "Spoken-argument slide design, investor-data PPTX generation, and source-to-presentation transformation have distinct inputs and output formats."),
    "024": ("REJECT_NO_COMMON_ENVELOPE", "Kanban UI design, a coding-workspace control plane, and live Asana mutation share terminology but not an operational envelope."),
    "025": ("REJECT_NO_COMMON_ENVELOPE", "Game feedback triage, CI/CD work, and performance profiling share only a broad domain rather than one competing task envelope."),
    "026": ("ADVANCE_C1_SOURCE_EVIDENCE", "Oracle-to-PostgreSQL, Oracle-to-Percona, and Oracle-to-MariaDB have explicit target and compatibility boundaries with distinct migration procedures."),
    "027": ("REJECT_NONPARALLEL_OR_COMPONENT", "The auto-loaded framework catalogue is not a bounded peer skill beside RICE scoring and interactive method selection."),
    "028": ("REJECT_NONPARALLEL_OR_COMPONENT", "General TRL post-training materially contains the GRPO and verifier-gated RLVR specialisations."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "Apple platform workout implementation is not parallel to end-user fitness lookup and coaching work."),
    "030": ("ADVANCE_C1_SOURCE_EVIDENCE", "Ranked incident hypotheses, software-bug RCA with remediation, and account-specific read-only RCA use distinct inputs, procedures, and output boundaries."),
}
AGENT_ADVANCES = {"001", "003", "004", "006", "009", "010", "014", "015", "016", "017", "018", "019", "022", "023", "025", "026", "028", "030"}
PRINCIPAL_OVERRIDES = {"009", "010", "016", "017", "018", "019", "025", "028"}


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
    checkpoint_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_005_CHECKPOINT.md"
    finaliser_audit_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_005_FINALISER_AUDIT.json"
    if ledger_path.exists() or checkpoint_path.exists() or finaliser_audit_path.exists():
        raise ValueError("refusing to overwrite final C0 decisions")
    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    records = []
    for row in roster:
        suffix = row["c0_review_id"].rsplit("-", 1)[1]
        outcome, reason = DECISIONS[suffix]
        records.append({
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
        })
    expected = {f"{index:03d}" for index in range(1, 31)}
    observed = {record["c0_review_id"].rsplit("-", 1)[1] for record in records}
    if len(records) != 30 or set(DECISIONS) != expected or observed != expected:
        raise ValueError("incomplete C0 roster binding")
    counts = Counter(record["final_c0_outcome"] for record in records)
    ledger_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    c1_ids = [record["c0_review_id"] for record in records if record["final_c0_outcome"] == "ADVANCE_C1_SOURCE_EVIDENCE"]
    checkpoint_path.write_text(
        "# RQ1b V3 C0 Source-Only Review Wave 005\n\n"
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
        "Wave 005 retained ten source-evidence candidates. Eight agent advances were rejected at C0 because they were broad containers, overlapping variants, or lacked one peer envelope. C0 uses a lower bar than strict singleton routing: a survivor only warrants construction of a source-evidence card. It must still pass cue control and two independent strict selection-only reviews before it can be a valid public cluster.\n\n"
        "The final ledger is `c0_review_final_ledger.jsonl`. It records source-only feasibility dispositions and no prompt, gold label, selector input, metric, field prevalence, semantic-fidelity, or strict routing outcome.\n"
    )
    result = {
        "status": "PASS", "records": len(records), "outcome_counts": dict(sorted(counts.items())),
        "agent_advance_count": len(AGENT_ADVANCES), "principal_override_count": len(PRINCIPAL_OVERRIDES),
        "ledger_sha256": sha256_file(ledger_path), "roster_sha256": sha256_file(roster_path),
        "manifest_sha256": sha256_file(manifest_path), "audit_sha256": sha256_file(audit_path),
        "network_calls": 0, "texts_transmitted": 0,
    }
    finaliser_audit_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
