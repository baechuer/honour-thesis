#!/usr/bin/env python3
"""Mechanically replace one invalid C4B review record with a fresh blind review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"json_not_object:{path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-review", type=Path, required=True)
    parser.add_argument("--correction", type=Path, required=True)
    parser.add_argument("--reviewer-packets", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    original = read_json(args.original_review)
    correction = read_json(args.correction)
    packet_ids = {str(row.get("review_packet_id", "")) for row in read_jsonl(args.reviewer_packets)}
    original_reviews = original.get("reviews")
    correction_reviews = correction.get("reviews")
    if not isinstance(original_reviews, list) or not isinstance(correction_reviews, list) or len(correction_reviews) != 1:
        raise SystemExit("invalid_review_or_correction_shape")
    replacement = correction_reviews[0]
    if not isinstance(replacement, dict):
        raise SystemExit("correction_not_object")
    packet_id = str(replacement.get("review_packet_id", ""))
    original_ids = [str(row.get("review_packet_id", "")) for row in original_reviews if isinstance(row, dict)]
    if packet_id not in packet_ids or original_ids.count(packet_id) != 1:
        raise SystemExit(f"correction_packet_not_exactly_one_original_packet:{packet_id}")
    merged_reviews = [replacement if str(row.get("review_packet_id", "")) == packet_id else row for row in original_reviews]
    output = {
        "reviewer_id": f"{original.get('reviewer_id', '')}_R1",
        "review_method": original.get("review_method"),
        "status": original.get("status"),
        "reviews": merged_reviews,
        "correction_lineage": {
            "original_review_path": str(args.original_review),
            "fresh_correction_path": str(args.correction),
            "replaced_review_packet_id": packet_id,
            "boundary": "One key-blind evidence-fidelity correction only; no target, source, selector, or other review answer was read or changed.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "RQ1B_V3_C4B_ONE_PACKET_CORRECTION_MERGED_NOT_A_RESULT", "review_packet_id": packet_id, "review_count": len(merged_reviews)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
