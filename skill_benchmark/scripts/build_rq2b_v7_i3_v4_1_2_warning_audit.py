#!/usr/bin/env python3
"""Build the post-repair V4.1.2 warning audit with exact carry-forward."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from build_rq2b_v7_i3_v4_1_warning_audit import warning_pairs
from build_rq2b_v7_i3_v4_1_2_warning_repair_integration import (
    OUTPUT_DIR as INTEGRATION,
    ROOT,
    verify as verify_integration,
)
from prepare_rq2b_v7_i3_full_reextraction_v4_1 import CACHE, build as build_inputs


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_2_warning_audit_2026_09_09_v3"
)
OLD_AUDIT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_warning_audit_2026_09_09_v1"
)
OLD_FINAL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_warning_audit_final_2026_09_09_v1"
)
SCHEMA_VERSION = "rq2b-v7-i3-v4.1.2-warning-audit-packet-v2"
RETURN_SCHEMA_VERSION = "rq2b-v7-i3-v4.1.2-warning-audit-return-v2"
FULL_REEXTRACTION = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_full_reextraction_2026_09_09_v4_1"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha(value: Any) -> str:
    return sha(canonical(value).encode())


def rows(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join((canonical(value) + "\n").encode() for value in values)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def warning_signature(source_sha256: str, warning: dict[str, Any]) -> str:
    return canonical_sha({"source_sha256": source_sha256, "warning": warning})


def build() -> dict[str, bytes]:
    verify_integration()
    integration_root = ROOT / INTEGRATION
    selection_path = integration_root / "selection_v2_ledger.jsonl"
    integration_report_path = integration_root / "integrity_report.json"
    selections = rows(selection_path.read_bytes())
    require(len(selections) == 95, "V4.1.2 selection coverage drift")

    assignments_path = ROOT / FULL_REEXTRACTION / "full_reextraction_assignment_manifest.jsonl"
    assignments = rows(assignments_path.read_bytes())
    assignment_by_batch = {row["batch_id"]: row for row in assignments}
    require(len(assignments) == len(assignment_by_batch) == 95, "V4.1.2 assignment coverage drift")
    _, input_payloads = build_inputs()

    old_docket_path = ROOT / OLD_AUDIT / "warning_docket.jsonl"
    old_final_path = ROOT / OLD_FINAL / "warning_disposition_ledger.jsonl"
    old_packets = {row["issue_id"]: row for row in rows(old_docket_path.read_bytes())}
    old_final = rows(old_final_path.read_bytes())
    old_accept_by_signature: dict[str, dict[str, Any]] = {}
    for disposition in old_final:
        if disposition["decision"] != "ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION":
            continue
        packet = old_packets[disposition["issue_id"]]
        signature = warning_signature(packet["source_sha256"], packet["warning"])
        require(signature not in old_accept_by_signature, "old accepted warning signature collision")
        old_accept_by_signature[signature] = disposition

    issues: list[dict[str, Any]] = []
    selected_bindings = []
    for selection in sorted(selections, key=lambda row: row["batch_id"]):
        batch_id = selection["batch_id"]
        assignment = assignment_by_batch[batch_id]
        input_name = str(Path(assignment["input_path"]).relative_to(CACHE))
        input_data = input_payloads[input_name]
        require(sha(input_data) == assignment["input_sha256"], f"V4.1.2 input drift: {batch_id}")
        output_path = ROOT / selection["selected_output_path"]
        output_data = output_path.read_bytes()
        require(sha(output_data) == selection["selected_output_sha256"], f"V4.1.2 output drift: {batch_id}")
        input_rows, output_rows = rows(input_data), rows(output_data)
        require(len(input_rows) == len(output_rows) == assignment["row_count"], f"V4.1.2 row drift: {batch_id}")
        for source, output in zip(input_rows, output_rows, strict=True):
            require(source["skill_id"] == output["skill_id"], f"V4.1.2 skill drift: {batch_id}")
            for local_id, warning in warning_pairs(output):
                evidence = warning["evidence"]
                require(bool(evidence) and evidence in source["text"], f"V4.1.2 warning evidence drift: {batch_id}/{source['skill_id']}/{local_id}")
                signature = warning_signature(source["source_sha256"], warning)
                issue_seed = {
                    "batch_id": batch_id,
                    "source_row_index": source["source_row_index"],
                    "skill_id": source["skill_id"],
                    "warning_signature": signature,
                    "selected_output_sha256": selection["selected_output_sha256"],
                }
                issues.append({
                    "schema_version": SCHEMA_VERSION,
                    "issue_id": "I3W2-" + canonical_sha(issue_seed)[:20],
                    "batch_id": batch_id,
                    "extractor_group": assignment["extractor_group"],
                    "reviewer_group": None,
                    "source_row_index": source["source_row_index"],
                    "skill_id": source["skill_id"],
                    "source_sha256": source["source_sha256"],
                    "source_text": source["text"],
                    "name": source["name"],
                    "description": source["description"],
                    "extracted_fields": output["fields"],
                    "warning": warning,
                    "warning_signature_sha256": signature,
                    "selected_output_sha256": selection["selected_output_sha256"],
                    "review_boundary": "Source-only V4.1.2 warning review. No benchmark prompt, target, acceptable set, retrieval output, metric, or experiment result may be inspected.",
                })
        selected_bindings.append({
            "batch_id": batch_id,
            "input_sha256": assignment["input_sha256"],
            "selected_output_sha256": selection["selected_output_sha256"],
        })
    require(len(issues) == len({row["issue_id"] for row in issues}) == len({row["warning_signature_sha256"] for row in issues}), "V4.1.2 warning identity collision")

    carry, fresh = [], []
    load = Counter({1: 0, 2: 0, 3: 0})
    for issue in sorted(issues, key=lambda row: row["issue_id"]):
        previous = old_accept_by_signature.get(issue["warning_signature_sha256"])
        if previous is not None:
            carry.append({
                "schema_version": "rq2b-v7-i3-v4.1.2-warning-acceptance-carry-forward-v1",
                "issue_id": issue["issue_id"],
                "warning_signature_sha256": issue["warning_signature_sha256"],
                "source_sha256": issue["source_sha256"],
                "selected_output_sha256": issue["selected_output_sha256"],
                "previous_issue_id": previous["issue_id"],
                "previous_decision": previous["decision"],
                "previous_review_sha256": canonical_sha(previous["review"]),
                "decision": "ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION",
                "carry_forward_rule": "EXACT_SOURCE_SHA_AND_CANONICAL_WARNING_SIGNATURE_MATCH",
            })
            continue
        eligible = [group for group in (1, 2, 3) if group != issue["extractor_group"]]
        group = min(eligible, key=lambda value: (load[value], value))
        issue["reviewer_group"] = group
        load[group] += 1
        fresh.append(issue)

    payloads: dict[str, bytes] = {
        "warning_docket.jsonl": rows_bytes(sorted(issues, key=lambda row: row["issue_id"])),
        "carried_forward_acceptances.jsonl": rows_bytes(carry),
        "fresh_review_docket.jsonl": rows_bytes(fresh),
    }
    for group in (1, 2, 3):
        group_rows = [row for row in fresh if row["reviewer_group"] == group]
        payloads[f"reviewer_group_{group}_packet.jsonl"] = rows_bytes(group_rows)
    payloads["reviewer_return_schema.json"] = json_bytes({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "issue_id", "reviewer_group", "source_sha256", "selected_output_sha256", "decision", "evidence_is_exact_and_complete", "warning_is_justified", "field_assignment_is_correct", "rationale"],
        "properties": {
            "schema_version": {"const": RETURN_SCHEMA_VERSION},
            "issue_id": {"type": "string", "pattern": "^I3W2-[0-9a-f]{20}$"},
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
    report = {
        "schema_version": "rq2b-v7-i3-v4.1-warning-audit-build-report-v1",
        "state": "MATERIALISED_PENDING_SOURCE_ONLY_WARNING_RETURNS" if fresh else "PASS_NO_WARNINGS_REQUIRING_DISPOSITION",
        "formal_execution_ready": False,
        "counts": {
            "selected_batches": 95,
            "sources": 3798,
            "unique_warning_issues": len(issues),
            "carried_forward_exact_acceptances": len(carry),
            "fresh_review_issues": len(fresh),
            "by_reviewer_group": {str(group): load[group] for group in (1, 2, 3)},
        },
        "bindings": {
            "integration_report_sha256": sha(integration_report_path.read_bytes()),
            "assignment_manifest_sha256": sha(assignments_path.read_bytes()),
            "selection_ledger_sha256": sha(selection_path.read_bytes()),
            "old_warning_docket_sha256": sha(old_docket_path.read_bytes()),
            "old_final_ledger_sha256": sha(old_final_path.read_bytes()),
            "warning_docket_sha256": sha(payloads["warning_docket.jsonl"]),
            "carried_forward_acceptances_sha256": sha(payloads["carried_forward_acceptances.jsonl"]),
            "fresh_review_docket_sha256": sha(payloads["fresh_review_docket.jsonl"]),
            "reviewer_return_schema_sha256": sha(payloads["reviewer_return_schema.json"]),
            "selected_batches_sha256": canonical_sha(selected_bindings),
            "builder_sha256": sha(Path(__file__).read_bytes()),
        },
        "rules": {
            "old_acceptance_carry_forward_requires_exact_source_and_warning_signature": True,
            "old_reissue_decisions_never_carried_forward": True,
            "changed_or_new_warnings_require_fresh_cross_group_review": True,
            "own_extractor_review_forbidden": True,
            "no_selector_or_result_access": True,
        },
    }
    payloads["integrity_report.json"] = json_bytes(report)
    payloads["README.md"] = (
        "# V7 I3 V4.1.2 warning audit v3\n\n"
        "Unchanged accepted warnings are carried forward only when source SHA and the complete canonical warning object match exactly. Old reissue decisions are never inherited. Every new or changed warning is cross-assigned for fresh source-only review and may fail closed with REISSUE_REQUIRED. V2 is preserved as a superseded schema-only build because its return schema accidentally allowed only acceptance. No experiment is run here.\n"
    ).encode()
    return payloads


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "V4.1.2 warning audit missing")
    expected = build()
    actual = {path.name for path in root.iterdir() if path.is_file()}
    require(actual == set(expected), "V4.1.2 warning-audit file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"V4.1.2 warning-audit drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_I3_V4_1_2_WARNING_AUDIT_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite V4.1.2 warning audit")
        payloads = build()
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale V4.1.2 warning-audit staging directory")
        staging.mkdir(parents=True)
        for name, data in payloads.items():
            (staging / name).write_bytes(data)
        staging.rename(output)
        status = "PASS_V7_I3_V4_1_2_WARNING_AUDIT_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
