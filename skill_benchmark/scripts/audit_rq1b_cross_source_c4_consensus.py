#!/usr/bin/env python3
"""Validate blinded RQ1b C4 reviews and materialise their pre-unsealing consensus.

This is local curation bookkeeping only.  It receives the anonymous C4 cards
and two completed model-assisted reviews, but intentionally never reads a
sealed card-to-skill key.  It therefore cannot create a gold label, retrieval
input, model result, metric, or frozen benchmark packet.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ADEQUACY = {"fully_adequate", "partially_adequate", "not_adequate"}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected_json_object:{path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"expected_json_object:{path}:{line_number}")
        rows.append(value)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-input", type=Path, required=True)
    parser.add_argument("--review", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def validate_review(
    review: dict[str, Any],
    packet_by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, set[str]], list[str]]:
    reviewer_id = str(review.get("reviewer_id", ""))
    failures: list[str] = []
    if not reviewer_id:
        failures.append("missing_reviewer_id")
    if review.get("review_method") != "model_assisted_blinded_review_not_human":
        failures.append(f"unexpected_review_method:{reviewer_id}")

    review_by_packet: dict[str, dict[str, Any]] = {}
    for item in review.get("reviews", []):
        packet_id = str(item.get("review_packet_id", ""))
        if packet_id in review_by_packet:
            failures.append(f"duplicate_review_packet:{reviewer_id}:{packet_id}")
        review_by_packet[packet_id] = item
    if set(review_by_packet) != set(packet_by_id):
        missing = sorted(set(packet_by_id) - set(review_by_packet))
        extra = sorted(set(review_by_packet) - set(packet_by_id))
        failures.extend(f"missing_packet:{reviewer_id}:{packet_id}" for packet_id in missing)
        failures.extend(f"unexpected_packet:{reviewer_id}:{packet_id}" for packet_id in extra)

    fully_by_packet: dict[str, set[str]] = {}
    for packet_id, packet in packet_by_id.items():
        item = review_by_packet.get(packet_id)
        if item is None:
            continue
        cards = {str(card.get("card_label")): str(card.get("card_text", "")) for card in packet.get("candidate_cards", [])}
        judgments = item.get("candidate_judgments", [])
        judgments_by_label: dict[str, dict[str, Any]] = {}
        for judgment in judgments:
            label = str(judgment.get("card_label", ""))
            if label in judgments_by_label:
                failures.append(f"duplicate_card_judgment:{reviewer_id}:{packet_id}:{label}")
            judgments_by_label[label] = judgment
        if set(judgments_by_label) != set(cards):
            failures.append(f"card_coverage_mismatch:{reviewer_id}:{packet_id}")
            continue
        fully: set[str] = set()
        for label, card_text in cards.items():
            judgment = judgments_by_label[label]
            adequacy = str(judgment.get("adequacy", ""))
            if adequacy not in ADEQUACY:
                failures.append(f"invalid_adequacy:{reviewer_id}:{packet_id}:{label}:{adequacy}")
            if not str(judgment.get("rationale", "")).strip():
                failures.append(f"missing_rationale:{reviewer_id}:{packet_id}:{label}")
            snippets = judgment.get("evidence_snippets", [])
            if not isinstance(snippets, list) or not snippets:
                failures.append(f"missing_evidence:{reviewer_id}:{packet_id}:{label}")
            for snippet in snippets if isinstance(snippets, list) else []:
                if not isinstance(snippet, str) or not snippet or snippet not in card_text:
                    failures.append(f"non_exact_evidence:{reviewer_id}:{packet_id}:{label}:{snippet}")
            if adequacy == "fully_adequate":
                fully.add(label)
        fully_by_packet[packet_id] = fully
    return fully_by_packet, failures


def main() -> int:
    args = parse_args()
    if len(args.review) != 2:
        raise SystemExit("requires_exactly_two_reviews")
    packets = read_jsonl(args.reviewer_input)
    packet_by_id = {str(packet.get("review_packet_id")): packet for packet in packets}
    if len(packet_by_id) != len(packets):
        raise SystemExit("duplicate_reviewer_input_packet")

    reviews = [read_json(path) for path in args.review]
    reviewer_ids = [str(review.get("reviewer_id", "")) for review in reviews]
    failures: list[str] = []
    if len(set(reviewer_ids)) != 2:
        failures.append("reviewer_ids_not_distinct")
    validated = [validate_review(review, packet_by_id) for review in reviews]
    failures.extend(problem for _, problems in validated for problem in problems)

    consensus: list[dict[str, Any]] = []
    first_fully, second_fully = (validated[0][0], validated[1][0])
    for packet in packets:
        packet_id = str(packet["review_packet_id"])
        sets = [sorted(first_fully.get(packet_id, set())), sorted(second_fully.get(packet_id, set()) )]
        if len(sets[0]) == len(sets[1]) == 1 and sets[0] == sets[1]:
            disposition = "C4_EXACT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT"
        elif sets[0] == sets[1] and len(sets[0]) > 1:
            disposition = "C4_MULTI_ADEQUATE_AGREEMENT_EXPLORATORY_ONLY_NOT_A_LABEL_OR_RESULT"
        else:
            disposition = "C4_REVIEWER_DISAGREEMENT_RETURN_TO_C2_OR_EXCLUDE_NOT_A_LABEL_OR_RESULT"
        consensus.append({
            "review_packet_id": packet_id,
            "proposal_ref": packet.get("proposal_ref"),
            "reviewer_fully_adequate_sets": sets,
            "disposition": disposition,
        })

    output = {
        "status": "C4_MODEL_ASSISTED_BLIND_CONSENSUS_AUDITED_NOT_A_LABEL_OR_RESULT" if not failures else "C4_MODEL_ASSISTED_BLIND_CONSENSUS_INVALID_NOT_A_LABEL_OR_RESULT",
        "reviewer_method": "model_assisted_blinded_review_not_human",
        "reviewer_ids": reviewer_ids,
        "reviewer_input_packet_count": len(packets),
        "reviewer_coverage": [
            {"reviewer_id": reviewer_id, "expected_packets": len(packets), "returned_packets": len(review.get("reviews", []))}
            for reviewer_id, review in zip(reviewer_ids, reviews)
        ],
        "prompt_consensus": consensus,
        "exact_singleton_agreement_count": sum(row["disposition"] == "C4_EXACT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT" for row in consensus),
        "multi_adequate_agreement_count": sum(row["disposition"] == "C4_MULTI_ADEQUATE_AGREEMENT_EXPLORATORY_ONLY_NOT_A_LABEL_OR_RESULT" for row in consensus),
        "disagreement_count": sum(row["disposition"] == "C4_REVIEWER_DISAGREEMENT_RETURN_TO_C2_OR_EXCLUDE_NOT_A_LABEL_OR_RESULT" for row in consensus),
        "failures": sorted(set(failures)),
        "exclusions": [
            "C4 documents blinded model-assisted adequacy judgment only; it is not human review, a gold label, retrieval input, metric, or frozen benchmark result.",
            "This audit intentionally does not read the sealed card-to-skill key.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("status", "reviewer_input_packet_count", "exact_singleton_agreement_count", "multi_adequate_agreement_count", "disagreement_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
