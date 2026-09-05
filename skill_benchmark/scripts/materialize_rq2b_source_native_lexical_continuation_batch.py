#!/usr/bin/env python3
"""Materialise a fresh-source B002 lexical-only continuation reading queue."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
BOOTSTRAP_DIR = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04"
HYPOTHESES = BOOTSTRAP_DIR / "all_mutual_triangle_hypotheses.jsonl"
B001_QUEUE = BOOTSTRAP_DIR / "batch_001_full_source_review_queue_internal.jsonl"
OUTPUT_DIR = NC_ROOT / "review/source_native_lexical_continuation_2026-09-04"

BATCH_FAMILIES = 25


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(WORKSPACE))


def main() -> int:
    required = [PROTOCOL, HYPOTHESES, B001_QUEUE]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")
    prior_rows = read_jsonl(B001_QUEUE)
    if len(prior_rows) != BATCH_FAMILIES:
        raise SystemExit("Expected exactly twenty-five B001 queue families")
    prior_sources = {str(source) for row in prior_rows for source in row["member_source_sha256"]}
    if len(prior_sources) != 75:
        raise SystemExit("B001 should bind exactly seventy-five distinct source hashes")
    hypotheses = read_jsonl(HYPOTHESES)
    hypotheses.sort(key=lambda row: (-row["reciprocal_link_count"], -row["rank_fusion_score"], row["member_source_sha256"]))
    queue: list[dict[str, Any]] = []
    used_sources: set[str] = set()
    excluded_due_to_b001 = 0
    excluded_due_to_b002_collision = 0
    for row in hypotheses:
        members = {str(source) for source in row["member_source_sha256"]}
        if members & prior_sources:
            excluded_due_to_b001 += 1
            continue
        if members & used_sources:
            excluded_due_to_b002_collision += 1
            continue
        queue.append({
            **row,
            "batch_id": "SN-LEX-B002",
            "batch_rank": len(queue) + 1,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "claim_boundary": "Fresh-source lexical reading priority only; full original sources must establish every semantic decision. Not dense semantic coverage or a cluster result.",
        })
        used_sources.update(members)
        if len(queue) == BATCH_FAMILIES:
            break
    if len(queue) != BATCH_FAMILIES or len(used_sources) != 75:
        raise SystemExit("Could not materialise a complete fresh-source B002 queue")
    OUTPUT_DIR.mkdir(parents=True)
    queue_path = OUTPUT_DIR / "batch_002_full_source_review_queue_internal.jsonl"
    write_jsonl(queue_path, queue)
    summary = {
        "status": "PASS_SOURCE_NATIVE_LEXICAL_ONLY_CONTINUATION_B002_UNREVIEWED_FAMILY_HYPOTHESES",
        "bound_inputs": {relative(path): sha256_file(path) for path in required},
        "parameters": {"batch_families": BATCH_FAMILIES, "fresh_source_policy": "exclude_all_75_B001_reviewed_source_hashes; disjoint_members_within_B002", "ranking_rule": "replay_B001_frozen_mutual_triangle_order"},
        "counts": {"b002_families": len(queue), "b002_sources": len(used_sources), "b001_excluded_source_hashes": len(prior_sources), "hypotheses_excluded_due_to_b001_source_overlap": excluded_due_to_b001, "hypotheses_excluded_due_to_b002_source_collision": excluded_due_to_b002_collision},
        "outputs": {"batch_002_full_source_review_queue_internal.jsonl": sha256_file(queue_path)},
        "dense_status": "NOT_EXECUTED_NO_PROVIDER_CREDENTIAL_IN_PROCESS_ENVIRONMENT_NO_PROVIDER_CONTACT",
        "claim_boundary": "B002 source-reading queue only; no full-source approval, prompt, admission, acceptable set, selector or metric has occurred.",
    }
    write_json(OUTPUT_DIR / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
