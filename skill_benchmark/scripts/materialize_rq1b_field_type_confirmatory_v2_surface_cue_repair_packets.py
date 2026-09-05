#!/usr/bin/env python3
"""Prepare source-only remediation packets for pre-review RQ1b v2 card cues."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    canonical_cards,
    load_list,
    load_object,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    preflight = load_object(root / "audits" / "opaque_packet_binding_preflight.json")
    failures = preflight.get("failures")
    if not isinstance(failures, list) or preflight.get("valid") is not False:
        raise ValueError("expected failed surface-cue opaque packet preflight")
    packet_map = {
        row.get("packet_id"): row
        for row in load_list(root / "selection_packet_private_map.json")
        if isinstance(row, dict)
    }
    grouped: dict[str, dict[tuple[str, str], set[str]]] = defaultdict(lambda: defaultdict(set))
    for failure in failures:
        if not isinstance(failure, str) or not failure.startswith("selection_card_surface_cue:"):
            continue
        parts = failure.split(":")
        if len(parts) != 6:
            raise ValueError(f"surface cue failure shape invalid: {failure}")
        _, packet_id, cue, candidate, field, quote_index = parts
        mapping = packet_map.get(packet_id)
        if not isinstance(mapping, dict) or not isinstance(mapping.get("composition_id"), str):
            raise ValueError(f"no private composition binding for packet: {packet_id}")
        if quote_index != "0":
            raise ValueError(f"unexpected cue quote index: {failure}")
        grouped[mapping["composition_id"]][(candidate, field)].add(cue)
    if not grouped:
        raise ValueError("no selection surface-cue remediation targets discovered")
    manifest = []
    for composition_id, target_cues in sorted(grouped.items()):
        cards = canonical_cards(root, composition_id)
        targets = []
        for (candidate, field), cues in sorted(target_cues.items()):
            cell = cards.get(candidate, {}).get(field)
            if not isinstance(cell, dict) or cell.get("status") != "EVIDENCE":
                raise ValueError(f"flagged target lacks evidence: {composition_id}:{candidate}:{field}")
            targets.append(
                {
                    "candidate": candidate,
                    "field": field,
                    "cue_classes": sorted(cues),
                    "current_quotes": cell.get("quotes"),
                }
            )
        packet = {
            "status": "RQ1B_FIELD_TYPE_V2_SOURCE_ONLY_SURFACE_CUE_REPAIR_PACKET_NOT_A_RESULT",
            "composition_id": composition_id,
            "instructions": [
                "Read only this packet and the anonymous Candidate_*.md files in this composition's sources directory.",
                "Do not inspect prompts, gold labels, provenance, masks, selectors, embeddings, retrieval, scores, or results.",
                "For every flagged candidate-field location, return a source-exact contiguous replacement excerpt for the same slot that does not contain a URL, markdown link target, local SKILL.md/README.md reference, or copied markdown heading block.",
                "If no such source-exact replacement exists, return NO_SAFE_ALTERNATIVE for that location.",
                "Do not paraphrase, edit, summarise, or change unflagged fields.",
                "Return exactly one JSON object matching required_response_schema and no prose.",
            ],
            "sources_directory": str(root / composition_id / "sources"),
            "targets": targets,
            "required_response_schema": {
                "composition_id": composition_id,
                "replacements": [
                    {
                        "candidate": "Candidate A",
                        "field": "one flagged field",
                        "replacement": ["one or more exact source substrings"],
                        "reason": "brief source-only rationale",
                    }
                ],
                "no_safe_alternative_value": "NO_SAFE_ALTERNATIVE",
            },
        }
        path = root / "surface_cue_repair_packets" / f"{composition_id}.json"
        write_json(path, packet)
        manifest.append(
            {
                "composition_id": composition_id,
                "target_count": len(targets),
                "packet_path": str(path),
                "status": "READY_FOR_TWO_INDEPENDENT_SOURCE_ONLY_SURFACE_CUE_REPAIR_BUILDERS_NOT_A_RESULT",
            }
        )
    write_json(root / "surface_cue_repair_packet_manifest.json", manifest)
    print({"composition_count": len(manifest), "target_count": sum(row["target_count"] for row in manifest)})


if __name__ == "__main__":
    main()
