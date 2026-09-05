#!/usr/bin/env python3
"""Substitute the audited post-micro-rewrite C3 record into Round 40's final ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGET = (
    "R40-C0A-web_commerce_automation-06",
    "r40m1-exa-labs-agent-skills-skills-lead-generation",
    "direct",
)


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
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--replacement", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.baseline)
    replacement_rows = read_jsonl(args.replacement)
    if len(replacement_rows) != 1 or key(replacement_rows[0]) != TARGET:
        raise SystemExit("invalid_replacement")
    by_key = {key(row): row for row in rows}
    if len(by_key) != len(rows) or TARGET not in by_key:
        raise SystemExit("invalid_baseline")
    old = by_key[TARGET]
    if old.get("c3_disposition") != "C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT":
        raise SystemExit("baseline_not_rewrite_record")
    by_key[TARGET] = replacement_rows[0]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for _, row in sorted(by_key.items())),
        encoding="utf-8",
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps({
        "status": "C3_ROUND40_FINAL_MANUAL_LEDGER_MERGED_NOT_A_LABEL_OR_RESULT",
        "row_count": len(by_key),
        "replaced_identity": {
            "proposal_id": TARGET[0],
            "intended_candidate_skill_id": TARGET[1],
            "variant": TARGET[2],
        },
        "prior_disposition": old.get("c3_disposition"),
        "replacement_disposition": replacement_rows[0].get("c3_disposition"),
        "exclusions": ["The merger does not create a gold label, adequacy decision, C4 review, C5 stratum, C6 freeze, retrieval input, metric, or result."],
    }, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"row_count": len(by_key), "replaced_identity": TARGET}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
