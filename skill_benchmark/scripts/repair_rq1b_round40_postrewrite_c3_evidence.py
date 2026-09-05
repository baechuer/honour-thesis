#!/usr/bin/env python3
"""Replace only non-literal Round 40 post-rewrite C3 evidence citations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TICK = chr(96)
REPAIRS = {
    f"Mobile First: Design for mobile, then adapt for tablet ({TICK}600-840dp{TICK}) and desktop ({TICK}>840dp{TICK}).": (
        "Design for mobile, then adapt for tablet"
    ),
    f"Use {TICK}SliverList.builder{TICK} or {TICK}SliverGrid.builder{TICK} for lists > 10 items.": "SliverList.builder",
    "Use SliverList.builder or SliverGrid.builder for lists > 10 items.": "SliverList.builder",
    f"Wrap main layouts in {TICK}SafeArea{TICK} to avoid device notches and system bar overlays.": "SafeArea",
    "Wrap main layouts in SafeArea to avoid device notches and system bar overlays.": "SafeArea",
    f"Each feature is self-contained under {TICK}src/features/<name>/{TICK}.": "Feature Module Structure",
    f"Rule: Never store tokens in AsyncStorage. Always use {TICK}expo-secure-store{TICK}.": "AsyncStorage",
    f"Test file naming: {TICK}useXxxViewModel.test.ts{TICK} — co-located or in {TICK}__tests__/{TICK}": "useXxxViewModel.test.ts",
    f"Collect flows with {TICK}collectAsStateWithLifecycle(){TICK}, not {TICK}collectAsState(){TICK}, so collection pauses in the background.": (
        "collectAsStateWithLifecycle()"
    ),
    "input.exclusion — companies to avoid (competitors, existing customers, results from earlier runs)": (
        "companies to avoid"
    ),
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict) -> tuple[str, str, str]:
    return (
        str(row.get("proposal_id", "")),
        str(row.get("intended_candidate_skill_id", "")),
        str(row.get("variant", "")),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    repairs: list[dict[str, str]] = []
    for row in rows:
        for index, evidence in enumerate(row.get("source_evidence_substrings", [])):
            if evidence in REPAIRS:
                replacement = REPAIRS[evidence]
                row["source_evidence_substrings"][index] = replacement
                repairs.append({
                    "proposal_id": key(row)[0],
                    "intended_candidate_skill_id": key(row)[1],
                    "variant": key(row)[2],
                    "old": evidence,
                    "new": replacement,
                    "reason": "validator-required exact original-artifact substring",
                })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in sorted(rows, key=key)),
        encoding="utf-8",
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps({
        "status": "C3_ROUND40_POSTREWRITE_LITERAL_EVIDENCE_REPAIRED_NOT_A_LABEL_OR_RESULT",
        "input_row_count": len(rows),
        "literal_citation_repairs": repairs,
        "preserved": [
            "proposal identity",
            "intended candidate identity",
            "prompt variant",
            "C3 disposition",
            "residual cue risk",
            "rationale",
            "review method",
        ],
        "exclusions": ["No C3 judgment, C4 review, C5 stratum, C6 freeze, retrieval input, metric, or result was changed."],
    }, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"citation_repairs": len(repairs)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
