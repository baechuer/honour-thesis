#!/usr/bin/env python3
"""Build a non-final Round 41 C3 ledger from initial and first-recheck reviews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REWORDED = "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict) -> tuple[str, str, str]:
    return (row["proposal_id"], row["intended_candidate_skill_id"], row["variant"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical", type=Path, required=True)
    parser.add_argument("--recheck", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    historical = {key(row): row for row in read_jsonl(args.historical)}
    recheck = {key(row): row for row in read_jsonl(args.recheck)}
    initially_reworded = {item for item, row in historical.items() if row["c3_disposition"] == REWORDED}
    if len(historical) != 24 or len(recheck) != len(initially_reworded) or set(recheck) != initially_reworded:
        raise SystemExit("invalid_round41_c3_lineage_coverage")

    merged = []
    for item, original in sorted(historical.items()):
        row = recheck[item] if item in recheck else original
        merged.append({
            **row,
            "c3_provisional_lineage": "initial_allowed" if item not in recheck else "initial_reworded_then_first_recheck",
            "c3_provisional_status": "C3_PROVISIONAL_PENDING_POSTREVIEW_FOR_UNRESOLVED_ROWS_NOT_A_LABEL_OR_RESULT",
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in merged), encoding="utf-8")
    unresolved = [row for row in merged if row["c3_disposition"] == REWORDED]
    summary = {
        "status": "C3_ROUND41_PROVISIONAL_LINEAGE_COMPLETE_PENDING_INDEPENDENT_POSTREVIEW_NOT_A_LABEL_OR_RESULT",
        "row_count": len(merged),
        "resolved_allowed_count": len(merged) - len(unresolved),
        "unresolved_postreview_count": len(unresolved),
        "unresolved_identities": [dict(proposal_id=row["proposal_id"], intended_candidate_skill_id=row["intended_candidate_skill_id"], variant=row["variant"]) for row in unresolved],
        "exclusions": [
            "This provisional ledger is not final C3 and must not be used for C4, C5, C6, retrieval, metrics, or results.",
            "The initial and recheck ledgers remain immutable review records.",
        ],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
