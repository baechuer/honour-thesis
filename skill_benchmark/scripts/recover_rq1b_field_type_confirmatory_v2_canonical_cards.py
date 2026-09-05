#!/usr/bin/env python3
"""Restore unchanged active RQ1b v2 cards after the surface-cue amendment."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import canonical_json_digest, load_object, write_json


ARCHIVE_NAME = "quarantine_pre_surface_cue_amendment_2026-08-29"
ORIGINAL_STATUS = "MATERIALISED_FROM_LITERAL_VALID_CARD"
REPAIRED_STATUS = "MATERIALISED_FROM_LITERAL_SAFE_SURFACE_CUE_REPAIR"
RECOVERY_NAME = "canonical_card_recovery_after_surface_cue_amendment_2026-08-29.json"


def card_digest(path: Path) -> str:
    return canonical_json_digest(load_object(path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    archive = root / ARCHIVE_NAME
    recovery_path = root / RECOVERY_NAME
    if recovery_path.exists():
        raise ValueError(f"canonical-card recovery already recorded: {recovery_path}")
    current = load_object(root / "canonicalisation_ledger.json")
    original = load_object(archive / "canonicalisation_ledger.json")
    current_entries = {entry.get("composition_id"): entry for entry in current.get("compositions", []) if isinstance(entry, dict)}
    original_entries = {entry.get("composition_id"): entry for entry in original.get("compositions", []) if isinstance(entry, dict)}
    if not current_entries or set(current_entries) != set(original_entries):
        raise ValueError("current and archived composition ledgers do not have the same ids")

    active_cards = root / "canonical_cards"
    archived_cards = archive / "canonical_cards"
    restored, repaired_verified, excluded_verified = [], [], []
    expected_active = set()
    for composition_id, old_entry in sorted(original_entries.items()):
        old_status = old_entry.get("status")
        new_entry = current_entries[composition_id]
        old_path = archived_cards / f"{composition_id}.json"
        new_path = active_cards / f"{composition_id}.json"
        if old_status != ORIGINAL_STATUS:
            if new_path.exists():
                raise ValueError(f"non-materialised composition unexpectedly has active card: {composition_id}")
            continue
        old_digest = card_digest(old_path)
        if old_digest != old_entry.get("canonical_card_sha256"):
            raise ValueError(f"archived canonical-card hash mismatch: {composition_id}")
        new_status = new_entry.get("status")
        if new_status == ORIGINAL_STATUS:
            if new_entry.get("canonical_card_sha256") != old_digest:
                raise ValueError(f"unchanged ledger/card hash mismatch: {composition_id}")
            if new_path.exists():
                raise ValueError(f"unchanged active card unexpectedly exists before recovery: {composition_id}")
            shutil.copy2(old_path, new_path)
            if card_digest(new_path) != old_digest:
                raise ValueError(f"restored canonical-card hash mismatch: {composition_id}")
            restored.append({"composition_id": composition_id, "canonical_card_sha256": old_digest})
            expected_active.add(composition_id)
        elif new_status == REPAIRED_STATUS:
            if not new_path.is_file() or card_digest(new_path) != new_entry.get("canonical_card_sha256"):
                raise ValueError(f"repaired canonical-card hash mismatch: {composition_id}")
            repaired_verified.append({"composition_id": composition_id, "canonical_card_sha256": card_digest(new_path)})
            expected_active.add(composition_id)
        elif new_status == "EXCLUDED_NO_LITERAL_SAFE_REPAIR":
            if new_path.exists():
                raise ValueError(f"strictly excluded composition unexpectedly has active card: {composition_id}")
            excluded_verified.append(composition_id)
        else:
            raise ValueError(f"unexpected amended status for original materialised card: {composition_id}:{new_status}")
    actual_active = {path.stem for path in active_cards.glob("*.json")}
    if actual_active != expected_active:
        raise ValueError("active canonical-card set does not match amended materialised set")
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_CANONICAL_CARD_RECOVERY_NOT_A_RESULT",
        "restored_unchanged_count": len(restored),
        "repaired_verified_count": len(repaired_verified),
        "excluded_verified_count": len(excluded_verified),
        "restored_unchanged": restored,
        "repaired_verified": repaired_verified,
        "excluded_verified": excluded_verified,
        "exclusions": [
            "No prompt selection, gold comparison, mask effect, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    write_json(recovery_path, payload)
    print({"restored_unchanged_count": len(restored), "repaired_verified_count": len(repaired_verified), "excluded_verified_count": len(excluded_verified)})


if __name__ == "__main__":
    main()
