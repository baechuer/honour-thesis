#!/usr/bin/env python3
"""Validate Wave 003's source-only candidate pool without reading it semantically.

The audit checks byte preservation and exact-duplicate status. It intentionally
does not form pairs, author prompts, infer fields, assign labels, or call a
model. Duplicate source files remain preserved in their original staging
directory but are excluded from the net-new candidate count in the emitted
pool manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ORIGINAL_FILE = "SKILL.original.md"
STAGED_STATUS = "STAGED_SOURCE_ONLY_NOT_A_CLUSTER"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staged-root",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/staged_sources"),
    )
    parser.add_argument(
        "--public-imported-root",
        type=Path,
        default=Path("skill_benchmark/skills/public_imported_background"),
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_003_candidate_pool_manifest.jsonl"),
    )
    parser.add_argument(
        "--output-summary",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_003_candidate_pool_summary.json"),
    )
    parser.add_argument("--minimum-net-new", type=int, default=500)
    return parser.parse_args()


def previous_hashes(public_imported_root: Path, staged_root: Path) -> set[str]:
    roots = [public_imported_root]
    roots.extend(path for path in staged_root.iterdir() if path.is_dir() and not path.name.startswith("wave_003-"))
    hashes: set[str] = set()
    for root in roots:
        if root.exists():
            hashes.update(sha256(path) for path in root.rglob(ORIGINAL_FILE))
    return hashes


def main() -> int:
    args = parse_args()
    staged_root = args.staged_root.resolve()
    wave_dirs = sorted(path for path in staged_root.glob("wave_003-*") if path.is_dir())
    if not wave_dirs:
        raise SystemExit("No Wave 003 source-stage directories found")
    old_hashes = previous_hashes(args.public_imported_root.resolve(), staged_root)

    rows: list[dict[str, object]] = []
    failures: list[str] = []
    for wave_dir in wave_dirs:
        manifest_path = wave_dir / "source_expansion_manifest.jsonl"
        summary_path = wave_dir / "source_expansion_summary.json"
        if not manifest_path.is_file() or not summary_path.is_file():
            failures.append(f"missing stage manifest or summary: {wave_dir.name}")
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("status") != "LOCAL_STAGED_SOURCE_EXPANSION_ONLY_NOT_A_BENCHMARK_OR_RESULT":
            failures.append(f"unexpected stage status: {wave_dir.name}")
        for record in read_jsonl(manifest_path):
            if record.get("source_status") != STAGED_STATUS:
                continue
            skill_id = str(record["skill_id"])
            staged_path = wave_dir / "skills" / skill_id / "source" / ORIGINAL_FILE
            if not staged_path.is_file():
                failures.append(f"missing staged file: {wave_dir.name}/{skill_id}")
                continue
            actual_sha = sha256(staged_path)
            if actual_sha != record.get("source_sha256"):
                failures.append(f"sha mismatch: {wave_dir.name}/{skill_id}")
                continue
            rows.append(
                {
                    "skill_id": skill_id,
                    "stage_directory": wave_dir.name,
                    "origin": record["origin"],
                    "repository_url": record["repository_url"],
                    "pinned_commit": record["pinned_commit"],
                    "source_repository_path": record["source_repository_path"],
                    "source_url": record["source_url"],
                    "license": record["license"],
                    "license_sha256": record["license_sha256"],
                    "source_sha256": actual_sha,
                    "source_bytes": record["source_bytes"],
                    "candidate_pool_status": "PENDING_DEDUPLICATION",
                }
            )

    by_hash: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_hash[str(row["source_sha256"])].append(row)
    for source_hash, grouped in by_hash.items():
        ordered = sorted(grouped, key=lambda row: (str(row["origin"]), str(row["skill_id"])))
        for position, row in enumerate(ordered):
            if source_hash in old_hashes:
                row["candidate_pool_status"] = "EXCLUDED_EXACT_DUPLICATE_OF_PRE_WAVE003_SOURCE"
            elif position == 0:
                row["candidate_pool_status"] = "NET_NEW_EXACT_BYTE_DISTINCT_STAGED_ARTIFACT"
            else:
                row["candidate_pool_status"] = "EXCLUDED_EXACT_DUPLICATE_WITHIN_WAVE003"
                row["duplicate_of_skill_id"] = ordered[0]["skill_id"]

    output_rows = sorted(rows, key=lambda row: (str(row["origin"]), str(row["skill_id"])))
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in output_rows), encoding="utf-8"
    )
    statuses = Counter(str(row["candidate_pool_status"]) for row in output_rows)
    net_new_rows = [row for row in output_rows if row["candidate_pool_status"] == "NET_NEW_EXACT_BYTE_DISTINCT_STAGED_ARTIFACT"]
    source_counts = Counter(str(row["origin"]) for row in net_new_rows)
    summary = {
        "status": (
            "D3_PASS_SOURCE_ONLY_POOL_TARGET_REACHED_NOT_A_CLUSTER_OR_RESULT"
            if not failures and len(net_new_rows) >= args.minimum_net_new
            else "D3_FAIL_OR_INCOMPLETE_SOURCE_ONLY_POOL_NOT_A_CLUSTER_OR_RESULT"
        ),
        "minimum_net_new": args.minimum_net_new,
        "wave_003_stage_directories": [path.name for path in wave_dirs],
        "raw_staged_record_count": len(output_rows),
        "net_new_exact_byte_distinct_staged_artifact_count": len(net_new_rows),
        "status_counts": dict(sorted(statuses.items())),
        "net_new_by_origin": dict(sorted(source_counts.items())),
        "cross_wave003_duplicate_hash_group_count": sum(len(group) > 1 for group in by_hash.values()),
        "pre_wave003_duplicate_hash_group_count": sum(source_hash in old_hashes for source_hash in by_hash),
        "integrity_failures": failures,
        "exclusions": [
            "No source artifact was executed.",
            "No pair, cluster, prompt, gold label, acceptable-set decision, representation, selector input, model call, retrieval score, or result was created.",
            "This is a diverse discovery pool only; it does not establish semantic confusability or naturalistic RQ1b validity.",
        ],
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"].startswith("D3_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
