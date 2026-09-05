#!/usr/bin/env python3
"""Repair the two known non-exact C4R30 reviewer-B evidence citations only."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


REPAIRS = {
    (
        "C4R30-008",
        "Candidate C",
        "provide a comprehensive ASO health audit",
    ): "Your goal is to perform a comprehensive ASO health audit and provide a prioritized action plan.",
    (
        "C4R30-015",
        "Candidate A",
        "收件人关系：上级 / 同事 / 客户 / 供应商",
    ): "**收件人关系**：上级 / 同事 / 客户 / 供应商 / 技术支持团队 / 教授 / 陌生人",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()

    review = json.loads(args.review.read_text(encoding="utf-8"))
    revised = copy.deepcopy(review)
    cards = {
        (packet["review_packet_id"], card["card_label"]): card["card_text"]
        for packet in (json.loads(line) for line in args.reviewer_input.read_text(encoding="utf-8").splitlines() if line.strip())
        for card in packet["candidate_cards"]
    }
    applied = []
    for packet in revised["reviews"]:
        for judgment in packet["candidate_judgments"]:
            card_text = cards[(packet["review_packet_id"], judgment["card_label"])]
            new_snippets = []
            for snippet in judgment["evidence_snippets"]:
                key = (packet["review_packet_id"], judgment["card_label"], snippet)
                replacement = REPAIRS.get(key, snippet)
                if replacement not in card_text:
                    raise SystemExit(f"replacement_not_exact:{key}:{replacement}")
                if replacement != snippet:
                    applied.append({
                        "review_packet_id": key[0],
                        "card_label": key[1],
                        "old_evidence": snippet,
                        "new_exact_evidence": replacement,
                    })
                new_snippets.append(replacement)
            judgment["evidence_snippets"] = new_snippets
    if len(applied) != len(REPAIRS):
        raise SystemExit(f"repair_coverage_mismatch:{len(applied)}:expected:{len(REPAIRS)}")

    args.output.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger = {
        "status": "C4R30_CITATION_EXACTNESS_REPAIR_ONLY_NOT_A_REVIEW_OR_LABEL",
        "input_review": str(args.review),
        "input_sha256": sha256(args.review),
        "output_review": str(args.output),
        "output_sha256": sha256(args.output),
        "repairs": applied,
        "not_changed": ["reviewer_id", "review_method", "adequacy", "rationale", "packet coverage"],
    }
    args.ledger.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": ledger["status"], "repair_count": len(applied)}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
