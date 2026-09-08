#!/usr/bin/env python3
"""Materialise a source-only, cross-group audit for every V4.1 warning.

The package is intentionally downstream of mechanical output selection and
upstream of the I3 merge.  It exposes source text and extraction evidence, but
never benchmark prompts, targets, acceptable sets, retrieval outputs, or
metrics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from freeze_rq2b_v7_i3_v4_1_output_selection import (
    OUTPUT as SELECTION,
    build_inputs,
    verify as verify_selection,
)
from validate_rq2b_v7_i3_v4_1_1_batch import PREP, ROOT


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_warning_audit_2026_09_09_v1"
)
SCHEMA_VERSION = "rq2b-v7-i3-v4.1-warning-audit-packet-v1"
RETURN_SCHEMA_VERSION = "rq2b-v7-i3-v4.1-warning-audit-return-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha(data)


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: list[dict]) -> bytes:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in values
    ).encode()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def selected_output(selection: dict) -> bytes:
    path = ROOT / selection["selected_output_path"]
    data = path.read_bytes()
    require(sha(data) == selection["selected_output_sha256"], f"selected output drift: {selection['batch_id']}")
    return data


def warning_pairs(output_row: dict) -> list[tuple[str, dict]]:
    """Return QA warnings after proving the field/QA mirrors are one-to-one."""
    qa = output_row["qa_warnings"]
    field_flat: list[dict] = []
    for field, warnings in output_row["field_warnings"].items():
        for warning in warnings:
            field_flat.append({"field": field, **warning})
    require(
        Counter(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in qa)
        == Counter(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in field_flat),
        f"field/QA warning mirror mismatch: {output_row['skill_id']}",
    )
    indexed = []
    for index, warning in enumerate(qa, 1):
        indexed.append((f"warning-{index:03d}", warning))
    return indexed


def assign_reviewer_groups(issues: list[dict]) -> None:
    """Greedily balance issues while forbidding own-extractor review."""
    load = Counter({1: 0, 2: 0, 3: 0})
    for issue in sorted(issues, key=lambda row: row["issue_id"]):
        eligible = [group for group in (1, 2, 3) if group != issue["extractor_group"]]
        chosen = min(eligible, key=lambda group: (load[group], group))
        issue["reviewer_group"] = chosen
        load[chosen] += 1


def build() -> dict[str, bytes]:
    verify_selection()
    assignments_path = ROOT / PREP / "full_reextraction_assignment_manifest.jsonl"
    selection_path = ROOT / SELECTION / "selection_ledger.jsonl"
    assignments = rows(assignments_path.read_bytes())
    selections = rows(selection_path.read_bytes())
    require(len(assignments) == len(selections) == 95, "warning audit requires 95 selected batches")
    assignment_by_batch = {row["batch_id"]: row for row in assignments}
    selection_by_batch = {row["batch_id"]: row for row in selections}
    require(len(assignment_by_batch) == len(selection_by_batch) == 95, "duplicate warning-audit batch ID")
    _, input_payloads = build_inputs()

    issues: list[dict] = []
    selected_bindings: list[dict] = []
    for batch_id in sorted(assignment_by_batch):
        assignment = assignment_by_batch[batch_id]
        selection = selection_by_batch[batch_id]
        input_name = str(Path(assignment["input_path"]).relative_to(
            "skill_benchmark/cache/rq2b_v7_phase7_i3_full_reextraction_2026_09_09_v4_1"
        ))
        input_data = input_payloads[input_name]
        output_data = selected_output(selection)
        require(sha(input_data) == assignment["input_sha256"], f"warning-audit input drift: {batch_id}")
        input_rows, output_rows = rows(input_data), rows(output_data)
        require(len(input_rows) == len(output_rows) == assignment["row_count"], f"warning-audit row mismatch: {batch_id}")
        for source_row, output_row in zip(input_rows, output_rows, strict=True):
            require(source_row["skill_id"] == output_row["skill_id"], f"warning-audit skill drift: {batch_id}")
            for local_id, warning in warning_pairs(output_row):
                evidence = warning["evidence"]
                require(not evidence or evidence in source_row["text"], f"warning evidence drift: {batch_id} {local_id}")
                issue_seed = {
                    "batch_id": batch_id,
                    "source_row_index": source_row["source_row_index"],
                    "skill_id": source_row["skill_id"],
                    "local_warning_id": local_id,
                    "warning": warning,
                    "selected_output_sha256": selection["selected_output_sha256"],
                }
                issues.append({
                    "schema_version": SCHEMA_VERSION,
                    "issue_id": "I3W-" + canonical_sha(issue_seed)[:20],
                    "batch_id": batch_id,
                    "extractor_group": assignment["extractor_group"],
                    "reviewer_group": None,
                    "source_row_index": source_row["source_row_index"],
                    "skill_id": source_row["skill_id"],
                    "source_sha256": source_row["source_sha256"],
                    "name": source_row["name"],
                    "description": source_row["description"],
                    "source_text": source_row["text"],
                    "extracted_fields": output_row["fields"],
                    "warning": warning,
                    "selected_output_sha256": selection["selected_output_sha256"],
                    "review_boundary": (
                        "Source-only warning disposition. Do not access benchmark prompts, targets, "
                        "acceptable sets, retrieval outputs, metrics, or the extractor's rationale outside this packet."
                    ),
                })
        selected_bindings.append({
            "batch_id": batch_id,
            "input_sha256": assignment["input_sha256"],
            "selected_output_sha256": selection["selected_output_sha256"],
        })

    require(len({row["issue_id"] for row in issues}) == len(issues), "warning issue ID collision")
    assign_reviewer_groups(issues)
    issues.sort(key=lambda row: (row["reviewer_group"], row["issue_id"]))
    payloads: dict[str, bytes] = {"warning_docket.jsonl": rows_bytes(issues)}
    payloads["reviewer_return_schema.json"] = json_bytes({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "issue_id", "reviewer_group", "source_sha256",
            "selected_output_sha256", "decision", "evidence_is_exact_and_complete",
            "warning_is_justified", "field_assignment_is_correct", "rationale",
        ],
        "properties": {
            "schema_version": {"const": RETURN_SCHEMA_VERSION},
            "issue_id": {"type": "string", "pattern": "^I3W-[0-9a-f]{20}$"},
            "reviewer_group": {"type": "integer", "enum": [1, 2, 3]},
            "source_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "selected_output_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "decision": {"enum": ["ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION", "REISSUE_REQUIRED"]},
            "evidence_is_exact_and_complete": {"type": "boolean"},
            "warning_is_justified": {"type": "boolean"},
            "field_assignment_is_correct": {"type": "boolean"},
            "rationale": {"type": "string", "minLength": 1},
        },
    })
    group_counts = Counter()
    extractor_counts = Counter()
    warning_codes = Counter()
    for group in (1, 2, 3):
        packet_rows = [row for row in issues if row["reviewer_group"] == group]
        payloads[f"reviewer_group_{group}_packet.jsonl"] = rows_bytes(packet_rows)
        payloads[f"reviewer_group_{group}_return_template.jsonl"] = rows_bytes([
            {
                "schema_version": RETURN_SCHEMA_VERSION,
                "issue_id": row["issue_id"],
                "reviewer_group": group,
                "source_sha256": row["source_sha256"],
                "selected_output_sha256": row["selected_output_sha256"],
                "decision": "PENDING",
                "evidence_is_exact_and_complete": None,
                "warning_is_justified": None,
                "field_assignment_is_correct": None,
                "rationale": "",
            }
            for row in packet_rows
        ])
        group_counts[group] = len(packet_rows)
    for row in issues:
        extractor_counts[row["extractor_group"]] += 1
        warning_codes[row["warning"]["code"]] += 1
        require(row["reviewer_group"] != row["extractor_group"], "own-extractor warning review")

    docket_data = payloads["warning_docket.jsonl"]
    report = {
        "schema_version": "rq2b-v7-i3-v4.1-warning-audit-build-report-v1",
        "state": "MATERIALISED_PENDING_SOURCE_ONLY_WARNING_RETURNS" if issues else "PASS_NO_WARNINGS_REQUIRING_DISPOSITION",
        "formal_execution_ready": False,
        "counts": {
            "selected_batches": 95,
            "sources": 3798,
            "unique_warning_issues": len(issues),
            "by_reviewer_group": {str(k): group_counts[k] for k in (1, 2, 3)},
            "by_extractor_group": {str(k): extractor_counts[k] for k in (1, 2, 3)},
            "by_warning_code": dict(sorted(warning_codes.items())),
        },
        "bindings": {
            "assignment_manifest_sha256": sha(assignments_path.read_bytes()),
            "selection_ledger_sha256": sha(selection_path.read_bytes()),
            "warning_docket_sha256": sha(docket_data),
            "builder_sha256": sha(Path(__file__).read_bytes()),
            "reviewer_return_schema_sha256": sha(payloads["reviewer_return_schema.json"]),
            "selected_batches_sha256": canonical_sha(selected_bindings),
        },
        "rules": {
            "cross_group_review": True,
            "own_extractor_review_forbidden": True,
            "allowed_decisions": ["ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION", "REISSUE_REQUIRED"],
            "reissue_effect": "Any REISSUE_REQUIRED decision blocks merge and requires a traceable batch reissue followed by a new selection/audit version.",
        },
    }
    payloads["integrity_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 I3 V4.1 source-only warning audit\n\n"
        "This package cross-assigns every unique extraction warning to a reviewer group other than the extractor group. "
        "Reviewers may use only their packet and the return schema. A warning may be accepted only when the cited source text is exact and complete, the warning is justified, and the retained field assignment is correct. Otherwise choose `REISSUE_REQUIRED`.\n\n"
        "The package contains no benchmark prompt, target, acceptable-set, retrieval-output, or metric data. "
        "Creation is not execution authority.\n"
    ).encode()
    return payloads


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "warning-audit package missing")
    expected = build()
    actual_names = {path.name for path in root.iterdir() if path.is_file()}
    require(actual_names == set(expected), "warning-audit file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"warning-audit artifact drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_I3_V4_1_WARNING_AUDIT_BUILD_REPLAY"
    else:
        expected = build()
        require(not root.exists(), "refusing to overwrite warning-audit package")
        root.mkdir(parents=True)
        for name, data in expected.items():
            (root / name).write_bytes(data)
        status = "PASS_V7_I3_V4_1_WARNING_AUDIT_MATERIALISED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
