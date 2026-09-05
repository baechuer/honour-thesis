#!/usr/bin/env python3
"""Validate independent PAF certificates and isolate result-code disagreements."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PACKET_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04/batch_001_full_source_review_packets/reconciliation/paf"
PAF_CODES = {
    "PAF_PASS", "PAF_PASS_DECLARED_TECHNICAL_CUE", "PAF_FAIL_REQUIRED_SOURCE_UNIQUE_CUE",
    "PAF_FAIL_NO_NONIDENTITY_CONTRAST", "PAF_FAIL_NO_NATURAL_TASK_FRAME",
    "PAF_DEFER_INSUFFICIENT_SOURCE_EVIDENCE",
}
CUE_RISKS = {
    "SOURCE_TITLE_OR_NAME", "REPOSITORY_OR_PROVIDER", "PATH_OR_URL",
    "FILE_OR_COMMAND_IDENTIFIER", "LITERAL_SOURCE_HEADING_OR_UNIQUE_PHRASE",
    "PROPRIETARY_ARTIFACT", "NONE_IDENTIFIED",
}
MEMBER_TOKENS = {"S-1", "S-2", "S-3"}


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


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_certificate(certificate: Any, family_token: str) -> dict[str, Any]:
    if not isinstance(certificate, dict) or set(certificate) != {
        "member_token", "neutral_task_frame", "functional_decision_boundary", "nonidentity_expression",
        "source_evidence_anchors", "cue_risk_inventory", "result_code",
    }:
        raise SystemExit(f"PAF certificate schema is not exact: {family_token}")
    if certificate["member_token"] not in MEMBER_TOKENS or certificate["result_code"] not in PAF_CODES:
        raise SystemExit(f"Invalid PAF member token or code: {family_token}")
    frame = certificate["neutral_task_frame"]
    if not isinstance(frame, dict) or set(frame) != {"goal", "input_or_state", "deliverable"} or not all(nonempty_string(frame[key]) for key in frame):
        raise SystemExit(f"Invalid neutral task frame: {family_token}/{certificate['member_token']}")
    if not nonempty_string(certificate["functional_decision_boundary"]) or not nonempty_string(certificate["nonidentity_expression"]):
        raise SystemExit(f"Missing PAF functional/nonidentity field: {family_token}/{certificate['member_token']}")
    anchors, risks = certificate["source_evidence_anchors"], certificate["cue_risk_inventory"]
    if not isinstance(anchors, list) or not anchors or not all(nonempty_string(value) for value in anchors):
        raise SystemExit(f"PAF source evidence anchors must be a nonempty string list: {family_token}/{certificate['member_token']}")
    if not isinstance(risks, list) or not risks or len(risks) != len(set(risks)) or not set(risks) <= CUE_RISKS:
        raise SystemExit(f"Invalid PAF cue-risk inventory: {family_token}/{certificate['member_token']}")
    return certificate


def validate_return(path: Path, expected_families: set[str]) -> dict[str, dict[str, dict[str, Any]]]:
    rows = read_jsonl(path)
    by_family = {str(row.get("family_token")): row for row in rows}
    if len(rows) != len(by_family) or set(by_family) != expected_families:
        raise SystemExit(f"PAF return does not contain exactly expected family tokens: {path}")
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for family_token, row in by_family.items():
        if set(row) != {"family_token", "member_certificates"} or not isinstance(row["member_certificates"], list):
            raise SystemExit(f"PAF return family schema is not exact: {path}/{family_token}")
        certificates = [validate_certificate(value, family_token) for value in row["member_certificates"]]
        member_map = {str(value["member_token"]): value for value in certificates}
        if len(certificates) != 3 or len(member_map) != 3 or set(member_map) != MEMBER_TOKENS:
            raise SystemExit(f"PAF return must contain exactly S-1/S-2/S-3 once: {path}/{family_token}")
        result[family_token] = member_map
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate A/B PAF feasibility certificates and queue only result-code disagreements.")
    parser.add_argument("--packet-dir", type=Path, default=PACKET_DIR)
    parser.add_argument("--expected-families", type=int, default=4)
    parser.add_argument("--batch-label", default="B001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    packet_dir = args.packet_dir.resolve()
    a_packet_path, b_packet_path = packet_dir / "reviewer_a_packet.jsonl", packet_dir / "reviewer_b_packet.jsonl"
    a_return_path, b_return_path = packet_dir / "reviewer_a_return.jsonl", packet_dir / "reviewer_b_return.jsonl"
    required = [a_packet_path, b_packet_path, a_return_path, b_return_path]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    output_dir = packet_dir / "reconciliation"
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    a_packets = read_jsonl(a_packet_path)
    b_packets = read_jsonl(b_packet_path)
    a_by_family = {str(row.get("family_token")): row for row in a_packets}
    b_by_family = {str(row.get("family_token")): row for row in b_packets}
    if len(a_packets) != len(a_by_family) or len(b_packets) != len(b_by_family) or len(a_by_family) != args.expected_families or set(a_by_family) != set(b_by_family):
        raise SystemExit("PAF A/B packets must exactly bind the expected opaque family-token set")
    for token in a_by_family:
        if a_by_family[token] != b_by_family[token] or not isinstance(a_by_family[token].get("members"), list) or {member.get("member_token") for member in a_by_family[token]["members"]} != MEMBER_TOKENS:
            raise SystemExit(f"PAF A/B packet identity/cardinality failure: {token}")
    reviewer_a = validate_return(a_return_path, set(a_by_family))
    reviewer_b = validate_return(b_return_path, set(a_by_family))

    direct, disagreement_index, coordinator_packets = [], [], []
    for family_token in sorted(a_by_family):
        disagreements = [member for member in sorted(MEMBER_TOKENS) if reviewer_a[family_token][member]["result_code"] != reviewer_b[family_token][member]["result_code"]]
        if not disagreements:
            direct.append({
                "family_token": family_token, "reconciliation_state": "DIRECT_A_B_RESULT_CODE_AGREEMENT",
                "reviewer_a_certificates": [reviewer_a[family_token][member] for member in sorted(MEMBER_TOKENS)],
                "reviewer_b_certificates": [reviewer_b[family_token][member] for member in sorted(MEMBER_TOKENS)],
                "claim_boundary": "A/B result-code agreement only; differing certificate prose is retained, not reconciled into a prompt or cue-safety claim.",
            })
        else:
            disagreement_index.append({"family_token": family_token, "member_tokens_with_result_code_disagreement": disagreements,
                                       "reviewer_a_result_codes": {member: reviewer_a[family_token][member]["result_code"] for member in disagreements},
                                       "reviewer_b_result_codes": {member: reviewer_b[family_token][member]["result_code"] for member in disagreements}})
            coordinator_packets.append({
                "record_type": "source_native_paf_sealed_result_code_adjudication", "family_token": family_token,
                "members": a_by_family[family_token]["members"],
                "instruction": "This sealed packet exists only because A/B result codes disagree for at least one member. Independently return one complete PAF feasibility certificate per opaque member from the complete original sources. Do not receive, infer, average, or discuss A/B outputs; do not write prompts.",
                "return_schema": a_by_family[family_token]["return_schema"],
            })
    output_dir.mkdir(parents=True)
    write_jsonl(output_dir / "direct_agreements.jsonl", direct)
    write_jsonl(output_dir / "disagreement_index.jsonl", disagreement_index)
    write_jsonl(output_dir / "coordinator_packet.jsonl", coordinator_packets)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_PAF_A_B_VALIDATION_AND_SEALED_RESULT_CODE_QUEUE",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "counts": {"families": len(a_by_family), "direct_agreements": len(direct), "disagreements": len(disagreement_index), "disagreed_members": sum(len(row["member_tokens_with_result_code_disagreement"]) for row in disagreement_index), "reviewer_a_codes": dict(sorted(Counter(c["result_code"] for rows in reviewer_a.values() for c in rows.values()).items())), "reviewer_b_codes": dict(sorted(Counter(c["result_code"] for rows in reviewer_b.values() for c in rows.values()).items()))},
        "outputs": {name: sha256_file(output_dir / name) for name in ["direct_agreements.jsonl", "disagreement_index.jsonl", "coordinator_packet.jsonl"]},
        "claim_boundary": "Only result-code disagreements enter sealed coordinator adjudication. No PAF result creates an actual prompt, source/cluster admission, acceptable-set, selector, metric, or cue-safety claim.",
    }
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
