#!/usr/bin/env python3
"""Create a mechanical comparison of two literal-valid RQ1b V3 C4A cards.

The report exposes only source-card differences for a later source-only slot
conformance reviewer. It does not accept a card, select a candidate, create a
gold label, or run a selector.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"json_object_required:{path}")
    return value


def require_literal_pass(audit: dict[str, Any], response: dict[str, Any], label: str) -> None:
    if audit.get("status") != "RQ1B_V3_C4A_LITERAL_AUDIT_PASS":
        raise ValueError(f"literal_audit_not_pass:{label}")
    if audit.get("packet_id") != response.get("packet_id"):
        raise ValueError(f"audit_response_packet_mismatch:{label}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-response", type=Path, required=True)
    parser.add_argument("--first-audit", type=Path, required=True)
    parser.add_argument("--second-response", type=Path, required=True)
    parser.add_argument("--second-audit", type=Path, required=True)
    parser.add_argument("--comparison", type=Path, required=True)
    args = parser.parse_args()
    if args.comparison.exists():
        raise SystemExit(f"refusing_to_overwrite_comparison:{args.comparison}")

    first_response = load_object(args.first_response)
    second_response = load_object(args.second_response)
    first_audit = load_object(args.first_audit)
    second_audit = load_object(args.second_audit)
    require_literal_pass(first_audit, first_response, "first")
    require_literal_pass(second_audit, second_response, "second")
    packet_id = first_response.get("packet_id")
    if not isinstance(packet_id, str) or packet_id != second_response.get("packet_id"):
        raise SystemExit("response_packet_id_mismatch")

    first_cards = first_response.get("cards")
    second_cards = second_response.get("cards")
    if not isinstance(first_cards, dict) or not isinstance(second_cards, dict):
        raise SystemExit("cards_missing_or_not_object")
    if set(first_cards) != set(second_cards):
        raise SystemExit("candidate_label_set_mismatch")

    cells: list[dict[str, Any]] = []
    for candidate in sorted(first_cards):
        first_card = first_cards[candidate]
        second_card = second_cards[candidate]
        if not isinstance(first_card, dict) or not isinstance(second_card, dict):
            raise SystemExit(f"card_not_object:{candidate}")
        if set(first_card) != set(FIELDS) or set(second_card) != set(FIELDS):
            raise SystemExit(f"field_set_mismatch:{candidate}")
        for field in FIELDS:
            first_cell = first_card[field]
            second_cell = second_card[field]
            if not isinstance(first_cell, dict) or not isinstance(second_cell, dict):
                raise SystemExit(f"cell_not_object:{candidate}:{field}")
            first_quotes = first_cell.get("quotes")
            second_quotes = second_cell.get("quotes")
            if not isinstance(first_quotes, list) or not isinstance(second_quotes, list):
                raise SystemExit(f"quotes_not_list:{candidate}:{field}")
            cells.append(
                {
                    "candidate_label": candidate,
                    "field": field,
                    "first_status": first_cell.get("status"),
                    "second_status": second_cell.get("status"),
                    "status_agrees": first_cell.get("status") == second_cell.get("status"),
                    "first_quotes": first_quotes,
                    "second_quotes": second_quotes,
                    "quote_set_agrees": set(first_quotes) == set(second_quotes),
                }
            )

    comparable = len(cells)
    agreement = sum(cell["status_agrees"] for cell in cells)
    payload = {
        "status": "RQ1B_V3_C4A_MECHANICAL_BUILDER_COMPARISON_NOT_A_CONFORMANCE_OR_RESULT",
        "packet_id": packet_id,
        "first_response_sha256": sha256_file(args.first_response),
        "first_audit_sha256": sha256_file(args.first_audit),
        "second_response_sha256": sha256_file(args.second_response),
        "second_audit_sha256": sha256_file(args.second_audit),
        "candidate_count": len(first_cards),
        "field_count": len(FIELDS),
        "comparable_cells": comparable,
        "status_agreement_count": agreement,
        "status_agreement_rate": agreement / comparable if comparable else None,
        "cells": cells,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": "Mechanical comparison only; it does not establish slot-rule conformance, a canonical card, strict adequacy, gold, selector performance or a routing result.",
    }
    args.comparison.parent.mkdir(parents=True, exist_ok=True)
    args.comparison.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"packet_id": packet_id, "status_agreement_rate": payload["status_agreement_rate"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
