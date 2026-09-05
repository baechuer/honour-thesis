#!/usr/bin/env python3
"""Validate one blinded RQ1b v2 FULL-card preservation review."""

from __future__ import annotations

import argparse
from pathlib import Path

from rq1b_field_type_confirmatory_v2_common import (
    load_object,
    load_list,
    rendered_packet_field_sections,
    sha256_file,
    usable_exact_packet_evidence,
    write_json,
)
from rq1b_field_type_confirmatory_v2_opaque_freeze import verify_freeze


OUTCOMES = {"SINGLETON", "MULTIPLE_ADEQUATE", "NONE_ADEQUATE"}


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
        for row in load_list(root / "selection_packet_manifest_opaque.json")
        if isinstance(row, dict)
    }
    private_maps = [
        row for row in load_list(root / "selection_packet_private_map.json")
        if isinstance(row, dict) and row.get("packet_id") == args.packet_id
    ]
    if args.packet_id not in manifest_ids or len(private_maps) != 1:
        raise ValueError("selection packet is absent from the frozen opaque manifest/map")
    packet = load_object(root / "selection_packets_opaque" / f"{args.packet_id}.json")
    response_path = root / "selection_reviews_opaque" / args.reviewer / f"{args.packet_id}.json"
    packet_path = root / "selection_packets_opaque" / f"{args.packet_id}.json"
    if private_maps[0].get("packet_sha256") != sha256_file(packet_path):
        raise ValueError("selection packet hash is not the frozen private-map hash")
    failures, records = [], []
    try:
        response = load_object(response_path)
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("packet_id") != args.packet_id:
        failures.append("packet_id_mismatch")
    expected_variants = [item["variant"] for item in packet.get("prompts", [])]
    candidates = {item["label"]: item["field_card"] for item in packet.get("candidates", [])}
    try:
        candidate_sections = {
            label: rendered_packet_field_sections(rendered)
            for label, rendered in candidates.items()
        }
    except Exception as error:
        candidate_sections = {}
        failures.append(f"packet_card_parse_error:{error}")
    rows = response.get("per_prompt") if isinstance(response.get("per_prompt"), list) else []
    if len(rows) != len(expected_variants):
        failures.append("prompt_row_count_mismatch")
    observed_variants = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"row_not_object:{index}")
            continue
        variant = row.get("variant")
        observed_variants.append(variant)
        outcome = row.get("adequacy_outcome")
        if outcome not in OUTCOMES:
            failures.append(f"invalid_adequacy_outcome:{index}")
        selected = row.get("fully_adequate_candidates")
        if not isinstance(selected, list) or len(selected) != len(set(selected)):
            failures.append(f"invalid_fully_adequate_candidates:{index}")
            selected = []
        if any(label not in candidates for label in selected):
            failures.append(f"unknown_candidate_label:{index}")
        if outcome == "SINGLETON" and len(selected) != 1:
            failures.append(f"singleton_cardinality_mismatch:{index}")
        if outcome == "MULTIPLE_ADEQUATE" and len(selected) < 2:
            failures.append(f"multiple_cardinality_mismatch:{index}")
        if outcome == "NONE_ADEQUATE" and selected:
            failures.append(f"none_cardinality_mismatch:{index}")
        evidence = row.get("evidence")
        if not isinstance(evidence, dict) or set(evidence) != set(selected):
            failures.append(f"evidence_candidate_set_mismatch:{index}")
            evidence = evidence if isinstance(evidence, dict) else {}
        for label in selected:
            quotes = evidence.get(label)
            if not isinstance(quotes, list) or not quotes:
                failures.append(f"missing_evidence:{index}:{label}")
                continue
            for quote_index, quote in enumerate(quotes):
                if not usable_exact_packet_evidence(quote, candidate_sections.get(label, {})):
                    failures.append(f"evidence_not_exact_card_substring:{index}:{label}:{quote_index}")
                records.append({"variant": variant, "candidate": label, "quote": quote})
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            failures.append(f"invalid_reason:{index}")
    if sorted(observed_variants) != sorted(expected_variants):
        failures.append("variant_set_mismatch")
    payload = {
        "status": "RQ1B_FIELD_TYPE_V2_BLINDED_FULL_CARD_REVIEW_AUDIT_NOT_A_RESULT",
        "packet_id": args.packet_id,
        "reviewer": args.reviewer,
        "packet_sha256": sha256_file(packet_path),
        "response_sha256": sha256_file(response_path) if response_path.is_file() else None,
        "valid": not failures,
        "failures": failures,
        "records": records,
        "exclusions": [
            "No strict-gold comparison, field attribution, mask condition, selector, embedding, retrieval, score, metric, API call, or result exists.",
        ],
    }
    output = root / "audits" / f"{args.packet_id}_{args.reviewer}_selection_review_audit.json"
    write_json(output, payload)
    print({"packet_id": args.packet_id, "reviewer": args.reviewer, "valid": payload["valid"]})
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
