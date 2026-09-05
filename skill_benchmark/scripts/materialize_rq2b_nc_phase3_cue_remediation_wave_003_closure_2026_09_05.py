#!/usr/bin/env python3
"""Seal the last permitted Phase-3 remediation review and its lineage."""
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
PHASE3 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
WAVE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_2026-09-05"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_closure_2026-09-05"

REVIEWER_A = [{"packet_id": "CUE-REMED-R3-01", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Draft the first statement", "What we know", "What we're doing", "When we'll update next"], "rationale": "It can produce a verified-facts customer statement with current action and a next-update commitment, while avoiding speculation. However, its first-statement workflow is organized around crisis severity, channel sequencing, legal boundaries, and an acknowledge-first response rather than selecting and drafting the confirmed-cause lifecycle stage requested."}, {"candidate_token": "C-2", "adequacy": "INADEQUATE", "source_anchors": ["Writes a tight escalation summary to engineering or management", "Do NOT use for replying to the customer", "The ask"], "rationale": "This is an internal escalation artifact, not a customer-facing incident update. Its required structure centers on impact quantification, reproduction, prior attempts, evidence, and an internal ask, none of which provides the requested lifecycle-stage communication."}, {"candidate_token": "C-3", "adequacy": "MOST_SUITABLE", "source_anchors": ["Writes customer-facing incident status updates for each lifecycle stage", "Identified (root cause understood, fix may still be in flight)", "We are [SPECIFIC ACTION IN PROGRESS]", "Next update by [TIME]", "never promise a fix time"], "rationale": "The confirmed cause and mitigation-in-progress facts directly fit its Identified stage. Its template supplies the affected symptom, plain-language confirmed cause, current mitigation work, and a specific next-update time while expressly prohibiting a restoration-time promise, speculation, and blame."}], "cue_decision": "AVOIDABLE_IDENTITY_CUE"}]
REVIEWER_B = [{"packet_id": "CUE-REMED-R3-01", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "MOST_SUITABLE", "source_anchors": ["Operating procedure: move to Identified once root cause is understood", "Template set: Identified", "Identified rules: plain-language cause and no blame"], "rationale": "Directly supports the confirmed-cause, mitigation-under-way lifecycle stage and supplies an identified-stage customer update structure with the affected symptom, action in progress, and a concrete next-update time, without requiring a restoration promise or speculation."}, {"candidate_token": "C-2", "adequacy": "INADEQUATE", "source_anchors": ["Description: escalation summary to engineering or management", "Required sections: customer impact, repro steps, already tried, and a single ask", "Do NOT: copy the customer on an internal escalation"], "rationale": "Its required output is an internal escalation package rather than a concise customer-facing incident update, and its mandated sections do not fit the requested lifecycle-stage communication."}, {"candidate_token": "C-3", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Step 3: first statement acknowledgement, verified facts, action, and next-update time", "Description: external communications during an incident or crisis", "Do NOT use: routine technical status posts during normal-severity incidents"], "rationale": "It contains compatible external-incident wording disciplines and a next-update commitment, but is designed for crisis communications with severity classification, channel orchestration, spokesperson control, and possible legal review. The prompt does not establish those broader crisis conditions, so it is less appropriately scoped."}], "cue_decision": "CUE_SAFE"}]
COORDINATOR = [{"packet_id": "CUE-REMED-R3-01", "final_cue_decision": "CUE_SAFE", "rationale": "The wording uses generic incident-communications constraints: affected function, confirmed status, mitigation, next-update commitment, and limits on speculation, restoration promises, and blame. ‘Lifecycle stage’ is broad operational language without a distinctive label, template phrase, organization-specific taxonomy, or other source-identifying marker."}]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def most_source(row: dict[str, Any], order: list[str]) -> str:
    selected = [assessment["candidate_token"] for assessment in row["candidate_assessments"] if assessment["adequacy"] == "MOST_SUITABLE"]
    if len(selected) != 1 or len(order) != 3 or selected[0] not in {"C-1", "C-2", "C-3"}:
        raise SystemExit("Malformed target-blind reviewer return")
    return order[int(selected[0][-1]) - 1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite Wave-3 remediation closure: {out}")
    paths = {"sop": SOP, "wave_summary": WAVE / "summary.json", "reviewer_a_packet": WAVE / "reviewer_a_packet.jsonl", "reviewer_b_packet": WAVE / "reviewer_b_packet.jsonl", "internal_target_join": WAVE / "internal_target_join.jsonl", "phase3_prompts": PHASE3 / "nc_prompt_manifest.jsonl"}
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    packet_a, packet_b, joins = read_jsonl(paths["reviewer_a_packet"]), read_jsonl(paths["reviewer_b_packet"]), read_jsonl(paths["internal_target_join"])
    if not all(len(rows) == 1 for rows in (packet_a, packet_b, joins, REVIEWER_A, REVIEWER_B, COORDINATOR)):
        raise SystemExit("Wave-3 packet/return count drift")
    join = joins[0]
    if join["packet_id"] != "CUE-REMED-R3-01" or REVIEWER_A[0]["packet_id"] != join["packet_id"] or REVIEWER_B[0]["packet_id"] != join["packet_id"]:
        raise SystemExit("Wave-3 packet identity drift")
    a_hashes = [hashlib.sha256(row["complete_original_skill"].encode("utf-8")).hexdigest() for row in packet_a[0]["candidates"]]
    b_hashes = [hashlib.sha256(row["complete_original_skill"].encode("utf-8")).hexdigest() for row in packet_b[0]["candidates"]]
    if a_hashes != list(join["candidate_source_sha256"]) or b_hashes != list(reversed(a_hashes)):
        raise SystemExit("Wave-3 full-source candidate order/replay defect")
    a_most = most_source(REVIEWER_A[0], a_hashes)
    b_most = most_source(REVIEWER_B[0], b_hashes)
    target = str(join["intended_target_source_sha256"])
    if a_most != b_most or a_most != target or COORDINATOR[0]["final_cue_decision"] != "CUE_SAFE":
        raise SystemExit("Wave-3 closure no longer supports reinstatement")
    prompts = {row["audit_prompt_id"]: row for row in read_jsonl(paths["phase3_prompts"]) if row.get("audit_prompt_id")}
    prompt = prompts.get(join["original_audit_prompt_id"])
    if not prompt:
        raise SystemExit("Wave-3 original prompt no longer exists in Phase-3 manifest")
    reconciliation = [{"packet_id": join["packet_id"], "original_audit_prompt_id": join["original_audit_prompt_id"], "audit_cluster_id": prompt["audit_cluster_id"], "family_token": prompt["family_token"], "intended_target_source_sha256": target, "reviewer_a_most_suitable_source_sha256": a_most, "reviewer_b_most_suitable_source_sha256": b_most, "fresh_target_blind_most_suitable": True, "final_cue_decision": "CUE_SAFE", "cue_review_path": "A_B_DISAGREEMENT_SEALED_COORDINATOR"}]
    final = [{**reconciliation[0], "remediation_round": 1, "second_remediation_permitted": False, "final_prompt_disposition": "PASS_REMEDIATION_GATE", "family_disposition": "REINSTATED_LOCAL_FAMILY_ELIGIBLE_AFTER_ONE_PERMITTED_REMEDIATION", "claim_boundary": "No source, rubric, candidate universe, retrieval outcome or acceptable-set label was changed. This one permitted source-grounded remediation passed fresh target-blind and cue review."}]
    counts = {"fresh_packets": 1, "affected_families": 1, "target_most_suitable_after_remediation": 1, "cue_safe_after_resolution": 1, "reinstated_local_families": 1, "second_remediations": 0, "coordinator_resolved_cue_disagreements": 1}
    summary = {"status": "CLOSED_ONE_TIME_REMEDIATION_FINAL_LOCAL_FAMILY_REINSTATED", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in paths.values()}, "counts": counts, "claim_boundary": "The fresh prompt is cue-safe and target-most-suitable after sealed reconciliation. The family is reinstated without a second rewrite. This produces no acceptable-set label, retrieval result or metric.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {"reviewer_a_return.jsonl": REVIEWER_A, "reviewer_b_return.jsonl": REVIEWER_B, "sealed_cue_coordinator_return.jsonl": COORDINATOR, "unblinded_target_reconciliation.jsonl": reconciliation, "final_remediation_dispositions.jsonl": final}
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": counts, "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
