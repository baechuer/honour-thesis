#!/usr/bin/env python3
"""Merge Codex-subagent I3C chunk outputs into one canonical JSONL file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


I3_FIELDS = [
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "constraints_boundaries",
    "dependencies_resources",
    "success_criteria",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def normalize_warning(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        item = dict(value)
        item["code"] = str(item.get("code") or "warning").strip()
        item["message"] = str(item.get("message") or item.get("text") or "").strip()
        item["field"] = str(item.get("field") or "").strip()
        item["evidence"] = str(item.get("evidence") or "").strip()
        return item
    return {
        "code": "warning",
        "message": str(value).strip(),
        "field": "",
        "evidence": "",
    }


def normalize_warning_list(values: Any) -> list[dict[str, Any]]:
    if values is None:
        return []
    if not isinstance(values, list):
        values = [values]
    return [normalize_warning(value) for value in values if str(value).strip()]


def normalize_field_warnings(value: Any) -> dict[str, list[dict[str, Any]]]:
    if not isinstance(value, dict):
        return {}
    normalized: dict[str, list[dict[str, Any]]] = {}
    for field, warnings in value.items():
        if field not in I3_FIELDS:
            continue
        field_items = normalize_warning_list(warnings)
        if field_items:
            normalized[field] = field_items
    return normalized


def item_prefix(field: str) -> str:
    return {
        "use_conditions": "use",
        "input_preconditions": "input",
        "output_artifacts": "output",
        "workflow_steps": "step",
        "constraints_boundaries": "boundary",
        "dependencies_resources": "dependency",
        "success_criteria": "success",
    }[field]


def normalize_item(value: Any, field: str, index: int) -> dict[str, Any]:
    prefix = item_prefix(field)
    if isinstance(value, dict):
        item = dict(value)
        text = str(item.get("text") or item.get("action") or item.get("evidence") or "").strip()
        item.setdefault("id", f"{prefix}_{index}")
        item.setdefault("text", text)
        item.setdefault("evidence", str(item.get("evidence") or text).strip())
        item.setdefault("evidence_status", "implicit")
        item.setdefault("confidence", 0.6)
        return item

    text = str(value).strip()
    return {
        "id": f"{prefix}_{index}",
        "text": text,
        "evidence": text,
        "evidence_status": "implicit",
        "confidence": 0.5,
    }


def normalize_row(row: dict[str, Any], source_row: dict[str, Any] | None = None) -> dict[str, Any]:
    source_row = source_row or {}
    raw_fields = row.get("fields")
    if not isinstance(raw_fields, dict):
        raw_fields = {field: row.get(field, []) for field in I3_FIELDS}

    fields: dict[str, list[dict[str, Any]]] = {}
    absent_fields = []
    for field in I3_FIELDS:
        values = raw_fields.get(field, [])
        if values is None:
            values = []
        if not isinstance(values, list):
            values = [values]
        fields[field] = [
            normalize_item(value, field, index)
            for index, value in enumerate(values, 1)
            if str(value).strip()
        ]
        if not fields[field]:
            absent_fields.append(field)

    row_absent = row.get("absent_fields")
    if isinstance(row_absent, list):
        absent_fields = sorted({field for field in absent_fields + [str(value) for value in row_absent] if field in I3_FIELDS})

    return {
        "schema_version": row.get("schema_version") or "I3C_CODEX_SUBAGENT_V1",
        "parser": "codex_subagent",
        "family": row.get("family") or source_row.get("family") or "skillrouter_eval_core_all_i2",
        "skill": row.get("skill") or source_row.get("skill"),
        "skill_id": row.get("skill_id") or source_row.get("skill_id"),
        "name": row.get("name") or source_row.get("name"),
        "description": row.get("description") or source_row.get("description"),
        "source": row.get("source") or source_row.get("source"),
        "fields": fields,
        "absent_fields": absent_fields,
        "field_warnings": normalize_field_warnings(row.get("field_warnings")),
        "qa_warnings": normalize_warning_list(row.get("qa_warnings")),
        "text": row.get("text") or source_row.get("text") or "",
        "parse_failed": bool(row.get("parse_failed")),
        **({"parse_error": row.get("parse_error")} if row.get("parse_error") else {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks-dir", required=True)
    parser.add_argument("--pattern", default="external_i3c_output_[0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9].jsonl")
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--summary-json", required=True)
    args = parser.parse_args()

    chunks_dir = Path(args.chunks_dir)
    output_jsonl = Path(args.output_jsonl)
    summary_json = Path(args.summary_json)
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    summary_json.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(chunks_dir.glob(args.pattern))
    rows: list[dict[str, Any]] = []
    source_files: dict[str, int] = {}
    field_row_coverage = {field: 0 for field in I3_FIELDS}
    field_item_counts = {field: 0 for field in I3_FIELDS}
    warning_counts: dict[str, int] = {}
    absent_field_counts = {field: 0 for field in I3_FIELDS}
    schema_version_counts: dict[str, int] = {}

    for path in files:
        input_path = path.parent.parent / "inputs" / path.name.replace("output", "input")
        source_rows = []
        if input_path.exists():
            source_rows = read_jsonl(input_path)
        count = 0
        with path.open("r", encoding="utf-8") as handle:
            output_lines = list(handle)
        for line_number, line in enumerate(output_lines, 1):
            if not line.strip():
                continue
            source_row = source_rows[count] if count < len(source_rows) else None
            try:
                normalized = normalize_row(json.loads(line), source_row=source_row)
            except Exception as exc:  # noqa: BLE001
                normalized = {
                    "schema_version": "I3C_CODEX_SUBAGENT_V1",
                    "parser": "codex_subagent",
                    "family": (source_row or {}).get("family") or "skillrouter_eval_core_all_i2",
                    "skill": (source_row or {}).get("skill"),
                    "skill_id": (source_row or {}).get("skill_id"),
                    "name": (source_row or {}).get("name"),
                    "description": (source_row or {}).get("description"),
                    "source": (source_row or {}).get("source"),
                    "fields": {field: [] for field in I3_FIELDS},
                    "absent_fields": list(I3_FIELDS),
                    "field_warnings": {},
                    "qa_warnings": [
                        {
                            "code": "normalization_error",
                            "field": "",
                            "message": str(exc),
                            "evidence": "",
                        }
                    ],
                    "text": (source_row or {}).get("text", ""),
                    "parse_failed": True,
                    "parse_error": f"{path.name}:{line_number}: {exc}",
                }
            rows.append(normalized)
            count += 1
            schema_version = str(normalized.get("schema_version") or "unknown")
            schema_version_counts[schema_version] = schema_version_counts.get(schema_version, 0) + 1
            for field in I3_FIELDS:
                n_items = len(normalized["fields"][field])
                if n_items:
                    field_row_coverage[field] += 1
                    field_item_counts[field] += n_items
            for field in normalized.get("absent_fields") or []:
                if field in absent_field_counts:
                    absent_field_counts[field] += 1
            for warning in normalized.get("qa_warnings") or []:
                code = str(warning.get("code") or "warning")
                warning_counts[code] = warning_counts.get(code, 0) + 1
            for warnings in (normalized.get("field_warnings") or {}).values():
                for warning in warnings:
                    code = str(warning.get("code") or "field_warning")
                    warning_counts[code] = warning_counts.get(code, 0) + 1
        source_files[path.name] = count

    with output_jsonl.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    parse_failed = sum(1 for row in rows if row.get("parse_failed"))
    summary = {
        "schema_version": "I3C_MERGED_NORMALIZED_V1",
        "schema_version_counts": schema_version_counts,
        "source_file_count": len(files),
        "row_count": len(rows),
        "parse_failed": parse_failed,
        "source_files": source_files,
        "field_row_coverage": field_row_coverage,
        "field_item_counts": field_item_counts,
        "absent_field_counts": absent_field_counts,
        "warning_counts": warning_counts,
        "output_jsonl": str(output_jsonl),
    }
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
