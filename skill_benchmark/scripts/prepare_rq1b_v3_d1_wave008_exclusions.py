#!/usr/bin/env python3
"""Build the local source-ID exclusion list for RQ1b V3 D1 Wave 008.

This is provenance preparation only. It neither ranks candidates nor makes a
semantic, prompt, label, field, selector, or retrieval decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior-manifest", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        raise SystemExit("refusing_to_overwrite_existing_wave008_exclusion_list")
    if any(not path.is_file() for path in args.prior_manifest):
        raise SystemExit("missing_prior_d1_manifest")

    ids: set[str] = set()
    membership: dict[str, list[str]] = {}
    for manifest in args.prior_manifest:
        for row in read_jsonl(manifest):
            for member in row.get("members", []):
                source_id = str(member["source_id"])
                ids.add(source_id)
                membership.setdefault(source_id, []).append(str(manifest))

    payload = {
        "status": "RQ1B_V3_D1_WAVE008_EXCLUSIONS_LOCAL_ONLY",
        "claim_boundary": (
            "This list prevents prior D1 source reuse. It does not determine semantic similarity, "
            "cluster validity, prompt suitability, labels, field effects, selector inputs or retrieval."
        ),
        "prior_manifest_sha256": {str(path): sha256_file(path) for path in args.prior_manifest},
        "excluded_source_count": len(ids),
        "excluded_source_ids": sorted(ids),
        "source_membership": {source_id: sorted(paths) for source_id, paths in sorted(membership.items())},
        "network_calls": 0,
        "texts_transmitted": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "excluded_source_count": payload["excluded_source_count"],
        "output_sha256": sha256_file(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
