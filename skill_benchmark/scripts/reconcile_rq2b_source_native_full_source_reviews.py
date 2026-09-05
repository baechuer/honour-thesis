#!/usr/bin/env python3
"""Validate A/B full-source reviews and materialise disagreement-only packets."""

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


def validate_return(path: Path, expected_tokens: set[str]) -> dict[str, dict[str, Any]]:
    rows = read_jsonl(path)
    by_token = {str(row.get("family_token")): row for row in rows}
    if len(rows) != len(by_token) or set(by_token) != expected_tokens:
        raise SystemExit(f"Return does not contain exactly the expected family tokens: {path}")
    for token, row in by_token.items():
        if row.get("decision") not in VALID_DECISIONS:
            raise SystemExit(f"Invalid decision for {token}: {row.get('decision')}")
        if not isinstance(row.get("common_envelope_evidence"), list):
            raise SystemExit(f"Missing common-envelope evidence list for {token}")
        contrasts = row.get("member_contrast_evidence")
        if not isinstance(contrasts, dict) or set(contrasts) != {"S-1", "S-2", "S-3"}:
            raise SystemExit(f"Missing member contrast evidence for {token}")
        if not isinstance(row.get("rationale"), str):
            raise SystemExit(f"Missing rationale for {token}")
    return by_token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate independent full-source reviews and isolate disagreements.")
    parser.add_argument("--packet-dir", type=Path, default=PACKET_DIR)
    parser.add_argument("--expected-families", type=int, default=25)
    parser.add_argument("--batch-label", default="B001")
    parser.add_argument(
        "--bind-reviewer-b-by-ordered-source-hashes",
        action="store_true",
        help="Bind Reviewer B's opaque family tokens to Reviewer A packets only when each ordered three-source SHA-256 tuple is unique and identical.",
    )
    parser.add_argument("--seal-existing", action="store_true", help="Validate and seal a prior deterministic write that stopped before its summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_families < 1:
        raise SystemExit("--expected-families must be positive")
    packet_dir = args.packet_dir.resolve()
    a_return_path = packet_dir / "reviewer_a_return.jsonl"
    b_return_path = packet_dir / "reviewer_b_return.jsonl"
    a_packet_path = packet_dir / "reviewer_a_packet.jsonl"
    output_dir = packet_dir / "reconciliation"
    b_packet_path = packet_dir / "reviewer_b_packet.jsonl"
    required = [a_return_path, b_return_path, a_packet_path]
    if args.bind_reviewer_b_by_ordered_source_hashes:
        required.append(b_packet_path)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    seal_existing = False
    if output_dir.exists():
        expected_partial = [output_dir / "direct_agreements.jsonl", output_dir / "disagreement_index.jsonl", output_dir / "coordinator_packet.jsonl"]
        if not args.seal_existing or (output_dir / "summary.json").exists() or not all(path.is_file() for path in expected_partial):
            raise SystemExit(f"Output directory already exists: {output_dir}")
        seal_existing = True
    packets = read_jsonl(a_packet_path)
    packet_by_token = {str(row["family_token"]): row for row in packets}
    if len(packets) != len(packet_by_token) or len(packets) != args.expected_families:
        raise SystemExit(f"Reviewer packet must contain {args.expected_families} unique family tokens")
    reviewer_a = validate_return(a_return_path, set(packet_by_token))
    if args.bind_reviewer_b_by_ordered_source_hashes:
        b_packets = read_jsonl(b_packet_path)
        b_packet_by_token = {str(row["family_token"]): row for row in b_packets}
        if len(b_packets) != len(b_packet_by_token) or len(b_packets) != args.expected_families:
            raise SystemExit(f"Reviewer B packet must contain {args.expected_families} unique family tokens")
        reviewer_b_raw = validate_return(b_return_path, set(b_packet_by_token))

        def ordered_hashes(packet: dict[str, Any]) -> tuple[str, str, str]:
            members = packet.get("members")
            if not isinstance(members, list) or len(members) != 3:
                raise SystemExit(f"Expected exactly three members in source-binding packet: {packet.get('family_token')}")
            hashes = tuple(str(member.get("source_byte_sha256")) for member in members)
            if any(len(value) != 64 for value in hashes):
                raise SystemExit(f"Invalid source SHA-256 in source-binding packet: {packet.get('family_token')}")
            return hashes  # type: ignore[return-value]

        a_hashes = {ordered_hashes(packet): token for token, packet in packet_by_token.items()}
        b_hashes = {ordered_hashes(packet): token for token, packet in b_packet_by_token.items()}
        if len(a_hashes) != args.expected_families or len(b_hashes) != args.expected_families or set(a_hashes) != set(b_hashes):
            raise SystemExit("Reviewer A/B packets cannot be one-to-one bound by ordered three-source SHA-256 tuples")
        b_to_a = {b_hashes[hashes]: a_hashes[hashes] for hashes in a_hashes}
        reviewer_b = {}
        for b_token, row in reviewer_b_raw.items():
            a_token = b_to_a[b_token]
            bound_row = dict(row)
            bound_row["family_token"] = a_token
            bound_row["source_bound_from_reviewer_b_family_token"] = b_token
            reviewer_b[a_token] = bound_row
        if set(reviewer_b) != set(packet_by_token):
            raise SystemExit("Reviewer B source-hash binding did not reconstruct Reviewer A family-token coverage")
    else:
        reviewer_b = validate_return(b_return_path, set(packet_by_token))

    reconciled: list[dict[str, Any]] = []
    disagreements: list[dict[str, Any]] = []
    coordinator_packets: list[dict[str, Any]] = []
    for family_token in sorted(packet_by_token):
        a = reviewer_a[family_token]
        b = reviewer_b[family_token]
        if a["decision"] == b["decision"]:
            reconciled.append({
                "family_token": family_token,
                "reconciliation_state": "DIRECT_AGREEMENT_PENDING_DOWNSTREAM_GATES",
                "decision": a["decision"],
                "reviewer_a_return": a,
                "reviewer_b_return": b,
                "claim_boundary": "Agreement decides only source-family disposition; it is not a cluster/prompt/admission/result.",
            })
        else:
            disagreements.append({
                "family_token": family_token,
                "reviewer_a_decision": a["decision"],
                "reviewer_b_decision": b["decision"],
            })
            packet = packet_by_token[family_token]
            coordinator_packets.append({
                "record_type": "source_native_full_source_disagreement_adjudication",
                "family_token": family_token,
                "members": packet["members"],
                "rubric": packet["rubric"],
                "return_schema": packet.get("return_schema", {
                    "record_type": "source_native_full_source_family_review_return",
                    "family_token": "F-...",
                    "decision": "PASS_TO_PROMPT_AUTHORING | rejection/defer code",
                    "common_envelope_evidence": [],
                    "member_contrast_evidence": {"S-1": [], "S-2": [], "S-3": []},
                    "rationale": "",
                }),
                "instruction": "Independently determine the source-family decision from complete original sources. Do not attempt to compromise or infer ranks/origins; resolve only the A/B decision disagreement.",
            })
    if seal_existing:
        existing = {
            "direct_agreements.jsonl": read_jsonl(output_dir / "direct_agreements.jsonl"),
            "disagreement_index.jsonl": read_jsonl(output_dir / "disagreement_index.jsonl"),
            "coordinator_packet.jsonl": read_jsonl(output_dir / "coordinator_packet.jsonl"),
        }
        expected = {
            "direct_agreements.jsonl": reconciled,
            "disagreement_index.jsonl": disagreements,
            "coordinator_packet.jsonl": coordinator_packets,
        }
        if existing != expected:
            raise SystemExit("Existing partial reconciliation outputs do not exactly match deterministic recomputation")
    else:
        output_dir.mkdir(parents=True)
    reconciled_path = output_dir / "direct_agreements.jsonl"
    disagreement_path = output_dir / "disagreement_index.jsonl"
    coordinator_path = output_dir / "coordinator_packet.jsonl"
    if not seal_existing:
        write_jsonl(reconciled_path, reconciled)
        write_jsonl(disagreement_path, disagreements)
        write_jsonl(coordinator_path, coordinator_packets)
    summary = {
        "status": f"PASS_SOURCE_NATIVE_{args.batch_label}_A_B_RETURN_VALIDATION_AND_DISAGREEMENT_QUEUE",
        "bound_inputs": {relative(a_return_path): sha256_file(a_return_path), relative(b_return_path): sha256_file(b_return_path), relative(a_packet_path): sha256_file(a_packet_path), **({relative(b_packet_path): sha256_file(b_packet_path)} if args.bind_reviewer_b_by_ordered_source_hashes else {})},
        "counts": {"families": len(packet_by_token), "direct_agreements": len(reconciled), "disagreements": len(disagreements), "reviewer_a_decisions": dict(sorted(Counter(row["decision"] for row in reviewer_a.values()).items())), "reviewer_b_decisions": dict(sorted(Counter(row["decision"] for row in reviewer_b.values()).items()))},
        "outputs": {"direct_agreements.jsonl": sha256_file(reconciled_path), "disagreement_index.jsonl": sha256_file(disagreement_path), "coordinator_packet.jsonl": sha256_file(coordinator_path)},
        "claim_boundary": "Reconciliation queue only; no prompt authoring, cluster admission, source admission, acceptable set, selector or metric is created.",
    }
    if args.bind_reviewer_b_by_ordered_source_hashes:
        summary["reviewer_b_token_binding"] = {
            "method": "ORDERED_THREE_SOURCE_SHA256_TUPLE_EXACT_MATCH",
            "status": "PASS_25_OF_25",
            "raw_reviewer_b_tokens": sorted(b_to_a),
            "canonical_reviewer_a_tokens": sorted(b_to_a.values()),
            "claim_boundary": "This corrects only opaque packet identity using complete-source byte hashes. It does not alter any Reviewer B decision, evidence, or rationale.",
        }
    if seal_existing:
        summary["recovery_note"] = "Prior execution wrote deterministic reconciliation JSONL then stopped before its summary because a local relative-path helper was missing. This run recomputed and byte-content validated all three JSONL outputs before sealing the summary; no review decision was changed."
    write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
