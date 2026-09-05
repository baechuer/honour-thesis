#!/usr/bin/env python3
"""Apply sealed eligibility to two blinded RQ1b residual reviews locally."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def exact_cross_slot_reuse(card: dict, target_field: str) -> bool:
    target_quotes = set(card[target_field]["quotes"])
    return bool(target_quotes) and any(
        target_quotes.intersection(cell["quotes"])
        for field, cell in card.items()
        if field != target_field
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--first-reviewer", required=True)
    parser.add_argument("--second-reviewer", required=True)
    parser.add_argument("--reviewer-map", type=Path)
    args = parser.parse_args()
    root = args.pilot_root
    eligibility = load_object(root / "audits" / "field_eligibility_ledger.json")
    reviewer_map = load_object(args.reviewer_map).get("families", {}) if args.reviewer_map else {}
    rows = []
    invalid_reviews = []
    for family in eligibility["families"]:
        pilot_id = family["pilot_id"]
        selected = reviewer_map.get(pilot_id, {})
        first_reviewer = selected.get("first_reviewer", args.first_reviewer)
        second_reviewer = selected.get("second_reviewer", args.second_reviewer)
        first_audit = load_object(root / "audits" / f"{pilot_id}_{first_reviewer}_residual_review_audit.json")
        second_audit = load_object(root / "audits" / f"{pilot_id}_{second_reviewer}_residual_review_audit.json")
        if not first_audit.get("valid") or not second_audit.get("valid"):
            invalid_reviews.append(pilot_id)
            continue
        first = load_object(root / "residual_reviews" / first_reviewer / f"{pilot_id}.json")
        second = load_object(root / "residual_reviews" / second_reviewer / f"{pilot_id}.json")
        first_by_key = {(item["candidate"], item["field"]): item for item in first["candidate_assessments"]}
        second_by_key = {(item["candidate"], item["field"]): item for item in second["candidate_assessments"]}
        card = load_object(root / "canonical_cards" / f"{pilot_id}.json")["cards"][family["sealed_gold_label"]]
        for field_row in family["field_rows"]:
            if not field_row["eligible"]:
                continue
            key = (family["sealed_gold_label"], field_row["field"])
            first_label = first_by_key[key]["residual_label"]
            second_label = second_by_key[key]["residual_label"]
            consensus = first_label if first_label == second_label else "disagreed"
            rows.append(
                {
                    "pilot_id": pilot_id,
                    "sealed_gold_label": family["sealed_gold_label"],
                    "field": field_row["field"],
                    "first_residual_label": first_label,
                    "second_residual_label": second_label,
                    "first_reviewer": first_reviewer,
                    "second_reviewer": second_reviewer,
                    "residual_consensus": consensus,
                    "exact_cross_slot_quote_reuse": exact_cross_slot_reuse(card, field_row["field"]),
                }
            )
    complete = not invalid_reviews
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_RESIDUAL_REDUNDANCY_LEDGER_NOT_A_RESULT",
        "first_reviewer": args.first_reviewer,
        "second_reviewer": args.second_reviewer,
        "review_audits_complete": complete,
        "families_with_invalid_review": invalid_reviews,
        "eligible_gold_field_rows": rows,
        "summary": {
            "eligible_row_count": len(rows),
            "none": sum(row["residual_consensus"] == "none" for row in rows),
            "partial": sum(row["residual_consensus"] == "partial" for row in rows),
            "substantial": sum(row["residual_consensus"] == "substantial" for row in rows),
            "disagreed": sum(row["residual_consensus"] == "disagreed" for row in rows),
        },
        "exclusions": [
            "No field attribution, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    output = root / "audits" / "residual_redundancy_ledger.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"review_audits_complete": complete, **payload["summary"]}, sort_keys=True))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
