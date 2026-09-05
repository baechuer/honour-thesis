#!/usr/bin/env python3
"""Freeze the source-only D1 Wave 001 C1 dispositions with literal evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-d1-c1-wave001-finaliser-v1"
BOUNDARY = (
    "C1 is source-only operational-evidence review. An advance permits later C2 "
    "prompt construction only; it is not a prompt, gold-label, selector, field-effect, "
    "or routing result."
)

# These strings are checked against the source bytes below. They preserve the
# operational basis for each decision without introducing a prompt or winner.
DECISIONS = {
    "RQ1B-V3-D1-C1-W1-001": {
        "outcome": "ADVANCE_C2_PROMPT_CONSTRUCTION",
        "reason": (
            "The members are natural peer routes for native-document-to-Markdown "
            "conversion: their input formats are mutually exclusive and each names a "
            "format-specific conversion operation and Markdown output."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-019877",
                "trigger": "Trigger this skill any time there is a `.pdf` file that needs to be",
                "operation": "always convert\nit to Markdown first using the script in this skill",
                "output": "writes a self-contained folder\nper document:",
                "constraint": "This skill only supports `.pdf`",
            },
            {
                "source_id": "RQ1B-V3-SRC-025411",
                "trigger": "Trigger this skill any time there is a `.docx` file that needs to be",
                "operation": "always convert it to Markdown first using the script in this\nskill",
                "output": "writes a self-contained\nfolder per document instead of a single loose `.md` file",
                "constraint": "This skill only supports `.docx`",
            },
            {
                "source_id": "RQ1B-V3-SRC-027887",
                "trigger": "Trigger this skill any time there is a `.xlsx` file that needs to be",
                "operation": "always convert it to Markdown first\nusing the script in this skill",
                "output": "maps them to the sheet they belong to, writing a\nself-contained folder per document:",
                "constraint": "This skill only supports `.xlsx`",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W1-002": {
        "outcome": "REJECT_NONPARALLEL_OR_COMPONENT",
        "reason": (
            "The source-visible states are a serial v4-to-v5-to-v6-to-v7 lifecycle. "
            "Each later guide consumes the preceding guide's target version, so they are "
            "not three alternative peer routes."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-019909",
                "trigger": "datadoghq-browser-agent.com CDN with /v4/ paths.",
                "operation": "Systematic migration guide from v4 to v5. Follow steps 1-7 in order.",
                "output": "datadoghq-browser-agent.com/us1/v5/datadog-rum.js",
                "constraint": "upgrade to v6 first if you need AP2",
            },
            {
                "source_id": "RQ1B-V3-SRC-013835",
                "trigger": "datadoghq-browser-agent.com CDN with /v5/ paths.",
                "operation": "Systematic migration guide from v5 to v6. Follow steps 1-6 in order.",
                "output": "datadoghq-browser-agent.com/us1/v6/datadog-rum.js",
                "constraint": "Keep using v5 if IE11 support is required.",
            },
            {
                "source_id": "RQ1B-V3-SRC-016429",
                "trigger": "datadoghq-browser-agent.com CDN with /v6/ paths.",
                "operation": "Systematic migration guide from v6 to v7. Follow steps 1-6 in order.",
                "output": "datadoghq-browser-agent.com/us1/v7/datadog-rum.js",
                "constraint": "crossorigin=\"anonymous\"",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W1-003": {
        "outcome": "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
        "reason": (
            "All three artifacts perform complete Sentry SDK setup by inspecting a project, "
            "installing the language SDK, configuring it, and verifying features. The source "
            "difference is the runtime/interface rather than a sufficiently distinct route."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-000998",
                "trigger": "Full Sentry SDK setup for Go.",
                "operation": "Opinionated wizard that scans your Go project and guides you through complete Sentry setup.",
                "output": "sentry-go",
                "constraint": "Supports net/http, Gin, Echo, Fiber, FastHTTP, Iris, and Negroni.",
            },
            {
                "source_id": "RQ1B-V3-SRC-006135",
                "trigger": "Full Sentry SDK setup for Python.",
                "operation": "Opinionated wizard that scans your Python project and guides you through complete Sentry setup.",
                "output": "sentry-sdk",
                "constraint": "Supports Django, Flask, FastAPI, Celery, Starlette, AIOHTTP, Tornado, and more.",
            },
            {
                "source_id": "RQ1B-V3-SRC-027082",
                "trigger": "Full Sentry SDK setup for Ruby.",
                "operation": "Opinionated wizard that scans the project and guides through complete Sentry setup.",
                "output": "sentry-ruby",
                "constraint": "Supports Rails, Sinatra, Rack, Sidekiq, and Resque.",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W1-004": {
        "outcome": "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
        "reason": (
            "The artifacts share the same core documentation-site chain: scaffold, configure, "
            "write Markdown documentation, build, and deploy. The generator ecosystem alone "
            "does not create a source-grounded operational contrast."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-021008",
                "trigger": "Build documentation websites with Docusaurus.",
                "operation": "Create new Docusaurus project",
                "output": "Build for production",
                "constraint": "Node.js 18+ (any hosting platform)",
            },
            {
                "source_id": "RQ1B-V3-SRC-022046",
                "trigger": "Build documentation sites with MkDocs and Material for MkDocs.",
                "operation": "mkdocs new my-docs && cd my-docs",
                "output": "mkdocs build                           # Generate static site",
                "constraint": "No special requirements",
            },
            {
                "source_id": "RQ1B-V3-SRC-026381",
                "trigger": "Build documentation sites with VitePress",
                "operation": "npx vitepress init",
                "output": "npx vitepress build docs",
                "constraint": "No special requirements",
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
    checkpoint_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_001_CHECKPOINT.md"
    audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_001_FINALISER_AUDIT.json"
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
        if set(members) != {entry["source_id"] for entry in decision["evidence"]}:
            raise ValueError(f"evidence membership mismatch: {row['c1_review_id']}")
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
        "# RQ1b V3 D1 C1 Source-Evidence Wave 001\n\n"
        "Status: `COMPLETE / SOURCE-ONLY GATE / NO PROMPT, GOLD, OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Four D1 source-only triad packets, comprising 12 unique canonical artifacts.\n"
        "- `C1_SOURCE_EVIDENCE_WAVE_AUDIT.json` passed: no hash drift and no source reuse.\n"
        "- Reviewers read only assigned originals; no prompt, label, representation, selector, score, or online source was available.\n\n"
        "## Final C1 Disposition\n\n"
        "| C1 outcome | Triads |\n|---|---:|\n"
        f"| Advance to C2 prompt construction | {counts['ADVANCE_C2_PROMPT_CONSTRUCTION']} |\n"
        f"| Reject: nonparallel/lifecycle/component | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n\n"
        "## Interpretation And Boundary\n\n"
        "The Office-format conversion triad advances because original sources establish mutually exclusive native input formats with one shared conversion goal. Datadog upgrades are a serial version chain, while the Sentry and documentation-generator triads vary runtime/framework but not the core operational route. A C1 advance is not a valid cluster or gold label: C2 direct/paraphrase construction, C3 cue control, independent C4 strict singleton reviews, and C5/C6 freeze remain mandatory.\n\n"
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
