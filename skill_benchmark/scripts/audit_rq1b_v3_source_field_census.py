#!/usr/bin/env python3
"""Census surface cues for the seven RQ1 fields in the frozen V3 source frame.

This intentionally describes literal, deterministic source evidence.  It does
not label the full semantic meaning of every public artifact and it is not a
retrieval experiment.  Its purpose is to replace the historical 460-artifact
supporting audit with a provenance-bound census of the public originals from
which the current V3 discovery work was filtered.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VERSION = "rq1b-v3-source-field-census-v1"
FROZEN_STATUS = "RQ1B_V3_PUBLIC_SOURCE_FRAME_FROZEN_LOCAL_ONLY"
FIELDS = (
    "use_condition",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "success_verification",
    "boundary_not_for",
    "dependency_resource",
)
# BODY_HEADING_RE removes headings from prose-cue scanning.  The deliberately
# stricter STRUCTURAL_HEADING_RE below is retained separately to reproduce the
# existing frozen V3 structural index exactly.
BODY_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
STRUCTURAL_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$")


@dataclass(frozen=True)
class FieldSpec:
    label: str
    metadata_keys: tuple[str, ...]
    metadata_patterns: tuple[str, ...]
    heading_patterns: tuple[str, ...]
    prose_patterns: tuple[str, ...]


# Heading patterns intentionally match build_rq1b_v3_public_source_index.py so
# this census can reconcile its structural layer with the frozen summary.
FIELD_SPECS: dict[str, FieldSpec] = {
    "use_condition": FieldSpec(
        label="Use condition",
        metadata_keys=("trigger", "triggers", "when_to_use", "use_when", "use_case", "use_cases", "applicability"),
        metadata_patterns=(
            r"\buse (?:this )?skill (?:when|for)\b",
            r"\bshould be used (?:when|for|to)\b",
            r"\bwhen (?:the user|you) (?:need|needs|want|wants|ask|asks|are|is)\b",
            r"\b(?:ideal|best|intended|designed) for\b",
        ),
        heading_patterns=("use when", "when to use", "use cases", "use case", "purpose", "applicability"),
        prose_patterns=(
            r"\buse (?:this )?skill (?:when|for)\b",
            r"\bshould be used (?:when|for|to)\b",
            r"\bwhen (?:the user|you) (?:need|needs|want|wants|ask|asks|are|is)\b",
            r"\b(?:ideal|best|intended|designed) for\b",
        ),
    ),
    "input_precondition": FieldSpec(
        label="Input / precondition",
        metadata_keys=("input", "inputs", "precondition", "preconditions", "requires", "requirements", "prerequisites"),
        metadata_patterns=(),
        heading_patterns=("input", "precondition", "prerequisite", "before you begin"),
        prose_patterns=(
            r"\b(?:required|expected|accepted) (?:inputs?|parameters?|arguments?|files?|documents?|data)\b",
            r"\binputs?\s*(?:include|:|are|should)\b",
            r"\b(?:provide|supply|upload|pass) (?:the |a |an )?(?:file|url|path|repository|document|data|parameter|argument)\b",
            r"\b(?:pre-?requisit|precondition|before you begin)\b",
        ),
    ),
    "output_artifact": FieldSpec(
        label="Output / artifact",
        metadata_keys=("output", "outputs", "output_format", "deliverable", "deliverables", "artifact", "artifacts"),
        metadata_patterns=(),
        heading_patterns=("output", "artifact", "deliverable", "result"),
        prose_patterns=(
            r"\b(?:outputs?|deliverables?|artifacts?|returns?)\s*(?:include|:|are|should|will)\b",
            r"\b(?:produce|produces|produced|generate|generates|generated) (?:a |an |the )?(?:file|report|table|json|csv|document|plan|draft|artifact)\b",
            r"\breturn(?:s)? (?:a |an |the )?(?:file|report|table|json|csv|document|plan|draft|artifact)\b",
        ),
    ),
    "workflow_procedure": FieldSpec(
        label="Workflow / procedure",
        metadata_keys=("workflow", "steps", "procedure", "instructions", "process"),
        metadata_patterns=(),
        heading_patterns=("workflow", "procedure", "steps", "process", "instructions"),
        prose_patterns=(
            r"\bstep\s+[1-9][0-9]*\b",
            r"\bfollow (?:these|the) steps\b",
            r"\b(?:first|then|next|finally),?\s+(?:you|the skill|it)\b",
            r"\b(?:workflow|procedure) (?:is|consists of|begins|starts)\b",
        ),
    ),
    "success_verification": FieldSpec(
        label="Success / verification",
        metadata_keys=("success", "verification", "validation", "tests", "test", "acceptance", "criteria"),
        metadata_patterns=(),
        heading_patterns=("success", "verification", "validation", "acceptance", "testing"),
        prose_patterns=(
            r"\b(?:verify|validate|test|check) (?:that|whether|the)\b",
            r"\b(?:acceptance|success) criteria\b",
            r"\b(?:must|should) (?:pass|match|contain|be valid|validate)\b",
            r"\b(?:expected|desired) (?:result|output|behavio[u]?r)\b",
        ),
    ),
    "boundary_not_for": FieldSpec(
        label="Boundary / not-for",
        metadata_keys=("not_for", "limitations", "constraints", "scope", "guardrails", "rules", "exclusions"),
        metadata_patterns=(),
        heading_patterns=("boundary", "not for", "limitations", "guardrails", "scope", "exclusions"),
        prose_patterns=(
            r"\bnot for\b",
            r"\bdo not use\b",
            r"\bout of scope\b",
            r"\bnot intended (?:for|to)\b",
            r"\boutside (?:the )?scope\b",
            r"\bdoes not (?:apply|support|cover)\b",
        ),
    ),
    "dependency_resource": FieldSpec(
        label="Dependency / resource",
        metadata_keys=("dependency", "dependencies", "resources", "tools", "environment", "permissions", "mcp", "allowed-tools", "models"),
        metadata_patterns=(),
        heading_patterns=("dependency", "dependencies", "resources", "tools", "environment", "permissions"),
        prose_patterns=(
            r"\b(?:requires?|depends on|needs?) (?:an? |the )?(?:api|api key|token|credential|account|permission|access|mcp|server|tool|environment|node(?:\.js)?|python|docker)\b",
            r"\b(?:api key|access token|environment variable|mcp server|oauth|credentials?)\b",
            r"\b(?:node(?:\.js)?|python)\s*[>=~^]*\s*\d+\b",
        ),
    ),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.DOTALL)
    return (match.group(1), text[match.end() :]) if match else ("", text)


def frontmatter_values(frontmatter: str) -> dict[str, list[str]]:
    values: dict[str, list[str]] = defaultdict(list)
    for line in frontmatter.splitlines():
        match = FRONTMATTER_KEY_RE.match(line.strip())
        if match:
            values[match.group(1).casefold()].append(match.group(2).strip())
    return dict(values)


def normalise_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold().strip("`*_:- "))


def extract_prose(body: str) -> str:
    prose_lines: list[str] = []
    for line in body.splitlines():
        if not BODY_HEADING_RE.match(line):
            prose_lines.append(line)
    return "\n".join(prose_lines)


def structural_headings(text: str) -> list[str]:
    """Match build_rq1b_v3_public_source_index.py exactly.

    The existing source index reads only the first 200 source lines and does
    not accept indented ATX headings.  This narrow definition is intentional:
    heading-marker counts in this census must be directly reconcilable with
    the previously frozen structural summary.
    """
    lines = text.splitlines()
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    found: list[str] = []
    for index, line in enumerate(lines[:200]):
        if in_frontmatter:
            if index and line.strip() == "---":
                in_frontmatter = False
                continue
            continue
        match = STRUCTURAL_HEADING_RE.match(line)
        if match:
            found.append(normalise_heading(match.group(1)))
    return found


def matched_patterns(text: str, patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]


def heading_hits(headings: list[str], patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if any(pattern in heading for heading in headings)]


def analyse_field(spec: FieldSpec, metadata: dict[str, list[str]], headings: list[str], prose: str) -> dict[str, Any]:
    keyed_metadata_hits = [key for key in spec.metadata_keys if key in metadata]
    # Description is start-visible routing metadata, but it is counted as a
    # use-condition field only when it contains an activation cue, not merely
    # because a description key exists.
    description_text = "\n".join(metadata.get("description", []))
    metadata_pattern_hits = matched_patterns(description_text, spec.metadata_patterns)
    marker_hits = heading_hits(headings, spec.heading_patterns)
    prose_hits = matched_patterns(prose, spec.prose_patterns)
    has_metadata = bool(keyed_metadata_hits or metadata_pattern_hits)
    has_heading = bool(marker_hits)
    has_prose = bool(prose_hits)
    return {
        "metadata": has_metadata,
        "heading": has_heading,
        "body_prose": has_prose,
        "any": has_metadata or has_heading or has_prose,
        "metadata_key_hits": keyed_metadata_hits,
        "metadata_description_pattern_hits": metadata_pattern_hits,
        "heading_pattern_hits": marker_hits,
        "body_pattern_hits": prose_hits,
    }


def percent(value: int | float, total: int | float) -> float:
    return round(100 * value / total, 3) if total else 0.0


def analyse_source(row: dict[str, Any], workspace_root: Path, verify_sha: bool) -> dict[str, Any]:
    canonical = row["canonical"]
    source_path = Path(canonical["absolute_path"]).resolve()
    try:
        source_path.relative_to(workspace_root)
    except ValueError as exc:
        raise ValueError(f"canonical source is outside workspace: {source_path}") from exc
    if not source_path.is_file():
        raise FileNotFoundError(f"canonical source is absent: {source_path}")
    if source_path.stat().st_size != row["byte_count"]:
        raise ValueError(f"byte count mismatch: {row['source_id']}")
    if verify_sha and sha256_file(source_path) != row["sha256"]:
        raise ValueError(f"SHA-256 mismatch: {row['source_id']}")
    text = source_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    metadata = frontmatter_values(frontmatter)
    marker_headings = structural_headings(text)
    prose = extract_prose(body)
    fields = {field: analyse_field(spec, metadata, marker_headings, prose) for field, spec in FIELD_SPECS.items()}
    return {
        "source_id": row["source_id"],
        "sha256": row["sha256"],
        "source_root": canonical["source_root"],
        "origin_key": canonical["origin_key"],
        "relative_path": canonical["relative_path"],
        "byte_count": row["byte_count"],
        "frontmatter_present": bool(frontmatter),
        "metadata_name_present": "name" in metadata,
        "metadata_description_present": "description" in metadata,
        "heading_count": len(marker_headings),
        "fields": fields,
    }


def location_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    result: dict[str, Any] = {}
    for field, spec in FIELD_SPECS.items():
        metadata = sum(row["fields"][field]["metadata"] for row in rows)
        heading = sum(row["fields"][field]["heading"] for row in rows)
        prose = sum(row["fields"][field]["body_prose"] for row in rows)
        any_location = sum(row["fields"][field]["any"] for row in rows)
        metadata_only = sum(
            data["metadata"] and not data["heading"] and not data["body_prose"]
            for row in rows
            for data in [row["fields"][field]]
        )
        body_only = sum(
            not data["metadata"] and (data["heading"] or data["body_prose"])
            for row in rows
            for data in [row["fields"][field]]
        )
        metadata_and_body = sum(
            data["metadata"] and (data["heading"] or data["body_prose"])
            for row in rows
            for data in [row["fields"][field]]
        )
        result[field] = {
            "label": spec.label,
            "metadata": metadata,
            "metadata_percent": percent(metadata, total),
            "heading_marker": heading,
            "heading_marker_percent": percent(heading, total),
            "body_prose_cue": prose,
            "body_prose_cue_percent": percent(prose, total),
            "recoverable_any_location": any_location,
            "recoverable_any_location_percent": percent(any_location, total),
            "metadata_only": metadata_only,
            "body_only": body_only,
            "metadata_and_body": metadata_and_body,
        }
    return result


def origin_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_origin[f"{row['source_root']}:{row['origin_key']}"] .append(row)
    result: dict[str, Any] = {}
    for field, spec in FIELD_SPECS.items():
        rates = [sum(row["fields"][field]["any"] for row in group) / len(group) for group in by_origin.values()]
        origins_with_any = sum(rate > 0 for rate in rates)
        result[field] = {
            "label": spec.label,
            "origins_with_recoverable_cue": origins_with_any,
            "origin_coverage_percent": percent(origins_with_any, len(by_origin)),
            "unweighted_mean_within_origin_percent": round(100 * statistics.mean(rates), 3),
            "median_within_origin_percent": round(100 * statistics.median(rates), 3),
        }
    return result


def root_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_root: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_root[row["source_root"]].append(row)
    result: dict[str, Any] = {}
    for root, group in sorted(by_root.items()):
        result[root] = {
            "canonical_artifacts": len(group),
            "origin_identities": len({f"{row['source_root']}:{row['origin_key']}" for row in group}),
            "field_recoverable_any_location": {
                field: {
                    "artifacts": sum(row["fields"][field]["any"] for row in group),
                    "percent": percent(sum(row["fields"][field]["any"] for row in group), len(group)),
                }
                for field in FIELDS
            },
        }
    return result


def expected_heading_counts(structural_summary: dict[str, Any]) -> dict[str, int]:
    fields = structural_summary.get("field_summary", {})
    return {field: fields[field]["marker_artifacts"] for field in FIELDS}


def validate_heading_reconciliation(field_summary: dict[str, Any], structural_summary: dict[str, Any]) -> None:
    expected = expected_heading_counts(structural_summary)
    observed = {field: field_summary[field]["heading_marker"] for field in FIELDS}
    if observed != expected:
        raise ValueError(f"heading-marker reconciliation failed; expected={expected}, observed={observed}")


def examples(rows: list[dict[str, Any]], limit: int = 3) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in FIELDS:
        buckets: dict[str, list[dict[str, Any]]] = {"metadata": [], "heading": [], "body_prose": []}
        for row in rows:
            data = row["fields"][field]
            for bucket, key in (("metadata", "metadata"), ("heading", "heading"), ("body_prose", "body_prose")):
                if data[key] and len(buckets[bucket]) < limit:
                    buckets[bucket].append({
                        "source_id": row["source_id"],
                        "source_root": row["source_root"],
                        "origin_key": row["origin_key"],
                        "relative_path": row["relative_path"],
                        "metadata_key_hits": data["metadata_key_hits"],
                        "metadata_description_pattern_hits": data["metadata_description_pattern_hits"],
                        "heading_pattern_hits": data["heading_pattern_hits"],
                        "body_pattern_hits": data["body_pattern_hits"],
                    })
        result[field] = buckets
    return result


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# RQ1b V3 Public-Source Field Surface-Cue Census",
        "",
        "Status: `LOCAL ONLY / FROZEN-SOURCE CENSUS / DETERMINISTIC SURFACE CUES / NOT SEMANTIC PREVALENCE OR RETRIEVAL`",
        "",
        "## What This Updates",
        "",
        "This replaces the historical 460-artifact field-realism audit only as supporting recoverability context. It uses the 29,292 canonical public-original artifacts in the frozen V3 source frame from which current RQ1b V3 discovery was filtered. It does not alter a V3 cluster, prompt, label, field-removal result, or controlled RQ1 result.",
        "",
        "## Boundary",
        "",
        "A cue is a deterministic, literal source-location match. `Recoverable at any location` means that the artifact contains a field-specific metadata key, a matching body heading, or a deliberately narrow body-prose pattern. For boundary/not-for, generic behavioural directives such as bare `never` or `do not` are deliberately excluded unless they state an explicit route-out or scope limit. This is not a manual semantic annotation, a universal population estimate, a claim that the field is complete or high quality, or evidence that the field improves retrieval. Artifacts are content-deduplicated but remain clustered within public source origins; origin-weighted descriptions are reported to make that visible.",
        "",
        "`Metadata` is frontmatter only. In particular, a generic short `description` is not automatically counted as a use condition: it must contain an explicit activation phrase. `Heading marker` and `body prose cue` are body locations. Thus this table does not equate startup-visible routing metadata with body-derived use-condition evidence.",
        "",
        "## Frame and Integrity",
        "",
        f"- Canonical artifacts: {summary['canonical_artifacts']:,}",
        f"- Canonical origin identities: {summary['canonical_origin_identities']:,}",
        f"- Source roots: {summary['source_roots']}",
        f"- Every canonical source SHA-256 verified: `{str(summary['verified_source_hashes']).lower()}`",
        "- No network calls and no source text transmitted.",
        "",
        "## Location-Specific Field Cues",
        "",
        "Columns overlap: an artifact can expose the same cue in both metadata and body. `Metadata only`, `body only`, and `both` partition the recoverable artifacts.",
        "",
        "| RQ1 field | Metadata | Heading marker | Body prose cue | Recoverable at any location | Metadata only | Body only | Both |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for field in FIELDS:
        item = summary["field_location_summary"][field]
        lines.append(
            f"| {item['label']} | {item['metadata']:,} ({item['metadata_percent']:.3f}%) | "
            f"{item['heading_marker']:,} ({item['heading_marker_percent']:.3f}%) | "
            f"{item['body_prose_cue']:,} ({item['body_prose_cue_percent']:.3f}%) | "
            f"{item['recoverable_any_location']:,} ({item['recoverable_any_location_percent']:.3f}%) | "
            f"{item['metadata_only']:,} | {item['body_only']:,} | {item['metadata_and_body']:,} |"
        )
    lines.extend([
        "",
        "The heading-marker column exactly reconciles with the existing V3 structural-marker summary; it remains a structural count rather than a semantic prevalence estimate.",
        "",
        "## Origin-Aware Description",
        "",
        "`Origin coverage` is the share of public source origins with at least one artifact containing the cue. The next two columns give an equal-origin view of within-origin artifact coverage; neither is a confidence interval or global-population estimate.",
        "",
        "| RQ1 field | Origins with any cue | Origin coverage | Mean within-origin coverage | Median within-origin coverage |",
        "|---|---:|---:|---:|---:|",
    ])
    for field in FIELDS:
        item = summary["field_origin_summary"][field]
        lines.append(
            f"| {item['label']} | {item['origins_with_recoverable_cue']:,} | {item['origin_coverage_percent']:.3f}% | "
            f"{item['unweighted_mean_within_origin_percent']:.3f}% | {item['median_within_origin_percent']:.3f}% |"
        )
    lines.extend([
        "",
        "## Interpretation for RQ1 Reporting",
        "",
        "The census can support only this descriptive statement: the field types used in RQ1 are visibly recoverable in varying proportions of the frozen public-source frame, and their evidence is distributed between startup-visible metadata and document body. It cannot support ‘all public skills have these fields’, ‘these are the only common fields’, or ‘the field is useful because it is common’. The usefulness result instead comes from the controlled field-isolation and source-original removal interventions.",
        "",
        "For the literature review, the reusable-skills paper's routing metadata refers to the startup-visible metadata layer. The thesis `use condition` is a broader operational construct: in this census it can be visible in metadata, headings, or prose. The paper can therefore motivate discoverability of activation information, but not validate a body-derived field-effect claim.",
        "",
        "## Reproducibility",
        "",
        f"- Builder: `{VERSION}`",
        "- Input source paths and hashes: frozen V3 `canonical_sources.jsonl`.",
        "- The JSONL row file stores only source bindings and matched rule identifiers; it does not copy source text.",
        "- Field rules are the `FIELD_SPECS` constants in the builder script; the heading rules are shared exactly with the existing V3 structural census.",
    ])
    return "\n".join(lines) + "\n"


def build(args: argparse.Namespace) -> dict[str, Any]:
    workspace_root = args.workspace_root.resolve()
    source_frame_dir = args.source_frame_dir.resolve()
    manifest_path = source_frame_dir / "source_frame_manifest.json"
    certificate_path = source_frame_dir / "SOURCE_FRAME_FREEZE_CERTIFICATE.json"
    canonical_path = source_frame_dir / "canonical_sources.jsonl"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    structural_summary = json.loads(args.structural_summary.read_text(encoding="utf-8"))
    if certificate.get("status") != FROZEN_STATUS:
        raise ValueError("input source frame is not frozen")
    canonical = load_jsonl(canonical_path)
    if len(canonical) != manifest.get("canonical_artifact_count"):
        raise ValueError("canonical source list does not match manifest count")
    if len(canonical) != certificate.get("counts", {}).get("canonical_artifacts"):
        raise ValueError("canonical source list does not match certificate count")
    if args.output_dir.exists():
        raise ValueError(f"refusing to overwrite output: {args.output_dir}")
    staging = args.output_dir.parent / f".{args.output_dir.name}.staging"
    if staging.exists():
        raise ValueError(f"stale staging directory: {staging}")
    staging.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    for index, source in enumerate(canonical, start=1):
        rows.append(analyse_source(source, workspace_root, verify_sha=not args.skip_source_sha_verification))
        if index % 500 == 0 or index == len(canonical):
            print(f"SOURCE_FIELD_CENSUS_PROGRESS analysed={index}/{len(canonical)}", flush=True)
    field_locations = location_summary(rows)
    validate_heading_reconciliation(field_locations, structural_summary)
    origin_identities = {f"{row['source_root']}:{row['origin_key']}" for row in rows}
    summary: dict[str, Any] = {
        "status": "RQ1B_V3_SOURCE_FIELD_SURFACE_CUE_CENSUS_LOCAL_ONLY",
        "version": VERSION,
        "canonical_artifacts": len(rows),
        "canonical_origin_identities": len(origin_identities),
        "source_roots": len({row["source_root"] for row in rows}),
        "verified_source_hashes": not args.skip_source_sha_verification,
        "source_frame_manifest_sha256": sha256_file(manifest_path),
        "source_frame_certificate_sha256": sha256_file(certificate_path),
        "canonical_sources_sha256": sha256_file(canonical_path),
        "structural_summary_sha256": sha256_file(args.structural_summary),
        "field_location_summary": field_locations,
        "field_origin_summary": origin_summary(rows),
        "source_root_summary": root_summary(rows),
        "metadata_surface": {
            "frontmatter_present": sum(row["frontmatter_present"] for row in rows),
            "metadata_name_present": sum(row["metadata_name_present"] for row in rows),
            "metadata_description_present": sum(row["metadata_description_present"] for row in rows),
        },
        "examples": examples(rows),
        "network_calls": 0,
        "texts_transmitted": 0,
        "claim_boundary": (
            "Deterministic surface-cue census over a frozen local source frame only. "
            "Not a semantic prevalence estimate, manual approval audit, cluster, prompt, label, selector run, or retrieval result."
        ),
    }
    for key in ("frontmatter_present", "metadata_name_present", "metadata_description_present"):
        summary["metadata_surface"][f"{key}_percent"] = percent(summary["metadata_surface"][key], len(rows))
    row_path = staging / "source_field_census_rows.jsonl"
    row_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    summary_path = staging / "source_field_census.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path = staging / "SOURCE_FIELD_CENSUS.md"
    markdown_path.write_text(render_markdown(summary), encoding="utf-8")
    artifacts = {
        "source_field_census_rows.jsonl": sha256_file(row_path),
        "source_field_census.json": sha256_file(summary_path),
        "SOURCE_FIELD_CENSUS.md": sha256_file(markdown_path),
    }
    run_manifest = {
        "status": "RQ1B_V3_SOURCE_FIELD_SURFACE_CUE_CENSUS_LOCAL_ONLY",
        "version": VERSION,
        "input": {
            "source_frame_dir": str(source_frame_dir),
            "source_frame_manifest_sha256": summary["source_frame_manifest_sha256"],
            "source_frame_certificate_sha256": summary["source_frame_certificate_sha256"],
            "canonical_sources_sha256": summary["canonical_sources_sha256"],
            "structural_summary_sha256": summary["structural_summary_sha256"],
        },
        "canonical_artifacts": len(rows),
        "heading_marker_reconciliation": "PASS",
        "source_sha256_verification": "SKIPPED" if args.skip_source_sha_verification else "PASS",
        "network_calls": 0,
        "texts_transmitted": 0,
        "artifacts": artifacts,
    }
    run_manifest_path = staging / "RUN_MANIFEST.json"
    run_manifest_path.write_text(json.dumps(run_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    staging.replace(args.output_dir)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--source-frame-dir", type=Path, required=True)
    parser.add_argument("--structural-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-source-sha-verification", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
