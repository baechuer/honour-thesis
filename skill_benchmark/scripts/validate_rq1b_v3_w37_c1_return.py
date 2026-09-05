#!/usr/bin/env python3
"""Validate one independent Wave 037 C1 source-evidence return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ALLOWED_OUTCOMES = {
    "ADVANCE_C2_PROMPT_CONSTRUCTION", "REJECT_SOURCE_BINDING",
    "REJECT_ABSENT_OPERATIONAL_CHAIN", "REJECT_NO_COMMON_ENVELOPE",
    "REJECT_NONPARALLEL_OR_COMPONENT", "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
    "NEEDS_PARENT_REVIEW",
}
FIELDS = ("trigger", "operation", "output", "constraint")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--review-id", required=True)
    parser.add_argument("--agent-return", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    packets = [json.loads(line) for line in args.roster.read_text(encoding="utf-8").splitlines() if line.strip()]
    packet = next((row for row in packets if row["c1_review_id"] == args.review_id), None)
    if packet is None:
        raise SystemExit("unknown_review_id")
    returned = json.loads(args.agent_return.read_text(encoding="utf-8"))
    failures = []
    if returned.get("c1_review_id") != args.review_id:
        failures.append("review_id_mismatch")
    if returned.get("outcome") not in ALLOWED_OUTCOMES:
        failures.append("invalid_outcome")
    expected_ids = [member["source_id"] for member in packet["members"]]
    if returned.get("member_source_ids") != expected_ids:
        failures.append("member_order_mismatch")
    evidence = returned.get("evidence")
    cells = []
    if not isinstance(evidence, dict) or set(evidence) != set(expected_ids):
        failures.append("evidence_key_mismatch")
        evidence = {}
    for member in packet["members"]:
        source_id = member["source_id"]
        source = Path(member["absolute_path"])
        field_map = evidence.get(source_id)
        if not isinstance(field_map, dict) or set(field_map) != set(FIELDS):
            failures.append(f"field_map_mismatch:{source_id}")
            continue
        exact_count = 0
        field_audit = {}
        text = source.read_text(encoding="utf-8") if source.is_file() else ""
        hash_ok = source.is_file() and sha256_file(source) == member["sha256"]
        for field in FIELDS:
            value = field_map[field]
            valid = value == "NOT STATED" or (isinstance(value, str) and value.strip() and value in text)
            if value != "NOT STATED" and valid:
                exact_count += 1
            field_audit[field] = "PASS" if valid else "FAIL"
            if not valid:
                failures.append(f"nonliteral:{source_id}:{field}")
        if not hash_ok:
            failures.append(f"hash_failure:{source_id}")
        if exact_count == 0:
            failures.append(f"no_exact_evidence:{source_id}")
        cells.append({"source_id": source_id, "hash_ok": hash_ok, "fields": field_audit, "exact_field_count": exact_count})
    if not isinstance(returned.get("reason"), str) or not returned["reason"].strip():
        failures.append("missing_reason")
    report = {
        "status": "RQ1B_V3_W37_C1_RETURN_LITERAL_AUDIT_PASS_NOT_A_CLUSTER" if not failures else "RQ1B_V3_W37_C1_RETURN_LITERAL_AUDIT_FAIL_NOT_A_CLUSTER",
        "c1_review_id": args.review_id,
        "failure_count": len(failures),
        "failures": failures,
        "evidence_audit": cells,
        "boundary": "This audit checks only review identity, source binding and literal evidence. It does not validate peer parallelism, prompt fitness, label validity, selector behaviour, metric, retrieval result or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "c1_review_id", "failure_count")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
