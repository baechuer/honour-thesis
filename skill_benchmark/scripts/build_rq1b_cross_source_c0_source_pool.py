#!/usr/bin/env python3
"""Build the source-agnostic, zero-network C0 pool for the RQ1b main benchmark.

Inputs are post-hold Wave 003 navigation inventories. The script verifies each
referenced original's SHA-256, deduplicates exact bytes, and emits source-only
metadata for later cross-source cluster triage. It does not assess semantic
similarity, create clusters/prompts/labels, or invoke a model/retriever.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EXPECTED_STATUS = "M2A_UNREVIEWED_SOURCE_NAVIGATION_ONLY"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-inventory", type=Path, action="append", required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = [path.resolve() for path in args.input_inventory]
    if len(inputs) != len(set(inputs)):
        raise SystemExit("Duplicate input inventory")

    failures: list[str] = []
    raw_rows: list[dict[str, Any]] = []
    for inventory in inputs:
        if not inventory.is_file():
            failures.append(f"missing_inventory:{inventory}")
            continue
        for row in read_jsonl(inventory):
            if row.get("m2_navigation_status") != EXPECTED_STATUS:
                failures.append(f"unexpected_navigation_status:{inventory.name}:{row.get('skill_id')}")
                continue
            required = ("skill_id", "origin", "pinned_commit", "source_repository_path", "source_sha256", "local_original_path")
            missing = [key for key in required if not row.get(key)]
            if missing:
                failures.append(f"missing_required_metadata:{inventory.name}:{row.get('skill_id')}:{','.join(missing)}")
                continue
            local_path = Path(str(row["local_original_path"]))
            if not local_path.is_absolute():
                local_path = (Path.cwd() / local_path).resolve()
            if not local_path.is_file():
                failures.append(f"missing_original:{row['skill_id']}")
                continue
            if sha256(local_path) != str(row["source_sha256"]):
                failures.append(f"source_hash_drift:{row['skill_id']}")
                continue
            raw_rows.append(
                {
                    **row,
                    "local_original_path": str(local_path),
                    "_source_inventory": str(inventory),
                }
            )

    by_skill: dict[str, dict[str, Any]] = {}
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in raw_rows:
        skill_id = str(row["skill_id"])
        prior = by_skill.get(skill_id)
        if prior is not None and prior["source_sha256"] != row["source_sha256"]:
            failures.append(f"skill_id_collision:{skill_id}")
            continue
        by_skill[skill_id] = row
        by_hash[str(row["source_sha256"])].append(row)

    pool: list[dict[str, Any]] = []
    exact_duplicate_groups: list[dict[str, Any]] = []
    for source_hash, grouped in sorted(by_hash.items()):
        grouped = sorted(grouped, key=lambda row: str(row["skill_id"]))
        if len(grouped) > 1:
            exact_duplicate_groups.append({"source_sha256": source_hash, "skill_ids": [row["skill_id"] for row in grouped]})
        selected = grouped[0]
        pool.append(
            {
                "c0_pool_status": "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT",
                "skill_id": selected["skill_id"],
                "origin": selected["origin"],
                "repository_url": selected.get("repository_url"),
                "pinned_commit": selected["pinned_commit"],
                "license": selected.get("license"),
                "license_status": selected.get(
                    "license_status", "DECLARED_REPOSITORY_LICENSE"
                ),
                "source_repository_path": selected["source_repository_path"],
                "source_url": selected.get("source_url"),
                "source_sha256": selected["source_sha256"],
                "source_bytes": selected.get("source_bytes"),
                "local_original_path": selected["local_original_path"],
                "source_name": selected.get("source_name"),
                "source_description_preview": selected.get("source_description_preview"),
                "source_heading_preview": selected.get("source_heading_preview"),
                "source_inventory": selected["_source_inventory"],
            }
        )

    pool.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    args.output_jsonl.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in pool), encoding="utf-8"
    )
    summary = {
        "status": "C0_SOURCE_POOL_PASS_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0_SOURCE_POOL_FAIL_OR_INCOMPLETE",
        "input_inventory_count": len(inputs),
        "raw_verified_source_rows": len(raw_rows),
        "unique_skill_id_count": len(by_skill),
        "source_only_pool_count": len(pool),
        "origins": dict(sorted(Counter(str(row["origin"]) for row in pool).items())),
        "exact_duplicate_hash_groups_excluded": exact_duplicate_groups,
        "integrity_failures": failures,
        "exclusions": [
            "No semantic grouping or similarity score was calculated.",
            "No candidate cluster, prompt, gold label, acceptable set, embedding, selector call, retrieval score, or result was created.",
            "Source selection is origin-agnostic; any later cluster must still pass cross-source C0-C6 gates.",
        ],
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "source_only_pool_count", "integrity_failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
