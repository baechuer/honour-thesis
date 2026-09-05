#!/usr/bin/env python3
"""Freeze the completed source-only C0 Wave 010 lexical-triage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave010-finaliser-v1"
BOUNDARY = (
    "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, "
    "field annotation, selector input, metric, semantic-fidelity claim, or strict routing result."
)
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "CloudWatch log querying is specialised beside broad AWS operations and universal troubleshooting containers."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "Page, signup, and onboarding optimisation are explicit lifecycle stages rather than three peer routes."),
    "003": ("REJECT_NONPARALLEL_OR_COMPONENT", "A broad cloud-security router, vendor-specific Prisma implementation, and posture hardening form container and specialised roles."),
    "004": ("REJECT_NONPARALLEL_OR_COMPONENT", "Literature search alternatives sit beside a broad systematic-review lifecycle container."),
    "005": ("REJECT_NONPARALLEL_OR_COMPONENT", "A broad partner programme, affiliate-planning component, and gym-specific referral implementation are not peer routes."),
    "006": ("REJECT_NONPARALLEL_OR_COMPONENT", "Viral content artifacts are platform/media specialisations with distinct commercial constraints, not one bounded route choice."),
    "007": ("REJECT_NONPARALLEL_OR_COMPONENT", "Interview-kit design, completed-loop debrief, and learner interview simulation are pre-, post-, and parallel-stage roles."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "Broad vendor TPRM contains a bounded security review, while vendor-check adds a distinct legal/compliance bundle."),
    "009": ("REJECT_NO_COMMON_ENVELOPE", "RCT power calculation and Power BI DAX optimisation share only lexical power terminology."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "Cloud cost anomaly investigation, general investigation, and governance occupy incident, container, and programme roles."),
    "011": ("REJECT_NO_COMMON_ENVELOPE", "Electron native-library extraction, reverse extraction, and live testing are different operational tasks."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "Technical pricing, GTM automation infrastructure, and web3 GTM strategy are component, infrastructure, and vertical-playbook roles."),
    "013": ("REJECT_NO_COMMON_ENVELOPE", "Regulatory examination work and academic study preparation share only the lexical term exam."),
    "014": ("REJECT_NONPARALLEL_OR_COMPONENT", "SageMaker deployment planning, full MLOps platform deployment, and generic model deployment are entry-point, container, and implementation roles."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "Supplementary Daytona evidence artifacts sit beside direct browser or UI recording workflows."),
    "016": ("REJECT_NONPARALLEL_OR_COMPONENT", "A tech-debt register is a component of broad tech leadership, while M&A diligence is a separate deal-assessment workflow."),
    "017": ("REJECT_NO_COMMON_ENVELOPE", "Music generation, image-loop construction, and hosted short-video production have different primary inputs and artifacts."),
    "018": ("REJECT_NONPARALLEL_OR_COMPONENT", "PlantUML ASCII is a specialised static-diagram implementation beside generic ASCII work and raster/video conversion."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "Pinterest pin design is bounded beneath Pinterest marketing strategy, while Pinterest-style UI work is a different product-interface domain."),
    "020": ("REJECT_NONPARALLEL_OR_COMPONENT", "Expense policy drafting, policy testing, and individual expense entry are policy-definition, assurance, and transaction-processing stages."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "Thread analysis sits beside a generic Reddit extraction interface and a broad multi-layer SaaS discovery workflow."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "AXI wraps Chrome DevTools and the optimizer prescribes its use; neither is a peer end-task route."),
    "023": ("REJECT_NO_COMMON_ENVELOPE", "Finance portfolio advisory, AI initiative posture advisory, and legal advisory are distinct operational domains."),
    "024": ("REJECT_NONPARALLEL_OR_COMPONENT", "General OTel instrumentation contains Go SDK work, while vendoring is a Sentry-specific code-maintenance workflow."),
    "025": ("REJECT_NO_COMMON_ENVELOPE", "Textbook chapter design, EPUB conversion, and book summarisation have distinct inputs, operations, and deliverables."),
    "026": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The three adoption artifacts share the same staged behavioural-change chain, differing mainly by target population or tool domain."),
    "027": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "Ethical influence, sales psychology, and marketing psychology overlap materially in principles and applications."),
    "028": ("REJECT_NO_COMMON_ENVELOPE", "Function-level refactoring, durable-goal governance, and C# architecture governance are different scopes."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "Developer-first community work is specialised beside broad community-growth and community-marketing containers."),
    "030": ("REJECT_NONPARALLEL_OR_COMPONENT", "FASTA curation, broad scikit-bio analysis, and Polars genomic-interval work are preparation, container, and specialised-engine roles."),
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
    checkpoint_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_010_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C0_SOURCE_REVIEW_WAVE_010_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C0 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    source_audit = json.loads(source_audit_path.read_text())
    if source_audit.get("status") != "PASS":
        raise ValueError("source-binding audit must pass before finalisation")
    expected = {f"{index:03d}" for index in range(1, 31)}
    if len(roster) != 30 or set(DECISIONS) != expected:
        raise ValueError("incomplete C0 Wave 010 decision binding")

    records = []
    for row in roster:
        suffix = row["c0_review_id"].rsplit("-", 1)[1]
        outcome, reason = DECISIONS[suffix]
        records.append({
            "c0_review_id": row["c0_review_id"],
            "lexical_draft_id": row["lexical_draft_id"],
            "member_source_ids": [member["source_id"] for member in row["members"]],
            "member_titles": [member["title"] for member in row["members"]],
            "review_mode": "source-only independent review plus principal disposition",
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
        "# RQ1b V3 C0 Source-Only Review Wave 010\n\n"
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
        "All 30 lexical drafts were rejected before C1: 21 for nonparallel/component/container structure, two for insufficient operational contrast, and seven for no common envelope. This calibrates the lexical-discovery path; it does not estimate public-cluster prevalence, strict-triad yield, field recoverability, or retrieval performance.\n"
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
