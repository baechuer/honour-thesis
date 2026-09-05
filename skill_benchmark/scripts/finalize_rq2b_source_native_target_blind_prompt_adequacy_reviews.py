#!/usr/bin/env python3
"""Bind reconciled blind adequacy judgments back to intended targets without admission."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
ADEQUACY_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets/reconciliation/prompt_authoring/target_blind_adequacy_packets"

INTEGRITY_CODES = {"CUE_SAFE", "CUE_RISK", "SOURCE_UNSUPPORTED_OR_MALFORMED"}
CANDIDATE_CODES = {"MOST_SUITABLE", "FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR_FROM_SOURCE"}


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


def decisions_from_return(row: dict[str, Any]) -> tuple[str, dict[str, str]]:
    integrity = row.get("prompt_integrity")
    assessments = row.get("candidate_assessments")
    if integrity not in INTEGRITY_CODES or not isinstance(assessments, list):
        raise SystemExit(f"Invalid coordinator adequacy return: {row.get('prompt_token')}")
    decisions = {str(item.get("candidate_token")): item.get("decision") for item in assessments}
    if len(decisions) != 3 or any(value not in CANDIDATE_CODES for value in decisions.values()):
        raise SystemExit(f"Invalid coordinator candidate decisions: {row.get('prompt_token')}")
    return str(integrity), {str(key): str(value) for key, value in decisions.items()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finalize a reconciled target-blind adequacy packet set.")
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
    key_path = adequacy_dir / "internal_reconciliation_key.jsonl"
    reconciliation_dir = adequacy_dir / "reconciliation"
    direct_path = reconciliation_dir / "direct_agreements.jsonl"
    coordinator_packet_path = reconciliation_dir / "coordinator_packet.jsonl"
    coordinator_return_path = reconciliation_dir / "coordinator_return.jsonl"
    output_dir = reconciliation_dir / "final_prompt_dispositions"
    required = [key_path, direct_path, coordinator_packet_path, coordinator_return_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    key_rows = read_jsonl(key_path)
    direct_rows = read_jsonl(direct_path)
    coordinator_packet_rows = read_jsonl(coordinator_packet_path)
    coordinator_returns = read_jsonl(coordinator_return_path)
    key_by_token = {str(row["prompt_token"]): row for row in key_rows}
    direct_by_token = {str(row["prompt_token"]): row for row in direct_rows}
    coordinator_packet_tokens = {str(row["prompt_token"]) for row in coordinator_packet_rows}
    coordinator_by_token = {str(row.get("prompt_token")): row for row in coordinator_returns}
    if len(key_rows) != len(key_by_token) or len(key_rows) != args.expected_prompts:
        raise SystemExit(f"Expected {args.expected_prompts} unique internal prompt bindings")
    if len(direct_rows) != len(direct_by_token) or len(coordinator_returns) != len(coordinator_by_token):
        raise SystemExit("Duplicate direct/coordinator decisions")
    if set(direct_by_token) & set(coordinator_by_token) or set(coordinator_by_token) != coordinator_packet_tokens:
        raise SystemExit("Direct/coordinator partition mismatch")
    if set(direct_by_token) | set(coordinator_by_token) != set(key_by_token):
        raise SystemExit("Reconciled reviews do not reconstruct internal prompt bindings")

    final_rows: list[dict[str, Any]] = []
    for token, key in sorted(key_by_token.items()):
        if token in direct_by_token:
            row = direct_by_token[token]
            integrity = str(row.get("prompt_integrity"))
            decisions = {str(k): str(v) for k, v in row.get("candidate_decisions", {}).items()}
            route = "DIRECT_A_B_AGREEMENT"
        else:
            integrity, decisions = decisions_from_return(coordinator_by_token[token])
            route = "INDEPENDENT_DISAGREEMENT_ADJUDICATION"
        candidates = key.get("candidates")
        target_sha = key.get("intended_target_source_sha256")
        if not isinstance(candidates, list) or len(candidates) != 3:
            raise SystemExit(f"Invalid internal candidate binding: {token}")
        candidate_to_sha = {str(item["candidate_token"]): str(item["canonical_source_sha256"]) for item in candidates}
        if set(decisions) != set(candidate_to_sha):
            raise SystemExit(f"Candidate decision/binding mismatch: {token}")
        target_candidate = next((candidate for candidate, sha in candidate_to_sha.items() if sha == target_sha), None)
        if target_candidate is None:
            raise SystemExit(f"Target binding missing: {token}")
        target_decision = decisions[target_candidate]
        alternatives = [
            {"candidate_token": candidate, "decision": decision}
            for candidate, decision in sorted(decisions.items()) if candidate != target_candidate
        ]
        if integrity == "CUE_RISK":
            disposition = "REMEDIATE_CUE_RISK"
        elif integrity == "SOURCE_UNSUPPORTED_OR_MALFORMED":
            disposition = "REJECT_OR_REMEDIATE_SOURCE_UNSUPPORTED"
        elif target_decision != "MOST_SUITABLE":
            disposition = "REMEDIATE_INTENDED_TARGET_NOT_MOST_SUITABLE"
        else:
            disposition = "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"
        final_rows.append({
            "prompt_token": token,
            "family_token": key["family_token"],
            "intended_target_member_token": key["intended_target_member_token"],
            "prompt_integrity": integrity,
            "intended_target_blind_decision": target_decision,
            "non_target_local_adequacy": alternatives,
            "review_route": route,
            "final_prompt_disposition": disposition,
            "claim_boundary": "Local three-source prompt adequacy only; no whole-library acceptable set, final-library admission, retrieval metric or benchmark result is established.",
        })
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in final_rows:
        by_family[str(row["family_token"])].append(row)
    family_rows = []
    for family_token, rows in sorted(by_family.items()):
        all_pass = len(rows) == 3 and all(row["final_prompt_disposition"] == "PASSES_TO_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT" for row in rows)
        family_rows.append({
            "family_token": family_token,
            "prompt_count": len(rows),
            "family_disposition": "ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT" if all_pass else "RETAIN_AS_UNADMITTED_REVIEW_RECORD",
            "prompt_disposition_counts": dict(sorted(Counter(row["final_prompt_disposition"] for row in rows).items())),
            "claim_boundary": "Eligibility only; a final cluster/source/prompt library admission requires a later whole-library acceptable-set audit and freeze QA.",
        })
    output_dir.mkdir(parents=True)
    prompt_path = output_dir / "reconciled_prompt_dispositions.jsonl"
    family_path = output_dir / "family_gate_dispositions.jsonl"
    write_jsonl(prompt_path, final_rows)
    write_jsonl(family_path, family_rows)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_TARGET_BLIND_ADEQUACY_FINALISED_NO_FINAL_LIBRARY_ADMISSION",
        "bound_inputs": {relative(key_path): sha256_file(key_path), relative(direct_path): sha256_file(direct_path), relative(coordinator_packet_path): sha256_file(coordinator_packet_path), relative(coordinator_return_path): sha256_file(coordinator_return_path)},
        "counts": {"prompts": len(final_rows), "families": len(family_rows), "prompt_dispositions": dict(sorted(Counter(row["final_prompt_disposition"] for row in final_rows).items())), "family_dispositions": dict(sorted(Counter(row["family_disposition"] for row in family_rows).items()))},
        "outputs": {"reconciled_prompt_dispositions.jsonl": sha256_file(prompt_path), "family_gate_dispositions.jsonl": sha256_file(family_path)},
        "claim_boundary": "A target-blind local adequacy outcome is not a whole-library acceptable-set result and does not admit a prompt, cluster or source to the final RQ2 library.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
