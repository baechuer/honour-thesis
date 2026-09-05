#!/usr/bin/env python3
"""Record exact raw-byte integrity and the prefreeze CRLF count correction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    version_root,
    write_json_new,
)


def compute(root: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    frozen_root = version_root(root)
    sources = read_jsonl(frozen_root / "source_manifest.jsonl")
    representation_manifest = read_json(frozen_root / "representations" / "manifest.json")
    i2_path = root / representation_manifest["artifacts"]["i2-original"]["path"]
    i2_rows = read_jsonl(i2_path)
    corrections: list[dict[str, Any]] = []
    raw_total = 0
    prefreeze_total = 0
    for source, i2 in zip(sources, i2_rows, strict=True):
        path = root / source["source_path"]
        raw = path.read_bytes()
        raw_total += len(raw)
        prefreeze_bytes = int(source["source_utf8_bytes"])
        prefreeze_total += prefreeze_bytes
        require(sha256_file(path) == source["source_sha256"], f"Source drift: {source['skill_id']}")
        require(i2["selector_text"].encode("utf-8") == raw, f"I2 byte mismatch: {source['skill_id']}")
        require(i2["selector_text_sha256"] == source["source_sha256"], f"I2 hash mismatch: {source['skill_id']}")
        require(i2["selector_visible_counts"]["utf8_bytes"] == len(raw), f"I2 byte count mismatch: {source['skill_id']}")
        if prefreeze_bytes != len(raw):
            corrections.append(
                {
                    "source_row_index": source["source_row_index"],
                    "skill_id": source["skill_id"],
                    "source_path": source["source_path"],
                    "source_sha256": source["source_sha256"],
                    "prefreeze_decoded_utf8_bytes": prefreeze_bytes,
                    "authoritative_raw_utf8_bytes": len(raw),
                    "byte_delta": len(raw) - prefreeze_bytes,
                    "crlf_sequences": raw.count(b"\r\n"),
                    "scientific_text_changed": False,
                }
            )
    return {
        "schema_version": "rq2b-exact-source-byte-integrity-v1",
        "version_id": VERSION_ID,
        "state": "provenance_metadata_correction_no_scientific_effect",
        "network_calls": 0,
        "source_rows": len(sources),
        "exact_i2_rows": len(i2_rows),
        "prefreeze_decoded_utf8_bytes": prefreeze_total,
        "authoritative_raw_utf8_bytes": raw_total,
        "total_byte_delta": raw_total - prefreeze_total,
        "affected_rows": len(corrections),
        "corrections": corrections,
        "authority_rule": (
            "source_sha256 and exact raw bytes are authoritative; the copied "
            "prefreeze source_utf8_bytes field used universal-newline decoded text"
        ),
        "i2_representation": {
            "path": relative(i2_path, root),
            "sha256": sha256_file(i2_path),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    output_path = version_root(root) / "exact_source_byte_integrity.json"
    report = compute(root)
    if args.verify_only:
        require(output_path.exists(), f"Exact-byte integrity report missing: {output_path}")
        require(read_json(output_path) == report, "Exact-byte integrity report drift")
    else:
        write_json_new(output_path, report)
    print(
        json.dumps(
            {
                "state": report["state"],
                "source_rows": report["source_rows"],
                "affected_rows": report["affected_rows"],
                "total_byte_delta": report["total_byte_delta"],
                "authoritative_raw_utf8_bytes": report["authoritative_raw_utf8_bytes"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
