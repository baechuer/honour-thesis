#!/usr/bin/env python3
"""Flatten verified Round 20 source staging into an M1 source manifest.

This is a local integrity bridge between the per-origin staging records and
the existing zero-network navigation builder. It does not inspect semantic
relations or construct an RQ1b candidate cluster.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
STAGED_ROOT = ROOT / "rq1b_cross_source_public_benchmark" / "staged_sources"
STAGING_SUMMARY = MANIFEST_DIR / "m1_round20_staged_source_summary_2026-08-27.json"
OUT_MANIFEST = MANIFEST_DIR / "m1_round20_staged_source_manifest_2026-08-27.jsonl"
OUT_SUMMARY = MANIFEST_DIR / "m1_round20_staged_source_manifest_summary_2026-08-27.json"
ORIGINAL_FILE = "SKILL.original.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    batch = json.loads(STAGING_SUMMARY.read_text(encoding="utf-8"))
    if batch.get("status") != "M1_LOCAL_BYTE_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT":
        raise SystemExit("Round 20 staging summary is not complete")

    failures: list[str] = []
    staged_rows: list[dict[str, object]] = []
    all_stage_rows = 0
    for result in batch["results"]:
        destination = Path(str(result["staging_destination"]))
        stage_directory = destination.name
        manifest_path = destination / "source_expansion_manifest.jsonl"
        if not manifest_path.is_file():
            failures.append(f"missing_source_expansion_manifest:{stage_directory}")
            continue
        source_rows = read_jsonl(manifest_path)
        all_stage_rows += len(source_rows)
        source_summary = json.loads((destination / "source_expansion_summary.json").read_text(encoding="utf-8"))
        if source_summary != result["staging_summary"]:
            failures.append(f"summary_drift:{stage_directory}")
        if int(source_summary["discovered_skill_files"]) != len(source_rows):
            failures.append(f"source_row_count_mismatch:{stage_directory}")

        for source in source_rows:
            if source.get("source_status") != "STAGED_SOURCE_ONLY_NOT_A_CLUSTER":
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
            staged_rows.append(
                {
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
                    "m1_batch": "round20_2026-08-27",
                }
            )

    by_skill = Counter(str(row["skill_id"]) for row in staged_rows)
    duplicate_skills = sorted(skill_id for skill_id, count in by_skill.items() if count > 1)
    by_hash: dict[str, list[dict[str, object]]] = {}
    for row in staged_rows:
        by_hash.setdefault(str(row["source_sha256"]), []).append(row)
    duplicate_hash_groups = {
        source_sha: rows
        for source_sha, rows in by_hash.items()
        if len(rows) > 1
    }
    if duplicate_skills:
        failures.append(f"duplicate_staged_skill_ids:{len(duplicate_skills)}")

    # Exact source-byte aliases are not independent candidate skills. Keep one
    # deterministic canonical path and retain every omitted mirror as provenance.
    canonical_rows: list[dict[str, object]] = []
    alias_count = 0
    for source_sha, rows in by_hash.items():
        ordered = sorted(
            rows,
            key=lambda row: (
                len(str(row["source_repository_path"])),
                str(row["source_repository_path"]),
                str(row["skill_id"]),
            ),
        )
        canonical = dict(ordered[0])
        aliases = [
            {
                "skill_id": row["skill_id"],
                "origin": row["origin"],
                "source_repository_path": row["source_repository_path"],
                "source_url": row["source_url"],
                "local_original_path": row["local_original_path"],
            }
            for row in ordered[1:]
        ]
        canonical["exact_source_hash_group_size"] = len(ordered)
        canonical["source_hash_aliases"] = aliases
        canonical["source_hash_canonicalisation"] = (
            "UNIQUE_SOURCE_HASH" if not aliases else "CANONICAL_SHORTEST_PATH_THEN_LEXICAL"
        )
        canonical_rows.append(canonical)
        alias_count += len(aliases)

    canonical_rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    OUT_MANIFEST.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in canonical_rows),
        encoding="utf-8",
    )
    summary = {
        "status": "M1_PASS_PINNED_BYTE_VERIFIED_NOT_A_CLUSTER_OR_RESULT" if not failures else "M1_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT",
        "batch_staging_summary": str(STAGING_SUMMARY.relative_to(Path.cwd())),
        "all_source_stage_rows": all_stage_rows,
        "all_hash_verified_stage_rows": len(staged_rows),
        "m1_staged_source_count": len(canonical_rows),
        "origin_count": len({str(row["origin"]) for row in canonical_rows}),
        "by_origin": dict(sorted(Counter(str(row["origin"]) for row in canonical_rows).items())),
        "reference_only_source_count": sum(row["license_status"] == "NO_DECLARED_REPOSITORY_LICENSE_REFERENCE_ONLY" for row in canonical_rows),
        "duplicate_skill_ids": duplicate_skills,
        "exact_source_hash_duplicate_groups": {
            source_sha: [
                {
                    "skill_id": row["skill_id"],
                    "origin": row["origin"],
                    "source_repository_path": row["source_repository_path"],
                    "source_url": row["source_url"],
                }
                for row in sorted(
                    rows,
                    key=lambda row: (
                        len(str(row["source_repository_path"])),
                        str(row["source_repository_path"]),
                        str(row["skill_id"]),
                    ),
                )
            ]
            for source_sha, rows in sorted(duplicate_hash_groups.items())
        },
        "exact_source_hash_alias_count_excluded_from_candidate_navigation": alias_count,
        "integrity_failures": failures,
        "exclusions": [
            "No source content was executed.",
            "No semantic grouping, cluster, prompt, gold label, acceptable set, embedding, selector call, retrieval score, metric, or thesis result was created.",
        "This M1 manifest only records exact-byte-preserved original-source candidates for later source-agnostic navigation.",
        "Exact source-byte mirrors are represented as canonical source plus alias provenance; aliases cannot act as separate candidates.",
        ],
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("status", "m1_staged_source_count", "origin_count", "reference_only_source_count", "integrity_failures")}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
