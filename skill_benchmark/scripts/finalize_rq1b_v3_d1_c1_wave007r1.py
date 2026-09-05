#!/usr/bin/env python3
"""Freeze RQ1b V3 D1 W7r1 C1 source-only dispositions.

The finaliser reuses the upstream D1 literal evidence rather than rewriting
reviewer paraphrases. It validates source hashes and source spans again, then
freezes only source-only C1 decisions. It cannot create a prompt, gold label,
valid cluster, field effect or retrieval result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-d1-c1-wave007r1-finaliser-v1"
OUTCOMES = {
    "ADVANCE_C2_PROMPT_CONSTRUCTION",
    "REJECT_SOURCE_BINDING",
    "REJECT_ABSENT_OPERATIONAL_CHAIN",
    "REJECT_NO_COMMON_ENVELOPE",
    "REJECT_NONPARALLEL_OR_COMPONENT",
    "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
    "NEEDS_PARENT_REVIEW",
}
BOUNDARY = (
    "C1 is source-only operational-evidence review. Any advance permits only later "
    "cue-controlled prompt construction; it is not a valid cluster, gold label, selector "
    "input, field effect or routing result."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    parser.add_argument("--d1-manifest", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    args = parser.parse_args()

    roster_path = args.wave_dir / "c1_review_roster.jsonl"
    manifest_path = args.wave_dir / "c1_review_manifest.json"
    ledger_path = args.wave_dir / "c1_review_final_ledger.jsonl"
    audit_path = args.wave_dir / "C1_SOURCE_EVIDENCE_WAVE_007R1_FINALISER_AUDIT.json"
    if ledger_path.exists() or audit_path.exists():
        raise SystemExit("refusing_to_overwrite_final_c1_artifacts")

    roster = {row["c1_review_id"]: row for row in read_jsonl(roster_path)}
    c1_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if c1_manifest.get("artifacts", {}).get("c1_review_roster.jsonl") != sha256_file(roster_path):
        raise SystemExit("roster_manifest_binding_mismatch")
    if c1_manifest.get("parent_d1_manifest_sha256") != sha256_file(args.d1_manifest):
        raise SystemExit("parent_d1_manifest_binding_mismatch")
    d1_by_id = {row["d1_draft_id"]: row for row in read_jsonl(args.d1_manifest)}

    decisions_doc = json.loads(args.decisions.read_text(encoding="utf-8"))
    decisions = decisions_doc.get("decisions")
    if not isinstance(decisions, list):
        raise SystemExit("decisions_missing_or_not_list")
    by_id = {row.get("c1_review_id"): row for row in decisions}
    if set(by_id) != set(roster) or len(by_id) != len(decisions):
        raise SystemExit("decision_coverage_or_duplicate_mismatch")

    records: list[dict[str, Any]] = []
    for c1_id, roster_row in roster.items():
        decision = by_id[c1_id]
        outcome = decision.get("allowed_outcome")
        if outcome not in OUTCOMES:
            raise SystemExit(f"invalid_outcome:{c1_id}:{outcome}")
        for key in ("common_envelope", "peer_route_rationale", "decision_reason"):
            if not isinstance(decision.get(key), str) or not decision[key].strip():
                raise SystemExit(f"missing_decision_text:{c1_id}:{key}")
        d1 = d1_by_id.get(roster_row["parent_d1_draft_id"])
        if d1 is None:
            raise SystemExit(f"missing_parent_d1_draft:{c1_id}")

        roster_members = {member["source_id"]: member for member in roster_row["members"]}
        d1_members = {member["source_id"]: member for member in d1["members"]}
        if set(roster_members) != set(d1_members):
            raise SystemExit(f"d1_roster_member_mismatch:{c1_id}")
        evidence_rows: list[dict[str, str]] = []
        for source_id, roster_member in roster_members.items():
            d1_member = d1_members[source_id]
            if roster_member["sha256"] != d1_member["sha256"]:
                raise SystemExit(f"d1_roster_hash_mismatch:{c1_id}:{source_id}")
            source_path = Path(roster_member["absolute_path"])
            if not source_path.is_file() or sha256_file(source_path) != roster_member["sha256"]:
                raise SystemExit(f"source_binding_drift:{c1_id}:{source_id}")
            source_text = source_path.read_text(encoding="utf-8")
            evidence = d1_member["evidence"]
            for field in ("trigger", "operation", "output"):
                if evidence[field] not in source_text:
                    raise SystemExit(f"nonliteral_d1_evidence:{c1_id}:{source_id}:{field}")
            constraint = evidence.get("constraint", "NOT STATED")
            if constraint != "NOT STATED" and constraint not in source_text:
                raise SystemExit(f"nonliteral_d1_constraint:{c1_id}:{source_id}")
            evidence_rows.append({
                "source_id": source_id,
                "trigger": evidence["trigger"],
                "operation": evidence["operation"],
                "output": evidence["output"],
                "boundary": constraint,
            })

        records.append({
            "c1_review_id": c1_id,
            "parent_d1_draft_id": roster_row["parent_d1_draft_id"],
            "discovery_lane": roster_row["discovery_lane"],
            "member_source_ids": [member["source_id"] for member in roster_row["members"]],
            "member_titles": [member["title"] for member in roster_row["members"]],
            "candidate_count": roster_row["candidate_count"],
            "review_mode": "independent source-only review plus principal D1-evidence, literal and source-binding recheck",
            "source_binding_verified": True,
            "literal_spans_verified": True,
            "final_c1_outcome": outcome,
            "common_envelope": decision["common_envelope"],
            "reason": decision["decision_reason"],
            "peer_route_rationale": decision["peer_route_rationale"],
            "source_evidence": evidence_rows,
            "claim_boundary": BOUNDARY,
        })

    ledger_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in records),
        encoding="utf-8",
    )
    counts = Counter(row["final_c1_outcome"] for row in records)
    audit = {
        "status": "RQ1B_V3_D1_C1_W7R1_FINALISATION_PASS_NOT_A_CLUSTER_OR_RESULT",
        "version": VERSION,
        "record_count": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "advance_c2_count": counts["ADVANCE_C2_PROMPT_CONSTRUCTION"],
        "roster_sha256": sha256_file(roster_path),
        "c1_manifest_sha256": sha256_file(manifest_path),
        "parent_d1_manifest_sha256": sha256_file(args.d1_manifest),
        "decisions_sha256": sha256_file(args.decisions),
        "ledger_sha256": sha256_file(ledger_path),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
