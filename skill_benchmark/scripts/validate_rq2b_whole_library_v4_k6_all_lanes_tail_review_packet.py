#!/usr/bin/env python3
"""Validate an independent V4 all-lane-K6 tail-review packet return."""

from __future__ import annotations

from pathlib import Path

import validate_rq2b_whole_library_v2_tail_review_packet as base


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
base.PACKET_ROOT = ROOT / "review/whole_library_pooled_tail_packets_v4_k6_all_lanes_2026-08-31"
base.RETURN_ROOT = ROOT / "review/whole_library_pooled_tail_reviews_v4_k6_all_lanes_2026-08-31"


if __name__ == "__main__":
    base.main()
