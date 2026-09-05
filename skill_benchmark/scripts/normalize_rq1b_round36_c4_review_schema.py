#!/usr/bin/env python3
"""Normalise declared C4 field aliases without changing any blind judgment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()

    original: dict[str, Any] = json.loads(args.input.read_text(encoding="utf-8"))
    revised = {
        "reviewer_id": original.get("reviewer_id"),
        "review_method": original.get("review_method"),
        "reviews": [],
    }
    changes: list[dict[str, str]] = []
    for review in original.get("reviews", []):
        if set(review) != {"review_packet_id", "card_reviews"}:
            raise SystemExit(f"unexpected_review_shape:{review.get('review_packet_id')}")
        normalised_judgments: list[dict[str, Any]] = []
        for card in review["card_reviews"]:
            allowed = {"card_label", "judgment", "adequacy", "rationale", "evidence_substrings"}
            if set(card) - allowed:
                raise SystemExit(f"unexpected_card_fields:{review.get('review_packet_id')}:{sorted(set(card) - allowed)}")
            has_judgment = "judgment" in card
            has_adequacy = "adequacy" in card
            if has_judgment == has_adequacy:
                raise SystemExit(f"ambiguous_adequacy_alias:{review.get('review_packet_id')}:{card.get('card_label')}")
            adequacy = card["judgment"] if has_judgment else card["adequacy"]
            normalised_judgments.append({
                "card_label": card.get("card_label"),
                "adequacy": adequacy,
                "rationale": card.get("rationale"),
                "evidence_snippets": card.get("evidence_substrings"),
            })
            changes.append({
                "review_packet_id": str(review.get("review_packet_id")),
                "card_label": str(card.get("card_label")),
                "input_adequacy_key": "judgment" if has_judgment else "adequacy",
                "output_adequacy_key": "adequacy",
                "input_card_collection_key": "card_reviews",
                "output_card_collection_key": "candidate_judgments",
            })
        revised["reviews"].append({
            "review_packet_id": review.get("review_packet_id"),
            "candidate_judgments": normalised_judgments,
        })
    if not revised["reviewer_id"] or revised["review_method"] != "model_assisted_blinded_review_not_human":
        raise SystemExit("unexpected_reviewer_header")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(revised, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    args.ledger.write_text(json.dumps({
        "status": "C4_ROUND36_SCHEMA_NORMALISATION_ONLY_PENDING_REVALIDATION_NOT_A_REVIEW_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "normalised_card_count": len(changes),
        "changes": changes,
        "invariant": "Only field aliases card_reviews/candidate_judgments, judgment/adequacy, and evidence_substrings/evidence_snippets were normalised. Reviewer identity, method, packet order, card order, adequacy value, rationale, and cited text are unchanged.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"reviewer_id": revised["reviewer_id"], "normalised_card_count": len(changes)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
