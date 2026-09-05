#!/usr/bin/env python3
"""Validate one blinded RQ1b-S original-field-card route-preservation review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    family_dir = args.pilot_root / args.pilot_id
    packet = json.loads((family_dir / "original_card_route_preservation_packet.json").read_text())
    response_path = args.pilot_root / "route_reviews" / args.reviewer / f"{args.pilot_id}.json"
    failures = []
    try:
        response = json.loads(response_path.read_text())
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")

    if response.get("pilot_id") != args.pilot_id:
        failures.append("pilot_id_mismatch")
    rows = response.get("per_prompt")
    packet_rows = packet.get("prompts", [])
    if not isinstance(rows, list) or len(rows) != len(packet_rows):
        failures.append("prompt_row_count_mismatch")
        rows = rows if isinstance(rows, list) else []
    candidates = {item["label"]: item["field_card"] for item in packet["candidates"]}
    allowed_fields = set(packet["allowed_primary_fields"])
    expected_variants = [item["variant"] for item in packet_rows]
    seen_variants = []
    records = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"row_not_object:{index}")
            continue
        variant = row.get("variant")
        seen_variants.append(variant)
        if variant not in expected_variants:
            failures.append(f"unknown_variant:{index}")
        fully_adequate = row.get("fully_adequate_candidates")
        if not isinstance(fully_adequate, list) or not fully_adequate or len(set(fully_adequate)) != len(fully_adequate):
            failures.append(f"invalid_fully_adequate_candidates:{index}")
            fully_adequate = []
        if any(label not in candidates for label in fully_adequate):
            failures.append(f"unknown_candidate_label:{index}")
        if row.get("primary_field") not in allowed_fields:
            failures.append(f"invalid_primary_field:{index}")
        evidence = row.get("evidence")
        if not isinstance(evidence, dict):
            failures.append(f"invalid_evidence:{index}")
            evidence = {}
        if set(evidence) - set(fully_adequate):
            failures.append(f"evidence_for_nonadequate_candidate:{index}")
        for label in fully_adequate:
            quotes = evidence.get(label)
            if not isinstance(quotes, list) or not quotes:
                failures.append(f"missing_evidence:{index}:{label}")
                continue
            for quote_index, quote in enumerate(quotes):
                if not isinstance(quote, str) or not quote or quote not in candidates[label]:
                    failures.append(f"evidence_not_exact_card_substring:{index}:{label}:{quote_index}")
                records.append({"variant": variant, "candidate": label, "quote": quote})
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            failures.append(f"invalid_reason:{index}")
    if sorted(seen_variants) != sorted(expected_variants):
        failures.append("variant_set_mismatch")

    output = args.pilot_root / "audits" / f"{args.pilot_id}_{args.reviewer}_route_review_audit.json"
    payload = {
        "status": "RQ1B_S_BLINDED_ORIGINAL_CARD_ROUTE_REVIEW_AUDIT_NOT_A_RESULT",
        "pilot_id": args.pilot_id,
        "reviewer": args.reviewer,
        "valid": not failures,
        "failures": failures,
        "records": records,
        "exclusions": [
            "No strict-gold comparison, card acceptance, neutralisation, selector, embedding, retrieval, API call, score, metric, or result exists.",
        ],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "valid": payload["valid"]}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
