#!/usr/bin/env python3
"""Build a local-only, hash-deduplicated RQ1b v3 public skill source frame."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-public-source-frame-builder-v1"


def sha256_and_size(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def source_record(root_name: str, root: Path, path: Path) -> dict[str, str]:
    relative = path.relative_to(root)
    parts = relative.parts
    # Staged-source roots are the provenance units; imported background slugs are too.
    origin_key = parts[0] if parts else "."
    return {
        "source_root": root_name,
        "origin_key": origin_key,
        "relative_path": relative.as_posix(),
        "absolute_path": str(path.resolve()),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def build(source_roots: dict[str, Path], output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite source frame: {output_dir}")
    for name, root in source_roots.items():
        if not root.is_dir():
            raise ValueError(f"source root unavailable: {name}={root}")
    candidates: list[tuple[str, Path, Path]] = []
    for name, root in source_roots.items():
        candidates.extend((name, root, path) for path in sorted(root.rglob("SKILL.original.md")) if path.is_file())
    if not candidates:
        raise ValueError("no original public skill artifacts found")

    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    invalid_utf8: list[dict[str, Any]] = []
    started = time.perf_counter()
    for index, (root_name, root, path) in enumerate(candidates, start=1):
        sha256, byte_count = sha256_and_size(path)
        record = source_record(root_name, root, path)
        record.update({"sha256": sha256, "byte_count": byte_count})
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            invalid_utf8.append(record)
            continue
        by_hash[sha256].append(record)
        if index % 500 == 0 or index == len(candidates):
            print(f"SOURCE_FRAME_PROGRESS scanned={index}/{len(candidates)} canonical_so_far={len(by_hash)}", flush=True)

    canonical_rows: list[dict[str, Any]] = []
    alias_rows: list[dict[str, Any]] = []
    for ordinal, sha256 in enumerate(sorted(by_hash), start=1):
        aliases = sorted(by_hash[sha256], key=lambda row: (row["source_root"], row["origin_key"], row["relative_path"]))
        canonical = aliases[0]
        source_id = f"RQ1B-V3-SRC-{ordinal:06d}"
        canonical_rows.append(
            {
                "source_id": source_id,
                "sha256": sha256,
                "byte_count": canonical["byte_count"],
                "canonical": canonical,
                "alias_count": len(aliases),
                "origin_roots": sorted({f"{row['source_root']}:{row['origin_key']}" for row in aliases}),
                "source_status": "CANONICAL_PUBLIC_ORIGINAL_LOCAL_ONLY",
            }
        )
        alias_rows.extend({"source_id": source_id, "is_canonical": alias == canonical, **alias} for alias in aliases)

    root_counts = Counter(row["source_root"] for aliases in by_hash.values() for row in aliases)
    origin_counts = Counter(f"{row['source_root']}:{row['origin_key']}" for aliases in by_hash.values() for row in aliases)
    manifest = {
        "status": "RQ1B_V3_PUBLIC_SOURCE_FRAME_LOCAL_ONLY_UNFROZEN",
        "builder_version": VERSION,
        "network_calls": 0,
        "texts_transmitted": 0,
        "source_roots": {name: str(root.resolve()) for name, root in source_roots.items()},
        "input_path_count": len(candidates),
        "invalid_utf8_path_count": len(invalid_utf8),
        "canonical_artifact_count": len(canonical_rows),
        "duplicate_alias_path_count": len(alias_rows) - len(canonical_rows),
        "canonical_total_bytes": sum(row["byte_count"] for row in canonical_rows),
        "input_root_path_counts": dict(sorted(root_counts.items())),
        "source_origin_count": len(origin_counts),
        "source_origin_path_counts": dict(sorted(origin_counts.items())),
        "elapsed_seconds": time.perf_counter() - started,
        "claim_boundary": "This is a local source-frame inventory. It is not a field-prevalence estimate, cluster result, selector run, or external-text transfer.",
    }

    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    try:
        write_jsonl(staging / "canonical_sources.jsonl", canonical_rows)
        write_jsonl(staging / "source_aliases.jsonl", alias_rows)
        write_jsonl(staging / "invalid_utf8_exclusions.jsonl", invalid_utf8)
        manifest["artifacts"] = {
            name: hashlib.sha256((staging / name).read_bytes()).hexdigest()
            for name in ("canonical_sources.jsonl", "source_aliases.jsonl", "invalid_utf8_exclusions.jsonl")
        }
        (staging / "source_frame_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        staging.replace(output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cross-source-root", type=Path, required=True)
    parser.add_argument("--naturalistic-root", type=Path, required=True)
    parser.add_argument("--imported-background-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    roots = {
        "cross_source_staged": args.cross_source_root,
        "naturalistic_staged": args.naturalistic_root,
        "imported_background": args.imported_background_root,
    }
    print(json.dumps(build(roots, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
