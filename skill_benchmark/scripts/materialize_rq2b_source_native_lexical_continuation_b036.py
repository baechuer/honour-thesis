#!/usr/bin/env python3
"""Materialise the B036 fresh-source lexical continuation reading queue."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC_ROOT = WORKSPACE / "skill_benchmark/rq2b_naturalistic_confusability"
PROTOCOL = NC_ROOT / "review/SOURCE_NATIVE_CONFUSABLE_CLUSTER_DISCOVERY_PROTOCOL_2026-09-04.md"
BOOTSTRAP = NC_ROOT / "review/source_native_lexical_bootstrap_2026-09-04"
HYPOTHESES = BOOTSTRAP / "all_mutual_triangle_hypotheses.jsonl"
REVIEW_ROOT = NC_ROOT / "review"
OUTPUT_DIR = REVIEW_ROOT / "source_native_dense_lexical_union_b036_2026-09-04"
QUEUE_PATH = OUTPUT_DIR / "batch_036_full_source_review_queue_internal.jsonl"
EXPECTED_PREVIOUS_BATCHES = set(range(1, 36))
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


def previous_keys() -> dict[int, Path]:
    result: dict[int, Path] = {}
    pattern = re.compile(r"batch_(\d+)_full_source_review_packets/internal_reconciliation_key\.jsonl$")
    for path in REVIEW_ROOT.glob("**/internal_reconciliation_key.jsonl"):
        match = pattern.search(relative(path))
        if match is None:
            continue
        batch = int(match.group(1))
        if batch in EXPECTED_PREVIOUS_BATCHES:
            if batch in result:
                raise SystemExit(f"Duplicate reconciliation key for B{batch:03d}")
            result[batch] = path
    if set(result) != EXPECTED_PREVIOUS_BATCHES:
        missing = sorted(EXPECTED_PREVIOUS_BATCHES - set(result))
        raise SystemExit(f"Missing previous reconciliation key(s): {missing}")
    return result


def main() -> int:
    required = [PROTOCOL, HYPOTHESES]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")
    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")
    key_paths = previous_keys()
    prior_sources: set[str] = set()
    for batch, path in key_paths.items():
        rows = read_jsonl(path)
        if len(rows) != 75:
            raise SystemExit(f"B{batch:03d} does not bind exactly 75 source rows")
        prior_sources.update(str(row["canonical_source_sha256"]) for row in rows)
    if len(prior_sources) != len(EXPECTED_PREVIOUS_BATCHES) * 75:
        raise SystemExit("Prior B001-B035 source ledger is not source-disjoint")

    hypotheses = read_jsonl(HYPOTHESES)
    hypotheses.sort(key=lambda row: (-row["reciprocal_link_count"], -row["rank_fusion_score"], row["member_source_sha256"]))
    selected: list[dict[str, Any]] = []
    selected_sources: set[str] = set()
    excluded_prior = 0
    excluded_collision = 0
    for row in hypotheses:
        members = {str(value) for value in row["member_source_sha256"]}
        if members & prior_sources:
            excluded_prior += 1
            continue
        if members & selected_sources:
            excluded_collision += 1
            continue
        selected.append({
            **row,
            "batch_id": "SN-LEX-B036",
            "batch_rank": len(selected) + 1,
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "review_state": "UNREVIEWED_FULL_SOURCE",
            "claim_boundary": "Fresh-source lexical reading priority only; complete original sources remain authoritative for every later decision. Not dense semantic coverage or a cluster result.",
        })
        selected_sources.update(members)
        if len(selected) == BATCH_FAMILIES:
            break
    if len(selected) != BATCH_FAMILIES or len(selected_sources) != BATCH_FAMILIES * 3:
        raise SystemExit("Could not materialise 25 source-disjoint B036 hypotheses")
    if selected_sources & prior_sources:
        raise SystemExit("B036 selection reuses an earlier source hash")

    OUTPUT_DIR.mkdir(parents=True)
    write_jsonl(QUEUE_PATH, selected)
    summary = {
        "status": "PASS_SOURCE_NATIVE_LEXICAL_ONLY_CONTINUATION_B036_UNREVIEWED_FAMILY_HYPOTHESES",
        "bound_inputs": {
            relative(PROTOCOL): sha256_file(PROTOCOL),
            relative(HYPOTHESES): sha256_file(HYPOTHESES),
            "prior_reconciliation_keys": {f"B{batch:03d}": sha256_file(path) for batch, path in sorted(key_paths.items())},
        },
        "parameters": {
            "batch_families": BATCH_FAMILIES,
            "fresh_source_policy": "exclude_all_source_hashes_in_B001_to_B035; disjoint_members_within_B036",
            "ranking_rule": "frozen_reciprocal_link_count_then_rank_fusion_then_distinct_source_paths_then_sorted_member_hashes",
            "discovery_route": "LEXICAL_ONLY_CONTINUATION_EXACT_NATIVE_DESCRIPTION",
            "dense_status": "NOT_EXECUTED_NO_PROVIDER_CREDENTIAL_IN_PROCESS_ENVIRONMENT_NO_PROVIDER_CONTACT",
        },
        "counts": {
            "prior_batches": len(key_paths),
            "prior_source_hashes": len(prior_sources),
            "b036_families": len(selected),
            "b036_sources": len(selected_sources),
            "hypotheses_excluded_due_to_prior_source_overlap": excluded_prior,
            "hypotheses_excluded_due_to_b036_source_collision": excluded_collision,
        },
        "outputs": {QUEUE_PATH.name: sha256_file(QUEUE_PATH)},
        "claim_boundary": "B036 source-reading queue only; no full-source review, prompt, adequacy, admission, acceptable-set, selector, or metric result has occurred.",
    }
    write_json(OUTPUT_DIR / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
