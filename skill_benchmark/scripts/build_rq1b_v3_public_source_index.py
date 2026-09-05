#!/usr/bin/env python3
"""Create a local structural census and FTS discovery index for the frozen RQ1b v3 source frame."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import statistics
import time
from collections import Counter
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-public-source-index-builder-v1"
BODY_INDEX_CHAR_LIMIT = 16_000
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FRONT_MATTER_NAME_RE = re.compile(r"^name\s*:\s*[\"']?(.+?)[\"']?\s*$", re.IGNORECASE)

FIELD_HEADING_PATTERNS = {
    "use_condition": ("use when", "when to use", "use cases", "use case", "purpose", "applicability"),
    "input_precondition": ("input", "precondition", "prerequisite", "before you begin"),
    "output_artifact": ("output", "artifact", "deliverable", "result"),
    "workflow_procedure": ("workflow", "procedure", "steps", "process", "instructions"),
    "success_verification": ("success", "verification", "validation", "acceptance", "testing"),
    "boundary_not_for": ("boundary", "not for", "limitations", "guardrails", "scope", "exclusions"),
    "dependency_resource": ("dependency", "dependencies", "resources", "tools", "environment", "permissions"),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def normalise_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold().strip("`*_:- "))


def extract_title_and_headings(text: str, fallback: str) -> tuple[str, list[str]]:
    lines = text.splitlines()
    title = None
    headings: list[str] = []
    in_front_matter = bool(lines and lines[0].strip() == "---")
    for index, line in enumerate(lines[:200]):
        if in_front_matter:
            if index and line.strip() == "---":
                in_front_matter = False
                continue
            match = FRONT_MATTER_NAME_RE.match(line.strip())
            if match and not title:
                title = match.group(1).strip()
            continue
        match = HEADING_RE.match(line)
        if match:
            heading = match.group(1).strip()
            headings.append(heading)
            if line.startswith("# ") and not title:
                title = heading
    return title or fallback, headings


def explicit_field_markers(headings: list[str]) -> dict[str, bool]:
    lowered = [normalise_heading(heading) for heading in headings]
    return {
        field: any(any(pattern in heading for pattern in patterns) for heading in lowered)
        for field, patterns in FIELD_HEADING_PATTERNS.items()
    }


def build(source_frame_dir: Path, output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite source index: {output_dir}")
    certificate = json.loads((source_frame_dir / "SOURCE_FRAME_FREEZE_CERTIFICATE.json").read_text())
    if certificate.get("status") != "RQ1B_V3_PUBLIC_SOURCE_FRAME_FROZEN_LOCAL_ONLY":
        raise ValueError("source frame must be frozen before indexing")
    canonical_path = source_frame_dir / "canonical_sources.jsonl"
    canonical = read_jsonl(canonical_path)
    if len(canonical) != certificate["counts"]["canonical_artifacts"]:
        raise ValueError("frozen source-frame count mismatch")

    staging = output_dir.parent / f".{output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    database_path = staging / "source_discovery.sqlite"
    feature_path = staging / "source_features.jsonl"
    started = time.perf_counter()
    heading_counts: Counter[str] = Counter()
    marker_counts: Counter[str] = Counter()
    title_count = 0
    token_counts: list[int] = []
    features: list[dict[str, Any]] = []
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA journal_mode=OFF")
        connection.execute("PRAGMA synchronous=OFF")
        connection.execute(
            "CREATE TABLE source_metadata (source_id TEXT PRIMARY KEY, sha256 TEXT UNIQUE, source_root TEXT, origin_key TEXT, relative_path TEXT, absolute_path TEXT, title TEXT, headings_json TEXT, byte_count INTEGER, lexical_token_count INTEGER, discovery_index_char_count INTEGER)"
        )
        connection.execute("CREATE VIRTUAL TABLE source_fts USING fts5(source_id UNINDEXED, title, headings, body)")
        for index, row in enumerate(canonical, start=1):
            source = row["canonical"]
            path = Path(source["absolute_path"])
            text = path.read_text(encoding="utf-8")
            fallback = Path(source["relative_path"]).parent.parent.name
            title, headings = extract_title_and_headings(text, fallback)
            marker_map = explicit_field_markers(headings)
            normalised_headings = [normalise_heading(heading) for heading in headings]
            lexical_tokens = len(TOKEN_RE.findall(text))
            index_body = text[:BODY_INDEX_CHAR_LIMIT]
            feature = {
                "source_id": row["source_id"],
                "sha256": row["sha256"],
                "source_root": source["source_root"],
                "origin_key": source["origin_key"],
                "relative_path": source["relative_path"],
                "title": title,
                "headings": headings,
                "explicit_heading_markers": marker_map,
                "byte_count": row["byte_count"],
                "lexical_token_count": lexical_tokens,
                "discovery_index_char_count": len(index_body),
            }
            features.append(feature)
            heading_counts.update(normalised_headings)
            marker_counts.update(field for field, present in marker_map.items() if present)
            title_count += int(title != fallback)
            token_counts.append(lexical_tokens)
            connection.execute(
                "INSERT INTO source_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row["source_id"], row["sha256"], source["source_root"], source["origin_key"], source["relative_path"], source["absolute_path"], title, json.dumps(headings), row["byte_count"], lexical_tokens, len(index_body)),
            )
            connection.execute("INSERT INTO source_fts VALUES (?, ?, ?, ?)", (row["source_id"], title, "\n".join(headings), index_body))
            if index % 500 == 0 or index == len(canonical):
                connection.commit()
                print(f"SOURCE_INDEX_PROGRESS indexed={index}/{len(canonical)}", flush=True)
        connection.commit()
    finally:
        connection.close()
    feature_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in features))
    census = {
        "status": "RQ1B_V3_STRUCTURAL_CENSUS_LOCAL_ONLY",
        "builder_version": VERSION,
        "source_frame_certificate_sha256": sha256_file(source_frame_dir / "SOURCE_FRAME_FREEZE_CERTIFICATE.json"),
        "canonical_artifact_count": len(canonical),
        "artifact_title_count": title_count,
        "explicit_heading_marker_counts": dict(sorted(marker_counts.items())),
        "top_normalised_headings": heading_counts.most_common(100),
        "lexical_token_count": {
            "min": min(token_counts),
            "median": statistics.median(token_counts),
            "mean": statistics.mean(token_counts),
            "max": max(token_counts),
        },
        "fts_body_character_limit": BODY_INDEX_CHAR_LIMIT,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": "Heading markers are deterministic structural proxies only. This census is not a semantic field-prevalence estimate or a cluster/selector result.",
        "elapsed_seconds": time.perf_counter() - started,
    }
    (staging / "structural_census.json").write_text(json.dumps(census, indent=2, sort_keys=True) + "\n")
    census["artifacts"] = {
        "source_features.jsonl": sha256_file(feature_path),
        "source_discovery.sqlite": sha256_file(database_path),
    }
    (staging / "structural_census.json").write_text(json.dumps(census, indent=2, sort_keys=True) + "\n")
    staging.replace(output_dir)
    return census


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-frame-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.source_frame_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
