#!/usr/bin/env python3
"""Create anonymous source-card-only residual-redundancy review packets."""

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
DISPLAY_NAMES = {
    "use_condition": "Use condition",
    "input_precondition": "Input / precondition",
    "output_artifact": "Output artifact",
    "workflow_procedure": "Workflow / procedure",
    "success_verification": "Success / verification",
    "boundary_not_for": "Boundary / not for",
    "dependency_resource": "Dependency / resource",
}


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def render_card(card: dict) -> str:
    lines = []
    for field in FIELDS:
        cell = card[field]
        lines.append(f"{DISPLAY_NAMES[field]}:")
        lines.extend(cell["quotes"] if cell["status"] == "EVIDENCE" else ["NOT_STATED"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pilot_root
    ledger = load_object(root / "canonicalisation_ledger.json")
    manifest = []
    for entry in ledger.get("families", []):
        if entry.get("status") != "MATERIALISED_FROM_LITERAL_VALID_CARD":
            continue
        pilot_id = entry["pilot_id"]
        cards = load_object(root / "canonical_cards" / f"{pilot_id}.json")["cards"]
        targets = [
            {"candidate": label, "field": field}
            for label, card in sorted(cards.items())
            for field in FIELDS
            if card[field]["status"] == "EVIDENCE" and card[field]["quotes"]
        ]
        packet = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_SOURCE_CARD_ONLY_RESIDUAL_PACKET_NOT_A_RESULT",
            "pilot_id": pilot_id,
            "instructions": [
                "Use only this packet.",
                "Do not inspect any source original, prompt, label, provenance, mask, selector, or result.",
                "Do not use web, external APIs, embeddings, or retrieval.",
                "For every listed candidate-field target, decide whether an operationally equivalent proposition remains in another field of the SAME candidate card.",
                "Use none when no corresponding proposition remains, partial when some but not all of the operational content remains, and substantial when another field substantially restates it.",
                "For partial or substantial, cite exact text from another named card field; for none, return an empty evidence list.",
                "Do not infer a winner or infer from any unstated source content.",
                "Return exactly one JSON object and no prose.",
            ],
            "candidates": [
                {"label": label, "field_card": render_card(card)}
                for label, card in sorted(cards.items())
            ],
            "targets": targets,
            "required_response_schema": {
                "pilot_id": pilot_id,
                "candidate_assessments": [
                    {
                        "candidate": "Candidate A",
                        "field": "one listed target field",
                        "residual_label": "none, partial, or substantial",
                        "remaining_slot_evidence": [{"field": "other field", "quotes": ["exact card substring"]}],
                        "reason": "brief source-card-only rationale",
                    }
                ],
            },
        }
        path = root / "residual_packets" / f"{pilot_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
        manifest.append({"pilot_id": pilot_id, "target_count": len(targets), "packet_path": str(path)})
    output = root / "residual_packet_manifest.json"
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"packet_count": len(manifest), "target_count": sum(item["target_count"] for item in manifest)}, sort_keys=True))


if __name__ == "__main__":
    main()
