#!/usr/bin/env python3
"""Repair two Round 21 C0B evidence citations without altering judgments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPAIRS = {
    (
        "R21-C0A-CREATIVE-MEDIA-EDUCATION-002",
        "r21m1-icgma-slide-skill-unknown",
    ): (
        "this entry file owns scenario routing only",
        "**scenario routing only**",
    ),
    (
        "R21-C0A-SPECIALISED-PROFESSIONAL-001",
        "r21m1-kayaman-skills-app-security",
    ): (
        "suitable for both quick audits and thorough threat modeling sessions.",
        "Structured as actionable checklists organized by domain, suitable for both\nquick audits and thorough threat modeling sessions.",
    ),
}


def read(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows = read(args.input)
    repairs: list[dict[str, str]] = []
    for row in rows:
        for evidence in row.get("candidate_evidence", []):
            key = (str(row.get("proposal_id")), str(evidence.get("skill_id")))
            replacement = REPAIRS.get(key)
            if replacement is None:
                continue
            old, new = replacement
            values = evidence.get("evidence_substrings")
            if not isinstance(values, list) or old not in values:
                raise SystemExit(f"unexpected_original_citation:{key}")
            evidence["evidence_substrings"] = [new if value == old else value for value in values]
            repairs.append({"proposal_id": key[0], "skill_id": key[1], "old": old, "new": new})
    if len(repairs) != len(REPAIRS):
        raise SystemExit(f"repair_count:{repairs}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "status": "C0B_CITATION_ONLY_REPAIR_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "input": str(args.input),
        "output": str(args.output),
        "repairs": repairs,
        "judgment_boundary": "Only the two evidence substrings changed. Candidate IDs, C0B statuses, assessments, and rationales were preserved.",
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "repair_count": repairs}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
