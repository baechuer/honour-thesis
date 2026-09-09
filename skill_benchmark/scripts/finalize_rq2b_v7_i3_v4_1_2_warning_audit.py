#!/usr/bin/env python3
"""Finalize the post-repair V4.1.2 source-only warning audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from build_rq2b_v7_i3_v4_1_2_warning_audit import (
    OUTPUT as AUDIT,
    RETURN_SCHEMA_VERSION,
    ROOT,
    verify as verify_audit,
)


OUTPUT = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase7_i3_v4_1_2_warning_audit_final_2026_09_09_v3"
)
RETURN_KEYS = {
    "schema_version", "issue_id", "reviewer_group", "source_sha256",
    "selected_output_sha256", "decision", "evidence_is_exact_and_complete",
    "warning_is_justified", "field_assignment_is_correct", "rationale",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def rows(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.splitlines()]


def rows_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join((canonical(value) + "\n").encode() for value in values)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def validate_return(packet: dict[str, Any], returned: dict[str, Any]) -> None:
    require(set(returned) == RETURN_KEYS, f"V4.1.2 warning return key drift: {packet['issue_id']}")
    require(returned["schema_version"] == RETURN_SCHEMA_VERSION, f"V4.1.2 warning return schema drift: {packet['issue_id']}")
    for field in ("issue_id", "reviewer_group", "source_sha256", "selected_output_sha256"):
        require(returned[field] == packet[field], f"V4.1.2 warning return binding drift: {packet['issue_id']}/{field}")
    require(returned["reviewer_group"] != packet["extractor_group"], f"own-extractor V4.1.2 warning review: {packet['issue_id']}")
    require(returned["decision"] == "ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION", f"V4.1.2 warning still requires reissue: {packet['issue_id']}")
    require(returned["evidence_is_exact_and_complete"] is True, f"V4.1.2 incomplete warning evidence: {packet['issue_id']}")
    require(returned["warning_is_justified"] is True, f"V4.1.2 unjustified warning: {packet['issue_id']}")
    require(returned["field_assignment_is_correct"] is True, f"V4.1.2 wrong field assignment: {packet['issue_id']}")
    require(isinstance(returned["rationale"], str) and returned["rationale"].strip(), f"V4.1.2 empty warning rationale: {packet['issue_id']}")


def build(*, replay: bool) -> dict[str, bytes]:
    verify_audit()
    audit_root = ROOT / AUDIT
    report_path = audit_root / "integrity_report.json"
    report = json.loads(report_path.read_bytes())
    docket_path = audit_root / "warning_docket.jsonl"
    carry_path = audit_root / "carried_forward_acceptances.jsonl"
    fresh_path = audit_root / "fresh_review_docket.jsonl"
    docket = rows(docket_path.read_bytes())
    carry = rows(carry_path.read_bytes())
    fresh = rows(fresh_path.read_bytes())
    require(len(docket) == 1221 and len(carry) == 1156 and len(fresh) == 65, "V4.1.2 warning cardinality drift")
    docket_by_id = {row["issue_id"]: row for row in docket}
    carry_by_id = {row["issue_id"]: row for row in carry}
    fresh_by_id = {row["issue_id"]: row for row in fresh}
    require(len(docket_by_id) == 1221 and set(carry_by_id).isdisjoint(fresh_by_id), "V4.1.2 warning identity drift")
    require(set(carry_by_id) | set(fresh_by_id) == set(docket_by_id), "V4.1.2 warning partition drift")

    return_payloads: dict[str, bytes] = {}
    returned_by_id: dict[str, dict[str, Any]] = {}
    return_bindings = []
    for group in (1, 2, 3):
        source = (
            ROOT / OUTPUT / "reviewer_returns" / f"reviewer_group_{group}_return.jsonl"
            if replay
            else audit_root / "returns" / f"reviewer_group_{group}_return.jsonl"
        )
        require(source.is_file(), f"missing V4.1.2 warning return: group {group}")
        data = source.read_bytes()
        returned = rows(data)
        assigned = rows((audit_root / f"reviewer_group_{group}_packet.jsonl").read_bytes())
        require(len(returned) == len(assigned), f"V4.1.2 warning return count drift: group {group}")
        require([row["issue_id"] for row in returned] == [row["issue_id"] for row in assigned], f"V4.1.2 warning return order drift: group {group}")
        for packet, result in zip(assigned, returned, strict=True):
            validate_return(packet, result)
            require(result["issue_id"] not in returned_by_id, f"duplicate V4.1.2 warning return: {result['issue_id']}")
            returned_by_id[result["issue_id"]] = result
        output_name = f"reviewer_returns/reviewer_group_{group}_return.jsonl"
        return_payloads[output_name] = data
        return_bindings.append({"reviewer_group": group, "path": str((OUTPUT / output_name)), "sha256": sha(data), "rows": len(returned)})
    require(set(returned_by_id) == set(fresh_by_id), "V4.1.2 fresh warning return coverage drift")

    final_rows = []
    for issue_id in sorted(docket_by_id):
        packet = docket_by_id[issue_id]
        if issue_id in carry_by_id:
            evidence = carry_by_id[issue_id]
            decision_source = "EXACT_SOURCE_AND_CANONICAL_WARNING_SIGNATURE_CARRY_FORWARD"
        else:
            evidence = returned_by_id[issue_id]
            decision_source = "FRESH_CROSS_GROUP_SOURCE_ONLY_REVIEW"
        final_rows.append({
            "schema_version": "rq2b-v7-i3-v4.1-warning-audit-final-ledger-v1",
            "issue_id": issue_id,
            "batch_id": packet["batch_id"],
            "source_row_index": packet["source_row_index"],
            "skill_id": packet["skill_id"],
            "source_sha256": packet["source_sha256"],
            "selected_output_sha256": packet["selected_output_sha256"],
            "extractor_group": packet["extractor_group"],
            "reviewer_group": packet["reviewer_group"],
            "warning_code": packet["warning"]["code"],
            "decision": "ACCEPT_AS_DOCUMENTED_SOURCE_EXCEPTION",
            "decision_source": decision_source,
            "review": evidence,
        })
    final_data = rows_bytes(final_rows)
    payloads = {**return_payloads, "warning_disposition_ledger.jsonl": final_data}
    final_report = {
        "schema_version": "rq2b-v7-i3-v4.1-warning-audit-final-report-v1",
        "state": "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA",
        "formal_execution_ready": False,
        "counts": {
            "selected_batches": 95,
            "sources": 3798,
            "warning_issues": 1221,
            "accepted": 1221,
            "reissue_required": 0,
            "carried_forward_exact_acceptances": 1156,
            "fresh_cross_group_acceptances": 65,
            "decision_sources": dict(sorted(Counter(row["decision_source"] for row in final_rows).items())),
        },
        "bindings": {
            "warning_build_report_sha256": sha(report_path.read_bytes()),
            "warning_docket_sha256": sha(docket_path.read_bytes()),
            "carried_forward_acceptances_sha256": sha(carry_path.read_bytes()),
            "fresh_review_docket_sha256": sha(fresh_path.read_bytes()),
            "final_ledger_sha256": sha(final_data),
            "reviewer_returns": return_bindings,
            "finalizer_sha256": sha(Path(__file__).read_bytes()),
        },
        "rules": report["rules"],
        "boundary": "Warning disposition is source-only extraction QA, not selector authority, retrieval performance, or evidence for the future scale-out.",
    }
    payloads["integrity_report.json"] = json_bytes(final_report)
    payloads["README.md"] = (
        "# V7 I3 V4.1.2 warning audit final v2\n\n"
        "All 1,221 current warnings are accepted: 1,156 by exact immutable carry-forward and 65 by fresh cross-group source-only review. Replay verifies every binding. This is not experiment authority.\n"
    ).encode()
    return payloads


def verify() -> None:
    root = ROOT / OUTPUT
    require(root.is_dir(), "V4.1.2 warning final package missing")
    expected = build(replay=True)
    actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    require(actual == set(expected), "V4.1.2 warning final file-set drift")
    for name, data in expected.items():
        require((root / name).read_bytes() == data, f"V4.1.2 warning final drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / OUTPUT
    if args.verify:
        verify()
        status = "PASS_V7_I3_V4_1_2_WARNING_FINAL_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite V4.1.2 warning final package")
        payloads = build(replay=False)
        staging = output.parent / f".{output.name}.staging-{os.getpid()}"
        require(not staging.exists(), "stale V4.1.2 warning final staging directory")
        for name, data in payloads.items():
            path = staging / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        staging.rename(output)
        status = "PASS_V7_I3_V4_1_2_WARNING_FINAL_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
