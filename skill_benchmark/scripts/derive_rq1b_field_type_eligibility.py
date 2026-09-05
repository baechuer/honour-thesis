#!/usr/bin/env python3
"""Derive the sealed-label RQ1b per-field eligibility ledger locally.

Eligibility is a representation-coverage predicate only: the gold card must
contain source evidence for a field and at least one wrong card must render a
different value for it.  This does not score a selector or infer a field's
causal importance.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def rendered_value(cell: dict) -> str:
    return json.dumps({"status": cell["status"], "quotes": cell["quotes"]}, sort_keys=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pilot_root
    ledger = load_object(root / "canonicalisation_ledger.json")
    private_rows = json.loads((root / "pilot_input_manifest_private.json").read_text())
    private_by_id = {item["pilot_id"]: item for item in private_rows}
    families = []

    for entry in ledger.get("families", []):
        if entry.get("status") != "MATERIALISED_FROM_LITERAL_VALID_CARD":
            continue
        pilot_id = entry["pilot_id"]
        private = private_by_id[pilot_id]
        label_by_skill = {item["skill_id"]: item["label"] for item in private["private_candidates"]}
        gold_label = label_by_skill[private["strict_gold_skill_id"]]
        cards = load_object(root / "canonical_cards" / f"{pilot_id}.json")["cards"]
        gold_card = cards[gold_label]
        rows = []
        for field in FIELDS:
            gold_cell = gold_card[field]
            has_gold_evidence = gold_cell["status"] == "EVIDENCE" and bool(gold_cell["quotes"])
            gold_value = rendered_value(gold_cell)
            different_wrong_labels = [
                label for label, card in sorted(cards.items())
                if label != gold_label and rendered_value(card[field]) != gold_value
            ]
            rows.append(
                {
                    "field": field,
                    "gold_has_nonmarker_source_evidence": has_gold_evidence,
                    "wrong_candidates_with_different_value": different_wrong_labels,
                    "eligible": has_gold_evidence and bool(different_wrong_labels),
                }
            )
        families.append(
            {
                "pilot_id": pilot_id,
                "sealed_gold_label": gold_label,
                "candidate_count": len(cards),
                "field_rows": rows,
            }
        )

    totals = {
        field: sum(
            row["eligible"]
            for family in families
            for row in family["field_rows"]
            if row["field"] == field
        )
        for field in FIELDS
    }
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_ELIGIBILITY_LEDGER_NOT_A_RESULT",
        "families": families,
        "eligible_counts_by_field": totals,
        "exclusions": [
            "No prompt selection, mask effect, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    output = root / "audits" / "field_eligibility_ledger.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"family_count": len(families), "eligible_counts_by_field": totals}, sort_keys=True))


if __name__ == "__main__":
    main()
