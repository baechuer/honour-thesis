#!/usr/bin/env python3
"""Build provenance-correct local I1 and exact-source I2 representations."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    selector_counts,
    serialize_i1,
    sha256_file,
    sha256_text,
    verify_frozen_manifest,
    version_root,
    write_json_new,
    write_jsonl_new,
)


SERIALIZER_VERSION = "rq2b-representation-serializer-v1"


def representation_row(
    source: dict[str, Any],
    representation: str,
    selector_text: str,
) -> dict[str, Any]:
    return {
        "schema_version": "rq2b-representation-row-v1",
        "serializer_version": SERIALIZER_VERSION,
        "representation": representation,
        "source_row_index": source["source_row_index"],
        "skill_id": source["skill_id"],
        "family": source["family"],
        "source_policy": source["source_policy"],
        "source_path": source["source_path"],
        "source_sha256": source["source_sha256"],
        "source_name_sha256": source["source_name_sha256"],
        "source_description_sha256": source["source_description_sha256"],
        "selector_text": selector_text,
        "selector_text_sha256": sha256_text(selector_text),
        "selector_visible_counts": selector_counts(selector_text),
    }


def verify_rows(
    root: Path,
    sources: list[dict[str, Any]],
    i1_rows: list[dict[str, Any]],
    i2_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    require(len(sources) == 2433, "Frozen source manifest must contain 2,433 rows")
    require(len(i1_rows) == len(sources), "I1 row count mismatch")
    require(len(i2_rows) == len(sources), "I2 row count mismatch")
    i1_ids: set[str] = set()
    i2_ids: set[str] = set()
    total_source_bytes = 0
    total_i1_bytes = 0
    for source, i1, i2 in zip(sources, i1_rows, i2_rows, strict=True):
        index = source["source_row_index"]
        skill_id = source["skill_id"]
        require(i1["source_row_index"] == index, f"I1 row-index mismatch: {skill_id}")
        require(i2["source_row_index"] == index, f"I2 row-index mismatch: {skill_id}")
        require(i1["skill_id"] == skill_id, f"I1 identity mismatch: {skill_id}")
        require(i2["skill_id"] == skill_id, f"I2 identity mismatch: {skill_id}")
        require(skill_id not in i1_ids, f"Duplicate I1 skill ID: {skill_id}")
        require(skill_id not in i2_ids, f"Duplicate I2 skill ID: {skill_id}")
        i1_ids.add(skill_id)
        i2_ids.add(skill_id)

        source_path = root / source["source_path"]
        source_bytes = source_path.read_bytes()
        source_text = source_bytes.decode("utf-8")
        require(source_text.encode("utf-8") == source_bytes, f"Non-roundtrip UTF-8: {skill_id}")
        require(sha256_file(source_path) == source["source_sha256"], f"Source drift: {skill_id}")
        expected_i1 = serialize_i1(source["source_name"], source["source_description"])
        require(i1["selector_text"] == expected_i1, f"I1 serialization mismatch: {skill_id}")
        require(i2["selector_text"] == source_text, f"I2 is not the exact source: {skill_id}")
        require(i2["selector_text_sha256"] == source["source_sha256"], f"I2 byte hash mismatch: {skill_id}")
        require(i1["representation"] == "i1-discovery", f"I1 label mismatch: {skill_id}")
        require(i2["representation"] == "i2-original", f"I2 label mismatch: {skill_id}")
        total_source_bytes += len(source_bytes)
        total_i1_bytes += len(expected_i1.encode("utf-8"))
    require(i1_ids == i2_ids, "I1 and I2 identity sets differ")
    return {
        "skills": len(sources),
        "total_i1_utf8_bytes": total_i1_bytes,
        "total_i2_utf8_bytes": total_source_bytes,
        "i2_exact_source_rows": len(sources),
    }


def build(root: Path) -> dict[str, Any]:
    frozen = verify_frozen_manifest(root)
    frozen_root = version_root(root)
    source_manifest_path = frozen_root / "source_manifest.jsonl"
    sources = read_jsonl(source_manifest_path)
    output_root = frozen_root / "representations"
    staging_root = frozen_root / ".representations.staging"
    require(not output_root.exists(), f"Representation root already exists: {output_root}")
    require(not staging_root.exists(), f"Stale representation staging root: {staging_root}")
    staging_root.mkdir(parents=True, exist_ok=False)

    i1_rows: list[dict[str, Any]] = []
    i2_rows: list[dict[str, Any]] = []
    source_read_decode_seconds = 0.0
    i1_serialization_seconds = 0.0
    i2_serialization_seconds = 0.0
    for source in sources:
        source_started = time.perf_counter()
        source_path = root / source["source_path"]
        source_bytes = source_path.read_bytes()
        require(sha256_file(source_path) == source["source_sha256"], f"Source drift: {source['skill_id']}")
        source_text = source_bytes.decode("utf-8")
        require(source_text.encode("utf-8") == source_bytes, f"Non-roundtrip UTF-8: {source['skill_id']}")
        source_read_decode_seconds += time.perf_counter() - source_started
        i1_started = time.perf_counter()
        i1_text = serialize_i1(source["source_name"], source["source_description"])
        i1_rows.append(representation_row(source, "i1-discovery", i1_text))
        i1_serialization_seconds += time.perf_counter() - i1_started
        i2_started = time.perf_counter()
        i2_rows.append(representation_row(source, "i2-original", source_text))
        i2_serialization_seconds += time.perf_counter() - i2_started

    summary = verify_rows(root, sources, i1_rows, i2_rows)
    i1_path = staging_root / "i1-discovery.jsonl"
    i2_path = staging_root / "i2-original.jsonl"
    write_jsonl_new(i1_path, i1_rows)
    write_jsonl_new(i2_path, i2_rows)
    artifacts = {
        "i1-discovery": {
            "path": relative(output_root / i1_path.name, root),
            "sha256": sha256_file(i1_path),
            "rows": len(i1_rows),
            "utf8_bytes": i1_path.stat().st_size,
        },
        "i2-original": {
            "path": relative(output_root / i2_path.name, root),
            "sha256": sha256_file(i2_path),
            "rows": len(i2_rows),
            "utf8_bytes": i2_path.stat().st_size,
        },
    }
    manifest = {
        "schema_version": "rq2b-representation-manifest-v1",
        "version_id": VERSION_ID,
        "state": "local_i1_i2_built_no_scientific_run",
        "serializer_version": SERIALIZER_VERSION,
        "network_calls": 0,
        "source_manifest": {
            "path": relative(source_manifest_path, root),
            "sha256": sha256_file(source_manifest_path),
        },
        "frozen_manifest_sha256": sha256_file(frozen_root / "manifest.json"),
        "builder_sha256": sha256_file(Path(__file__).resolve()),
        "common_module_sha256": sha256_file(Path(__file__).with_name("rq2b_common.py")),
        "timing": {
            "source_read_decode_seconds": source_read_decode_seconds,
            "i1_serialization_seconds": i1_serialization_seconds,
            "i2_serialization_seconds": i2_serialization_seconds,
        },
        "summary": summary,
        "artifacts": artifacts,
        "exclusions": [
            "gold labels",
            "benchmark strata",
            "benchmark family labels",
            "normalised public wrappers",
            "generated dependency profiles",
            "generated tags",
        ],
    }
    write_json_new(staging_root / "manifest.json", manifest)
    staging_root.replace(output_root)
    return verify(root)


def verify(root: Path) -> dict[str, Any]:
    frozen = verify_frozen_manifest(root)
    frozen_root = version_root(root)
    output_root = frozen_root / "representations"
    manifest_path = output_root / "manifest.json"
    require(manifest_path.exists(), f"Representation manifest missing: {manifest_path}")
    manifest = read_json(manifest_path)
    require(manifest.get("schema_version") == "rq2b-representation-manifest-v1", "Representation manifest schema mismatch")
    require(manifest.get("version_id") == VERSION_ID, "Representation version mismatch")
    require(manifest.get("state") == "local_i1_i2_built_no_scientific_run", "Unsafe representation state")
    require(manifest.get("network_calls") == 0, "Representation build used network")
    require(
        manifest.get("builder_sha256") == sha256_file(Path(__file__).resolve()),
        "Representation builder provenance is stale",
    )
    require(
        manifest.get("common_module_sha256")
        == sha256_file(Path(__file__).with_name("rq2b_common.py")),
        "Representation common-module provenance is stale",
    )
    timing = manifest.get("timing", {})
    require(
        set(timing)
        == {
            "source_read_decode_seconds",
            "i1_serialization_seconds",
            "i2_serialization_seconds",
        },
        "Representation timing schema mismatch",
    )
    require(
        all(isinstance(value, (int, float)) and value >= 0.0 for value in timing.values()),
        "Representation timing value mismatch",
    )
    source_manifest_path = frozen_root / "source_manifest.jsonl"
    require(manifest["source_manifest"]["sha256"] == sha256_file(source_manifest_path), "Source manifest drift")
    sources = read_jsonl(source_manifest_path)
    rows_by_name: dict[str, list[dict[str, Any]]] = {}
    for name, artifact in manifest["artifacts"].items():
        path = root / artifact["path"]
        require(path.exists(), f"Representation artifact missing: {name}")
        require(sha256_file(path) == artifact["sha256"], f"Representation drift: {name}")
        rows = read_jsonl(path)
        require(len(rows) == artifact["rows"], f"Representation row count drift: {name}")
        rows_by_name[name] = rows
    summary = verify_rows(
        root,
        sources,
        rows_by_name["i1-discovery"],
        rows_by_name["i2-original"],
    )
    require(summary == manifest["summary"], "Representation summary drift")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = verify(root) if args.verify_only else build(root)
    print(
        json.dumps(
            {
                "version_id": manifest["version_id"],
                "state": manifest["state"],
                "summary": manifest["summary"],
                "network_calls": manifest["network_calls"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
