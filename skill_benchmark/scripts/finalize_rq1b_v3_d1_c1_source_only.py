#!/usr/bin/env python3
"""Freeze one source-only RQ1b V3 D1/C1 disposition after literal revalidation."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


OUTCOMES = {
    "ADVANCE_C2_PROMPT_CONSTRUCTION",
    "REJECT_SOURCE_BINDING",
    "REJECT_ABSENT_OPERATIONAL_CHAIN",
    "REJECT_NO_COMMON_ENVELOPE",
    "REJECT_NONPARALLEL_OR_COMPONENT",
    "REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST",
    "NEEDS_PARENT_REVIEW",
}
NOT_STATED = "NOT STATED"
BOUNDARY = (
    "C1 is source-only operational-evidence review. An advance would permit only later cue-controlled "
    "prompt construction; it is not a valid cluster, gold label, selector input, field effect, or routing result."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_span(value: object, source_text: str, field: str) -> None:
    if value == NOT_STATED:
        return
    if not isinstance(value, str) or not value.strip() or value not in source_text:
        raise ValueError(f"invalid literal {field}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--parent-d1-manifest", type=Path, required=True)
    parser.add_argument("--status", required=True)
    args = parser.parse_args()

    roster_path = args.wave_dir / "c1_review_roster.jsonl"
    manifest_path = args.wave_dir / "c1_review_manifest.json"
    ledger_path = args.wave_dir / "c1_review_final_ledger.jsonl"
    audit_path = args.wave_dir / "C1_SOURCE_EVIDENCE_FINALISER_AUDIT.json"
    if ledger_path.exists() or audit_path.exists():
        raise SystemExit("refusing_to_overwrite_final_c1_artifacts")
    roster = read_jsonl(roster_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["artifacts"]["c1_review_roster.jsonl"] != sha256_file(roster_path):
        raise SystemExit("roster_manifest_binding_mismatch")
    decisions_doc = json.loads(args.decisions.read_text(encoding="utf-8"))
    decisions = {item["c1_review_id"]: item for item in decisions_doc["decisions"]}
    if set(decisions) != {row["c1_review_id"] for row in roster}:
        raise SystemExit("decision_coverage_mismatch")

    records: list[dict] = []
    for packet in roster:
        decision = decisions[packet["c1_review_id"]]
        outcome = decision.get("allowed_outcome")
        if outcome not in OUTCOMES:
            raise SystemExit(f"invalid_outcome:{outcome}")
        evidence_by_id = {item["source_id"]: item for item in decision.get("source_evidence", [])}
        members = packet["members"]
        if set(evidence_by_id) != {member["source_id"] for member in members}:
            raise SystemExit("source_evidence_identity_mismatch")
        validated_evidence: list[dict] = []
        for member in members:
            source_path = Path(member["absolute_path"])
            if not source_path.is_file() or sha256_file(source_path) != member["sha256"]:
                raise SystemExit(f"source_binding_drift:{member['source_id']}")
            source_text = source_path.read_text(encoding="utf-8")
            item = evidence_by_id[member["source_id"]]
            for field in ("trigger", "operation", "output", "boundary"):
                validate_span(item.get(field), source_text, f"{member['source_id']}:{field}")
            validated_evidence.append({"source_id": member["source_id"], **{field: item[field] for field in ("trigger", "operation", "output", "boundary")}})
        for field in ("common_envelope", "peer_route_rationale", "decision_reason"):
            if not isinstance(decision.get(field), str) or not decision[field].strip():
                raise SystemExit(f"missing_decision_text:{field}")
        records.append({
            "c1_review_id": packet["c1_review_id"], "parent_d1_draft_id": packet["parent_d1_draft_id"],
            "discovery_lane": packet["discovery_lane"], "member_source_ids": [member["source_id"] for member in members],
            "member_titles": [member["title"] for member in members], "candidate_count": packet["candidate_count"],
            "review_mode": "independent source-only review plus principal literal and source-binding recheck",
            "source_binding_verified": True, "literal_spans_verified": True, "final_c1_outcome": outcome,
            "common_envelope": decision["common_envelope"], "reason": decision["decision_reason"],
            "peer_route_rationale": decision["peer_route_rationale"], "source_evidence": validated_evidence,
            "claim_boundary": BOUNDARY,
        })

    ledger_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    counts = Counter(row["final_c1_outcome"] for row in records)
    audit = {
        "status": args.status, "record_count": len(records), "outcome_counts": dict(sorted(counts.items())),
        "advance_c2_count": counts["ADVANCE_C2_PROMPT_CONSTRUCTION"], "roster_sha256": sha256_file(roster_path),
        "packet_manifest_sha256": sha256_file(manifest_path), "parent_d1_manifest_sha256": sha256_file(args.parent_d1_manifest),
        "decisions_sha256": sha256_file(args.decisions), "ledger_sha256": sha256_file(ledger_path),
        "network_calls": 0, "texts_transmitted": 0, "claim_boundary": BOUNDARY,
    }
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
