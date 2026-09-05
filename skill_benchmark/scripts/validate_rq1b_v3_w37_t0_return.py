#!/usr/bin/env python3
"""Validate one structured Wave 037 source-only T0 reviewer return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ALLOWED_OUTCOMES = {
    "READY_FOR_C1", "LIKELY_NONPARALLEL", "NO_PLAUSIBLE_TRIAD", "NEEDS_PARENT_REVIEW",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-file", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--agent-return", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    batches = [json.loads(line) for line in args.batch_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    batch = next((row for row in batches if row["batch_id"] == args.batch_id), None)
    if batch is None:
        raise SystemExit("unknown_batch_id")
    returned = json.loads(args.agent_return.read_text(encoding="utf-8"))
    expected = {triad["t0_review_id"]: triad for triad in batch["triads"]}
    screened = returned.get("screened")
    failures = []
    audits = []
    if returned.get("batch_id") != args.batch_id:
        failures.append("batch_id_mismatch")
    if not isinstance(screened, list) or len(screened) != len(expected):
        failures.append("screened_count_mismatch")
        screened = screened if isinstance(screened, list) else []
    seen = set()
    for row in screened:
        triad_id = row.get("t0_review_id")
        triad = expected.get(triad_id)
        if triad is None or triad_id in seen:
            failures.append(f"unknown_or_duplicate_triad:{triad_id}")
            continue
        seen.add(triad_id)
        member_ids = [member["source_id"] for member in triad["members"]]
        if row.get("outcome") not in ALLOWED_OUTCOMES:
            failures.append(f"invalid_outcome:{triad_id}")
        if row.get("member_source_ids") != member_ids:
            failures.append(f"member_order_mismatch:{triad_id}")
        evidence = row.get("literal_evidence")
        if not isinstance(evidence, dict) or set(evidence) != set(member_ids):
            failures.append(f"evidence_key_mismatch:{triad_id}")
            continue
        row_audit = []
        for member in triad["members"]:
            source_id = member["source_id"]
            span = evidence[source_id]
            source_path = Path(member["absolute_path"])
            valid = (
                isinstance(span, str) and span.strip() and source_path.is_file()
                and sha256_file(source_path) == member["sha256"]
                and span in source_path.read_text(encoding="utf-8")
            )
            row_audit.append({"source_id": source_id, "status": "PASS" if valid else "FAIL", "substring": span})
            if not valid:
                failures.append(f"literal_or_hash_failure:{triad_id}:{source_id}")
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            failures.append(f"missing_reason:{triad_id}")
        audits.append({"t0_review_id": triad_id, "outcome": row.get("outcome"), "literal_evidence_audit": row_audit})
    if set(expected) != seen:
        failures.append("missing_assigned_triad")
    report = {
        "status": "RQ1B_V3_W37_T0_RETURN_LITERAL_AUDIT_PASS_NOT_A_CLUSTER" if not failures else "RQ1B_V3_W37_T0_RETURN_LITERAL_AUDIT_FAIL_NOT_A_CLUSTER",
        "batch_id": args.batch_id,
        "failure_count": len(failures),
        "failures": failures,
        "triad_audits": audits,
        "boundary": "This audit checks only batch identity, source binding and literal evidence. It does not validate the reviewer judgement, a cluster, prompt, gold label, selector, metric, field effect, retrieval result or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "batch_id", "failure_count")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
