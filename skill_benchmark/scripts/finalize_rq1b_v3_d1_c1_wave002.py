#!/usr/bin/env python3
"""Freeze the source-only D1 Wave 002 C1 dispositions with literal evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-d1-c1-wave002-finaliser-v1"
BOUNDARY = (
    "C1 is source-only operational-evidence review. A rejection records a peer-role "
    "failure only; it is not a prompt, gold-label, selector, field-effect, or routing result."
)
DECISIONS = {
    "RQ1B-V3-D1-C1-W2-001": {
        "outcome": "REJECT_NONPARALLEL_OR_COMPONENT",
        "reason": (
            "Vercel and Netlify expose direct deploy-to-URL routes. Render instead combines "
            "Blueprint and MCP service/resource creation with later deployment checking, so "
            "the three sources are not peer first routes."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-028026",
                "trigger": "Deploy applications and websites to Vercel.",
                "operation": "vercel deploy [path] -y",
                "output": "Show the user the deployment URL.",
                "constraint": "Always deploy as preview",
            },
            {
                "source_id": "RQ1B-V3-SRC-022197",
                "trigger": "Deploy applications to Render",
                "operation": "Create the service (web or static) and any required databases or key-value stores.",
                "output": "Check deploy status, logs, and metrics.",
                "constraint": "Repository must be pushed to a Git provider.",
            },
            {
                "source_id": "RQ1B-V3-SRC-021434",
                "trigger": "Deploy web projects to Netlify using the Netlify CLI",
                "operation": "npx netlify deploy",
                "output": "Returns deployment URL",
                "constraint": "Valid web project in current directory",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W2-002": {
        "outcome": "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
        "reason": (
            "All three artifacts accept text or messages, call a hosted-provider generation "
            "API, and return generated text. Their source-visible differences are provider and "
            "client-interface substitutions, not distinct operational routes; the Claude source "
            "also embeds language-specific material."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-016869",
                "trigger": "generate text with OpenAI",
                "operation": "openai.chat.completions.create",
                "output": "response.choices[0].message.content",
                "constraint": "Node.js 18+, Python 3.8+",
            },
            {
                "source_id": "RQ1B-V3-SRC-001543",
                "trigger": "Classification, summarization, extraction, Q&A",
                "operation": "Claude API",
                "output": "One request, one response",
                "constraint": "Do not edit a non-Anthropic file with Anthropic SDK calls.",
            },
            {
                "source_id": "RQ1B-V3-SRC-014823",
                "trigger": "contents=\"Explain quantum computing\"",
                "operation": "client.models.generate_content(",
                "output": "print(response.text)",
                "constraint": "Legacy SDKs `google-generativeai` (Python) and `@google/generative-ai` (JS) are **deprecated**. Never use them.",
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
    checkpoint_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md"
    audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_002_FINALISER_AUDIT.json"
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
        "# RQ1b V3 D1 C1 Source-Evidence Wave 002\n\n"
        "Status: `COMPLETE / SOURCE-ONLY GATE / ZERO C2 ADVANCES / NO PROMPT, GOLD, OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Two cross-origin D1 source-only triad packets, comprising six unique canonical artifacts.\n"
        "- `C1_SOURCE_EVIDENCE_WAVE_AUDIT.json` passed: no hash drift and no source reuse.\n"
        "- Reviewers read only assigned originals; no prompt, label, representation, selector, score, or online source was available.\n\n"
        "## Final C1 Disposition\n\n"
        "| C1 outcome | Triads |\n|---|---:|\n"
        f"| Advance to C2 prompt construction | {counts['ADVANCE_C2_PROMPT_CONSTRUCTION']} |\n"
        f"| Reject: nonparallel/lifecycle/component | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n\n"
        "## Interpretation And Boundary\n\n"
        "A common product word or provider substitution is insufficient. The hosting packet mixed direct deploy-to-URL routes with a resource/deployment container; the hosted-LLM packet retained one input-to-generation-to-text pattern across providers. These are C1 source-only peer-role findings, not evidence that provider, dependency or interface information lacks any routing value.\n\n"
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
