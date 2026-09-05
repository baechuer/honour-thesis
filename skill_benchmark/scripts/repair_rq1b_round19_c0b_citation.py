#!/usr/bin/env python3
"""Repair one verified Round 19 C0B citation without altering a judgment.

The correction replaces only a nonliteral space with the source's literal line
break. Candidate IDs, C0B status, and all prose judgments must remain bytewise
unchanged after JSON serialisation except for that evidence string.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROPOSAL = "R19-C0A-PBD-02"
SKILL = "r18m1-GoogleCloudPlatform-generative-ai-search-gemini-enterprise-ge-demo-generator-agent-template-demo-skills-professional-presentation"
OLD = "Build a polished 16:9 widescreen deck that looks like it came from a top-tier consulting firm, using python-pptx."
NEW = "Build a polished 16:9 widescreen deck that looks like it came from a top-tier\nconsulting firm, using python-pptx."


def read(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows = read(args.input)
    repairs = 0
    for row in rows:
        if row.get("proposal_id") != PROPOSAL:
            continue
        for evidence in row.get("candidate_evidence", []):
            if evidence.get("skill_id") != SKILL:
                continue
            values = evidence.get("evidence_substrings")
            if values != [OLD]:
                raise SystemExit("unexpected_original_citation")
            evidence["evidence_substrings"] = [NEW]
            repairs += 1
    if repairs != 1:
        raise SystemExit(f"repair_count:{repairs}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "status": "C0B_CITATION_ONLY_REPAIR_COMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "input": str(args.input),
        "output": str(args.output),
        "proposal_id": PROPOSAL,
        "skill_id": SKILL,
        "old_nonliteral_citation": OLD,
        "new_literal_citation": NEW,
        "judgment_boundary": "Only the evidence substring changed. Candidate IDs, C0B status, assessments, and rationales were preserved.",
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "repair_count": repairs}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
