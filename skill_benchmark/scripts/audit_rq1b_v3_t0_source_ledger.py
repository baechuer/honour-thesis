#!/usr/bin/env python3
"""Verify local provenance and literal source evidence for an RQ1b V3 T0 ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_t0_literal_audit")

    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    errors: list[str] = []
    literal_count = 0
    member_count = 0
    for composition in ledger.get("candidate_compositions", []):
        for member in composition.get("members", []):
            member_count += 1
            source_path = Path(member["local_raw_path"])
            if not source_path.exists():
                errors.append(f"missing_source:{member['source_id']}")
                continue
            raw = source_path.read_bytes()
            actual_hash = hashlib.sha256(raw).hexdigest()
            if actual_hash != member["source_sha256"]:
                errors.append(f"hash_mismatch:{member['source_id']}")
            source_text = raw.decode("utf-8")
            for literal in member.get("literal_evidence", []):
                literal_count += 1
                if literal not in source_text:
                    errors.append(f"nonliteral_evidence:{composition['composition_id']}:{member['source_id']}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "claim_boundary": "This audit verifies only frozen local source-byte hashes and exact literal evidence substrings. It does not decide peer roles, C1 eligibility, prompts, labels, selectors, retrieval, metrics, or results.",
        "review": str(args.ledger),
        "composition_count": len(ledger.get("candidate_compositions", [])),
        "checked_member_count": member_count,
        "checked_literal_count": literal_count,
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
