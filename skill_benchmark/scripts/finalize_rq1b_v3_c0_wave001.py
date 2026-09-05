#!/usr/bin/env python3
"""Record the completed source-only C0 Wave 001 triage decision ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c0-wave001-finaliser-v1"
DECISIONS = {
    "001": ("REJECT_NONPARALLEL_OR_COMPONENT", "The module-specific source is nested inside two broad protocol/API guides."),
    "002": ("REJECT_NONPARALLEL_OR_COMPONENT", "The Cilium platform guide is a broad container for the network and mesh work."),
    "003": ("REJECT_NONPARALLEL_OR_COMPONENT", "Principal recheck: the privacy-rights source itself covers DSAR, notices and vendor contracts, overlapping the advisory and implementation candidates."),
    "004": ("REJECT_COPY_OR_DERIVATIVE", "Two candidates repeat the same Aurora DSQL declared purpose; the psql variant does not restore triad independence."),
    "005": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "A general animation container overlaps the two GSAP/Framer animation guides."),
    "006": ("REJECT_NONPARALLEL_OR_COMPONENT", "Principal recheck: both Enrichr sources are specialised instances of the broad ORA/GSEA pathway workflow, which subsumes their operation."),
    "007": ("ADVANCE_C1_SOURCE_EVIDENCE", "Configuration authoring, configuration assessment, and authorised scan execution are separate source-visible DAST operations."),
    "008": ("REJECT_NONPARALLEL_OR_COMPONENT", "A narrow register audit is paired with two broad DORA compliance containers, one of which is an incomplete preview."),
    "009": ("REJECT_NONPARALLEL_OR_COMPONENT", "Checkout extension work is a specialised component of the two broad Shopify guides."),
    "010": ("REJECT_NONPARALLEL_OR_COMPONENT", "KEDA resource configuration is nested in broader Kubernetes autoscaling guides."),
    "011": ("REJECT_COPY_OR_DERIVATIVE", "Two MSAA DAG-authoring candidates state the same purpose; troubleshooting is a different lifecycle role."),
    "012": ("REJECT_NONPARALLEL_OR_COMPONENT", "The MSSQL bug harness is a test component, not a peer alternative to CDC pipeline design/deployment."),
    "013": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All candidates perform the same PyDESeq2 differential-expression operation with depth/interface variations."),
    "014": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All candidates route to ffuf content discovery; framing and authentication support do not create three operations."),
    "015": ("REJECT_NONPARALLEL_OR_COMPONENT", "A narrow GDScript guide and a broad Godot umbrella do not form parallel alternatives."),
    "016": ("REJECT_NONPARALLEL_OR_COMPONENT", "The workload-identity playbook and GKE-security source contain the SPIFFE/SPIRE role."),
    "017": ("ADVANCE_C1_SOURCE_EVIDENCE", "Incident diagnosis, pipeline design and schema/resilience guardrails are distinct source-visible Kafka operations."),
    "018": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All three describe end-to-end OpenTelemetry instrumentation and Collector deployment."),
    "019": ("REJECT_NONPARALLEL_OR_COMPONENT", "The lakehouse architecture guide contains the narrower governance and federation roles."),
    "020": ("REJECT_NO_COMMON_ENVELOPE", "A migration away from Next.js is not a peer task to Next.js patterns/optimisation."),
    "021": ("REJECT_NONPARALLEL_OR_COMPONENT", "PCI network segmentation is a component within two all-requirements PCI guides."),
    "022": ("REJECT_NONPARALLEL_OR_COMPONENT", "Gatekeeper policy authoring is one component of the broader OPA policy guides."),
    "023": ("REJECT_NONPARALLEL_OR_COMPONENT", "The mathematical SLI/SLO explanation is nested in design and implementation workflows."),
    "024": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "All candidates share the same PostGIS querying/design core, differing mainly in depth and scope."),
    "025": ("REJECT_NONPARALLEL_OR_COMPONENT", "Blue-green deployment is a component within broad progressive-release strategy guides."),
    "026": ("REJECT_NONPARALLEL_OR_COMPONENT", "The social-content setup source is a workflow component and the provider/API sources overlap."),
    "027": ("REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST", "The triad mixes the same Manim task with an implementation-specific CLI/Web wrapper."),
    "028": ("ADVANCE_C1_SOURCE_EVIDENCE", "Connected-workspace AR aging, GL tie-out/re-age, and supplied-invoice aging have distinct source-visible inputs and outputs."),
    "029": ("REJECT_NONPARALLEL_OR_COMPONENT", "The triad mixes a provider umbrella, API integration guide and downstream brand-content workflow."),
    "030": ("REJECT_NONPARALLEL_OR_COMPONENT", "The HIPAA umbrella overlaps the vendor-BAA assessment and privacy-engineering candidates."),
}
AGENT_ADVANCES = {"003", "006", "007", "017", "028"}


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
    checkpoint_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_001_CHECKPOINT.md"
    if ledger_path.exists() or checkpoint_path.exists():
        raise ValueError("refusing to overwrite final C0 decisions")
    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    records = []
    for row in roster:
        suffix = row["c0_review_id"].rsplit("-", 1)[1]
        if suffix not in DECISIONS:
            raise ValueError(f"missing final decision for {row['c0_review_id']}")
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
                "principal_override": suffix in {"003", "006"},
                "reason": reason,
                "claim_boundary": "C0 is lexical-draft feasibility triage only. It creates no prompt, gold label, field annotation, selector input, metric, semantic-fidelity claim, or strict routing result.",
            }
        )
    if len(records) != 30 or set(DECISIONS) != {record["c0_review_id"].rsplit("-", 1)[1] for record in records}:
        raise ValueError("incomplete C0 roster binding")
    counts = Counter(record["final_c0_outcome"] for record in records)
    ledger_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    checkpoint = f"""# RQ1b V3 C0 Source-Only Review Wave 001\n\nStatus: `COMPLETE / FEASIBILITY CALIBRATION ONLY / NO GOLD OR SELECTOR RESULT`\n\n## Inputs And Mechanical Audit\n\n- Roster: `c0_review_roster.jsonl` (30 triads, 90 unique canonical sources).\n- Mechanical source-binding audit: `C0_SOURCE_REVIEW_WAVE_AUDIT.json` (`PASS`; no source reuse or hash drift).\n- Review constraint: reviewers read only assigned original source artifacts; no prompts, labels, representations, selector outputs or online sources.\n\n## Final C0 Disposition\n\n| Outcome | Triads |\n|---|---:|\n| Advance to C1 source evidence | {counts['ADVANCE_C1_SOURCE_EVIDENCE']} |\n| Reject: nonparallel/component/container | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n| Reject: copy/derivative | {counts['REJECT_COPY_OR_DERIVATIVE']} |\n| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n| Reject: no common envelope | {counts['REJECT_NO_COMMON_ENVELOPE']} |\n\nC1 candidates: `RQ1B-V3-C0-W1-007` (DAST configuration authoring, configuration assessment, authorised scan execution), `RQ1B-V3-C0-W1-017` (Kafka incident diagnosis, pipeline design, resilience/schema guardrails), and `RQ1B-V3-C0-W1-028` (connected-workspace AR aging, AR-to-GL tie-out, supplied-invoice aging). They remain triage advances, not strict clusters.\n\nTwo reviewer-suggested advances (`003` CCPA and `006` pathway enrichment) were conservatively rejected after principal source recheck because a broad candidate visibly subsumed the allegedly distinct roles. This calibration therefore supports a stronger next lexical prefilter against bare-topic or title-containment containers; it does not estimate the prevalence or feasibility rate of strict public triads.\n\n## Claim Boundary\n\nThe final ledger is `c0_review_final_ledger.jsonl`. It records source-only feasibility decisions. It does **not** create a prompt, choose a gold label, test field availability, run a selector, establish semantic fidelity or support a thesis result. A C1 source-evidence card, then later cue control and two independent strict selection-only reviews, remain required.\n"""
    checkpoint_path.write_text(checkpoint)
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
    (args.wave_dir / "C0_SOURCE_REVIEW_WAVE_001_FINALISER_AUDIT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
