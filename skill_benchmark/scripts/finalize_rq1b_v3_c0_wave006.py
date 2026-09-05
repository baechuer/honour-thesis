#!/usr/bin/env python3
"""Freeze the completed source-only C0 Wave 006 lexical-triage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave006-finaliser-v1"
BOUNDARY = (
    "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, "
    "field annotation, selector input, metric, semantic-fidelity claim, or strict routing result."
)
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "RAG ingestion is a component beside broad RAG infrastructure and end-to-end pipeline construction."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "Creative-direction planning, video orchestration, and a broad creator workflow occupy different lifecycle roles."),
    "003": ("REJECT_NO_COMMON_ENVELOPE", "Todoist API integration, task management, and Todoist UI design share a product name but not one peer operation."),
    "004": ("REJECT_NO_COMMON_ENVELOPE", "Photo captioning, TikTok carousel creation, and photo-metadata work do not form one competing task envelope."),
    "005": ("REJECT_NONPARALLEL_OR_COMPONENT", "PostgreSQL backup, Azure deployment, and a command-line wrapper are specialised or interface components rather than peer routes."),
    "006": ("REJECT_NONPARALLEL_OR_COMPONENT", "OpenTelemetry collector setup, broad stack deployment, and Sentry export are layered implementation roles, not competing first routes."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "Sampling capability, .NET MCP construction, and a broad MCP entrypoint are component and container roles."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "PowerPoint styling, broad presentation generation, and extension work are style, container, and interface roles."),
    "009": ("REJECT_NO_COMMON_ENVELOPE", "CUDA kernel work, an index problem, and CUDA-Q share terminology but not a bounded operational envelope."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "NestJS architecture guidance, scaffolding, and audit work are container, construction, and review stages."),
    "011": ("REJECT_NONPARALLEL_OR_COMPONENT", "Generic incident response contains forensic checklists and osquery as diagnostic components."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "The broad churn workflow contains the more specialised retention strategies rather than competing with them."),
    "013": ("REJECT_NO_COMMON_ENVELOPE", "Tax preparation and daily-calendar preparation share no bounded peer task envelope."),
    "014": ("REJECT_NONPARALLEL_OR_COMPONENT", "Agent-security scanning contains supply-chain detection as one diagnostic component."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "EKS maintenance/security and end-to-end deployment orchestration are nonparallel operational scopes."),
    "016": ("REJECT_NONPARALLEL_OR_COMPONENT", "A mentoring programme is an HR lifecycle container rather than a peer route."),
    "017": ("REJECT_NONPARALLEL_OR_COMPONENT", "Kubernetes networking sources cover different stack layers and components rather than alternatives."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "Account-based-marketing operations is a broad container around narrower execution routes."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Paid-media operations is a broad container rather than a peer to specialised operational steps."),
    "020": ("REJECT_NO_COMMON_ENVELOPE", "The shared word Cosmos does not establish a common operational envelope."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "Generic Maven guidance contains or overlaps the specialist implementation route."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "Bedrock troubleshooting is a host-local subcase beside broad Bedrock containers that overlap its scope."),
    "023": ("REJECT_NONPARALLEL_OR_COMPONENT", "Board-deck production is an artifact component within broader board communication and management workflows."),
    "024": ("REJECT_NONPARALLEL_OR_COMPONENT", "Meta Ads planning contains diagnostics for existing accounts, while guardrails is a cross-cutting internal constraint."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "EC2 configuration, broad deployment, and app-specific deployment are component and container roles."),
    "026": ("REJECT_NONPARALLEL_OR_COMPONENT", "Receipt extraction, broad audit, and generic report generation are nonparallel operational scopes."),
    "027": ("REJECT_NONPARALLEL_OR_COMPONENT", "React Native development is a broad container beside migration orchestration and specialised monitoring setup."),
    "028": ("REJECT_NONPARALLEL_OR_COMPONENT", "React Native development is a broad container beside web-to-native migration and Sentry SDK setup."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "Video preproduction, ASCII rendering, and audio-reactive composition are distinct lifecycle or transformation roles."),
    "030": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The Xquik sources are overlapping integration entrypoints; the Hermes variant changes host interface, not task role."),
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
    checkpoint_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_006_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_006_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C0 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    mechanical_audit = json.loads(audit_path.read_text())
    if mechanical_audit.get("status") != "PASS":
        raise ValueError("source-binding audit must pass before finalisation")
    expected = {f"{index:03d}" for index in range(1, 31)}
    if len(roster) != 30 or set(DECISIONS) != expected:
        raise ValueError("incomplete C0 Wave 006 decision binding")

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
        "# RQ1b V3 C0 Source-Only Review Wave 006\n\n"
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
        "All 30 lexical-title/local-FTS drafts were rejected before C1. The dominant pattern was a broad container combined with a lifecycle component, specialised implementation, or interface wrapper. This calibrates this particular discovery method; it is not a prevalence estimate, a public-cluster yield, a strict-gold result, or a retrieval result.\n\n"
        "The final ledger is `c0_review_final_ledger.jsonl`. Directed D1 discovery remains a separate prospective path under unchanged C1--C6 gates.\n"
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
