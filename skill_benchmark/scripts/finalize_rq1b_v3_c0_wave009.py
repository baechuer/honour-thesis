#!/usr/bin/env python3
"""Freeze the completed source-only C0 Wave 009 lexical-triage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave009-finaliser-v1"
BOUNDARY = (
    "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, "
    "field annotation, selector input, metric, semantic-fidelity claim, or strict routing result."
)
DECISIONS = {
    "001": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The resume-tailoring artifacts overlap on the same input-output chain; their distinctions are packaging rather than peer routes."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "Zotero setup, a wrapper/interface, and a citation-management workflow occupy component or container roles."),
    "003": ("REJECT_NONPARALLEL_OR_COMPONENT", "Foundry validation, broad deployment guidance, and specialised frontend implementation are lifecycle or container roles rather than peers."),
    "004": ("REJECT_NONPARALLEL_OR_COMPONENT", "Fine-tuning method choice, data preparation, and deployment guidance are upstream, component, and container roles."),
    "005": ("REJECT_NONPARALLEL_OR_COMPONENT", "Tracking audit, provider configuration, and broad setup guidance are component/container alternatives."),
    "006": ("REJECT_NONPARALLEL_OR_COMPONENT", "Feature-flag cleanup is a lifecycle operation within broad feature-flag configuration and management containers."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "The two Cognito authentication artifacts materially overlap, while TypeScript OTP implementation is a specialised custom-auth route rather than a peer alternative."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "Python/PHP Sentry SDK setup and downstream Sentry integration or investigation are implementation and lifecycle roles, not peer routes."),
    "009": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The AWS cost-optimisation artifacts overlap materially beside a broad cost-management container."),
    "010": ("REJECT_NO_COMMON_ENVELOPE", "Entra app registration, agent-user provisioning, and M365 incident investigation share platform terminology but not a bounded peer operation."),
    "011": ("REJECT_NONPARALLEL_OR_COMPONENT", "Google Ads creation and budget operations are components within a broad advertising-management container."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "Runbook authoring and runbook execution are lifecycle stages beside a broad runbook container."),
    "013": ("REJECT_NONPARALLEL_OR_COMPONENT", "ZeroGPU setup, model selection, and broad infrastructure guidance are component/container roles."),
    "014": ("REJECT_NONPARALLEL_OR_COMPONENT", "Lease extraction is a specialised step within document review rather than a peer route."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "UGC briefing is upstream of a specialised advertising implementation, not a competing peer route."),
    "016": ("REJECT_NO_COMMON_ENVELOPE", "Video light design, a narrow HTML spotlight animation, and broad UI light-mode design are cross-medium, nonparallel tasks."),
    "017": ("REJECT_NONPARALLEL_OR_COMPONENT", "Telemetry instrumentation supplies data consumed by telemetry analysis, while product-event registry work is a specialised implementation."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "Search-led social campaign construction and a social-ad implementation sit beside a broad campaign-management container."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Page, signup, and post-signup conversion work are explicit lifecycle stages, not peer routes."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "Fine-tuning method selection is an explicit router and LoRA execution is a specialised implementation beside a broad container."),
    "021": ("REJECT_NO_COMMON_ENVELOPE", "Theory distillation, generic paper writing, and economics-paper writing do not form one bounded peer task."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "PowerShell/Windows defensive operations sit inside a broad Blue Team container."),
    "023": ("REJECT_NONPARALLEL_OR_COMPONENT", "Google Veo generation is downstream of prompt-production artifacts rather than a peer route."),
    "024": ("REJECT_NO_COMMON_ENVELOPE", "KeyVault administration, compliance audit, and incident response share cloud-security vocabulary but not one operation."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "Lollms agentic-swarm implementation and dashboard management are component/container roles."),
    "026": ("REJECT_NO_COMMON_ENVELOPE", "Sales de-escalation, support sentiment checking, and reputation monitoring are different operational envelopes."),
    "027": ("REJECT_NONPARALLEL_OR_COMPONENT", "A UK-specific legal-citation implementation is specialised beside a broad legal-citation container and policy guidance."),
    "028": ("REJECT_NONPARALLEL_OR_COMPONENT", "ADK coding, onboarding, and broad toolkit guidance are lifecycle/container roles."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "A Solana scanner is a specialised implementation within broad blockchain-development artifacts."),
    "030": ("REJECT_NO_COMMON_ENVELOPE", "The Alibaba/image/cloud/store lexical overlap is polysemous and does not establish a common route envelope."),
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
    checkpoint_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_009_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_009_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C0 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    source_audit = json.loads(source_audit_path.read_text())
    if source_audit.get("status") != "PASS":
        raise ValueError("source-binding audit must pass before finalisation")
    expected = {f"{index:03d}" for index in range(1, 31)}
    if len(roster) != 30 or set(DECISIONS) != expected:
        raise ValueError("incomplete C0 Wave 009 decision binding")

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
        "# RQ1b V3 C0 Source-Only Review Wave 009\n\n"
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
        "All 30 lexical drafts were rejected before C1: 22 for nonparallel/component/container structure, two for insufficient operational contrast, and six for no common envelope. The principal recheck rejected the apparent AWS Cognito/OTP candidate because the broad Cognito/auth artifacts materially overlap while the OTP artifact is a specialised implementation. This calibrates the lexical-discovery path; it does not estimate public-cluster prevalence, strict-triad yield, field recoverability, or retrieval performance.\n"
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
