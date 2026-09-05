#!/usr/bin/env python3
"""Freeze the prompt-free C1 dispositions for lexical C0 Wave 007 advances."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-c1-wave002-finaliser-v1"
BOUNDARY = (
    "C1 is source-only evidence review. This decision creates no prompt, intended winner, "
    "gold label, acceptable set, field card, representation, selector input, metric, or retrieval result."
)
DECISIONS = {
    "001": {
        "outcome": "REJECT_NO_COMMON_ENVELOPE",
        "reason": "Traffic decay and content decay diagnose organic-page performance, whereas ad-creative fatigue manages paid-ad rotation. Their shared decline/refresh wording is broad marketing-performance containment, not one competing operational envelope.",
        "source_evidence_summary": {
            "RQ1B-V3-SRC-002531": "Requires current/prior GSC data; compares each page across periods and reports declining pages, loss-driving queries and refresh candidates.",
            "RQ1B-V3-SRC-004900": "Requires a public indexed site or content list; checks freshness/ranking signals and returns a prioritised content-refresh queue.",
            "RQ1B-V3-SRC-010695": "Requires active-creative performance metrics; calculates creative-fatigue signals and recommends ad rotation or replacement.",
        },
    },
    "002": {
        "outcome": "REJECT_NONPARALLEL_OR_COMPONENT",
        "reason": "The source artifacts explicitly form an upstream enrichment, intelligence-product production and downstream SIEM hunt chain. The producer-versus-consumer distinction makes them lifecycle-related rather than competing first routes.",
        "source_evidence_summary": {
            "RQ1B-V3-SRC-020745": "Investigates CVEs, IOCs, malware names or threat actors with search/extract to produce a threat-intelligence brief; requires TAVILY_API_KEY.",
            "RQ1B-V3-SRC-015090": "Packages investigation observations, IOCs and TTPs into a finished intelligence product; explicitly says it produces products and a hunt consumes intelligence.",
            "RQ1B-V3-SRC-009870": "Uses a threat actor identifier and time window for SIEM/GTI hunting, then documents and reports internal findings using GTI, SIEM and SOAR dependencies.",
        },
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
    checkpoint_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md"
    finaliser_audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_002_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, finaliser_audit_path)):
        raise ValueError("refusing to overwrite final C1 decisions")
    audit = json.loads(audit_path.read_text())
    if audit.get("status") != "PASS":
        raise ValueError("C1 source-binding audit must pass before finalisation")
    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    expected = {f"{index:03d}" for index in range(1, 3)}
    if len(roster) != 2 or set(DECISIONS) != expected:
        raise ValueError("incomplete C1 Wave 002 decision binding")
    records = []
    for row in roster:
        suffix = row["c1_review_id"].rsplit("-", 1)[1]
        decision = DECISIONS[suffix]
        source_ids = [member["source_id"] for member in row["members"]]
        if set(source_ids) != set(decision["source_evidence_summary"]):
            raise ValueError(f"source evidence does not bind roster: {row['c1_review_id']}")
        records.append({
            "c1_review_id": row["c1_review_id"],
            "parent_c0_review_id": row["parent_c0_review_id"],
            "lexical_draft_id": row["lexical_draft_id"],
            "member_source_ids": source_ids,
            "member_titles": [member["title"] for member in row["members"]],
            "review_mode": "independent source-only review plus principal source recheck",
            "final_c1_outcome": decision["outcome"],
            "reason": decision["reason"],
            "source_evidence_summary": decision["source_evidence_summary"],
            "claim_boundary": BOUNDARY,
        })
    counts = Counter(record["final_c1_outcome"] for record in records)
    ledger_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    checkpoint_path.write_text(
        "# RQ1b V3 C1 Source-Evidence Wave 002\n\n"
        "Status: `COMPLETE / SOURCE-ONLY REJECTS / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT`\n\n"
        "Two Wave 007 lexical C0 permissions were source-bound and independently reviewed without prompts, labels, representations, selector outputs, metrics or network access. Both reject before C2: performance-decay artifacts share only a broad marketing-performance frame, and threat-intelligence artifacts form an explicit producer-consumer lifecycle.\n\n"
        "| Outcome | Triads |\n|---|---:|\n"
        f"| Reject: no common envelope | {counts['REJECT_NO_COMMON_ENVELOPE']} |\n"
        f"| Reject: nonparallel/component/lifecycle | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n\n"
        "The final ledger records one source-grounded summary per original and preserves the C0 lineage. No prompt, strict-gold label, acceptable set, field card, representation, selector input, metric or retrieval result exists.\n"
    )
    result = {
        "status": "PASS",
        "version": VERSION,
        "records": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "c2_permission_count": counts["ADVANCE_C2_PROMPT_CONSTRUCTION"],
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
