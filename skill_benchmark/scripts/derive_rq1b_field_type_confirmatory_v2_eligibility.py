#!/usr/bin/env python3
"""Derive composition-keyed RQ1b v2 field coverage and later-preservation gates."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    FIELDS,
    canonical_cards,
    canonical_entries,
    cell_signature,
    composition_rows,
    label_for_skill,
    load_object,
    load_list,
    sha256_file,
    materialised_composition_ids,
    routing_family_rows,
    write_json,
)
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze


def preservation_state(
    root: Path,
    family_id: str,
    composition_id: str,
    gold_label: str,
    packet_map: dict[str, dict],
) -> tuple[str, bool | None]:
    mapping = packet_map.get(family_id)
    if not isinstance(mapping, dict):
        raise ValueError(f"private selection packet map missing family: {family_id}")
    packet_id = mapping.get("packet_id")
    current_card_sha = canonical_entries(root)[composition_id].get("canonical_card_sha256")
    if (
        not isinstance(packet_id, str)
        or mapping.get("composition_id") != composition_id
        or mapping.get("canonical_card_sha256") != current_card_sha
    ):
        raise ValueError(f"private selection packet binding invalid: {family_id}")
    path = root / "preservation_ledger" / f"{family_id}.json"
    if not path.is_file():
        return "PENDING_FULL_CARD_PRESERVATION", None
    payload = load_object(path)
    passed = payload.get("strict_singleton_preserved")
    if not isinstance(passed, bool):
        raise ValueError(f"invalid preservation record: {family_id}")
    expected_status = (
        "RQ1B_FIELD_TYPE_V2_FULL_CARD_PRESERVATION_PASS_NOT_A_SELECTOR_RESULT"
        if passed
        else "RQ1B_FIELD_TYPE_V2_FULL_CARD_PRESERVATION_FAIL_NOT_A_SELECTOR_RESULT"
    )
    if (
        payload.get("status") != expected_status
        or payload.get("routing_family_id") != family_id
        or payload.get("composition_id") != composition_id
        or payload.get("sealed_gold_label") != gold_label
        or payload.get("packet_id") != packet_id
        or payload.get("packet_sha256") != mapping.get("packet_sha256")
        or payload.get("both_reviews_schema_valid") is not True
        or not isinstance(payload.get("first_reviewer"), str)
        or not isinstance(payload.get("second_reviewer"), str)
        or payload["first_reviewer"] == payload["second_reviewer"]
    ):
        raise ValueError(f"preservation record binding invalid: {family_id}")
    audit_specs = (
        ("first", payload["first_reviewer"]),
        ("second", payload["second_reviewer"]),
    )
    for position, reviewer in audit_specs:
        audit_path = root / "audits" / f"{packet_id}_{reviewer}_selection_review_audit.json"
        response_path = root / "selection_reviews_opaque" / reviewer / f"{packet_id}.json"
        audit = load_object(audit_path)
        if (
            payload.get(f"{position}_audit_sha256") != sha256_file(audit_path)
            or payload.get(f"{position}_response_sha256") != sha256_file(response_path)
            or audit.get("packet_id") != packet_id
            or audit.get("reviewer") != reviewer
            or audit.get("packet_sha256") != mapping.get("packet_sha256")
            or audit.get("response_sha256") != sha256_file(response_path)
            or audit.get("valid") is not True
        ):
            raise ValueError(f"preservation audit/response chain invalid: {family_id}:{position}")
    rows = payload.get("variant_rows")
    variants = {row.get("variant") for row in rows if isinstance(row, dict)} if isinstance(rows, list) else set()
    if not isinstance(rows, list) or len(rows) != 2 or variants != {"direct", "paraphrase"}:
        raise ValueError(f"preservation variants invalid: {family_id}")
    if passed and not all(row.get("strict_singleton_preserved") is True for row in rows):
        raise ValueError(f"preservation pass does not match rows: {family_id}")
    return ("FULL_CARD_PRESERVATION_PASS" if passed else "FULL_CARD_PRESERVATION_FAIL"), passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    verify_freeze(root)
    compositions = composition_rows(root)
    families = routing_family_rows(root)
    materialised = materialised_composition_ids(root)
    raw_packet_map = load_list(root / "selection_packet_private_map.json")
    packet_map = {}
    for item in raw_packet_map:
        family_id = item.get("routing_family_id") if isinstance(item, dict) else None
        if not isinstance(family_id, str) or family_id in packet_map:
            raise ValueError("invalid or duplicate private selection packet map")
        packet_map[family_id] = item
    family_rows = []

    for family_id, family in sorted(families.items()):
        composition_id = family["composition_id"]
        if composition_id not in materialised:
            continue
        composition = compositions[composition_id]
        gold_label = label_for_skill(composition, family["strict_gold_skill_id"])
        cards = canonical_cards(root, composition_id)
        state, passed = preservation_state(root, family_id, composition_id, gold_label, packet_map)
        fields = []
        for field in FIELDS:
            gold_cell = cards[gold_label][field]
            gold_value = cell_signature(gold_cell)
            different_wrong_labels = [
                label
                for label, card in sorted(cards.items())
                if label != gold_label and cell_signature(card[field]) != gold_value
            ]
            has_gold_evidence = gold_cell["status"] == "EVIDENCE" and bool(gold_cell["quotes"])
            fields.append(
                {
                    "field": field,
                    "gold_has_nonmarker_source_evidence": has_gold_evidence,
                    "wrong_candidates_with_different_value": different_wrong_labels,
                    "eligible_by_card_coverage": has_gold_evidence and bool(different_wrong_labels),
                    "scoring_eligible_after_preservation": (
                        passed and has_gold_evidence and bool(different_wrong_labels)
                        if passed is not None
                        else None
                    ),
                }
            )
        family_rows.append(
            {
                "routing_family_id": family_id,
                "composition_id": composition_id,
                "sealed_gold_label": gold_label,
                "candidate_count": len(cards),
                "full_card_preservation_state": state,
                "field_rows": fields,
            }
        )

    coverage = {
        field: sum(
            row["eligible_by_card_coverage"]
            for family in family_rows
            for row in family["field_rows"]
            if row["field"] == field
        )
        for field in FIELDS
    }
    preserved_coverage = {
        field: sum(
            row["scoring_eligible_after_preservation"] is True
            for family in family_rows
            for row in family["field_rows"]
            if row["field"] == field
        )
        for field in FIELDS
    }
    preservation_counts = {
        state: sum(family["full_card_preservation_state"] == state for family in family_rows)
        for state in {
            "PENDING_FULL_CARD_PRESERVATION",
            "FULL_CARD_PRESERVATION_PASS",
            "FULL_CARD_PRESERVATION_FAIL",
        }
    }
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_ELIGIBILITY_LEDGER_NOT_A_RESULT",
        "materialised_routing_family_count": len(family_rows),
        "full_card_preservation_counts": preservation_counts,
        "eligible_counts_by_field_before_preservation": coverage,
        "eligible_counts_by_field_after_preservation": preserved_coverage,
        "families": family_rows,
        "exclusions": [
            "This is source-card coverage and a local preservation join only. No mask effect, selector, embedding, retrieval, score, metric, API call, or result is created.",
        ],
    }
    output = root / "audits" / "field_eligibility_ledger.json"
    write_json(output, payload)
    print(
        {
            "materialised_routing_family_count": len(family_rows),
            "eligible_counts_by_field_before_preservation": coverage,
            "full_card_preservation_counts": preservation_counts,
        }
    )


if __name__ == "__main__":
    main()
