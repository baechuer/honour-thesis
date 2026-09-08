#!/usr/bin/env python3
"""Finalize the cross-group V4.1 source-only warning audit."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from build_rq2b_v7_i3_v4_1_warning_audit import (
    OUTPUT as AUDIT,
    RETURN_SCHEMA_VERSION,
    ROOT,
    verify as verify_audit,
)


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_warning_audit_final_2026_09_09_v1"
)
RETURN_KEYS = {
    "schema_version", "issue_id", "reviewer_group", "source_sha256",
    "reviewer_slot", "selected_output_sha256", "decision", "evidence_is_exact_and_complete",
    "warning_is_justified", "field_assignment_is_correct", "rationale",
}
ALLOWED_DECISIONS = {"ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION", "REISSUE_REQUIRED"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: list[dict]) -> bytes:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in values
    ).encode()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def validate_return(packet: dict, returned: dict) -> None:
    require(set(returned) == RETURN_KEYS, f"warning return schema fields drift: {packet['issue_id']}")
    require(returned["schema_version"] == RETURN_SCHEMA_VERSION, f"warning return schema version: {packet['issue_id']}")
    for field in ("issue_id", "reviewer_group", "reviewer_slot", "source_sha256", "selected_output_sha256"):
        require(returned[field] == packet[field], f"warning return binding drift: {packet['issue_id']} {field}")
    require(returned["reviewer_group"] != packet["extractor_group"], f"own-extractor warning return: {packet['issue_id']}")
    require(returned["decision"] in ALLOWED_DECISIONS, f"invalid warning decision: {packet['issue_id']}")
    require(isinstance(returned["rationale"], str) and returned["rationale"].strip(), f"empty warning rationale: {packet['issue_id']}")
    for field in ("evidence_is_exact_and_complete", "warning_is_justified", "field_assignment_is_correct"):
        require(isinstance(returned[field], bool), f"non-boolean warning audit field: {packet['issue_id']} {field}")
    if returned["decision"] == "ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION":
        require(
            returned["evidence_is_exact_and_complete"]
            and returned["warning_is_justified"]
            and returned["field_assignment_is_correct"],
            f"accepted warning lacks unanimous source checks: {packet['issue_id']}",
        )


def build() -> dict[str, bytes]:
    verify_audit()
    audit_root = ROOT / AUDIT
    docket_path = audit_root / "warning_docket.jsonl"
    docket = rows(docket_path.read_bytes())
    packet_by_issue = {row["issue_id"]: row for row in docket}
    require(len(packet_by_issue) == len(docket), "duplicate warning docket issue ID")

    returned_by_issue: dict[str, dict] = {}
    return_bindings = []
    for group in (1, 2, 3):
        group_rows = [row for row in docket if row["reviewer_group"] == group]
        slot_ids = sorted({row["reviewer_slot"] for row in group_rows})
        for slot in slot_ids:
            expected = [row for row in group_rows if row["reviewer_slot"] == slot]
            path = audit_root / "returns" / f"reviewer_group_{group}_slot_{slot:03d}_return.jsonl"
            require(path.is_file(), f"missing warning return: reviewer group {group} slot {slot:03d}")
            data = path.read_bytes()
            returned = rows(data)
            require(len(returned) == len(expected), f"warning return count mismatch: reviewer group {group} slot {slot:03d}")
            require(len({row.get('issue_id') for row in returned}) == len(returned), f"duplicate warning return: group {group} slot {slot:03d}")
            expected_ids = {row["issue_id"] for row in expected}
            require({row.get("issue_id") for row in returned} == expected_ids, f"warning return coverage mismatch: group {group} slot {slot:03d}")
            for row in returned:
                packet = packet_by_issue[row["issue_id"]]
                validate_return(packet, row)
                require(row["issue_id"] not in returned_by_issue, f"warning returned more than once: {row['issue_id']}")
                returned_by_issue[row["issue_id"]] = row
            return_bindings.append({
                "reviewer_group": group,
                "reviewer_slot": slot,
                "path": str(path.relative_to(ROOT)),
                "sha256": sha(data),
                "rows": len(returned),
            })
    require(len(returned_by_issue) == len(docket), "warning return union does not cover docket")

    ledger = []
    decisions = Counter()
    for packet in sorted(docket, key=lambda row: row["issue_id"]):
        returned = returned_by_issue[packet["issue_id"]]
        decisions[returned["decision"]] += 1
        ledger.append({
            "schema_version": "rq2b-v7-i3-v4.1-warning-audit-final-ledger-v1",
            "issue_id": packet["issue_id"],
            "batch_id": packet["batch_id"],
            "source_row_index": packet["source_row_index"],
            "skill_id": packet["skill_id"],
            "source_sha256": packet["source_sha256"],
            "extractor_group": packet["extractor_group"],
            "reviewer_group": packet["reviewer_group"],
            "warning_code": packet["warning"]["code"],
            "selected_output_sha256": packet["selected_output_sha256"],
            "decision": returned["decision"],
            "review": returned,
        })
    ledger_data = rows_bytes(ledger)
    blocked = decisions["REISSUE_REQUIRED"]
    report = {
        "schema_version": "rq2b-v7-i3-v4.1-warning-audit-final-report-v1",
        "state": (
            "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA"
            if blocked == 0 else
            "BLOCKED_TRACEABLE_REISSUE_REQUIRED_NEW_SELECTION_AND_WARNING_AUDIT_VERSION"
        ),
        "formal_execution_ready": False,
        "counts": {
            "warning_issues": len(docket),
            "returns": len(returned_by_issue),
            "decisions": dict(sorted(decisions.items())),
        },
        "bindings": {
            "warning_docket_sha256": sha(docket_path.read_bytes()),
            "final_ledger_sha256": sha(ledger_data),
            "returns": return_bindings,
            "finalizer_sha256": sha(Path(__file__).read_bytes()),
        },
        "boundary": (
            "This closes warning disposition only. It is not the fresh 120-row blinded semantic QA "
            "and does not authorise retrieval, reranking, metrics, or thesis-result updates."
        ),
    }
    return {
        "warning_disposition_ledger.jsonl": ledger_data,
        "integrity_report.json": json_bytes(report),
        "README.md": (
            "# V7 I3 V4.1 warning-audit finalization\n\n"
            "This immutable package binds the cross-group source-only warning returns. "
            "A PASS state permits the selected outputs to proceed to merge and fresh blinded QA; "
            "it does not permit formal retrieval execution.\n"
        ).encode(),
    }


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "warning-audit final package missing")
    expected = build()
    require({path.name for path in root.iterdir() if path.is_file()} == set(expected), "warning-audit final file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"warning-audit final artifact drift: {name}")
    report = json.loads((root / "integrity_report.json").read_bytes())
    require(
        report["state"] == "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA",
        "warning-audit final replay is not PASS",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_I3_V4_1_WARNING_AUDIT_FINAL_REPLAY"
    else:
        expected = build()
        report = json.loads(expected["integrity_report.json"])
        require(
            report["state"] == "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA",
            "refusing to freeze a blocked warning audit; create traceable reissues and a new version",
        )
        require(not root.exists(), "refusing to overwrite warning-audit final package")
        root.mkdir(parents=True)
        for name, data in expected.items():
            (root / name).write_bytes(data)
        status = "PASS_V7_I3_V4_1_WARNING_AUDIT_FINAL_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
