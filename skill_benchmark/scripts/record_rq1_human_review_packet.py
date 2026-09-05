#!/usr/bin/env python3
"""Record one researcher-confirmation packet and refresh live RQ1 review counts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(canonical_json(row) for row in rows) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_status(root: Path) -> dict[str, dict[str, int]]:
    labels = {
        "controlled": "Controlled field-isolation",
        "public_gold": "Public strict gold",
        "public_removal": "Public removal fidelity",
    }
    progress: dict[str, dict[str, int]] = {}
    table_rows = []
    for stream, label in labels.items():
        rows = read_jsonl(root / stream / "review_ledger.jsonl")
        completed = sum(row["review_status"] != "PENDING" for row in rows)
        pending = len(rows) - completed
        progress[stream] = {
            "units": len(rows),
            "completed": completed,
            "pending": pending,
        }
        table_rows.append(
            f"| {label} | {len(rows)} | {completed} | {pending} | "
            "See the stream ledger and decision receipts. |"
        )

    total_units = sum(item["units"] for item in progress.values())
    total_completed = sum(item["completed"] for item in progress.values())
    total_pending = total_units - total_completed
    total_claim = (
        "Researcher confirmation complete."
        if total_pending == 0
        else "Researcher confirmation remains incomplete."
    )
    progress["total"] = {
        "units": total_units,
        "completed": total_completed,
        "pending": total_pending,
    }
    root.joinpath("STATUS.md").write_text(
        "# RQ1 Human Review Status\n\n"
        f"Updated: {datetime.now().astimezone().isoformat(timespec='seconds')}\n\n"
        "| Review stream | Units | Completed | Pending | Current claim |\n"
        "| --- | ---: | ---: | ---: | --- |\n"
        + "\n".join(table_rows)
        + "\n"
        + f"| **Total** | **{total_units}** | **{total_completed}** | "
        + f"**{total_pending}** | {total_claim} |\n\n"
        + "A row counts as completed only when its ledger records the reviewer, "
        + "timestamp, disposition, and required judgements. All three streams are "
        + "unblinded: frozen labels are visible for controlled/public-gold "
        + "confirmation, while intact and removed documents are visible for "
        + "removal-fidelity review.\n",
        encoding="utf-8",
    )

    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["review_progress"] = progress
    manifest["status"] = (
        "RESEARCHER_REVIEW_COMPLETE" if total_pending == 0 else "RESEARCHER_REVIEW_IN_PROGRESS"
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return progress


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--decision", choices=("APPROVE", "REVISE", "EXCLUDE"), required=True)
    parser.add_argument("--reviewer", default="Jacky Zhang")
    parser.add_argument("--notes", required=True)
    parser.add_argument("--user-instruction", required=True)
    args = parser.parse_args()

    packet = args.packet.resolve()
    if packet.parent.name != "confirmation_packets":
        raise RuntimeError("Only an unblinded confirmation packet may be recorded here")
    stream_root = packet.parent.parent
    stream = stream_root.name
    if stream not in {"controlled", "public_gold"}:
        raise RuntimeError(f"Unsupported confirmation stream: {stream}")
    root = stream_root.parent
    receipt_dir = stream_root / "decision_receipts"
    receipt_path = receipt_dir / f"{packet.stem}_approve_receipt.json"
    if receipt_path.exists():
        raise RuntimeError(f"Receipt already exists: {receipt_path}")
    packet_text = packet.read_text(encoding="utf-8")
    expected_prefix = "C" if stream == "controlled" else "P"
    review_ids = re.findall(rf"^## ({expected_prefix}-\d{{4}})(?::[^\n]*)?$", packet_text, re.MULTILINE)
    if not review_ids or len(review_ids) != len(set(review_ids)):
        raise RuntimeError("Packet review IDs are missing or duplicated")

    ledger_path = stream_root / "review_ledger.jsonl"
    key_path = root / "private_keys" / (
        "controlled_gold_keys.jsonl" if stream == "controlled" else "public_gold_keys.jsonl"
    )
    ledger_rows = read_jsonl(ledger_path)
    key_by_id = {row["review_id"]: row for row in read_jsonl(key_path)}
    ledger_by_id = {row["review_id"]: row for row in ledger_rows}
    reviewed_at = datetime.now().astimezone().isoformat(timespec="seconds")

    for review_id in review_ids:
        row = ledger_by_id[review_id]
        if row["review_status"] != "PENDING":
            raise RuntimeError(f"Refusing to overwrite completed row: {review_id}")
        if args.decision != "APPROVE":
            raise RuntimeError(
                "Batch recording of REVISE/EXCLUDE needs case-specific fields; "
                "record those individually"
            )
        key = key_by_id[review_id]
        gold_labels = [
            label
            for label, candidate in key["candidate_key"].items()
            if candidate["is_frozen_gold"]
        ]
        if len(gold_labels) != 1:
            raise RuntimeError(f"Expected one frozen gold label for {review_id}")

        row["selected_candidate_label"] = gold_labels[0]
        row["review_status"] = "APPROVE"
        row["reviewer"] = args.reviewer
        row["reviewed_at"] = reviewed_at
        row["notes"] = args.notes
        if stream == "public_gold":
            row["one_candidate_fully_adequate_for_both_prompts"] = True
            row["other_candidates_are_plausible_near_neighbours"] = True
            row["prompt_pair_preserves_one_intent"] = True
            row["prompt_has_no_source_or_skill_name_leak"] = True
        else:
            row["unique_fully_adequate_candidate"] = True
            row["alternatives_are_plausible_near_neighbours"] = True
            row["non_target_information_is_shared"] = True
            row["prompt_variants_preserve_intent"] = True
            row["prompt_has_no_candidate_name_or_title_leak"] = True

    write_jsonl(ledger_path, ledger_rows)
    progress = refresh_status(root)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema_version": "RQ1_UNBLINDED_CONFIRMATION_PACKET_RECEIPT_V1",
        "stream": stream,
        "packet": packet.relative_to(root).as_posix(),
        "packet_sha256": sha256_file(packet),
        "review_ids": review_ids,
        "decision": args.decision,
        "reviewer": args.reviewer,
        "reviewed_at": reviewed_at,
        "active_review_mode": "UNBLINDED_FROZEN_GOLD_VISIBLE",
        "frozen_gold_visible_to_reviewer": True,
        "user_instruction": args.user_instruction,
        "notes": args.notes,
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
