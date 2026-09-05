#!/usr/bin/env python3
"""Build a hash-canonical RQ2b-NC candidate-union preflight.

The output is an intake manifest, not the final benchmark: no RQ2 prompt,
I1/I2/I3 representation, extraction, retrieval, reranking or result is
materialised here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_V3_IDENTITY = ROOT / "rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_extraction/identity_manifest.jsonl"
DEFAULT_RQ1_INVENTORY = ROOT / "rq1b_naturalistic_public_replication/manifest/source_inventory.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "rq2b_naturalistic_confusability/manifests/candidate_union_preflight_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def source_import_binding(source_path: Path, source_hash: str) -> dict[str, Any]:
    if not source_path.is_absolute():
        source_path = ROOT.parent / source_path
    import_path = source_path.with_name("IMPORT.json")
    result: dict[str, Any] = {
        "source_path": str(source_path.relative_to(ROOT)),
        "source_hash_matches_inventory": source_path.is_file() and sha256_file(source_path) == source_hash,
        "import_metadata_path": str(import_path.relative_to(ROOT)) if import_path.is_file() else None,
    }
    if not import_path.is_file():
        result["status"] = "FAIL_NO_IMPORT_METADATA"
        return result
    try:
        metadata = json.loads(import_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        result["status"] = "FAIL_UNREADABLE_IMPORT_METADATA"
        return result

    metadata_hash = metadata.get("source_sha256")
    pinned_reference = metadata.get("pinned_commit") or metadata.get("repository_ref")
    licence = metadata.get("license")
    licence_hash = metadata.get("license_sha256")
    licence_path = metadata.get("license_path")
    local_licence_hash_matches: bool | None = None
    local_licence_path: Path | None = None
    # The RQ1 staged layout is <stage>/skills/<id>/source/SKILL.original.md.
    if licence_path and licence_hash and len(source_path.parents) >= 4:
        local_licence_path = source_path.parents[3] / str(licence_path)
        if local_licence_path.is_file():
            local_licence_hash_matches = sha256_file(local_licence_path) == str(licence_hash)

    if not result["source_hash_matches_inventory"] or metadata_hash != source_hash:
        status = "FAIL_SOURCE_OR_IMPORT_HASH_MISMATCH"
    elif not pinned_reference:
        status = "FAIL_NO_IMMUTABLE_SOURCE_REFERENCE"
    elif not licence:
        status = "FAIL_LICENSE_UNDECLARED"
    elif local_licence_hash_matches is True:
        status = "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH"
    else:
        status = "PASS_CAPTURED_SOURCE_PIN_LICENSE_DECLARED_FILE_NOT_VERIFIED"

    result.update(
        {
            "status": status,
            "import_metadata_sha256": sha256_file(import_path),
            "origin": metadata.get("origin"),
            "repository_url": metadata.get("repository_url"),
            "source_url": metadata.get("source_url"),
            "pinned_reference": pinned_reference,
            "license_declared": licence,
            "license_path": licence_path,
            "license_sha256": licence_hash,
            "local_license_path": str(local_licence_path.relative_to(ROOT)) if local_licence_path and local_licence_path.is_file() else None,
            "local_license_hash_matches_record": local_licence_hash_matches,
        }
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v3-identity", type=Path, default=DEFAULT_V3_IDENTITY)
    parser.add_argument("--rq1-inventory", type=Path, default=DEFAULT_RQ1_INVENTORY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = [args.v3_identity, args.rq1_inventory]
    missing = [str(path) for path in inputs if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    v3_rows = read_jsonl(args.v3_identity)
    rq1_rows = read_jsonl(args.rq1_inventory)

    v3_by_hash: dict[str, list[dict[str, str]]] = {}
    for row in v3_rows:
        source_hash = str(row["source_sha256"])
        v3_by_hash.setdefault(source_hash, []).append(
            {"skill_id": str(row["skill_id"]), "source_path": str(row["source"])}
        )
    for records in v3_by_hash.values():
        records.sort(key=lambda row: row["skill_id"])

    rq1_by_hash: dict[str, list[dict[str, Any]]] = {}
    for row in rq1_rows:
        source_hash = str(row["source_sha256"])
        rq1_by_hash.setdefault(source_hash, []).append(row)
    for records in rq1_by_hash.values():
        records.sort(key=lambda row: str(row["skill_id"]))

    all_hashes = sorted(set(v3_by_hash) | set(rq1_by_hash))
    output_rows: list[dict[str, Any]] = []
    new_status_counts: Counter[str] = Counter()
    for source_hash in all_hashes:
        v3_records = v3_by_hash.get(source_hash, [])
        rq1_records = rq1_by_hash.get(source_hash, [])
        if v3_records:
            output_rows.append(
                {
                    "canonical_source_sha256": source_hash,
                    "final_intake_role": "PARENT_V3_CANONICAL_SOURCE",
                    "v3_identity_records": v3_records,
                    "rq1_exact_reuse_records": [
                        {"skill_id": str(row["skill_id"]), "source_path": str(row["source_path"])}
                        for row in rq1_records
                    ],
                    "parent_v3_duplicate_alias_count": len(v3_records) - 1,
                    "status": "PARENT_V3_SOURCE_NOT_REAUDITED_BY_NC_PRECHECK",
                }
            )
            continue

        if not rq1_records:
            raise SystemExit(f"Internal union error for {source_hash}")
        if len({str(row["source_path"]) for row in rq1_records}) != len(rq1_records):
            raise SystemExit(f"Unexpected duplicate RQ1 source path for {source_hash}")
        binding = source_import_binding(Path(str(rq1_records[0]["source_path"])), source_hash)
        new_status_counts[str(binding["status"])] += 1
        output_rows.append(
            {
                "canonical_source_sha256": source_hash,
                "final_intake_role": "RQ1_NEW_PUBLIC_SOURCE_CANDIDATE",
                "rq1_records": [
                    {
                        "skill_id": str(row["skill_id"]),
                        "source_path": str(row["source_path"]),
                        "frontmatter_name": str(row.get("frontmatter_name") or ""),
                    }
                    for row in rq1_records
                ],
                "rq1_duplicate_alias_count": len(rq1_records) - 1,
                "provenance_binding": binding,
                "status": str(binding["status"]),
            }
        )

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    union_path = output_dir / "canonical_candidate_union_preflight.jsonl"
    write_jsonl(union_path, output_rows)

    v3_duplicate_aliases = sum(max(0, len(records) - 1) for records in v3_by_hash.values())
    rq1_duplicate_aliases = sum(max(0, len(records) - 1) for records in rq1_by_hash.values())
    shared_hashes = set(v3_by_hash) & set(rq1_by_hash)
    summary = {
        "status": "PASS_HASH_CANONICAL_UNION_PREFLIGHT_NOT_FINAL_BENCHMARK",
        "claim_boundary": [
            "One final candidate is planned per exact source SHA-256; aliases are retained only in the parent mapping.",
            "The parent V3 set remains preserved for historical reproducibility; this preflight does not alter V3.",
            "RQ1-only sources pass only a provenance intake check here. They still need semantic-cluster, prompt/label and representation-integrity gates.",
            "No model, network, embedding, selector, reranker, prompt, label, extraction or metric is produced.",
        ],
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in inputs},
        "v3_identity_rows": len(v3_rows),
        "v3_unique_source_hashes": len(v3_by_hash),
        "v3_duplicate_alias_rows": v3_duplicate_aliases,
        "rq1_inventory_rows": len(rq1_rows),
        "rq1_unique_source_hashes": len(rq1_by_hash),
        "rq1_duplicate_alias_rows": rq1_duplicate_aliases,
        "v3_rq1_exact_shared_source_hashes": len(shared_hashes),
        "rq1_new_unique_source_candidates": len(set(rq1_by_hash) - set(v3_by_hash)),
        "potential_final_canonical_candidate_count": len(all_hashes),
        "rq1_new_provenance_status_counts": dict(sorted(new_status_counts.items())),
        "artifacts": {"canonical_candidate_union_preflight.jsonl": sha256_file(union_path)},
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
