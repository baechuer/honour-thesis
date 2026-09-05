#!/usr/bin/env python3
"""Materialise exactly one fresh, target-blind review packet per remediable cue."""
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
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_001_2026-09-05_v2"

REMEDIATIONS = {
    "RQ2B-NC-SOURCE-NATIVE-B001-P-d08c88dba2b20964": {
        "revised_prompt": "A recently incorporated German limited-liability company needs help completing the official onboarding form needed to obtain its tax number. First check whether a draft already exists and continue only with the backend-reported incomplete fields; otherwise begin a new draft and use the available valid choices. Gather the required information in small related groups: the notarized company identity, addresses and activity; incorporation and register details; the complete lists of managing directors and owners; capital, activity start and expected results; then revenue, VAT-related selections and refund account. Do not infer missing values, and clearly flag incomplete sections before moving on. Treat this as form-filling support rather than legal or tax advice. Once every section is complete, give a brief completion summary and provide the in-app review handoff; the director must check the rendered filing and personally make any binding submission there.",
        "source_anchors": ["Backend sections.missing is the progress authority; collect a few related fields at a time.", "Resume an unfinished record and use valid-choice lookup before requesting remaining fields.", "Company, registration, director/shareholder, capital/activity/financial and revenue/VAT/bank sections are source-supported.", "When no fields remain, summarize and hand off; final binding submission is in-app, never in chat."],
    },
    "RQ2B-NC-SOURCE-NATIVE-B063-P-7759baff1ea302cc": {
        "revised_prompt": "We are shaping a premium meal-planning service and have customer reviews, support tickets, and a small survey, but no formal segmentation study. Build a practical picture of the customer group we should prioritise first: give a concise overview, one core profile, and two detailed archetypes covering motivations, frustrations, decision habits, discovery channels, and the words they use for their problems and desired outcomes. State which potential buyers should not be prioritised, then translate the findings into implications for the product experience, positioning, messaging, voice, channels, and pricing. Clearly distinguish observed evidence from hypotheses; do not imply that every plausible buyer is equally central.",
        "source_anchors": ["Reviews, interviews, support tickets, NPS and surveys are permitted evidence inputs.", "Prioritisation uses psychographics, behaviours, jobs-to-be-done and customer language.", "One core profile with two to three detailed archetypes is source-supported.", "Explicit exclusions and product, messaging, voice and channel implications are required; limited evidence stays hypothesis-labelled."],
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


def paths(candidate: dict[str, Any]) -> list[str]:
    found: set[str] = set()
    for origin in candidate.get("local_nc_origin_records", []):
        if isinstance(origin, dict):
            for field in (origin, origin.get("provenance_record", {})):
                if isinstance(field, dict) and isinstance(field.get("source_paths"), list):
                    found.update(value for value in field["source_paths"] if isinstance(value, str))
    if not found:
        raise SystemExit(f"Remediation candidate lacks local source path: {candidate.get('canonical_source_sha256')}")
    return sorted(found)


def replay(candidate: dict[str, Any]) -> str:
    source_hash = str(candidate["canonical_source_sha256"])
    for stored in paths(candidate):
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
    prompt_path, cluster_path, candidate_path = PHASE3 / "nc_prompt_manifest.jsonl", PHASE3 / "nc_cluster_manifest.jsonl", PHASE3 / "candidate_source_union.jsonl"
    disposition_path = CUE / "final_prompt_cue_dispositions.jsonl"
    for path in (SOP, prompt_path, cluster_path, candidate_path, disposition_path):
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    prompts = {str(row.get("audit_prompt_id")): row for row in read_jsonl(prompt_path)}
    clusters = {str(row.get("audit_cluster_id")): row for row in read_jsonl(cluster_path) if isinstance(row.get("audit_cluster_id"), str)}
    candidates = {str(row["canonical_source_sha256"]): row for row in read_jsonl(candidate_path)}
    dispositions = {str(row["prompt_id"]): row for row in read_jsonl(disposition_path)}
    if set(REMEDIATIONS) != set(prompts) & set(REMEDIATIONS):
        raise SystemExit("Remediation prompt input drift")
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
        packet_id = f"CUE-REMED-R1-{index:02d}"
        revised = REMEDIATIONS[original_id]["revised_prompt"]
        author_returns.append({"packet_id": packet_id, "original_audit_prompt_id": original_id, "remediation_round": 1, "source_grounded_reason": "Remove independently adjudicated avoidable target-title cue without changing source bytes, rubric, or intended task boundary.", "revised_prompt": revised, "source_anchors": REMEDIATIONS[original_id]["source_anchors"], "author_model": "gpt-5.6-terra", "author_reasoning_effort": "high"})
        member_rows = [{"canonical_source_sha256": source_hash, "complete_original_skill": replay(candidates[str(source_hash)])} for source_hash in hashes]
        for reviewer, ordered in (("A", member_rows), ("B", list(reversed(member_rows)))):
            packet = {"packet_id": packet_id, "reviewer": reviewer, "review_boundary": "Receive only this prompt and three complete original candidates under opaque tokens. Do not infer intended target, author mapping, source path, rank, prior review, benchmark role, retrieval, or acceptable-set outcome.", "prompt": revised, "candidates": [{"candidate_token": f"C-{number}", "complete_original_skill": row["complete_original_skill"]} for number, row in enumerate(ordered, 1)], "return_schema": {"packet_id": packet_id, "candidate_assessments": [{"candidate_token": "C-*", "adequacy": "MOST_SUITABLE | FULLY_ACCEPTABLE | PARTIALLY_ADEQUATE | INADEQUATE | UNCLEAR", "source_anchors": [], "rationale": ""}], "cue_decision": "CUE_SAFE | AVOIDABLE_IDENTITY_CUE | DECLARED_NECESSARY_CUE_STRATUM | UNCLEAR"}}
            (reviewer_a if reviewer == "A" else reviewer_b).append(packet)
        joins.append({"packet_id": packet_id, "original_audit_prompt_id": original_id, "intended_target_source_sha256": prompt["intended_target_source_sha256"], "candidate_source_sha256": hashes, "prompt_sha256": hashlib.sha256(revised.encode("utf-8")).hexdigest(), "claim_boundary": "Withheld from reviewers until returns are sealed."})
    summary = {"status": "PENDING_FRESH_TARGET_BLIND_A_B_REVIEW", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in (SOP, prompt_path, cluster_path, candidate_path, disposition_path)}, "counts": {"one_time_remediations": 2, "preserved_upstream_cross_reuse_quarantined_prompts": 5, "fresh_reviewer_a_packets": 2, "fresh_reviewer_b_packets": 2}, "claim_boundary": "This package preserves superseded prompts and creates exactly one source-grounded remediation per unblocked local cue. It creates no label, family eligibility, audit-input freeze, retrieval result, or metric.", "outputs": {}}
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
