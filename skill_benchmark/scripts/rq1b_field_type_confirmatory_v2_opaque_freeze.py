"""Freeze and verify opaque RQ1b v2 review inputs before blinded review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


FREEZE_NAME = "opaque_review_input_freeze_amendment_2026-08-29.json"
CONDITION_FREEZE_NAME = "condition_materialisation_freeze_amendment_2026-08-29.json"
MATERIALISED_CARD_STATUSES = {
    "MATERIALISED_FROM_LITERAL_VALID_CARD",
    "MATERIALISED_FROM_LITERAL_SAFE_SURFACE_CUE_REPAIR",
    "MATERIALISED_FROM_FROZEN_CANONICAL_CARD",
}
TRACKED_ROOT_FILES = (
    "canonicalisation_ledger.json",
    "composition_manifest_private.json",
    "routing_family_manifest_private.json",
    "selection_packet_manifest_opaque.json",
    "selection_packet_private_map.json",
    "residual_packet_manifest_opaque.json",
    "residual_packet_private_map.json",
    "audits/opaque_packet_binding_preflight.json",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_list(path: Path) -> list:
    value = json.loads(path.read_text())
    if not isinstance(value, list):
        raise ValueError(f"JSON array required: {path}")
    return value


def snapshot(root: Path) -> dict:
    tracked = {}
    for relative in TRACKED_ROOT_FILES:
        path = root / relative
        if not path.is_file():
            raise ValueError(f"freeze input missing: {relative}")
        tracked[relative] = sha256_file(path)
    binding = json.loads((root / "audits" / "opaque_packet_binding_preflight.json").read_text())
    if binding.get("valid") is not True:
        raise ValueError("opaque packet binding preflight is not valid")
    ledger = json.loads((root / "canonicalisation_ledger.json").read_text())
    compositions = ledger.get("compositions")
    if not isinstance(compositions, list):
        raise ValueError("canonicalisation ledger has no compositions list")
    canonical_hashes = {}
    for entry in compositions:
        if not isinstance(entry, dict):
            raise ValueError("canonicalisation ledger composition entry is invalid")
        composition_id = entry.get("composition_id")
        if not isinstance(composition_id, str):
            raise ValueError("canonicalisation ledger composition id is invalid")
        if entry.get("status") in MATERIALISED_CARD_STATUSES:
            path = root / "canonical_cards" / f"{composition_id}.json"
            if not path.is_file():
                raise ValueError(f"materialised canonical card missing: {composition_id}")
            canonical_hashes[composition_id] = sha256_file(path)
    selection_manifest = load_list(root / "selection_packet_manifest_opaque.json")
    residual_manifest = load_list(root / "residual_packet_manifest_opaque.json")
    selection_hashes, residual_hashes = {}, {}
    for row in selection_manifest:
        packet_id = row.get("packet_id")
        if not isinstance(packet_id, str) or packet_id in selection_hashes:
            raise ValueError("invalid selection manifest packet id")
        selection_hashes[packet_id] = sha256_file(root / "selection_packets_opaque" / f"{packet_id}.json")
    for row in residual_manifest:
        packet_id = row.get("packet_id")
        if not isinstance(packet_id, str) or packet_id in residual_hashes:
            raise ValueError("invalid residual manifest packet id")
        residual_hashes[packet_id] = sha256_file(root / "residual_packets_opaque" / f"{packet_id}.json")
    return {
        "status": "RQ1B_FIELD_TYPE_V2_OPAQUE_REVIEW_INPUT_FREEZE_NOT_A_RESULT",
        "tracked_file_sha256": tracked,
        "canonical_card_file_sha256": canonical_hashes,
        "selection_packet_sha256": selection_hashes,
        "residual_packet_sha256": residual_hashes,
        "selection_packet_count": len(selection_hashes),
        "residual_packet_count": len(residual_hashes),
        "exclusions": [
            "No blinded review, strict-gold comparison, residual judgment, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }


def verify_opaque_core(root: Path) -> dict:
    expected = json.loads((root / FREEZE_NAME).read_text())
    current = snapshot(root)
    expected_core = json.loads(json.dumps(expected))
    current_core = json.loads(json.dumps(current))
    expected_core["tracked_file_sha256"].pop("canonicalisation_ledger.json", None)
    current_core["tracked_file_sha256"].pop("canonicalisation_ledger.json", None)
    if expected_core != current_core:
        raise ValueError("opaque review input core freeze mismatch")
    return current


def verify_freeze(root: Path) -> dict:
    current = verify_opaque_core(root)
    path = root / CONDITION_FREEZE_NAME
    if not path.is_file():
        raise ValueError("condition materialisation freeze amendment missing")
    expected = json.loads(path.read_text())
    if expected != current:
        raise ValueError("condition materialisation freeze mismatch")
    return expected
