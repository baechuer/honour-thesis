#!/usr/bin/env python3
"""Check C1 source packet binding against immutable original source bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave-dir", type=Path, required=True)
    args = parser.parse_args()
    roster_path = args.wave_dir / "c1_review_roster.jsonl"
    manifest_path = args.wave_dir / "c1_review_manifest.json"
    rows = [json.loads(line) for line in roster_path.read_text().splitlines() if line.strip()]
    errors = []
    source_ids = []
    for row in rows:
        if row["candidate_count"] != 3 or len(row["members"]) != 3:
            errors.append(f"invalid candidate count: {row['c1_review_id']}")
        for member in row["members"]:
            path = Path(member["absolute_path"])
            if not path.is_file():
                errors.append(f"missing original: {member['source_id']}")
                continue
            if sha256_file(path) != member["sha256"]:
                errors.append(f"source hash drift: {member['source_id']}")
            source_ids.append(member["source_id"])
    result = {
        "status": "PASS" if not errors else "FAIL",
        "packets": len(rows),
        "sources": len(source_ids),
        "unique_sources": len(set(source_ids)),
        "errors": errors,
        "claim_boundary": "This audit checks only C1 source binding; it does not assess card quality, operational contrast, strict-gold validity, or retrieval.",
    }
    (args.wave_dir / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
