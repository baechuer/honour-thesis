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
SELECTION = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_warning_return_selection_2026_09_09_v1/"
    "reviewer_return_selection_ledger.jsonl"
)
RETURN_KEYS = {
    "schema_version", "issue_id", "reviewer_group", "source_sha256",
    "reviewer_slot", "selected_output_sha256", "decision", "evidence_is_exact_and_complete",
    "warning_is_justified", "field_assignment_is_correct", "rationale",
}
ALLOWED_DECISIONS = {"ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION", "REISSUE_REQUIRED"}
ALLOWED_SELECTION_REASON_CODES = {
    "REVIEWER_MISREAD_FROZEN_ROUTE_OUT_RULE",
    "REVIEWER_USED_NORMALISED_NOT_RAW_WARNING_EVIDENCE",
}
SELECTION_SCHEMA_VERSION = "rq2b-v7-i3-v4.1-warning-review-return-selection-v1"
SELECTION_KEYS = {
    "schema_version", "reviewer_group", "reviewer_slot",
    "canonical_original_path", "canonical_original_sha256",
    "selected_reissue_path", "selected_reissue_sha256", "reason_code",
    "packet_or_extraction_changed",
}


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


def selected_return_paths(audit_root: Path) -> tuple[dict[tuple[int, int], dict], bytes | None]:
    """Load an explicit, hash-bound reviewer-return reissue ledger if present.

    A reviewer correction never overwrites the first return.  Only the exact
    selected reissue named here is consumed; the original remains immutable
    evidence.  The ledger may correct reviewer interpretation only and cannot
    change a packet or an extraction.
    """
    path = ROOT / SELECTION
    if not path.is_file():
        return {}, None
    data = path.read_bytes()
    values = rows(data)
    selected: dict[tuple[int, int], dict] = {}
    for row in values:
        require(set(row) == SELECTION_KEYS, "warning return selection schema fields drift")
        require(row["schema_version"] == SELECTION_SCHEMA_VERSION, "warning return selection schema version drift")
        group, slot = row["reviewer_group"], row["reviewer_slot"]
        require(group in (1, 2, 3) and isinstance(slot, int) and slot > 0, "warning return selection group/slot drift")
        key = (group, slot)
        require(key not in selected, f"duplicate warning return selection: {group}:{slot:03d}")
        original = ROOT / row["canonical_original_path"]
        reissue = ROOT / row["selected_reissue_path"]
        expected_original = audit_root / "returns" / f"reviewer_group_{group}_slot_{slot:03d}_return.jsonl"
        expected_reissue = audit_root / "reviewer_return_reissues" / f"reviewer_group_{group}_slot_{slot:03d}_return_reissue_001.jsonl"
        require(original.resolve() == expected_original.resolve(), f"warning original selection path drift: {group}:{slot:03d}")
        require(reissue.resolve() == expected_reissue.resolve(), f"warning reissue selection path drift: {group}:{slot:03d}")
        require(original.is_file() and sha(original.read_bytes()) == row["canonical_original_sha256"], f"warning original selection hash drift: {group}:{slot:03d}")
        require(reissue.is_file() and sha(reissue.read_bytes()) == row["selected_reissue_sha256"], f"warning reissue selection hash drift: {group}:{slot:03d}")
        require(row["reason_code"] in ALLOWED_SELECTION_REASON_CODES, f"warning reissue reason drift: {group}:{slot:03d}")
        require(row["packet_or_extraction_changed"] is False, f"warning reissue cannot change packet/extraction: {group}:{slot:03d}")
        selected[key] = row
    return selected, data


