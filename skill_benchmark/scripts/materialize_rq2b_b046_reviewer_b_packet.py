#!/usr/bin/env python3
"""Materialise a blinded, source-complete Reviewer B packet for B046."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_commerce_ecommerce_retail_sales_travel_hospitality_real_estate_logistics_procurement_b046_2026-09-04"
INPUT = ROOT / "b046_source_native_three_skill_full_original_packets.jsonl"
LEDGER = ROOT / "source_native_reciprocal_family_ledger.jsonl"
PACKET_DIR = ROOT / "batch_046_full_source_review_packets"
PACKET = PACKET_DIR / "reviewer_b_packet.jsonl"
TEMPLATE = PACKET_DIR / "reviewer_b_return_template.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    if PACKET.exists() or TEMPLATE.exists():
        raise SystemExit("refusing to overwrite existing B046 Reviewer B material")
    rows, ledger = read_jsonl(INPUT), read_jsonl(LEDGER)
    if len(rows) != 25 or len(ledger) != 25:
        raise SystemExit("B046 input cardinality mismatch")
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != "2fd09e2bed0f46c5ddd4c580a454143ab26506a8b3efbfedf9ce13d8348c8e15":
        raise SystemExit("immutable B046 full-original packet hash mismatch")
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest() != "a8f24eeddc6294af1e27abdbaec770e85858e3cbc3f74825c3bcfc63a65e67dd":
        raise SystemExit("immutable B046 family-ledger hash mismatch")

    packets: list[dict[str, Any]] = []
    source_hashes: list[str] = []
    for row in rows:
        rank = int(row["batch_rank"])
        if row["family_id"] != ledger[rank - 1]["family_id"] or len(row["members"]) != 3:
            raise SystemExit(f"family ledger/member mismatch at rank {rank}")
        members = []
        for position, member in enumerate(row["members"], 1):
            originals = member["preserved_complete_original_sources"]
            expected_hash = str(member["canonical_source_sha256"])
            if not originals:
                raise SystemExit(f"missing complete source at rank {rank}, member {position}")
            source_texts = [item["preserved_original_skill_utf8"] for item in originals]
            if any(hashlib.sha256(source.encode("utf-8")).hexdigest() != expected_hash for source in source_texts):
                raise SystemExit(f"complete-source hash mismatch at rank {rank}, member {position}")
            if len(set(source_texts)) != 1:
                raise SystemExit(f"non-identical source aliases at rank {rank}, member {position}")
            members.append({
                "member_token": f"S-{position}",
                "source_byte_sha256": expected_hash,
                "complete_original_skill": source_texts[0],
                "review_instruction": "Read the complete original skill. Cite literal excerpts or line locations; do not infer missing capability from topic familiarity.",
            })
            source_hashes.append(expected_hash)
        packets.append({
            "record_type": "source_native_full_source_reviewer_b_packet",
            "family_token": "F-" + str(row["family_id"]).removeprefix("SN-LEX-"),
            "members": members,
            "rubric": {
                "pass": "Three independent first-route skills share a bounded objective/input/output envelope and have source-supported operational contrast for natural prompts.",
                "reject_codes": ["REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION", "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK", "REJECT_NO_BOUNDED_ENVELOPE", "REJECT_NO_MEMBER_LEVEL_PROMPTABILITY"],
                "defer_codes": ["DEFER_PROVENANCE_OR_LICENSE", "DEFER_INSUFFICIENT_SOURCE_EVIDENCE"],
                "rule": "The complete original source is authoritative. Do not use discovery rank, source path, origin, prior outcomes, or another reviewer's judgement.",
            },
            "return_schema": {
                "decision": "PASS_TO_PROMPT_AUTHORING | rejection/defer code",
                "common_envelope_evidence": ["literal source evidence"],
                "member_contrast_evidence": {"S-1": ["literal evidence"], "S-2": ["literal evidence"], "S-3": ["literal evidence"]},
                "rationale": "short source-grounded explanation",
            },
        })

    if len(packets) != 25 or len(source_hashes) != 75:
        raise SystemExit("packet cardinality mismatch")
    template = {
        "record_type": "source_native_full_source_reviewer_b_return",
        "family_token": "F-...",
        "decision": "PASS_TO_PROMPT_AUTHORING | rejection/defer code",
        "common_envelope_evidence": [],
        "member_contrast_evidence": {"S-1": [], "S-2": [], "S-3": []},
        "rationale": "",
        "review_boundary": "Reviewer B full-source family assessment only; no provenance, prompt, adequacy, admission, selector, retrieval-result, or metric decision.",
    }
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(PACKET, packets)
    TEMPLATE.write_text(json.dumps(template, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"packet_sha256": hashlib.sha256(PACKET.read_bytes()).hexdigest(), "template_sha256": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(), "families": len(packets), "sources": len(source_hashes)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
