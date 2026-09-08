#!/usr/bin/env python3
"""Read-only validation for one V7 full-corpus I3 V4.1 extraction batch."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from merge_rq2b_i3c import canonical_extraction


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_full_reextraction_2026_09_09_v4_1")
FIELD_PREFIX = {
    "use_conditions": "use_",
    "input_preconditions": "input_",
    "output_artifacts": "output_",
    "workflow_steps": "workflow_",
    "constraints_boundaries": "boundary_",
    "dependencies_resources": "dependency_",
    "success_criteria": "success_",
}
NOT_FOR_USE = re.compile(
    r"\b(?:do\s+not\s+use|don't\s+use|not\s+for|when\s+not\s+to\s+use|"
    r"must\s+not\s+use|never\s+use|cannot\s+be\s+used|can't\s+be\s+used|"
    r"does\s+not\s+support|doesn't\s+support|does\s+not\s+work|doesn't\s+work|unsupported)\b",
    re.I,
)
RAW_DESCRIPTION_KEY = re.compile(r"(?m)^\s*description\s*:")
FORBIDDEN_METADATA_KEY = re.compile(
    r"(?m)^\s*(?:prompt_id|target_skill|gold_label|gold_set|acceptable_set|routing_label|benchmark_id)\s*:",
    re.I,
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def frontmatter_span(source_text: str) -> tuple[int, int] | None:
    """Return the opening YAML-frontmatter span, including delimiters."""
    lines = source_text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    offset = len(lines[0])
    for line in lines[1:]:
        offset += len(line)
        if line.strip() in {"---", "..."}:
            return 0, offset
    return None


def evidence_in_frontmatter(source_text: str, evidence: str) -> bool:
    span = frontmatter_span(source_text)
    if span is None:
        return False
    start = source_text.find(evidence)
    while start >= 0:
        if span[0] <= start and start + len(evidence) <= span[1]:
            return True
        start = source_text.find(evidence, start + 1)
    return False


def validate_v4_1_semantics(input_row: dict, output_row: dict) -> tuple[int, int]:
    source_text = input_row["text"]
    seen_evidence: dict[str, str] = {}
    item_count = 0
    for field, items in output_row["fields"].items():
        for item in items:
            item_count += 1
            if not item["id"].startswith(FIELD_PREFIX[field]):
                raise ValueError(f"V4.1 item ID/field mismatch: {input_row['skill_id']} {field} {item['id']}")
            evidence = item["evidence"]
            stripped = evidence.strip()
            in_frontmatter = evidence_in_frontmatter(source_text, evidence)
            if stripped in {">", "|"}:
                raise ValueError(f"V4.1 bare scalar marker retained: {input_row['skill_id']}")
            if in_frontmatter and RAW_DESCRIPTION_KEY.search(evidence):
                raise ValueError(f"V4.1 raw frontmatter description syntax retained: {input_row['skill_id']}")
            if in_frontmatter and FORBIDDEN_METADATA_KEY.search(evidence):
                raise ValueError(f"V4.1 forbidden candidate metadata retained: {input_row['skill_id']}")
            lowered = evidence.lower()
            if in_frontmatter and (
                "category: public-style-controlled" in lowered
                and "controlled-confusability" in lowered
                and ("source_style: public_style_controlled" in lowered or re.search(r"cluster_id:\s*psc_", lowered))
            ):
                raise ValueError(f"V4.1 controlled-corpus metadata leakage: {input_row['skill_id']}")
            if field == "use_conditions" and NOT_FOR_USE.search(evidence):
                raise ValueError(f"V4.1 explicit not-for/use-prohibition under use_conditions: {input_row['skill_id']}")
            previous_field = seen_evidence.get(evidence)
            if previous_field is not None and previous_field != field:
                raise ValueError(f"V4.1 same evidence duplicated across fields: {input_row['skill_id']}")
            seen_evidence[evidence] = field
    warning_count = sum(len(values) for values in output_row["field_warnings"].values()) + len(output_row["qa_warnings"])
    return item_count, warning_count


def validate(batch_id: str, output_override: Path | None = None) -> dict:
    assignments = rows((ROOT / PREP / "full_reextraction_assignment_manifest.jsonl").read_bytes())
    assignment_by_id = {row["batch_id"]: row for row in assignments}
    assignment = assignment_by_id.get(batch_id)
    if assignment is None:
        raise ValueError(f"unknown V4.1 batch: {batch_id}")
    input_path = ROOT / assignment["input_path"]
    input_data = input_path.read_bytes()
    if sha(input_data) != assignment["input_sha256"]:
        raise ValueError("V4.1 input hash mismatch")
    input_rows = rows(input_data)
    output_path = output_override if output_override else ROOT / assignment["expected_output_path"]
    output_data = output_path.read_bytes()
    output_rows = rows(output_data)
    if len(input_rows) != assignment["row_count"] or len(output_rows) != len(input_rows):
        raise ValueError("V4.1 input/output row count mismatch")
    item_count = warning_count = 0
    for input_row, output_row in zip(input_rows, output_rows, strict=True):
        canonical_extraction(input_row, output_row)
        items, warnings = validate_v4_1_semantics(input_row, output_row)
        item_count += items
        warning_count += warnings
    return {
        "status": "PASS_I3_V4_1_BATCH_VALIDATION",
        "batch_id": batch_id,
        "rows": len(output_rows),
        "items": item_count,
        "warnings_pending_source_only_disposition": warning_count,
        "input_sha256": sha(input_data),
        "output_sha256": sha(output_data),
        "output_path": str(output_path.resolve().relative_to(ROOT.resolve())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_id")
    parser.add_argument("--output-path", type=Path)
    args = parser.parse_args()
    if re.fullmatch(r"I3V41-\d{3}", args.batch_id) is None:
        parser.error("batch_id must be I3V41-NNN")
    print(json.dumps(validate(args.batch_id, args.output_path), sort_keys=True))


if __name__ == "__main__":
    main()
