#!/usr/bin/env python3
"""Summarise deterministic heading-marker structure in a frozen RQ1b V3 frame."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


VERSION = "rq1b-v3-structural-marker-summary-v3"
FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
BOUNDARY = (
    "This is a deterministic analysis of explicit heading markers in a frozen "
    "local public-source frame. It does not estimate semantic field prevalence, "
    "induce the seven-field taxonomy, establish recoverability from prose, or "
    "create a cluster, prompt, gold label, selector input, metric, or retrieval result."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def percent(count: int, total: int) -> float:
    return round(100 * count / total, 3) if total else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--source-frame-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError(f"refusing to overwrite output: {args.output_dir}")

    census = json.loads(args.census.read_text())
    source_frame_manifest = json.loads(args.source_frame_manifest.read_text())
    if census.get("status") != "RQ1B_V3_STRUCTURAL_CENSUS_LOCAL_ONLY":
        raise ValueError("features must come from the frozen local structural census")
    rows = read_jsonl(args.features)
    total = len(rows)
    if total != census.get("canonical_artifact_count"):
        raise ValueError("feature row count disagrees with structural census")
    if total != source_frame_manifest.get("canonical_artifact_count"):
        raise ValueError("feature row count disagrees with source-frame manifest")

    field_counts = Counter()
    field_origins: dict[str, set[str]] = {field: set() for field in FIELDS}
    field_roots: dict[str, set[str]] = {field: set() for field in FIELDS}
    pair_counts = Counter()
    marker_cardinality = Counter()
    combination_counts = Counter()
    all_origins: set[str] = set()
    all_roots: set[str] = set()
    for row in rows:
        marker_map = row["explicit_heading_markers"]
        present = tuple(field for field in FIELDS if marker_map.get(field) is True)
        marker_cardinality[len(present)] += 1
        combination_counts["|".join(present) if present else "NO_MARKER"] += 1
        origin_identity = f"{row['source_root']}:{row['origin_key']}"
        all_origins.add(origin_identity)
        all_roots.add(row["source_root"])
        for field in present:
            field_counts[field] += 1
            field_origins[field].add(origin_identity)
            field_roots[field].add(row["source_root"])
        for left, right in combinations(present, 2):
            pair_counts[(left, right)] += 1

    field_summary = {
        field: {
            "marker_artifacts": field_counts[field],
            "marker_artifact_percent": percent(field_counts[field], total),
            "origins_with_marker": len(field_origins[field]),
            "source_roots_with_marker": len(field_roots[field]),
        }
        for field in FIELDS
    }
    pair_summary = []
    for left, right in combinations(FIELDS, 2):
        joint = pair_counts[(left, right)]
        union = field_counts[left] + field_counts[right] - joint
        pair_summary.append({
            "left": left,
            "right": right,
            "joint_marker_artifacts": joint,
            "joint_marker_percent": percent(joint, total),
            "jaccard_of_marker_sets": round(joint / union, 4) if union else 0.0,
        })
    pair_summary.sort(key=lambda item: (-item["joint_marker_artifacts"], item["left"], item["right"]))
    top_combinations = [
        {"marker_combination": name, "artifacts": count, "percent": percent(count, total)}
        for name, count in combination_counts.most_common(25)
    ]

    result = {
        "status": "RQ1B_V3_STRUCTURAL_MARKER_SUMMARY_LOCAL_ONLY",
        "version": VERSION,
        "feature_input_sha256": sha256_file(args.features),
        "census_input_sha256": sha256_file(args.census),
        "source_frame_manifest_sha256": sha256_file(args.source_frame_manifest),
        "canonical_artifacts": total,
        "canonical_origin_identities": len(all_origins),
        "raw_source_origin_path_identities": source_frame_manifest["source_origin_count"],
        "source_roots": len(all_roots),
        "marker_cardinality": {
            str(cardinality): {"artifacts": marker_cardinality[cardinality], "percent": percent(marker_cardinality[cardinality], total)}
            for cardinality in range(len(FIELDS) + 1)
        },
        "field_summary": field_summary,
        "pair_marker_summary": pair_summary,
        "top_marker_combinations": top_combinations,
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": BOUNDARY,
    }
    args.output_dir.mkdir(parents=True)
    json_path = args.output_dir / "structural_marker_summary.json"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    lines = [
        "# RQ1b V3 Structural Heading-Marker Summary",
        "",
        "Status: `LOCAL ONLY / DETERMINISTIC HEADING-MARKER DESCRIPTION / NOT SEMANTIC PREVALENCE`",
        "",
        f"- Frozen canonical artifacts: {total:,}",
        f"- Canonical artifact origin identities: {len(all_origins):,}",
        f"- Raw source-path origin identities: {source_frame_manifest['source_origin_count']:,}",
        f"- Source roots: {len(all_roots):,}",
        "- No network calls or text transmission.",
        "",
        "The raw source-path total retains origins visible only through exact duplicate aliases; marker coverage is calculated only over canonical content identities.",
        "",
        "## Boundary",
        "",
        BOUNDARY,
        "",
        "## Individual Markers",
        "",
        "| Marker | Artifacts | Share | Origins | Source roots |",
        "|---|---:|---:|---:|---:|",
    ]
    for field in FIELDS:
        item = field_summary[field]
        lines.append(
            f"| `{field}` | {item['marker_artifacts']:,} | {item['marker_artifact_percent']:.3f}% | "
            f"{item['origins_with_marker']:,} | {item['source_roots_with_marker']:,} |"
        )
    lines.extend([
        "",
        "## Marker Cardinality",
        "",
        "| Explicit markers per artifact | Artifacts | Share |",
        "|---:|---:|---:|",
    ])
    for cardinality in range(len(FIELDS) + 1):
        item = result["marker_cardinality"][str(cardinality)]
        lines.append(f"| {cardinality} | {item['artifacts']:,} | {item['percent']:.3f}% |")
    lines.extend([
        "",
        "## Strongest Pairwise Marker Co-occurrences",
        "",
        "| Pair | Joint artifacts | Share | Marker-set Jaccard |",
        "|---|---:|---:|---:|",
    ])
    for item in pair_summary[:10]:
        lines.append(
            f"| `{item['left']}` + `{item['right']}` | {item['joint_marker_artifacts']:,} | "
            f"{item['joint_marker_percent']:.3f}% | {item['jaccard_of_marker_sets']:.4f} |"
        )
    markdown_path = args.output_dir / "STRUCTURAL_MARKER_SUMMARY.md"
    markdown_path.write_text("\n".join(lines) + "\n")
    result["artifacts"] = {
        "structural_marker_summary.json": sha256_file(json_path),
        "STRUCTURAL_MARKER_SUMMARY.md": sha256_file(markdown_path),
    }
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
