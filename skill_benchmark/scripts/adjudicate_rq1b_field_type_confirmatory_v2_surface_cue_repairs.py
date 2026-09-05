#!/usr/bin/env python3
"""Apply the pre-recorded B1/B2 rule for RQ1b v2 surface-cue repairs."""

from __future__ import annotations

import argparse
import copy
import shutil
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    MATERIALISED_CARD_STATUSES,
    canonical_json_digest,
    card_surface_cue_violations,
    load_list,
    load_object,
    sha256_file,
    validate_card,
    write_json,
)


ARCHIVE_NAME = "quarantine_pre_surface_cue_amendment_2026-08-29"


def repair_audit(root: Path, composition_id: str, builder: str) -> dict:
    path = root / "audits" / f"{composition_id}_{builder}_surface_cue_repair_audit.json"
    payload = load_object(path)
    response_path = root / "surface_cue_repair_responses" / builder / f"{composition_id}.json"
    if (
        payload.get("composition_id") != composition_id
        or payload.get("builder") != builder
        or payload.get("response_sha256") != sha256_file(response_path)
        or not isinstance(payload.get("safe_updates"), list)
    ):
        raise ValueError(f"repair audit/response chain invalid: {composition_id}:{builder}")
    return payload


def replacement_card(existing: dict, audit: dict) -> tuple[dict, str]:
    payload = copy.deepcopy(existing)
    cards = payload.get("cards")
    if not isinstance(cards, dict):
        raise ValueError("canonical repair base has no cards")
    targets = {
        (update.get("candidate"), update.get("field"))
        for update in audit["safe_updates"]
        if isinstance(update, dict)
    }
    original_unflagged = {
        f"{candidate}:{field}": canonical_json_digest(cell)
        for candidate, card in cards.items()
        for field, cell in card.items()
        if (candidate, field) not in targets
    }
    for update in audit["safe_updates"]:
        candidate, field, quotes = update.get("candidate"), update.get("field"), update.get("quotes")
        if candidate not in cards or field not in cards[candidate] or not isinstance(quotes, list):
            raise ValueError("repair audit update does not bind a canonical card cell")
        cards[candidate][field] = {"status": "EVIDENCE", "quotes": quotes}
    validate_card(cards, payload.get("composition_id", "unknown"))
    cues = card_surface_cue_violations(cards)
    if cues:
        raise ValueError(f"repaired card retains surface cues: {cues}")
    repaired_unflagged = {
        f"{candidate}:{field}": canonical_json_digest(cell)
        for candidate, card in cards.items()
        for field, cell in card.items()
        if (candidate, field) not in targets
    }
    if repaired_unflagged != original_unflagged:
        raise ValueError("unflagged canonical cells changed during repair")
    return payload, canonical_json_digest(original_unflagged)


