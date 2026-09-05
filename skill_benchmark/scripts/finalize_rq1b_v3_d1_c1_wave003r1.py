#!/usr/bin/env python3
"""Freeze source-only D1 Wave 003r1 C1 dispositions with literal evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-d1-c1-wave003r1-finaliser-v1"
BOUNDARY = (
    "C1 is source-only operational-evidence review. A rejection records a peer-route "
    "failure only; it is not a prompt, gold-label, selector, field-effect, or routing result."
)
DECISIONS = {
    "RQ1B-V3-D1-C1-W3R1-001": {
        "outcome": "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
        "reason": (
            "The Scala, Java, and PySpark coordinators each start from a different language "
            "dialect but retain the same multi-phase SCOS migration chain, coordinator role, "
            "and converted-file/report output family. The dialect substitution alone is not "
            "sufficient operational contrast for a C1 peer-route composition."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-010462",
                "trigger": "Path to the Spark Scala file or directory to migrate",
                "operation": "Orchestrate a multi-phase migration",
                "output": "Issues.csv",
                "constraint": "Install `uv` if it is not already available.",
            },
            {
                "source_id": "RQ1B-V3-SRC-011921",
                "trigger": "Path to the Spark Java file or directory to migrate",
                "operation": "Orchestrate a multi-phase migration",
                "output": "Issues.csv",
                "constraint": "Install `uv` if it is not already available.",
            },
            {
                "source_id": "RQ1B-V3-SRC-019949",
                "trigger": "Path to the PySpark file or directory to migrate",
                "operation": "Orchestrate a multi-phase migration",
                "output": "Issues.csv",
                "constraint": "Install `uv` if it is not already available.",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W3R1-002": {
        "outcome": "REJECT_NONPARALLEL_OR_COMPONENT",
        "reason": (
            "PDF-to-images and PDF-to-layout-preserving-text are bounded PDF-specific routes. "
            "The ADP source is a broad 10-plus-format document-processing container with PDF "
            "as one capability, which creates generic-specialist asymmetry rather than three "
            "parallel first routes."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-001605",
                "trigger": "Path to the PDF file",
                "operation": "Use ImageMagick to convert each page to image",
                "output": "individual PNG images, one per page",
                "constraint": "Requires ImageMagick installed on the system",
            },
            {
                "source_id": "RQ1B-V3-SRC-003645",
                "trigger": "$SKILL_DIR/bin/pdf-to-text INPUT.pdf OUTPUT.txt",
                "operation": "Run the converter",
                "output": "layout-preserving plain text",
                "constraint": "This skill does not OCR",
            },
            {
                "source_id": "RQ1B-V3-SRC-027118",
                "trigger": "Run `adp parse local <file_path> --app-id <document_parsing_app_id>`",
                "operation": "a single command completes intelligent document understanding and structured output",
                "output": "Markdown-formatted text",
                "constraint": "Maximum 50MB per file.",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W3R1-003": {
        "outcome": "REJECT_NONPARALLEL_OR_COMPONENT",
        "reason": (
            "The CCPA/CPRA and LGPD sources are broad jurisdictional privacy-compliance "
            "programmes spanning data mapping, governance and rights management. The GDPR "
            "source is a bounded inbound data-subject-request workflow nested in that larger "
            "domain. This is generic-programme versus specialist-workflow asymmetry, not three "
            "parallel peer routes."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-010664",
                "trigger": "Processing California residents' PI",
                "operation": "Map **data flows** for California consumers",
                "output": "cpra-data-map-{id}.json",
                "constraint": "SOC 2 TSC-only audits without California PI",
            },
            {
                "source_id": "RQ1B-V3-SRC-021453",
                "trigger": "processing of personal data carried out in Brazil",
                "operation": "Map all processing activities involving Brazilian personal data",
                "output": "Create RIPD template aligned with Art. 38 requirements",
                "constraint": "RIPD is strongly recommended for",
            },
            {
                "source_id": "RQ1B-V3-SRC-024738",
                "trigger": "a subject access request, erasure request, objection, or portability request arrives",
                "operation": "The workflow classifies the request, tracks the deadline",
                "output": "register entry recording receipt date, request type, deadline, and outcome",
                "constraint": "A human verifies identity, decides whether to fulfil or refuse",
            },
        ],
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
    binding_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json"
    ledger_path = wave_dir / "c1_review_final_ledger.jsonl"
    checkpoint_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_003R1_CHECKPOINT.md"
    audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_003R1_FINALISER_AUDIT.json"
    if any(path.exists() for path in (ledger_path, checkpoint_path, audit_path)):
        raise ValueError("refusing to overwrite final C1 decisions")

    roster = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    binding = json.loads(binding_path.read_text())
    if binding.get("status") != "PASS":
        raise ValueError("source-binding audit must pass before finalisation")
    if {row["c1_review_id"] for row in roster} != set(DECISIONS):
        raise ValueError("decision mapping does not exactly cover the frozen C1 roster")

    records = []
    for row in roster:
        decision = DECISIONS[row["c1_review_id"]]
        members = {member["source_id"]: member for member in row["members"]}
        for entry in decision["evidence"]:
            source_text = Path(members[entry["source_id"]]["absolute_path"]).read_text()
            for key in ("trigger", "operation", "output", "constraint"):
                if entry[key] not in source_text:
                    raise ValueError(
                        f"literal evidence span missing: {row['c1_review_id']} {entry['source_id']} {key}"
                    )
        records.append(
            {
                "c1_review_id": row["c1_review_id"],
                "parent_d1_draft_id": row["parent_d1_draft_id"],
                "discovery_lane": row["discovery_lane"],
                "member_source_ids": [member["source_id"] for member in row["members"]],
                "member_titles": [member["title"] for member in row["members"]],
                "candidate_count": row["candidate_count"],
                "review_mode": "source-only independent review plus principal source recheck",
                "source_binding_verified": True,
                "final_c1_outcome": decision["outcome"],
                "reason": decision["reason"],
                "source_evidence": decision["evidence"],
                "claim_boundary": BOUNDARY,
            }
        )
    counts = Counter(record["final_c1_outcome"] for record in records)
    ledger_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    checkpoint_path.write_text(
        "# RQ1b V3 D1 C1 Source-Evidence Wave 003r1\n\n"
        "Status: `COMPLETE / SOURCE-ONLY GATE / ZERO C2 ADVANCES / NO PROMPT, GOLD, OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Three D1 source-only triad packets, comprising nine unique canonical artifacts.\n"
        "- The initial W3 literal-span failure is retained. W3r1 changes only the nonliteral LGPD constraint span.\n"
        "- `C1_SOURCE_EVIDENCE_WAVE_AUDIT.json` passed: no hash drift and no source reuse.\n"
        "- Reviewers read only assigned originals; no prompt, label, representation, selector, score, or online source was available.\n\n"
        "## Final C1 Disposition\n\n"
        "| C1 outcome | Triads |\n|---|---:|\n"
        f"| Advance to C2 prompt construction | {counts['ADVANCE_C2_PROMPT_CONSTRUCTION']} |\n"
        f"| Reject: nonparallel/lifecycle/component | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n\n"
        "## Interpretation And Boundary\n\n"
        "A source-language substitution, a generic document-processing container, or a broad jurisdictional compliance programme is insufficient for a strict parallel peer-route unit. These are C1 source-only discovery findings. They do not show that source-language, output-artifact, jurisdiction, provider, dependency, or boundary information has no routing value in general.\n\n"
        "The final source-evidence ledger is `c1_review_final_ledger.jsonl`; all quoted spans are mechanically checked as exact source substrings.\n"
    )
    result = {
        "status": "PASS",
        "version": VERSION,
        "records": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "advance_c2_count": counts["ADVANCE_C2_PROMPT_CONSTRUCTION"],
        "ledger_sha256": sha256_file(ledger_path),
        "roster_sha256": sha256_file(roster_path),
        "manifest_sha256": sha256_file(manifest_path),
        "source_binding_audit_sha256": sha256_file(binding_path),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    audit_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
