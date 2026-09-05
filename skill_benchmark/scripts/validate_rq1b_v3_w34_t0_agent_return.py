#!/usr/bin/env python3
"""Validate source binding and literal evidence in one Wave 034 T0 return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--agent-return", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--status-prefix", default="RQ1B_V3_W34")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    args = parse_args()
    sources = {
        row["amendment_source_id"]: row
        for row in (
            json.loads(line)
            for line in args.amendment.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    returned = json.loads(args.agent_return.read_text(encoding="utf-8"))
    proposals = returned.get("proposals")
    if not isinstance(proposals, list):
        raise SystemExit("missing_proposals")

    proposal_audits = []
    failures = []
    for proposal in proposals:
        proposal_id = proposal.get("proposal_id")
        member_ids = proposal.get("member_source_ids")
        if not isinstance(member_ids, list) or len(member_ids) < 2 or len(set(member_ids)) != len(member_ids):
            failures.append({"proposal_id": proposal_id, "problem": "invalid_member_ids"})
            continue
        evidence = proposal.get("literal_evidence")
        if not isinstance(evidence, dict) or set(evidence) != set(member_ids):
            failures.append({"proposal_id": proposal_id, "problem": "evidence_members_mismatch"})
            continue
        cells = []
        for source_id in member_ids:
            source = sources.get(source_id)
            if source is None:
                cells.append({"source_id": source_id, "status": "UNKNOWN_SOURCE"})
                continue
            raw_path = Path(source["canonical"]["local_raw_path"])
            substring = evidence[source_id]
            text = raw_path.read_text(encoding="utf-8", errors="strict") if raw_path.is_file() else ""
            status = "PASS" if raw_path.is_file() and sha256(raw_path) == source["canonical"]["source_sha256"] and substring in text else "FAIL"
            cells.append({
                "source_id": source_id,
                "local_raw_path": str(raw_path),
                "substring": substring,
                "status": status,
            })
            if status != "PASS":
                failures.append({"proposal_id": proposal_id, "source_id": source_id, "problem": "source_hash_or_literal_mismatch"})
        proposal_audits.append({"proposal_id": proposal_id, "literal_cells": cells})

    report = {
        "status": (
            f"{args.status_prefix}_T0_AGENT_RETURN_LITERAL_AUDIT_PASS_NOT_A_CLUSTER"
            if not failures
            else f"{args.status_prefix}_T0_AGENT_RETURN_LITERAL_AUDIT_FAIL_NOT_A_CLUSTER"
        ),
        "agent_return": str(args.agent_return),
        "proposal_count": len(proposals),
        "failure_count": len(failures),
        "failures": failures,
        "proposal_audits": proposal_audits,
        "boundary": "This audit verifies only returned source IDs, source bytes and exact evidence substrings. It does not validate a task envelope, peer parallelism, C1 eligibility, prompt, label, selector, metric or result.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "proposal_count", "failure_count")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
