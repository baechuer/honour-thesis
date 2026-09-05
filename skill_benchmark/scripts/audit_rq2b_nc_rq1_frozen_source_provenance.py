#!/usr/bin/env python3
"""Audit local provenance records for frozen RQ1b candidates proposed as NC leads.

The audit checks local byte identity and captured metadata only. It does not
verify a remote repository's present state or make a legal judgement about a
licence; an explicit licence disposition remains required before NC finalisation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WAVE_001 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_001_frozen_manifest.jsonl"
DEFAULT_WAVE_002 = ROOT / "rq1b_naturalistic_public_replication/manifest/wave_002_frozen_manifest.jsonl"
DEFAULT_STAGED_ROOT = ROOT / "rq1b_naturalistic_public_replication/staged_sources"
DEFAULT_SKILLS_ROOT = ROOT / "skills"
DEFAULT_OUTPUT_DIR = ROOT / "rq2b_naturalistic_confusability/manifests/rq1_frozen_source_provenance_2026-08-31"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-001", type=Path, default=DEFAULT_WAVE_001)
    parser.add_argument("--wave-002", type=Path, default=DEFAULT_WAVE_002)
    parser.add_argument("--staged-root", type=Path, default=DEFAULT_STAGED_ROOT)
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def local_license_binding(import_path: Path, metadata: dict[str, Any]) -> tuple[str | None, bool | None]:
    license_path = metadata.get("license_path")
    expected_hash = metadata.get("license_sha256")
    if not license_path or not expected_hash:
        return None, None
    # IMPORT.json lives at <stage>/skills/<id>/source/; licences are captured
    # at the corresponding stage root when locally retained.
    stage_root = import_path.parents[3]
    candidate = stage_root / str(license_path)
    if not candidate.is_file():
        return str(candidate), None
    return str(candidate), sha256_file(candidate) == str(expected_hash)


def main() -> int:
    args = parse_args()
    required = [args.wave_001, args.wave_002, args.staged_root, args.skills_root]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required input(s): {missing}")

    source_to_context: dict[str, dict[str, Any]] = {}
    for parent_wave, manifest_path in (("wave_001", args.wave_001), ("wave_002", args.wave_002)):
        for cluster in read_jsonl(manifest_path):
            for skill_id, source_hash in dict(cluster["source_hashes"]).items():
                source_hash = str(source_hash)
                if source_hash in source_to_context:
                    raise SystemExit(f"Frozen candidate source hash reused: {source_hash}")
                source_to_context[source_hash] = {
                    "parent_rq1_wave": parent_wave,
                    "parent_rq1_cluster_id": str(cluster["cluster_id"]),
                    "rq1_candidate_skill_id": str(skill_id),
                }

    metadata_by_hash: dict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    parsed_import_count = 0
    for import_root in (args.staged_root, args.skills_root):
        for import_path in sorted(import_root.rglob("IMPORT.json")):
            try:
                metadata = json.loads(import_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise SystemExit(f"Unreadable IMPORT.json: {import_path}: {exc}") from exc
            parsed_import_count += 1
            source_hash = metadata.get("source_sha256")
            if not source_hash:
                original_path = import_path.with_name("SKILL.original.md")
                if original_path.is_file():
                    source_hash = sha256_file(original_path)
            if source_hash in source_to_context:
                metadata_by_hash[str(source_hash)].append((import_path, metadata))

    audit_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for source_hash, context in sorted(source_to_context.items()):
        bindings = metadata_by_hash.get(source_hash, [])
        if not bindings:
            status = "FAIL_NO_LOCAL_IMPORT_METADATA"
            row = {**context, "source_sha256": source_hash, "status": status, "import_metadata_bindings": []}
            audit_rows.append(row)
            status_counts[status] += 1
            continue

        binding_rows: list[dict[str, Any]] = []
        for import_path, metadata in bindings:
            original_path = import_path.with_name("SKILL.original.md")
            original_hash_match = original_path.is_file() and sha256_file(original_path) == source_hash
            pinned_value = metadata.get("pinned_commit") or metadata.get("repository_ref")
            pinned = bool(pinned_value)
            licence = metadata.get("license")
            licence_path, licence_hash_matches = local_license_binding(import_path, metadata)
            binding_rows.append(
                {
                    "import_metadata_path": str(import_path.relative_to(ROOT)),
                    "import_metadata_sha256": sha256_file(import_path),
                    "original_path": str(original_path.relative_to(ROOT)) if original_path.is_file() else str(original_path),
                    "original_hash_matches_source_sha256": original_hash_match,
                    "origin": metadata.get("origin"),
                    "repository_url": metadata.get("repository_url"),
                    "source_url": metadata.get("source_url"),
                    "pinned_reference": pinned_value,
                    "license_declared": licence,
                    "license_path": metadata.get("license_path"),
                    "license_sha256": metadata.get("license_sha256"),
                    "local_license_path": licence_path,
                    "local_license_hash_matches_record": licence_hash_matches,
                    "immutable_provenance_eligible": original_hash_match and pinned,
                }
            )

        # One source hash may have multiple local aliases.  A legacy alias whose
        # import record points at `main` cannot invalidate a separate, exact
        # captured commit for the *same verified source bytes*.  Select the
        # strongest exact binding and retain every other binding for audit.
        def binding_priority(binding: dict[str, Any]) -> tuple[int, str]:
            if not binding["immutable_provenance_eligible"]:
                return (0, str(binding["import_metadata_path"]))
            if binding["license_declared"] and binding["local_license_hash_matches_record"] is True:
                return (3, str(binding["import_metadata_path"]))
            if binding["license_declared"]:
                return (2, str(binding["import_metadata_path"]))
            return (1, str(binding["import_metadata_path"]))

        selected = max(binding_rows, key=binding_priority)
        any_source_hash_match = any(row["original_hash_matches_source_sha256"] for row in binding_rows)
        if not any_source_hash_match:
            status = "FAIL_CAPTURED_ORIGINAL_HASH_MISMATCH"
        elif not selected["immutable_provenance_eligible"]:
            status = "FAIL_NO_IMMUTABLE_SOURCE_REFERENCE"
        elif selected["license_declared"] and selected["local_license_hash_matches_record"] is True:
            status = "PASS_CAPTURED_SOURCE_PIN_AND_LICENSE_FILE_HASH"
        elif selected["license_declared"]:
            status = "PASS_CAPTURED_SOURCE_PIN_LICENSE_DECLARED_FILE_NOT_VERIFIED"
        else:
            status = "PASS_CAPTURED_SOURCE_PIN_LICENSE_UNKNOWN"
        status_counts[status] += 1
        audit_rows.append(
            {
                **context,
                "source_sha256": source_hash,
                "status": status,
                "import_metadata_binding_count": len(binding_rows),
                "import_metadata_bindings": binding_rows,
                "selected_provenance_binding": selected,
                "unselected_binding_count": len(binding_rows) - 1,
            }
        )

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = output_dir / "source_provenance_audit.jsonl"
    write_jsonl(rows_path, audit_rows)
    summary = {
        "status": "PASS_LOCAL_CAPTURE_AUDIT_NOT_A_REMOTE_OR_LEGAL_VALIDATION",
        "claim_boundary": [
            "The audit validates the local original-file SHA-256 against its captured metadata.",
            "A recorded pinned commit/reference is provenance evidence for the captured source, not a claim that the remote is still available.",
            "A matching local licence-file hash verifies the captured licence file, not legal scope or compatibility.",
            "When duplicate local aliases share verified source bytes, the strongest exact pinned binding is selected; unpinned legacy aliases remain recorded rather than causing a false failure.",
            "No RQ1 prompt/label is transferred and no RQ2 source row is admitted by this audit alone.",
        ],
        "input_sha256": {
            str(args.wave_001.relative_to(ROOT)): sha256_file(args.wave_001),
            str(args.wave_002.relative_to(ROOT)): sha256_file(args.wave_002),
        },
        "frozen_candidate_source_hash_count": len(source_to_context),
        "staged_import_metadata_files_scanned": parsed_import_count,
        "import_metadata_roots": [str(args.staged_root.relative_to(ROOT)), str(args.skills_root.relative_to(ROOT))],
        "status_counts": dict(sorted(status_counts.items())),
        "artifacts": {"source_provenance_audit.jsonl": sha256_file(rows_path)},
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
