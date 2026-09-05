#!/usr/bin/env python3
"""Materialise the remaining authorised one-time Phase-3 cue remediations."""
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
CUE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_prompt_cue_adjudication_2026-09-05_v2"
REUSE = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cross_cluster_reuse_adjudication_2026-09-05"
WAVE1 = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_001_closure_2026-09-05"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_2026-09-05"


REMEDIATIONS = {
    "RQ2B-NC-SOURCE-NATIVE-B064-P-854fb573d80cf313": {
        "revised_prompt": "Create a market-entry plan for a new business software offering. Define the buyer segment and its key need, choose and justify one primary acquisition approach—self-service trial, direct sales, community building, or customer referrals—then select suitable distribution channels. Design one repeatable mechanism in which each cycle can contribute to the next, and provide a staged preparation, launch, and follow-up plan covering positioning, acquisition actions, milestones, activation, conversion, source attribution, and feedback measures.",
        "source_anchors": ["Choose a primary route based on product and buyer conditions.", "Define the highest-fit buyer before selecting channels.", "Structure preparation, launch, follow-up, compounding acquisition and measurement."],
    },
    "RQ2B-NC-SOURCE-NATIVE-B064-P-a4ec30b0421a742a": {
        "revised_prompt": "Prepare a decision-ready plan for building a durable, compounding acquisition system for a product that helps teams work together. First determine whether the available evidence shows that the product solves a sustained customer need and that customers continue to use it. Choose one primary self-reinforcing mechanism by which existing users or their activity can help attract others; explain how product, engineering, data, and marketing will operate it; assess whether more participants increase value and whether prospective acquisition routes are approaching diminishing returns; and specify the evidence, measures, and threshold required before committing more budget. Return a prioritized plan with rationale, responsibilities, risks, and next milestones.",
        "source_anchors": ["Expansion follows evidence of a sustained customer need and continuing use.", "Use one compounding mechanism operated across product, engineering, data and marketing.", "Assess participant-driven value and diminishing returns in acquisition routes."],
    },
    "RQ2B-NC-SOURCE-NATIVE-B064-P-a8263423308c5aff": {
        "revised_prompt": "Write a formal peer review of this research manuscript. Assess methods, statistical validity, ethical reporting, data and figure presentation, applicable reporting-guideline compliance, and whether conclusions are supported by the evidence. Return constructive major comments, minor comments, and optional section- or line-level notes.",
        "source_anchors": ["Formal scientific-manuscript review covers methodology, statistics, ethics, reporting standards and constructive feedback.", "Assess methods and statistical rigor, figures and data presentation, ethics, reporting standards and evidence-supported conclusions.", "Provide major comments, minor comments and optional specific section- or line-level comments."],
    },
}


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


def source_paths(candidate: dict[str, Any]) -> list[str]:
    found: set[str] = set()
    for origin in candidate.get("local_nc_origin_records", []):
        if not isinstance(origin, dict):
            continue
        for field in (origin, origin.get("provenance_record", {})):
            if isinstance(field, dict) and isinstance(field.get("source_paths"), list):
                found.update(value for value in field["source_paths"] if isinstance(value, str))
    if not found:
        raise SystemExit(f"Remediation candidate lacks a local source path: {candidate.get('canonical_source_sha256')}")
    return sorted(found)


