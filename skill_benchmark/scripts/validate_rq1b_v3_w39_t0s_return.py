#!/usr/bin/env python3
"""Validate a Wave 039 source-only high-recall proposal-discovery return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batches", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--agent-return", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    batch = next((row for row in read_jsonl(args.batches) if row["batch_id"] == args.batch_id), None)
    if batch is None:
        raise SystemExit("unknown_batch")
    returned = json.loads(args.agent_return.read_text(encoding="utf-8"))
    failures, audits = [], []
    if returned.get("batch_id") != args.batch_id:
        failures.append("batch_id_mismatch")
    proposals = returned.get("proposals")
    if not isinstance(proposals, list) or len(proposals) > 3:
        failures.append("invalid_proposal_list")
        proposals = proposals if isinstance(proposals, list) else []
    no_reason = returned.get("no_proposal_reason")
    if not isinstance(no_reason, str) or (not proposals and not no_reason.strip()):
        failures.append("missing_no_proposal_reason")
    if proposals and no_reason.strip():
        failures.append("unexpected_no_proposal_reason")
    members = {row["source_id"]: row for row in batch["members"]}
    seen_groups = set()
    for proposal in proposals:
        ids = proposal.get("candidate_source_ids")
        if not isinstance(ids, list) or len(ids) not in {3, 4} or len(set(ids)) != len(ids):
            failures.append(f"invalid_candidate_ids:{proposal.get('proposal_id')}")
            continue
        group_key = tuple(sorted(ids))
        if group_key in seen_groups:
            failures.append(f"duplicate_candidate_group:{proposal.get('proposal_id')}")
        seen_groups.add(group_key)
        if any(source_id not in members for source_id in ids):
            failures.append(f"source_outside_batch:{proposal.get('proposal_id')}")
            continue
        if len({members[source_id]["origin_url"] for source_id in ids}) != len(ids):
            failures.append(f"non_distinct_origin:{proposal.get('proposal_id')}")
        if not isinstance(proposal.get("common_operational_envelope"), str) or not proposal["common_operational_envelope"].strip():
            failures.append(f"missing_envelope:{proposal.get('proposal_id')}")
        if not isinstance(proposal.get("reason"), str) or not proposal["reason"].strip():
            failures.append(f"missing_reason:{proposal.get('proposal_id')}")
        if not isinstance(proposal.get("known_risks"), str):
            failures.append(f"missing_known_risks:{proposal.get('proposal_id')}")
        evidence = proposal.get("literal_evidence")
        if not isinstance(evidence, dict) or set(evidence) != set(ids):
            failures.append(f"evidence_keys_mismatch:{proposal.get('proposal_id')}")
            continue
        cell_audit = []
        for source_id in ids:
            member = members[source_id]
            path = Path(member["local_raw_path"])
            span = evidence[source_id]
            valid = (
                isinstance(span, str) and bool(span.strip()) and path.is_file()
                and sha256_file(path) == member["source_sha256"]
                and span in path.read_text(encoding="utf-8", errors="replace")
            )
            cell_audit.append({"source_id": source_id, "status": "PASS" if valid else "FAIL", "substring": span})
            if not valid:
                failures.append(f"literal_or_hash_failure:{proposal.get('proposal_id')}:{source_id}")
        audits.append({"proposal_id": proposal.get("proposal_id"), "candidate_count": len(ids), "literal_evidence_audit": cell_audit})
    report = {
        "status": "RQ1B_V3_W39_T0S_RETURN_LITERAL_AUDIT_PASS_NOT_A_CLUSTER" if not failures else "RQ1B_V3_W39_T0S_RETURN_LITERAL_AUDIT_FAIL_NOT_A_CLUSTER",
        "batch_id": args.batch_id,
        "proposal_count": len(proposals),
        "failure_count": len(failures),
        "failures": failures,
        "proposal_audits": audits,
        "boundary": "This audit verifies only batch membership, distinct origins, local source binding and literal evidence. It does not validate a composition, prompt, label, selector, metric, retrieval result or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("batch_id", "proposal_count", "failure_count", "status")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
