#!/usr/bin/env python3
"""Assign RQ1b C5 strict or unresolved strata from blinded C4 consensus.

This is local curation bookkeeping. It does not score retrieval, call a model,
or freeze a benchmark packet. A strict gold is emitted only when both accepted
C4 reviewers returned the same one-card fully-adequate set and that card maps
to the sealed C2 construction target.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c4-consensus", type=Path, required=True)
    parser.add_argument("--c4-key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    c4 = read_json(args.c4_consensus)
    key_by_packet = {str(row["review_packet_id"]): row for row in read_jsonl(args.c4_key)}
    consensus_rows = c4.get("prompt_consensus", [])
    if len(consensus_rows) != len(key_by_packet):
        raise SystemExit(f"coverage_mismatch:c4={len(consensus_rows)}:key={len(key_by_packet)}")

    rows: list[dict[str, Any]] = []
    strict_count = 0
    exploratory_count = 0
    unresolved_count = 0
    failures: list[str] = []
    for consensus in consensus_rows:
        packet_id = str(consensus["review_packet_id"])
        key = key_by_packet.get(packet_id)
        if key is None:
            failures.append(f"missing_key:{packet_id}")
            continue
        sets = [sorted(set(values)) for values in consensus.get("reviewer_fully_adequate_sets", [])]
        cards = {str(card["card_label"]): str(card["skill_id"]) for card in key.get("card_key", [])}
        base = {
            "review_packet_id": packet_id,
            "proposal_id": key.get("proposal_id"),
            "prompt_variant": key.get("prompt_variant"),
            "c4_reviewer_fully_adequate_sets": sets,
            "c5_method": "exact_two_reviewer_singleton_agreement",
            "exclusions": ["not frozen", "not a retrieval input", "not a model result", "not a metric"],
        }
        exact_singleton = len(sets) == 2 and sets[0] == sets[1] and len(sets[0]) == 1
        if exact_singleton:
            card_label = sets[0][0]
            skill_id = cards.get(card_label)
            if skill_id is None:
                failures.append(f"missing_card_mapping:{packet_id}:{card_label}")
                continue
            sealed = str(key.get("intended_candidate_skill_id_sealed"))
            if skill_id != sealed:
                failures.append(f"sealed_intent_mismatch:{packet_id}:{skill_id}:{sealed}")
                continue
            rows.append({
                **base,
                "c5_status": "C5_PRIMARY_STRICT_SINGLETON_GOLD_NOT_FROZEN_NOT_A_RESULT",
                "strict_gold_card_label": card_label,
                "strict_gold_skill_id": skill_id,
                "sealed_intent_match": True,
            })
            strict_count += 1
        elif len(sets) == 2 and sets[0] == sets[1] and len(sets[0]) > 1:
            acceptable_labels = sets[0]
            acceptable_skills = [cards.get(label) for label in acceptable_labels]
            if any(skill_id is None for skill_id in acceptable_skills):
                failures.append(f"missing_acceptable_card_mapping:{packet_id}")
                continue
            sealed = str(key.get("intended_candidate_skill_id_sealed"))
            rows.append({
                **base,
                "c5_status": "C5_EXPLORATORY_ACCEPTABLE_SET_NOT_A_GOLD_OR_RESULT",
                "acceptable_card_labels": acceptable_labels,
                "acceptable_skill_ids": acceptable_skills,
                "sealed_intent_in_acceptable_set": sealed in acceptable_skills,
                "required_next_step": "retain_only_for_separate_acceptable_set_exploration_not_primary_top1",
            })
            exploratory_count += 1
        else:
            rows.append({
                **base,
                "c5_status": "C5_UNRESOLVED_C4_DISAGREEMENT_NOT_A_GOLD_OR_RESULT",
                "strict_gold_card_label": None,
                "strict_gold_skill_id": None,
                "sealed_intent_match": None,
                "required_next_step": "revise_at_C2_C3_and_repeat_full_C4_or_exclude",
            })
            unresolved_count += 1

    summary = {
        "status": "C5_PASS_NOT_FROZEN_NOT_A_RETRIEVAL_OR_RESULT" if not failures else "C5_FAILED_NOT_A_RESULT",
        "prompt_count": len(rows),
        "primary_strict_singleton_count": strict_count,
        "exploratory_acceptable_set_count": exploratory_count,
        "unresolved_c4_disagreement_count": unresolved_count,
        "failures": failures,
        "exclusions": ["C5 is an internal stratum assignment only; C6 must still validate and freeze any usable packet."],
    }
    write_jsonl(args.output, rows)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
