#!/usr/bin/env python3
"""Apply audited Round 40 C3 record-format and literal-citation repairs only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TICK = chr(96)
METHOD = "model_assisted_source_informed_c3_semantic_cue_review_not_human"
REPLACEMENTS = {
    "input, collision/physics, scoring, objectives, feedback": (
        "input, collision/physics, scoring, objectives"
    ),
    f"the {TICK}libs.versions.toml{TICK} version catalog": (
        f"Read {TICK}gradle/libs.versions.toml{TICK} and the module {TICK}build.gradle.kts{TICK}"
    ),
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    method_repairs = 0
    citation_repairs: list[dict[str, str]] = []
    for row in rows:
        if row.get("review_method") != METHOD:
            row["review_method"] = METHOD
            method_repairs += 1
        evidence = row.get("source_evidence_substrings", [])
        for index, item in enumerate(evidence):
            if item in REPLACEMENTS:
                replacement = REPLACEMENTS[item]
                evidence[index] = replacement
                citation_repairs.append({
                    "proposal_id": str(row.get("proposal_id")),
                    "intended_candidate_skill_id": str(row.get("intended_candidate_skill_id")),
                    "variant": str(row.get("variant")),
                    "old": item,
                    "new": replacement,
                    "reason": "validator-required exact original-artifact substring",
                })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in sorted(
            rows,
            key=lambda row: (str(row.get("proposal_id")), str(row.get("intended_candidate_skill_id")), str(row.get("variant"))),
        )),
        encoding="utf-8",
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps({
        "status": "C3_ROUND40_RECORD_FORMAT_AND_LITERAL_EVIDENCE_REPAIRED_NOT_A_LABEL_OR_RESULT",
        "input_row_count": len(rows),
        "review_method_key_repairs": method_repairs,
        "literal_citation_repairs": citation_repairs,
        "preserved": [
            "proposal identity",
            "intended candidate identity",
            "prompt variant",
            "C3 disposition",
            "residual cue risk",
            "rationale",
        ],
        "exclusions": ["No C3 judgment, C4 review, C5 stratum, C6 freeze, retrieval input, metric, or result was changed."],
    }, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "method_repairs": method_repairs,
        "citation_repairs": len(citation_repairs),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
