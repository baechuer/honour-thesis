#!/usr/bin/env python3
"""Materialise the final authorised one-time Phase-3 cue remediation."""
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
SEMANTIC = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_semantic_qa_300plus_2026-09-05_v2"
OUT = BENCHMARK / "rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_2026-09-05"

ORIGINAL_ID = "RQ2B-NC-SOURCE-NATIVE-B025-P-fb2722090a1e4bdf"
REVISED_PROMPT = "Customers are currently unable to complete purchases. The cause has been confirmed and mitigation work is under way. Draft a concise customer-facing incident update for the appropriate lifecycle stage. Use plain language, state the affected function and current work, and commit to a specific next-update time. Do not promise a restoration time, speculate beyond verified facts, or assign blame."
SOURCE_ANCHORS = ["Collect observable symptom, affected scope, lifecycle stage and confirmed cause.", "For confirmed cause, state plain-language cause, action in progress and next-update time.", "Do not use jargon, blame or speculative restoration timing."]


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
        if isinstance(origin, dict):
            for field in (origin, origin.get("provenance_record", {})):
                if isinstance(field, dict) and isinstance(field.get("source_paths"), list):
                    found.update(value for value in field["source_paths"] if isinstance(value, str))
    if not found:
        raise SystemExit(f"Missing local source path: {candidate.get('canonical_source_sha256')}")
    return sorted(found)


def replay_source(candidate: dict[str, Any]) -> str:
    source_hash = str(candidate["canonical_source_sha256"])
    for stored in source_paths(candidate):
        locations = [WORKSPACE / stored]
        if not stored.startswith("skill_benchmark/"):
            locations.append(BENCHMARK / stored)
        for location in locations:
            if location.is_file() and sha(location) == source_hash:
                return location.read_text(encoding="utf-8", errors="replace")
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
    cue_path = CUE / "final_prompt_cue_dispositions.jsonl"
    source_screen_path = SEMANTIC / "source_relation_screen.jsonl"
    for path in (SOP, prompt_path, cluster_path, candidate_path, cue_path, source_screen_path):
        if not path.is_file():
            raise SystemExit(f"Missing required binding: {path}")
    prompts = {str(row.get("audit_prompt_id")): row for row in read_jsonl(prompt_path)}
    clusters = {str(row.get("audit_cluster_id")): row for row in read_jsonl(cluster_path) if isinstance(row.get("audit_cluster_id"), str)}
    candidates = {str(row["canonical_source_sha256"]): row for row in read_jsonl(candidate_path)}
    cue = {str(row["prompt_id"]): row for row in read_jsonl(cue_path)}
    prompt = prompts.get(ORIGINAL_ID)
    if not prompt or cue.get(ORIGINAL_ID, {}).get("phase3_disposition") != "BLOCKED_LOCAL_PROMPT_REMEDIATION_AND_FRESH_BLIND_REVIEW_REQUIRED":
        raise SystemExit("The lone remaining B025 prompt is not authorised for this remediation")
    cluster = clusters.get(str(prompt["audit_cluster_id"]))
    hashes = cluster.get("candidate_source_sha256") if isinstance(cluster, dict) else None
    if not isinstance(hashes, list) or len(hashes) != 3 or prompt["intended_target_source_sha256"] not in hashes:
        raise SystemExit("Malformed B025 family join")
    source_reuse_clusters = {cluster_id for row in read_jsonl(source_screen_path) for cluster_id in row["local_cluster_ids"]}
    if prompt["audit_cluster_id"] in source_reuse_clusters:
        raise SystemExit("B025 prompt family is source-reuse excluded and must not receive remediation")
    author = [{"packet_id": "CUE-REMED-R3-01", "original_audit_prompt_id": ORIGINAL_ID, "remediation_round": 1, "source_grounded_reason": "Remove independently adjudicated avoidable implementation-specific cue without changing source bytes, rubric or intended task boundary.", "revised_prompt": REVISED_PROMPT, "source_anchors": SOURCE_ANCHORS, "author_model": "gpt-5.6-terra", "author_reasoning_effort": "high"}]
    members = [{"canonical_source_sha256": source_hash, "complete_original_skill": replay_source(candidates[str(source_hash)])} for source_hash in hashes]
    reviewer_packets = {}
    for reviewer, ordered in (("A", members), ("B", list(reversed(members)))):
        reviewer_packets[reviewer] = [{"packet_id": "CUE-REMED-R3-01", "reviewer": reviewer, "review_boundary": "Receive only this prompt and three complete original candidates under opaque tokens. Do not infer intended target, author mapping, source path, rank, prior review, benchmark role, retrieval or acceptable-set outcome.", "prompt": REVISED_PROMPT, "candidates": [{"candidate_token": f"C-{number}", "complete_original_skill": member["complete_original_skill"]} for number, member in enumerate(ordered, 1)], "return_schema": {"packet_id": "CUE-REMED-R3-01", "candidate_assessments": [{"candidate_token": "C-*", "adequacy": "MOST_SUITABLE | FULLY_ACCEPTABLE | PARTIALLY_ADEQUATE | INADEQUATE | UNCLEAR", "source_anchors": [], "rationale": ""}], "cue_decision": "CUE_SAFE | AVOIDABLE_IDENTITY_CUE | DECLARED_NECESSARY_CUE_STRATUM | UNCLEAR"}}]
    joins = [{"packet_id": "CUE-REMED-R3-01", "original_audit_prompt_id": ORIGINAL_ID, "intended_target_source_sha256": prompt["intended_target_source_sha256"], "candidate_source_sha256": hashes, "prompt_sha256": hashlib.sha256(REVISED_PROMPT.encode("utf-8")).hexdigest(), "claim_boundary": "Withheld from reviewers until returns are sealed."}]
    summary = {"status": "PENDING_FRESH_TARGET_BLIND_A_B_REVIEW", "bound_inputs": {str(path.relative_to(WORKSPACE)): sha(path) for path in (SOP, prompt_path, cluster_path, candidate_path, cue_path, source_screen_path)}, "counts": {"one_time_remediations": 1, "affected_families": 1, "fresh_reviewer_a_packets": 1, "fresh_reviewer_b_packets": 1}, "claim_boundary": "This package preserves the superseded prompt and creates its one permitted source-grounded remediation. It creates no label, family eligibility, audit-input freeze, retrieval result or metric.", "outputs": {}}
    if args.validate_only:
        print(json.dumps({"counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
        return 0
    out.mkdir(parents=True)
    outputs = {"author_return.jsonl": author, "reviewer_a_packet.jsonl": reviewer_packets["A"], "reviewer_b_packet.jsonl": reviewer_packets["B"], "internal_target_join.jsonl": joins}
    for name, rows in outputs.items():
        write_jsonl(out / name, rows)
        summary["outputs"][name] = sha(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "counts": summary["counts"], "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
