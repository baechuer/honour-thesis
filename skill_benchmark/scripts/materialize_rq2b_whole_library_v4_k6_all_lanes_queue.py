#!/usr/bin/env python3
"""Materialise V4 discovery queues with the frozen all-lane K=6 override."""

from __future__ import annotations

from pathlib import Path

import materialize_rq2b_whole_library_pooled_discovery_queue as base


ROOT = Path(__file__).resolve().parents[2]
NC_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
base.K6_OVERRIDE = NC_ROOT / "review/WHOLE_LIBRARY_POOLED_DISCOVERY_V4_K6_ALL_LANES_OVERRIDE_2026-08-31.json"
base.OUTPUT_DIR = NC_ROOT / "manifests/whole_library_pooled_discovery_queue_v4_k6_all_lanes_2026-08-31"
base.QUEUE_OUT = base.OUTPUT_DIR / "prompt_discovery_queues.jsonl"
base.PAIR_OUT = base.OUTPUT_DIR / "source_visible_review_pairs.jsonl"
base.ANCHOR_GATE_OUT = base.OUTPUT_DIR / "anchor_gate_accounting.jsonl"
base.TERM_STATS_OUT = base.OUTPUT_DIR / "lane_term_statistics.json"
base.SUMMARY_OUT = base.OUTPUT_DIR / "summary.json"


if __name__ == "__main__":
    base.main()
