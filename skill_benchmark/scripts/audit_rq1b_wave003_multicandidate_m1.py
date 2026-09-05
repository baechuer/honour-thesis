#!/usr/bin/env python3
"""Audit the separate Wave 003 multi-candidate M1 source-staging batch.

This is provenance and byte-integrity validation only. It does not read skill
content semantically, form candidate sets, author prompts, assign labels, or
run a model/retriever.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ORIGINAL_FILE = "SKILL.original.md"
STAGED_STATUS = "STAGED_SOURCE_ONLY_NOT_A_CLUSTER"
EXPECTED_STAGE_STATUS = "LOCAL_STAGED_SOURCE_EXPANSION_ONLY_NOT_A_BENCHMARK_OR_RESULT"


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
        "--stage-directory",
        action="append",
        default=[],
        help=(
            "Exact staging-directory name to audit; repeatable. When omitted, "
            "audit every wave_003-mc-* directory under --staged-root."
        ),
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=Path(
            "skill_benchmark/rq1b_naturalistic_public_replication/manifest/"
            "wave_003_multicandidate_m1_staged_source_manifest_2026-08-26.jsonl"
        ),
    )
    parser.add_argument(
        "--output-summary",
        type=Path,
        default=Path(
            "skill_benchmark/rq1b_naturalistic_public_replication/manifest/"
            "wave_003_multicandidate_m1_staging_audit_2026-08-26.json"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    staged_root = args.staged_root.resolve()
    if args.stage_directory:
        stage_dirs = [staged_root / name for name in args.stage_directory]
        missing_dirs = [path.name for path in stage_dirs if not path.is_dir()]
        if missing_dirs:
            raise SystemExit(f"Requested staging directory does not exist: {', '.join(missing_dirs)}")
        if len(set(args.stage_directory)) != len(args.stage_directory):
            raise SystemExit("Duplicate --stage-directory argument")
        stage_dirs = sorted(stage_dirs)
    else:
        stage_dirs = sorted(path for path in staged_root.glob("wave_003-mc-*") if path.is_dir())
    if not stage_dirs:
        raise SystemExit("No Wave 003 multi-candidate M1 staging directories found")

    failures: list[str] = []
    records: list[dict[str, object]] = []
    skipped_counts: Counter[str] = Counter()
    source_summaries: list[dict[str, object]] = []

    for stage_dir in stage_dirs:
        manifest_path = stage_dir / "source_expansion_manifest.jsonl"
        summary_path = stage_dir / "source_expansion_summary.json"
        if not manifest_path.is_file() or not summary_path.is_file():
            failures.append(f"missing stage manifest or summary: {stage_dir.name}")
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("status") != EXPECTED_STAGE_STATUS:
            failures.append(f"unexpected stage status: {stage_dir.name}")
        source_summaries.append(
            {
                "stage_directory": stage_dir.name,
                "origin": summary.get("origin"),
                "repository_url": summary.get("repository_url"),
                "pinned_commit": summary.get("pinned_commit"),
                "license": summary.get("license"),
                "license_status": summary.get("license_status", "DECLARED_REPOSITORY_LICENSE"),
                "discovered_skill_files": summary.get("discovered_skill_files"),
                "staged_sources": summary.get("staged_sources"),
                "skipped_exact_duplicates": summary.get("skipped_exact_duplicates"),
                "skipped_missing_frontmatter": summary.get("skipped_missing_frontmatter"),
            }
        )
        for source_record in read_jsonl(manifest_path):
            source_status = str(source_record.get("source_status"))
            if source_status != STAGED_STATUS:
                skipped_counts[source_status] += 1
                continue
            skill_id = str(source_record["skill_id"])
            original_path = stage_dir / "skills" / skill_id / "source" / ORIGINAL_FILE
            if not original_path.is_file():
                failures.append(f"missing staged original: {stage_dir.name}/{skill_id}")
                continue
            actual_sha = sha256(original_path)
            if actual_sha != source_record.get("source_sha256"):
                failures.append(f"sha mismatch: {stage_dir.name}/{skill_id}")
                continue
            records.append(
                {
                    "source_admission_status": "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER",
                    "skill_id": skill_id,
                    "stage_directory": stage_dir.name,
                    "origin": source_record["origin"],
                    "repository_url": source_record["repository_url"],
                    "pinned_commit": source_record["pinned_commit"],
                    "source_repository_path": source_record["source_repository_path"],
                    "source_url": source_record["source_url"],
                    "license": source_record["license"],
                    "license_status": source_record.get(
                        "license_status", "DECLARED_REPOSITORY_LICENSE"
                    ),
                    "license_sha256": source_record["license_sha256"],
                    "source_sha256": actual_sha,
                    "source_bytes": source_record["source_bytes"],
                }
            )

    by_hash: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        by_hash[str(record["source_sha256"])].append(record)
    for source_hash, grouped in by_hash.items():
        if len(grouped) > 1:
            ids = ", ".join(sorted(str(record["skill_id"]) for record in grouped))
            failures.append(f"duplicate source hash within M1 batch {source_hash}: {ids}")

    manifest_records = sorted(records, key=lambda record: (str(record["origin"]), str(record["skill_id"])))
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in manifest_records),
        encoding="utf-8",
    )

    by_origin = Counter(str(record["origin"]) for record in manifest_records)
    summary = {
        "status": (
            "M1_PASS_PINNED_SOURCE_STAGING_ONLY_NOT_A_CLUSTER_OR_RESULT"
            if not failures
            else "M1_FAIL_PINNED_SOURCE_STAGING_ONLY_NOT_A_CLUSTER_OR_RESULT"
        ),
        "stage_directories": [directory.name for directory in stage_dirs],
        "source_stage_summaries": source_summaries,
        "staged_original_count": len(manifest_records),
        "staged_by_origin": dict(sorted(by_origin.items())),
        "skipped_status_counts": dict(sorted(skipped_counts.items())),
        "intra_batch_duplicate_hash_groups": sum(len(grouped) > 1 for grouped in by_hash.values()),
        "integrity_failures": failures,
        "exclusions": [
            "No source artifact was executed.",
            "No M2 source-only multi-candidate judgement was made.",
            "No prompt, label, acceptable-set decision, representation, model call, retrieval score, or result was created.",
            "A staged original is not a valid RQ1b cluster.",
        ],
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
