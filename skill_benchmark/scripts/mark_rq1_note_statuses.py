#!/usr/bin/env python3
"""Add a single, idempotent current/supporting/historical banner to RQ1 notes."""

from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
CURRENT = REPO / "thesis_notes/current"
INDEX = "thesis_notes/current/RQ1/README.md"
MARKER_START = "<!-- RQ1-RECORD-STATUS:START -->"
MARKER_END = "<!-- RQ1-RECORD-STATUS:END -->"


CANONICAL = {
    "RQ1 Marking Criteria Audit - 2026-09-04.md": (
        "CURRENT_CANONICAL",
        "Current rubric audit and inconsistency register. Reassess after the prospective human-review ledgers are completed.",
    ),
    "RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP - 2026-09-04.md": (
        "CURRENT_CANONICAL",
        "Current single-field public-original experiment protocol and scoring boundary.",
    ),
    "RQ1 Public Original Round 3 Joint Group Extension SOP - 2026-09-04.md": (
        "CURRENT_CANONICAL",
        "Current supporting joint-group public-original experiment protocol.",
    ),
}

SUPPORTING = {
    "RQ1 Field Targeted Test Plan.md": (
        "CURRENT_SUPPORTING",
        "Its controlled field-isolation design remains current. Its dated public-RQ1 status sections are historical and are superseded by the Round-3 public-original SOP and result packet.",
    ),
    "RQ1 Public Corpus Consolidation Policy - 2026-08-31.md": (
        "CURRENT_SUPPORTING",
        "Use for source-registry provenance and counting policy only, not as the current scored result.",
    ),
    "RQ1 Step 1 Body-Only Field Audit Protocol - 2026-09-04.md": (
        "CURRENT_PLANNED_SUPPORTING",
        "Current optional public-corpus prevalence protocol. Its output directory is empty and no pilot or full-frame result exists yet; it is not part of the completed RQ1 evidence.",
    ),
}

SPECIAL_HISTORICAL = {
    "RQ1a Human Review Protocol - 2026-08-30.md": (
        "HISTORICAL_RETROSPECTIVE_REVIEW",
        "Retains the retrospective author-confirmation record. The prospective gold-hidden review workspace at skill_benchmark/rq1_human_review/2026-09-04/ is now the active human-review route.",
    ),
    "RQ1 Public Original-Document Exhaustive Field-Cue Ablation Protocol - 2026-08-31.md": (
        "HISTORICAL_METHOD_LINEAGE",
        "Retains the protocol lineage that led to Round 3. Its pending/no-selector status is superseded by the completed Round-3 scoring records.",
    ),
}


def status_for(path: Path) -> tuple[str, str]:
    if path.name in CANONICAL:
        return CANONICAL[path.name]
    if path.name in SUPPORTING:
        return SUPPORTING[path.name]
    if path.name in SPECIAL_HISTORICAL:
        return SPECIAL_HISTORICAL[path.name]
    return (
        "HISTORICAL_OR_SUPERSEDED",
        "Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward.",
    )


def add_banner(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    status, note = status_for(path)
    banner = (
        f"{MARKER_START}\n"
        f"> **RQ1 record status (2026-09-04): `{status}`.** {note} "
        f"Canonical index: `{INDEX}`.\n"
        f"{MARKER_END}"
    )
    pattern = re.compile(
        rf"\n?{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?",
        flags=re.DOTALL,
    )
    text = pattern.sub("\n", text)
    lines = text.splitlines()
    heading_index = next((index for index, line in enumerate(lines) if line.startswith("# ")), None)
    if heading_index is None:
        raise RuntimeError(f"No H1 heading in {path}")
    lines[heading_index + 1 : heading_index + 1] = ["", banner]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    paths = sorted(CURRENT.glob("RQ1*.md"))
    if not paths:
        raise RuntimeError("No RQ1 notes found")
    for path in paths:
        add_banner(path)
    print(f"Marked {len(paths)} RQ1 notes")


if __name__ == "__main__":
    main()
