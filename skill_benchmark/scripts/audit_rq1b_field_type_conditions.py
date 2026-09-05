#!/usr/bin/env python3
"""Mechanically validate RQ1b field-type ablation conditions.

This local audit confirms that each all-candidate mask replaces exactly one
named card slot with the same marker while preserving every other rendered
slot byte-for-byte.  It never reads prompts, gold labels, selectors, scores,
or external services.
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
CONDITIONS = {
    "FULL": None,
    "MASK_USE": "use_condition",
    "MASK_INPUT": "input_precondition",
    "MASK_OUTPUT": "output_artifact",
    "MASK_WORKFLOW": "workflow_procedure",
    "MASK_SUCCESS": "success_verification",
    "MASK_BOUNDARY": "boundary_not_for",
    "MASK_DEPENDENCY": "dependency_resource",
}
MARKER = "[FIELD WITHHELD IN THIS REPRESENTATION]"


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pilot_root
    ledger = load_object(root / "canonicalisation_ledger.json")
    materialised = [
        item for item in ledger.get("families", [])
        if item.get("status") == "MATERIALISED_FROM_LITERAL_VALID_CARD"
    ]
    results = []

    for entry in materialised:
        pilot_id = entry["pilot_id"]
        family_dir = root / "conditions" / pilot_id
        failures: list[str] = []
        try:
            full = load_object(family_dir / "FULL.json")
        except Exception as error:
            full = {}
            failures.append(f"full_load_error:{error}")

        full_cards = full.get("cards") if isinstance(full.get("cards"), list) else []
        labels = [card.get("label") for card in full_cards if isinstance(card, dict)]
        if len(labels) != len(full_cards) or len(set(labels)) != len(labels):
            failures.append("full_labels_invalid")
        if full.get("pilot_id") != pilot_id:
            failures.append("full_pilot_id_mismatch")
        if full.get("condition") != "FULL" or full.get("withheld_field") is not None or full.get("marker") is not None:
            failures.append("full_metadata_invalid")
        if full.get("field_order") != list(FIELDS):
            failures.append("full_field_order_invalid")

        full_by_label = {
            card.get("label"): card.get("slots")
            for card in full_cards
            if isinstance(card, dict) and isinstance(card.get("slots"), dict)
        }
        if set(full_by_label) != set(labels):
            failures.append("full_slots_invalid")
        for label, slots in full_by_label.items():
            if set(slots) != set(FIELDS):
                failures.append(f"full_slot_schema_invalid:{label}")
            if any(value == MARKER for value in slots.values()):
                failures.append(f"full_contains_marker:{label}")

        per_condition = []
        for condition, withheld_field in CONDITIONS.items():
            path = family_dir / f"{condition}.json"
            if not path.is_file():
                failures.append(f"missing_condition:{condition}")
                continue
            if condition == "FULL":
                continue
            try:
                payload = load_object(path)
            except Exception as error:
                failures.append(f"condition_load_error:{condition}:{error}")
                continue
            condition_failures: list[str] = []
            if payload.get("pilot_id") != pilot_id:
                condition_failures.append("pilot_id_mismatch")
            if payload.get("condition") != condition:
                condition_failures.append("condition_name_mismatch")
            if payload.get("withheld_field") != withheld_field:
                condition_failures.append("withheld_field_mismatch")
            if payload.get("marker") != MARKER:
                condition_failures.append("marker_metadata_mismatch")
            if payload.get("field_order") != list(FIELDS):
                condition_failures.append("field_order_mismatch")
            cards = payload.get("cards") if isinstance(payload.get("cards"), list) else []
            current_labels = [card.get("label") for card in cards if isinstance(card, dict)]
            if current_labels != labels:
                condition_failures.append("candidate_order_or_set_mismatch")
            marker_count = 0
            for card in cards:
                if not isinstance(card, dict):
                    condition_failures.append("card_not_object")
                    continue
                label = card.get("label")
                slots = card.get("slots")
                if label not in full_by_label or not isinstance(slots, dict) or set(slots) != set(FIELDS):
                    condition_failures.append(f"slot_schema_invalid:{label}")
                    continue
                for field in FIELDS:
                    actual = slots[field]
                    expected = MARKER if field == withheld_field else full_by_label[label][field]
                    if actual != expected:
                        condition_failures.append(f"unexpected_slot_value:{label}:{field}")
                    if actual == MARKER:
                        marker_count += 1
            if marker_count != len(labels):
                condition_failures.append(f"marker_count:{marker_count}:expected:{len(labels)}")
            failures.extend(f"{condition}:{failure}" for failure in condition_failures)
            per_condition.append({"condition": condition, "valid": not condition_failures, "failures": condition_failures})

        result = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_MASK_MECHANICS_AUDIT_NOT_A_RESULT",
            "pilot_id": pilot_id,
            "valid": not failures,
            "candidate_count": len(labels),
            "condition_count": len(CONDITIONS),
            "failures": failures,
            "per_condition": per_condition,
            "exclusions": [
                "No prompt, gold label, selector, embedding, retrieval, score, metric, API call, or result is read or created.",
            ],
        }
        output = root / "audits" / f"{pilot_id}_mask_mechanics_audit.json"
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        results.append(result)

    summary = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_MASK_MECHANICS_AUDIT_SUMMARY_NOT_A_RESULT",
        "families_audited": len(results),
        "families_valid": sum(item["valid"] for item in results),
        "families": [
            {"pilot_id": item["pilot_id"], "valid": item["valid"], "failures": item["failures"]}
            for item in results
        ],
    }
    output = root / "audits" / "mask_mechanics_audit_summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"families_audited": summary["families_audited"], "families_valid": summary["families_valid"]}, sort_keys=True))
    if summary["families_valid"] != summary["families_audited"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
