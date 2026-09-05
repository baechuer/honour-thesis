#!/usr/bin/env python3
"""Reconcile two validated independent V2 tail-review returns coordinator-side.

This joins opaque reviewer tokens only through the sealed map.  It decides
whether the predeclared whole-lane K=6 tail trigger is reached; it does not
make a final acceptable-set, strict-gold, selector, or metric claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
RETURN_ROOT = ROOT / "review/whole_library_pooled_tail_reviews_v1_2026-08-31"
SEALED_MAP = ROOT / "review/whole_library_pooled_tail_packets_v1_2026-08-31/coordinator_sealed/blinding_map.jsonl"
OUT_ROOT = RETURN_ROOT / "coordinator_reconciliation"
POSITIVE_TAIL_OUTCOMES = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE"}
POSITIVE_TRIGGER_STATE = "WHOLE_LANE_K6_RERUN_REQUIRED"
POSITIVE_TRIGGER_CLAIM = "A confirmed positive tail triggers the predeclared whole-lane K=6 discovery rerun."
POSITIVE_COUNT_FIELD = "confirmed_k6_triggers_by_lane"
RECONCILIATION_STATUS = "PASS_TAIL_PACKET_RECONCILIATION_K6_TRIGGER_CHECK_NOT_A_FINAL_LABEL_OR_METRIC"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True)
    args = parser.parse_args()
    returns = {
        stream: read_jsonl(RETURN_ROOT / f"reviewer_{stream}" / f"{args.packet}.jsonl")
        for stream in ("A", "B")
    }
    sealed = read_jsonl(SEALED_MAP)
    sealed_by_token = {row["opaque_case_token"]: row for row in sealed}
    canonical_returns: dict[str, dict[tuple[str, str, str, str], dict[str, Any]]] = {}
    for stream, rows in returns.items():
        mapped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        for row in rows:
            token = row["opaque_case_token"]
            sealed_row = sealed_by_token.get(token)
            if sealed_row is None or sealed_row["packet_id"] != args.packet or sealed_row["reviewer_stream"] != stream:
                raise SystemExit(f"missing_or_wrong_sealed_map:{stream}:{token}")
            key = (
                sealed_row["lane_id"], sealed_row["prompt_id"],
                sealed_row["canonical_source_sha256"], sealed_row["tail_class"],
            )
            if key in mapped:
                raise SystemExit(f"duplicate_canonical_return:{stream}:{key}")
            mapped[key] = {"response": row, "sealed": sealed_row}
        canonical_returns[stream] = mapped
    if set(canonical_returns["A"]) != set(canonical_returns["B"]) or len(canonical_returns["A"]) != 22:
        raise SystemExit("stream_canonical_pair_mismatch")

    reconciled: list[dict[str, Any]] = []
    lane_trigger_counts: Counter[str] = Counter()
    state_counts: Counter[str] = Counter()
    for key in sorted(canonical_returns["A"]):
        a = canonical_returns["A"][key]
        b = canonical_returns["B"][key]
        outcome_a = a["response"]["outcome"]
        outcome_b = b["response"]["outcome"]
        if outcome_a == outcome_b:
            state = "AGREED_OUTCOME"
            reconciled_outcome = outcome_a
        else:
            state = "THIRD_REVIEW_REQUIRED_OUTCOME_DISAGREEMENT"
            reconciled_outcome = "UNRESOLVED"
        if state == "AGREED_OUTCOME" and reconciled_outcome in POSITIVE_TAIL_OUTCOMES:
            trigger = POSITIVE_TRIGGER_STATE
            lane_trigger_counts[key[0]] += 1
        else:
            trigger = "NO_CONFIRMED_K6_TRIGGER_FROM_THIS_PAIR"
        state_counts[state] += 1
        reconciled.append({
            "packet_id": args.packet,
            "lane_id": key[0],
            "prompt_id": key[1],
            "canonical_source_sha256": key[2],
            "tail_class": key[3],
            "reviewer_A_outcome": outcome_a,
            "reviewer_B_outcome": outcome_b,
            "reconciliation_state": state,
            "reconciled_outcome": reconciled_outcome,
            "tail_trigger_state": trigger,
            "reviewer_A_return_sha256": sha256(RETURN_ROOT / "reviewer_A" / f"{args.packet}.jsonl"),
            "reviewer_B_return_sha256": sha256(RETURN_ROOT / "reviewer_B" / f"{args.packet}.jsonl"),
            "status": "COORDINATOR_TAIL_RECONCILIATION_NOT_A_FINAL_ACCEPTABLE_SET_OR_METRIC",
        })
    output = OUT_ROOT / f"{args.packet}.jsonl"
    write_jsonl(output, reconciled)
    summary = {
        "status": RECONCILIATION_STATUS,
        "packet_id": args.packet,
        "pair_count": len(reconciled),
        "reconciliation_states": dict(sorted(state_counts.items())),
        POSITIVE_COUNT_FIELD: dict(sorted(lane_trigger_counts.items())),
        "bound_inputs": {
            "reviewer_A_return": sha256(RETURN_ROOT / "reviewer_A" / f"{args.packet}.jsonl"),
            "reviewer_B_return": sha256(RETURN_ROOT / "reviewer_B" / f"{args.packet}.jsonl"),
            "sealed_blinding_map": sha256(SEALED_MAP),
        },
        "output": {str(output.relative_to(ROOT)): sha256(output)},
        "claim_boundary": [
            POSITIVE_TRIGGER_CLAIM,
            "This is pooled-tail reconciliation only, not an exhaustive relevance claim or final acceptable set.",
            "No selector output, retrieval result, metric, or final benchmark membership is produced.",
        ],
    }
    summary_path = OUT_ROOT / f"{args.packet}_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
