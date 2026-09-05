#!/usr/bin/env python3
"""Materialise immutable cards/masks once per validated RQ1b v2 composition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


FIELDS = ("use_condition", "input_precondition", "output_artifact", "workflow_procedure", "success_verification", "boundary_not_for", "dependency_resource")
CONDITIONS = {"FULL": None, "MASK_USE": "use_condition", "MASK_INPUT": "input_precondition", "MASK_OUTPUT": "output_artifact", "MASK_WORKFLOW": "workflow_procedure", "MASK_SUCCESS": "success_verification", "MASK_BOUNDARY": "boundary_not_for", "MASK_DEPENDENCY": "dependency_resource"}
MARKER = "[FIELD WITHHELD IN THIS REPRESENTATION]"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def write_immutable(path: Path, value: object) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text() != text:
            raise ValueError(f"refusing to overwrite non-identical frozen artifact: {path}")
        return
    path.write_text(text)


def literal_valid(root: Path, composition_id: str, reviewer: str) -> bool | None:
    path = root / "audits" / f"{composition_id}_{reviewer}_literal_audit.json"
    return None if not path.is_file() else json.loads(path.read_text()).get("valid") is True


def render(cell: dict) -> str:
    return "NOT_STATED" if cell["status"] == "NOT_STATED" else "\n\n".join(cell["quotes"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    manifest = json.loads((root / "source_card_builder_manifest.json").read_text())
    frozen_compositions = {
        row["composition_id"]
        for row in json.loads((root / "residual_packet_private_map.json").read_text())
        if isinstance(row, dict) and isinstance(row.get("composition_id"), str)
    }
    ledger = []
    for item in manifest:
        composition_id = item["composition_id"]
        if composition_id not in frozen_compositions:
            ledger.append({"composition_id": composition_id, "status": "FROZEN_CANONICAL_NOT_IN_OPAQUE_REVIEW_CORPUS"})
            continue
        canonical_path = root / "canonical_cards" / f"{composition_id}.json"
        if not canonical_path.is_file():
            b1, b2 = literal_valid(root, composition_id, "b1"), literal_valid(root, composition_id, "b2")
            ledger.append({"composition_id": composition_id, "status": "NO_FROZEN_CANONICAL_CARD", "b1_literal_valid": b1, "b2_literal_valid": b2})
            continue
        canonical = json.loads(canonical_path.read_text())
        if canonical.get("composition_id") != composition_id or canonical.get("field_order") != list(FIELDS) or not isinstance(canonical.get("cards"), dict):
            raise ValueError(f"invalid frozen canonical card: {canonical_path}")
        cards = canonical["cards"]
        condition_hashes = {}
        for condition, withheld in CONDITIONS.items():
            payload = {"status": "RQ1B_FIELD_TYPE_ABLATION_V2_CONDITION_NOT_A_RESULT", "composition_id": composition_id, "condition": condition, "withheld_field": withheld, "marker": MARKER if withheld else None, "field_order": list(FIELDS), "cards": [{"label": label, "slots": {field: MARKER if field == withheld else render(cards[label][field]) for field in FIELDS}} for label in sorted(cards)]}
            condition_hashes[condition] = digest(payload)
            write_immutable(root / "conditions" / composition_id / f"{condition}.json", payload)
        ledger.append({"composition_id": composition_id, "status": "MATERIALISED_FROM_FROZEN_CANONICAL_CARD", "canonical_builder": canonical.get("canonical_builder"), "canonical_card_sha256": digest(canonical), "condition_sha256": condition_hashes})
    payload = {"status": "RQ1B_FIELD_TYPE_ABLATION_V2_CONDITION_MATERIALISATION_NOT_A_RESULT", "canonical_rule": "materialise only an existing immutable canonical card that belongs to the frozen opaque review corpus; never rebuild or overwrite it from builder responses", "conditions": list(CONDITIONS), "marker": MARKER, "compositions": ledger, "exclusions": ["No prompt, gold label, selector, embedding, retrieval score, metric, or external transfer is read or created."]}
    path = root / "canonicalisation_ledger.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    counts = {}
    for row in ledger:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
