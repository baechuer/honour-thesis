#!/usr/bin/env python3
"""Validate complete direct/paraphrase C2 coverage against C1-passing drafts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c1", type=Path, required=True)
    parser.add_argument("--draft", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    expected = {
        (str(record["proposal_id"]), str(skill_id))
        for record in read_jsonl(args.c1)
        if record.get("c1_status") == "C1_INTEGRITY_PASS_NOT_A_CLUSTER_OR_RESULT"
        for skill_id in record["candidate_skill_ids"]
    }
    rows = [row for path in args.draft for row in read_jsonl(path)]
    counts: Counter[tuple[str, str, str]] = Counter()
    failures: list[str] = []
    for row in rows:
        key = (str(row.get("proposal_id", "")), str(row.get("intended_candidate_skill_id", "")))
        variant = str(row.get("variant", ""))
        if key not in expected:
            failures.append(f"unexpected_candidate:{key[0]}:{key[1]}")
        if variant not in {"direct", "paraphrase"}:
            failures.append(f"invalid_variant:{key[0]}:{key[1]}:{variant}")
        if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
            failures.append(f"blank_prompt:{key[0]}:{key[1]}:{variant}")
        counts[(key[0], key[1], variant)] += 1
    for proposal_id, skill_id in sorted(expected):
        for variant in ("direct", "paraphrase"):
            if counts[(proposal_id, skill_id, variant)] != 1:
                failures.append(f"variant_count:{proposal_id}:{skill_id}:{variant}:{counts[(proposal_id, skill_id, variant)]}")
    rows.sort(key=lambda row: (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary = {
        "status": "C2_DRAFT_VALID_NOT_A_LABEL_OR_RESULT" if not failures else "C2_DRAFT_INVALID_NOT_A_LABEL_OR_RESULT",
        "prompt_count": len(rows),
        "candidate_count": len(expected),
        "direct_count": sum(row.get("variant") == "direct" for row in rows),
        "paraphrase_count": sum(row.get("variant") == "paraphrase" for row in rows),
        "failures": failures,
        "exclusions": ["No C3 cue disposition, C4 adequacy review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was created."],
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
