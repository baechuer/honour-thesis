#!/usr/bin/env python3
"""Merge a Round 42 C3 follow-up review into the prior complete C3 ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row["proposal_id"]), str(row["intended_candidate_skill_id"]), str(row["variant"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--rewrites", type=Path, required=True)
    parser.add_argument("--followup", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    prior_rows = read_jsonl(args.prior)
    prior_by_key = {key(row): row for row in prior_rows}
    rewrite_keys = {key(row) for row in read_jsonl(args.rewrites)}
    followup_rows = [row for path in args.followup for row in read_jsonl(path)]
    followup_by_key = {key(row): row for row in followup_rows}
    if len(prior_by_key) != len(prior_rows) or len(followup_by_key) != len(followup_rows):
        raise SystemExit("duplicate_identity")
    if set(followup_by_key) != rewrite_keys or not rewrite_keys <= set(prior_by_key):
        raise SystemExit("followup_coverage_mismatch")

    final_rows = [followup_by_key.get(row_key, row) for row_key, row in prior_by_key.items()]
    final_rows.sort(key=key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in final_rows), encoding="utf-8")
    summary = {
        "status": "C3_ROUND42_FOLLOWUP_RECHECK_MERGED_NOT_A_LABEL_OR_RESULT",
        "prior_prompt_count": len(prior_rows),
        "followup_rechecked_prompt_count": len(followup_rows),
        "final_prompt_count": len(final_rows),
        "risk_counts": {risk: sum(row.get("residual_cue_risk") == risk for row in final_rows) for risk in ("low", "medium", "high")},
        "exclusions": ["This merge is C3 cue history only; it does not create adequacy, a label, retrieval input, metric, or frozen cluster."],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
