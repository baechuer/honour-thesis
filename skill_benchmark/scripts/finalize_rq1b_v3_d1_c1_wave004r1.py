#!/usr/bin/env python3
"""Freeze source-only D1 Wave 004r1 C1 dispositions with literal evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


VERSION = "rq1b-v3-d1-c1-wave004r1-finaliser-v1"
BOUNDARY = (
    "C1 is source-only operational-evidence review. An advance permits only later "
    "cue-controlled prompt construction; it is not a valid cluster, gold label, "
    "selector input, field effect, or routing result."
)
NOT_STATED = "NOT STATED"
DECISIONS = {
    "RQ1B-V3-D1-C1-W4R1-001": {
        "outcome": "ADVANCE_C2_PROMPT_CONSTRUCTION",
        "reason": (
            "All three artifacts are first-route agreement reviews under a bounded agreement "
            "envelope. They differ in agreement type and required review context: a practical "
            "NDA read-through, an outsourcing agreement requiring a represented party, and a "
            "TSA checked against the deal perimeter. C2 must still reject any prompt where more "
            "than one review route is fully adequate."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-026295",
                "trigger": "Use this skill for a practical NDA read-through.",
                "operation": "Identify mutual or one-way NDA, parties, purpose, and term.",
                "output": "NDA summary",
                "constraint": NOT_STATED,
            },
            {
                "source_id": "RQ1B-V3-SRC-003741",
                "trigger": "Review the uploaded Business Process Outsourcing (BPO), IS outsourcing, or IT outsourcing agreement",
                "operation": "Once the represented party is clear, provide exactly one Markdown result table.",
                "output": "Overall Risk Rating",
                "constraint": "Do not produce the review until the represented party is clear.",
            },
            {
                "source_id": "RQ1B-V3-SRC-026070",
                "trigger": "A buyer or seller's deal team has a draft TSA (or a term sheet for one) and needs it checked against the deal perimeter before signing.",
                "operation": "Check service-schedule completeness against the deal perimeter.",
                "output": "Agreement Summary",
                "constraint": "If the TSA text or the purchase agreement/deal perimeter is not provided, stop and request it.",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W4R1-002": {
        "outcome": "ADVANCE_C2_PROMPT_CONSTRUCTION",
        "reason": (
            "The sources supply three peer visualisation routes from structured data: static "
            "DataFrame-oriented exploratory figures, R grammar-of-graphics publication figures, "
            "and interactive scientific charts. The artifact behaviour and runtime evidence are "
            "operationally distinct, but C2/C3 must remove source names and test whether a prompt "
            "remains singleton adequate rather than merely framework-specific."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-000006",
                "trigger": "Use for quick exploration of distributions, relationships, and categorical comparisons with attractive defaults.",
                "operation": "Work directly with DataFrames and named variables",
                "output": "fig.savefig('figure.png', dpi=300, bbox_inches='tight')",
                "constraint": "For interactive plots use plotly; for publication styling use scientific-visualization.",
            },
            {
                "source_id": "RQ1B-V3-SRC-010026",
                "trigger": "Build a publication figure in R",
                "operation": "Express the figure as **data + aesthetic mappings + one or more geometries + scales + facets + theme**.",
                "output": "ggsave('out.pdf', device = cairo_pdf)",
                "constraint": "Requires R and ggplot2; inspect installed package versions and export devices before using version-sensitive examples.",
            },
            {
                "source_id": "RQ1B-V3-SRC-012750",
                "trigger": "Create interactive scientific and statistical charts with Plotly.",
                "operation": "You help developers create publication-quality interactive charts",
                "output": "hover tooltips, zoom, and export capabilities",
                "constraint": "No special requirements",
            },
        ],
    },
    "RQ1B-V3-D1-C1-W4R1-003": {
        "outcome": "ADVANCE_C2_PROMPT_CONSTRUCTION",
        "reason": (
            "The sources provide peer presentation-authoring routes whose native deliverable and "
            "workspace boundary differ: a PowerPoint file, a cloud presentation object, and a "
            "repository-template HTML deck. This is enough to construct cue-controlled candidate "
            "prompts, but not enough to predeclare a strict winner for a generic request."
        ),
        "evidence": [
            {
                "source_id": "RQ1B-V3-SRC-019213",
                "trigger": "a .pptx or .potx file is involved in any way",
                "operation": "Write a `pptxgenjs` script",
                "output": ".pptx",
                "constraint": "`pptxgenjs` is preinstalled",
            },
            {
                "source_id": "RQ1B-V3-SRC-019694",
                "trigger": "Google Slides: Read and write presentations.",
                "operation": "Creates a blank presentation using the title given in the request.",
                "output": "Returns the created presentation.",
                "constraint": "Read `../gws-shared/SKILL.md` for auth, global flags, and security rules.",
            },
            {
                "source_id": "RQ1B-V3-SRC-011582",
                "trigger": "Create or update a RevealJS HTML presentation using the repository's bundled slide template.",
                "operation": "Copy that file to the requested output path, then edit the copied file.",
                "output": "RevealJS-based slide deck",
                "constraint": "repository's house template",
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
    checkpoint_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_004R1_CHECKPOINT.md"
    audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_004R1_FINALISER_AUDIT.json"
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
                if entry[key] == NOT_STATED:
                    continue
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
        "# RQ1b V3 D1 C1 Source-Evidence Wave 004r1\n\n"
        "Status: `COMPLETE / SOURCE-ONLY GATE / THREE C2 PERMISSIONS / NO PROMPT, GOLD, OR SELECTOR RESULT`\n\n"
        "## Inputs And Mechanical Audit\n\n"
        "- Three D1 source-only triad packets, comprising nine unique cross-origin canonical artifacts.\n"
        "- The initial W4 materialisation failure is retained. W4r1 changes only literal evidence formatting.\n"
        "- `C1_SOURCE_EVIDENCE_WAVE_AUDIT.json` passed: no hash drift and no source reuse.\n"
        "- Reviewers read only assigned originals; no prompt, label, representation, selector, score, or online source was available.\n"
        "- `NOT STATED` is retained only as a card-level absence marker for the NDA source; it is not invented evidence.\n\n"
        "## Final C1 Disposition\n\n"
        "| C1 outcome | Triads |\n|---|---:|\n"
        f"| Advance to C2 prompt construction | {counts['ADVANCE_C2_PROMPT_CONSTRUCTION']} |\n"
        f"| Reject: nonparallel/lifecycle/component | {counts['REJECT_NONPARALLEL_OR_COMPONENT']} |\n"
        f"| Reject: insufficient operational contrast | {counts['REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST']} |\n\n"
        "## Interpretation And Boundary\n\n"
        "The agreement, visualisation, and presentation triads provide three source-grounded peer-route compositions for later prompt construction. They are not yet strict clusters. C2 must construct direct and paraphrased requests, C3 must remove source/name/template/tool cues, and two independent C4 reviews must confirm a single fully adequate candidate before any C5/C6 freeze.\n\n"
        "The final source-evidence ledger is `c1_review_final_ledger.jsonl`; all quoted non-absence spans are mechanically checked as exact source substrings.\n"
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
