#!/usr/bin/env python3
"""Validate a hash-bound, role-hidden Phase-4 independent batch return."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v4-unified-8candidate-blind-delivery"
BATCH_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-unified-target-blind-batches-2026-09-05"
RETURN_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-unified-independent-returns-2026-09-05"
ALLOWED = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}
FORBIDDEN_RENDER_KEYS = {"packet_kind", "tail_kind", "lane_id", "reporting_stratum", "reporting_group", "allocation_slot", "selection_channel", "rank_position", "channel_score", "canonical_source_sha256", "source_path", "target", "historical_gold", "local_roster"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("reviewer_output_sha256", None)
    return hashlib.sha256(json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def keys_deep(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | set().union(*(keys_deep(item) for item in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(keys_deep(item) for item in value)) if value else set()
    return set()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--reviewer", choices=("A", "B"), required=True)
    parser.add_argument("--return-file", type=Path)
    args = parser.parse_args()
    execution_summary = json.loads((EXECUTION / "summary.json").read_text(encoding="utf-8"))
    if execution_summary.get("status") != "PASS_PHASE4_UNIFIED_BLIND_REVIEW_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS":
        raise SystemExit("Unified execution status drift")
    for name, expected in execution_summary["outputs"].items():
        path = EXECUTION / name
        if not path.is_file() or sha(path) != expected:
            raise SystemExit(f"Unified freeze hash drift: {name}")
    manifest = next((json.loads(line) for line in (EXECUTION / "unified_prompt_group_batch_manifest.jsonl").read_text(encoding="utf-8").splitlines() if line and json.loads(line)["batch_id"] == args.batch_id), None)
    if manifest is None:
        raise SystemExit("Unknown unified batch")
    batch_path = BATCH_ROOT / f"reviewer_{args.reviewer}" / f"{args.batch_id}.json"
    if not batch_path.is_file():
        raise SystemExit("Missing frozen unified reviewer rendering")
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    if keys_deep(batch) & FORBIDDEN_RENDER_KEYS:
        raise SystemExit(f"Reviewer rendering leakage: {sorted(keys_deep(batch) & FORBIDDEN_RENDER_KEYS)}")
    packet = batch.get("packet")
    if not isinstance(packet, dict) or packet.get("blind_packet_id") != manifest["blind_packet_id"] or len(packet.get("candidates", [])) != 8:
        raise SystemExit("Unified rendering cardinality or identity drift")
    if [candidate["candidate_token"] for candidate in packet["candidates"]] != sorted(candidate["candidate_token"] for candidate in packet["candidates"]):
        raise SystemExit("Unified candidate order drift")
    return_path = args.return_file or (RETURN_ROOT / f"reviewer_{args.reviewer}" / f"{args.batch_id}.json")
    if not return_path.is_file():
        raise SystemExit(f"Missing reviewer return: {return_path}")
    returned = json.loads(return_path.read_text(encoding="utf-8"))
    schema = json.loads((EXECUTION / "unified_independent_reviewer_return_schema.json").read_text(encoding="utf-8"))
    required = set(schema["required_top_level"])
    if required - set(returned):
        raise SystemExit(f"Return lacks fields: {sorted(required - set(returned))}")
    if returned["reviewer_blind_id"] != args.reviewer or returned["batch_id"] != args.batch_id or returned["blind_packet_id"] != manifest["blind_packet_id"]:
        raise SystemExit("Return reviewer/batch/packet identity drift")
    if returned["batch_input_sha256"] != batch["batch_input_sha256"] or returned["reviewer_instruction_sha256"] != manifest["reviewer_instruction_sha256"] or returned["reviewer_output_sha256"] != canonical_sha(returned):
        raise SystemExit("Return hash binding drift")
    assessments = returned.get("assessments")
    expected_tokens = {candidate["candidate_token"] for candidate in packet["candidates"]}
    if not isinstance(assessments, list) or len(assessments) != 8 or {assessment.get("candidate_token") for assessment in assessments} != expected_tokens:
        raise SystemExit("Return candidate partition drift")
    for assessment in assessments:
        if assessment.get("adequacy") not in ALLOWED or not isinstance(assessment.get("source_anchor"), str) or not assessment["source_anchor"].strip() or not isinstance(assessment.get("rationale"), str) or not assessment["rationale"].strip() or (assessment.get("missing_material_requirement_or_null") is not None and not isinstance(assessment.get("missing_material_requirement_or_null"), str)):
            raise SystemExit("Invalid assessment record")
    print(json.dumps({"assessments": 8, "batch_id": args.batch_id, "return_sha256": sha(return_path), "reviewer": args.reviewer, "status": "PASS_UNIFIED_TARGET_BLIND_RETURN_VALIDATION"}, sort_keys=True))


if __name__ == "__main__":
    main()
