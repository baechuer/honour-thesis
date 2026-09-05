#!/usr/bin/env python3
"""Repair declared Round 36 C4 citation substrings without changing judgments."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


REPLACEMENTS = {
    (
        "R36-B", "C4R36-005", "Candidate B", "State the spec that defines its contract."
    ): "state the spec that defines its contract.",
    (
        "R36-B", "C4R36-009", "Candidate C", "before opening a Playwright session"
    ): "Skip the browser when you can",
    (
        "R36-B", "C4R36-009", "Candidate C", "one or more web pages"
    ): "one or more",
    (
        "R36-B", "C4R36-012", "Candidate C", "pull structured data off one or more web pages"
    ): "pull structured data off one or more",
    (
        "R36-B", "C4R36-014", "Candidate B", "Re-snapshot: After navigation or DOM changes"
    ): "After navigation or DOM changes, get fresh refs",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def card_texts(path: Path) -> dict[tuple[str, str], str]:
    return {
        (str(packet["review_packet_id"]), str(card["card_label"])): str(card["card_text"])
        for packet in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        for card in packet["candidate_cards"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()

    original: dict[str, Any] = json.loads(args.review.read_text(encoding="utf-8"))
    revised = copy.deepcopy(original)
    reviewer_id = str(revised.get("reviewer_id", ""))
    cards = card_texts(args.reviewer_input)
    applied: list[dict[str, str]] = []
    for review in revised.get("reviews", []):
        packet_id = str(review.get("review_packet_id", ""))
        for judgment in review.get("candidate_judgments", []):
            label = str(judgment.get("card_label", ""))
            exact: list[str] = []
            for snippet in judgment.get("evidence_snippets", []):
                replacement = REPLACEMENTS.get((reviewer_id, packet_id, label, str(snippet)), snippet)
                if replacement not in cards[(packet_id, label)]:
                    raise SystemExit(f"replacement_not_exact:{reviewer_id}:{packet_id}:{label}:{replacement}")
                if replacement != snippet:
                    applied.append({
                        "review_packet_id": packet_id,
                        "card_label": label,
                        "old_evidence": str(snippet),
                        "replacement_exact_substring": str(replacement),
                    })
                exact.append(replacement)
            judgment["evidence_snippets"] = exact
    if len(applied) != len(REPLACEMENTS):
        raise SystemExit(f"repair_coverage_mismatch:{len(applied)}:{len(REPLACEMENTS)}")

    args.output.write_text(json.dumps(revised, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    args.ledger.write_text(json.dumps({
        "status": "C4_ROUND36_CITATION_EXACTNESS_REPAIR_ONLY_PENDING_REVALIDATION_NOT_A_REVIEW_OR_LABEL",
        "input": str(args.review),
        "input_sha256": sha256(args.review),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "repairs": applied,
        "invariant": "Only five cited evidence strings were shortened or corrected to exact text from the same anonymous card. Reviewer identity, method, adequacy, rationale, packet/card coverage, and order are unchanged.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"reviewer_id": reviewer_id, "repair_count": len(applied)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
