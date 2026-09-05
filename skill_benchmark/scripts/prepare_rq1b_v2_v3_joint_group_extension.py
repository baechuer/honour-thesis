#!/usr/bin/env python3
"""Freeze V3 joint-group masks for the RQ1b V2+V3 extension, locally only."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from prepare_rq1b_joint_field_mask_v21 import GROUPS, MARKER
from run_rq1b_v2_v3_complete_triad_extension import EXTENSION, load_extension, sha256_file


OUTPUT = Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/rq1b_v2_v3_joint_group_extension_2026-08-30")
V2_FREEZE = Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_joint_mask_v21_2026-08-29/joint_mask_freeze.json")
VERSION = "rq1b-v2-v3-joint-group-extension-freeze-v1"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def validate_cards(full_cards: list[dict[str, Any]], cards: list[dict[str, Any]], withheld: tuple[str, ...], composition_id: str, condition: str) -> None:
    if [card["label"] for card in cards] != [card["label"] for card in full_cards]:
        raise ValueError(f"candidate membership drift: {composition_id}/{condition}")
    for full, derived in zip(full_cards, cards, strict=True):
        if set(full["slots"]) != set(derived["slots"]):
            raise ValueError(f"slot schema drift: {composition_id}/{condition}/{full['label']}")
        for field, value in full["slots"].items():
            expected = MARKER if field in withheld else value
            if derived["slots"][field] != expected:
                raise ValueError(f"slot mutation: {composition_id}/{condition}/{full['label']}/{field}")


def build(output: Path = OUTPUT) -> dict[str, Any]:
    if output.exists():
        raise ValueError(f"refusing to overwrite V3 joint-group freeze: {output}")
    cards_by_key, families, extension_audit = load_extension()
    v2_freeze = read_json(V2_FREEZE)
    expected_v2 = {condition: count for condition, count in (("MASK_TASK_SPECIFICATION", 73), ("MASK_EXECUTION_VERIFICATION", 77), ("MASK_APPLICABILITY_CAPABILITY", 70))}
    eligible = v2_freeze.get("group_eligible_routing_family_ids")
    if not isinstance(eligible, dict) or {condition: len(eligible.get(condition, [])) for condition in GROUPS} != expected_v2:
        raise ValueError("V2 joint eligibility drift")
    composition_ids = sorted({family["composition_id"] for family in families})
    if len(families) != 12 or len(composition_ids) != 4:
        raise ValueError("V3 complete-triad scope drift")

    staging = output.parent / f".{output.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        condition_sha256: dict[str, dict[str, str]] = {}
        for composition_id in composition_ids:
            full_cards = cards_by_key[f"{composition_id}/FULL"]
            condition_sha256[composition_id] = {}
            for condition, withheld in GROUPS.items():
                cards = [
                    {
                        "label": card["label"],
                        "slots": {field: MARKER if field in withheld else value for field, value in card["slots"].items()},
                    }
                    for card in full_cards
                ]
                validate_cards(full_cards, cards, withheld, composition_id, condition)
                payload = {
                    "status": "RQ1B_V2_V3_JOINT_GROUP_CONDITION_NOT_A_RESULT",
                    "version": VERSION,
                    "composition_id": composition_id,
                    "condition": condition,
                    "withheld_fields": list(withheld),
                    "marker": MARKER,
                    "cards": cards,
                }
                path = staging / "conditions" / composition_id / f"{condition}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                condition_sha256[composition_id][condition] = digest(payload)

        freeze = {
            "status": "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_FREEZE_NOT_A_RESULT",
            "version": VERSION,
            "v2_joint_freeze": str(V2_FREEZE),
            "v2_joint_freeze_sha256": sha256_file(V2_FREEZE),
            "v2_eligible_family_counts": expected_v2,
            "v3_extension_root": str(EXTENSION),
            "v3_extension_audit": extension_audit,
            "v3_composition_ids": composition_ids,
            "v3_routing_family_ids": [family["routing_family_id"] for family in families],
            "v3_family_count": len(families),
            "groups": {condition: list(fields) for condition, fields in GROUPS.items()},
            "marker": MARKER,
            "condition_sha256": condition_sha256,
            "combined_group_scope": {
                condition: {
                    "v2_eligible_families": len(eligible[condition]),
                    "v3_eligible_families": len(families),
                    "combined_families": len(eligible[condition]) + len(families),
                    "combined_prompts": 2 * (len(eligible[condition]) + len(families)),
                }
                for condition in GROUPS
            },
            "rules": [
                "Every withheld field is replaced by the same marker for every candidate in a V3 composition.",
                "Every non-withheld V3 slot is byte-identical to that composition's imported FULL card.",
                "V2 group eligibility is unchanged; every complete V3 family enters each group.",
                "No selector, embedding, API request or thesis write occurs during materialisation.",
            ],
        }
        (staging / "freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
        staging.replace(output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "status": freeze["status"],
        "output": str(output),
        "v3_cards_materialised": len(composition_ids) * 3 * len(GROUPS),
        "combined_group_scope": freeze["combined_group_scope"],
    }


def check(output: Path = OUTPUT) -> dict[str, Any]:
    freeze = read_json(output / "freeze.json")
    if freeze.get("status") != "RQ1B_V2_V3_JOINT_GROUP_EXTENSION_FREEZE_NOT_A_RESULT" or freeze.get("version") != VERSION:
        raise ValueError("freeze status/version drift")
    if freeze.get("v2_joint_freeze_sha256") != sha256_file(V2_FREEZE):
        raise ValueError("V2 joint freeze drift")
    cards_by_key, families, audit = load_extension()
    if freeze.get("v3_extension_audit") != audit or freeze.get("v3_routing_family_ids") != [family["routing_family_id"] for family in families]:
        raise ValueError("V3 extension drift")
    for composition_id in freeze["v3_composition_ids"]:
        full = cards_by_key[f"{composition_id}/FULL"]
        for condition, withheld in GROUPS.items():
            payload = read_json(output / "conditions" / composition_id / f"{condition}.json")
            if payload.get("condition") != condition or payload.get("withheld_fields") != list(withheld) or payload.get("marker") != MARKER:
                raise ValueError(f"condition metadata drift: {composition_id}/{condition}")
            validate_cards(full, payload["cards"], withheld, composition_id, condition)
            if freeze["condition_sha256"][composition_id][condition] != digest(payload):
                raise ValueError(f"condition hash drift: {composition_id}/{condition}")
    return {"status": "PASS", "combined_group_scope": freeze["combined_group_scope"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.build == args.check:
        parser.error("choose exactly one of --build or --check")
    print(json.dumps(build() if args.build else check(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
