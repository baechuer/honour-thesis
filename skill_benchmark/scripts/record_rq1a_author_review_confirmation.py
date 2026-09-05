#!/usr/bin/env python3
"""Record the author's retrospective confirmation of iterative RQ1a review."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "rq1a_field_discriminability" / "human_review_2026-08-30"
LEDGER = REVIEW_DIR / "review_ledger.jsonl"
RECEIPT = REVIEW_DIR / "author_review_confirmation_receipt.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--recorded-on", default=str(date.today()))
    parser.add_argument("--confirm-all-core-retained", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.confirm_all_core_retained:
        raise SystemExit("Refusing to alter the ledger without --confirm-all-core-retained.")

    rows = [json.loads(line) for line in LEDGER.read_text().splitlines() if line]
    field_counts = Counter(row["field"] for row in rows)
    if len(rows) != 350 or set(field_counts.values()) != {50} or len(field_counts) != 7:
        raise SystemExit(f"Unexpected RQ1a ledger inventory: {len(rows)} rows; {field_counts}")

    note = (
        "Retrospectively logged author confirmation on "
        f"{args.recorded_on}: reviewed iteratively during RQ1a design; retained. "
        "This is author review, not independent or blinded annotation."
    )
    for row in rows:
        if row["researcher_review_status"] != "PENDING_RESEARCHER_REVIEW":
            raise SystemExit(f"Refusing to overwrite non-pending row: {row['cluster_id']}")
        row["researcher_review_status"] = "AUTHOR_REVIEWED_RETAINED"
        row["reviewer"] = args.reviewer
        row["reviewed_at"] = args.recorded_on
        row["review_notes"] = note
        row["review_method"] = "retrospective_author_confirmation_of_iterative_design_review"
        row["decisions"] = {
            "gold_is_unique_for_each_prompt_variant": True,
            "both_alternatives_are_plausible_near_neighbours": True,
            "target_field_is_the_decisive_skill_side_distinction": True,
            "prompt_variants_preserve_gold_intent_without_name_or_title_leakage": True,
            "retain_in_primary_rq1a": True,
        }

    rendered = "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows)
    LEDGER.write_text(rendered)
    receipt = {
        "schema_version": "RQ1A_AUTHOR_REVIEW_CONFIRMATION_RECEIPT_V1",
        "recorded_on": args.recorded_on,
        "reviewer": args.reviewer,
        "review_method": "retrospective_author_confirmation_of_iterative_design_review",
        "scope": "all 350 core RQ1a clusters",
        "retained_clusters": len(rows),
        "excluded_clusters": 0,
        "claim_boundary": "Author-reviewed, not independent or blinded annotation.",
        "review_ledger_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
