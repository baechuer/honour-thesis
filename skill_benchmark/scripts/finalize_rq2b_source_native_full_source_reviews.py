#!/usr/bin/env python3
"""Finalize source-family dispositions after A/B and disagreement adjudication."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PACKET_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets"

VALID_DECISIONS = {
    "PASS_TO_PROMPT_AUTHORING",
    "REJECT_TOPIC_ONLY",
    "REJECT_COMPONENT_OR_COMPOSITION",
    "REJECT_GENERIC_SPECIALIST",
    "REJECT_NEAR_DUPLICATE_OR_FORK",
    "REJECT_NO_BOUNDED_ENVELOPE",
    "REJECT_NO_MEMBER_LEVEL_PROMPTABILITY",
    "DEFER_PROVENANCE_OR_LICENSE",
    "DEFER_INSUFFICIENT_SOURCE_EVIDENCE",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finalize reconciled full-source family dispositions.")
    parser.add_argument("--packet-dir", type=Path, default=PACKET_DIR)
    parser.add_argument("--expected-families", type=int, default=25)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    packet_dir = args.packet_dir.resolve()
    reconciliation_dir = packet_dir / "reconciliation"
    direct_path = reconciliation_dir / "direct_agreements.jsonl"
    coordinator_packet_path = reconciliation_dir / "coordinator_packet.jsonl"
    coordinator_return_path = reconciliation_dir / "coordinator_return.jsonl"
    output_dir = reconciliation_dir / "final_dispositions"
    required = [direct_path, coordinator_packet_path, coordinator_return_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    direct_rows = read_jsonl(direct_path)
    coordinator_packets = read_jsonl(coordinator_packet_path)
    coordinator_returns = read_jsonl(coordinator_return_path)
    direct_by_token = {str(row["family_token"]): row for row in direct_rows}
    packet_by_token = {str(row["family_token"]): row for row in coordinator_packets}
    return_by_token = {str(row.get("family_token")): row for row in coordinator_returns}
    if len(direct_rows) != len(direct_by_token) or len(coordinator_packets) != len(packet_by_token):
        raise SystemExit("Duplicate direct-agreement or coordinator packet token")
    if len(coordinator_returns) != len(return_by_token) or set(return_by_token) != set(packet_by_token):
        raise SystemExit("Coordinator return does not exactly bind disagreement packet")
    if set(direct_by_token) & set(packet_by_token) or len(direct_by_token) + len(packet_by_token) != args.expected_families:
        raise SystemExit(f"Direct and adjudicated token partition does not reconstruct {args.expected_families} families")
    for token, row in return_by_token.items():
        if row.get("decision") not in VALID_DECISIONS:
            raise SystemExit(f"Invalid coordinator decision: {token}")
        if not isinstance(row.get("common_envelope_evidence"), list) or not isinstance(row.get("member_contrast_evidence"), dict):
            raise SystemExit(f"Coordinator evidence fields invalid: {token}")

    final_rows: list[dict[str, Any]] = []
    for token, row in direct_by_token.items():
        final_rows.append({
            "family_token": token,
            "final_decision": row["decision"],
            "decision_route": "DIRECT_A_B_AGREEMENT",
            "evidence_records": {"reviewer_a": row["reviewer_a_return"], "reviewer_b": row["reviewer_b_return"]},
            "downstream_state": "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE" if row["decision"] == "PASS_TO_PROMPT_AUTHORING" else "NOT_A_CLUSTER_OR_PROMPT",
            "claim_boundary": "Source-family disposition only; downstream provenance/prompt/adequacy/final-library gates remain required.",
        })
    for token, row in return_by_token.items():
        final_rows.append({
            "family_token": token,
            "final_decision": row["decision"],
            "decision_route": "INDEPENDENT_DISAGREEMENT_ADJUDICATION",
            "evidence_records": {"coordinator": row},
            "downstream_state": "ELIGIBLE_FOR_PROMPT_AUTHORING_GATE" if row["decision"] == "PASS_TO_PROMPT_AUTHORING" else "NOT_A_CLUSTER_OR_PROMPT",
            "claim_boundary": "Source-family disposition only; downstream provenance/prompt/adequacy/final-library gates remain required.",
        })
    final_rows.sort(key=lambda row: row["family_token"])
    output_dir.mkdir(parents=True)
    dispositions_path = output_dir / "reconciled_family_dispositions.jsonl"
    write_jsonl(dispositions_path, final_rows)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_RECONCILED_FAMILY_DISPOSITIONS_NO_CLUSTER_ADMISSION",
        "bound_inputs": {relative(direct_path): sha256_file(direct_path), relative(coordinator_packet_path): sha256_file(coordinator_packet_path), relative(coordinator_return_path): sha256_file(coordinator_return_path)},
        "counts": {"families": len(final_rows), "decisions": dict(sorted(Counter(row["final_decision"] for row in final_rows).items())), "eligible_for_prompt_authoring_gate": sum(row["final_decision"] == "PASS_TO_PROMPT_AUTHORING" for row in final_rows)},
        "outputs": {"reconciled_family_dispositions.jsonl": sha256_file(dispositions_path)},
        "claim_boundary": "Passing a source-family review does not admit a cluster/source/prompt. Each pass remains subject to provenance, prompt, target-blind adequacy, acceptable-set and final-freeze gates.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
