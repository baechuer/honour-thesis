#!/usr/bin/env python3
"""Literal audit for one independent RQ1b field-type source-card response.

This is a local transcription/schema check only. It does not choose a card,
unseal a prompt or gold label, build a mask, or produce any selector result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter_end(text: str) -> int:
    if not text.startswith("---\n"):
        return 0
    marker = text.find("\n---\n", 4)
    return 0 if marker < 0 else marker + 5


def heading_only(quote: str) -> bool:
    lines = [line for line in quote.splitlines() if line.strip()]
    return bool(lines) and all(line.lstrip().startswith("#") for line in lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()

    family_dir = args.pilot_root / args.pilot_id
    packet = json.loads((family_dir / "field_card_builder_packet.json").read_text())
    response_path = args.pilot_root / "builder_responses" / args.reviewer / f"{args.pilot_id}.json"
    failures: list[str] = []
    warnings: list[str] = []
    records: list[dict] = []
    try:
        response = json.loads(response_path.read_text())
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")

    if response.get("pilot_id") != args.pilot_id:
        failures.append("pilot_id_mismatch")
    expected_labels = [candidate["label"] for candidate in packet["candidates"]]
    cards = response.get("cards")
    if not isinstance(cards, dict) or set(cards) != set(expected_labels):
        failures.append("candidate_labels_mismatch")
        cards = cards if isinstance(cards, dict) else {}

    source_text: dict[str, str] = {}
    for candidate in packet["candidates"]:
        source_path = family_dir / candidate["text_path"]
        label = candidate["label"]
        if not source_path.is_file():
            failures.append(f"missing_packet_source:{label}")
            continue
        if sha256(source_path) != candidate["source_sha256"]:
            failures.append(f"packet_source_hash_mismatch:{label}")
        source_text[label] = source_path.read_text()

    for label in expected_labels:
        card = cards.get(label)
        if not isinstance(card, dict) or set(card) != set(FIELDS):
            failures.append(f"field_schema_mismatch:{label}")
            continue
        seen_quotes: dict[str, str] = {}
        for field in FIELDS:
            cell = card[field]
            if not isinstance(cell, dict) or set(cell) != {"status", "quotes"}:
                failures.append(f"cell_schema_mismatch:{label}:{field}")
                continue
            status = cell["status"]
            quotes = cell["quotes"]
            if status not in {"EVIDENCE", "NOT_STATED"}:
                failures.append(f"invalid_status:{label}:{field}")
            if not isinstance(quotes, list) or not all(isinstance(item, str) for item in quotes):
                failures.append(f"invalid_quotes:{label}:{field}")
                continue
            if status == "EVIDENCE" and not quotes:
                failures.append(f"evidence_without_quote:{label}:{field}")
            if status == "NOT_STATED" and quotes:
                failures.append(f"not_stated_with_quote:{label}:{field}")
            for quote_index, quote in enumerate(quotes):
                text = source_text.get(label, "")
                if not quote or quote not in text:
                    failures.append(f"quote_not_exact:{label}:{field}:{quote_index}")
                else:
                    if text.find(quote) < frontmatter_end(text):
                        failures.append(f"frontmatter_quote:{label}:{field}:{quote_index}")
                    if heading_only(quote):
                        failures.append(f"heading_only_quote:{label}:{field}:{quote_index}")
                    if URL_RE.search(quote):
                        failures.append(f"url_quote:{label}:{field}:{quote_index}")
                    if quote in seen_quotes:
                        warnings.append(f"cross_slot_quote_reuse:{label}:{seen_quotes[quote]}:{field}")
                    else:
                        seen_quotes[quote] = field
                records.append({"candidate": label, "field": field, "status": status, "quote": quote})

    output = args.pilot_root / "audits" / f"{args.pilot_id}_{args.reviewer}_literal_audit.json"
    output.parent.mkdir(exist_ok=True)
    payload = {
        "status": "RQ1B_FIELD_TYPE_ABLATION_LITERAL_CARD_AUDIT_NOT_A_RESULT",
        "pilot_id": args.pilot_id,
        "reviewer": args.reviewer,
        "valid": not failures,
        "failures": failures,
        "warnings": warnings,
        "record_count": len(records),
        "records": records,
        "exclusions": [
            "No canonical card, mask, selector, embedding, retrieval, API call, score, metric, or result exists.",
        ],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "valid": payload["valid"], "record_count": len(records)}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
