#!/usr/bin/env python3
"""Fail-closed K selection after complete E23 A/B reconciliation.

This accepts no ranking or reviewer work.  It only combines pre-existing
reconciled source-visible outcomes with the pre-registered K membership map.
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
REVIEW_DIR = NC_ROOT / "review/background_corpus_k_calibration_reviews_2026-09-03"
PREFLIGHT_DIR = REVIEW_DIR / "coordinator_preflight"
AGREEMENTS = PREFLIGHT_DIR / "agreed_reconciliations.jsonl"
DISAGREEMENTS = PREFLIGHT_DIR / "disagreement_adjudication_queue.jsonl"
COORDINATOR_RETURNS = REVIEW_DIR / "coordinator_adjudication_return.jsonl"
OUTPUT_DIR = REVIEW_DIR / "k_selection"
RECONCILED_OUT = OUTPUT_DIR / "reconciled_calibration_outcomes.jsonl"
DECISION_OUT = OUTPUT_DIR / "k_selection_decision.json"
K_VALUES = (8, 12, 16)
EXPECTED_PAIRS = 3798
OUTCOMES = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "NOT_ADEQUATE", "UNCLEAR"}
POSITIVE = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE"}


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


def main() -> int:
    required = [PAIR_REGISTER, AGREEMENTS, DISAGREEMENTS, COORDINATOR_RETURNS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"K_SELECTION_HOLD: missing reconciliation input(s): {missing}")
    pairs = read_jsonl(PAIR_REGISTER)
    agreements = read_jsonl(AGREEMENTS)
    disagreements = read_jsonl(DISAGREEMENTS)
    coordinator = read_jsonl(COORDINATOR_RETURNS)
    pair_by_id = {str(row["calibration_pair_id"]): row for row in pairs}
    agreement_by_id = {str(row["calibration_pair_id"]): row for row in agreements}
    disagreement_by_id = {str(row["calibration_pair_id"]): row for row in disagreements}
    coordinator_by_id = {str(row.get("calibration_pair_id")): row for row in coordinator}
    if len(pairs) != len(pair_by_id) != EXPECTED_PAIRS:
        raise SystemExit("K_SELECTION_HOLD: calibration register cardinality failure")
    if set(agreement_by_id) & set(disagreement_by_id):
        raise SystemExit("K_SELECTION_HOLD: a pair appears in both agreement and disagreement ledgers")
    if set(agreement_by_id) | set(disagreement_by_id) != set(pair_by_id):
        raise SystemExit("K_SELECTION_HOLD: A/B preflight did not cover the calibration register")
    if len(coordinator) != len(coordinator_by_id) or set(coordinator_by_id) != set(disagreement_by_id):
        raise SystemExit("K_SELECTION_HOLD: coordinator return does not cover exactly every disagreement")
    reconciled: list[dict[str, Any]] = []
    for pair_id, pair in sorted(pair_by_id.items()):
        if pair_id in agreement_by_id:
            row = agreement_by_id[pair_id]
            outcome = row["reconciled_outcome"]
            state = "AGREED_OUTCOME"
            coordinator_evidence = None
        else:
            coordinator_row = coordinator_by_id[pair_id]
            outcome = coordinator_row.get("coordinator_outcome")
            state = "COORDINATOR_ADJUDICATED_DISAGREEMENT"
            coordinator_evidence = {
                "supporting_anchor_positions": coordinator_row.get("supporting_anchor_positions"),
                "limitation_anchor_positions": coordinator_row.get("limitation_anchor_positions"),
                "source_visible_reason": coordinator_row.get("source_visible_reason"),
            }
            if coordinator_row.get("status") != "COORDINATOR_SOURCE_VISIBLE_E23_K_CALIBRATION_ADJUDICATION":
                raise SystemExit(f"K_SELECTION_HOLD: invalid coordinator status at {pair_id}")
        if outcome not in OUTCOMES:
            raise SystemExit(f"K_SELECTION_HOLD: invalid reconciled outcome at {pair_id}: {outcome}")
        reconciled.append({
            "calibration_pair_id": pair_id,
            "lane_id": pair["lane_id"],
            "prompt_id": pair["prompt_id"],
            "canonical_source_sha256": pair["canonical_source_sha256"],
            "selected_at_k": pair["selected_at_k"],
            "tail": pair["tail"],
            "reconciled_outcome": outcome,
            "reconciliation_state": state,
            "coordinator_evidence": coordinator_evidence,
            "status": "RECONCILED_E23_CALIBRATION_OUTCOME_NOT_A_FINAL_ACCEPTABLE_SET_OR_METRIC",
        })
    if len(reconciled) != EXPECTED_PAIRS:
        raise SystemExit("K_SELECTION_HOLD: final reconciliation count mismatch")

    k_evidence: dict[str, Any] = {}
    passing: list[int] = []
    for k in K_VALUES:
        outside = [row for row in reconciled if not row["selected_at_k"][str(k)]]
        post_k_positive = [row for row in outside if row["reconciled_outcome"] in POSITIVE]
        post_k_unclear = [row for row in outside if row["reconciled_outcome"] == "UNCLEAR"]
        positive_by_lane = Counter(row["lane_id"] for row in post_k_positive)
        unclear_by_lane = Counter(row["lane_id"] for row in post_k_unclear)
        # An unresolved source cannot support a zero-positive coverage statement.
        passes = not post_k_positive and not post_k_unclear
        if passes:
            passing.append(k)
        k_evidence[str(k)] = {
            "outside_k_pair_count": len(outside),
            "post_k_positive_count": len(post_k_positive),
            "post_k_positive_by_lane": dict(sorted(positive_by_lane.items())),
            "post_k_unclear_count": len(post_k_unclear),
            "post_k_unclear_by_lane": dict(sorted(unclear_by_lane.items())),
            "post_k_positive_pair_ids": [row["calibration_pair_id"] for row in post_k_positive],
            "post_k_unclear_pair_ids": [row["calibration_pair_id"] for row in post_k_unclear],
            "passes_predeclared_zero_post_k_gate": passes,
        }
    selected_k = min(passing) if passing else None
    decision = {
        "status": "K_SELECTION_PASS_BOUNDED_CALIBRATION_NOT_A_FINAL_COVERAGE_OR_CLUSTER_RESULT" if selected_k else "K_SELECTION_HOLD",
        "selected_k": selected_k,
        "candidate_grid": list(K_VALUES),
        "selection_rule": "Smallest K with zero reconciled post-K positives and no unresolved outside-K pair in both lanes.",
        "counts": {
            "reconciled_pairs": len(reconciled),
            "agreed_pairs": len(agreements),
            "coordinator_adjudicated_pairs": len(coordinator),
            "reconciled_outcomes": dict(sorted(Counter(row["reconciled_outcome"] for row in reconciled).items())),
        },
        "k_evidence": k_evidence,
        "bound_inputs": {str(path.relative_to(BENCHMARK_ROOT)): sha256_file(path) for path in required},
        "claim_boundary": [
            "A selected K is a bounded 72-prompt calibration decision, not proof that no unreviewed source is adequate.",
            "No held-out coverage result, final acceptable set, cluster admission, representation, selector output, or metric is created here.",
            "If K_SELECTION_HOLD, no automatic increase above K=16 is permitted.",
        ],
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(RECONCILED_OUT, reconciled)
    DECISION_OUT.write_text(json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
