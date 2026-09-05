#!/usr/bin/env python3
"""Create a C2 construction roster from one frozen C1 final ledger.

This source-only lineage step does not construct a prompt, gold label,
acceptable set, selector input, embedding, metric, or routing result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c1-ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing_to_overwrite_existing_output:{args.output}")
    rows = [json.loads(line) for line in args.c1_ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
    approved = [row for row in rows if row.get("final_c1_outcome") == "ADVANCE_C2_PROMPT_CONSTRUCTION"]
    if not approved:
        raise SystemExit("no_c1_approved_rows")
    ledger_sha = sha256_file(args.c1_ledger)
    roster = []
    for row in approved:
        member_ids = list(row["member_source_ids"])
        if len(member_ids) not in {3, 4} or len(member_ids) != len(set(member_ids)):
            raise SystemExit(f"invalid_member_set:{row['c1_review_id']}")
        roster.append({
            "c1_review_id": row["c1_review_id"],
            "composition_id": row["parent_d1_draft_id"],
            "ledger_path": str(args.c1_ledger),
            "ledger_sha256": ledger_sha,
            "candidate_count": len(member_ids),
            "member_source_ids": member_ids,
            "prompt_variants_per_candidate": ["direct", "paraphrase"],
            "c2_scope": "SOURCE_INFORMED_DRAFT_ONLY",
            "claim_boundary": "C2 roster materialisation only. It is not a prompt, gold label, strict cluster, selector input, metric or routing result.",
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in roster), encoding="utf-8")
    audit = {
        "status": "RQ1B_V3_C2_ROSTER_MATERIALISATION_PASS_NOT_A_RESULT",
        "c1_ledger_sha256": ledger_sha,
        "composition_count": len(roster),
        "candidate_count": sum(row["candidate_count"] for row in roster),
        "expected_c2_record_count": 2 * sum(row["candidate_count"] for row in roster),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": "C2 roster materialisation only. It is not a prompt, gold label, strict cluster, selector input, metric or routing result.",
    }
    audit_path = args.output.with_name("C2_W5_ROSTER_AUDIT.json")
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
