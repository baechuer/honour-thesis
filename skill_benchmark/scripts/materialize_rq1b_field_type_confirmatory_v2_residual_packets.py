#!/usr/bin/env python3
"""Create anonymous source-card-only residual-redundancy packets for RQ1b v2."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    FIELDS,
    canonical_entries,
    canonical_cards,
    materialised_composition_ids,
    opaque_packet_id,
    render_card,
    sha256_file,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    manifest = []
    private_map = []
    seen_packet_ids = set()
    for composition_id in sorted(materialised_composition_ids(root)):
        cards = canonical_cards(root, composition_id)
        canonical_sha256 = canonical_entries(root)[composition_id]["canonical_card_sha256"]
        packet_id = opaque_packet_id("rrp", composition_id, canonical_sha256)
        if packet_id in seen_packet_ids:
            raise ValueError("opaque residual packet ID collision")
        seen_packet_ids.add(packet_id)
        targets = [
            {"candidate": label, "field": field}
            for label, card in sorted(cards.items())
            for field in FIELDS
            if card[field]["status"] == "EVIDENCE" and card[field]["quotes"]
        ]
        packet = {
            "status": "RQ1B_FIELD_TYPE_V2_SOURCE_CARD_ONLY_RESIDUAL_PACKET_NOT_A_RESULT",
            "packet_id": packet_id,
            "instructions": [
                "Use only this packet.",
                "Do not inspect source originals, prompts, labels, provenance, masks, selectors, or results.",
                "Do not use web, external APIs, embeddings, or retrieval.",
                "For every listed candidate-field target, decide whether an operationally equivalent proposition remains in another field of the SAME candidate card.",
                "Use none when no corresponding proposition remains, partial when some but not all of the operational content remains, and substantial when another field substantially restates it.",
                "For partial or substantial, cite exact text from another named card field; for none, return an empty remaining_slot_evidence list.",
                "Do not infer a winner or use unstated source content.",
                "Return exactly one JSON object and no prose.",
            ],
            "candidates": [
                {"label": label, "field_card": render_card(card)}
                for label, card in sorted(cards.items())
            ],
            "targets": targets,
            "required_response_schema": {
                "packet_id": packet_id,
                "candidate_assessments": [
                    {
                        "candidate": "Candidate A",
                        "field": "one listed target field",
                        "residual_label": "none, partial, or substantial",
                        "remaining_slot_evidence": [
                            {"field": "a different field", "quotes": ["exact card substring"]}
                        ],
                        "reason": "brief source-card-only rationale",
                    }
                ],
            },
        }
        path = root / "residual_packets_opaque" / f"{packet_id}.json"
        write_json(path, packet)
        manifest.append(
            {
                "packet_id": packet_id,
                "target_count": len(targets),
                "packet_path": str(path),
                "status": "READY_FOR_TWO_INDEPENDENT_SOURCE_CARD_ONLY_RESIDUAL_REVIEWS_NOT_A_RESULT",
            }
        )
        private_map.append(
            {
                "packet_id": packet_id,
                "composition_id": composition_id,
                "canonical_card_sha256": canonical_sha256,
                "packet_sha256": sha256_file(path),
            }
        )
    output = root / "residual_packet_manifest_opaque.json"
    write_json(output, manifest)
    private_output = root / "residual_packet_private_map.json"
    write_json(private_output, private_map)
    print(
        {
            "packet_count": len(manifest),
            "target_count": sum(item["target_count"] for item in manifest),
            "private_map": str(private_output),
        }
    )


if __name__ == "__main__":
    main()
