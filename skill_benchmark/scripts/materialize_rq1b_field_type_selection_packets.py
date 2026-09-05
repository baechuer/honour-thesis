#!/usr/bin/env python3
"""Create anonymous FULL-card preservation packets for the RQ1b pilot.

The private lineage is consulted only to obtain the already-frozen direct and
paraphrase prompts.  Output packets contain neither strict labels, source
paths, source identities, historical field locks, masks, nor selector data.
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
    lines: list[str] = []
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
    private_rows = json.loads((root / "pilot_input_manifest_private.json").read_text())
    private_by_id = {item["pilot_id"]: item for item in private_rows}
    public_manifest: list[dict] = []

    for entry in ledger.get("families", []):
        if entry.get("status") != "MATERIALISED_FROM_LITERAL_VALID_CARD":
            continue
        pilot_id = entry["pilot_id"]
        private = private_by_id.get(pilot_id)
        if private is None:
            raise ValueError(f"private lineage missing: {pilot_id}")
        prompts = private.get("prompt_lineage", [])
        variants = {item.get("prompt_variant") for item in prompts}
        if variants != {"direct", "paraphrase"}:
            raise ValueError(f"direct/paraphrase pair missing: {pilot_id}")
        canonical = load_object(root / "canonical_cards" / f"{pilot_id}.json")
        cards = canonical.get("cards")
        if not isinstance(cards, dict) or not cards:
            raise ValueError(f"canonical cards missing: {pilot_id}")
        for label, card in cards.items():
            if not isinstance(card, dict) or set(card) != set(FIELDS):
                raise ValueError(f"canonical card schema invalid: {pilot_id}:{label}")

        packet = {
            "status": "RQ1B_FIELD_TYPE_ABLATION_BLINDED_FULL_CARD_PRESERVATION_PACKET_NOT_A_RESULT",
            "pilot_id": pilot_id,
            "instructions": [
                "Use only this packet.",
                "Do not inspect source originals, other workspace files, labels, provenance, historical field assignments, masks, selectors, or results.",
                "Do not use web, external APIs, embeddings, or retrieval.",
                "For each prompt, identify every candidate that is fully adequate using only these cards.",
                "Do not force a singleton: return more than one label when more than one candidate is fully adequate.",
                "For every selected candidate, cite one or more exact card substrings that support the judgement.",
                "Return exactly one JSON object to the assigned response path and no prose.",
            ],
            "prompts": [
                {"variant": item["prompt_variant"], "text": item["prompt"]}
                for item in sorted(prompts, key=lambda item: item["prompt_variant"])
            ],
            "candidates": [
                {"label": label, "field_card": render_card(cards[label])}
                for label in sorted(cards)
            ],
            "required_response_schema": {
                "pilot_id": pilot_id,
                "per_prompt": [
                    {
                        "variant": "direct or paraphrase",
                        "fully_adequate_candidates": ["Candidate A"],
                        "evidence": {"Candidate A": ["exact card substring"]},
                        "reason": "brief selection rationale",
                    }
                ],
            },
        }
        packet_path = root / "selection_packets" / f"{pilot_id}.json"
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
        public_manifest.append(
            {
                "pilot_id": pilot_id,
                "candidate_count": len(cards),
                "prompt_variants": ["direct", "paraphrase"],
                "packet_path": str(packet_path),
                "status": "READY_FOR_TWO_INDEPENDENT_BLINDED_FULL_CARD_REVIEWS_NOT_A_RESULT",
            }
        )

    output = root / "selection_packet_manifest.json"
    output.write_text(json.dumps(public_manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"packet_count": len(public_manifest), "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
