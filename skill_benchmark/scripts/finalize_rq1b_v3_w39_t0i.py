#!/usr/bin/env python3
"""Finalize independent T0 reviews of Wave 039 T0S source-only drafts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


FINAL_RETURN = {
    "RQ1B-V3-W39-T0I-B01": ("RQ1B-V3-W39-T0I-B01_R1_RAW_RETURN.json", "RQ1B-V3-W39-T0I-B01_R1_LITERAL_AUDIT.json"),
    "RQ1B-V3-W39-T0I-B02": ("RQ1B-V3-W39-T0I-B02_RAW_RETURN.json", "RQ1B-V3-W39-T0I-B02_LITERAL_AUDIT.json"),
    "RQ1B-V3-W39-T0I-B03": ("RQ1B-V3-W39-T0I-B03_RAW_RETURN.json", "RQ1B-V3-W39-T0I-B03_LITERAL_AUDIT.json"),
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-file", type=Path, required=True)
    parser.add_argument("--return-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_ledger")
    batches = {row["batch_id"]: row for row in read_jsonl(args.batch_file)}
    if set(batches) != set(FINAL_RETURN):
        raise SystemExit("unexpected_independent_t0_batches")
    outcomes, decisions = Counter(), []
    for batch_id, (return_name, audit_name) in FINAL_RETURN.items():
        audit = json.loads((args.audit_dir / audit_name).read_text(encoding="utf-8"))
        if audit.get("failure_count") != 0:
            raise SystemExit(f"literal_audit_failure:{batch_id}")
        raw = json.loads((args.return_dir / return_name).read_text(encoding="utf-8"))
        for row in raw["screened"]:
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
        "status": "RQ1B_V3_W39_T0I_COMPLETE_AWAITING_C1_NOT_A_CLUSTER",
        "screened_triads": len(decisions),
        "valid_final_batches": len(FINAL_RETURN),
        "outcome_counts": dict(sorted(outcomes.items())),
        "ready_for_c1_count": len(ready),
        "ready_for_c1": ready,
        "final_decisions": decisions,
        "invalid_retained_predecessor_returns": ["RQ1B-V3-W39-T0I-B01_RAW_RETURN.json", "RQ1B-V3-W39-T0I-B01_LITERAL_AUDIT.json"],
        "strict_total_before_and_after": {"compositions": 37, "prompt_cases": 231},
        "boundary": "Independent source-only T0 feasibility only. This creates no valid cluster, prompt, gold label, selector input, metric, retrieval result, information-field effect or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("screened_triads", "outcome_counts", "ready_for_c1_count", "status")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
