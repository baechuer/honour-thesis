#!/usr/bin/env python3
"""Literal-validation gate for an RQ1b V3 C4A anonymous field-card response.

Checks exact source-substring fidelity and identity-line exclusion only. It does
not assess slot placement, selection adequacy, gold labels or retrieval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
URL_RE = re.compile(r"https?://|www\\.", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity_lines(text: str) -> set[str]:
    """Return frontmatter and heading lines that must not appear in a card quote."""
    lines = text.splitlines()
    blocked: set[str] = set()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            blocked.add(lines[index])
            if lines[index].strip() == "---":
                break
        blocked.add(lines[0])
    for line in lines:
        if line.lstrip().startswith("#"):
            blocked.add(line)
    return blocked


def quote_contains_identity_line(quote: str, blocked: set[str]) -> bool:
    return any(line in blocked for line in quote.splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.audit.exists():
        raise SystemExit(f"refusing_to_overwrite_audit:{args.audit}")
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    response = json.loads(args.response.read_text(encoding="utf-8"))
    if response.get("packet_id") != packet.get("packet_id"):
        raise SystemExit("packet_id_mismatch")
    cards = response.get("cards")
    if not isinstance(cards, dict):
        raise SystemExit("cards_missing_or_not_object")
    packet_dir = args.packet.parent
    expected = {item["label"]: item for item in packet["candidates"]}
    findings: list[dict[str, Any]] = []
    failures: list[str] = []
    if set(cards) != set(expected):
        failures.append("candidate_label_set_mismatch")
    for label, candidate in expected.items():
        source_path = packet_dir / candidate["text_path"]
        source_text = source_path.read_text(encoding="utf-8")
        if sha256_file(source_path) != candidate["source_sha256"]:
            failures.append(f"source_hash_mismatch:{label}")
        card = cards.get(label)
        if not isinstance(card, dict) or set(card) != set(FIELDS):
            failures.append(f"field_set_mismatch:{label}")
            continue
        blocked = identity_lines(source_text)
        for field in FIELDS:
            cell = card[field]
            cell_failures: list[str] = []
            if not isinstance(cell, dict) or set(cell) != {"status", "quotes"}:
                cell_failures.append("cell_schema")
            else:
                status, quotes = cell["status"], cell["quotes"]
                if status not in {"EVIDENCE", "NOT_STATED"}:
                    cell_failures.append("invalid_status")
                if not isinstance(quotes, list) or not all(isinstance(quote, str) for quote in quotes):
                    cell_failures.append("quotes_not_string_list")
                elif status == "EVIDENCE" and not quotes:
                    cell_failures.append("evidence_without_quote")
                elif status == "NOT_STATED" and quotes:
                    cell_failures.append("not_stated_with_quote")
                else:
                    for index, quote in enumerate(quotes):
                        if not quote.strip():
                            cell_failures.append(f"blank_quote:{index}")
                        elif quote not in source_text:
                            cell_failures.append(f"nonliteral_quote:{index}")
                        elif quote_contains_identity_line(quote, blocked):
                            cell_failures.append(f"identity_line_quote:{index}")
                        elif URL_RE.search(quote):
                            cell_failures.append(f"url_quote:{index}")
            if cell_failures:
                failures.extend(f"{label}:{field}:{item}" for item in cell_failures)
            findings.append({"candidate_label": label, "field": field, "failures": cell_failures})
    audit = {
        "status": "RQ1B_V3_C4A_LITERAL_AUDIT_PASS" if not failures else "RQ1B_V3_C4A_LITERAL_AUDIT_FAIL",
        "packet_id": packet["packet_id"],
        "packet_sha256": sha256_file(args.packet),
        "response_sha256": sha256_file(args.response),
        "field_count": len(FIELDS),
        "candidate_count": len(expected),
        "findings": findings,
        "failures": failures,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": "Literal audit only; it does not establish slot placement, card preservation, strict gold, adequacy, selector performance or any routing result.",
    }
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    args.audit.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"packet_id": packet["packet_id"], "failures": len(failures), "status": audit["status"]}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
