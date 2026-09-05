#!/usr/bin/env python3
"""Seal Wave-2 fresh blinded reviews and close their capped remediation path."""
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
WAVE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_2026-09-05"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_closure_2026-09-05"


# Verbatim independent returns. Candidate tokens remain opaque in these rows.
REVIEWER_A = [
    {"packet_id": "CUE-REMED-R2-01", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "MOST_SUITABLE", "source_anchors": ["GTM Motion Selection", "Ideal Customer Profile (ICP)", "Launch Playbook", "Growth Loops"], "rationale": "Directly covers selecting a primary GTM motion, defining an ICP, selecting channels, designing repeatable growth loops, and executing pre-launch through follow-up measures."}, {"candidate_token": "C-2", "adequacy": "FULLY_ACCEPTABLE", "source_anchors": ["Positioning Strategy", "Go-to-Market Strategy", "GTM Plan Template", "Product-Led Growth"], "rationale": "Provides a complete GTM-plan structure with target customers, positioning, channels, launch phases, success metrics, and product-led growth measures, though its loop guidance is less operationally specific."}, {"candidate_token": "C-3", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Growth Loops Framework", "Growth Models", "Product-Led Growth", "Growth Experimentation"], "rationale": "Strongly supports loop and acquisition-system design, but does not provide a comparably direct staged market-entry and launch playbook with buyer definition, channel selection, and follow-up planning."}], "cue_decision": "CUE_SAFE"},
    {"packet_id": "CUE-REMED-R2-02", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Growth Loops", "Product-Led Growth (PLG)", "Launch Playbook", "Guidelines"], "rationale": "Addresses acquisition motions, loops, activation, conversion, attribution, and cohort retention, but gives limited guidance for cross-functional loop operation, diminishing-return assessment, and evidence thresholds for further budget commitment."}, {"candidate_token": "C-2", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Product-Led Growth", "PLG Metrics", "Go-to-Market Strategy", "Unit Economics"], "rationale": "Supports product-use metrics, acquisition and retention measurement, GTM planning, and economics, but lacks a developed framework for self-reinforcing mechanisms, network effects, and cross-functional operation."}, {"candidate_token": "C-3", "adequacy": "MOST_SUITABLE", "source_anchors": ["Growth Loops Framework", "Network Effects", "Product-Led Growth (PLG)", "Growth Experimentation", "Growth Team & Timing"], "rationale": "Directly addresses compounding loops, participant-value dynamics, product-led growth measures, experiment and commitment criteria, and coordination of product, engineering, data, and marketing."}], "cue_decision": "CUE_SAFE"},
    {"packet_id": "CUE-REMED-R2-03", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "MOST_SUITABLE", "source_anchors": ["Peer Review Workflow", "Methodological and Statistical Rigor", "Reproducibility and Transparency", "Figure and Data Presentation", "Ethical Considerations", "Structuring Peer Review Reports"], "rationale": "Explicitly covers every requested review dimension, including methodology, statistics, ethics, reporting standards, figures and data, evidence-supported conclusions, and structured major, minor, and optional line-level comments."}, {"candidate_token": "C-2", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Dimension-Based Evaluation", "Scoring and Rating", "Synthesize Overall Assessment", "Actionable Feedback"], "rationale": "Provides broad scholarly evaluation of methodology, data, analysis, results interpretation, and writing, but is less specific on ethical reporting, figure review, reporting-guideline compliance, and formal peer-review comment structure."}, {"candidate_token": "C-3", "adequacy": "FULLY_ACCEPTABLE", "source_anchors": ["Review Methodology", "Methodology Assessment", "Strengths and Weaknesses Analysis", "Review Output Template", "Ethical Review Practices"], "rationale": "Provides a structured manuscript-review workflow, assesses methodological and statistical rigor, checks evidence for claims, and produces strengths, weaknesses, questions, minor issues, and actionable recommendations; reporting-guideline and figure-specific coverage is less explicit."}], "cue_decision": "CUE_SAFE"},
]

