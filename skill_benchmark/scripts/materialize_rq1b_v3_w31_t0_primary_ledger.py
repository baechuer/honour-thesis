#!/usr/bin/env python3
"""Bind W31 T0 source-only decisions to frozen provenance for literal audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--decision-manifest", type=Path, required=True)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wave-label", default="W31")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_t0_primary_ledger")
    candidates = json.loads(args.candidate_manifest.read_text(encoding="utf-8"))
    decisions = json.loads(args.decision_manifest.read_text(encoding="utf-8"))
    candidate_by_id = {row["triad_id"]: row for row in candidates["candidate_triads"]}
    decision_rows = decisions["decisions"]
    if set(candidate_by_id) != {row["triad_id"] for row in decision_rows}:
        raise SystemExit("candidate_and_decision_triad_ids_mismatch")
    source_by_id = {row["amendment_source_id"]: row for row in read_jsonl(args.amendment)}
    composition_rows = []
    reviewed_ids: list[str] = []
    for decision in decision_rows:
        candidate = candidate_by_id[decision["triad_id"]]
        member_ids = candidate["members"]
        evidence_by_id = decision["member_evidence"]
        if set(member_ids) != set(evidence_by_id):
            raise SystemExit(f"member_evidence_mismatch:{decision['triad_id']}")
        members = []
        for source_id in member_ids:
            source = source_by_id.get(source_id)
            if source is None:
                raise SystemExit(f"unknown_source_id:{source_id}")
            canonical = source["canonical"]
            reviewed_ids.append(source_id)
            members.append({
                "source_id": source_id,
                "artifact_path": canonical["artifact_path"],
                "local_raw_path": canonical["local_raw_path"],
                "source_sha256": canonical["source_sha256"],
                "literal_evidence": [evidence_by_id[source_id]],
            })
        composition_rows.append({
            "composition_id": decision["triad_id"],
            "structural_decision": decision["structural_decision"],
            "common_envelope": decision["common_envelope"],
            "members": members,
            "literal_envelope_evidence": list(decision["member_evidence"].values()),
            "consensus_reason": decision["decision_rationale"],
            "rejection_reason": decision["rejection_reason"],
        })
    ledger = {
        "review_type": f"RQ1B_V3_{args.wave_label}_T0_PRIMARY_SOURCE_ONLY_STRUCTURAL_TRIAGE",
        "review_scope": {
            "reviewed_source_ids": reviewed_ids,
            "excluded_actions": ["no prompts", "no intended winners", "no gold labels", "no selectors", "no metrics", "no network", "no source-code execution"],
        },
        "candidate_compositions": composition_rows,
        "claim_boundary": decisions["claim_boundary"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ledger, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": f"RQ1B_V3_{args.wave_label}_T0_PRIMARY_LEDGER_MATERIALISED_AWAITING_LITERAL_AUDIT", "triad_count": len(composition_rows), "source_count": len(reviewed_ids)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