def source_slot_audit(root: Path, composition_id: str) -> dict[str, bool]:
    path = root / "audits" / f"{composition_id}_surface_cue_source_slot_audit.json"
    payload = load_object(path)
    if payload.get("composition_id") != composition_id or payload.get("valid") is not True:
        raise ValueError(f"source-slot audit invalid: {composition_id}")
    decisions = payload.get("builder_slot_preserved")
    if not isinstance(decisions, dict) or set(decisions) != {"b1", "b2"} or any(not isinstance(value, bool) for value in decisions.values()):
        raise ValueError(f"source-slot audit builder decisions invalid: {composition_id}")
    for builder in ("b1", "b2"):
        response_path = root / "surface_cue_repair_responses" / builder / f"{composition_id}.json"
        if payload.get(f"{builder}_repair_response_sha256") != sha256_file(response_path):
            raise ValueError(f"source-slot audit repair binding invalid: {composition_id}:{builder}")
    return decisions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root
    repair_manifest = load_list(root / "surface_cue_repair_packet_manifest.json")
    repair_ids = [row.get("composition_id") for row in repair_manifest if isinstance(row, dict)]
    if not repair_ids or len(repair_ids) != len(set(repair_ids)) or any(not isinstance(item, str) for item in repair_ids):
        raise ValueError("surface-cue repair manifest is invalid")
    original_ledger_path = root / "canonicalisation_ledger.json"
    original_ledger = load_object(original_ledger_path)
    entries = original_ledger.get("compositions")
    if not isinstance(entries, list):
        raise ValueError("canonicalisation ledger has no compositions list")
    entry_by_id = {entry.get("composition_id"): entry for entry in entries if isinstance(entry, dict)}
    if set(repair_ids) - set(entry_by_id):
        raise ValueError("repair manifest refers to unknown canonical composition")
    decisions = []
    replacements, unflagged_digests = {}, {}
    for composition_id in sorted(repair_ids):
        b1, b2 = repair_audit(root, composition_id, "b1"), repair_audit(root, composition_id, "b2")
        slot_decisions = source_slot_audit(root, composition_id)
        chosen = "b1" if b1.get("complete_literal_safe_repair") is True and slot_decisions["b1"] else (
            "b2" if b2.get("complete_literal_safe_repair") is True and slot_decisions["b2"] else None
        )
        decisions.append(
            {
                "composition_id": composition_id,
                "b1_response_sha256": b1.get("response_sha256"),
                "b2_response_sha256": b2.get("response_sha256"),
                "b1_audit_sha256": sha256_file(root / "audits" / f"{composition_id}_b1_surface_cue_repair_audit.json"),
                "b2_audit_sha256": sha256_file(root / "audits" / f"{composition_id}_b2_surface_cue_repair_audit.json"),
                "source_slot_audit_sha256": sha256_file(root / "audits" / f"{composition_id}_surface_cue_source_slot_audit.json"),
                "chosen_builder": chosen,
                "outcome": "MATERIALISED_FROM_LITERAL_SAFE_SURFACE_CUE_REPAIR" if chosen else "EXCLUDED_NO_LITERAL_SAFE_REPAIR",
                "b1_unresolved": b1.get("unresolved"),
                "b2_unresolved": b2.get("unresolved"),
                "source_slot_preserved": slot_decisions,
                "unflagged_cell_map_sha256": None,
            }
        )
        if chosen:
            base = load_object(root / "canonical_cards" / f"{composition_id}.json")
            expected_hash = entry_by_id[composition_id].get("canonical_card_sha256")
            if canonical_json_digest(base) != expected_hash:
                raise ValueError(f"pre-amendment canonical card hash mismatch: {composition_id}")
            replacements[composition_id], unflagged_digests[composition_id] = replacement_card(base, b1 if chosen == "b1" else b2)
            decisions[-1]["unflagged_cell_map_sha256"] = unflagged_digests[composition_id]
    # Every unaffected materialised card must already be cue-free before an amended
    # ledger can be made active.
    for entry in entries:
        composition_id = entry.get("composition_id") if isinstance(entry, dict) else None
        if entry.get("status") not in MATERIALISED_CARD_STATUSES or composition_id in replacements or composition_id in repair_ids:
            continue
        card = load_object(root / "canonical_cards" / f"{composition_id}.json")
        cues = card_surface_cue_violations(card.get("cards", {}))
        if cues:
            raise ValueError(f"unlisted source cue remains: {composition_id}:{cues}")
    proposed_ledger = copy.deepcopy(original_ledger)
    proposed_entries = {entry["composition_id"]: entry for entry in proposed_ledger["compositions"]}
    for decision in decisions:
        entry = proposed_entries[decision["composition_id"]]
        entry["pre_surface_cue_status"] = entry.get("status")
        entry["surface_cue_repair_outcome"] = decision["outcome"]
        entry["surface_cue_repair_chosen_builder"] = decision["chosen_builder"]
        if decision["chosen_builder"]:
            repaired = replacements[decision["composition_id"]]
            entry["status"] = "MATERIALISED_FROM_LITERAL_SAFE_SURFACE_CUE_REPAIR"
            entry["canonical_card_sha256"] = canonical_json_digest(repaired)
        else:
            entry["status"] = "EXCLUDED_NO_LITERAL_SAFE_REPAIR"
            entry.pop("canonical_card_sha256", None)
    ledger_payload = {
        "status": "RQ1B_FIELD_TYPE_V2_SURFACE_CUE_REPAIR_ADJUDICATION_NOT_A_RESULT",
        "repair_count": len(decisions),
        "repair_pass_count": sum(row["chosen_builder"] is not None for row in decisions),
        "strict_exclusion_count": sum(row["chosen_builder"] is None for row in decisions),
        "decisions": decisions,
        "exclusions": [
            "No prompt selection, gold comparison, mask effect, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    if not args.write:
        print({"mode": "dry_run", "repair_count": len(decisions), "repair_pass_count": ledger_payload["repair_pass_count"], "strict_exclusion_count": ledger_payload["strict_exclusion_count"]})
        return
    archive = root / ARCHIVE_NAME
    if archive.exists() or (root / "surface_cue_repair_ledger.json").exists():
        raise ValueError("surface-cue repair has already been applied or archive exists")
    archive.mkdir()
    for relative in ("canonicalisation_ledger.json", "canonical_cards", "conditions", "selection_packets", "residual_packets", "selection_packets_opaque", "residual_packets_opaque", "selection_packet_manifest_opaque.json", "selection_packet_private_map.json", "residual_packet_manifest_opaque.json", "residual_packet_private_map.json", "opaque_review_input_freeze.json", "audits/opaque_packet_binding_preflight.json", "audits/field_eligibility_ledger.json"):
        source = root / relative
        if source.exists():
            destination = archive / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Preserve the pre-amendment cards for audit, but leave the active
            # directory intact so unmodified cards remain available after only
            # the approved replacements are overwritten below.
            if relative == "canonical_cards":
                shutil.copytree(source, destination)
            else:
                shutil.move(str(source), str(destination))
    for composition_id, repaired in replacements.items():
        write_json(root / "canonical_cards" / f"{composition_id}.json", repaired)
    write_json(original_ledger_path, proposed_ledger)
    write_json(root / "surface_cue_repair_ledger.json", ledger_payload)
    print({"mode": "written", "repair_count": len(decisions), "repair_pass_count": ledger_payload["repair_pass_count"], "strict_exclusion_count": ledger_payload["strict_exclusion_count"], "archive": str(archive)})


if __name__ == "__main__":
    main()
