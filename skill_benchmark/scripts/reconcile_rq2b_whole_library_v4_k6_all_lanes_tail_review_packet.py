#!/usr/bin/env python3
"""Coordinator reconciliation for the final predeclared V4 tail-review queue."""

from __future__ import annotations

from pathlib import Path

import reconcile_rq2b_whole_library_v2_tail_review_packet as base


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
base.RETURN_ROOT = ROOT / "review/whole_library_pooled_tail_reviews_v4_k6_all_lanes_2026-08-31"
base.SEALED_MAP = ROOT / "review/whole_library_pooled_tail_packets_v4_k6_all_lanes_2026-08-31/coordinator_sealed/blinding_map.jsonl"
base.OUT_ROOT = base.RETURN_ROOT / "coordinator_reconciliation"
base.POSITIVE_TRIGGER_STATE = "POST_K6_METHOD_DECISION_REQUIRED_NO_AUTOMATIC_RERUN"
base.POSITIVE_TRIGGER_CLAIM = "A confirmed positive V4 tail is recorded for a new method decision; the protocol does not authorise automatic K=8 expansion."
base.POSITIVE_COUNT_FIELD = "confirmed_post_k6_method_decision_cases_by_lane"
base.RECONCILIATION_STATUS = "PASS_POST_K6_TAIL_PACKET_RECONCILIATION_METHOD_DECISION_REQUIRED_NOT_A_FINAL_LABEL_OR_METRIC"


if __name__ == "__main__":
    base.main()
