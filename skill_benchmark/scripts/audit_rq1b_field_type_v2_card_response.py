#!/usr/bin/env python3
"""Literal audit for one composition-keyed RQ1b v2 source-card response."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


FIELDS = (
    "use_condition", "input_precondition", "output_artifact",
    "workflow_procedure", "success_verification", "boundary_not_for",
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
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--composition-id", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    root, composition_id = args.root, args.composition_id
    packet = json.loads((root / composition_id / "field_card_builder_packet.json").read_text())
    response_path = root / "builder_responses" / args.reviewer / f"{composition_id}.json"
    failures: list[str] = []
    warnings: list[str] = []
    records: list[dict] = []
    try:
        response = json.loads(response_path.read_text())
    except Exception as error:
        response = {}
        failures.append(f"json_parse_or_missing:{error}")
    if response.get("composition_id") != composition_id:
        failures.append("composition_id_mismatch")
    expected_labels = [candidate["label"] for candidate in packet["candidates"]]
    cards = response.get("cards")
    if not isinstance(cards, dict) or set(cards) != set(expected_labels):
        failures.append("candidate_labels_mismatch")
        cards = cards if isinstance(cards, dict) else {}
    source_text = {}
    for candidate in packet["candidates"]:
        label = candidate["label"]
        path = root / composition_id / candidate["text_path"]
        if not path.is_file():
            failures.append(f"missing_packet_source:{label}")
            continue
        if sha256(path) != candidate["source_sha256"]:
            failures.append(f"packet_source_hash_mismatch:{label}")
        source_text[label] = path.read_text()
    for label in expected_labels:
        card = cards.get(label)
        if not isinstance(card, dict) or set(card) != set(FIELDS):
            failures.append(f"field_schema_mismatch:{label}")
            continue
        seen_quotes = {}
        for field in FIELDS:
            cell = card[field]
            if not isinstance(cell, dict) or set(cell) != {"status", "quotes"}:
                failures.append(f"cell_schema_mismatch:{label}:{field}")
                continue
            status, quotes = cell["status"], cell["quotes"]
            if status not in {"EVIDENCE", "NOT_STATED"}:
                failures.append(f"invalid_status:{label}:{field}")
            if not isinstance(quotes, list) or not all(isinstance(value, str) for value in quotes):
                failures.append(f"invalid_quotes:{label}:{field}")
                continue
            if status == "EVIDENCE" and not quotes:
                failures.append(f"evidence_without_quote:{label}:{field}")
            if status == "NOT_STATED" and quotes:
                failures.append(f"not_stated_with_quote:{label}:{field}")
            for quote_index, quote in enumerate(quotes):
                source = source_text.get(label, "")
                if not quote or quote not in source:
                    failures.append(f"quote_not_exact:{label}:{field}:{quote_index}")
                else:
                    if source.find(quote) < frontmatter_end(source):
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
    payload = {"status": "RQ1B_FIELD_TYPE_ABLATION_V2_LITERAL_CARD_AUDIT_NOT_A_RESULT", "composition_id": composition_id, "reviewer": args.reviewer, "valid": not failures, "failures": failures, "warnings": warnings, "record_count": len(records), "records": records, "exclusions": ["No canonical card, mask, selector, embedding, retrieval, API call, score, metric, or result exists."]}
    output = root / "audits" / f"{composition_id}_{args.reviewer}_literal_audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "valid": payload["valid"], "record_count": len(records)}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
