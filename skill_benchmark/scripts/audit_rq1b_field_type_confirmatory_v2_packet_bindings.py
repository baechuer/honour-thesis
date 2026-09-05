#!/usr/bin/env python3
"""Audit opaque v2 review packets before any blinded review is dispatched."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    canonical_cards,
    canonical_entries,
    card_surface_cue_violations,
    composition_rows,
    load_list,
    materialised_composition_ids,
    opaque_packet_id,
    routing_family_rows,
    FIELDS,
    render_card,
    sha256_file,
    write_json,
)


FORBIDDEN_PACKET_KEYS = {
    "routing_family_id",
    "composition_id",
    "strict_gold_skill_id",
    "source_sha256",
    "source_path",
    "packet_original_path",
    "packet_realpath",
    "canonical_source",
    "provenance",
}


def contains_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(key in FORBIDDEN_PACKET_KEYS or contains_forbidden_key(child) for key, child in value.items())
    if isinstance(value, list):
        return any(contains_forbidden_key(item) for item in value)
    return False


def contains_private_value(value: object, forbidden_values: set[str]) -> bool:
    if isinstance(value, str):
        return any(item and item in value for item in forbidden_values)
    if isinstance(value, dict):
        return any(contains_private_value(child, forbidden_values) for child in value.values())
    if isinstance(value, list):
        return any(contains_private_value(item, forbidden_values) for item in value)
    return False


def require_unique_map(rows: list, private_key: str) -> dict[str, dict]:
    output = {}
    for row in rows:
        packet_id = row.get("packet_id") if isinstance(row, dict) else None
        if not isinstance(packet_id, str) or packet_id in output or not isinstance(row.get(private_key), str):
            raise ValueError(f"invalid or duplicate opaque packet map: {private_key}")
        output[packet_id] = row
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    failures = []
    entries = canonical_entries(root)
    compositions = composition_rows(root)
    families = routing_family_rows(root)
    materialised = materialised_composition_ids(root)
    materialised_families = {
        family_id: family
        for family_id, family in families.items()
        if family["composition_id"] in materialised
    }

    selection_manifest = load_list(root / "selection_packet_manifest_opaque.json")
    selection_map = require_unique_map(load_list(root / "selection_packet_private_map.json"), "routing_family_id")
    manifest_ids = {row.get("packet_id") for row in selection_manifest if isinstance(row, dict)}
    mapped_family_ids = {row["routing_family_id"] for row in selection_map.values()}
    if len(selection_map) != len(materialised_families) or mapped_family_ids != set(materialised_families):
        failures.append("selection_private_map_family_set_mismatch")
    if manifest_ids != set(selection_map):
        failures.append("selection_manifest_packet_set_mismatch")
    for packet_id, mapping in selection_map.items():
        family = materialised_families.get(mapping["routing_family_id"])
        if family is None:
            failures.append(f"selection_map_unknown_family:{packet_id}")
            continue
        composition_id = family["composition_id"]
        expected_hash = entries[composition_id].get("canonical_card_sha256")
        if mapping.get("composition_id") != composition_id or mapping.get("canonical_card_sha256") != expected_hash:
            failures.append(f"selection_map_canonical_binding_mismatch:{packet_id}")
        if packet_id != opaque_packet_id("sfp", mapping["routing_family_id"], expected_hash):
            failures.append(f"selection_opaque_id_mismatch:{packet_id}")
        try:
            cards = canonical_cards(root, composition_id)
            expected_labels = {candidate["label"] for candidate in compositions[composition_id]["private_candidates"]}
            if set(cards) != expected_labels:
                failures.append(f"selection_card_label_binding_mismatch:{packet_id}")
            for violation in card_surface_cue_violations(cards):
                failures.append(f"selection_card_surface_cue:{packet_id}:{violation}")
        except Exception as error:
            failures.append(f"selection_canonical_validation_error:{packet_id}:{error}")
        path = root / "selection_packets_opaque" / f"{packet_id}.json"
        if not path.is_file() or mapping.get("packet_sha256") != sha256_file(path):
            failures.append(f"selection_packet_hash_mismatch:{packet_id}")
            continue
        import json
        packet = json.loads(path.read_text())
        if packet.get("packet_id") != packet_id or contains_forbidden_key(packet):
            failures.append(f"selection_packet_identity_leak_or_mismatch:{packet_id}")
        expected_cards = canonical_cards(root, composition_id)
        expected_prompts = [
            {"variant": item["prompt_variant"], "text": item["prompt"]}
            for item in sorted(family["prompt_lineage"], key=lambda item: item["prompt_variant"])
        ]
        expected_candidates = [
            {"label": label, "field_card": render_card(expected_cards[label])}
            for label in sorted(expected_cards)
        ]
        if packet.get("prompts") != expected_prompts or packet.get("candidates") != expected_candidates:
            failures.append(f"selection_packet_content_binding_mismatch:{packet_id}")
        private_values = {
            mapping["routing_family_id"],
            composition_id,
            family["strict_gold_skill_id"],
            *{
                value
                for candidate in compositions[composition_id]["private_candidates"]
                for value in (
                    candidate.get("skill_id"),
                    candidate.get("source_sha256"),
                    candidate.get("canonical_source", {}).get("packet_original_path"),
                    candidate.get("canonical_source", {}).get("packet_realpath"),
                )
                if isinstance(value, str)
            },
        }
        if contains_private_value(packet, private_values):
            failures.append(f"selection_packet_private_value_leak:{packet_id}")
        if {item.get("variant") for item in packet.get("prompts", [])} != {"direct", "paraphrase"}:
            failures.append(f"selection_packet_variant_mismatch:{packet_id}")
        if len(packet.get("candidates", [])) not in {3, 4}:
            failures.append(f"selection_packet_candidate_count_mismatch:{packet_id}")

    residual_manifest = load_list(root / "residual_packet_manifest_opaque.json")
    residual_map = require_unique_map(load_list(root / "residual_packet_private_map.json"), "composition_id")
    residual_manifest_ids = {row.get("packet_id") for row in residual_manifest if isinstance(row, dict)}
    mapped_composition_ids = {row["composition_id"] for row in residual_map.values()}
    if len(residual_map) != len(materialised) or mapped_composition_ids != materialised:
        failures.append("residual_private_map_composition_set_mismatch")
    if residual_manifest_ids != set(residual_map):
        failures.append("residual_manifest_packet_set_mismatch")
    for packet_id, mapping in residual_map.items():
        composition_id = mapping["composition_id"]
        expected_hash = entries[composition_id].get("canonical_card_sha256")
        if mapping.get("canonical_card_sha256") != expected_hash:
            failures.append(f"residual_map_canonical_binding_mismatch:{packet_id}")
        if packet_id != opaque_packet_id("rrp", composition_id, expected_hash):
            failures.append(f"residual_opaque_id_mismatch:{packet_id}")
        try:
            cards = canonical_cards(root, composition_id)
            for violation in card_surface_cue_violations(cards):
                failures.append(f"residual_card_surface_cue:{packet_id}:{violation}")
        except Exception as error:
            failures.append(f"residual_canonical_validation_error:{packet_id}:{error}")
        path = root / "residual_packets_opaque" / f"{packet_id}.json"
        if not path.is_file() or mapping.get("packet_sha256") != sha256_file(path):
            failures.append(f"residual_packet_hash_mismatch:{packet_id}")
            continue
        import json
        packet = json.loads(path.read_text())
        if packet.get("packet_id") != packet_id or contains_forbidden_key(packet):
            failures.append(f"residual_packet_identity_leak_or_mismatch:{packet_id}")
        expected_cards = canonical_cards(root, composition_id)
        expected_candidates = [
            {"label": label, "field_card": render_card(expected_cards[label])}
            for label in sorted(expected_cards)
        ]
        expected_targets = [
            {"candidate": label, "field": field}
            for label, card in sorted(expected_cards.items())
            for field in FIELDS
            if card[field]["status"] == "EVIDENCE" and card[field]["quotes"]
        ]
        if packet.get("candidates") != expected_candidates or packet.get("targets") != expected_targets:
            failures.append(f"residual_packet_content_binding_mismatch:{packet_id}")
        private_values = {
            composition_id,
            *{
                value
                for candidate in compositions[composition_id]["private_candidates"]
                for value in (
                    candidate.get("skill_id"),
                    candidate.get("source_sha256"),
                    candidate.get("canonical_source", {}).get("packet_original_path"),
                    candidate.get("canonical_source", {}).get("packet_realpath"),
                )
                if isinstance(value, str)
            },
        }
        if contains_private_value(packet, private_values):
            failures.append(f"residual_packet_private_value_leak:{packet_id}")

    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_OPAQUE_PACKET_BINDING_PREFLIGHT_NOT_A_RESULT",
        "valid": not failures,
        "selection_packet_count": len(selection_map),
        "residual_packet_count": len(residual_map),
        "failures": failures,
        "exclusions": [
            "No blinded review, strict-gold comparison, residual judgment, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    output = root / "audits" / "opaque_packet_binding_preflight.json"
    write_json(output, payload)
    print({"valid": payload["valid"], "selection_packet_count": len(selection_map), "residual_packet_count": len(residual_map)})
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
