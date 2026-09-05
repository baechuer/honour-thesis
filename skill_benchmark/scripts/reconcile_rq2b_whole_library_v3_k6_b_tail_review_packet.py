#!/usr/bin/env python3
"""Coordinator-side reconciliation for V3 K6-B tail-review packet returns."""

from __future__ import annotations

from pathlib import Path

import reconcile_rq2b_whole_library_v2_tail_review_packet as base


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
base.RETURN_ROOT = ROOT / "review/whole_library_pooled_tail_reviews_v3_k6_b_2026-08-31"
base.SEALED_MAP = ROOT / "review/whole_library_pooled_tail_packets_v3_k6_b_2026-08-31/coordinator_sealed/blinding_map.jsonl"
base.OUT_ROOT = base.RETURN_ROOT / "coordinator_reconciliation"


if __name__ == "__main__":
    base.main()
