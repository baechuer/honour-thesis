#!/usr/bin/env python3
"""Verify and flatten completed Round 22 M1 byte-staging batches.

This is a source-integrity bridge.  It reads per-source staging manifests,
rehashes every preserved original, and emits only source-navigation metadata.
It never forms candidate clusters or produces prompts, labels, model inputs,
metrics, or empirical results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ORIGINAL_FILE = "SKILL.original.md"
COMPLETE = "M1_ROUND22_BATCH_COMPLETE_WITH_PER_SOURCE_STATUS_NOT_A_CLUSTER_OR_RESULT"
STAGED = {
    "M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT",
    "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-summary", action="append", type=Path, required=True)
    parser.add_argument("--out-manifest", type=Path, required=True)
    parser.add_argument("--out-summary", type=Path, required=True)
    args = parser.parse_args()

    batches = [json.loads(path.read_text(encoding="utf-8")) for path in args.batch_summary]
    batch_ids = [str(batch.get("batch_id")) for batch in batches]
    if len(batch_ids) != len(set(batch_ids)):
        raise SystemExit("duplicate_batch_id")
    if any(batch.get("status") != COMPLETE for batch in batches):
        raise SystemExit("incomplete_or_wrong_round22_batch")

    integrity_failures: list[str] = []
    staged_records: list[dict[str, Any]] = []
    all_source_manifest_rows = 0
    for batch, batch_path in zip(batches, args.batch_summary):
        for result in batch.get("results", []):
            if result.get("m1_stage_status") not in STAGED:
                integrity_failures.append(f"not_staged:{batch.get('batch_id')}:{result.get('origin')}:{result.get('m1_stage_status')}")
                continue
            destination = Path(str(result["staging_destination"])).resolve()
            source_manifest = destination / "source_expansion_manifest.jsonl"
            source_summary = destination / "source_expansion_summary.json"
            if not source_manifest.is_file() or not source_summary.is_file():
                integrity_failures.append(f"missing_stage_record:{batch.get('batch_id')}:{destination.name}")
                continue
            local_summary = json.loads(source_summary.read_text(encoding="utf-8"))
            if local_summary != result.get("staging_summary"):
                integrity_failures.append(f"summary_drift:{batch.get('batch_id')}:{destination.name}")
            if sha256(source_summary) != result.get("staging_summary_sha256"):
                integrity_failures.append(f"summary_hash_drift:{batch.get('batch_id')}:{destination.name}")
            source_rows = read_jsonl(source_manifest)
            all_source_manifest_rows += len(source_rows)
            if int(local_summary.get("discovered_skill_files", -1)) != len(source_rows):
                integrity_failures.append(f"source_row_count_mismatch:{batch.get('batch_id')}:{destination.name}")
            for source in source_rows:
                if source.get("source_status") != "STAGED_SOURCE_ONLY_NOT_A_CLUSTER":
                    continue
                skill_id = str(source["skill_id"])
                original = destination / "skills" / skill_id / "source" / ORIGINAL_FILE
                if not original.is_file():
                    integrity_failures.append(f"missing_original:{destination.name}:{skill_id}")
                    continue
                actual = sha256(original)
                if actual != source.get("source_sha256"):
                    integrity_failures.append(f"source_hash_drift:{destination.name}:{skill_id}")
                    continue
                staged_records.append({
                    "source_admission_status": "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER",
                    "skill_id": skill_id,
                    "origin": source["origin"],
                    "repository_url": source["repository_url"],
                    "pinned_commit": source["pinned_commit"],
                    "source_repository_path": source["source_repository_path"],
                    "source_url": source["source_url"],
                    "source_sha256": actual,
                    "source_bytes": original.stat().st_size,
                    "license": source["license"],
                    "license_status": source["license_status"],
                    "frontmatter_name": source.get("frontmatter_name"),
                    "frontmatter_description": source.get("frontmatter_description"),
                    "stage_directory": destination.name,
                    "local_original_path": str(original.relative_to(Path.cwd())),
                    "m1_batch": batch["batch_id"],
                    "m1_batch_summary": str(batch_path),
                })

    duplicate_skill_ids = sorted(skill for skill, count in Counter(str(row["skill_id"]) for row in staged_records).items() if count > 1)
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in staged_records:
        by_hash[str(row["source_sha256"])].append(row)
    canonical: list[dict[str, Any]] = []
    duplicate_hash_groups: list[dict[str, Any]] = []
    for source_hash, grouped in sorted(by_hash.items()):
        grouped.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
        canonical.append(grouped[0])
        if len(grouped) > 1:
            duplicate_hash_groups.append({
                "source_sha256": source_hash,
                "canonical_skill_id": grouped[0]["skill_id"],
                "excluded_duplicate_skill_ids": [row["skill_id"] for row in grouped[1:]],
            })
    if duplicate_skill_ids:
        integrity_failures.append(f"duplicate_skill_ids:{len(duplicate_skill_ids)}")
    canonical.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))

    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in canonical), encoding="utf-8")
    summary = {
        "status": "M1_PASS_ROUND22_PINNED_BYTE_VERIFIED_NOT_A_CLUSTER_OR_RESULT" if not integrity_failures else "M1_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "batch_ids": batch_ids,
        "batch_summary_inputs": [str(path) for path in args.batch_summary],
        "staged_origin_count": len({str(row["origin"]) for row in staged_records}),
        "all_source_stage_rows": all_source_manifest_rows,
        "pre_canonical_source_count": len(staged_records),
        "m1_staged_source_count": len(canonical),
        "origin_count": len({str(row["origin"]) for row in canonical}),
        "by_origin": dict(sorted(Counter(str(row["origin"]) for row in canonical).items())),
        "skipped_missing_frontmatter_count": all_source_manifest_rows - len(staged_records),
        "exact_duplicate_source_count_excluded_from_navigation": len(staged_records) - len(canonical),
        "exact_duplicate_hash_groups_excluded_from_navigation": duplicate_hash_groups,
        "duplicate_skill_ids": duplicate_skill_ids,
        "integrity_failures": integrity_failures,
        "exclusions": [
            "No source content was executed.",
            "No semantic grouping, cluster, prompt, gold label, acceptable set, embedding, selector call, retrieval score, metric, or result was created.",
            "The manifest records byte-verified original-source candidates only; later source-only review remains required for any cluster draft.",
        ],
    }
    args.out_summary.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "m1_staged_source_count", "origin_count", "skipped_missing_frontmatter_count", "integrity_failures")}, sort_keys=True))
    return 0 if not integrity_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
