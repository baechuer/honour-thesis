#!/usr/bin/env python3
"""Materialise a target-blind, hash-bound readiness memo for six V7 gate records."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
U0323_NOTE = NC / "manifests" / "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_2026_09_08_v2" / "U0323_method_gate_note.md"
U0527_R001 = NC / "review" / "RQ2B-NC-phase5-v7-machine-b-microbatch-008-reissue-001-validation-2026-09-07-v1" / "summary.json"
U0527_R002 = NC / "review" / "RQ2B-NC-phase5-v7-machine-b-microbatch-008-reissue-002-validation-2026-09-07-v1" / "summary.json"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_gate_docket_readiness_2026_09_08_v1"


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_json_prefix_with_preserved_suffix(path: Path) -> tuple[dict[str, Any], str]:
    """Read one historical JSON object without rewriting its known literal suffix."""
    text = path.read_text(encoding="utf-8")
    value, offset = json.JSONDecoder().raw_decode(text)
    suffix = text[offset:]
    if suffix not in ("", "\n", "\\n"):
        raise ValueError(f"unexpected non-JSON suffix in {path}: {suffix!r}")
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object prefix in {path}")
    return value, suffix


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite frozen gate-docket readiness package: {OUTPUT}")
    docket = load_jsonl(INTEGRATION / "gate_docket.jsonl")
    expected = {
        "RQ2B-P4-V7-U0323": "historical_REOPEN_PACKET_method_gate_requires_user_decision",
        "RQ2B-P4-V7-U0527": "both_lanes_source_anchor_or_rationale_drift",
        "RQ2B-P4-V7-U0979": "machine_a_reviewer_B_identity_or_cryptographic_binding_drift",
        "RQ2B-P4-V7-U1068": "machine_a_reviewer_B_raw_return_missing",
        "RQ2B-P4-V7-U1078": "machine_a_reviewer_B_identity_or_cryptographic_binding_drift",
        "RQ2B-P4-V7-U1157": "machine_a_both_raw_returns_missing",
    }
    by_id = {row["batch_id"]: row for row in docket}
    if set(by_id) != set(expected) or any(by_id[bid]["gate_reason"] != reason for bid, reason in expected.items()):
        raise ValueError("historical gate-docket identity/reason drift")
    u0527_r001, u0527_r001_suffix = load_json_prefix_with_preserved_suffix(U0527_R001)
    u0527_r002, u0527_r002_suffix = load_json_prefix_with_preserved_suffix(U0527_R002)
    if u0527_r001["status"] != "PARTIAL_INVALID_PRESERVE_ORIGINAL_LANE_B_REISSUE_REQUIRED":
        raise ValueError("U0527 R001 state drift")
    if u0527_r001["lanes"]["A"]["validation"] != "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_REISSUE_RETURN_VALIDATION":
        raise ValueError("U0527 R001 A state drift")
    if u0527_r002["status"] != "PENDING_REISSUE_REQUIRES_FRESH_TARGET_BLIND_REVIEWER" or u0527_r002["invalid_lane"] != "B":
        raise ValueError("U0527 R002 state drift")

    instructions = {
        "RQ2B-P4-V7-U0323": {
            "classification": "SUBSTANTIVE_CONSTRUCT_METHOD_GATE",
            "current_evidence": "Historical sealed coordinator records materially incompatible requested workflows; not an anchor, schema, hash, path, or byte-preservation defect.",
            "permitted_next_action": "Explicitly defer/exclude from the V7 frozen-library closure, or approve a prospective method amendment followed by fresh review. A same-packet A+B reissue is not a mechanical repair.",
            "requires_user_method_decision": True,
        },
        "RQ2B-P4-V7-U0527": {
            "classification": "REISSUABLE_LANE_B_VALIDATION_DRIFT",
            "current_evidence": "Both canonical raw lanes are invalid. Reissue-001 A validates; both recorded B attempts remain invalid. All raw returns are preserved.",
            "permitted_next_action": "After the U0323 method disposition, issue one fresh target-blind B-lane reissue against the unchanged frozen packet, independent of retained reissue-001 A; otherwise explicitly defer/exclude.",
            "requires_user_method_decision": True,
        },
        "RQ2B-P4-V7-U0979": {
            "classification": "REISSUABLE_LANE_B_BINDING_DRIFT",
            "current_evidence": "A active raw return validates; B identity/cryptographic binding drift prevents B selection.",
            "permitted_next_action": "Fresh target-blind B-lane reissue on the unchanged frozen packet, or explicit defer/exclude.",
            "requires_user_method_decision": False,
        },
        "RQ2B-P4-V7-U1068": {
            "classification": "REISSUABLE_LANE_B_RAW_MISSING",
            "current_evidence": "A active raw return validates; B raw return is absent at the frozen Machine-A source commit.",
            "permitted_next_action": "Fresh target-blind B-lane reissue on the unchanged frozen packet, or explicit defer/exclude.",
            "requires_user_method_decision": False,
        },
        "RQ2B-P4-V7-U1078": {
            "classification": "REISSUABLE_LANE_B_BINDING_DRIFT",
            "current_evidence": "A active raw return validates; B identity/cryptographic binding drift prevents B selection.",
            "permitted_next_action": "Fresh target-blind B-lane reissue on the unchanged frozen packet, or explicit defer/exclude.",
            "requires_user_method_decision": False,
        },
        "RQ2B-P4-V7-U1157": {
            "classification": "REISSUABLE_WHOLE_GROUP_RAW_MISSING",
            "current_evidence": "Neither A nor B raw return is present at the frozen Machine-A source commit.",
            "permitted_next_action": "Fresh independent target-blind A+B reissue on the unchanged frozen packet, or explicit defer/exclude.",
            "requires_user_method_decision": False,
        },
    }
    rows = []
    for batch_id in sorted(expected):
        row = by_id[batch_id]
        rows.append({
            "batch_id": batch_id,
            "blind_packet_id": row["blind_packet_id"],
            "owner_machine": row["owner_machine"],
            "active_return_lane_count": row["active_return_lane_count"],
            "historical_gate_reason": row["gate_reason"],
            **instructions[batch_id],
            "closure_state": "PENDING_EXPLICIT_DISPOSITION",
        })
    OUTPUT.mkdir(parents=True)
    write_jsonl(OUTPUT / "target_blind_gate_docket_reconciliation.jsonl", rows)
    report = {
        "schema_version": "rq2b_nc_phase5_v7_gate_docket_readiness_v1",
        "status": "PASS_TARGET_BLIND_GATE_DOCKET_EVIDENCE_CONSOLIDATED_PENDING_USER_METHOD_DECISION",
        "claim_boundary": "Target-blind gate evidence only; no target join, acceptable-set decision, library update, retrieval result, metric, thesis result update, or K change.",
        "counts": {
            "gate_records": len(rows),
            "substantive_construct_method_gates": 1,
            "reissuable_mechanical_or_validation_gates": 5,
            "requires_user_method_decision": sum(row["requires_user_method_decision"] for row in rows),
        },
        "bound_inputs": {
            "historical_mechanical_integration_gate_docket": str((INTEGRATION / "gate_docket.jsonl").relative_to(WORKSPACE)),
            "historical_mechanical_integration_gate_docket_sha256": sha_path(INTEGRATION / "gate_docket.jsonl"),
            "u0323_method_gate_note": str(U0323_NOTE.relative_to(WORKSPACE)),
            "u0323_method_gate_note_sha256": sha_path(U0323_NOTE),
            "u0527_reissue_001_validation": str(U0527_R001.relative_to(WORKSPACE)),
            "u0527_reissue_001_validation_sha256": sha_path(U0527_R001),
            "u0527_reissue_001_non_json_suffix_repr": repr(u0527_r001_suffix),
            "u0527_reissue_002_validation": str(U0527_R002.relative_to(WORKSPACE)),
            "u0527_reissue_002_validation_sha256": sha_path(U0527_R002),
            "u0527_reissue_002_non_json_suffix_repr": repr(u0527_r002_suffix),
        },
        "stop_boundary": "No group is finalised by this package. Target join and acceptable-set/library closure require an explicit disposition for all six records, then master-SOP readiness verification.",
    }
    write_json(OUTPUT / "integrity_report.json", report)
    (OUTPUT / "integrity_report.md").write_text(
        "# V7 target-blind gate-docket readiness\n\n"
        "- Gate records: 6\n"
        "- Substantive construct/method gate: 1 (`U0323`)\n"
        "- Reissuable mechanical or validation gates: 5\n"
        "- User method decisions required: 2 (`U0323`, `U0527`)\n\n"
        "This package consolidates existing target-blind evidence only. It neither joins targets nor creates an acceptable set. `U0323` cannot be repaired by a same-packet reissue. The five reissuable records remain held until their allowed reissue/defer path is explicitly selected.\n",
        encoding="utf-8",
    )
    (OUTPUT / "README.md").write_text(
        "# V7 gate-docket readiness\n\n"
        "Reproduce with:\n\n```sh\npython3 skill_benchmark/scripts/materialise_rq2b_nc_phase5_v7_gate_docket_readiness.py\n```\n\n"
        "The script refuses to overwrite a frozen package and verifies the source docket, U0323 method-gate note, and U0527 reissue validation states. It contains no target identity, gold, retrieval outcome, acceptable-set, library outcome, or K change.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
