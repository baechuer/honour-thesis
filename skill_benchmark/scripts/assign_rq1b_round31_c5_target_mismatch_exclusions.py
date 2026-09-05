#!/usr/bin/env python3
"""Add explicit non-primary records for expected Round 31 C5 target mismatches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STRICT = "C5_PRIMARY_STRICT_SINGLETON_GOLD_NOT_FROZEN_NOT_A_RESULT"
EXPLORATORY = "C5_EXPLORATORY_ACCEPTABLE_SET_NOT_A_GOLD_OR_RESULT"
UNRESOLVED = "C5_UNRESOLVED_C4_DISAGREEMENT_NOT_A_GOLD_OR_RESULT"
MISMATCH = "C5_SEALED_TARGET_MISMATCH_EXCLUDE_NOT_A_GOLD_OR_RESULT"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-c5", type=Path, required=True)
    parser.add_argument("--c4-consensus", type=Path, required=True)
    parser.add_argument("--c4-key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    base = read_jsonl(args.base_c5)
    c4 = read_json(args.c4_consensus)
    keys = {str(row["review_packet_id"]): row for row in read_jsonl(args.c4_key)}
    represented = {str(row["review_packet_id"]) for row in base}
    additions: list[dict[str, Any]] = []
    failures: list[str] = []
    for consensus in c4.get("prompt_consensus", []):
        packet_id = str(consensus.get("review_packet_id", ""))
        if packet_id in represented:
            continue
        key = keys.get(packet_id)
        if key is None:
            failures.append(f"missing_key:{packet_id}")
            continue
        sets = [sorted(set(values)) for values in consensus.get("reviewer_fully_adequate_sets", [])]
        cards = {str(card["card_label"]): str(card["skill_id"]) for card in key.get("card_key", [])}
        if not (len(sets) == 2 and sets[0] == sets[1] and len(sets[0]) == 1):
            failures.append(f"non_singleton_missing_base_row:{packet_id}")
            continue
        selected_label = sets[0][0]
        selected_skill = cards.get(selected_label)
        sealed = str(key.get("intended_candidate_skill_id_sealed", ""))
        if selected_skill is None or selected_skill == sealed:
            failures.append(f"unexpected_missing_base_row:{packet_id}")
            continue
        additions.append({
            "review_packet_id": packet_id,
            "proposal_id": key.get("proposal_id"),
            "prompt_variant": key.get("prompt_variant"),
            "c4_reviewer_fully_adequate_sets": sets,
            "c5_method": "exact_two_reviewer_singleton_agreement_then_sealed_target_check",
            "c5_status": MISMATCH,
            "blind_singleton_skill_id": selected_skill,
            "sealed_intended_candidate_skill_id": sealed,
            "required_next_step": "exclude_from_primary_and_do_not_relabel_blind_singleton_as_gold",
            "exclusions": ["not frozen", "not a retrieval input", "not a model result", "not a metric"],
        })
    rows = sorted(base + additions, key=lambda row: str(row["review_packet_id"]))
    if {str(row["review_packet_id"]) for row in rows} != set(keys):
        failures.append("final_coverage_mismatch")
    summary = {
        "status": "C5_PASS_WITH_EXPLICIT_TARGET_MISMATCH_EXCLUSIONS_NOT_FROZEN_NOT_A_RESULT" if not failures else "C5_EXCLUSION_WRAPPER_INCOMPLETE_NOT_A_RESULT",
        "prompt_count": len(rows),
        "primary_strict_singleton_count": sum(row.get("c5_status") == STRICT for row in rows),
        "exploratory_acceptable_set_count": sum(row.get("c5_status") == EXPLORATORY for row in rows),
        "unresolved_c4_disagreement_count": sum(row.get("c5_status") == UNRESOLVED for row in rows),
        "sealed_target_mismatch_exclusion_count": sum(row.get("c5_status") == MISMATCH for row in rows),
        "failures": failures,
        "base_c5_preserved": str(args.base_c5),
        "exclusions": ["A mismatch is an explicit strict-primary exclusion, not a replacement gold label or a retrieval result."],
    }
    write_jsonl(args.output, rows)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