REVIEWER_B = [
    {"packet_id": "CUE-REMED-R2-01", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Quick Reference", "Part 2: Growth Loops Framework", "Part 7: Growth Experimentation"], "rationale": "Covers acquisition channels, compounding loops, PLG, and experimentation, but lacks a concrete buyer-definition method and a staged market-entry or launch playbook."}, {"candidate_token": "C-2", "adequacy": "FULLY_ACCEPTABLE", "source_anchors": ["Market Analysis: Customer Segments", "Go-to-Market Strategy: GTM Plan Template", "Product-Led Growth: PLG Flywheel"], "rationale": "Provides customer segmentation, positioning, channel strategy, launch phases, success measures, and a PLG flywheel; it can produce the requested plan, though its loop guidance is less operationally detailed than C-3."}, {"candidate_token": "C-3", "adequacy": "MOST_SUITABLE", "source_anchors": ["GTM Motion Selection", "Ideal Customer Profile (ICP)", "Launch Playbook", "Growth Loops"], "rationale": "Directly supports selecting a GTM motion and channels, defining an ICP, designing a repeatable loop, and executing pre-launch, launch, and post-launch measurement activities."}], "cue_decision": "CUE_SAFE"},
    {"packet_id": "CUE-REMED-R2-02", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "MOST_SUITABLE", "source_anchors": ["Part 1: Foundational Truths", "Growth Is Not Marketing", "Part 2: Growth Loops Framework", "Part 5: Network Effects", "Part 7: Growth Experimentation"], "rationale": "Directly addresses product-market fit and retention before growth, cross-functional growth operation, compounding loops, network effects, channel saturation, and evidence-based experimentation."}, {"candidate_token": "C-2", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Market Analysis", "Go-to-Market Strategy", "Product-Led Growth"], "rationale": "Supports market and GTM planning, channels, PLG metrics, and a flywheel, but does not provide substantive guidance for validating sustained need and retention, channel saturation, network effects, or budget-commitment thresholds."}, {"candidate_token": "C-3", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["GTM Motion Selection", "Ideal Customer Profile (ICP)", "Growth Loops", "Guidelines"], "rationale": "Supports GTM motion selection, acquisition loops, ICPs, and cohort-oriented measurement, but lacks the requested PMF and retention validation, cross-functional operating model, diminishing-return assessment, and explicit investment gate."}], "cue_decision": "AVOIDABLE_IDENTITY_CUE"},
    {"packet_id": "CUE-REMED-R2-03", "candidate_assessments": [{"candidate_token": "C-1", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Review Methodology: Phase 2", "Review Output Template", "Review Principles: Ethical Review Practices"], "rationale": "Provides a formal, constructive manuscript-review structure with methodological and statistical assessment, evidence-linked comments, and major/minor issues, but has limited explicit coverage of reporting-guideline compliance, formal ethical reporting, and figure/data-presentation checks."}, {"candidate_token": "C-2", "adequacy": "PARTIALLY_ADEQUATE", "source_anchors": ["Core Evaluation Dimensions", "Methodology & Research Design", "Results & Findings", "Step 5: Provide Actionable Feedback"], "rationale": "Covers research design, ethics, data, analysis, results visualization, evidence alignment, and actionable feedback, but does not specifically operationalize reporting-guideline compliance or a conventional peer-review major/minor-comment format."}, {"candidate_token": "C-3", "adequacy": "MOST_SUITABLE", "source_anchors": ["Stage 3: Methodological and Statistical Rigor", "Stage 4: Reproducibility and Transparency", "Stage 5: Figure and Data Presentation", "Stage 6: Ethical Considerations", "Structuring Peer Review Reports"], "rationale": "Explicitly covers every requested review dimension, including statistical validity, reporting standards, data and figures, ethics, evidence-supported conclusions, and constructive major, minor, and line-level comments."}], "cue_decision": "AVOIDABLE_IDENTITY_CUE"},
]

COORDINATOR = [
    {"packet_id": "CUE-REMED-R2-02", "final_cue_decision": "CUE_SAFE", "rationale": "The prompt specifies a general collaboration-product growth strategy and necessary evaluation dimensions. It contains no uniquely identifying names, proprietary concepts, or distinctive source markers beyond the operational boundary."},
    {"packet_id": "CUE-REMED-R2-03", "final_cue_decision": "CUE_SAFE", "rationale": "Formal manuscript peer review and the listed assessment criteria are standard task language. They establish the required review role and output without disclosing a particular source identity."},
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def most_source(return_row: dict[str, Any], source_order: list[str]) -> str:
    most = [item["candidate_token"] for item in return_row["candidate_assessments"] if item["adequacy"] == "MOST_SUITABLE"]
    if len(most) != 1 or most[0] not in {"C-1", "C-2", "C-3"} or len(source_order) != 3:
        raise SystemExit(f"Malformed target-blind review return: {return_row['packet_id']}")
    return source_order[int(most[0].rsplit("-", 1)[1]) - 1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite Wave-2 remediation closure: {out}")
    paths = {
        "sop": SOP,
        "wave_summary": WAVE / "summary.json",
        "reviewer_a_packet": WAVE / "reviewer_a_packet.jsonl",
        "reviewer_b_packet": WAVE / "reviewer_b_packet.jsonl",
        "internal_target_join": WAVE / "internal_target_join.jsonl",
        "phase3_prompts": PHASE3 / "nc_prompt_manifest.jsonl",
    }
    for path in paths.values():
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    packet_a, packet_b, joins = read_jsonl(paths["reviewer_a_packet"]), read_jsonl(paths["reviewer_b_packet"]), read_jsonl(paths["internal_target_join"])
    expected = ["CUE-REMED-R2-01", "CUE-REMED-R2-02", "CUE-REMED-R2-03"]
    if [row["packet_id"] for row in packet_a] != expected or [row["packet_id"] for row in packet_b] != expected or [row["packet_id"] for row in joins] != expected or [row["packet_id"] for row in REVIEWER_A] != expected or [row["packet_id"] for row in REVIEWER_B] != expected:
        raise SystemExit("Wave-2 packet/return identity drift")
    join_by_packet = {row["packet_id"]: row for row in joins}
    prompt_by_id = {row["audit_prompt_id"]: row for row in read_jsonl(paths["phase3_prompts"]) if row.get("audit_prompt_id")}
    a_by_packet = {row["packet_id"]: row for row in REVIEWER_A}
    b_by_packet = {row["packet_id"]: row for row in REVIEWER_B}
    coordinator_by_packet = {row["packet_id"]: row for row in COORDINATOR}
    reconciled, final_rows = [], []
    for packet_id in expected:
        join = join_by_packet[packet_id]
        original_id = join["original_audit_prompt_id"]
        prompt = prompt_by_id.get(original_id)
        if not prompt:
            raise SystemExit(f"Original prompt missing from Phase-3 manifest: {original_id}")
        source_order_a = list(join["candidate_source_sha256"])
        source_order_b = list(reversed(source_order_a))
        a_most, b_most = most_source(a_by_packet[packet_id], source_order_a), most_source(b_by_packet[packet_id], source_order_b)
        if a_most != b_most:
            raise SystemExit("Wave-2 reviewers disagree on the selected source; target reconciliation requires a sealed coordinator")
        if a_by_packet[packet_id]["cue_decision"] == b_by_packet[packet_id]["cue_decision"]:
            cue, cue_path = a_by_packet[packet_id]["cue_decision"], "A_B_AGREEMENT"
        else:
            coordinator = coordinator_by_packet.get(packet_id)
            if not coordinator:
                raise SystemExit("Cue disagreement lacks sealed coordinator return")
            cue, cue_path = coordinator["final_cue_decision"], "A_B_DISAGREEMENT_SEALED_COORDINATOR"
        target = str(join["intended_target_source_sha256"])
        target_most = a_most == target
        reconciled.append({"packet_id": packet_id, "original_audit_prompt_id": original_id, "audit_cluster_id": prompt["audit_cluster_id"], "family_token": prompt["family_token"], "intended_target_source_sha256": target, "reviewer_a_most_suitable_source_sha256": a_most, "reviewer_b_most_suitable_source_sha256": b_most, "fresh_target_blind_most_suitable": target_most, "final_cue_decision": cue, "cue_review_path": cue_path})
        final_rows.append({"packet_id": packet_id, "original_audit_prompt_id": original_id, "audit_cluster_id": prompt["audit_cluster_id"], "family_token": prompt["family_token"], "remediation_round": 1, "fresh_target_blind_most_suitable": target_most, "final_cue_decision": cue, "second_remediation_permitted": False, "final_prompt_disposition": "PASS_REMEDIATION_GATE" if target_most and cue in {"CUE_SAFE", "DECLARED_NECESSARY_CUE_STRATUM"} else "DEFERRED_TARGET_OR_CUE_GATE_FAILED_AFTER_ONE_PERMITTED_REMEDIATION"})
    if not all(row["fresh_target_blind_most_suitable"] for row in final_rows) or any(row["final_cue_decision"] != "CUE_SAFE" for row in final_rows):
        raise SystemExit("This predeclared Wave-2 closure expects three target-most-suitable and cue-safe decisions; write a new closure if evidence differs")
    family_ids = {row["audit_cluster_id"] for row in final_rows}
    if len(family_ids) != 2:
        raise SystemExit("Wave-2 remediation should affect exactly two local families")
    for row in final_rows:
        row["family_disposition"] = "REINSTATED_LOCAL_FAMILY_ELIGIBLE_AFTER_ONE_PERMITTED_REMEDIATION"
        row["claim_boundary"] = "No source, rubric, candidate universe, retrieval outcome or acceptable-set label was changed. Each prompt used its one permitted remediation and passed fresh target-blind and cue review."
    counts = {"fresh_packets": 3, "affected_families": 2, "target_most_suitable_after_remediation": 3, "cue_safe_after_resolution": 3, "reinstated_local_families": 2, "deferred_local_families": 0, "second_remediations": 0, "coordinator_resolved_cue_disagreements": 2}
    summary = {"status": "CLOSED_ONE_TIME_REMEDIATION_TWO_ADDITIONAL_LOCAL_FAMILIES_REINSTATED", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in paths.values()}, "counts": counts, "claim_boundary": "All three fresh prompts were cue-safe after review closure and both independent reviewers selected the intended source as most suitable. The two affected families are reinstated without another rewrite. This produces no acceptable-set label, retrieval result or metric.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": counts, "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {"reviewer_a_return.jsonl": REVIEWER_A, "reviewer_b_return.jsonl": REVIEWER_B, "sealed_cue_coordinator_return.jsonl": COORDINATOR, "unblinded_target_reconciliation.jsonl": reconciled, "final_remediation_dispositions.jsonl": final_rows}
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": counts, "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
