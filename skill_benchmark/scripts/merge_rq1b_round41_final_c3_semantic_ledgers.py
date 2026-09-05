#!/usr/bin/env python3
"""Merge Round 41 C3 review lineage without overwriting prior review records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED = "C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT"
REWORDED = "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def index_unique(rows: list[dict[str, Any]], label: str) -> dict[tuple[str, str, str], dict[str, Any]]:
    indexed = {key(row): row for row in rows}
    if len(indexed) != len(rows):
        raise SystemExit(f"duplicate_identity:{label}")
    return indexed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical", type=Path, required=True)
    parser.add_argument("--recheck", type=Path, action="append", required=True)
    parser.add_argument("--postreview", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    historical = index_unique(read_jsonl(args.historical), "historical")
    recheck = index_unique([row for path in args.recheck for row in read_jsonl(path)], "recheck")
    postreview = index_unique(read_jsonl(args.postreview), "postreview")
    initially_reworded = {item for item, row in historical.items() if row.get("c3_disposition") == REWORDED}
    recheck_reworded = {item for item, row in recheck.items() if row.get("c3_disposition") == REWORDED}
    failures: list[str] = []
    if set(recheck) != initially_reworded:
        failures.append(f"recheck_coverage:expected={len(initially_reworded)}:actual={len(recheck)}")
    if set(postreview) != recheck_reworded:
        failures.append(f"postreview_coverage:expected={len(recheck_reworded)}:actual={len(postreview)}")
    if any(row.get("c3_disposition") not in {ALLOWED, REWORDED} for row in [*historical.values(), *recheck.values(), *postreview.values()]):
        failures.append("invalid_disposition")

    merged: list[dict[str, Any]] = []
    for item, initial in sorted(historical.items()):
        final = initial
        lineage = "initial_allowed"
        if initial.get("c3_disposition") == REWORDED:
            followup = recheck.get(item)
            if followup is None:
                failures.append(f"missing_recheck:{item}")
                continue
            final = followup
            lineage = "initial_reworded_then_recheck"
            if followup.get("c3_disposition") == REWORDED:
                second_followup = postreview.get(item)
                if second_followup is None:
                    failures.append(f"missing_postreview:{item}")
                    continue
                final = second_followup
                lineage = "initial_reworded_then_recheck_reworded_then_postreview"
        merged.append({
            **final,
            "c3_final_lineage": lineage,
            "c3_final_status": "C3_FINAL_SEMANTIC_DISPOSITION_NOT_A_LABEL_OR_RESULT",
        })
    merged.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in merged), encoding="utf-8")
    final_reworded = sum(row.get("c3_disposition") == REWORDED for row in merged)
    summary = {
        "status": "C3_ROUND41_FINAL_SEMANTIC_LINEAGE_MERGED_NOT_A_LABEL_OR_RESULT" if not failures else "C3_ROUND41_FINAL_SEMANTIC_LINEAGE_INVALID_NOT_A_LABEL_OR_RESULT",
        "initial_prompt_count": len(historical),
        "initial_reworded_count": len(initially_reworded),
        "first_recheck_count": len(recheck),
        "postreview_count": len(postreview),
        "final_allowed_count": sum(row.get("c3_disposition") == ALLOWED for row in merged),
        "final_reworded_unresolved_count": final_reworded,
        "failures": failures,
        "exclusions": [
            "Prior C3 records remain immutable source records; this is a final-reference ledger only.",
            "No C4 review, C5 stratum, C6 freeze, retrieval input, model call, metric, or result was created.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
