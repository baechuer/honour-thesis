#!/usr/bin/env python3
"""Create the one-sided, full-source Reviewer A packet for immutable B044."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_data_ml_ai_evaluation_data_engineering_databases_security_privacy_observability_b044_2026-09-04"
INPUT = ROOT / "b044_source_native_three_skill_full_original_packets.jsonl"
OUTPUT = ROOT / "batch_044_full_source_review_packets"

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

def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing packet root: {OUTPUT}")
    rows = [json.loads(line) for line in INPUT.read_text(encoding="utf-8").splitlines() if line]
    if len(rows) != 25:
        raise SystemExit("expected 25 immutable B044 packets")
    packets = []
    for row in rows:
        members = []
        for index, member in enumerate(row["members"], 1):
            originals = member["preserved_complete_original_sources"]
            if len(originals) != 1:
                raise SystemExit(f"unexpected preserved-source multiplicity: {row['family_id']}")
            original = originals[0]
            raw = original["preserved_original_skill_utf8"].encode("utf-8")
            if hashlib.sha256(raw).hexdigest() != member["canonical_source_sha256"]:
                raise SystemExit(f"immutable packet byte mismatch: {row['family_id']}")
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
    OUTPUT.mkdir(parents=True)
    packet_path = OUTPUT / "reviewer_a_packet.jsonl"
    packet_path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in packets), encoding="utf-8")
    (OUTPUT / "review_return_template.json").write_text(json.dumps(RETURN_SCHEMA, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"packets": len(packets), "members": sum(len(r["members"]) for r in packets), "packet_sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest()}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
