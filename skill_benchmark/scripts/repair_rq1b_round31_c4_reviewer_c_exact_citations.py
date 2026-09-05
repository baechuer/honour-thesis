#!/usr/bin/env python3
"""Repair two non-exact Round 31 C4 reviewer-C citations only."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


REVIEW = Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/c4_round31_reviewer_C_2026-08-28.json")
INPUT = Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/c4_round31_blind_reviewer_input_half_01")
OUTPUT = Path("skill_benchmark/rq1b_cross_source_public_benchmark/working/c4_round31_reviewer_C_citation_exact_v2_2026-08-28.json")
LEDGER = Path("skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round31_reviewer_C_citation_repair_2026-08-28.json")
REPAIRS = {
    ("C4R31-015", "Candidate B", "Prioritize the findings that actually matter"): "wrong logic, off-by-one, inverted conditions",
    ("C4R31-019", "Candidate D", "flag the risk rather than assuming failure"): "flag the *risk* rather than assuming failure",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    cards = {
        (packet["review_packet_id"], card["card_label"]): card["card_text"]
        for packet in (json.loads(line) for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip())
        for card in packet["candidate_cards"]
    }
    revised = copy.deepcopy(review)
    applied: list[dict[str, str]] = []
    for packet in revised["reviews"]:
        packet_id = packet["review_packet_id"]
        for judgment in packet["candidate_judgments"]:
            card_label = judgment["card_label"]
            card = cards[(packet_id, card_label)]
            repaired: list[str] = []
            for evidence in judgment["evidence_snippets"]:
                replacement = REPAIRS.get((packet_id, card_label, evidence), evidence)
                if replacement not in card:
                    raise SystemExit(f"replacement_not_exact:{packet_id}:{card_label}:{replacement}")
                if replacement != evidence:
                    applied.append({"review_packet_id": packet_id, "card_label": card_label, "old_evidence": evidence, "new_exact_evidence": replacement})
                repaired.append(replacement)
            judgment["evidence_snippets"] = repaired
    if len(applied) != len(REPAIRS):
        raise SystemExit(f"repair_coverage:{len(applied)}")
    OUTPUT.write_text(json.dumps(revised, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    ledger = {
        "status": "C4_CITATION_EXACTNESS_REPAIR_ONLY_NOT_A_REVIEW_OR_LABEL",
        "purpose": "Replace only two failed evidence snippets with exact text from the same anonymous cards.",
        "not_changed": ["reviewer_id", "review_method", "adequacy", "rationale", "packet coverage"],
        "input_review": str(REVIEW),
        "input_sha256": sha256(REVIEW),
        "output_review": str(OUTPUT),
        "output_sha256": sha256(OUTPUT),
        "repairs": applied,
    }
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"repairs": len(applied), "output_sha256": ledger["output_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
