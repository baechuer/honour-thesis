#!/usr/bin/env python3
"""Merge three audited disjoint Round 35 C4 blinded-review consensus slices."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


VALID = "C4_MODEL_ASSISTED_BLIND_CONSENSUS_AUDITED_NOT_A_LABEL_OR_RESULT"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"invalid_json_object:{path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slice", type=Path, action="append", required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.slice) != 3:
        raise SystemExit("requires_exactly_three_audited_slices")
    slices = [load(path) for path in args.slice]
    rows: list[dict[str, object]] = []
    reviewer_pairs: list[dict[str, object]] = []
    for path, item in zip(args.slice, slices):
        if item.get("status") != VALID or item.get("failures"):
            raise SystemExit(f"invalid_audited_slice:{path}")
        reviewers = item.get("reviewer_ids")
        consensus = item.get("prompt_consensus")
        if not isinstance(reviewers, list) or len(reviewers) != 2 or not isinstance(consensus, list):
            raise SystemExit(f"invalid_slice_shape:{path}")
        rows.extend(consensus)
        reviewer_pairs.append({"source_consensus": str(path), "reviewer_ids": reviewers, "review_packet_ids": [str(row.get("review_packet_id", "")) for row in consensus]})
    packet_ids = [str(row.get("review_packet_id", "")) for row in rows]
    key_ids = [str(json.loads(line).get("review_packet_id", "")) for line in args.key.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(packet_ids) != len(set(packet_ids)) or set(packet_ids) != set(key_ids):
        raise SystemExit("non_disjoint_or_incomplete_packet_coverage")
    reviewer_ids = [str(value) for pair in reviewer_pairs for value in pair["reviewer_ids"]]
    if len(reviewer_ids) != len(set(reviewer_ids)):
        raise SystemExit("reviewer_id_reused_across_slices")
    rows.sort(key=lambda row: str(row.get("review_packet_id", "")))
    output = {
        "status": VALID,
        "reviewer_method": "model_assisted_blinded_review_not_human",
        "reviewer_pairs_by_disjoint_packet_set": reviewer_pairs,
        "reviewer_input_packet_count": len(rows),
        "exact_singleton_agreement_count": sum(row.get("disposition") == "C4_EXACT_SINGLETON_AGREEMENT_NOT_A_LABEL_OR_RESULT" for row in rows),
        "multi_adequate_agreement_count": sum(row.get("disposition") == "C4_MULTI_ADEQUATE_AGREEMENT_EXPLORATORY_ONLY_NOT_A_LABEL_OR_RESULT" for row in rows),
        "disagreement_count": sum(row.get("disposition") == "C4_REVIEWER_DISAGREEMENT_RETURN_TO_C2_OR_EXCLUDE_NOT_A_LABEL_OR_RESULT" for row in rows),
        "prompt_consensus": rows,
        "exclusions": ["C4 is blinded model-assisted curation evidence, not a human review, gold label, retrieval input, metric, or result."],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("status", "reviewer_input_packet_count", "exact_singleton_agreement_count", "multi_adequate_agreement_count", "disagreement_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
