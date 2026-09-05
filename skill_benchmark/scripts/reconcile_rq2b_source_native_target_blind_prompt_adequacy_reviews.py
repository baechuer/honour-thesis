#!/usr/bin/env python3
"""Validate independent target-blind prompt adequacy reviews and isolate disagreements."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
ADEQUACY_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets/reconciliation/prompt_authoring/target_blind_adequacy_packets"

INTEGRITY_CODES = {"CUE_SAFE", "CUE_RISK", "SOURCE_UNSUPPORTED_OR_MALFORMED"}
CANDIDATE_CODES = {
    "MOST_SUITABLE",
    "FULLY_ACCEPTABLE",
    "PARTIALLY_ADEQUATE",
    "INADEQUATE",
    "UNCLEAR_FROM_SOURCE",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_returns(rows: list[dict[str, Any]], packet_by_token: dict[str, dict[str, Any]], reviewer: str) -> dict[str, dict[str, Any]]:
    by_token = {str(row.get("prompt_token")): row for row in rows}
    if len(rows) != len(by_token) or set(by_token) != set(packet_by_token):
        raise SystemExit(f"{reviewer} return does not exactly reconstruct the prompt packet")
    validated: dict[str, dict[str, Any]] = {}
    for token, row in by_token.items():
        candidate_tokens = {str(candidate["candidate_token"]) for candidate in packet_by_token[token]["candidate_sources"]}
        if row.get("prompt_integrity") not in INTEGRITY_CODES or not nonempty(row.get("prompt_integrity_evidence")) or not nonempty(row.get("prompt_adequacy_summary")):
            raise SystemExit(f"{reviewer} invalid prompt integrity fields: {token}")
        assessments = row.get("candidate_assessments")
        if not isinstance(assessments, list) or len(assessments) != 3:
            raise SystemExit(f"{reviewer} invalid candidate assessment cardinality: {token}")
        decisions: dict[str, str] = {}
        for assessment in assessments:
            candidate_token = str(assessment.get("candidate_token"))
            decision = assessment.get("decision")
            evidence = assessment.get("evidence")
            if candidate_token not in candidate_tokens or candidate_token in decisions or decision not in CANDIDATE_CODES:
                raise SystemExit(f"{reviewer} invalid candidate decision: {token}/{candidate_token}")
            if not isinstance(evidence, list) or not evidence or not all(nonempty(item) for item in evidence):
                raise SystemExit(f"{reviewer} invalid candidate evidence: {token}/{candidate_token}")
            decisions[candidate_token] = decision
        if set(decisions) != candidate_tokens:
            raise SystemExit(f"{reviewer} candidate tokens mismatch: {token}")
        validated[token] = row
    return validated


def signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "prompt_integrity": row["prompt_integrity"],
        "candidate_decisions": {
            str(assessment["candidate_token"]): assessment["decision"]
            for assessment in row["candidate_assessments"]
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile a hash-bound target-blind adequacy packet set.")
    parser.add_argument("--packet-dir", type=Path, default=ADEQUACY_DIR)
    parser.add_argument("--expected-prompts", type=int, default=12)
    parser.add_argument("--batch-label", default="BATCH_001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_prompts < 1:
        raise SystemExit("--expected-prompts must be positive")
    if not args.batch_label.strip():
        raise SystemExit("--batch-label must be non-empty")
    adequacy_dir = args.packet_dir.resolve()
    packet_path = adequacy_dir / "reviewer_a_packet.jsonl"
    return_a_path = adequacy_dir / "reviewer_a_return.jsonl"
    return_b_path = adequacy_dir / "reviewer_b_return.jsonl"
    reconciliation_dir = adequacy_dir / "reconciliation"
    required = [packet_path, return_a_path, return_b_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if reconciliation_dir.exists():
        raise SystemExit(f"Output directory already exists: {reconciliation_dir}")
    packets = read_jsonl(packet_path)
    packet_by_token = {str(row["prompt_token"]): row for row in packets}
    if len(packets) != len(packet_by_token) or len(packets) != args.expected_prompts:
        raise SystemExit(f"Expected exactly {args.expected_prompts} unique target-blind prompts")
    a = validate_returns(read_jsonl(return_a_path), packet_by_token, "reviewer_a")
    b = validate_returns(read_jsonl(return_b_path), packet_by_token, "reviewer_b")

    direct: list[dict[str, Any]] = []
    disagreements: list[dict[str, Any]] = []
    coordinator: list[dict[str, Any]] = []
    for token in sorted(packet_by_token):
        if signature(a[token]) == signature(b[token]):
            direct.append({
                "prompt_token": token,
                "prompt_integrity": a[token]["prompt_integrity"],
                "candidate_decisions": signature(a[token])["candidate_decisions"],
                "reviewer_a_return": a[token],
                "reviewer_b_return": b[token],
            })
        else:
            disagreements.append({
                "prompt_token": token,
                "reviewer_a_signature": signature(a[token]),
                "reviewer_b_signature": signature(b[token]),
            })
            coordinator.append({
                "record_type": "source_native_target_blind_prompt_adequacy_adjudication",
                "prompt_token": token,
                "natural_user_task_prompt": packet_by_token[token]["natural_user_task_prompt"],
                "candidate_sources": packet_by_token[token]["candidate_sources"],
                "review_instructions": packet_by_token[token]["review_instructions"],
                "reviewer_a_assessment": a[token],
                "reviewer_b_assessment": b[token],
                "required_return": packet_by_token[token]["required_return"],
            })

    reconciliation_dir.mkdir(parents=True)
    direct_path = reconciliation_dir / "direct_agreements.jsonl"
    disagreement_path = reconciliation_dir / "disagreement_index.jsonl"
    coordinator_path = reconciliation_dir / "coordinator_packet.jsonl"
    template_path = reconciliation_dir / "coordinator_return_template.json"
    write_jsonl(direct_path, direct)
    write_jsonl(disagreement_path, disagreements)
    write_jsonl(coordinator_path, coordinator)
    write_json(template_path, {
        "prompt_token": "P-...",
        "prompt_integrity": "CUE_SAFE",
        "prompt_integrity_evidence": "...",
        "candidate_assessments": [{"candidate_token": "C-1", "decision": "MOST_SUITABLE", "evidence": ["..."]}],
        "prompt_adequacy_summary": "...",
    })
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_TARGET_BLIND_ADEQUACY_RECONCILIATION_PACKETS_NO_FINAL_PROMPT_DECISION_YET",
        "bound_inputs": {relative(packet_path): sha256_file(packet_path), relative(return_a_path): sha256_file(return_a_path), relative(return_b_path): sha256_file(return_b_path)},
        "counts": {"prompts": len(packets), "direct_agreements": len(direct), "disagreements_for_adjudication": len(coordinator)},
        "outputs": {"direct_agreements.jsonl": sha256_file(direct_path), "disagreement_index.jsonl": sha256_file(disagreement_path), "coordinator_packet.jsonl": sha256_file(coordinator_path), "coordinator_return_template.json": sha256_file(template_path)},
        "claim_boundary": "Reconciliation packets only; the coordinator remains target-blind and no prompt/family/library admission decision has been made.",
    }
    write_json(reconciliation_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
