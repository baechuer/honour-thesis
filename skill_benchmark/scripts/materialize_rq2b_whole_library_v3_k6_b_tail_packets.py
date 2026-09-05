#!/usr/bin/env python3
"""Materialise fresh identity-blinded tail packets from the V3 K6-B queue."""

from __future__ import annotations

from pathlib import Path

import materialize_rq2b_whole_library_v2_tail_packets as base


BASE = Path(__file__).resolve().parents[2]
NC_ROOT = BASE / "skill_benchmark/rq2b_naturalistic_confusability"
base.QUEUE_DIR = NC_ROOT / "manifests/whole_library_pooled_discovery_queue_v3_k6_b_2026-08-31"
base.QUEUE_PAIRS = base.QUEUE_DIR / "source_visible_review_pairs.jsonl"
base.PROMPT_QUEUES = base.QUEUE_DIR / "prompt_discovery_queues.jsonl"
base.OUT = NC_ROOT / "review/whole_library_pooled_tail_packets_v3_k6_b_2026-08-31"
base.SEALED = base.OUT / "coordinator_sealed"
base.KEY_FILE = base.SEALED / "blinding_key.json"
base.MAP_OUT = base.SEALED / "blinding_map.jsonl"
base.ALLOCATION_OUT = base.SEALED / "allocation_ledger.jsonl"
base.SUMMARY_OUT = base.OUT / "summary.json"
base.TAIL_PACKET_QUEUE_VERSION = "V3_K6_B"
base.PACKET_ID_PREFIX = "RQ2B-TAIL-V3-K6B"


if __name__ == "__main__":
    base.main()
