#!/usr/bin/env python3
"""Materialise blinded original-card route-preservation packets for RQ1b-S.

It selects pre-audited primary field-card records, verifies packet-source
hashes again, and exposes only prompt plus anonymous field cards to later
reviewers. It writes no target/sham neutralisation or selector input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PILOT_SOURCES = {
    "FCP-001": "replacement_1",
    "FCP-002": "validated_builder_2",
    "FCP-003": "validated_builder_3",
    "FCP-004": "validated_builder_4",
    "FCP-005": "builder_5",
    "FCP-006": "builder_6",
}
FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def format_card(card: dict) -> str:
    labels = {
        "use_condition": "Use condition",
        "input_precondition": "Input / precondition",
        "output_artifact": "Output artifact",
        "workflow_procedure": "Workflow / procedure",
        "boundary_not_for": "Boundary / not for",
        "dependency_resource": "Dependency / resource",
        "success_verification": "Success / verification",
    }
    lines = []
    for field in FIELDS:
        cell = card[field]
        lines.append(f"{labels[field]}:")
        if cell["status"] == "NOT_STATED":
            lines.append("NOT_STATED")
        else:
            lines.extend(cell["quotes"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pilot-root",
        type=Path,
        default=Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/field_card_pilot_2026-08-28"),
    )
    args = parser.parse_args()
    root = args.pilot_root
    private_records = {row["pilot_id"]: row for row in json.loads((root / "private_lineage_manifest.json").read_text())}
    public_records = []

    for pilot_id, reviewer in PILOT_SOURCES.items():
        family_dir = root / pilot_id
        packet = load_object(family_dir / "field_card_builder_packet.json")
        response = load_object(root / "reviews" / reviewer / f"{pilot_id}.json")
        audit = load_object(root / "audits" / f"{pilot_id}_{reviewer}_literal_audit.json")
        if not audit.get("valid"):
            raise ValueError(f"cannot materialise invalid card response: {pilot_id}:{reviewer}")
        if response.get("pilot_id") != pilot_id:
            raise ValueError(f"response pilot mismatch: {pilot_id}:{reviewer}")

        candidate_cards = {}
        for candidate in packet["candidates"]:
            label = candidate["label"]
            source_path = family_dir / candidate["text_path"]
            if sha256(source_path) != candidate["source_sha256"]:
                raise ValueError(f"source packet hash mismatch: {pilot_id}:{label}")
            card = response.get("cards", {}).get(label)
            if not isinstance(card, dict) or set(card) != set(FIELDS):
                raise ValueError(f"card schema mismatch: {pilot_id}:{reviewer}:{label}")
            candidate_cards[label] = card

        review_packet = {
            "status": "RQ1B_S_ORIGINAL_FIELD_CARD_ROUTE_PRESERVATION_PACKET_NOT_A_RESULT",
            "pilot_id": pilot_id,
            "instructions": [
                "Use only this packet.",
                "Do not inspect any source originals, other workspace files, labels, provenance, reviews, masks, selectors, or results.",
                "Do not use web, external APIs, embeddings, or retrieval.",
                "For each prompt variant, identify all candidates that are fully adequate from the field cards.",
                "Do not force a singleton: if more than one is fully adequate, return all labels.",
                "Quote exact card text supporting each fully adequate candidate and name the primary operational field that drives your judgement.",
                "Return exactly one JSON object to the assigned response path.",
            ],
            "prompts": [
                {"variant": item["prompt_variant"], "text": item["prompt"]}
                for item in private_records[pilot_id]["prompt_lineage"]
            ],
            "candidates": [
                {"label": label, "field_card": format_card(candidate_cards[label])}
                for label in sorted(candidate_cards)
            ],
            "allowed_primary_fields": list(FIELDS) + ["MULTI_FIELD_OR_NONCODEABLE"],
            "required_response_schema": {
                "pilot_id": pilot_id,
                "per_prompt": [
                    {
                        "variant": "direct or paraphrase",
                        "fully_adequate_candidates": ["Candidate A"],
                        "primary_field": "one allowed field or MULTI_FIELD_OR_NONCODEABLE",
                        "evidence": {"Candidate A": ["exact card substring"]},
                        "reason": "brief rationale",
                    }
                ],
            },
        }
        output = family_dir / "original_card_route_preservation_packet.json"
        output.write_text(json.dumps(review_packet, indent=2, sort_keys=True) + "\n")
        public_records.append(
            {
                "pilot_id": pilot_id,
                "selected_card_reviewer": reviewer,
                "candidate_count": len(candidate_cards),
                "prompt_variants": [item["prompt_variant"] for item in private_records[pilot_id]["prompt_lineage"]],
                "packet_path": str(output),
                "status": "READY_FOR_TWO_BLINDED_ORIGINAL_CARD_ROUTE_PRESERVATION_REVIEWS_NOT_A_RESULT",
            }
        )

    (root / "original_card_route_preservation_packet_manifest.json").write_text(
        json.dumps(public_records, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({"pilot_root": str(root), "packet_count": len(public_records)}, sort_keys=True))


if __name__ == "__main__":
    main()
