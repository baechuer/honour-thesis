#!/usr/bin/env python3
"""Strictly merge RQ2b I3C worker chunks and derive matched I3-flat text."""

from __future__ import annotations

import argparse
import json
import math
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any

from rq2b_common import (
    FIELD_SPECS,
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    selector_counts,
    selector_evidence_spans,
    serialize_i3_flat,
    serialize_i3c,
    sha256_file,
    sha256_text,
    verify_b1s_implementation_seal,
    verify_b1r_execution_authorised,
    verify_frozen_manifest,
    version_root,
    write_json_new,
    write_jsonl_new,
)
from build_rq2b_i3c_transfer_packet import verify as verify_i3c_packet


MERGER_VERSION = "rq2b-i3c-strict-merger-v1"
FIELD_KEYS = tuple(field for field, _ in FIELD_SPECS)
ALLOWED_EVIDENCE_STATUS = {"explicit", "implicit"}
ALLOWED_USEFULNESS = {"high", "medium"}
BOLD_HEADING_RE = re.compile(r"^\*\*[^*]+\*\*:?[ \t]*$")
ALLOWED_TOP_LEVEL_KEYS = {
    "schema_version",
    "parser",
    "family",
    "skill",
    "skill_id",
    "name",
    "description",
    "source",
    "fields",
    "absent_fields",
    "field_warnings",
    "qa_warnings",
}
ALLOWED_ITEM_KEYS = {
    "id",
    "text",
    "evidence",
    "evidence_status",
    "confidence",
    "selector_usefulness",
}
PROHIBITED_METADATA_KEYS = {
    "prompt",
    "prompt_id",
    "gold",
    "gold_skill",
    "valid_skills",
    "closest_alternatives",
    "stratum",
    "group",
    "role",
    "retrieval_result",
}
FIELD_WARNING_KEYS = {"code", "message", "evidence"}
QA_WARNING_KEYS = {"code", "field", "message", "evidence"}
WARNING_CODE_RE = re.compile(r"^[a-z0-9_]{1,80}$")


