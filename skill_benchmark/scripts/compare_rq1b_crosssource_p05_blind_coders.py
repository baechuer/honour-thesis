#!/usr/bin/env python3
"""Compare two validated P0.5 coder audits without issuing a field lock.

This produces coordinator input only. Semantic equivalence of the stated
requirement and sealed-gold compatibility remain explicit human/coordinator
checks, so no automatic result can advance to P1.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_audit(path: Path) -> dict:
    value = json.loads(path.read_text())
    if value.get("status") != "P05_RESPONSE_AUDIT_NOT_A_CONSENSUS_OR_RESULT":
        raise ValueError(f"not a P0.5 response audit: {path}")
    return value


def by_family(audit: dict) -> dict[str, dict]:
    return {record["family_id"]: record for record in audit["records"]}


def code_map(record: dict) -> dict[str, str]:
    return {row["variant"]: row["code"] for row in record.get("compact", [])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-dir", type=Path, required=True)
    parser.add_argument("--primary-reviewer", required=True)
    parser.add_argument("--secondary-reviewer", required=True)
    args = parser.parse_args()

    audits_dir = args.batch_dir / "audits"
    primary = by_family(load_audit(audits_dir / f"p05_{args.primary_reviewer}_response_audit.json"))
    secondary = by_family(load_audit(audits_dir / f"p05_{args.secondary_reviewer}_response_audit.json"))
    families = sorted(set(primary) | set(secondary))
    records = []
    for family_id in families:
        first = primary.get(family_id, {"valid": False, "failures": ["missing_primary_audit_record"]})
        second = secondary.get(family_id, {"valid": False, "failures": ["missing_secondary_audit_record"]})
        first_codes = code_map(first)
        second_codes = code_map(second)
        same_code_by_variant = (
            first["valid"]
            and second["valid"]
            and first_codes == second_codes
            and bool(first_codes)
        )
        same_single_code_everywhere = (
            same_code_by_variant
            and len(set(first_codes.values())) == 1
            and next(iter(first_codes.values())) != "MULTI_FIELD_OR_NONCODEABLE"
        )
        records.append(
            {
                "family_id": family_id,
                "primary_valid": first["valid"],
                "secondary_valid": second["valid"],
                "primary_codes_by_variant": first_codes,
                "secondary_codes_by_variant": second_codes,
                "same_code_by_variant": same_code_by_variant,
                "same_single_nonmulti_code_everywhere": same_single_code_everywhere,
                "primary_failures": first.get("failures", []),
                "secondary_failures": second.get("failures", []),
                "required_next_coordinator_check": (
                    "MANUAL_REQUIREMENT_EQUIVALENCE_AND_SEALED_GOLD_COMPATIBILITY"
                    if first["valid"] and second["valid"] and same_single_code_everywhere
                    else "ORIGINAL_ONLY_UNLESS_REPLACEMENT_REVIEW_IS_SEPARATELY_COMPLETED"
                ),
            }
        )
    payload = {
        "status": "P05_BLIND_COMPARISON_INPUT_NOT_A_FIELD_LOCK_OR_RESULT",
        "primary_reviewer": args.primary_reviewer,
        "secondary_reviewer": args.secondary_reviewer,
        "counts": {
            "families": len(records),
            "both_valid": sum(item["primary_valid"] and item["secondary_valid"] for item in records),
            "same_single_nonmulti_code_everywhere": sum(item["same_single_nonmulti_code_everywhere"] for item in records),
        },
        "records": records,
        "exclusions": [
            "No field is locked by this comparison.",
            "No strict gold is unblinded by this comparison.",
            "No mask, selector, embedding, retrieval, API call, metric, or result exists.",
        ],
    }
    output = audits_dir / f"p05_{args.primary_reviewer}_vs_{args.secondary_reviewer}_comparison.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), **payload["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
