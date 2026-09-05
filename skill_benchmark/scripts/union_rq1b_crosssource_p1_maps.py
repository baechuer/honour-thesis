#!/usr/bin/env python3
"""Union two validated P1/P2 maps without approving masking."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    if value.get("status") != "P1_P2_LITERAL_EVIDENCE_AUDIT_NOT_A_UNION_DECISION_OR_RESULT":
        raise ValueError(f"unexpected audit status: {path}")
    if not value.get("valid"):
        raise ValueError(f"invalid map audit: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--family-id", required=True)
    parser.add_argument("--first-reviewer", required=True)
    parser.add_argument("--second-reviewer", required=True)
    args = parser.parse_args()
    audits = args.root / "audits"
    first = load(audits / f"{args.family_id}_{args.first_reviewer}_audit.json")
    second = load(audits / f"{args.family_id}_{args.second_reviewer}_audit.json")
    records = []
    seen = set()
    for review_name, audit in ((args.first_reviewer, first), (args.second_reviewer, second)):
        for record in audit["records"]:
            key = (record["candidate"], record["quote"], record["carrier"], record["classification"])
            if key not in seen:
                seen.add(key)
                records.append({"raised_by": [review_name], **record})
            else:
                next(item for item in records if (item["candidate"], item["quote"], item["carrier"], item["classification"]) == key)["raised_by"].append(review_name)
    inseparable = [record for record in records if record["classification"] == "inseparable_structural_cue"]
    unresolved = [record for record in records if record["classification"] not in {"differential_target_field", "shared_non_target", "inseparable_structural_cue"}]
    payload = {
        "status": "P1_P2_UNION_INPUT_NOT_A_MASK_DECISION_OR_RESULT",
        "family_id": args.family_id,
        "map_reviewers": [args.first_reviewer, args.second_reviewer],
        "entry_count": len(records),
        "inseparable_structural_cue_count": len(inseparable),
        "unresolved_count": len(unresolved),
        "mandatory_coordinator_disposition": (
            "ORIGINAL_ONLY_REQUIRED_BEFORE_P3" if inseparable or unresolved else "MANUAL_COMPLETENESS_REVIEW_REQUIRED_BEFORE_P3"
        ),
        "records": records,
        "exclusions": [
            "The union records source concerns; it does not approve a mask.",
            "No mask, selector, embedding, retrieval, API call, metric, or result exists.",
        ],
    }
    output = audits / f"{args.family_id}_{args.first_reviewer}_vs_{args.second_reviewer}_union.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "entry_count": len(records), "inseparable": len(inseparable)}, sort_keys=True))


if __name__ == "__main__":
    main()
