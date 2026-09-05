#!/usr/bin/env python3
"""Flatten one completed cross-source RQ1b M1 staging batch.

This is a local integrity bridge only. It verifies every byte-preserved
``SKILL.original.md`` against its per-source manifest before emitting a
source-only navigation manifest. It does not infer semantic relation or form
any cluster, prompt, label, acceptable set, retrieval input, or result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ORIGINAL_FILE = "SKILL.original.md"
EXPECTED_STAGE_STATUS = "STAGED_SOURCE_ONLY_NOT_A_CLUSTER"
EXPECTED_BATCH_STATUS = "M1_LOCAL_BYTE_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staging-summary", type=Path, required=True)
    parser.add_argument("--staged-root", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--out-manifest", type=Path, required=True)
    parser.add_argument("--out-summary", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    batch = json.loads(args.staging_summary.read_text(encoding="utf-8"))
    if batch.get("status") != EXPECTED_BATCH_STATUS:
        raise SystemExit("M1 staging summary is not complete")

    failures: list[str] = []
    rows: list[dict[str, Any]] = []
    all_stage_rows = 0
    for result in batch.get("results", []):
        destination = Path(str(result["staging_destination"])).resolve()
        stage_directory = destination.name
        manifest_path = destination / "source_expansion_manifest.jsonl"
        summary_path = destination / "source_expansion_summary.json"
        if not manifest_path.is_file() or not summary_path.is_file():
            failures.append(f"missing_stage_record:{stage_directory}")
            continue
        source_rows = read_jsonl(manifest_path)
        all_stage_rows += len(source_rows)
        source_summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if source_summary != result.get("staging_summary"):
            failures.append(f"summary_drift:{stage_directory}")
        if int(source_summary.get("discovered_skill_files", -1)) != len(source_rows):
            failures.append(f"source_row_count_mismatch:{stage_directory}")

        for source in source_rows:
            if source.get("source_status") != EXPECTED_STAGE_STATUS:
                continue
            skill_id = str(source["skill_id"])
            original = destination / "skills" / skill_id / "source" / ORIGINAL_FILE
            if not original.is_file():
                failures.append(f"missing_original:{stage_directory}:{skill_id}")
                continue
            actual_sha = sha256(original)
            if actual_sha != source.get("source_sha256"):
                failures.append(f"source_hash_drift:{stage_directory}:{skill_id}")
                continue
            rows.append({
                "source_admission_status": "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER",
                "skill_id": skill_id,
                "origin": source["origin"],
                "stage_directory": stage_directory,
                "repository_url": source["repository_url"],
                "pinned_commit": source["pinned_commit"],
                "license": source["license"],
                "license_status": (
                    "NO_DECLARED_REPOSITORY_LICENSE_REFERENCE_ONLY"
                    if source.get("license") == "NO_DECLARED_REPOSITORY_LICENSE"
                    else source["license_status"]
                ),
                "source_repository_path": source["source_repository_path"],
                "source_url": source["source_url"],
                "source_sha256": actual_sha,
                "source_bytes": original.stat().st_size,
                "local_original_path": str(original.relative_to(Path.cwd())),
                "frontmatter_name": source.get("frontmatter_name"),
                "frontmatter_description": source.get("frontmatter_description"),
                "m1_batch": args.batch_id,
            })

    by_skill = Counter(str(row["skill_id"]) for row in rows)
    duplicate_skills = sorted(skill for skill, count in by_skill.items() if count > 1)
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_hash[str(row["source_sha256"])].append(row)
    exact_duplicate_hash_groups = []
    canonical_rows = []
    for source_hash, grouped in sorted(by_hash.items()):
        grouped.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
        canonical_rows.append(grouped[0])
        if len(grouped) > 1:
            exact_duplicate_hash_groups.append({
                "source_sha256": source_hash,
                "canonical_skill_id": grouped[0]["skill_id"],
                "duplicate_skill_ids": [row["skill_id"] for row in grouped[1:]],
            })
    if duplicate_skills:
        failures.append(f"duplicate_staged_skill_ids:{len(duplicate_skills)}")

    pre_canonical_source_count = len(rows)
    rows = canonical_rows
    rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    summary = {
        "status": "M1_PASS_PINNED_BYTE_VERIFIED_NOT_A_CLUSTER_OR_RESULT" if not failures else "M1_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "batch_id": args.batch_id,
        "batch_staging_summary": str(args.staging_summary),
        "all_source_stage_rows": all_stage_rows,
        "pre_canonical_source_count": pre_canonical_source_count,
        "m1_staged_source_count": len(rows),
        "origin_count": len({str(row["origin"]) for row in rows}),
        "by_origin": dict(sorted(Counter(str(row["origin"]) for row in rows).items())),
        "reference_only_source_count": sum(row["license_status"] == "NO_DECLARED_REPOSITORY_LICENSE_REFERENCE_ONLY" for row in rows),
        "duplicate_skill_ids": duplicate_skills,
        "exact_duplicate_hash_groups_excluded_from_navigation": exact_duplicate_hash_groups,
        "exact_duplicate_source_count_excluded_from_navigation": pre_canonical_source_count - len(rows),
        "integrity_failures": failures,
        "exclusions": [
            "No source content was executed.",
            "No semantic grouping, cluster, prompt, gold label, acceptable set, embedding, selector call, retrieval score, metric, or thesis result was created.",
            "This M1 manifest only records exact-byte-preserved original-source candidates for later source-agnostic navigation.",
        ],
    }
    args.out_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "m1_staged_source_count", "origin_count", "reference_only_source_count", "integrity_failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
