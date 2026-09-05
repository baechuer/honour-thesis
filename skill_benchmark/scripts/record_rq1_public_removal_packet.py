#!/usr/bin/env python3
"""Record one unblinded RQ1 public-removal fidelity review packet."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from record_rq1_human_review_packet import (
    read_jsonl,
    refresh_status,
    sha256_file,
    write_jsonl,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--decision", choices=("APPROVE", "REVISE", "EXCLUDE"), required=True)
    parser.add_argument("--reviewer", default="Jacky Zhang")
    parser.add_argument("--notes", required=True)
    parser.add_argument("--user-instruction", required=True)
    args = parser.parse_args()

    packet = args.packet.resolve()
    if packet.parent.name != "packets" or packet.parent.parent.name != "public_removal":
        raise RuntimeError("Only a public-removal review packet may be recorded here")
    if args.decision != "APPROVE":
        raise RuntimeError(
            "Batch recording of REVISE/EXCLUDE needs case-specific fields; "
            "record those individually"
        )

    stream_root = packet.parent.parent
    root = stream_root.parent
    receipt_dir = stream_root / "decision_receipts"
    receipt_path = receipt_dir / f"{packet.stem}_approve_receipt.json"
    if receipt_path.exists():
        raise RuntimeError(f"Receipt already exists: {receipt_path}")

    packet_text = packet.read_text(encoding="utf-8")
    review_ids = re.findall(r"^## (R-\d{4})(?::[^\n]*)?$", packet_text, re.MULTILINE)
    if not review_ids or len(review_ids) != len(set(review_ids)):
        raise RuntimeError("Packet review IDs are missing or duplicated")

    match = re.fullmatch(r"(.+)_batch_\d+", packet.stem)
    if match is None:
        raise RuntimeError(f"Unexpected packet filename: {packet.name}")
    expected_field = match.group(1)

    ledger_path = stream_root / "review_ledger.jsonl"
    ledger_rows = read_jsonl(ledger_path)
    ledger_by_id = {row["review_id"]: row for row in ledger_rows}
    missing = [review_id for review_id in review_ids if review_id not in ledger_by_id]
    if missing:
        raise RuntimeError(f"Packet IDs missing from ledger: {missing}")

    reviewed_at = datetime.now().astimezone().isoformat(timespec="seconds")
    for review_id in review_ids:
        row = ledger_by_id[review_id]
        if row["review_status"] != "PENDING":
            raise RuntimeError(f"Refusing to overwrite completed row: {review_id}")
        if row["target_field"] != expected_field:
            raise RuntimeError(
                f"Target-field mismatch for {review_id}: "
                f"{row['target_field']} != {expected_field}"
            )
        if not row["mechanical_line_blanking_only_for_all_candidates"]:
            raise RuntimeError(f"Mechanical blanking gate is not clear for {review_id}")

        row["target_information_removed_from_all_candidates"] = True
        row["no_obvious_target_field_residue"] = True
        row["candidate_identity_preserved"] = True
        row["no_unlogged_addition_or_rewrite"] = True
        row["review_status"] = "APPROVE"
        row["reviewer"] = args.reviewer
        row["reviewed_at"] = reviewed_at
        row["notes"] = args.notes

    write_jsonl(ledger_path, ledger_rows)
    progress = refresh_status(root)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema_version": "RQ1_PUBLIC_REMOVAL_PACKET_RECEIPT_V1",
        "stream": "public_removal",
        "packet": packet.relative_to(root).as_posix(),
        "packet_sha256": sha256_file(packet),
        "review_ids": review_ids,
        "target_field": expected_field,
        "decision": args.decision,
        "reviewer": args.reviewer,
        "reviewed_at": reviewed_at,
        "active_review_mode": "UNBLINDED_TRANSFORMATION_FIDELITY_REVIEW",
        "user_instruction": args.user_instruction,
        "notes": args.notes,
        "confirmed_judgements": {
            "target_information_removed_from_all_candidates": True,
            "no_obvious_target_field_residue": True,
            "candidate_identity_preserved": True,
            "no_unlogged_addition_or_rewrite": True,
        },
        "ledger_sha256_after": sha256_file(ledger_path),
        "progress_after": progress,
    }
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
