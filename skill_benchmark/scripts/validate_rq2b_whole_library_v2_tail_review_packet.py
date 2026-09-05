#!/usr/bin/env python3
"""Fail closed on one independent V2 tail-review packet return.

This validator checks packet/return integrity only.  It neither reconciles the
two reviewer streams nor derives an adequacy conclusion, acceptable set,
selector result, or metric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PACKET_ROOT = ROOT / "review/whole_library_pooled_tail_packets_v1_2026-08-31"
RETURN_ROOT = ROOT / "review/whole_library_pooled_tail_reviews_v1_2026-08-31"
OUTCOMES = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "NOT_ADEQUATE", "UNCLEAR"}
STATUS = "INDEPENDENT_BLIND_TAIL_REVIEW_NOT_A_METRIC_OR_FINAL_LABEL"
ANCHOR_RE = re.compile(r"\[?(S\d{4}\|L\d{4})\]?")
FORBIDDEN_KEYS = {
    "canonical_source_sha256", "candidate_alias_ids", "source_name", "source_path",
    "lane_id", "tail_class", "discovery_reasons", "channel_scores",
    "historical_gold", "local_roster", "selector_output", "metric",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def card_sha(card: dict[str, Any]) -> str:
    copy = {key: value for key, value in card.items() if key != "rendered_card_sha256"}
    return hashlib.sha256(
        json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def anchors(value: Any) -> set[str]:
    return set(ANCHOR_RE.findall(json.dumps(value, ensure_ascii=False)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stream", choices=("A", "B"), required=True)
    parser.add_argument("--packet", required=True)
    args = parser.parse_args()
    packet_path = PACKET_ROOT / f"reviewer_stream_{args.stream}" / f"{args.packet}.jsonl"
    return_path = RETURN_ROOT / f"reviewer_{args.stream}" / f"{args.packet}.jsonl"
    cards = read_jsonl(packet_path)
    returns = read_jsonl(return_path)
    if len(cards) != 22 or len(returns) != 22:
        raise SystemExit(f"expected_22_cards_and_returns:{len(cards)}:{len(returns)}")
    cards_by_token = {row["opaque_case_token"]: row for row in cards}
    returns_by_token = {row.get("opaque_case_token"): row for row in returns}
    if len(cards_by_token) != 22 or len(returns_by_token) != 22 or set(cards_by_token) != set(returns_by_token):
        raise SystemExit("case_token_mismatch_or_duplicate")
    outcome_counts: dict[str, int] = {outcome: 0 for outcome in sorted(OUTCOMES)}
    for token, response in returns_by_token.items():
        if FORBIDDEN_KEYS & set(response):
            raise SystemExit(f"forbidden_response_key:{token}")
        if response.get("reviewer_blind_id") != args.stream:
            raise SystemExit(f"wrong_reviewer_id:{token}")
        if response.get("status") != STATUS:
            raise SystemExit(f"wrong_status:{token}")
        if response.get("outcome") not in OUTCOMES:
            raise SystemExit(f"invalid_outcome:{token}")
        if response.get("submitted_card_sha256") != cards_by_token[token]["rendered_card_sha256"]:
            raise SystemExit(f"submitted_card_sha_mismatch:{token}")
        if card_sha(cards_by_token[token]) != cards_by_token[token]["rendered_card_sha256"]:
            raise SystemExit(f"stored_card_sha_mismatch:{token}")
        for required in ("supporting_anchor_positions", "limitation_anchor_positions", "prompt_requirement_map", "short_rationale"):
            if required not in response or response[required] in (None, ""):
                raise SystemExit(f"missing_response_field:{token}:{required}")
        source_anchors = anchors(cards_by_token[token]["redacted_source_text"])
        support_anchors = anchors(response["supporting_anchor_positions"])
        limitation_anchors = anchors(response["limitation_anchor_positions"])
        response_anchors = support_anchors | limitation_anchors | anchors(response["prompt_requirement_map"])
        if not response_anchors <= source_anchors:
            raise SystemExit(f"response_anchor_not_in_card:{token}")
        has_support = bool(support_anchors)
        has_limitation = bool(limitation_anchors)
        if not has_support and not has_limitation:
            raise SystemExit(f"no_source_anchor:{token}")
        if response["outcome"] == "FULLY_ACCEPTABLE" and not has_support:
            raise SystemExit(f"no_support_anchor_for_full:{token}")
        if response["outcome"] in {"PARTIALLY_ADEQUATE", "NOT_ADEQUATE"} and not has_limitation:
            raise SystemExit(f"no_limitation_anchor_for_nonfull:{token}")
        outcome_counts[response["outcome"]] += 1
    print(json.dumps({
        "status": "PASS_INDEPENDENT_TAIL_PACKET_RETURN_SCHEMA_NOT_A_RECONCILED_LABEL_OR_METRIC",
        "stream": args.stream,
        "packet": args.packet,
        "card_count": len(cards),
        "outcome_counts": outcome_counts,
        "packet_sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
        "return_sha256": hashlib.sha256(return_path.read_bytes()).hexdigest(),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
