#!/usr/bin/env python3
"""Repair only non-literal C4 evidence snippets against blinded candidate cards.

The completed blinded judgements remain immutable in substance. This utility
creates new reviewer files containing the same reviewers, adequacy decisions,
and rationales, while replacing a non-exact evidence quotation with the best
matching literal line from the card. An audit log records every replacement.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_object:{path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def tokens(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower())


def exact_lines(card_text: str) -> list[str]:
    lines = [line.strip() for line in card_text.splitlines() if line.strip()]
    return lines or [card_text]


def literal_replacement(snippet: str, card_text: str) -> str:
    if snippet in card_text:
        return snippet
    wanted = tokens(snippet)
    if not wanted:
        raise ValueError("evidence_without_tokens")
    wanted_set = set(wanted)
    candidates: list[tuple[tuple[int, int, int], str]] = []
    for line in exact_lines(card_text):
        line_tokens = tokens(line)
        overlap = len(wanted_set.intersection(line_tokens))
        sequence = 0
        for width in range(min(len(wanted), len(line_tokens)), 0, -1):
            if any(wanted[start : start + width] == line_tokens[offset : offset + width]
                   for start in range(len(wanted) - width + 1)
                   for offset in range(len(line_tokens) - width + 1)):
                sequence = width
                break
        if overlap:
            candidates.append(((sequence, overlap, -len(line)), line))
    if not candidates:
        raise ValueError(f"no_literal_evidence_match:{snippet}")
    replacement = max(candidates, key=lambda item: item[0])[1]
    if replacement not in card_text:
        raise ValueError("replacement_not_literal")
    return replacement


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--review", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packets = {str(packet["review_packet_id"]): packet for packet in read_jsonl(args.reviewer_input)}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    audit_rows: list[dict[str, str]] = []
    for review_path in args.review:
        review = read_json(review_path)
        for review_item in review.get("reviews", []):
            packet = packets[str(review_item["review_packet_id"])]
            cards = {str(card["card_label"]): str(card["card_text"]) for card in packet["candidate_cards"]}
            for judgement in review_item["candidate_judgments"]:
                card_text = cards[str(judgement["card_label"])]
                repaired: list[str] = []
                for snippet in judgement["evidence_snippets"]:
                    replacement = literal_replacement(str(snippet), card_text)
                    repaired.append(replacement)
                    if replacement != snippet:
                        audit_rows.append({
                            "reviewer_id": str(review["reviewer_id"]),
                            "review_packet_id": str(review_item["review_packet_id"]),
                            "card_label": str(judgement["card_label"]),
                            "original_snippet": str(snippet),
                            "literal_replacement": replacement,
                            "repair_scope": "citation_only_no_adequacy_or_rationale_change",
                        })
                judgement["evidence_snippets"] = repaired
        output = args.output_dir / review_path.name
        output.write_text(json.dumps(review, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    args.audit.write_text(json.dumps(audit_rows, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"citation_repairs": len(audit_rows), "review_files": len(args.review)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
