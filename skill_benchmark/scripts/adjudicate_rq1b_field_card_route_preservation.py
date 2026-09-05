#!/usr/bin/env python3
"""Compare blinded original-card reviews with sealed RQ1b-S pilot lineage.

This is a local validation gate for a derivative field-card representation. It
creates no target/sham neutralisation, selector input, embedding, retrieval,
API call, score, metric, or thesis result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--first-reviewer", required=True)
    parser.add_argument("--second-reviewer", required=True)
    args = parser.parse_args()

    root = args.pilot_root
    private_records = {item["pilot_id"]: item for item in json.loads((root / "private_lineage_manifest.json").read_text())}
    private = private_records[args.pilot_id]
    label_by_skill = {item["skill_id"]: item["label"] for item in private["private_candidates"]}
    gold_label = label_by_skill[private["strict_gold_skill_id"]]
    locked_field = private["locked_field"]
    variants = [item["prompt_variant"] for item in private["prompt_lineage"]]

    first_audit = load_object(root / "audits" / f"{args.pilot_id}_{args.first_reviewer}_route_review_audit.json")
    second_audit = load_object(root / "audits" / f"{args.pilot_id}_{args.second_reviewer}_route_review_audit.json")
    first = load_object(root / "route_reviews" / args.first_reviewer / f"{args.pilot_id}.json")
    second = load_object(root / "route_reviews" / args.second_reviewer / f"{args.pilot_id}.json")
    first_by_variant = {item["variant"]: item for item in first.get("per_prompt", [])}
    second_by_variant = {item["variant"]: item for item in second.get("per_prompt", [])}

    rows = []
    for variant in variants:
        one = first_by_variant.get(variant, {})
        two = second_by_variant.get(variant, {})
        first_set = one.get("fully_adequate_candidates", [])
        second_set = two.get("fully_adequate_candidates", [])
        singleton_gold = first_set == [gold_label] and second_set == [gold_label]
        field_reaffirmed = one.get("primary_field") == locked_field and two.get("primary_field") == locked_field
        rows.append(
            {
                "variant": variant,
                "sealed_gold_label": gold_label,
                "first_fully_adequate_candidates": first_set,
                "second_fully_adequate_candidates": second_set,
                "first_primary_field": one.get("primary_field"),
                "second_primary_field": two.get("primary_field"),
                "singleton_gold_preserved": singleton_gold,
                "locked_field_reaffirmed": field_reaffirmed,
                "pass": singleton_gold and field_reaffirmed,
            }
        )

    valid_reviews = bool(first_audit.get("valid")) and bool(second_audit.get("valid"))
    passed = valid_reviews and all(row["pass"] for row in rows)
    payload = {
        "status": (
            "RQ1B_S_ORIGINAL_CARD_ROUTE_PRESERVATION_PASS_NOT_A_SELECTOR_RESULT"
            if passed
            else "RQ1B_S_ORIGINAL_CARD_ROUTE_PRESERVATION_FAIL_NOT_A_SELECTOR_RESULT"
        ),
        "pilot_id": args.pilot_id,
        "locked_field": locked_field,
        "sealed_gold_label": gold_label,
        "first_reviewer": args.first_reviewer,
        "second_reviewer": args.second_reviewer,
        "both_reviews_schema_valid": valid_reviews,
        "variant_rows": rows,
        "exclusions": [
            "No target neutralisation, sham neutralisation, selector, embedding, retrieval, API call, score, metric, or thesis result exists.",
        ],
    }
    output = root / "audits" / f"{args.pilot_id}_{args.first_reviewer}_vs_{args.second_reviewer}_route_preservation_decision.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "passed": passed, "status": payload["status"]}, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
