#!/usr/bin/env python3
"""Freeze literal-valid Wave 039 source-only proposal-discovery outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batches", type=Path, required=True)
    parser.add_argument("--return-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_ledger")
    batch_rows = read_jsonl(args.batches)
    proposals, empty_batches = [], []
    for batch in batch_rows:
        batch_id = batch["batch_id"]
        raw = json.loads((args.return_dir / f"{batch_id}_RAW_RETURN.json").read_text(encoding="utf-8"))
        audit = json.loads((args.audit_dir / f"{batch_id}_LITERAL_AUDIT.json").read_text(encoding="utf-8"))
        if audit.get("failure_count") != 0:
            raise SystemExit(f"literal_audit_failure:{batch_id}")
        if raw["proposals"]:
            for proposal in raw["proposals"]:
                proposals.append({"batch_id": batch_id, **proposal})
        else:
            empty_batches.append({"batch_id": batch_id, "reason": raw["no_proposal_reason"]})
    report = {
        "status": "RQ1B_V3_W39_T0S_PROPOSALS_FROZEN_AWAITING_INDEPENDENT_T0_NOT_A_CLUSTER",
        "batch_count": len(batch_rows),
        "literal_valid_proposal_count": len(proposals),
        "literal_valid_proposals": proposals,
        "empty_batch_count": len(empty_batches),
        "empty_batches": empty_batches,
        "boundary": "These are source-only high-recall draft proposals. They have no prompt, intended winner, gold label, selector input, metric, retrieval result, information-field effect or valid-cluster status. Each needs a separate independent T0 review.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("batch_count", "literal_valid_proposal_count", "empty_batch_count", "status")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
