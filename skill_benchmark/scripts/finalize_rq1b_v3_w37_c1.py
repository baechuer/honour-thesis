#!/usr/bin/env python3
"""Freeze Wave 037 C1 decisions after checking literal-audited reviewer returns."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c1-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_final_decisions")
    roster_path = args.c1_dir / "packet_materialisation" / "c1_review_roster.jsonl"
    source_audit_path = args.c1_dir / "packet_materialisation" / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json"
    roster = read_jsonl(roster_path)
    source_audit = json.loads(source_audit_path.read_text(encoding="utf-8"))
    if source_audit.get("status") != "RQ1B_V3_W37_C1_SOURCE_BINDING_AUDIT_PASS_NOT_A_CLUSTER":
        raise SystemExit("source_binding_audit_not_passed")

    decisions = []
    literal_audits: dict[str, str] = {}
    for packet in roster:
        review_id = packet["c1_review_id"]
        returned = []
        for reviewer in ("A", "B"):
            stem = review_id.rsplit("-", 1)[-1]
            raw_path = args.c1_dir / "reviewer_returns" / f"C1_{stem}_REVIEWER_{reviewer}_RAW_RETURN.json"
            audit_path = args.c1_dir / "reviewer_return_audits" / f"C1_{stem}_REVIEWER_{reviewer}_LITERAL_AUDIT.json"
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            if audit.get("status") != "RQ1B_V3_W37_C1_RETURN_LITERAL_AUDIT_PASS_NOT_A_CLUSTER" or audit.get("failure_count") != 0:
                raise SystemExit(f"literal_audit_failure:{review_id}:{reviewer}")
            if raw.get("c1_review_id") != review_id:
                raise SystemExit(f"review_id_mismatch:{review_id}:{reviewer}")
            literal_audits[f"C1_{stem}_REVIEWER_{reviewer}"] = "PASS"
            returned.append(raw)

        outcomes = [row["outcome"] for row in returned]
        advance = outcomes == ["ADVANCE_C2_PROMPT_CONSTRUCTION", "ADVANCE_C2_PROMPT_CONSTRUCTION"]
        if advance:
            final_outcome = "ADVANCE_C2_PROMPT_CONSTRUCTION"
            next_stage = "C2_PROMPT_CONSTRUCTION"
        elif outcomes[0] == outcomes[1]:
            final_outcome = outcomes[0]
            next_stage = "NONE"
        else:
            final_outcome = "REJECT_NO_C1_ADVANCE_CONSENSUS"
            next_stage = "NONE"
        decisions.append({
            "c1_review_id": review_id,
            "outcome": final_outcome,
            "valid_reviewer_outcomes": outcomes,
            "reviewer_return_sha256": [sha256_file(args.c1_dir / "reviewer_returns" / f"C1_{review_id.rsplit('-', 1)[-1]}_REVIEWER_{reviewer}_RAW_RETURN.json") for reviewer in ("A", "B")],
            "reason_summary": [row["reason"] for row in returned],
            "next_stage": next_stage,
        })
    advances = sum(row["next_stage"] == "C2_PROMPT_CONSTRUCTION" for row in decisions)
    result = {
        "status": "RQ1B_V3_W37_C1_COMPLETE_NO_ADVANCES" if advances == 0 else "RQ1B_V3_W37_C1_COMPLETE_WITH_C2_ADVANCES",
        "source_binding": source_audit["status"],
        "reviewer_literal_audits": literal_audits,
        "decisions": decisions,
        "counts": {
            "t0_ready_for_c1": len(roster),
            "c1_packets": len(roster),
            "c1_advanced_to_c2": advances,
            "strict_clusters_frozen_before_and_after": 37,
            "strict_prompts_frozen_before_and_after": 231,
        },
        "boundary": "This is source-only curation feasibility. It does not test retrieval, information-field effect, prompt fitness, label validity, selector behaviour, metric or thesis claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "c1_advanced_to_c2": advances}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
