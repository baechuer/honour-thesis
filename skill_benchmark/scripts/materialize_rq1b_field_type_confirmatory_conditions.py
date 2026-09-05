#!/usr/bin/env python3
"""Create canonical cards and all-candidate masks for valid RQ1b CFTA cards.

This local materialiser uses only builder responses and literal-audit outcomes.
It never reads prompts, strict gold labels, selectors, scores, or external
services. The B1-then-B2 canonicalisation rule is immutable and idempotent.
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


def write_immutable_json(path: Path, payload: object) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text() != encoded:
            raise ValueError(f"refusing to overwrite non-identical frozen artifact: {path}")
        return
    path.write_text(encoded)


def write_progress_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def literal_valid(root: Path, family_id: str, reviewer: str) -> bool | None:
    path = root / "audits" / f"{family_id}_{reviewer}_literal_audit.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text()).get("valid") is True


def rendered_slot(cell: dict) -> str:
    return "NOT_STATED" if cell["status"] == "NOT_STATED" else "\n\n".join(cell["quotes"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    manifest = json.loads((root / "source_card_builder_manifest.json").read_text())
    ledger = []
    for item in manifest:
        family_id = item["family_id"]
        b1 = literal_valid(root, family_id, "b1")
        b2 = literal_valid(root, family_id, "b2")
        selected = "b1" if b1 is True else "b2" if b2 is True else None
        if selected is None:
            status = "NO_LITERAL_VALID_CARD" if b1 is False and b2 is False else "PENDING_LITERAL_AUDITS"
            ledger.append({"family_id": family_id, "status": status, "b1_literal_valid": b1, "b2_literal_valid": b2})
            continue
        response = json.loads((root / "builder_responses" / selected / f"{family_id}.json").read_text())
        cards = response["cards"]
        canonical = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_CANONICAL_SOURCE_CARD_NOT_A_RESULT",
            "family_id": family_id,
            "canonical_builder": selected,
            "field_order": list(FIELDS),
            "cards": cards,
        }
        canonical_text = json.dumps(canonical, sort_keys=True)
        write_immutable_json(root / "canonical_cards" / f"{family_id}.json", canonical)
        condition_hashes = {}
        for condition, withheld_field in CONDITIONS.items():
            rendered_cards = []
            for label in sorted(cards):
                slots = {field: MARKER if field == withheld_field else rendered_slot(cards[label][field]) for field in FIELDS}
                rendered_cards.append({"label": label, "slots": slots})
            payload = {
                "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_CONDITION_NOT_A_RESULT",
                "family_id": family_id,
                "condition": condition,
                "withheld_field": withheld_field,
                "marker": MARKER if withheld_field else None,
                "field_order": list(FIELDS),
                "cards": rendered_cards,
            }
            condition_hashes[condition] = sha256_text(json.dumps(payload, sort_keys=True))
            write_immutable_json(root / "conditions" / family_id / f"{condition}.json", payload)
        ledger.append(
            {
                "family_id": family_id,
                "status": "MATERIALISED_FROM_LITERAL_VALID_CARD",
                "canonical_builder": selected,
                "canonical_card_sha256": sha256_text(canonical_text),
                "condition_sha256": condition_hashes,
            }
        )
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_CONFIRMATORY_CONDITION_MATERIALISATION_NOT_A_RESULT",
        "canonical_rule": "B1 if literal-valid, otherwise B2 if literal-valid, otherwise no card",
        "conditions": list(CONDITIONS),
        "marker": MARKER,
        "families": ledger,
        "exclusions": ["No prompt, gold label, selector, embedding, retrieval score, metric, or external transfer is read or created."],
    }
    # This ledger is explicitly a live construction-progress record. Frozen
    # canonical cards and conditions above remain immutable once materialised.
    write_progress_json(root / "canonicalisation_ledger.json", payload)
    counts = {}
    for item in ledger:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    print(json.dumps({"counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
