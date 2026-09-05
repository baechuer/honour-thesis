#!/usr/bin/env python3
"""Create the Wave 037 T0 principal ledger from literal-valid final returns."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


FINALS = {
    "RQ1B-V3-W37-T0-B01": ("W37_T0_B01_R1_RAW_RETURN.json", "W37_T0_B01_R1_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B02": ("W37_T0_B02_R2_RAW_RETURN.json", "W37_T0_B02_R2_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B03": ("W37_T0_B03_R2_RAW_RETURN.json", "W37_T0_B03_R2_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B04": ("W37_T0_B04_RAW_RETURN.json", "W37_T0_B04_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B05": ("W37_T0_B05_RAW_RETURN.json", "W37_T0_B05_LITERAL_AUDIT.json"),
    "RQ1B-V3-W37-T0-B06": ("W37_T0_B06_RAW_RETURN.json", "W37_T0_B06_LITERAL_AUDIT.json"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--return-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_existing_ledger")
    outcomes = Counter()
    decisions = []
    for batch_id, (return_name, audit_name) in FINALS.items():
        audit = json.loads((args.audit_dir / audit_name).read_text(encoding="utf-8"))
        if audit.get("failure_count") != 0:
            raise SystemExit(f"final_return_not_literal_valid:{batch_id}")
        returned = json.loads((args.return_dir / return_name).read_text(encoding="utf-8"))
        for row in returned["screened"]:
            outcomes[row["outcome"]] += 1
            decisions.append({
                "batch_id": batch_id,
                "t0_review_id": row["t0_review_id"],
                "member_source_ids": row["member_source_ids"],
                "outcome": row["outcome"],
                "reason": row["reason"],
            })
    ready = [row for row in decisions if row["outcome"] == "READY_FOR_C1"]
    report = {
        "status": "RQ1B_V3_W37_T0_COMPLETE_THREE_C1_CANDIDATES_NOT_A_CLUSTER",
        "screened_triads": len(decisions),
        "valid_final_batches": len(FINALS),
        "outcome_counts": dict(sorted(outcomes.items())),
        "ready_for_c1_count": len(ready),
        "ready_for_c1": ready,
        "final_decisions": decisions,
        "invalid_retained_predecessor_returns": [
            "W37_T0_B01_RAW_RETURN.json", "W37_T0_B02_RAW_RETURN.json",
            "W37_T0_B02_R1_RAW_RETURN.json", "W37_T0_B03_RAW_RETURN.json",
            "W37_T0_B03_R1_RAW_RETURN.json",
        ],
        "strict_total_before_and_after": {"compositions": 37, "prompt_cases": 231},
        "boundary": "T0 is local source-only curation feasibility. It creates no valid cluster, prompt, gold label, selector input, metric, retrieval result, information-field effect or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "screened_triads", "outcome_counts", "ready_for_c1_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