def replay_source(candidate: dict[str, Any]) -> str:
    source_hash = str(candidate["canonical_source_sha256"])
    for stored in source_paths(candidate):
        options = [WORKSPACE / stored]
        if not stored.startswith("skill_benchmark/"):
            options.append(BENCHMARK / stored)
        for path in options:
            if path.is_file() and sha(path) == source_hash:
                return path.read_text(encoding="utf-8", errors="replace")
    raise SystemExit(f"Source-byte replay failed: {source_hash}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out.exists() and not args.validate_only:
        raise SystemExit(f"Refusing to overwrite cue remediation wave: {out}")
    prompt_path = PHASE3 / "nc_prompt_manifest.jsonl"
    cluster_path = PHASE3 / "nc_cluster_manifest.jsonl"
    candidate_path = PHASE3 / "candidate_source_union.jsonl"
    disposition_path = CUE / "final_prompt_cue_dispositions.jsonl"
    reuse_path = REUSE / "final_cross_cluster_dispositions.jsonl"
    wave1_path = WAVE1 / "final_remediation_dispositions.jsonl"
    for path in (SOP, prompt_path, cluster_path, candidate_path, disposition_path, reuse_path, wave1_path):
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    prompts = {str(row.get("audit_prompt_id")): row for row in read_jsonl(prompt_path)}
    clusters = {str(row.get("audit_cluster_id")): row for row in read_jsonl(cluster_path) if isinstance(row.get("audit_cluster_id"), str)}
    candidates = {str(row["canonical_source_sha256"]): row for row in read_jsonl(candidate_path)}
    dispositions = {str(row["prompt_id"]): row for row in read_jsonl(disposition_path)}
    if set(REMEDIATIONS) != set(prompts) & set(REMEDIATIONS):
        raise SystemExit("Remediation prompt input drift")
    source_reuse_target_ids = {
        "RQ2B-NC-SOURCE-NATIVE-B025-P-fb2722090a1e4bdf",
        "RQ2B-NC-SOURCE-NATIVE-B064-P-af9332dbd015d004",
    }
    prior_capped_ids = {str(row["original_audit_prompt_id"]) for row in read_jsonl(wave1_path)}
    local_blocked_ids = {prompt_id for prompt_id, row in dispositions.items() if row.get("phase3_disposition") == "BLOCKED_LOCAL_PROMPT_REMEDIATION_AND_FRESH_BLIND_REVIEW_REQUIRED"}
    if prior_capped_ids != {"RQ2B-NC-SOURCE-NATIVE-B001-P-d08c88dba2b20964", "RQ2B-NC-SOURCE-NATIVE-B063-P-7759baff1ea302cc"}:
        raise SystemExit("Prior capped-remediation roster drift")
    if local_blocked_ids != set(REMEDIATIONS) | source_reuse_target_ids | prior_capped_ids:
        raise SystemExit("Remaining cue remediation roster drift or unauthorised prompt introduced")
    author_returns, reviewer_a, reviewer_b, joins = [], [], [], []
    for index, original_id in enumerate(sorted(REMEDIATIONS), 1):
        prompt = prompts[original_id]
        disposition = dispositions.get(original_id, {})
        if disposition.get("phase3_disposition") != "BLOCKED_LOCAL_PROMPT_REMEDIATION_AND_FRESH_BLIND_REVIEW_REQUIRED":
            raise SystemExit(f"Prompt is not authorised for this single remediation: {original_id}")
        cluster = clusters.get(str(prompt["audit_cluster_id"]))
        hashes = cluster.get("candidate_source_sha256") if isinstance(cluster, dict) else None
        if not isinstance(hashes, list) or len(hashes) != 3 or str(prompt["intended_target_source_sha256"]) not in hashes:
            raise SystemExit(f"Malformed local family join for remediation: {original_id}")
        packet_id = f"CUE-REMED-R2-{index:02d}"
        revised = REMEDIATIONS[original_id]["revised_prompt"]
        author_returns.append({"packet_id": packet_id, "original_audit_prompt_id": original_id, "remediation_round": 1, "source_grounded_reason": "Remove independently adjudicated avoidable identity cue without changing source bytes, rubric or intended task boundary.", "revised_prompt": revised, "source_anchors": REMEDIATIONS[original_id]["source_anchors"], "author_model": "gpt-5.6-terra", "author_reasoning_effort": "high"})
        member_rows = [{"canonical_source_sha256": source_hash, "complete_original_skill": replay_source(candidates[str(source_hash)])} for source_hash in hashes]
        for reviewer, ordered in (("A", member_rows), ("B", list(reversed(member_rows)))):
            packet = {"packet_id": packet_id, "reviewer": reviewer, "review_boundary": "Receive only this prompt and three complete original candidates under opaque tokens. Do not infer intended target, author mapping, source path, rank, prior review, benchmark role, retrieval or acceptable-set outcome.", "prompt": revised, "candidates": [{"candidate_token": f"C-{number}", "complete_original_skill": row["complete_original_skill"]} for number, row in enumerate(ordered, 1)], "return_schema": {"packet_id": packet_id, "candidate_assessments": [{"candidate_token": "C-*", "adequacy": "MOST_SUITABLE | FULLY_ACCEPTABLE | PARTIALLY_ADEQUATE | INADEQUATE | UNCLEAR", "source_anchors": [], "rationale": ""}], "cue_decision": "CUE_SAFE | AVOIDABLE_IDENTITY_CUE | DECLARED_NECESSARY_CUE_STRATUM | UNCLEAR"}}
            (reviewer_a if reviewer == "A" else reviewer_b).append(packet)
        joins.append({"packet_id": packet_id, "original_audit_prompt_id": original_id, "intended_target_source_sha256": prompt["intended_target_source_sha256"], "candidate_source_sha256": hashes, "prompt_sha256": hashlib.sha256(revised.encode("utf-8")).hexdigest(), "claim_boundary": "Withheld from reviewers until returns are sealed."})
    summary = {"status": "PENDING_FRESH_TARGET_BLIND_A_B_REVIEW", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in (SOP, prompt_path, cluster_path, candidate_path, disposition_path, reuse_path, wave1_path)}, "counts": {"one_time_remediations": 3, "affected_families": 2, "prior_capped_remediation_prompts": 2, "remaining_source_reuse_exclusion_prompts": 2, "fresh_reviewer_a_packets": 3, "fresh_reviewer_b_packets": 3}, "claim_boundary": "This package preserves superseded prompts and creates exactly one source-grounded remediation per remaining remediable local cue. It creates no label, family eligibility, audit-input freeze, retrieval result or metric.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {"author_return.jsonl": author_returns, "reviewer_a_packet.jsonl": reviewer_a, "reviewer_b_packet.jsonl": reviewer_b, "internal_target_join.jsonl": joins}
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
