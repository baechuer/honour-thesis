#!/usr/bin/env python3
"""Validate one source-card-only RQ1b v2 residual-redundancy review."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    FIELDS,
    load_object,
    load_list,
    rendered_packet_field_sections,
    sha256_file,
    usable_exact_packet_evidence,
    write_json,
)
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze


LABELS = {"none", "partial", "substantial"}


def parse_cards(packet: dict) -> dict[str, dict[str, str]]:
    cards = {}
    for candidate in packet.get("candidates", []):
        label, rendered = candidate.get("label"), candidate.get("field_card")
        if not isinstance(label, str) or not isinstance(rendered, str) or label in cards:
            raise ValueError("packet candidates invalid")
        cards[label] = rendered_packet_field_sections(rendered)
    return cards


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--packet-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    root = args.root
    verify_freeze(root)
    manifest_ids = {
        row.get("packet_id")
        for row in load_list(root / "residual_packet_manifest_opaque.json")
        if isinstance(row, dict)
    }
    private_maps = [
        row for row in load_list(root / "residual_packet_private_map.json")
        if isinstance(row, dict) and row.get("packet_id") == args.packet_id
    ]
    if args.packet_id not in manifest_ids or len(private_maps) != 1:
        raise ValueError("residual packet is absent from the frozen opaque manifest/map")
    packet = load_object(root / "residual_packets_opaque" / f"{args.packet_id}.json")
    response_path = root / "residual_reviews_opaque" / args.reviewer / f"{args.packet_id}.json"
    packet_path = root / "residual_packets_opaque" / f"{args.packet_id}.json"
    if private_maps[0].get("packet_sha256") != sha256_file(packet_path):
        raise ValueError("residual packet hash is not the frozen private-map hash")
    failures, records = [], []
    try:
        card_fields = parse_cards(packet)
    except Exception as error:
        card_fields = {}
        failures.append(f"packet_parse_error:{error}")
    expected = {(item["candidate"], item["field"]) for item in packet.get("targets", [])}
    if len(expected) != len(packet.get("targets", [])):
        failures.append("duplicate_or_invalid_packet_targets")
    try:
        response = load_object(response_path)
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("packet_id") != args.packet_id:
        failures.append("packet_id_mismatch")
    assessments = response.get("candidate_assessments") if isinstance(response.get("candidate_assessments"), list) else []
    seen = set()
    for index, assessment in enumerate(assessments):
        if not isinstance(assessment, dict):
            failures.append(f"assessment_not_object:{index}")
            continue
        key = (assessment.get("candidate"), assessment.get("field"))
        if key not in expected:
            failures.append(f"unknown_target:{index}")
        if key in seen:
            failures.append(f"duplicate_target:{index}")
        seen.add(key)
        label = assessment.get("residual_label")
        if label not in LABELS:
            failures.append(f"invalid_residual_label:{index}")
        evidence = assessment.get("remaining_slot_evidence")
        if not isinstance(evidence, list):
            failures.append(f"invalid_remaining_slot_evidence:{index}")
            evidence = []
        if label == "none" and evidence:
            failures.append(f"none_with_evidence:{index}")
        if label in {"partial", "substantial"} and not evidence:
            failures.append(f"non_none_without_evidence:{index}")
        candidate, target_field = key
        for item_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                failures.append(f"evidence_item_not_object:{index}:{item_index}")
                continue
            field, quotes = item.get("field"), item.get("quotes")
            if field not in FIELDS or field == target_field:
                failures.append(f"invalid_remaining_field:{index}:{item_index}")
            if not isinstance(quotes, list) or not quotes:
                failures.append(f"invalid_remaining_quotes:{index}:{item_index}")
                continue
            sections = {field: card_fields.get(candidate, {}).get(field, "")}
            for quote_index, quote in enumerate(quotes):
                if not usable_exact_packet_evidence(quote, sections):
                    failures.append(f"remaining_evidence_not_exact_card_substring:{index}:{item_index}:{quote_index}")
                records.append({"candidate": candidate, "target_field": target_field, "remaining_field": field, "quote": quote})
        if not isinstance(assessment.get("reason"), str) or not assessment["reason"].strip():
            failures.append(f"invalid_reason:{index}")
    if seen != expected:
        failures.append("target_set_mismatch")
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_SOURCE_CARD_ONLY_RESIDUAL_REVIEW_AUDIT_NOT_A_RESULT",
        "packet_id": args.packet_id,
        "reviewer": args.reviewer,
        "packet_sha256": sha256_file(packet_path),
        "response_sha256": sha256_file(response_path) if response_path.is_file() else None,
        "valid": not failures,
        "failures": failures,
        "records": records,
        "exclusions": [
            "No prompt selection, strict-gold comparison, field attribution, selector, embedding, retrieval, score, metric, API call, or result exists.",
        ],
    }
    output = root / "audits" / f"{args.packet_id}_{args.reviewer}_residual_review_audit.json"
    write_json(output, payload)
    print({"packet_id": args.packet_id, "reviewer": args.reviewer, "valid": payload["valid"]})
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
