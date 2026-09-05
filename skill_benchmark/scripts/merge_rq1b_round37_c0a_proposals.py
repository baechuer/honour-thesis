#!/usr/bin/env python3
"""Reuse the frozen C0A mechanical validator with Round 37 status labels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from merge_rq1b_round21_c0a_proposals import main as validate_round21_shape


def main() -> int:
    try:
        summary_path = Path(sys.argv[sys.argv.index("--output-summary") + 1])
    except (ValueError, IndexError) as error:
        raise SystemExit("--output-summary is required") from error
    exit_code = validate_round21_shape()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["status"] = (
        "C0A_ROUND37_MERGED_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT"
        if summary.get("status") == "C0A_ROUND21_MERGED_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT"
        else "C0A_ROUND37_MERGE_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT"
    )
    summary["round"] = "RQ1b cross-source Round 37"
    summary["round21_validator_reused_only_for_structural_mechanics"] = True
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "structurally_valid_proposal_count": summary.get("structurally_valid_proposal_count"), "structurally_rejected_proposal_count": summary.get("structurally_rejected_proposal_count")}, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
