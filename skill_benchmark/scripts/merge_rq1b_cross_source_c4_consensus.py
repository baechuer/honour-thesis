#!/usr/bin/env python3
"""Merge audited disjoint C4 halves without changing their consensus rows."""

import argparse
import json
from pathlib import Path


VALID = "C4_MODEL_ASSISTED_BLIND_CONSENSUS_AUDITED_NOT_A_LABEL_OR_RESULT"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--half", action="append", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.half) != 2:
        raise SystemExit("exactly_two_disjoint_halves_required")

    halves = [load(path) for path in args.half]
    for path, half in zip(args.half, halves):
        if half.get("status") != VALID:
            raise SystemExit(f"invalid_half_status:{path}:{half.get('status')}")
        if half.get("failures"):
            raise SystemExit(f"half_has_failures:{path}:{half['failures']}")
        if len(half.get("reviewer_ids", [])) != 2:
            raise SystemExit(f"invalid_reviewer_pair:{path}")

    rows = [row for half in halves for row in half["prompt_consensus"]]
    packet_ids = [str(row["review_packet_id"]) for row in rows]
    if len(packet_ids) != len(set(packet_ids)):
        raise SystemExit("non_disjoint_packet_coverage")
    key_ids = [str(json.loads(line)["review_packet_id"]) for line in args.key.read_text().splitlines() if line.strip()]
    if set(packet_ids) != set(key_ids):
        raise SystemExit(f"key_coverage_mismatch:consensus={len(packet_ids)}:key={len(key_ids)}")

    rows.sort(key=lambda row: row["review_packet_id"])
    output = {
        "status": VALID,
        "reviewer_method": "model_assisted_blinded_review_not_human",
        "reviewer_pairs_by_disjoint_packet_set": [
            {
                "source_consensus": str(path),
                "reviewer_ids": half["reviewer_ids"],
                "review_packet_ids": [row["review_packet_id"] for row in half["prompt_consensus"]],
            }
            for path, half in zip(args.half, halves)
        ],
        "reviewer_input_packet_count": len(rows),
        "exact_singleton_agreement_count": sum(
            row.get("disposition") == "C4_EXACT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT"
            for row in rows
        ),
        "multi_adequate_agreement_count": sum(
            row.get("disposition") == "C4_MULTI_ADEQUATE_AGREEMENT_EXPLORATORY_ONLY_NOT_A_LABEL_OR_RESULT"
            for row in rows
        ),
        "disagreement_count": sum(
            row.get("disposition") == "C4_REVIEWER_DISAGREEMENT_RETURN_TO_C2_OR_EXCLUDE_NOT_A_LABEL_OR_RESULT"
            for row in rows
        ),
        "prompt_consensus": rows,
        "exclusions": [
            "C4 is blinded curation evidence only.",
            "It is not a gold label, retrieval input, model result, or metric.",
        ],
    }
    args.output.write_text(json.dumps(output, ensure_ascii=True, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: output[key] for key in ["status", "reviewer_input_packet_count", "exact_singleton_agreement_count", "multi_adequate_agreement_count", "disagreement_count"]}))


if __name__ == "__main__":
    main()
