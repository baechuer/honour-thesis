#!/usr/bin/env python3
"""Compare two valid independent RQ1b-S field-card builders.

This is a schema/status agreement report. It makes no source-card acceptance,
gold, mask, selector, or scientific decision.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "boundary_not_for",
    "dependency_resource",
    "success_verification",
)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--first-reviewer", required=True)
    parser.add_argument("--second-reviewer", required=True)
    args = parser.parse_args()

    first_audit = load_json(args.pilot_root / "audits" / f"{args.pilot_id}_{args.first_reviewer}_literal_audit.json")
    second_audit = load_json(args.pilot_root / "audits" / f"{args.pilot_id}_{args.second_reviewer}_literal_audit.json")
    first_response = load_json(args.pilot_root / "reviews" / args.first_reviewer / f"{args.pilot_id}.json")
    second_response = load_json(args.pilot_root / "reviews" / args.second_reviewer / f"{args.pilot_id}.json")

    comparison = []
    valid = bool(first_audit.get("valid")) and bool(second_audit.get("valid"))
    if set(first_response.get("cards", {})) != set(second_response.get("cards", {})):
        valid = False
        comparison.append({"issue": "candidate_labels_mismatch"})
    else:
        for candidate in sorted(first_response["cards"]):
            for field in FIELDS:
                first_status = first_response["cards"][candidate][field]["status"]
                second_status = second_response["cards"][candidate][field]["status"]
                comparison.append(
                    {
                        "candidate": candidate,
                        "field": field,
                        "first_status": first_status,
                        "second_status": second_status,
                        "status_agrees": first_status == second_status,
                        "first_quote_count": len(first_response["cards"][candidate][field]["quotes"]),
                        "second_quote_count": len(second_response["cards"][candidate][field]["quotes"]),
                    }
                )

    agreement_count = sum(item.get("status_agrees", False) for item in comparison)
    comparable_count = sum("status_agrees" in item for item in comparison)
    payload = {
        "status": "RQ1B_S_INDEPENDENT_CARD_STATUS_COMPARISON_NOT_AN_ACCEPTANCE_OR_RESULT",
        "pilot_id": args.pilot_id,
        "first_reviewer": args.first_reviewer,
        "second_reviewer": args.second_reviewer,
        "both_literal_valid": bool(first_audit.get("valid")) and bool(second_audit.get("valid")),
        "comparable_cells": comparable_count,
        "status_agreement_count": agreement_count,
        "status_agreement_rate": agreement_count / comparable_count if comparable_count else None,
        "comparison": comparison,
        "exclusions": [
            "No source-card acceptance, target neutralisation, sham neutralisation, selector, embedding, retrieval, API call, score, metric, or result is created.",
        ],
    }
    output = args.pilot_root / "audits" / f"{args.pilot_id}_{args.first_reviewer}_vs_{args.second_reviewer}_comparison.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "both_literal_valid": payload["both_literal_valid"], "status_agreement_rate": payload["status_agreement_rate"]}, sort_keys=True))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
