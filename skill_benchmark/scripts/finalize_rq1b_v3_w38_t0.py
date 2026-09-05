#!/usr/bin/env python3
"""Create a Wave 038 T0 ledger from literal-valid batch returns."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-file", type=Path, required=True)
    parser.add_argument("--return-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_existing_ledger")
    batches = [json.loads(line) for line in args.batch_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    outcomes, decisions = Counter(), []
    for batch in batches:
        batch_id = batch["batch_id"]
        return_path = args.return_dir / f"{batch_id}_RAW_RETURN.json"
        audit_path = args.audit_dir / f"{batch_id}_LITERAL_AUDIT.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if audit.get("failure_count") != 0:
            raise SystemExit(f"final_return_not_literal_valid:{batch_id}")
        returned = json.loads(return_path.read_text(encoding="utf-8"))
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
        "status": "RQ1B_V3_W38_T0_COMPLETE_AWAITING_C1_NOT_A_CLUSTER",
        "screened_triads": len(decisions),
        "valid_final_batches": len(batches),
        "outcome_counts": dict(sorted(outcomes.items())),
        "ready_for_c1_count": len(ready),
        "ready_for_c1": ready,
        "final_decisions": decisions,
        "strict_total_before_and_after": {"compositions": 37, "prompt_cases": 231},
        "boundary": "T0 is source-only curation feasibility. It creates no valid cluster, prompt, gold label, selector input, metric, retrieval result, information-field effect or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "screened_triads", "outcome_counts", "ready_for_c1_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
