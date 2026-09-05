#!/usr/bin/env python3
"""Freeze RQ1b V3 D1 W6r2 C1 source-only review dispositions.

This finaliser independently rechecks every listed original artifact hash and
every quoted source span before writing an immutable ledger. It validates a
source-evidence review only. It cannot establish a prompt, a gold label,
semantic field recoverability, a valid cluster, or a retrieval result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-d1-c1-wave006r2-finaliser-v1"
NOT_STATED = "NOT STATED"
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
    "C1 is source-only operational-evidence review. Any advance would permit only later "
    "cue-controlled prompt construction; it is not a valid cluster, gold label, selector "
    "input, field effect, or routing result."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_quote(value: Any, source_text: str, context: str) -> None:
    if value == NOT_STATED:
        return
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"invalid_source_evidence:{context}")
    if value not in source_text:
        raise ValueError(f"nonliteral_source_evidence:{context}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    args = parser.parse_args()

    wave_dir = args.wave_dir
    roster_path = wave_dir / "c1_review_roster.jsonl"
    manifest_path = wave_dir / "c1_review_manifest.json"
    ledger_path = wave_dir / "c1_review_final_ledger.jsonl"
    audit_path = wave_dir / "C1_SOURCE_EVIDENCE_WAVE_006R2_FINALISER_AUDIT.json"
    if ledger_path.exists() or audit_path.exists():
        raise SystemExit("refusing_to_overwrite_final_c1_artifacts")

    roster = {row["c1_review_id"]: row for row in read_jsonl(roster_path)}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("artifacts", {}).get("c1_review_roster.jsonl") != sha256_file(roster_path):
        raise SystemExit("roster_manifest_binding_mismatch")

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
        evidence = decision.get("source_evidence")
        if not isinstance(evidence, list) or len(evidence) != roster_row["candidate_count"]:
            raise SystemExit(f"evidence_member_count_mismatch:{c1_id}")

        members = {member["source_id"]: member for member in roster_row["members"]}
        evidence_by_source = {item.get("source_id"): item for item in evidence}
        if set(evidence_by_source) != set(members) or len(evidence_by_source) != len(evidence):
            raise SystemExit(f"evidence_member_identity_mismatch:{c1_id}")

        validated_evidence: list[dict[str, str]] = []
        for source_id, member in members.items():
            source_path = Path(member["absolute_path"])
            if not source_path.is_file() or sha256_file(source_path) != member["sha256"]:
                raise SystemExit(f"source_binding_drift:{c1_id}:{source_id}")
            source_text = source_path.read_text(encoding="utf-8")
            item = evidence_by_source[source_id]
            for key in ("trigger", "operation", "output", "boundary"):
                validate_quote(item.get(key), source_text, f"{c1_id}:{source_id}:{key}")
            validated_evidence.append({
                "source_id": source_id,
                **{key: item[key] for key in ("trigger", "operation", "output", "boundary")},
            })

        for required in ("common_envelope", "peer_route_rationale", "decision_reason"):
            if not isinstance(decision.get(required), str) or not decision[required].strip():
                raise SystemExit(f"missing_decision_text:{c1_id}:{required}")
        if outcome == "ADVANCE_C2_PROMPT_CONSTRUCTION":
            for item in validated_evidence:
                if any(item[key] == NOT_STATED for key in ("trigger", "operation", "output")):
                    raise SystemExit(f"advance_with_absent_operational_chain:{c1_id}:{item['source_id']}")

        records.append({
            "c1_review_id": c1_id,
            "parent_d1_draft_id": roster_row["parent_d1_draft_id"],
            "discovery_lane": roster_row["discovery_lane"],
            "member_source_ids": [member["source_id"] for member in roster_row["members"]],
            "member_titles": [member["title"] for member in roster_row["members"]],
            "candidate_count": roster_row["candidate_count"],
            "review_mode": "independent source-only review plus principal literal and source-binding recheck",
            "source_binding_verified": True,
            "literal_spans_verified": True,
            "final_c1_outcome": outcome,
            "common_envelope": decision["common_envelope"],
            "reason": decision["decision_reason"],
            "peer_route_rationale": decision["peer_route_rationale"],
            "source_evidence": validated_evidence,
            "claim_boundary": BOUNDARY,
        })

    ledger_path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    counts = Counter(record["final_c1_outcome"] for record in records)
    audit = {
        "status": "RQ1B_V3_D1_C1_W6R2_FINALISATION_PASS_ALL_REJECTED_NOT_A_CLUSTER_OR_RESULT",
        "version": VERSION,
        "record_count": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "advance_c2_count": counts["ADVANCE_C2_PROMPT_CONSTRUCTION"],
        "roster_sha256": sha256_file(roster_path),
        "manifest_sha256": sha256_file(manifest_path),
        "parent_d1_manifest_sha256": manifest["parent_d1_manifest_sha256"],
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
