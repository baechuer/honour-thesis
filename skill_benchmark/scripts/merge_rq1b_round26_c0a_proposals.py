#!/usr/bin/env python3
"""Run the frozen C0A structural validator with Round 26 provenance labels.

The shared validator checks proposal mechanics against a source-only pool; the
post-processing here changes only its round-specific summary label. It does
not inspect original bodies or make a semantic, prompt, label, or result claim.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from merge_rq1b_round21_c0a_proposals import main as validate_round21_shape


def output_summary_path(argv: list[str]) -> Path:
    try:
        return Path(argv[argv.index("--output-summary") + 1])
    except (ValueError, IndexError) as error:
        raise SystemExit("--output-summary is required") from error


def main() -> int:
    summary_path = output_summary_path(sys.argv[1:])
    exit_code = validate_round21_shape()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    old_status = summary.get("status")
    if old_status == "C0A_ROUND21_MERGED_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT":
        summary["status"] = "C0A_ROUND26_MERGED_SOURCE_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT"
    else:
        summary["status"] = "C0A_ROUND26_MERGE_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT"
    summary["round"] = "RQ1b cross-source Round 26"
    summary["round21_validator_reused_only_for_structural_mechanics"] = True
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "structurally_valid_proposal_count": summary.get("structurally_valid_proposal_count"),
        "structurally_rejected_proposal_count": summary.get("structurally_rejected_proposal_count"),
    }, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
