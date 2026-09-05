#!/usr/bin/env python3
"""Mechanically validate C2 coverage for the Round 34 C1-passed drafts.

This checker is intentionally narrow: it verifies one direct and one
paraphrase construction target per admitted candidate. It does not determine
cue safety, adequacy, a gold label, an acceptable set, or a benchmark result.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


PASS = "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c1", type=Path, required=True)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    expected = {
        (str(row["proposal_id"]), str(skill_id))
        for row in read_jsonl(args.c1)
        if row.get("c1_status") == PASS
        for skill_id in row.get("candidate_skill_ids", [])
    }
    rows = [row for path in args.input for row in read_jsonl(path)]
    counts: Counter[tuple[str, str, str]] = Counter()
    failures: list[str] = []
    for row in rows:
        proposal_id = str(row.get("proposal_id", ""))
        skill_id = str(row.get("intended_candidate_skill_id", ""))
        variant = str(row.get("variant", ""))
        prompt = row.get("prompt")
        if row.get("c2_status") != "C2_DRAFT_NOT_A_LABEL_OR_RESULT":
            failures.append(f"unexpected_status:{proposal_id}:{skill_id}:{variant}")
        if (proposal_id, skill_id) not in expected:
            failures.append(f"unexpected_candidate:{proposal_id}:{skill_id}")
        if variant not in {"direct", "paraphrase"}:
            failures.append(f"invalid_variant:{proposal_id}:{skill_id}:{variant}")
        if not isinstance(prompt, str) or not prompt.strip():
            failures.append(f"blank_prompt:{proposal_id}:{skill_id}:{variant}")
        counts[(proposal_id, skill_id, variant)] += 1
    for proposal_id, skill_id in sorted(expected):
        for variant in ("direct", "paraphrase"):
            if counts[(proposal_id, skill_id, variant)] != 1:
                failures.append(f"variant_count:{proposal_id}:{skill_id}:{variant}:{counts[(proposal_id, skill_id, variant)]}")
    if len(rows) != 2 * len(expected):
        failures.append(f"row_count:{len(rows)}:expected:{2 * len(expected)}")
    rows.sort(key=lambda row: (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C2_ROUND34_COVERAGE_VALID_NOT_A_LABEL_OR_RESULT" if not failures else "C2_ROUND34_COVERAGE_INVALID_NOT_A_LABEL_OR_RESULT",
        "c1_candidate_count": len(expected),
        "prompt_count": len(rows),
        "direct_count": sum(row.get("variant") == "direct" for row in rows),
        "paraphrase_count": sum(row.get("variant") == "paraphrase" for row in rows),
        "failures": failures,
        "exclusions": [
            "This validates construction coverage only.",
            "No C3 cue disposition, C4 adequacy decision, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was produced.",
        ],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "c1_candidate_count", "prompt_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