def reject_prohibited_metadata(value: Any, path: str = "output") -> None:
    if isinstance(value, dict):
        prohibited = set(value) & PROHIBITED_METADATA_KEYS
        require(not prohibited, f"Prohibited I3C metadata at {path}: {sorted(prohibited)}")
        for key, child in value.items():
            reject_prohibited_metadata(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_prohibited_metadata(child, f"{path}[{index}]")


def is_heading_only(source_text: str, evidence: str) -> bool:
    if "\n" in evidence.strip():
        return False
    target = evidence.strip()
    for raw_line in source_text.splitlines():
        if raw_line.strip() != target:
            continue
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            return True
        if BOLD_HEADING_RE.fullmatch(stripped):
            return True
        if stripped.endswith(":") and len(stripped) <= 120:
            return True
    return False


def validate_item(item: dict[str, Any], field_key: str) -> None:
    required = {
        "id",
        "text",
        "evidence",
        "evidence_status",
        "confidence",
        "selector_usefulness",
    }
    require(set(item) == required == ALLOWED_ITEM_KEYS, f"I3C item key mismatch in {field_key}")
    require(isinstance(item["id"], str) and bool(item["id"]), f"Invalid I3C item ID in {field_key}")
    require(isinstance(item["text"], str), f"Invalid I3C normalized text in {field_key}")
    require(isinstance(item["evidence"], str) and bool(item["evidence"]), f"Invalid I3C evidence in {field_key}")
    require(item["evidence_status"] in ALLOWED_EVIDENCE_STATUS, f"Invalid evidence status in {field_key}")
    require(item["selector_usefulness"] in ALLOWED_USEFULNESS, f"Invalid selector usefulness in {field_key}")
    confidence = float(item["confidence"])
    require(math.isfinite(confidence) and 0.0 <= confidence <= 1.0, f"Invalid confidence in {field_key}")


def validate_warning(
    warning: dict[str, Any],
    *,
    expected_keys: set[str],
    source_text: str,
    path: str,
) -> None:
    require(isinstance(warning, dict), f"I3C warning must be an object: {path}")
    require(set(warning) == expected_keys, f"I3C warning key mismatch: {path}")
    code = warning["code"]
    message = warning["message"]
    evidence = warning["evidence"]
    require(isinstance(code, str) and WARNING_CODE_RE.fullmatch(code) is not None, f"Invalid I3C warning code: {path}")
    require(isinstance(message, str) and 0 < len(message) <= 500, f"Invalid I3C warning message: {path}")
    require(isinstance(evidence, str) and len(evidence) <= 500, f"Invalid I3C warning evidence: {path}")
    require(not evidence or evidence in source_text, f"Non-substring I3C warning evidence: {path}")
    if "field" in expected_keys:
        field = warning["field"]
        require(
            isinstance(field, str) and (field == "" or field in FIELD_KEYS),
            f"Invalid I3C warning field: {path}",
        )


def validate_warning_containers(output_row: dict[str, Any], source_text: str) -> None:
    field_warnings = output_row.get("field_warnings")
    require(isinstance(field_warnings, dict), "I3C field_warnings must be an object")
    require(set(field_warnings) <= set(FIELD_KEYS), "I3C field_warnings field-key mismatch")
    for field_key, warnings in field_warnings.items():
        require(isinstance(warnings, list), f"I3C field warning list mismatch: {field_key}")
        for index, warning in enumerate(warnings):
            validate_warning(
                warning,
                expected_keys=FIELD_WARNING_KEYS,
                source_text=source_text,
                path=f"field_warnings.{field_key}[{index}]",
            )
    qa_warnings = output_row.get("qa_warnings")
    require(isinstance(qa_warnings, list), "I3C qa_warnings must be an array")
    for index, warning in enumerate(qa_warnings):
        validate_warning(
            warning,
            expected_keys=QA_WARNING_KEYS,
            source_text=source_text,
            path=f"qa_warnings[{index}]",
        )


def canonical_extraction(
    input_row: dict[str, Any],
    output_row: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    require(set(output_row) == ALLOWED_TOP_LEVEL_KEYS, "I3C worker top-level key mismatch")
    reject_prohibited_metadata(output_row)
    require(output_row.get("schema_version") == "I3C_SUBAGENT_EXTRACTION_V2", "I3C worker schema mismatch")
    require(output_row.get("parser") == "codex_subagent", "I3C worker parser mismatch")
    require(output_row.get("skill") is None, "RQ2b I3C worker skill field must be null")
    for key, input_key in (
        ("skill_id", "skill_id"),
        ("name", "name"),
        ("description", "description"),
        ("family", "family"),
        ("source", "source"),
    ):
        require(output_row.get(key) == input_row[input_key], f"I3C worker identity mismatch: {key}")
    fields = output_row.get("fields")
    require(isinstance(fields, dict), "I3C worker fields must be an object")
    require(set(fields) == set(FIELD_KEYS), "I3C worker field-key set mismatch")
    for field_key in FIELD_KEYS:
        values = fields[field_key]
        require(isinstance(values, list), f"I3C worker field must be an array: {field_key}")
        seen_ids: set[str] = set()
        for item in values:
            require(isinstance(item, dict), f"I3C item must be an object: {field_key}")
            validate_item(item, field_key)
            require(item["id"] not in seen_ids, f"Duplicate I3C item ID in {field_key}")
            seen_ids.add(item["id"])
            require(item["evidence"] in input_row["text"], f"Non-substring I3C evidence: {input_row['skill_id']}")
    empty_fields = {field for field in FIELD_KEYS if not fields[field]}
    absent_fields = output_row.get("absent_fields")
    require(isinstance(absent_fields, list), "I3C absent_fields must be an array")
    require(set(absent_fields) == empty_fields, f"I3C absent-field mismatch: {input_row['skill_id']}")
    validate_warning_containers(output_row, input_row["text"])

    retained, omitted = selector_evidence_spans(
        output_row,
        source_text=input_row["text"],
        name=input_row["name"],
        description=input_row["description"],
    )
    heading_omitted: list[dict[str, Any]] = []
    heading_filtered: list[dict[str, Any]] = []
    for span in retained:
        if is_heading_only(input_row["text"], span["evidence"]):
            heading = {**span, "omission_reason": "heading_only_evidence"}
            heading_omitted.append(heading)
        else:
            heading_filtered.append(span)
    omitted = [*omitted, *heading_omitted]
    canonical = {
        "schema_version": "rq2b-i3c-canonical-extraction-v1",
        "merger_version": MERGER_VERSION,
        "source_row_index": input_row["source_row_index"],
        "skill_id": input_row["skill_id"],
        "family": input_row["family"],
        "source": input_row["source"],
        "source_sha256": input_row["source_sha256"],
        "name": input_row["name"],
        "description": input_row["description"],
        "fields": fields,
        "absent_fields": sorted(empty_fields),
        "field_warnings": output_row["field_warnings"],
        "qa_warnings": output_row["qa_warnings"],
        "retained_selector_spans": heading_filtered,
        "omitted_selector_spans": omitted,
        "worker_output_sha256": sha256_text(
            json.dumps(output_row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ),
    }
    return canonical, heading_filtered, omitted


def representation_row(
    canonical: dict[str, Any],
    representation: str,
    selector_text: str,
) -> dict[str, Any]:
    return {
        "schema_version": "rq2b-representation-row-v1",
        "serializer_version": MERGER_VERSION,
        "representation": representation,
        "source_row_index": canonical["source_row_index"],
        "skill_id": canonical["skill_id"],
        "family": canonical["family"],
        "source_path": canonical["source"],
        "source_sha256": canonical["source_sha256"],
        "selector_text": selector_text,
        "selector_text_sha256": sha256_text(selector_text),
        "selector_visible_counts": selector_counts(selector_text),
        "selector_evidence_spans": [
            {
                "field_key": span["field_key"],
                "field_label": span["field_label"],
                "item_id": span["item_id"],
                "source_position": span["source_position"],
                "selector_evidence": span["selector_evidence"],
            }
            for span in canonical["retained_selector_spans"]
        ],
    }


def summarize(
    canonical_rows: list[dict[str, Any]],
    i3c_rows: list[dict[str, Any]],
    flat_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    coverage = Counter()
    items = Counter()
    absent = Counter()
    warnings = Counter()
    omissions = Counter()
    for row in canonical_rows:
        for field_key in FIELD_KEYS:
            field_items = row["fields"][field_key]
            if field_items:
                coverage[field_key] += 1
                items[field_key] += len(field_items)
            else:
                absent[field_key] += 1
        for warning in row["qa_warnings"]:
            if isinstance(warning, dict):
                warnings[str(warning.get("code") or "warning")] += 1
            else:
                warnings["non_object_warning"] += 1
        for span in row["omitted_selector_spans"]:
            omissions[span["omission_reason"]] += 1
    duplicate_i3c_texts = sum(
        count - 1 for count in Counter(row["selector_text_sha256"] for row in i3c_rows).values() if count > 1
    )
    for i3c, flat in zip(i3c_rows, flat_rows, strict=True):
        require(i3c["skill_id"] == flat["skill_id"], "I3C/I3-flat identity mismatch")
        require(
            [row["selector_evidence"] for row in i3c["selector_evidence_spans"]]
            == [row["selector_evidence"] for row in flat["selector_evidence_spans"]],
            f"I3C/I3-flat evidence mismatch: {i3c['skill_id']}",
        )
    return {
        "rows": len(canonical_rows),
        "parse_failures": 0,
        "identity_failures": 0,
        "evidence_substring_failures": 0,
        "field_row_coverage": dict(sorted(coverage.items())),
        "field_item_counts": dict(sorted(items.items())),
        "absent_field_counts": dict(sorted(absent.items())),
        "warning_counts": dict(sorted(warnings.items())),
        "omission_counts": dict(sorted(omissions.items())),
        "heading_only_evidence_removed": omissions["heading_only_evidence"],
        "duplicate_i3c_selector_text_rows_beyond_first": duplicate_i3c_texts,
        "i3c_i3flat_evidence_match_rows": len(i3c_rows),
        "i3c_selector_utf8_bytes": sum(row["selector_visible_counts"]["utf8_bytes"] for row in i3c_rows),
        "i3flat_selector_utf8_bytes": sum(row["selector_visible_counts"]["utf8_bytes"] for row in flat_rows),
    }


def merge(root: Path) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    verify_b1r_execution_authorised(root)
    frozen_root = version_root(root)
    packet_root = frozen_root / "i3c_extraction"
    packet = verify_i3c_packet(root)
    require(packet.get("state") == "built_not_transmitted", "Unexpected I3C packet state")
    missing_outputs = [row["expected_output_path"] for row in packet["chunks"] if not (root / row["expected_output_path"]).exists()]
    require(not missing_outputs, f"I3C worker outputs are incomplete: {len(missing_outputs)} missing")

    canonical_rows: list[dict[str, Any]] = []
    i3c_rows: list[dict[str, Any]] = []
    flat_rows: list[dict[str, Any]] = []
    output_hashes: list[dict[str, Any]] = []
    canonicalization_seconds = 0.0
    i3c_serialization_seconds = 0.0
    i3flat_serialization_seconds = 0.0
    for chunk in packet["chunks"]:
        input_path = root / chunk["input_path"]
        output_path = root / chunk["expected_output_path"]
        inputs = read_jsonl(input_path)
        outputs = read_jsonl(output_path)
        require(len(inputs) == len(outputs) == chunk["row_count"], f"I3C chunk row mismatch: {output_path}")
        output_hashes.append(
            {
                "path": relative(output_path, root),
                "sha256": sha256_file(output_path),
                "rows": len(outputs),
            }
        )
        for input_row, output_row in zip(inputs, outputs, strict=True):
            canonical_started = time.perf_counter()
            canonical, retained, _ = canonical_extraction(input_row, output_row)
            canonicalization_seconds += time.perf_counter() - canonical_started
            i3c_started = time.perf_counter()
            i3c_text = serialize_i3c(input_row["name"], input_row["description"], retained)
            i3c_serialization_seconds += time.perf_counter() - i3c_started
            i3flat_started = time.perf_counter()
            flat_text = serialize_i3_flat(input_row["name"], input_row["description"], retained)
            i3flat_serialization_seconds += time.perf_counter() - i3flat_started
            canonical_rows.append(canonical)
            i3c_rows.append(representation_row(canonical, "i3c-fielded-evidence", i3c_text))
            flat_rows.append(representation_row(canonical, "i3-flat-evidence", flat_text))

    require(len(canonical_rows) == 2433, "Merged I3C row count must be 2,433")
    require([row["source_row_index"] for row in canonical_rows] == list(range(2433)), "Merged I3C row indices are not contiguous")
    require(len({row["skill_id"] for row in canonical_rows}) == 2433, "Merged I3C skill IDs are not unique")
    summary = summarize(canonical_rows, i3c_rows, flat_rows)

    output_root = frozen_root / "i3c_merged"
    staging_root = frozen_root / ".i3c_merged.staging"
    require(not output_root.exists(), f"Merged I3C output root exists: {output_root}")
    require(not staging_root.exists(), f"Stale merged I3C staging root: {staging_root}")
    staging_root.mkdir(parents=True, exist_ok=False)
    canonical_path = staging_root / "canonical_extractions.jsonl"
    i3c_path = staging_root / "i3c-fielded-evidence.jsonl"
    flat_path = staging_root / "i3-flat-evidence.jsonl"
    write_jsonl_new(canonical_path, canonical_rows)
    write_jsonl_new(i3c_path, i3c_rows)
    write_jsonl_new(flat_path, flat_rows)
    artifacts = {
        "canonical_extractions": canonical_path,
        "i3c-fielded-evidence": i3c_path,
        "i3-flat-evidence": flat_path,
    }
    manifest = {
        "schema_version": "rq2b-i3c-merge-manifest-v1",
        "version_id": VERSION_ID,
        "state": "automatic_gates_passed_manual_qa_pending",
        "merger_version": MERGER_VERSION,
        "network_calls": 0,
        "packet_manifest_sha256": sha256_file(packet_root / "manifest.json"),
        "worker_outputs": output_hashes,
        "timing": {
            "canonicalization_seconds": canonicalization_seconds,
            "i3c_serialization_seconds": i3c_serialization_seconds,
            "i3flat_serialization_seconds": i3flat_serialization_seconds,
        },
        "summary": summary,
        "artifacts": {
            name: {
                "path": relative(output_root / path.name, root),
                "sha256": sha256_file(path),
                "rows": len(canonical_rows),
            }
            for name, path in artifacts.items()
        },
        "retrieval_authorized": False,
        "manual_qa_required_rows": 120,
    }
    write_json_new(staging_root / "manifest.json", manifest)
    staging_root.replace(output_root)
    return manifest


def self_test() -> dict[str, Any]:
    source = (
        "---\nname: pdf-worker\ndescription: Handle PDF jobs.\n---\n"
        "# Workflow\nUse this for scanned PDF files.\nRun OCR before table extraction.\n"
        "Output a JSON table.\nDependency:\nRequires Tesseract.\n"
    )
    input_row = {
        "source_row_index": 0,
        "skill_id": "pdf-worker",
        "name": "pdf-worker",
        "description": "Handle PDF jobs.",
        "family": "synthetic",
        "source": "synthetic/SKILL.md",
        "source_sha256": sha256_text(source),
        "text": source,
    }
    fields = {field: [] for field in FIELD_KEYS}
    fields["use_conditions"] = [
        {
            "id": "use_1",
            "text": "scanned PDFs",
            "evidence": "Use this for scanned PDF files.",
            "evidence_status": "explicit",
            "confidence": 0.95,
            "selector_usefulness": "high",
        }
    ]
    fields["workflow_steps"] = [
        {
            "id": "step_2",
            "text": "extract tables",
            "evidence": "Output a JSON table.",
            "evidence_status": "implicit",
            "confidence": 0.8,
            "selector_usefulness": "medium",
        },
        {
            "id": "step_1",
            "text": "run OCR",
            "evidence": "Run OCR before table extraction.",
            "evidence_status": "explicit",
            "confidence": 0.9,
            "selector_usefulness": "high",
        },
    ]
    fields["dependencies_resources"] = [
        {
            "id": "dependency_1",
            "text": "Tesseract",
            "evidence": "Requires Tesseract.",
            "evidence_status": "explicit",
            "confidence": 0.99,
            "selector_usefulness": "high",
        }
    ]
    fields["constraints_boundaries"] = [
        {
            "id": "boundary_1",
            "text": "duplicate for dedupe test",
            "evidence": "Requires Tesseract.",
            "evidence_status": "explicit",
            "confidence": 0.7,
            "selector_usefulness": "medium",
        }
    ]
    output_row = {
        "schema_version": "I3C_SUBAGENT_EXTRACTION_V2",
        "parser": "codex_subagent",
        "family": input_row["family"],
        "skill": None,
        "skill_id": input_row["skill_id"],
        "name": input_row["name"],
        "description": input_row["description"],
        "source": input_row["source"],
        "fields": fields,
        "absent_fields": sorted(field for field in FIELD_KEYS if not fields[field]),
        "field_warnings": {
            "output_artifacts": [
                {
                    "code": "field_absent",
                    "message": "No selector-useful output artifact is stated.",
                    "evidence": "",
                }
            ]
        },
        "qa_warnings": [
            {
                "code": "generic_fragment_skipped",
                "field": "workflow_steps",
                "message": "The heading alone is not selector-useful.",
                "evidence": "# Workflow",
            }
        ],
    }
    canonical, retained, omitted = canonical_extraction(input_row, output_row)
    require([row["item_id"] for row in retained] == ["use_1", "step_1", "step_2", "dependency_1"], "I3C canonical ordering failed")
    require(any(row["omission_reason"] == "global_exact_evidence_duplicate" for row in omitted), "I3C global dedupe failed")
    i3c = serialize_i3c(input_row["name"], input_row["description"], retained)
    flat = serialize_i3_flat(input_row["name"], input_row["description"], retained)
    require("Use condition:" in i3c and "Use condition:" not in flat, "I3C/flat labels failed")
    require(all(row["selector_evidence"] in i3c for row in retained), "I3C evidence serialization failed")
    require(all(row["selector_evidence"] in flat for row in retained), "I3-flat evidence serialization failed")
    malformed_warning = json.loads(json.dumps(output_row))
    malformed_warning["qa_warnings"][0]["prompt_id"] = "forbidden"
    try:
        canonical_extraction(input_row, malformed_warning)
    except ValueError as exc:
        require("Prohibited I3C metadata" in str(exc), "I3C warning-schema rejection message drift")
    else:
        raise AssertionError("Nested I3C warning metadata was accepted")
    return {
        "state": "synthetic_no_source_transfer_no_scientific_score",
        "retained_spans": len(retained),
        "omitted_spans": len(omitted),
        "i3c_sha256": sha256_text(i3c),
        "i3flat_sha256": sha256_text(flat),
        "canonical_skill_id": canonical["skill_id"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = self_test() if args.self_test else merge(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
