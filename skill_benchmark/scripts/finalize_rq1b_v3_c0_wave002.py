#!/usr/bin/env python3
"""Record the completed source-only C0 Wave 002r1 triage decision ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave002r1-finaliser-v1"
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "Cilium architecture analysis is a conceptual prerequisite beside gateway configuration and operational policy management."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "The broad alerting/on-call source subsumes platform-specific PagerDuty/Opsgenie and Grafana work."),
    "003": ("REJECT_NONPARALLEL_OR_COMPONENT", "Schema-registry design is a broad container for contract governance and Kafka compatibility work."),
    "004": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All sources cover the end-to-end blameless postmortem process, differing mainly in emphasis and template depth."),
    "005": ("ADVANCE_C1_SOURCE_EVIDENCE", "Finland employer-process construction, general HR mobility administration, and UK document compliance review have distinct source-visible jurisdictions, inputs, and outputs."),
    "006": ("REJECT_NO_COMMON_ENVELOPE", "AWS CI/CD deployment and broad AWS solution architecture do not form one sufficiently narrow operational envelope."),
    "007": ("ADVANCE_C1_SOURCE_EVIDENCE", "Framework-agnostic SHAP analysis, DataRobot explanation retrieval, and scikit-learn inspection expose distinct source-visible tool contexts and explanation operations."),
    "008": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The GEO candidates largely offer overlapping website/content optimisation and readiness guidance."),
    "009": ("REJECT_NONPARALLEL_OR_COMPONENT", "GPU sharing is a component of the two broader GPU cluster infrastructure and operations sources."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "The CTI lifecycle container includes the threat-hunting work of the other sources."),
    "011": ("ADVANCE_C1_SOURCE_EVIDENCE", "Dagster/Prefect authoring, AI pipeline orchestration, and end-to-end pipeline design/review have distinct source-visible implementation contexts and deliverables."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "Dependency setup is a prerequisite, not a peer operation to agent-control-flow implementation or broad architecture guidance."),
    "013": ("ADVANCE_C1_SOURCE_EVIDENCE", "Tauri IPC debugging, secure IPC implementation, and maintainability auditing are distinct source-visible operations with different inputs and outputs."),
    "014": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The supply-chain security sources substantially overlap on SBOM, provenance, policy, and audit work."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "PostgreSQL syntax guidance is not a peer operational alternative to service-specific Azure or Aurora database tooling."),
    "016": ("REJECT_NONPARALLEL_OR_COMPONENT", "Principal recheck: the general geospatial-analysis source includes raster and vector analysis, materially overlapping the specialised GeoPandas source rather than forming a peer role."),
    "017": ("REJECT_NONPARALLEL_OR_COMPONENT", "A multi-agent patent umbrella contains the narrower triage and market-signal roles."),
    "018": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The SBOM sources overlap materially on generation, policy, provenance, and supply-chain controls."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Conceptual GitOps mechanics and tool-bound GitOps operation are not peer alternatives to an end-to-end ArgoCD provisioning workflow."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "The BDD/ATDD lifecycle container is not parallel to plan-stage Gherkin authoring or narrow scenario-editing rules."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "KYC rules scoring is an explicit downstream component of the broader onboarding review, while vendor risk research has a different subject."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "Framework reference material is not a peer task alternative to executed well-architected reviews."),
    "023": ("ADVANCE_C1_SOURCE_EVIDENCE", "Smart-contract security assessment, full-stack DApp construction, and contract-test authoring are distinct source-visible lifecycle operations."),
    "024": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The general service-mesh source materially overlaps the Istio installation and operation candidate."),
    "025": ("REJECT_NO_COMMON_ENVELOPE", "Flutter/Dart is only a platform cue across SDK upgrade, monitoring integration, and database CRUD work."),
    "026": ("ADVANCE_C1_SOURCE_EVIDENCE", "Single-conversation response, queue triage/resolution, and trigger-based communication automation expose distinct source-visible Intercom operations."),
    "027": ("REJECT_NONPARALLEL_OR_COMPONENT", "A general Blender workflow container and a live-interface source are not peer alternatives to add-on development."),
    "028": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "Two candidates decide the ETL/ELT execution boundary and the remaining pipeline source does not restore three distinct operational roles."),
    "029": ("ADVANCE_C1_SOURCE_EVIDENCE", "Cohort-scale PLINK2 analysis, PLINK2-plus-REGENIE pipeline automation, and published GWAS-catalog retrieval have distinct source-visible inputs, methods, and outputs."),
    "030": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The broad modern-C++ containers overlap the RAII-focused implementation guidance."),
}
AGENT_ADVANCES = {"005", "007", "011", "013", "016", "023", "026", "029"}


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
    checkpoint_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_002R1_CHECKPOINT.md"
    if ledger_path.exists() or checkpoint_path.exists():
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
                "review_mode": "source-only model-assisted reviewer plus principal source recheck for all final advances and overrides",
                "agent_recommendation": "ADVANCE_C1_SOURCE_EVIDENCE" if suffix in AGENT_ADVANCES else outcome,
                "final_c0_outcome": outcome,
                "principal_override": suffix == "016",
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
        "# RQ1b V3 C0 Source-Only Review Wave 002r1\n\n"
        "Status: `COMPLETE / FEASIBILITY CALIBRATION ONLY / NO GOLD OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Roster: `c0_review_roster.jsonl` (30 triads, 90 unique canonical sources).\n"
        "- Mechanical source-binding audit: `C0_SOURCE_REVIEW_WAVE_AUDIT.json` (`PASS`; no source reuse or hash drift).\n"
        "- Review constraint: reviewers read only assigned original source artifacts; no prompts, labels, representations, selector outputs, or online sources.\n"
        "- The non-contained-title setting was used only to prioritise source review; it is not a scientific inclusion/exclusion criterion or a field result.\n\n"
        "## Final C0 Disposition\n\n"
        "| Outcome | Triads |\n|---|---:|\n"
        f"| Advance to C1 source evidence | {counts['ADVANCE_C1_SOURCE_EVIDENCE']} |\n"
        f"| Reject: nonparallel/component/container | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: copy/derivative | {counts['REJECT_COPY_OR_DERIVATIVE']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n"
        f"| Reject: no common envelope | {counts['REJECT_NO_COMMON_ENVELOPE']} |\n\n"
        f"C1 triage advances: {', '.join(f'`{item}`' for item in c1_ids)}. They remain source-evidence candidates, not strict clusters.\n\n"
        "## Interpretation And Claim Boundary\n\n"
        "Wave 002r1 verifies that a broad, cross-origin lexical queue contains some source-visible multi-skill operational contrasts, but it does not establish their prevalence or a benchmark yield. In particular, surviving source roles can still be cue-heavy, overlapping, or fail later singleton selection review. The ledger therefore records source-only feasibility dispositions and no routing result.\n\n"
        "The final ledger is `c0_review_final_ledger.jsonl`. A C1 source-evidence card, later cue control, and two independent strict selection-only reviews remain required before any candidate could become a strict public cluster.\n"
    )
    result = {
        "status": "PASS",
        "records": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "ledger_sha256": sha256_file(ledger_path),
        "roster_sha256": sha256_file(roster_path),
        "manifest_sha256": sha256_file(manifest_path),
        "audit_sha256": sha256_file(audit_path),
        "network_calls": 0,
        "texts_transmitted": 0,
    }
    (args.wave_dir / "C0_SOURCE_REVIEW_WAVE_002R1_FINALISER_AUDIT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
