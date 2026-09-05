#!/usr/bin/env python3
"""Validate independent E23 returns and prepare disagreement-only adjudication.

This script is fail-closed.  It never resolves an A/B disagreement, chooses K,
or makes a cluster/selector/metric claim.  A coordinator must supply a fresh
source-visible adjudication for every disagreement before final K selection.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK_ROOT = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK_ROOT / "rq2b_naturalistic_confusability"
CALIBRATION_DIR = NC_ROOT / "manifests/background_corpus_k_calibration_2026-09-03"
PAIR_REGISTER = CALIBRATION_DIR / "calibration_pair_register_internal.jsonl"
PACKET_A = CALIBRATION_DIR / "reviewer_a_packet.jsonl"
PACKET_B = CALIBRATION_DIR / "reviewer_b_packet.jsonl"
REVIEW_DIR = NC_ROOT / "review/background_corpus_k_calibration_reviews_2026-09-03"
RETURN_A = REVIEW_DIR / "reviewer_A_return.jsonl"
RETURN_B = REVIEW_DIR / "reviewer_B_return.jsonl"
OUTPUT_DIR = REVIEW_DIR / "coordinator_preflight"
AGREEMENTS_OUT = OUTPUT_DIR / "agreed_reconciliations.jsonl"
DISAGREEMENTS_OUT = OUTPUT_DIR / "disagreement_adjudication_queue.jsonl"
SUMMARY_OUT = OUTPUT_DIR / "summary.json"
OUTCOMES = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "NOT_ADEQUATE", "UNCLEAR"}
EXPECTED_PAIRS = 3798


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_return(
    rows: list[dict[str, Any]], *, reviewer: str, expected_item_ids: set[str]
) -> dict[str, dict[str, Any]]:
    by_id = {str(row.get("review_item_id")): row for row in rows}
    if len(rows) != len(by_id) or set(by_id) != expected_item_ids:
        missing = len(expected_item_ids - set(by_id))
        unexpected = len(set(by_id) - expected_item_ids)
        raise SystemExit(
            f"Reviewer {reviewer} return coverage failed: rows={len(rows)}, unique={len(by_id)}, "
            f"missing={missing}, unexpected={unexpected}"
        )
    for item_id, row in by_id.items():
        if row.get("reviewer_blind_id") != reviewer:
            raise SystemExit(f"Reviewer {reviewer} id mismatch at {item_id}")
        if row.get("outcome") not in OUTCOMES:
            raise SystemExit(f"Reviewer {reviewer} invalid outcome at {item_id}: {row.get('outcome')}")
        if not isinstance(row.get("supporting_anchor_positions"), list):
            raise SystemExit(f"Reviewer {reviewer} missing supporting anchors at {item_id}")
        if not isinstance(row.get("limitation_anchor_positions"), list):
            raise SystemExit(f"Reviewer {reviewer} missing limitation anchors at {item_id}")
        if not isinstance(row.get("prompt_requirement_map"), list) or not row["prompt_requirement_map"]:
            raise SystemExit(f"Reviewer {reviewer} missing requirement map at {item_id}")
        if not isinstance(row.get("short_rationale"), str) or not row["short_rationale"].strip():
            raise SystemExit(f"Reviewer {reviewer} missing rationale at {item_id}")
    return by_id


def main() -> int:
    required = [PAIR_REGISTER, PACKET_A, PACKET_B, RETURN_A, RETURN_B]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Cannot reconcile before complete independent returns: {missing}")
    pairs = read_jsonl(PAIR_REGISTER)
    packet_a = read_jsonl(PACKET_A)
    packet_b = read_jsonl(PACKET_B)
    if len(pairs) != EXPECTED_PAIRS or len(packet_a) != EXPECTED_PAIRS or len(packet_b) != EXPECTED_PAIRS:
        raise SystemExit("E23 calibration cardinality is not the fixed 3,798-pair packet")
    pair_by_id = {str(row["calibration_pair_id"]): row for row in pairs}
    if len(pair_by_id) != EXPECTED_PAIRS:
        raise SystemExit("Duplicate internal calibration pair IDs")
    expected_a = {str(row["reviewer_item_ids"]["A"]) for row in pairs}
    expected_b = {str(row["reviewer_item_ids"]["B"]) for row in pairs}
    if {str(row["review_item_id"]) for row in packet_a} != expected_a:
        raise SystemExit("Reviewer A packet does not bind to the internal register")
    if {str(row["review_item_id"]) for row in packet_b} != expected_b:
        raise SystemExit("Reviewer B packet does not bind to the internal register")
    return_a = validate_return(read_jsonl(RETURN_A), reviewer="A", expected_item_ids=expected_a)
    return_b = validate_return(read_jsonl(RETURN_B), reviewer="B", expected_item_ids=expected_b)

    agreements: list[dict[str, Any]] = []
    disagreements: list[dict[str, Any]] = []
    for pair_id, pair in sorted(pair_by_id.items()):
        a = return_a[str(pair["reviewer_item_ids"]["A"])]
        b = return_b[str(pair["reviewer_item_ids"]["B"])]
        common = {
            "calibration_pair_id": pair_id,
            "lane_id": pair["lane_id"],
            "prompt_id": pair["prompt_id"],
            "prompt_sha256": pair["prompt_sha256"],
            "canonical_source_sha256": pair["canonical_source_sha256"],
            "source_paths": pair["source_paths"],
            "tail": pair["tail"],
            "local_roster_forced": pair["local_roster_forced"],
            "selected_at_k": pair["selected_at_k"],
            "reviewer_A_outcome": a["outcome"],
            "reviewer_B_outcome": b["outcome"],
            "reviewer_A_return_sha256": sha256_file(RETURN_A),
            "reviewer_B_return_sha256": sha256_file(RETURN_B),
        }
        if a["outcome"] == b["outcome"]:
            agreements.append({
                **common,
                "reconciled_outcome": a["outcome"],
                "reconciliation_state": "AGREED_OUTCOME",
                "status": "COORDINATOR_PREFLIGHT_AGREEMENT_NOT_A_K_DECISION_OR_FINAL_LABEL",
            })
        else:
            disagreements.append({
                **common,
                "prompt": next(
                    row["prompt"] for row in packet_a
                    if row["review_item_id"] == pair["reviewer_item_ids"]["A"]
                ),
                "reviewer_A_evidence": {
                    "supporting_anchor_positions": a["supporting_anchor_positions"],
                    "limitation_anchor_positions": a["limitation_anchor_positions"],
                    "prompt_requirement_map": a["prompt_requirement_map"],
                    "short_rationale": a["short_rationale"],
                },
                "reviewer_B_evidence": {
                    "supporting_anchor_positions": b["supporting_anchor_positions"],
                    "limitation_anchor_positions": b["limitation_anchor_positions"],
                    "prompt_requirement_map": b["prompt_requirement_map"],
                    "short_rationale": b["short_rationale"],
                },
                "coordinator_required_fields": [
                    "coordinator_outcome", "source_visible_reason", "supporting_anchor_positions",
                    "limitation_anchor_positions", "status",
                ],
                "status": "PENDING_FRESH_SOURCE_VISIBLE_COORDINATOR_ADJUDICATION",
            })
    if len(agreements) + len(disagreements) != EXPECTED_PAIRS:
        raise SystemExit("A/B preflight did not preserve every pair")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(AGREEMENTS_OUT, agreements)
    write_jsonl(DISAGREEMENTS_OUT, disagreements)
    summary = {
        "status": "PASS_E23_A_B_RETURN_VALIDATION_PENDING_DISAGREEMENT_ADJUDICATION",
        "bound_inputs": {str(path.relative_to(BENCHMARK_ROOT)): sha256_file(path) for path in required},
        "counts": {
            "calibration_pairs": EXPECTED_PAIRS,
            "agreed_pairs": len(agreements),
            "disagreement_pairs_requiring_coordinator": len(disagreements),
            "reviewer_A_outcomes": dict(sorted(Counter(row["outcome"] for row in return_a.values()).items())),
            "reviewer_B_outcomes": dict(sorted(Counter(row["outcome"] for row in return_b.values()).items())),
        },
        "outputs": {path.name: sha256_file(path) for path in [AGREEMENTS_OUT, DISAGREEMENTS_OUT]},
        "claim_boundary": [
            "Agreement is a reconciled pair outcome only; it does not select K or form an acceptable set.",
            "Every disagreement remains unresolved until fresh coordinator source-visible adjudication is recorded.",
            "This script has no rank-, cluster-, selector-, or metric-producing path.",
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
