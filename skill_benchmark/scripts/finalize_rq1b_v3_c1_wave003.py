#!/usr/bin/env python3
"""Freeze the prompt-free C1 disposition for the Wave 008 C0 advance."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c1-wave003-finaliser-v1"
BOUNDARY = (
    "C1 is source-only evidence review. This decision creates no prompt, intended winner, "
    "gold label, acceptable set, field card, representation, selector input, metric, or retrieval result."
)
DECISION = {
    "outcome": "REJECT_NONPARALLEL_OR_COMPONENT",
    "reason": "The Figma artifacts are a bounded component-documentation/handoff route, a multi-phase design-system container that includes component documentation, and a downstream screen-construction route that consumes a published system. They are component, parent/container and downstream roles rather than competing peer routes.",
    "source_evidence_summary": {
        "RQ1B-V3-SRC-014035": "Takes a selected Figma component or component-set node, collects data and deterministically converts it to a Markdown documentation and handoff page; requires the Figma Desktop Plugin API and Node conversion.",
        "RQ1B-V3-SRC-014549": "Takes codebase and Figma-file discovery material, then builds variables, styles, documented pages and components through a multi-phase design-system workflow; explicitly requires figma-use and user checkpoints.",
        "RQ1B-V3-SRC-007979": "Takes Figma target context plus source code or a screen description, discovers a published design system and builds a full screen from its instances; excludes reusable-component creation and requires a connected Figma MCP and system access.",
    },
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    args = parser.parse_args()
    wave_dir = args.wave_dir
    roster_path = wave_dir / "c1_review_roster.jsonl"
    manifest_path = wave_dir / "c1_review_manifest.json"
    audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json"
    ledger_path = wave_dir / "c1_review_final_ledger.jsonl"
    checkpoint_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_003_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_003_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C1 decisions")

    audit = json.loads(audit_path.read_text())
    if audit.get("status") != "PASS":
        raise ValueError("C1 source-binding audit must pass before finalisation")
    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    if len(roster) != 1 or roster[0]["c1_review_id"] != "RQ1B-V3-C1-W1-001":
        raise ValueError("unexpected C1 Wave 003 roster")
    row = roster[0]
    source_ids = [member["source_id"] for member in row["members"]]
    if set(source_ids) != set(DECISION["source_evidence_summary"]):
        raise ValueError("source evidence does not bind roster")
    record = {
        "c1_review_id": row["c1_review_id"],
        "parent_c0_review_id": row["parent_c0_review_id"],
        "lexical_draft_id": row["lexical_draft_id"],
        "member_source_ids": source_ids,
        "member_titles": [member["title"] for member in row["members"]],
        "review_mode": "independent source-only review plus principal source recheck",
        "final_c1_outcome": DECISION["outcome"],
        "reason": DECISION["reason"],
        "source_evidence_summary": DECISION["source_evidence_summary"],
        "claim_boundary": BOUNDARY,
    }
    counts = Counter([record["final_c1_outcome"]])
    ledger_path.write_text(json.dumps(record, sort_keys=True) + "\n")
    checkpoint_path.write_text(
        "# RQ1b V3 C1 Source-Evidence Wave 003\n\n"
        "Status: `COMPLETE / SOURCE-ONLY REJECT / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT`\n\n"
        "The sole Wave 008 C0 permission was source-bound and independently reviewed without prompts, labels, representations, selector outputs, metrics or network access. It rejects because component documentation, design-system construction and screen assembly are a component-parent-downstream chain rather than peer routes.\n\n"
        "| Outcome | Triads |\n|---|---:|\n"
        f"| Reject: nonparallel/component/lifecycle | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n\n"
        "The final ledger preserves one source-grounded summary per original and C0 lineage. No prompt, strict-gold label, acceptable set, field card, representation, selector input, metric or retrieval result exists.\n"
    )
    result = {
        "status": "PASS",
        "version": VERSION,
        "records": 1,
        "outcome_counts": dict(sorted(counts.items())),
        "c2_permission_count": 0,
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
