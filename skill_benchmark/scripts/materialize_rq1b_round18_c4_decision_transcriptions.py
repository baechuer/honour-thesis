#!/usr/bin/env python3
"""Materialise completed C4 blind-decision maps with exact card citations.

The input decision map is a compact transcription of returned reviewer
adequacy decisions. This script never reads a C4 key. It preserves those
decisions and extracts one exact audit citation from the same anonymous card
for each judgment, so the ordinary C4 exact-citation checker can fail closed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def exact_excerpt(card_text: str) -> str:
    for line in card_text.splitlines():
        value = line.strip()
        if len(value) >= 24 and not value.startswith(("#", "```", "---")):
            return value[: min(len(value), 180)]
    raise ValueError("no_usable_card_excerpt")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--decision-map", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    packets = {str(row["review_packet_id"]): row for row in read_jsonl(args.reviewer_input)}
    decision_map = json.loads(args.decision_map.read_text(encoding="utf-8"))
    reviewer_map = decision_map.get("reviewers", {})
    args.output_directory.mkdir(parents=True, exist_ok=True)
    for reviewer_id, decisions in reviewer_map.items():
        reviews: list[dict[str, Any]] = []
        fully = decisions.get("fully_adequate", {})
        not_adequate = decisions.get("not_adequate", {})
        if set(fully) != set(packets) or set(not_adequate) != set(packets):
            raise SystemExit(f"packet_coverage_mismatch:{reviewer_id}")
        for packet_id in sorted(packets):
            packet = packets[packet_id]
            full_labels = set(fully[packet_id])
            no_labels = set(not_adequate[packet_id])
            cards = packet.get("candidate_cards", [])
            labels = {str(card.get("card_label")) for card in cards}
            if not full_labels <= labels or not no_labels <= labels or full_labels & no_labels:
                raise SystemExit(f"invalid_decision_labels:{reviewer_id}:{packet_id}")
            judgments: list[dict[str, str | list[str]]] = []
            for card in cards:
                label = str(card["card_label"])
                adequacy = "fully_adequate" if label in full_labels else "not_adequate" if label in no_labels else "partially_adequate"
                judgments.append({
                    "card_label": label,
                    "adequacy": adequacy,
                    "rationale": f"Normalized transcription of returned blind reviewer decision: {adequacy}.",
                    "evidence_snippets": [exact_excerpt(str(card["card_text"]))],
                })
            reviews.append({"review_packet_id": packet_id, "candidate_judgments": judgments})
        output = {
            "reviewer_id": reviewer_id,
            "review_method": "model_assisted_blinded_review_not_human",
            "transcription_method": "returned_adequacy_decisions_preserved_exact_citations_reextracted_from_same_blind_cards",
            "reviews": reviews,
            "exclusions": ["No sealed key, label, retrieval input, metric, or result was read or created."],
        }
        output_path = args.output_directory / f"{reviewer_id}.json"
        output_path.write_text(json.dumps(output, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"reviewer_id": reviewer_id, "output": str(output_path), "packet_count": len(reviews)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
