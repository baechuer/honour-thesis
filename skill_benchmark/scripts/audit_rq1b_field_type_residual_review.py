#!/usr/bin/env python3
"""Validate one anonymous RQ1b source-card residual-redundancy review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LABELS = {"none", "partial", "substantial"}
FIELDS = {
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
}


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
    packet = load_object(root / "residual_packets" / f"{args.pilot_id}.json")
    response_path = root / "residual_reviews" / args.reviewer / f"{args.pilot_id}.json"
    failures: list[str] = []
    try:
        response = load_object(response_path)
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("pilot_id") != args.pilot_id:
        failures.append("pilot_id_mismatch")
    expected = {(item["candidate"], item["field"]) for item in packet["targets"]}
    candidate_cards = {item["label"]: item["field_card"] for item in packet["candidates"]}
    rows = response.get("candidate_assessments") if isinstance(response.get("candidate_assessments"), list) else []
    observed = [(row.get("candidate"), row.get("field")) for row in rows if isinstance(row, dict)]
    if len(observed) != len(set(observed)):
        failures.append("duplicate_candidate_field_assessment")
    if set(observed) != expected:
        failures.append("candidate_field_target_set_mismatch")
    records = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"row_not_object:{index}")
            continue
        candidate = row.get("candidate")
        field = row.get("field")
        label = row.get("residual_label")
        evidence = row.get("remaining_slot_evidence")
        if label not in LABELS:
            failures.append(f"invalid_residual_label:{index}")
        if not isinstance(evidence, list):
            failures.append(f"invalid_remaining_slot_evidence:{index}")
            evidence = []
        if label == "none" and evidence:
            failures.append(f"none_with_remaining_evidence:{index}")
        if label in {"partial", "substantial"} and not evidence:
            failures.append(f"residual_without_remaining_evidence:{index}")
        for evidence_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                failures.append(f"evidence_not_object:{index}:{evidence_index}")
                continue
            other_field = item.get("field")
            quotes = item.get("quotes")
            if other_field not in FIELDS or other_field == field:
                failures.append(f"invalid_other_field:{index}:{evidence_index}")
            if not isinstance(quotes, list) or not quotes:
                failures.append(f"invalid_other_field_quotes:{index}:{evidence_index}")
                continue
            for quote_index, quote in enumerate(quotes):
                if not isinstance(quote, str) or not quote or quote not in candidate_cards.get(candidate, ""):
                    failures.append(f"evidence_not_exact_card_substring:{index}:{evidence_index}:{quote_index}")
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            failures.append(f"invalid_reason:{index}")
        records.append({"candidate": candidate, "field": field, "residual_label": label})
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_SOURCE_CARD_RESIDUAL_REVIEW_AUDIT_NOT_A_RESULT",
        "pilot_id": args.pilot_id,
        "reviewer": args.reviewer,
        "valid": not failures,
        "failures": failures,
        "records": records,
        "exclusions": [
            "No prompt, gold label, field attribution, selector, embedding, retrieval, score, metric, API call, or result exists.",
        ],
    }
    output = root / "audits" / f"{args.pilot_id}_{args.reviewer}_residual_review_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pilot_id": args.pilot_id, "reviewer": args.reviewer, "valid": payload["valid"]}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
