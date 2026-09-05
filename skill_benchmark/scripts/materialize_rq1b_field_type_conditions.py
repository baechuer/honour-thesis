#!/usr/bin/env python3
"""Create canonical RQ1b field cards and all-candidate field masks locally.

The script uses only independent builder responses and literal audit outcomes.
It does not read prompts, strict-gold labels, retrieval code, or selector
outputs. Canonical selection is fixed: use B1 when literal-valid; otherwise use
B2 when literal-valid; otherwise mark the family ineligible for materialisation.
"""

from __future__ import annotations

import argparse
import hashlib
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


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def literal_valid(root: Path, pilot_id: str, reviewer: str) -> bool:
    audit_path = root / "audits" / f"{pilot_id}_{reviewer}_literal_audit.json"
    if not audit_path.is_file():
        return False
    audit = json.loads(audit_path.read_text())
    return audit.get("valid") is True


def rendered_slot(cell: dict) -> str:
    if cell["status"] == "NOT_STATED":
        return "NOT_STATED"
    return "\n\n".join(cell["quotes"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pilot_root
    manifest = json.loads((root / "source_card_builder_manifest.json").read_text())
    ledger: list[dict] = []
    for item in manifest:
        pilot_id = item["pilot_id"]
        selected = "b1" if literal_valid(root, pilot_id, "b1") else "b2" if literal_valid(root, pilot_id, "b2") else None
        if selected is None:
            ledger.append({"pilot_id": pilot_id, "status": "NO_LITERAL_VALID_CARD"})
            continue
        response = json.loads((root / "builder_responses" / selected / f"{pilot_id}.json").read_text())
        cards = response["cards"]
        canonical = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_CANONICAL_SOURCE_CARD_NOT_A_RESULT",
            "pilot_id": pilot_id,
            "canonical_builder": selected,
            "field_order": list(FIELDS),
            "cards": cards,
        }
        canonical_text = json.dumps(canonical, sort_keys=True)
        write_json(root / "canonical_cards" / f"{pilot_id}.json", canonical)

        condition_hashes: dict[str, str] = {}
        for condition, withheld_field in CONDITIONS.items():
            rendered_cards = []
            for label in sorted(cards):
                slots = {}
                for field in FIELDS:
                    slots[field] = MARKER if field == withheld_field else rendered_slot(cards[label][field])
                rendered_cards.append({"label": label, "slots": slots})
            condition_payload = {
                "status": "RQ1B_FIELD_TYPE_ABLATION_CONDITION_NOT_A_RESULT",
                "pilot_id": pilot_id,
                "condition": condition,
                "withheld_field": withheld_field,
                "marker": MARKER if withheld_field else None,
                "field_order": list(FIELDS),
                "cards": rendered_cards,
            }
            encoded = json.dumps(condition_payload, sort_keys=True)
            condition_hashes[condition] = sha256_text(encoded)
            write_json(root / "conditions" / pilot_id / f"{condition}.json", condition_payload)
        ledger.append(
            {
                "pilot_id": pilot_id,
                "status": "MATERIALISED_FROM_LITERAL_VALID_CARD",
                "canonical_builder": selected,
                "canonical_card_sha256": sha256_text(canonical_text),
                "condition_sha256": condition_hashes,
            }
        )
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_CONDITION_MATERIALISATION_NOT_A_RESULT",
        "canonical_rule": "B1 if literal-valid, otherwise B2 if literal-valid, otherwise no card",
        "conditions": list(CONDITIONS),
        "marker": MARKER,
        "families": ledger,
        "exclusions": [
            "No prompt, gold label, selector, embedding, retrieval score, metric, or external transfer is read or created.",
        ],
    }
    write_json(root / "canonicalisation_ledger.json", payload)
    print(json.dumps({"materialised": sum(item["status"].startswith("MATERIALISED") for item in ledger), "total": len(ledger)}, sort_keys=True))


if __name__ == "__main__":
    main()
