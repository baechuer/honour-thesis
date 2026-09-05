#!/usr/bin/env python3
"""Check D1-derived C1 packet binding against immutable source bytes."""

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
    rows = [json.loads(line) for line in (args.wave_dir / "c1_review_roster.jsonl").read_text().splitlines() if line.strip()]
    errors, source_ids = [], []
    for row in rows:
        if row["candidate_count"] not in {3, 4} or len(row["members"]) != row["candidate_count"]:
            errors.append(f"invalid candidate count: {row['c1_review_id']}")
        for member in row["members"]:
            path = Path(member["absolute_path"])
            if not path.is_file() or sha256_file(path) != member["sha256"]:
                errors.append(f"source binding failure: {member['source_id']}")
            source_ids.append(member["source_id"])
    result = {"status": "PASS" if not errors else "FAIL", "packets": len(rows), "sources": len(source_ids), "unique_sources": len(set(source_ids)), "source_reuse_count": len(source_ids) - len(set(source_ids)), "errors": errors, "claim_boundary": "This audit checks only C1 source binding; it does not assess card quality, operational contrast, strict-gold validity, or retrieval."}
    (args.wave_dir / "C1_SOURCE_EVIDENCE_WAVE_AUDIT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
