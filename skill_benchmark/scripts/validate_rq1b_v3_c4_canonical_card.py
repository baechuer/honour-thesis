#!/usr/bin/env python3
"""Validate that a C4A canonical proposal uses only literal-valid evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from validate_rq1b_v3_c4_field_cards import FIELDS, URL_RE, identity_lines, quote_contains_identity_line, sha256_file


ACCEPT = "RQ1B_V3_C4A_CONFORMANCE_ACCEPT_CANONICAL_CARD_NOT_A_RESULT"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"json_object_required:{path}")
    return value


def literal_pass(audit: dict[str, Any], response: dict[str, Any], name: str) -> str | None:
    if audit.get("status") != "RQ1B_V3_C4A_LITERAL_AUDIT_PASS":
        return f"literal_audit_not_pass:{name}"
    if audit.get("packet_id") != response.get("packet_id"):
        return f"audit_response_packet_mismatch:{name}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--first-response", type=Path, required=True)
    parser.add_argument("--first-audit", type=Path, required=True)
    parser.add_argument("--second-response", type=Path, required=True)
    parser.add_argument("--second-audit", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.audit.exists():
        raise SystemExit(f"refusing_to_overwrite_audit:{args.audit}")

    packet = load(args.packet)
    proposal = load(args.proposal)
    first_response = load(args.first_response)
    second_response = load(args.second_response)
    first_audit = load(args.first_audit)
    second_audit = load(args.second_audit)
    packet_id = packet.get("packet_id")
    failures = [failure for failure in (
        literal_pass(first_audit, first_response, "first"),
        literal_pass(second_audit, second_response, "second"),
    ) if failure]
    if proposal.get("packet_id") != packet_id:
        failures.append("proposal_packet_id_mismatch")
    if proposal.get("status") != ACCEPT:
        failures.append("proposal_not_canonical_accept")
    if first_response.get("packet_id") != packet_id or second_response.get("packet_id") != packet_id:
        failures.append("builder_packet_id_mismatch")

    candidates = {item["label"]: item for item in packet.get("candidates", [])}
    cards = proposal.get("cards")
    first_cards = first_response.get("cards") if isinstance(first_response.get("cards"), dict) else {}
    second_cards = second_response.get("cards") if isinstance(second_response.get("cards"), dict) else {}
    if not isinstance(cards, dict) or set(cards) != set(candidates):
        failures.append("canonical_candidate_set_mismatch")
        cards = cards if isinstance(cards, dict) else {}

    findings: list[dict[str, Any]] = []
    packet_dir = args.packet.parent
    for label, candidate in candidates.items():
        source_path = packet_dir / candidate["text_path"]
        source = source_path.read_text(encoding="utf-8")
        if sha256_file(source_path) != candidate["source_sha256"]:
            failures.append(f"source_hash_mismatch:{label}")
        card = cards.get(label)
        if not isinstance(card, dict) or set(card) != set(FIELDS):
            failures.append(f"field_set_mismatch:{label}")
            continue
        blocked = identity_lines(source)
        for field in FIELDS:
            cell = card[field]
            cell_failures: list[str] = []
            if not isinstance(cell, dict) or set(cell) != {"status", "quotes"}:
                cell_failures.append("cell_schema")
            else:
                status = cell["status"]
                quotes = cell["quotes"]
                if status not in {"EVIDENCE", "NOT_STATED"}:
                    cell_failures.append("invalid_status")
                elif not isinstance(quotes, list) or not all(isinstance(quote, str) for quote in quotes):
                    cell_failures.append("quotes_not_string_list")
                elif (status == "EVIDENCE" and not quotes) or (status == "NOT_STATED" and quotes):
                    cell_failures.append("status_quote_mismatch")
                else:
                    permitted = set(first_cards.get(label, {}).get(field, {}).get("quotes", [])) | set(second_cards.get(label, {}).get(field, {}).get("quotes", []))
                    for index, quote in enumerate(quotes):
                        if not quote.strip():
                            cell_failures.append(f"blank_quote:{index}")
                        elif quote not in source:
                            cell_failures.append(f"nonliteral_quote:{index}")
                        elif quote_contains_identity_line(quote, blocked):
                            cell_failures.append(f"identity_line_quote:{index}")
                        elif URL_RE.search(quote):
                            cell_failures.append(f"url_quote:{index}")
                        elif quote not in permitted:
                            cell_failures.append(f"quote_not_from_literal_valid_builder:{index}")
            findings.append({"candidate_label": label, "field": field, "failures": cell_failures})
            failures.extend(f"{label}:{field}:{failure}" for failure in cell_failures)

    payload = {
        "status": "RQ1B_V3_C4A_CANONICAL_CARD_AUDIT_PASS" if not failures else "RQ1B_V3_C4A_CANONICAL_CARD_AUDIT_FAIL",
        "packet_id": packet_id,
        "packet_sha256": sha256_file(args.packet),
        "proposal_sha256": sha256_file(args.proposal),
        "first_response_sha256": sha256_file(args.first_response),
        "second_response_sha256": sha256_file(args.second_response),
        "findings": findings,
        "failures": failures,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": "Canonical-card fidelity audit only; it does not establish slot completeness, strict adequacy, gold, selector performance or routing.",
    }
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    args.audit.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"packet_id": packet_id, "failures": len(failures), "status": payload["status"]}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
