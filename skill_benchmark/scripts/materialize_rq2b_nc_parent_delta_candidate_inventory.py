#!/usr/bin/env python3
"""Materialise the replaceable pre-freeze candidate delta against parent V3."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


BENCHMARK_ROOT = Path(__file__).resolve().parents[1]
PARENT = BENCHMARK_ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
UNION = BENCHMARK_ROOT / "rq2b_naturalistic_confusability/manifests/current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
OUTPUT_DIR = BENCHMARK_ROOT / "rq2b_naturalistic_confusability/manifests/parent_v3_delta_candidate_inventory_current_pre_freeze_2026-08-31"
OUTPUT_JSONL = OUTPUT_DIR / "new_to_parent_v3_candidates.jsonl"
OUTPUT_SUMMARY = OUTPUT_DIR / "summary.json"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> None:
    parent_rows = read_jsonl(PARENT)
    union_rows = read_jsonl(UNION)
    parent_hashes = {row["source_sha256"] for row in parent_rows}
    union_hashes = [row["canonical_source_sha256"] for row in union_rows]

    assert len(parent_rows) == 2433, len(parent_rows)
    assert len(parent_hashes) == 2431, len(parent_hashes)
    assert len(union_rows) == 3094, len(union_rows)
    assert len(union_hashes) == len(set(union_hashes)), "union source hashes are not unique"
    assert parent_hashes <= set(union_hashes), "parent source set is not contained in current union"

    delta_rows = []
    for row in union_rows:
        source_hash = row["canonical_source_sha256"]
        if source_hash in parent_hashes:
            continue
        augmented = dict(row)
        augmented["audit_lane"] = "PARENT_V3_DELTA_ACCEPTABLE_SET_CANDIDATE"
        augmented["delta_against_parent_v3"] = True
        augmented["status_boundary"] = (
            "CURRENT_PREFREEZE_INVENTORY_ONLY_NOT_A_REVIEW_SHORTLIST_LABEL_GOLD_OR_FINAL_UNION"
        )
        delta_rows.append(augmented)

    delta_rows.sort(key=lambda row: row["canonical_source_sha256"])
    assert len(delta_rows) == 663, len(delta_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_JSONL, delta_rows)

    role_counts = Counter(row.get("final_intake_role", "MISSING") for row in delta_rows)
    summary = {
        "status": "PASS_CURRENT_PREFREEZE_PARENT_V3_DELTA_INVENTORY_NOT_FINAL_AUDIT_QUEUE",
        "bound_inputs": {
            str(PARENT.relative_to(BENCHMARK_ROOT)): sha256(PARENT),
            str(UNION.relative_to(BENCHMARK_ROOT)): sha256(UNION),
        },
        "counts": {
            "parent_identity_rows": len(parent_rows),
            "parent_unique_source_hashes": len(parent_hashes),
            "current_union_unique_source_hashes": len(union_rows),
            "current_new_to_parent_v3_source_hashes": len(delta_rows),
            "current_parent_source_hashes_in_union": len(parent_hashes),
        },
        "delta_final_intake_role_counts": dict(sorted(role_counts.items())),
        "output": {
            "path": str(OUTPUT_JSONL.relative_to(BENCHMARK_ROOT)),
            "sha256": sha256(OUTPUT_JSONL),
        },
        "claim_boundary": [
            "This is the full current candidate difference, not 381 x 663 manual-review pairs.",
            "A frozen outcome-blind discovery procedure must shortlist plausible alternatives for each parent prompt after the final union closes.",
            "No candidate in this inventory is thereby acceptable for any prompt.",
            "Any later candidate admission invalidates and replaces this pre-freeze inventory.",
        ],
    }
    OUTPUT_SUMMARY.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
