#!/usr/bin/env python3
"""Materialise Reviewer B's B044 packet from immutable full-original evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_data_ml_ai_evaluation_data_engineering_databases_security_privacy_observability_b044_2026-09-04"
INPUT = ROOT / "b044_source_native_three_skill_full_original_packets.jsonl"
BYTE_LEDGER = ROOT / "source_byte_replay_ledger.jsonl"
RECIPROCAL_LEDGER = ROOT / "source_native_reciprocal_family_ledger.jsonl"
OUTPUT = ROOT / "batch_044_full_source_review_packets"
PACKET = OUTPUT / "reviewer_b_packet.jsonl"
TEMPLATE = OUTPUT / "review_return_template.json"

RUBRIC = {
    "pass": "Three independent first-route skills share a bounded objective/input/output envelope and have source-supported operational contrast for natural prompts.",
    "reject_codes": ["REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION", "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE", "REJECT_NO_MEMBER_LEVEL_PROMPTABILITY"],
    "defer_codes": ["DEFER_PROVENANCE_OR_LICENSE", "DEFER_INSUFFICIENT_SOURCE_EVIDENCE"],
    "rule": "Do not use discovery rank, source path, origin, population role, previous results or another reviewer's judgement. The complete original source is authoritative.",
}
RETURN_SCHEMA = {
    "record_type": "source_native_full_source_family_review_return",
    "family_token": "F-...",
    "decision": "PASS_TO_PROMPT_AUTHORING | rejection/defer code",
    "common_envelope_evidence": [],
    "member_contrast_evidence": {"S-1": [], "S-2": [], "S-3": []},
    "rationale": "",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate(rows: list[dict[str, Any]], byte_rows: list[dict[str, Any]], reciprocal_rows: list[dict[str, Any]]) -> None:
    if len(rows) != 25 or len({row["family_id"] for row in rows}) != 25:
        raise SystemExit("B044 must contain exactly 25 uniquely identified families")
    if len(byte_rows) != 75 or len(reciprocal_rows) != 25:
        raise SystemExit("B044 immutable ledgers must cover 75 sources and 25 families")
    ledger_by_hash = {str(row["canonical_source_sha256"]): row for row in byte_rows}
    if len(ledger_by_hash) != 75:
        raise SystemExit("source-byte ledger must contain 75 unique canonical source hashes")
    reciprocal_by_id = {str(row["family_id"]): row for row in reciprocal_rows}
    if len(reciprocal_by_id) != 25 or set(reciprocal_by_id) != {row["family_id"] for row in rows}:
        raise SystemExit("reciprocal ledger family coverage does not exactly bind B044")
    packet_hashes: set[str] = set()
    for row in rows:
        family_id = str(row["family_id"])
        members = row.get("members", [])
        if len(members) != 3:
            raise SystemExit(f"{family_id}: expected three members")
        member_hashes = []
        for member in members:
            source_hash = str(member["canonical_source_sha256"])
            originals = member.get("preserved_complete_original_sources", [])
            if len(originals) != 1:
                raise SystemExit(f"{family_id}: unexpected preserved-source multiplicity")
            original = originals[0]
            if sha256(str(original["preserved_original_skill_utf8"]).encode("utf-8")) != source_hash:
                raise SystemExit(f"{family_id}: preserved original does not match canonical hash")
            ledger = ledger_by_hash.get(source_hash)
            if ledger is None or ledger.get("source_byte_replay_status") != "PASS_ALL_PRESERVED_PATHS_MATCH_CANONICAL_SHA256":
                raise SystemExit(f"{family_id}: no passing source-byte replay for {source_hash}")
            if ledger.get("native_description_literal_replay_status") != "LITERAL_REPLAY_PASS" or set(ledger.get("replayed_path_sha256", [])) != {source_hash}:
                raise SystemExit(f"{family_id}: invalid native/source replay binding for {source_hash}")
            for relative_path in ledger.get("source_paths", []):
                source_path = WORKSPACE / str(relative_path)
                if not source_path.is_file() or sha256(source_path.read_bytes()) != source_hash:
                    raise SystemExit(f"{family_id}: full-source path byte replay failed for {source_path}")
            packet_hashes.add(source_hash)
            member_hashes.append(source_hash)
        reciprocal_hashes = [str(value) for value in reciprocal_by_id[family_id]["member_source_sha256"]]
        if member_hashes != reciprocal_hashes:
            raise SystemExit(f"{family_id}: reciprocal-ledger member binding mismatch")
    if packet_hashes != set(ledger_by_hash):
        raise SystemExit("packet/source-byte ledger hash coverage mismatch")


def main() -> int:
    if PACKET.exists():
        raise SystemExit(f"refusing to overwrite existing Reviewer B packet: {PACKET}")
    rows = read_jsonl(INPUT)
    validate(rows, read_jsonl(BYTE_LEDGER), read_jsonl(RECIPROCAL_LEDGER))
    packets = []
    for row in rows:
        members = []
        for index, member in enumerate(row["members"], 1):
            original = member["preserved_complete_original_sources"][0]
            members.append({
                "member_token": f"S-{index}",
                "source_byte_sha256": member["canonical_source_sha256"],
                "complete_original_skill": original["preserved_original_skill_utf8"],
                "review_instruction": "Read the complete original skill. Cite literal excerpts or line locations; do not infer missing capability from topic familiarity.",
            })
        packets.append({
            "record_type": "source_native_full_source_family_review",
            "family_token": f"F-{row['family_id'].split('-')[-1]}",
            "members": members,
            "rubric": RUBRIC,
            "return_schema": RETURN_SCHEMA,
        })
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PACKET.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in packets), encoding="utf-8", newline="\n")
    if TEMPLATE.exists() and json.loads(TEMPLATE.read_text(encoding="utf-8")) != RETURN_SCHEMA:
        raise SystemExit(f"unexpected pre-existing return template: {TEMPLATE}")
    TEMPLATE.write_text(json.dumps(RETURN_SCHEMA, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"families": len(packets), "sources": sum(len(row["members"]) for row in packets), "reviewer_b_packet_sha256": sha256(PACKET.read_bytes()), "return_template_sha256": sha256(TEMPLATE.read_bytes())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
