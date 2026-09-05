#!/usr/bin/env python3
"""Audit provenance and disjointness of an RQ1b v3 C0 source-review wave."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    args = parser.parse_args()
    roster_path = args.wave_dir / "c0_review_roster.jsonl"
    manifest_path = args.wave_dir / "c0_review_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    rows = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    errors: list[str] = []
    source_ids: list[str] = []
    triad_ids: set[tuple[str, ...]] = set()
    for row in rows:
        members = row.get("members", [])
        ids = tuple(sorted(member.get("source_id", "") for member in members))
        if len(members) != 3 or len(set(ids)) != 3:
            errors.append(f"{row.get('c0_review_id')}: invalid member cardinality")
        if ids in triad_ids:
            errors.append(f"{row.get('c0_review_id')}: duplicate triad")
        triad_ids.add(ids)
        if len({member.get('origin_key') for member in members}) != 3:
            errors.append(f"{row.get('c0_review_id')}: origins not distinct")
        for member in members:
            path = Path(member["absolute_path"])
            if not path.is_file():
                errors.append(f"{row.get('c0_review_id')}: missing source {path}")
                continue
            if sha256_file(path) != member["sha256"]:
                errors.append(f"{row.get('c0_review_id')}: hash drift {member['source_id']}")
            source_ids.append(member["source_id"])
    if len(source_ids) != len(set(source_ids)):
        errors.append("source reuse detected across C0 triads")
    if manifest.get("triads") != len(rows):
        errors.append("manifest triad count mismatch")
    result = {
        "status": "PASS" if not errors else "FAIL",
        "triads": len(rows),
        "sources": len(source_ids),
        "unique_sources": len(set(source_ids)),
        "errors": errors,
        "claim_boundary": "This audit checks only source binding and roster disjointness; it does not assess semantic validity, gold labels, field recoverability, or retrieval.",
    }
    output_path = args.wave_dir / "C0_SOURCE_REVIEW_WAVE_AUDIT.json"
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
