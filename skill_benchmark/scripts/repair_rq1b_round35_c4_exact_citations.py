#!/usr/bin/env python3
"""Repair known Round 35 C4 citation substrings without changing judgments."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


REPLACEMENTS = {
    (
        "R35-A1",
        "C4R35-002",
        "Candidate B",
        "Verify the observable result with page text, URL, network evidence, and a screenshot when visual state matters.",
    ): "Verify the observable result with page text, URL, network evidence, and a",
    (
        "R35-A1",
        "C4R35-003",
        "Candidate B",
        "Verify the observable result with page text, URL, network evidence, and a screenshot when visual state matters.",
    ): "Verify the observable result with page text, URL, network evidence, and a",
    (
        "R35-A1",
        "C4R35-004",
        "Candidate B",
        "Use `kill-all` only for confirmed stale daemons because it affects unrelated sessions.",
    ): "Close the named session when finished. Use `kill-all` only for confirmed",
    (
        "R35-A1",
        "C4R35-005",
        "Candidate B",
        "Verify the observable result with page text, URL, network evidence, and a screenshot when visual state matters.",
    ): "Verify the observable result with page text, URL, network evidence, and a",
    (
        "R35-A1",
        "C4R35-009",
        "Candidate C",
        "Use a focused draft PR, state the source of truth and checks run, and never push directly to `main`.",
    ): "Use a focused draft PR, state the source of truth and checks run, and never",
    (
        "R35-A1",
        "C4R35-012",
        "Candidate C",
        "Use a focused draft PR, state the source of truth and checks run, and never push directly to `main`.",
    ): "Use a focused draft PR, state the source of truth and checks run, and never",
    (
        "R35-A3",
        "C4R35-026",
        "Candidate B",
        "`ok: false` with an `error` is a resource telling you what went wrong.",
    ): "One row per resource, holding its LAST run.",
    (
        "R35-A3",
        "C4R35-027",
        "Candidate B",
        "duplicate detection, backlog satisfiability, fabricated-return tripwires, the mega-cap canary, per-country\nsymbol coverage, and resource health.",
    ): "39 assertions as `anon` — floors on the universe, zero-CUSIP and zero-ISIN checks,",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cards(path: Path) -> dict[tuple[str, str], str]:
    return {
        (packet["review_packet_id"], card["card_label"]): card["card_text"]
        for packet in (
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
        )
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
    reviewer_id = str(revised["reviewer_id"])
    cards = read_cards(args.reviewer_input)
    expected = [key for key in REPLACEMENTS if key[0] == reviewer_id]
    applied: list[dict[str, str]] = []
    for review in revised["reviews"]:
        packet_id = str(review["review_packet_id"])
        for judgment in review["candidate_judgments"]:
            label = str(judgment["card_label"])
            card = cards[(packet_id, label)]
            repaired: list[str] = []
            for snippet in judgment["evidence_snippets"]:
                key = (reviewer_id, packet_id, label, snippet)
                replacement = REPLACEMENTS.get(key, snippet)
                if replacement not in card:
                    raise SystemExit(f"replacement_not_exact:{key}:{replacement}")
                if replacement != snippet:
                    applied.append(
                        {
                            "review_packet_id": packet_id,
                            "card_label": label,
                            "old_evidence": snippet,
                            "new_exact_evidence": replacement,
                        }
                    )
                repaired.append(replacement)
            judgment["evidence_snippets"] = repaired
    if len(applied) != len(expected):
        raise SystemExit(f"repair_coverage_mismatch:applied={len(applied)}:expected={len(expected)}")

    args.output.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger = {
        "status": "C4_R35_CITATION_EXACTNESS_REPAIR_ONLY_NOT_A_REVIEW_OR_LABEL",
        "purpose": "Replaces only known non-exact evidence snippets with exact contiguous text from the same anonymous card.",
        "not_changed": ["reviewer_id", "review_method", "adequacy", "rationale", "packet/card coverage", "ordering"],
        "input_review": str(args.review),
        "input_sha256": sha256(args.review),
        "output_review": str(args.output),
        "output_sha256": sha256(args.output),
        "repairs": applied,
    }
    args.ledger.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewer_id": reviewer_id, "repairs": len(applied), "output_sha256": ledger["output_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
