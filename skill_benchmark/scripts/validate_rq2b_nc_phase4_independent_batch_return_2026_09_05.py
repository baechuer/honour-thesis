#!/usr/bin/env python3
"""Validate one sealed Phase-4 target-blind batch return without adjudicating it."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
EXECUTION = NC_ROOT / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v3_review-execution-batch-return-repair"
BATCH_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-target-blind-batches-2026-09-05_v2_batch-return-repair"
RETURN_ROOT = NC_ROOT / "review/RQ2B-NC-phase4-independent-returns-2026-09-05_v2_batch-return-schema"
ALLOWED = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("reviewer_output_sha256", None)
    return hashlib.sha256(json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--reviewer", required=True, choices=("A", "B"))
    parser.add_argument("--return-file", type=Path)
    args = parser.parse_args()
    return_path = args.return_file or (RETURN_ROOT / f"reviewer_{args.reviewer}" / f"{args.batch_id}.json")
    if not return_path.is_file():
        raise SystemExit(f"Missing reviewer return: {return_path}")
    batch_path = BATCH_ROOT / f"reviewer_{args.reviewer}" / f"{args.batch_id}.json"
    if not batch_path.is_file():
        raise SystemExit(f"Missing frozen blinded batch: {batch_path}")
    schema_path = EXECUTION / "independent_reviewer_return_schema.json"
    manifest_path = EXECUTION / "prompt_group_batch_manifest.jsonl"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    returned = json.loads(return_path.read_text(encoding="utf-8"))
    expected_manifest = next((json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines() if line and json.loads(line)["batch_id"] == args.batch_id), None)
    if expected_manifest is None:
        raise SystemExit("Batch is absent from execution manifest")
    required = set(schema["required_top_level"])
    if required - set(returned):
        raise SystemExit(f"Return lacks required fields: {sorted(required - set(returned))}")
    if returned["reviewer_blind_id"] != args.reviewer or returned["batch_id"] != args.batch_id:
        raise SystemExit("Reviewer or batch identity mismatch")
    if returned["batch_input_sha256"] != batch["batch_input_sha256"] or returned["reviewer_instruction_sha256"] != expected_manifest["reviewer_instruction_sha256"]:
        raise SystemExit("Return does not bind the frozen batch/instruction")
    if returned["reviewer_output_sha256"] != canonical_sha(returned):
        raise SystemExit("Reviewer output SHA-256 is invalid")
    expected_packets = {packet["packet_id"]: packet for packet in batch["packets"]}
    records = returned["packet_returns"]
    if not isinstance(records, list) or len(records) != 3 or {record.get("packet_id") for record in records} != set(expected_packets):
        raise SystemExit("Return packet partition drift")
    total = 0
    for record in records:
        packet = expected_packets[record["packet_id"]]
        if record.get("packet_sha256") != packet["packet_sha256"]:
            raise SystemExit(f"Packet SHA mismatch: {record['packet_id']}")
        assessments = record.get("assessments")
        expected_tokens = {candidate["candidate_token"] for candidate in packet["candidates"]}
        if not isinstance(assessments, list) or len(assessments) != len(expected_tokens) or {assessment.get("candidate_token") for assessment in assessments} != expected_tokens:
            raise SystemExit(f"Candidate-token partition drift: {record['packet_id']}")
        for assessment in assessments:
            if assessment.get("adequacy") not in ALLOWED:
                raise SystemExit("Invalid adequacy label")
            if not isinstance(assessment.get("source_anchor"), str) or not assessment["source_anchor"].strip() or not isinstance(assessment.get("rationale"), str) or not assessment["rationale"].strip():
                raise SystemExit("Each assessment requires nonempty source anchor and rationale")
            missing = assessment.get("missing_material_requirement_or_null")
            if missing is not None and not isinstance(missing, str):
                raise SystemExit("Missing-requirement value must be string or null")
        total += len(assessments)
    if total != 8:
        raise SystemExit("Batch must contain exactly eight assessments")
    print(json.dumps({"batch_id": args.batch_id, "return_file": str(return_path), "return_sha256": sha(return_path), "reviewer": args.reviewer, "assessments": total, "status": "PASS_SEALED_TARGET_BLIND_RETURN_VALIDATION"}, sort_keys=True))


if __name__ == "__main__":
    main()
