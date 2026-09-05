#!/usr/bin/env python3
"""Create anonymous composition-card FULL preservation packets for RQ1b v2."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    canonical_entries,
    canonical_cards,
    composition_rows,
    materialised_composition_ids,
    opaque_packet_id,
    render_card,
    routing_family_rows,
    sha256_file,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    compositions = composition_rows(root)
    families = routing_family_rows(root)
    materialised = materialised_composition_ids(root)
    manifest = []
    private_map = []
    seen_packet_ids = set()

    for family_id, family in sorted(families.items()):
        composition_id = family.get("composition_id")
        if composition_id not in materialised:
            continue
        composition = compositions.get(composition_id)
        if composition is None:
            raise ValueError(f"private composition missing: {family_id}")
        cards = canonical_cards(root, composition_id)
        canonical_sha256 = canonical_entries(root)[composition_id]["canonical_card_sha256"]
        packet_id = opaque_packet_id("sfp", family_id, canonical_sha256)
        if packet_id in seen_packet_ids:
            raise ValueError("opaque selection packet ID collision")
        seen_packet_ids.add(packet_id)
        expected_labels = {candidate["label"] for candidate in composition["private_candidates"]}
        if set(cards) != expected_labels:
            raise ValueError(f"canonical/private label mismatch: {family_id}")
        prompts = sorted(family["prompt_lineage"], key=lambda item: item["prompt_variant"])
        packet = {
            "status": "RQ1B_FIELD_TYPE_V2_BLINDED_FULL_CARD_PRESERVATION_PACKET_NOT_A_RESULT",
            "packet_id": packet_id,
            "instructions": [
                "Use only this packet.",
                "Do not inspect source originals, other workspace files, labels, provenance, masks, selectors, or results.",
                "Do not use web, external APIs, embeddings, or retrieval.",
                "For each prompt, identify every candidate that is fully adequate using only these cards.",
                "Do not force a singleton: use MULTIPLE_ADEQUATE when more than one candidate is fully adequate, or NONE_ADEQUATE when none is fully adequate.",
                "For every selected candidate, cite one or more exact card substrings that support the judgement.",
                "Return exactly one JSON object and no prose.",
            ],
            "prompts": [
                {"variant": item["prompt_variant"], "text": item["prompt"]}
                for item in prompts
            ],
            "candidates": [
                {"label": label, "field_card": render_card(cards[label])}
                for label in sorted(cards)
            ],
            "required_response_schema": {
                "packet_id": packet_id,
                "per_prompt": [
                    {
                        "variant": "direct or paraphrase",
                        "adequacy_outcome": "SINGLETON, MULTIPLE_ADEQUATE, or NONE_ADEQUATE",
                        "fully_adequate_candidates": ["Candidate A"],
                        "evidence": {"Candidate A": ["exact card substring"]},
                        "reason": "brief selection rationale",
                    }
                ],
            },
        }
        path = root / "selection_packets_opaque" / f"{packet_id}.json"
        write_json(path, packet)
        manifest.append(
            {
                "packet_id": packet_id,
                "candidate_count": len(cards),
                "prompt_variants": ["direct", "paraphrase"],
                "packet_path": str(path),
                "status": "READY_FOR_TWO_INDEPENDENT_BLINDED_FULL_CARD_REVIEWS_NOT_A_RESULT",
            }
        )
        private_map.append(
            {
                "packet_id": packet_id,
                "routing_family_id": family_id,
                "composition_id": composition_id,
                "canonical_card_sha256": canonical_sha256,
                "packet_sha256": sha256_file(path),
            }
        )

    output = root / "selection_packet_manifest_opaque.json"
    write_json(output, manifest)
    private_output = root / "selection_packet_private_map.json"
    write_json(private_output, private_map)
    print({"packet_count": len(manifest), "output": str(output), "private_map": str(private_output)})


if __name__ == "__main__":
    main()
