#!/usr/bin/env python3
"""Bind B045 reviewed family tokens to their already replayed source bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_collaboration_project_management_meeting_notes_email_calendar_crm_customer_support_workflow_automation_b045_2026-09-04"
PACKETS = ROOT / "b045_source_native_three_skill_full_original_packets.jsonl"
REPLAY = ROOT / "source_byte_replay_ledger.jsonl"
OUTPUT = ROOT / "batch_045_full_source_review_packets/internal_reconciliation_key.jsonl"


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite B045 reconciliation key: {OUTPUT}")
    packets = rows(PACKETS)
    replay_by_hash = {row["canonical_source_sha256"]: row for row in rows(REPLAY)}
    if len(packets) != 25 or len(replay_by_hash) != 75:
        raise SystemExit("B045 packet/replay cardinality mismatch")
    key_rows = []
    for packet in packets:
        family_id = str(packet["family_id"])
        members = packet.get("members", [])
        if len(members) != 3:
            raise SystemExit(f"{family_id}: expected three members")
        for index, member in enumerate(members, 1):
            source_hash = str(member["canonical_source_sha256"])
            replay = replay_by_hash.get(source_hash)
            paths = [] if replay is None else replay.get("source_paths", [])
            if not isinstance(paths, list) or not paths or replay.get("source_byte_replay_status") != "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256":
                raise SystemExit(f"{family_id}: no passing source-byte replay ledger for {source_hash}")
            for relative_path in paths:
                path = WORKSPACE / str(relative_path)
                if not path.is_file() or sha256_file(path) != source_hash:
                    raise SystemExit(f"{family_id}: source byte replay failed for {path}")
            key_rows.append({
                "family_token": f"F-{family_id.removeprefix('SN-LEX-')}",
                "family_id": family_id,
                "member_token": f"S-{index}",
                "canonical_source_sha256": source_hash,
                "source_paths": paths,
                "source_byte_replay": "PASS_SHA256_MATCH",
                "bootstrap_batch_rank": packet["batch_rank"],
                "bootstrap_discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
                "claim_boundary": "Reviewed source identity and byte replay binding only; no provenance, prompt, adequacy, admission, selector, or metric decision.",
            })
    if len(key_rows) != 75 or len({row["canonical_source_sha256"] for row in key_rows}) != 75:
        raise SystemExit("B045 reconciliation key source coverage mismatch")
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in key_rows), encoding="utf-8", newline="\n")
    print(json.dumps({"families": 25, "sources": len(key_rows), "key_sha256": sha256_file(OUTPUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
