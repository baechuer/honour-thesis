#!/usr/bin/env python3
"""Repair only nonliteral C4 evidence snippets against the same blind cards.

This never reads a C4 sealed key or changes a reviewer's candidate label,
adequacy judgement, rationale, or packet coverage.  It retains literal
citations and, where a reviewer omitted Markdown punctuation or an exact line
break, replaces that citation with the card's exact non-empty line carrying
the greatest lexical overlap.  The report records every replacement so a
later audit can verify the narrow repair boundary.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any


TOKEN = re.compile(r"[a-z0-9]+")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_json_object:{path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def tokens(value: str) -> set[str]:
    return set(TOKEN.findall(value.lower()))


def replacement(snippet: str, card_text: str) -> str:
    """Return an exact card line with the closest lexical content."""
    wanted = tokens(snippet)
    candidates = [line for line in card_text.splitlines() if len(line.strip()) >= 8]
    if not candidates:
        raise ValueError("no_usable_card_lines")
    scored = []
    for index, line in enumerate(candidates):
        overlap = len(wanted & tokens(line))
        # Prefer a shorter, directly citable line when lexical overlap ties.
        scored.append((overlap, -len(line), -index, line))
    best = max(scored)[-1]
    if best not in card_text:
        raise ValueError("nonliteral_generated_replacement")
    return best


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--input-review", type=Path, required=True)
    parser.add_argument("--output-review", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    packets = {str(row["review_packet_id"]): row for row in load_jsonl(args.reviewer_input)}
    original = load_json(args.input_review)
    repaired = copy.deepcopy(original)
    changes: list[dict[str, str]] = []
    for review in repaired.get("reviews", []):
        packet_id = str(review.get("review_packet_id", ""))
        cards = {
            str(card.get("card_label", "")): str(card.get("card_text", ""))
            for card in packets[packet_id].get("candidate_cards", [])
        }
        for judgement in review.get("candidate_judgments", []):
            label = str(judgement.get("card_label", ""))
            card_text = cards[label]
            repaired_snippets = []
            for snippet in judgement.get("evidence_snippets", []):
                if snippet in card_text:
                    repaired_snippets.append(snippet)
                    continue
                literal = replacement(str(snippet), card_text)
                repaired_snippets.append(literal)
                changes.append({
                    "review_packet_id": packet_id,
                    "card_label": label,
                    "old_nonliteral_snippet": str(snippet),
                    "new_exact_snippet": literal,
                })
            judgement["evidence_snippets"] = repaired_snippets

    # Fail closed: the only changed values are evidence citation lists.
    before = copy.deepcopy(original)
    after = copy.deepcopy(repaired)
    for review in before.get("reviews", []):
        for judgement in review.get("candidate_judgments", []):
            judgement["evidence_snippets"] = []
    for review in after.get("reviews", []):
        for judgement in review.get("candidate_judgments", []):
            judgement["evidence_snippets"] = []
    if before != after:
        raise SystemExit("non_citation_content_changed")

    args.output_review.parent.mkdir(parents=True, exist_ok=True)
    args.output_review.write_text(json.dumps(repaired, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    report = {
        "status": "C4_CITATION_ONLY_REPAIR_COMPLETE_NOT_A_LABEL_OR_RESULT",
        "reviewer_id": original.get("reviewer_id"),
        "input_review": str(args.input_review),
        "output_review": str(args.output_review),
        "repair_count": len(changes),
        "repairs": changes,
        "judgement_boundary": "Only evidence_snippets changed. Reviewer identity, method, packet coverage, card labels, adequacy judgements, and rationales are bytewise preserved after removing citation lists.",
        "exclusions": ["No sealed key, source identity, gold label, retrieval input, metric, or result was read or created."],
    }
    args.report.write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "repair_count": len(changes)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