def build() -> dict[str, bytes]:
    verify_audit()
    audit_root = ROOT / AUDIT
    docket_path = audit_root / "warning_docket.jsonl"
    docket = rows(docket_path.read_bytes())
    packet_by_issue = {row["issue_id"]: row for row in docket}
    require(len(packet_by_issue) == len(docket), "duplicate warning docket issue ID")
    selected_returns, selection_data = selected_return_paths(audit_root)

    returned_by_issue: dict[str, dict] = {}
    return_bindings = []
    expected_return_names: set[str] = set()
    for group in (1, 2, 3):
        group_rows = [row for row in docket if row["reviewer_group"] == group]
        slot_ids = sorted({row["reviewer_slot"] for row in group_rows})
        for slot in slot_ids:
            expected = [row for row in group_rows if row["reviewer_slot"] == slot]
            canonical_path = audit_root / "returns" / f"reviewer_group_{group}_slot_{slot:03d}_return.jsonl"
            expected_return_names.add(canonical_path.name)
            require(canonical_path.is_file(), f"missing warning return: reviewer group {group} slot {slot:03d}")
            selection = selected_returns.get((group, slot))
            path = ROOT / selection["selected_reissue_path"] if selection else canonical_path
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
                "canonical_original_path": str(canonical_path.relative_to(ROOT)),
                "canonical_original_sha256": sha(canonical_path.read_bytes()),
                "selection": "TRACEABLE_REISSUE_001" if selection else "CANONICAL_ORIGINAL",
            })
    returns_root = audit_root / "returns"
    actual_return_names = (
        {path.name for path in returns_root.iterdir() if path.is_file()}
        if returns_root.is_dir() else set()
    )
    require(actual_return_names == expected_return_names, "warning return file-set drift")
    expected_slots = {(row["reviewer_group"], row["reviewer_slot"]) for row in docket}
    require(set(selected_returns) <= expected_slots, "warning return selection names an unknown slot")
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
    payloads = {
        "warning_disposition_ledger.jsonl": ledger_data,
        "integrity_report.json": json_bytes(report),
        "README.md": (
            "# V7 I3 V4.1 warning-audit finalization\n\n"
            "This immutable package binds the cross-group source-only warning returns. "
            "A PASS state permits the selected outputs to proceed to merge and fresh blinded QA; "
            "it does not permit formal retrieval execution.\n"
        ).encode(),
    }
    if selection_data is not None:
        payloads["reviewer_return_selection_ledger.jsonl"] = selection_data
        report["bindings"]["reviewer_return_selection_ledger_sha256"] = sha(selection_data)
        report["counts"]["selected_reviewer_return_reissues"] = len(selected_returns)
        payloads["integrity_report.json"] = json_bytes(report)
    return payloads


def verify() -> str:
    root = ROOT / OUTPUT
    require(root.is_dir(), "warning-audit final package missing")
    expected = build()
    require({path.name for path in root.iterdir() if path.is_file()} == set(expected), "warning-audit final file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"warning-audit final artifact drift: {name}")
    report = json.loads((root / "integrity_report.json").read_bytes())
    require(
        report["state"] in {
            "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA",
            "BLOCKED_TRACEABLE_REISSUE_REQUIRED_NEW_SELECTION_AND_WARNING_AUDIT_VERSION",
        },
        "warning-audit final replay has an unknown state",
    )
    return report["state"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument(
        "--freeze-blocked-evidence",
        action="store_true",
        help="Materialise an immutable blocked receipt while preserving all returns; never authorises merge.",
    )
    args = parser.parse_args()
    root = ROOT / OUTPUT
    if args.verify:
        state = verify()
        status = (
            "PASS_V7_I3_V4_1_WARNING_AUDIT_FINAL_REPLAY"
            if state == "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA"
            else "PASS_V7_I3_V4_1_WARNING_AUDIT_BLOCKED_EVIDENCE_REPLAY"
        )
    else:
        expected = build()
        report = json.loads(expected["integrity_report.json"])
        if report["state"] != "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA":
            require(
                args.freeze_blocked_evidence,
                "refusing to freeze a blocked warning audit without --freeze-blocked-evidence",
            )
        require(not root.exists(), "refusing to overwrite warning-audit final package")
        root.mkdir(parents=True)
        for name, data in expected.items():
            (root / name).write_bytes(data)
        status = (
            "PASS_V7_I3_V4_1_WARNING_AUDIT_FINAL_CREATED"
            if report["state"] == "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA"
            else "PASS_V7_I3_V4_1_WARNING_AUDIT_BLOCKED_EVIDENCE_CREATED"
        )
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
