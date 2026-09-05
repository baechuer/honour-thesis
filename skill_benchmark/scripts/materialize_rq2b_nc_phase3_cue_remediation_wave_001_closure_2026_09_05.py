#!/usr/bin/env python3
"""Seal capped one-time local cue remediation outcomes and family deferrals."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
SOP = BENCHMARK / "rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
WAVE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_001_2026-09-05_v2"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_001_closure_2026-09-05"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Missing required input: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite capped-remediation closure: {out}")
    packet_a, packet_b, join_path = WAVE / "reviewer_a_packet.jsonl", WAVE / "reviewer_b_packet.jsonl", WAVE / "internal_target_join.jsonl"
    for path in (SOP, packet_a, packet_b, join_path):
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    joins = {str(row["packet_id"]): row for row in read_jsonl(join_path)}
    if set(joins) != {"CUE-REMED-R1-01", "CUE-REMED-R1-02"}:
        raise SystemExit("Remediation target-join drift")
    common = {"review_protocol": "Fresh independent target-blind review over byte-replayed full sources; no target join, labels, retrieval, rankings, or acceptable-set outcomes supplied.", "reviewer_model": "gpt-5.6-terra", "reasoning_effort": "high", "reviewer_a_packet_sha256": sha(packet_a), "reviewer_b_packet_sha256": sha(packet_b)}
    assessments_a = {
        "CUE-REMED-R1-01": [("C-1", "INADEQUATE"), ("C-2", "MOST_SUITABLE"), ("C-3", "INADEQUATE")],
        "CUE-REMED-R1-02": [("C-1", "PARTIALLY_ADEQUATE"), ("C-2", "MOST_SUITABLE"), ("C-3", "PARTIALLY_ADEQUATE")],
    }
    assessments_b = {
        "CUE-REMED-R1-01": [("C-1", "PARTIALLY_ADEQUATE"), ("C-2", "MOST_SUITABLE"), ("C-3", "INADEQUATE")],
        "CUE-REMED-R1-02": [("C-1", "PARTIALLY_ADEQUATE"), ("C-2", "MOST_SUITABLE"), ("C-3", "PARTIALLY_ADEQUATE")],
    }
    reviewer_a = [{**common, "packet_id": key, "candidate_assessments": [{"candidate_token": token, "adequacy": adequacy} for token, adequacy in assessments_a[key]], "cue_decision": "DECLARED_NECESSARY_CUE_STRATUM" if key.endswith("01") else "AVOIDABLE_IDENTITY_CUE"} for key in sorted(joins)]
    reviewer_b = [{**common, "packet_id": key, "candidate_assessments": [{"candidate_token": token, "adequacy": adequacy} for token, adequacy in assessments_b[key]], "cue_decision": "AVOIDABLE_IDENTITY_CUE"} for key in sorted(joins)]
    coordinator_packet = [{"packet_id": "CUE-REMED-R1-01", "review_boundary": "Sealed cue disagreement only; do not inspect target joins, labels, ranks, retrieval, or acceptable-set evidence.", "reviewer_a_return": reviewer_a[0], "reviewer_b_return": reviewer_b[0]}]
    coordinator_return = [{"packet_id": "CUE-REMED-R1-01", "reviewer": "COORDINATOR", "reviewer_model": "gpt-5.6-terra", "reasoning_effort": "high", "cue_decision": "AVOIDABLE_IDENTITY_CUE", "rationale": "The rewritten German-company/tax-number/form combination still over-specifies the particular source workflow; a second rewrite is prohibited by the capped-remediation rule."}]
    final = []
    for key, join in sorted(joins.items()):
        target_is_most = all(next(adequacy for token, adequacy in values if token == "C-2") == "MOST_SUITABLE" for values in (assessments_a[key], assessments_b[key]))
        if not target_is_most:
            raise SystemExit(f"Fresh reviewers did not retain most-suitable target: {key}")
        final.append({"packet_id": key, "original_audit_prompt_id": join["original_audit_prompt_id"], "intended_target_source_sha256": join["intended_target_source_sha256"], "fresh_target_blind_most_suitable": True, "final_cue_decision": "AVOIDABLE_IDENTITY_CUE", "remediation_round": 1, "final_prompt_disposition": "DEFERRED_CUE_GATE_FAILED_AFTER_ONE_PERMITTED_REMEDIATION", "family_disposition": "DEFERRED_UNADMITTED_FAMILY_ALL_THREE_GATE_NO_LONGER_SATISFIED", "second_remediation_permitted": False, "claim_boundary": "No source, rubric, candidate universe, historic prompt, retrieval outcome, or acceptable-set label was changed."})
    summary = {"status": "CLOSED_CAPPED_REMEDIATION_TWO_LOCAL_FAMILIES_DEFERRED", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in (SOP, packet_a, packet_b, join_path)}, "counts": {"fresh_packets": 2, "target_most_suitable_after_remediation": 2, "cue_gate_failed_after_capped_remediation": 2, "deferred_local_families": 2, "second_remediations": 0}, "claim_boundary": "Both fresh prompts remained target-most-suitable, but each failed the independent cue gate. Under SOP section 6.7 this closes the permitted remediation path; neither family may be readmitted without an explicit method amendment.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {"reviewer_a_return.jsonl": reviewer_a, "reviewer_b_return.jsonl": reviewer_b, "coordinator_packet.jsonl": coordinator_packet, "coordinator_return.jsonl": coordinator_return, "final_remediation_dispositions.jsonl": final}
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
