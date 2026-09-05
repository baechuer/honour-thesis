#!/usr/bin/env python3
"""Build a fresh-discovery-plus-unreviewed aggregate pool for Round 42 C0A.

Round 42 still begins with fresh public discovery. This local step makes the
resulting aggregate-library setting explicit: new byte-verified sources are
combined with earlier byte-verified sources that have never appeared in a
protocol-complete C0B or C6 candidate set. It exposes navigation metadata
only and is not semantic grouping or a candidate composition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SUPERSEDED_SOURCE_POOL_FILES = {
    # Round 40's original M1 inventory had a historic-prefix provenance defect.
    # The separately named corrected pool is the sole admissible Round 40 pool.
    "c0_round40_source_pool_2026-08-28.jsonl",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if isinstance(value, dict):
                rows.append(value)
    return rows


def candidate_ids(row: dict[str, Any]) -> set[str]:
    values = row.get("candidate_skill_ids")
    if isinstance(values, list):
        return {str(value) for value in values if str(value)}
    return set()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_files = sorted(
        path
        for path in args.manifest_dir.glob("c0*_source_pool*.jsonl")
        if "aggregate_unreviewed" not in path.name and path.name not in SUPERSEDED_SOURCE_POOL_FILES
    )
    source_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for source_file in source_files:
        for row in read_jsonl(source_file):
            required = ("skill_id", "origin", "source_sha256", "local_original_path")
            if any(not row.get(key) for key in required):
                continue
            local = Path(str(row["local_original_path"]))
            if not local.is_absolute():
                local = (Path.cwd() / local).resolve()
            if not local.is_file():
                failures.append(f"missing_original:{source_file.name}:{row['skill_id']}")
                continue
            if sha256(local) != str(row["source_sha256"]):
                failures.append(f"source_hash_drift:{source_file.name}:{row['skill_id']}")
                continue
            source_rows.append({**row, "_source_file": str(source_file), "local_original_path": str(local)})

    id_to_hash: dict[str, str] = {}
    for row in source_rows:
        skill_id = str(row["skill_id"])
        prior = id_to_hash.get(skill_id)
        if prior is not None and prior != str(row["source_sha256"]):
            failures.append(f"skill_id_hash_collision:{skill_id}")
        id_to_hash[skill_id] = str(row["source_sha256"])

    screened_ids: set[str] = set()
    screened_files = sorted(list(args.manifest_dir.glob("c0b*.jsonl")) + list(args.manifest_dir.glob("c6*.jsonl")))
    for screened_file in screened_files:
        for row in read_jsonl(screened_file):
            screened_ids.update(candidate_ids(row))
    screened_hashes = {id_to_hash[skill_id] for skill_id in screened_ids if skill_id in id_to_hash}

    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    excluded_screened = 0
    for row in source_rows:
        if str(row["source_sha256"]) in screened_hashes:
            excluded_screened += 1
            continue
        by_hash[str(row["source_sha256"])].append(row)

    pool: list[dict[str, Any]] = []
    for source_hash, rows in sorted(by_hash.items()):
        selected = sorted(rows, key=lambda row: (str(row["origin"]), str(row.get("source_repository_path", "")), str(row["skill_id"])))[0]
        pool.append({
            "c0_pool_status": "SOURCE_ONLY_UNPROMPTED_UNLABELLED_NOT_A_CLUSTER_OR_RESULT",
            "round42_aggregate_status": "FRESH_DISCOVERY_PLUS_PRIOR_UNSCREENED_SOURCE_METADATA_ONLY",
            "skill_id": selected["skill_id"],
            "origin": selected["origin"],
            "repository_url": selected.get("repository_url"),
            "pinned_commit": selected.get("pinned_commit"),
            "license": selected.get("license"),
            "license_status": selected.get("license_status"),
            "source_repository_path": selected.get("source_repository_path"),
            "source_url": selected.get("source_url"),
            "source_sha256": source_hash,
            "source_bytes": selected.get("source_bytes"),
            "local_original_path": selected["local_original_path"],
            "source_name": selected.get("source_name") or selected.get("frontmatter_name"),
            "source_description_preview": selected.get("source_description_preview") or selected.get("frontmatter_description"),
            "source_heading_preview": selected.get("source_heading_preview"),
            "source_inventory": selected.get("source_inventory") or selected.get("_source_file"),
        })
    pool.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in pool), encoding="utf-8")
    summary = {
        "status": "C0_ROUND42_AGGREGATE_UNSCREENED_POOL_PASS_NOT_A_CLUSTER_OR_RESULT" if not failures else "C0_ROUND42_AGGREGATE_UNSCREENED_POOL_FAIL_OR_INCOMPLETE",
        "fresh_round42_inventory": "m1_round42_byte_verified_source_inventory_2026-08-28.jsonl",
        "source_pool_file_count": len(source_files),
        "superseded_source_pool_files_excluded": sorted(SUPERSEDED_SOURCE_POOL_FILES),
        "verified_raw_source_rows": len(source_rows),
        "protocol_complete_screened_id_count": len(screened_ids),
        "screened_hash_count": len(screened_hashes),
        "source_rows_excluded_due_to_prior_screened_hash": excluded_screened,
        "aggregate_unscreened_source_count": len(pool),
        "aggregate_unscreened_origin_count": len({str(row["origin"]) for row in pool}),
        "origins": dict(sorted(Counter(str(row["origin"]) for row in pool).items())),
        "integrity_failures": sorted(set(failures)),
        "exclusions": [
            "Every pool item has a local SHA-verified original source; no source body is exposed by this output.",
            "Rows previously used by a protocol-complete C0B or C6 candidate set are excluded by skill id and source hash.",
            "The pool is not a semantic clustering, candidate composition, prompt, label, acceptable-set judgement, retrieval input, model call, metric, or result.",
        ],
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "verified_raw_source_rows", "protocol_complete_screened_id_count", "aggregate_unscreened_source_count", "aggregate_unscreened_origin_count", "integrity_failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
