#!/usr/bin/env python3
"""Compare two blind FULL-card selections to sealed RQ1b strict labels.

This is a local representation-preservation gate.  It performs no field
attribution and creates no masked selector result.
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
    private_rows = json.loads((root / "pilot_input_manifest_private.json").read_text())
    private = next((item for item in private_rows if item["pilot_id"] == args.pilot_id), None)
    if private is None:
        raise ValueError(f"private lineage missing: {args.pilot_id}")
    label_by_skill = {item["skill_id"]: item["label"] for item in private["private_candidates"]}
    gold_label = label_by_skill[private["strict_gold_skill_id"]]
    variants = [item["prompt_variant"] for item in private["prompt_lineage"]]
    first_audit = load_object(root / "audits" / f"{args.pilot_id}_{args.first_reviewer}_selection_review_audit.json")
    second_audit = load_object(root / "audits" / f"{args.pilot_id}_{args.second_reviewer}_selection_review_audit.json")
    first = load_object(root / "selection_reviews" / args.first_reviewer / f"{args.pilot_id}.json")
    second = load_object(root / "selection_reviews" / args.second_reviewer / f"{args.pilot_id}.json")
    first_rows = {item.get("variant"): item for item in first.get("per_prompt", [])}
    second_rows = {item.get("variant"): item for item in second.get("per_prompt", [])}
    rows = []
    for variant in variants:
        first_set = first_rows.get(variant, {}).get("fully_adequate_candidates", [])
        second_set = second_rows.get(variant, {}).get("fully_adequate_candidates", [])
        passed = first_set == [gold_label] and second_set == [gold_label]
        rows.append(
            {
                "variant": variant,
                "sealed_gold_label": gold_label,
                "first_fully_adequate_candidates": first_set,
                "second_fully_adequate_candidates": second_set,
                "strict_singleton_preserved": passed,
            }
        )
    reviews_valid = bool(first_audit.get("valid")) and bool(second_audit.get("valid"))
    passed = reviews_valid and all(row["strict_singleton_preserved"] for row in rows)
    payload = {
        "status": (
            "RQ1B_FIELD_TYPE_ABLATION_FULL_CARD_PRESERVATION_PASS_NOT_A_SELECTOR_RESULT"
            if passed
            else "RQ1B_FIELD_TYPE_ABLATION_FULL_CARD_PRESERVATION_FAIL_NOT_A_SELECTOR_RESULT"
        ),
        "pilot_id": args.pilot_id,
        "sealed_gold_label": gold_label,
        "first_reviewer": args.first_reviewer,
        "second_reviewer": args.second_reviewer,
        "both_reviews_schema_valid": reviews_valid,
        "variant_rows": rows,
        "exclusions": [
            "No primary field, masked-field attribution, selector, embedding, retrieval, score, metric, API call, or result exists.",
        ],
    }
    output = root / "audits" / f"{args.pilot_id}_{args.first_reviewer}_vs_{args.second_reviewer}_full_card_preservation.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pilot_id": args.pilot_id, "passed": passed, "status": payload["status"]}, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
