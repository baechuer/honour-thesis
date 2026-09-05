#!/usr/bin/env python3
"""Mechanically audit one-mask-per-field RQ1b v2 composition conditions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = ("use_condition", "input_precondition", "output_artifact", "workflow_procedure", "success_verification", "boundary_not_for", "dependency_resource")
CONDITIONS = {"FULL": None, "MASK_USE": "use_condition", "MASK_INPUT": "input_precondition", "MASK_OUTPUT": "output_artifact", "MASK_WORKFLOW": "workflow_procedure", "MASK_SUCCESS": "success_verification", "MASK_BOUNDARY": "boundary_not_for", "MASK_DEPENDENCY": "dependency_resource"}
MARKER = "[FIELD WITHHELD IN THIS REPRESENTATION]"


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    ledger = load(root / "canonicalisation_ledger.json")
    results = []
    for entry in ledger.get("compositions", []):
        if entry.get("status") != "MATERIALISED_FROM_FROZEN_CANONICAL_CARD":
            continue
        composition_id = entry["composition_id"]
        folder = root / "conditions" / composition_id
        failures = []
        full = load(folder / "FULL.json")
        full_cards = full.get("cards") if isinstance(full.get("cards"), list) else []
        labels = [card.get("label") for card in full_cards if isinstance(card, dict)]
        if len(labels) != len(full_cards) or len(set(labels)) != len(labels):
            failures.append("full_labels_invalid")
        if full.get("composition_id") != composition_id or full.get("condition") != "FULL" or full.get("withheld_field") is not None or full.get("marker") is not None or full.get("field_order") != list(FIELDS):
            failures.append("full_metadata_invalid")
        full_by_label = {card.get("label"): card.get("slots") for card in full_cards if isinstance(card, dict) and isinstance(card.get("slots"), dict)}
        if set(full_by_label) != set(labels):
            failures.append("full_slots_invalid")
        for label, slots in full_by_label.items():
            if set(slots) != set(FIELDS) or any(value == MARKER for value in slots.values()):
                failures.append(f"full_slot_invalid:{label}")
        per_condition = []
        for condition, withheld in CONDITIONS.items():
            if condition == "FULL":
                continue
            payload = load(folder / f"{condition}.json")
            condition_failures = []
            if payload.get("composition_id") != composition_id or payload.get("condition") != condition or payload.get("withheld_field") != withheld or payload.get("marker") != MARKER or payload.get("field_order") != list(FIELDS):
                condition_failures.append("metadata_mismatch")
            cards = payload.get("cards") if isinstance(payload.get("cards"), list) else []
            if [card.get("label") for card in cards if isinstance(card, dict)] != labels:
                condition_failures.append("candidate_order_or_set_mismatch")
            marker_count = 0
            for card in cards:
                label, slots = (card.get("label"), card.get("slots")) if isinstance(card, dict) else (None, None)
                if label not in full_by_label or not isinstance(slots, dict) or set(slots) != set(FIELDS):
                    condition_failures.append(f"slot_schema_invalid:{label}")
                    continue
                for field in FIELDS:
                    expected = MARKER if field == withheld else full_by_label[label][field]
                    if slots[field] != expected:
                        condition_failures.append(f"unexpected_slot_value:{label}:{field}")
                    if slots[field] == MARKER:
                        marker_count += 1
            if marker_count != len(labels):
                condition_failures.append(f"marker_count:{marker_count}:expected:{len(labels)}")
            failures.extend(f"{condition}:{failure}" for failure in condition_failures)
            per_condition.append({"condition": condition, "valid": not condition_failures, "failures": condition_failures})
        result = {"status": "RQ1B_FIELD_TYPE_ABLATION_V2_MASK_MECHANICS_AUDIT_NOT_A_RESULT", "composition_id": composition_id, "valid": not failures, "candidate_count": len(labels), "condition_count": len(CONDITIONS), "failures": failures, "per_condition": per_condition}
        (root / "audits").mkdir(exist_ok=True)
        (root / "audits" / f"{composition_id}_mask_mechanics_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        results.append(result)
    summary = {"status": "RQ1B_FIELD_TYPE_ABLATION_V2_MASK_MECHANICS_AUDIT_SUMMARY_NOT_A_RESULT", "compositions_audited": len(results), "compositions_valid": sum(row["valid"] for row in results), "compositions": [{"composition_id": row["composition_id"], "valid": row["valid"], "failures": row["failures"]} for row in results]}
    (root / "audits" / "mask_mechanics_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"compositions_audited": summary["compositions_audited"], "compositions_valid": summary["compositions_valid"]}, sort_keys=True))
    if summary["compositions_valid"] != summary["compositions_audited"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
