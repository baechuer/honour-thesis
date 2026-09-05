#!/usr/bin/env python3
"""Audit RQ1b V3 C4B blind reviews before C5 target unsealing.

This program reads only reviewer inputs, reviewer responses, and the anonymous
C4A-card unpermutation map.  It intentionally has no argument for the C5
target key, so it cannot compare a C4B adequacy consensus with the sealed C2
construction target.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RESPONSES = {"ONE_FULLY_ADEQUATE", "MULTIPLE_ADEQUATE", "NONE_ADEQUATE", "UNCERTAIN"}
REVIEW_METHOD = "key_blind_model_assisted_adequacy_review_not_human"
REVIEW_COMPLETE = "RQ1B_V3_C4B_REVIEW_COMPLETE_NOT_A_LABEL_OR_RESULT"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"json_not_object:{path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_row_not_object:{path}:{number}")
            rows.append(value)
    return rows


def case_id(packet_id: str) -> str:
    prefix, separator, suffix = packet_id.rpartition("-R")
    if not separator or suffix not in {"1", "2"}:
        raise ValueError(f"invalid_reviewer_packet_id:{packet_id}")
    return prefix


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-packets", type=Path, action="append", required=True)
    parser.add_argument("--review", type=Path, action="append", required=True)
    parser.add_argument("--unpermutation-key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def input_cards(rows: list[dict[str, Any]]) -> dict[str, dict[str, set[str]]]:
    result: dict[str, dict[str, set[str]]] = {}
    for row in rows:
        packet_id = str(row.get("review_packet_id", ""))
        if not packet_id or packet_id in result:
            raise ValueError(f"duplicate_or_missing_input_packet:{packet_id}")
        cards = row.get("candidate_cards")
        if not isinstance(cards, list):
            raise ValueError(f"candidate_cards_missing:{packet_id}")
        result[packet_id] = {}
        for card in cards:
            if not isinstance(card, dict):
                continue
            label = str(card.get("card_label", ""))
            body = card.get("card")
            if not label or not isinstance(body, dict):
                continue
            result[packet_id][label] = {
                quote
                for field in body.values()
                if isinstance(field, dict)
                for quote in field.get("quotes", [])
                if isinstance(quote, str)
            }
        if len(result[packet_id]) != len(cards):
            raise ValueError(f"invalid_card_labels:{packet_id}")
    return result


def validate_review(
    review: dict[str, Any],
    cards_by_packet: dict[str, dict[str, set[str]]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    failures: list[str] = []
    reviewer_id = str(review.get("reviewer_id", ""))
    if not reviewer_id:
        failures.append("missing_reviewer_id")
    if review.get("review_method") != REVIEW_METHOD:
        failures.append(f"unexpected_review_method:{reviewer_id}")
    if review.get("status") != REVIEW_COMPLETE:
        failures.append(f"unexpected_review_status:{reviewer_id}")
    items: dict[str, dict[str, Any]] = {}
    for item in review.get("reviews", []):
        if not isinstance(item, dict):
            failures.append(f"review_item_not_object:{reviewer_id}")
            continue
        packet_id = str(item.get("review_packet_id", ""))
        if not packet_id or packet_id in items:
            failures.append(f"duplicate_or_missing_review_packet:{reviewer_id}:{packet_id}")
            continue
        items[packet_id] = item
    if set(items) != set(cards_by_packet):
        for packet_id in sorted(set(cards_by_packet) - set(items)):
            failures.append(f"missing_review_packet:{reviewer_id}:{packet_id}")
        for packet_id in sorted(set(items) - set(cards_by_packet)):
            failures.append(f"unexpected_review_packet:{reviewer_id}:{packet_id}")
    for packet_id, item in items.items():
        cards = cards_by_packet.get(packet_id)
        if cards is None:
            continue
        response = str(item.get("response_label", ""))
        selected = item.get("selected_card_label")
        snippets = item.get("evidence_snippets")
        if response not in RESPONSES:
            failures.append(f"invalid_response_label:{reviewer_id}:{packet_id}")
        if not isinstance(snippets, list) or not all(isinstance(value, str) and value for value in snippets):
            failures.append(f"invalid_evidence_snippets:{reviewer_id}:{packet_id}")
        if not str(item.get("rationale", "")).strip():
            failures.append(f"missing_rationale:{reviewer_id}:{packet_id}")
        if response == "ONE_FULLY_ADEQUATE":
            if selected not in cards:
                failures.append(f"invalid_selected_card:{reviewer_id}:{packet_id}")
                continue
            if not snippets:
                failures.append(f"missing_selected_evidence:{reviewer_id}:{packet_id}")
            for snippet in snippets:
                if snippet not in cards[str(selected)]:
                    failures.append(f"nonexact_selected_evidence:{reviewer_id}:{packet_id}")
        elif selected is not None:
            failures.append(f"unexpected_selected_card:{reviewer_id}:{packet_id}")
    return items, failures


def main() -> int:
    args = parse_args()
    if len(args.reviewer_packets) != 2 or len(args.review) != 2:
        raise SystemExit("requires_exactly_two_packet_files_and_two_reviews")
    input_by_reviewer = [input_cards(read_jsonl(path)) for path in args.reviewer_packets]
    reviews = [read_json(path) for path in args.review]
    reviewer_ids = [str(review.get("reviewer_id", "")) for review in reviews]
    failures: list[str] = []
    if len(set(reviewer_ids)) != 2:
        failures.append("reviewer_ids_not_distinct")
    validated = [validate_review(review, cards) for review, cards in zip(reviews, input_by_reviewer)]
    failures.extend(item for _, items in validated for item in items)

    key_rows = read_jsonl(args.unpermutation_key)
    key_by_packet = {str(row.get("review_packet_id", "")): row for row in key_rows}
    input_ids = set(input_by_reviewer[0]) | set(input_by_reviewer[1])
    if set(key_by_packet) != input_ids or len(key_by_packet) != len(key_rows):
        failures.append("unpermutation_key_coverage_mismatch")

    key_by_case: dict[str, dict[int, dict[str, Any]]] = {}
    for packet_id, row in key_by_packet.items():
        try:
            base = case_id(packet_id)
            reviewer_index = int(packet_id.rsplit("-R", 1)[1])
        except ValueError as error:
            failures.append(str(error))
            continue
        key_by_case.setdefault(base, {})[reviewer_index] = row

    responses_by_case: dict[str, dict[int, dict[str, Any]]] = {}
    for reviewer_index, items in enumerate((validated[0][0], validated[1][0]), start=1):
        for packet_id, item in items.items():
            try:
                responses_by_case.setdefault(case_id(packet_id), {})[reviewer_index] = item
            except ValueError as error:
                failures.append(str(error))

    consensus: list[dict[str, Any]] = []
    for base in sorted(key_by_case):
        maps = key_by_case[base]
        answers = responses_by_case.get(base, {})
        if set(maps) != {1, 2} or set(answers) != {1, 2}:
            failures.append(f"case_pair_coverage:{base}")
            continue
        canonical_selected: list[str | None] = []
        response_labels: list[str] = []
        for reviewer_index in (1, 2):
            response = answers[reviewer_index]
            response_label = str(response.get("response_label", ""))
            response_labels.append(response_label)
            selected = response.get("selected_card_label")
            mapping = {
                str(item.get("review_card_label")): str(item.get("canonical_card_label"))
                for item in maps[reviewer_index].get("card_key", [])
            }
            canonical_selected.append(mapping.get(str(selected)) if response_label == "ONE_FULLY_ADEQUATE" else None)
        if response_labels == ["ONE_FULLY_ADEQUATE", "ONE_FULLY_ADEQUATE"] and canonical_selected[0] and canonical_selected[0] == canonical_selected[1]:
            disposition = "RQ1B_V3_C4B_STRICT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT"
        elif response_labels == ["MULTIPLE_ADEQUATE", "MULTIPLE_ADEQUATE"]:
            disposition = "RQ1B_V3_C4B_MULTIPLE_ADEQUATE_AGREEMENT_EXPLORATORY_ONLY_NOT_A_LABEL_OR_RESULT"
        else:
            disposition = "RQ1B_V3_C4B_NO_STRICT_SINGLETON_CONSENSUS_NOT_A_LABEL_OR_RESULT"
        consensus.append({
            "case_id": base,
            "c4a_packet_id": maps[1].get("c4a_packet_id"),
            "reviewer_response_labels": response_labels,
            "canonical_selected_cards": canonical_selected,
            "disposition": disposition,
        })

    output = {
        "status": "RQ1B_V3_C4B_CONSENSUS_AUDIT_PASS_NOT_A_LABEL_OR_RESULT" if not failures else "RQ1B_V3_C4B_CONSENSUS_AUDIT_FAIL_NOT_A_RESULT",
        "reviewer_ids": reviewer_ids,
        "review_case_count": len(consensus),
        "strict_singleton_agreement_count": sum(row["disposition"] == "RQ1B_V3_C4B_STRICT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT" for row in consensus),
        "multiple_adequate_agreement_count": sum(row["disposition"] == "RQ1B_V3_C4B_MULTIPLE_ADEQUATE_AGREEMENT_EXPLORATORY_ONLY_NOT_A_LABEL_OR_RESULT" for row in consensus),
        "no_strict_singleton_consensus_count": sum(row["disposition"] == "RQ1B_V3_C4B_NO_STRICT_SINGLETON_CONSENSUS_NOT_A_LABEL_OR_RESULT" for row in consensus),
        "consensus": consensus,
        "failures": sorted(set(failures)),
        "boundary": "This audit has no C5 target-key input. It records anonymous adequacy consensus only; it does not create a gold label, retrieval input, metric, or frozen cluster.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("status", "review_case_count", "strict_singleton_agreement_count", "multiple_adequate_agreement_count", "no_strict_singleton_consensus_count", "failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
