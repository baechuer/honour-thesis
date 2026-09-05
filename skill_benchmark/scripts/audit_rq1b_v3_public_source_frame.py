#!/usr/bin/env python3
"""Independently validate and freeze an RQ1b v3 local public source frame."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any


AUDIT_VERSION = "rq1b-v3-public-source-frame-audit-v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_and_size(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-frame-dir", type=Path, required=True)
    parser.add_argument("--rehash", action="store_true")
    args = parser.parse_args()
    root = args.source_frame_dir
    manifest_path = root / "source_frame_manifest.json"
    canonical_path = root / "canonical_sources.jsonl"
    aliases_path = root / "source_aliases.jsonl"
    invalid_path = root / "invalid_utf8_exclusions.jsonl"
    certificate_path = root / "SOURCE_FRAME_FREEZE_CERTIFICATE.json"
    if certificate_path.exists():
        raise ValueError(f"refusing to overwrite existing freeze certificate: {certificate_path}")
    manifest = json.loads(manifest_path.read_text())
    canonical = read_jsonl(canonical_path)
    aliases = read_jsonl(aliases_path)
    invalid = read_jsonl(invalid_path)
    if manifest.get("status") != "RQ1B_V3_PUBLIC_SOURCE_FRAME_LOCAL_ONLY_UNFROZEN":
        raise ValueError("unexpected source-frame status")
    artifacts = manifest.get("artifacts", {})
    for path in (canonical_path, aliases_path, invalid_path):
        if artifacts.get(path.name) != sha256_file(path):
            raise ValueError(f"artifact hash mismatch: {path.name}")
    if len(canonical) != manifest.get("canonical_artifact_count") or len(aliases) != manifest.get("input_path_count") - len(invalid):
        raise ValueError("manifest count mismatch")
    source_ids = [row.get("source_id") for row in canonical]
    source_hashes = [row.get("sha256") for row in canonical]
    if len(set(source_ids)) != len(source_ids) or len(set(source_hashes)) != len(source_hashes):
        raise ValueError("canonical source identity is not unique")
    canonical_by_id = {row["source_id"]: row for row in canonical}
    aliases_by_id: dict[str, list[dict[str, Any]]] = {identifier: [] for identifier in canonical_by_id}
    roots = {Path(path).resolve() for path in manifest["source_roots"].values()}
    for alias in aliases:
        source_id = alias.get("source_id")
        if source_id not in aliases_by_id:
            raise ValueError("alias references unknown canonical source")
        path = Path(alias["absolute_path"])
        if path.name != "SKILL.original.md" or not any(root in path.resolve().parents for root in roots):
            raise ValueError("alias lies outside frozen public-source roots")
        if alias.get("sha256") != canonical_by_id[source_id]["sha256"]:
            raise ValueError("alias SHA does not match canonical source")
        aliases_by_id[source_id].append(alias)
    for source_id, row in canonical_by_id.items():
        aliases_for_id = aliases_by_id[source_id]
        if len(aliases_for_id) != row.get("alias_count") or sum(alias.get("is_canonical") is True for alias in aliases_for_id) != 1:
            raise ValueError("alias cardinality/canonical binding mismatch")
    rehash_count = 0
    if args.rehash:
        started = time.perf_counter()
        for index, row in enumerate(canonical, start=1):
            path = Path(row["canonical"]["absolute_path"])
            sha256, byte_count = sha256_and_size(path)
            if sha256 != row["sha256"] or byte_count != row["byte_count"]:
                raise ValueError(f"canonical source drift: {row['source_id']}")
            rehash_count += 1
            if index % 500 == 0 or index == len(canonical):
                print(f"SOURCE_FRAME_AUDIT_PROGRESS rehashed={index}/{len(canonical)}", flush=True)
        rehash_seconds = time.perf_counter() - started
    else:
        rehash_seconds = None
    certificate = {
        "status": "RQ1B_V3_PUBLIC_SOURCE_FRAME_FROZEN_LOCAL_ONLY",
        "audit_version": AUDIT_VERSION,
        "source_frame_manifest_sha256": sha256_file(manifest_path),
        "artifact_hashes": {path.name: sha256_file(path) for path in (canonical_path, aliases_path, invalid_path)},
        "counts": {
            "canonical_artifacts": len(canonical),
            "source_paths": len(aliases),
            "duplicate_alias_paths": len(aliases) - len(canonical),
            "invalid_utf8_exclusions": len(invalid),
            "rehash_count": rehash_count,
        },
        "rehash_seconds": rehash_seconds,
        "network_calls": 0,
        "texts_transmitted": 0,
        "next_gate": "V3-S2 structural census and V3-C0 local candidate-draft discovery only; no selector or external-text run is authorised by this certificate.",
    }
    certificate_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"valid": True, **certificate}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
