#!/usr/bin/env python3
"""Freeze candidate-synchronous joint field masks derived from immutable RQ1b v2 cards."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from rq1b_field_type_confirmatory_v2_common import FIELDS, canonical_entries
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze
from run_rq1b_field_type_confirmatory_v2_bm25 import load_condition, load_strict_families


VERSION = "rq1b-joint-field-mask-v21-freeze-v1"
MARKER = "[FIELD WITHHELD IN THIS REPRESENTATION]"
GROUPS: dict[str, tuple[str, ...]] = {
    "MASK_TASK_SPECIFICATION": ("use_condition", "input_precondition", "output_artifact"),
    "MASK_EXECUTION_VERIFICATION": ("workflow_procedure", "success_verification"),
    "MASK_APPLICABILITY_CAPABILITY": ("boundary_not_for", "dependency_resource"),
}
CONDITIONS = ("FULL", *GROUPS)


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def group_eligibility(field_eligible: dict[str, set[str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for condition, fields in GROUPS.items():
        if any(field not in field_eligible for field in fields):
            raise ValueError(f"unknown field in joint group: {condition}")
        result[condition] = set.intersection(*(field_eligible[field] for field in fields))
        if not result[condition]:
            raise ValueError(f"empty joint eligibility set: {condition}")
    return result


def validate_cards(cards: list[dict[str, Any]], condition: str) -> None:
    withheld = set(GROUPS.get(condition, ()))
    labels = [card.get("label") for card in cards]
    if not labels or len(labels) != len(set(labels)):
        raise ValueError(f"invalid candidate labels: {condition}")
    for card in cards:
        slots = card.get("slots")
        if not isinstance(slots, dict) or set(slots) != set(FIELDS):
            raise ValueError(f"invalid slots: {condition}/{card.get('label')}")
        for field in FIELDS:
            if not isinstance(slots[field], str):
                raise ValueError(f"non-text slot: {condition}/{card.get('label')}/{field}")
            if field in withheld and slots[field] != MARKER:
                raise ValueError(f"joint mask missing: {condition}/{card.get('label')}/{field}")


def materialize(source_root: Path, output_root: Path) -> dict[str, Any]:
    if output_root.exists():
        raise ValueError(f"refusing to overwrite joint-mask root: {output_root}")
    verify_freeze(source_root)
    families, field_eligible = load_strict_families(source_root)
    group_eligible = group_eligibility(field_eligible)
    entries = canonical_entries(source_root)
    strict_compositions = sorted({family["composition_id"] for family in families})
    if len(families) != 87 or len(strict_compositions) != 42:
        raise ValueError("v2 strict scope drift")

    staging = output_root.parent / f".{output_root.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging root: {staging}")
    staging.mkdir(parents=True)
    try:
        condition_sha256: dict[str, dict[str, str]] = {}
        source_full_sha256: dict[str, str] = {}
        for composition_id in strict_compositions:
            entry = entries[composition_id]
            full_cards = load_condition(source_root, composition_id, "FULL", entry)
            validate_cards(full_cards, "FULL")
            source_full_sha256[composition_id] = entry["condition_sha256"]["FULL"]
            condition_sha256[composition_id] = {}
            for condition in CONDITIONS:
                withheld = list(GROUPS.get(condition, ()))
                cards = [
                    {
                        "label": card["label"],
                        "slots": {
                            field: MARKER if field in withheld else card["slots"][field]
                            for field in FIELDS
                        },
                    }
                    for card in full_cards
                ]
                validate_cards(cards, condition)
                if [card["label"] for card in cards] != [card["label"] for card in full_cards]:
                    raise ValueError(f"candidate membership drift: {composition_id}/{condition}")
                for full, derived in zip(full_cards, cards, strict=True):
                    for field in FIELDS:
                        expected = MARKER if field in withheld else full["slots"][field]
                        if derived["slots"][field] != expected:
                            raise ValueError(f"slot mutation: {composition_id}/{condition}/{field}")
                payload = {
                    "status": "RQ1B_JOINT_FIELD_MASK_V21_CONDITION_NOT_A_RESULT",
                    "composition_id": composition_id,
                    "condition": condition,
                    "withheld_fields": withheld,
                    "marker": MARKER if withheld else None,
                    "field_order": list(FIELDS),
                    "cards": cards,
                }
                path = staging / "conditions" / composition_id / f"{condition}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                condition_sha256[composition_id][condition] = digest(payload)

        freeze = {
            "status": "RQ1B_JOINT_FIELD_MASK_V21_PROSPECTIVE_FREEZE_NOT_A_RESULT",
            "version": VERSION,
            "source_v2_root": str(source_root),
            "source_v2_freeze_verified": True,
            "source_v2_canonicalisation_ledger_sha256": sha256_file(source_root / "canonicalisation_ledger.json"),
            "source_full_condition_sha256": source_full_sha256,
            "groups": {condition: list(fields) for condition, fields in GROUPS.items()},
            "conditions": list(CONDITIONS),
            "marker": MARKER,
            "strict_routing_family_ids": [family["routing_family_id"] for family in families],
            "strict_composition_ids": strict_compositions,
            "group_eligible_routing_family_ids": {condition: sorted(ids) for condition, ids in group_eligible.items()},
            "condition_sha256": condition_sha256,
            "rules": [
                "FULL is copied only from the source v2 immutable FULL condition.",
                "Every field in a joint set is replaced with the same marker for every candidate in the composition.",
                "Every field outside a joint set remains byte-identical to source v2 FULL cards.",
                "This is a prospective-before-joint-results amendment, not a retroactive v2 preregistration.",
            ],
            "exclusions": [
                "No selector, embedding, retrieval score, metric, API request, or external transfer is created by materialisation.",
                "The source v2 root and completed single-field outputs are not modified.",
            ],
        }
        (staging / "joint_mask_freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
        staging.replace(output_root)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "valid": True,
        "joint_root": str(output_root),
        "strict_routing_families": len(families),
        "strict_compositions": len(strict_compositions),
        "group_eligible_families": {condition: len(ids) for condition, ids in group_eligible.items()},
        "conditions": list(CONDITIONS),
    }


def load_joint_scope(root: Path) -> tuple[dict[str, Any], Path, list[dict[str, Any]], dict[str, set[str]]]:
    freeze = load_object(root / "joint_mask_freeze.json")
    if freeze.get("status") != "RQ1B_JOINT_FIELD_MASK_V21_PROSPECTIVE_FREEZE_NOT_A_RESULT" or freeze.get("version") != VERSION:
        raise ValueError("unexpected joint-mask freeze status")
    if freeze.get("groups") != {condition: list(fields) for condition, fields in GROUPS.items()} or freeze.get("conditions") != list(CONDITIONS):
        raise ValueError("joint-group definition drift")
    source_root = Path(freeze["source_v2_root"])
    verify_freeze(source_root)
    if freeze.get("source_v2_canonicalisation_ledger_sha256") != sha256_file(source_root / "canonicalisation_ledger.json"):
        raise ValueError("source canonicalisation ledger drift")
    families, field_eligible = load_strict_families(source_root)
    eligible = group_eligibility(field_eligible)
    if [family["routing_family_id"] for family in families] != freeze.get("strict_routing_family_ids"):
        raise ValueError("strict family binding drift")
    if sorted({family["composition_id"] for family in families}) != freeze.get("strict_composition_ids"):
        raise ValueError("strict composition binding drift")
    if {condition: sorted(ids) for condition, ids in eligible.items()} != freeze.get("group_eligible_routing_family_ids"):
        raise ValueError("joint eligibility drift")
    return freeze, source_root, families, eligible


def load_joint_condition(root: Path, freeze: dict[str, Any], composition_id: str, condition: str) -> list[dict[str, Any]]:
    path = root / "conditions" / composition_id / f"{condition}.json"
    payload = load_object(path)
    withheld = list(GROUPS.get(condition, ()))
    if (
        payload.get("status") != "RQ1B_JOINT_FIELD_MASK_V21_CONDITION_NOT_A_RESULT"
        or payload.get("composition_id") != composition_id
        or payload.get("condition") != condition
        or payload.get("withheld_fields") != withheld
        or digest(payload) != freeze["condition_sha256"][composition_id][condition]
    ):
        raise ValueError(f"joint condition binding invalid: {composition_id}/{condition}")
    cards = payload.get("cards")
    if not isinstance(cards, list) or len(cards) not in {3, 4}:
        raise ValueError(f"joint condition cards invalid: {composition_id}/{condition}")
    validate_cards(cards, condition)
    return cards


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-v2-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(materialize(args.source_v2_root, args.output_root), sort_keys=True))


if __name__ == "__main__":
    main()
