#!/usr/bin/env python3
"""Validate one blinded RQ1b field-type FULL-card selection review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    root = args.pilot_root
    packet = load_object(root / "selection_packets" / f"{args.pilot_id}.json")
    response_path = root / "selection_reviews" / args.reviewer / f"{args.pilot_id}.json"
    failures: list[str] = []
    try:
        response = load_object(response_path)
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("pilot_id") != args.pilot_id:
        failures.append("pilot_id_mismatch")
    expected_variants = [item["variant"] for item in packet["prompts"]]
    candidates = {item["label"]: item["field_card"] for item in packet["candidates"]}
    rows = response.get("per_prompt") if isinstance(response.get("per_prompt"), list) else []
    if len(rows) != len(expected_variants):
        failures.append("prompt_row_count_mismatch")
    observed_variants: list[str] = []
    records: list[dict] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"row_not_object:{index}")
            continue
        variant = row.get("variant")
        observed_variants.append(variant)
        selected = row.get("fully_adequate_candidates")
        if not isinstance(selected, list) or not selected or len(selected) != len(set(selected)):
            failures.append(f"invalid_fully_adequate_candidates:{index}")
            selected = []
        if any(label not in candidates for label in selected):
            failures.append(f"unknown_candidate_label:{index}")
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
                if not isinstance(quote, str) or not quote or quote not in candidates.get(label, ""):
                    failures.append(f"evidence_not_exact_card_substring:{index}:{label}:{quote_index}")
                records.append({"variant": variant, "candidate": label, "quote": quote})
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            failures.append(f"invalid_reason:{index}")
    if sorted(observed_variants) != sorted(expected_variants):
        failures.append("variant_set_mismatch")
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_BLINDED_FULL_CARD_REVIEW_AUDIT_NOT_A_RESULT",
        "pilot_id": args.pilot_id,
        "reviewer": args.reviewer,
        "valid": not failures,
        "failures": failures,
        "records": records,
        "exclusions": [
            "No strict-gold comparison, field attribution, mask condition, selector, embedding, retrieval, score, metric, API call, or result exists.",
        ],
    }
    output = root / "audits" / f"{args.pilot_id}_{args.reviewer}_selection_review_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pilot_id": args.pilot_id, "reviewer": args.reviewer, "valid": payload["valid"]}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
