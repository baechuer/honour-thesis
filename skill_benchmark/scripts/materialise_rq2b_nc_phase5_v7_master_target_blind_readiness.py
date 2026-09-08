#!/usr/bin/env python3
"""Freeze the V7 target-blind evidence readiness record under the master SOP.

The resulting package consolidates mechanical evidence only.  It deliberately
stops before a sealed target join, acceptable-set audit, library update,
retrieval/metric calculation, or thesis-results update.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
DIRECT = NC / "manifests" / "rq2b_nc_phase5_v7_direct_target_blind_reconciliation_2026_09_08_v1"
PROMPT = NC / "manifests" / "rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview_reconciliation_2026_09_08_v1"
GATE = NC / "manifests" / "rq2b_nc_phase5_v7_gate_reissue_final_reconciliation_2026_09_08_v1"
DISPOSITION = NC / "manifests" / "rq2b_nc_phase5_v7_gate_disposition_reissue_2026_09_08_v1"
V7 = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_master_target_blind_readiness_2026_09_08_v1"
FINAL_ADEQUACY = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE"}
FORBIDDEN_OUTPUT_KEYS = {"target_id", "target_identity", "gold_label", "retrieval_result", "source_full_skill"}


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def validate_no_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        if FORBIDDEN_OUTPUT_KEYS & set(value):
            raise ValueError("forbidden target/retrieval key in target-blind output")
        for child in value.values():
            validate_no_forbidden_keys(child)
    elif isinstance(value, list):
        for child in value:
            validate_no_forbidden_keys(child)


def packet_fields(batch_id: str, ledger_by_id: dict[str, dict[str, Any]], v7_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ledger = ledger_by_id[batch_id]
    v7 = v7_by_id[batch_id]
    if ledger["blind_packet_id"] != v7["blind_packet_id"]:
        raise ValueError(f"blind packet identity drift: {batch_id}")
    main = v7["sealed_main_packet"]
    tails = v7["sealed_tail_packets"]
    if main.get("candidate_count") != 6 or len(tails) != 2 or any(tail.get("candidate_count") != 1 for tail in tails):
        raise ValueError(f"K=6/two-tail V7 manifest shape drift: {batch_id}")
    return {
        "blind_packet_id": ledger["blind_packet_id"],
        "packet_input_sha256": ledger["packet_input_sha256"],
        "sealed_main_packet_sha256": main["packet_sha256"],
        "sealed_tail_packet_sha256s": [tail["packet_sha256"] for tail in tails],
    }


def normalise_reconciled_row(row: dict[str, Any], *, source_route: str, ledger_by_id: dict[str, dict[str, Any]], v7_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    batch_id = row["batch_id"]
    packet = packet_fields(batch_id, ledger_by_id, v7_by_id)
    if row["blind_packet_id"] != packet["blind_packet_id"]:
        raise ValueError(f"source reconciliation blind packet drift: {batch_id}")
    candidates = row["candidate_dispositions"]
    if len(candidates) != 8 or len({item["candidate_token"] for item in candidates}) != 8:
        raise ValueError(f"candidate partition drift: {batch_id}")
    if any(item["final_adequacy"] not in FINAL_ADEQUACY for item in candidates):
        raise ValueError(f"unresolved adequacy in purportedly reconciled group: {batch_id}")
    result = {
        "batch_id": batch_id,
        **packet,
        "source_route": source_route,
        "reconciliation_state": "TARGET_BLIND_RECONCILED_READY_FOR_SEALED_TARGET_JOIN",
        "candidate_dispositions": candidates,
    }
    validate_no_forbidden_keys(result)
    return result


def build_master_readiness() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    integration_rows = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    if len(integration_rows) != 2132:
        raise ValueError("integration ledger cardinality drift")
    lane_a = [row for row in integration_rows if row["reviewer_lane"] == "A"]
    ledger_by_id = {row["batch_id"]: row for row in lane_a}
    if len(lane_a) != 1066 or len(ledger_by_id) != 1066:
        raise ValueError("integration scope cardinality/identity drift")
    route_counts = Counter(row["group_route"] for row in lane_a)
    expected_routes = {"DIRECT_RECONCILIATION_ELIGIBLE": 228, "SEALED_COORDINATOR_ELIGIBLE": 832, "GATE_DOCKET": 6}
    if dict(route_counts) != expected_routes:
        raise ValueError(f"integration route drift: {dict(route_counts)}")
    v7_rows = load_jsonl(V7 / "unified_prompt_group_batch_manifest.jsonl")
    v7_by_id = {row["batch_id"]: row for row in v7_rows}
    if len(v7_by_id) != 1226 or not set(ledger_by_id) <= set(v7_by_id):
        raise ValueError("V7 manifest/scope drift")

    direct = load_jsonl(DIRECT / "target_blind_direct_group_reconciliation.jsonl")
    prompt = load_jsonl(PROMPT / "target_blind_group_reconciliation.jsonl")
    gate = load_jsonl(GATE / "target_blind_gate_reissue_final_reconciliation.jsonl")
    direct_ids, prompt_ids, gate_ids = ({row["batch_id"] for row in items} for items in (direct, prompt, gate))
    expected_direct = {row["batch_id"] for row in lane_a if row["group_route"] == "DIRECT_RECONCILIATION_ELIGIBLE"}
    expected_prompt = {row["batch_id"] for row in lane_a if row["group_route"] == "SEALED_COORDINATOR_ELIGIBLE"}
    expected_gate = {row["batch_id"] for row in lane_a if row["group_route"] == "GATE_DOCKET"}
    if direct_ids != expected_direct or prompt_ids != expected_prompt or not gate_ids <= expected_gate:
        raise ValueError("source reconciliation route/scope drift")
    if direct_ids & prompt_ids or direct_ids & gate_ids or prompt_ids & gate_ids:
        raise ValueError("source reconciliation groups overlap")
    if len(direct) != 228 or len(prompt) != 832 or len(gate) != 5:
        raise ValueError("source reconciliation cardinality drift")

    admin = load_jsonl(DISPOSITION / "sealed_admin_disposition_and_reissue_ledger.jsonl")
    excluded = [row for row in admin if row["disposition"] == "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE"]
    if len(excluded) != 1 or excluded[0]["batch_id"] != "RQ2B-P4-V7-U0323" or excluded[0].get("disposition_authority") != "USER_APPROVED_2026-09-08" or excluded[0].get("target_join_permitted") is not False:
        raise ValueError("U0323 user-approved exclusion disposition drift")
    u0323 = excluded[0]
    if u0323["batch_id"] not in expected_gate or u0323["batch_id"] in gate_ids:
        raise ValueError("U0323 gate/exclusion route drift")

    source_rows = [(direct, "DIRECT_EXACT_INDEPENDENT_AGREEMENT"), (prompt, "PROMPT_BOUND_COORDINATOR_REREVIEW"), (gate, "USER_APPROVED_GATE_REISSUE_RECONCILIATION")]
    master_rows: list[dict[str, Any]] = []
    for rows, route in source_rows:
        master_rows.extend(normalise_reconciled_row(row, source_route=route, ledger_by_id=ledger_by_id, v7_by_id=v7_by_id) for row in rows)
    excluded_row = {
        "batch_id": u0323["batch_id"],
        **packet_fields(u0323["batch_id"], ledger_by_id, v7_by_id),
        "source_route": "USER_APPROVED_METHOD_GATE_DISPOSITION",
        "reconciliation_state": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE",
        "exclusion_authority": u0323["disposition_authority"],
        "exclusion_reason": "SUBSTANTIVE_CONSTRUCT_METHOD_GATE; same-packet A+B reissue is not a mechanical repair.",
        "target_join_permitted": False,
    }
    validate_no_forbidden_keys(excluded_row)
    master_rows.append(excluded_row)
    master_rows.sort(key=lambda row: row["batch_id"])
    reconciled = [row for row in master_rows if row["reconciliation_state"] == "TARGET_BLIND_RECONCILED_READY_FOR_SEALED_TARGET_JOIN"]
    if len(master_rows) != 1066 or len({row["batch_id"] for row in master_rows}) != 1066 or {row["batch_id"] for row in master_rows} != set(ledger_by_id):
        raise ValueError("master coverage/disjointness drift")
    if len(reconciled) != 1065 or sum(len(row["candidate_dispositions"]) for row in reconciled) != 8520:
        raise ValueError("master reconciled evidence cardinality drift")
    adequacy_counts = Counter(item["final_adequacy"] for row in reconciled for item in row["candidate_dispositions"])
    report = {
        "schema_version": "rq2b_nc_phase5_v7_master_target_blind_readiness_v1",
        "status": "PASS_RQ2B_V7_TARGET_BLIND_AUDIT_EVIDENCE_READY_FOR_SEALED_TARGET_JOIN_EXCLUDING_U0323",
        "claim_boundary": "Target-blind mechanical evidence consolidation only. This is not a target join, acceptable-set audit, final library, retrieval result, metric, or thesis result; K remains 6 with two bounded tails.",
        "scope": {
            "mechanical_integration_scope_groups": 1066,
            "target_blind_reconciled_groups": 1065,
            "explicitly_deferred_excluded_groups": 1,
            "unresolved_or_blocked_groups": 0,
            "reconciled_candidate_dispositions": 8520,
            "u0323_exclusion": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE_BY_USER_APPROVAL_2026-09-08",
        },
        "route_counts": {"direct_exact_independent_groups": 228, "prompt_bound_rereview_groups": 832, "approved_gate_reissue_groups": 5, "user_method_gate_exclusions": 1},
        "target_blind_outcome_counts": dict(sorted(adequacy_counts.items())),
        "mechanical_checks": {
            "coverage_of_1066_group_integration_scope": "PASS",
            "source_route_disjointness": "PASS",
            "reconciled_group_packet_input_hash_and_k6_two_tail_shape": "PASS",
            "candidate_partition_eight_per_reconciled_group": "PASS",
            "no_unclear_or_reopen_in_reconciled_scope": "PASS",
            "target_blind_output_key_check": "PASS",
        },
        "bound_inputs": {
            "v7_unified_manifest": str((V7 / "unified_prompt_group_batch_manifest.jsonl").relative_to(WORKSPACE)),
            "v7_unified_manifest_sha256": sha_path(V7 / "unified_prompt_group_batch_manifest.jsonl"),
            "integration_ledger_sha256": sha_path(INTEGRATION / "integration_intake_ledger.jsonl"),
            "direct_reconciliation_integrity_sha256": sha_path(DIRECT / "integrity_report.json"),
            "prompt_bound_reconciliation_integrity_sha256": sha_path(PROMPT / "integrity_report.json"),
            "gate_reissue_final_reconciliation_integrity_sha256": sha_path(GATE / "integrity_report.json"),
            "user_gate_disposition_ledger_sha256": sha_path(DISPOSITION / "sealed_admin_disposition_and_reissue_ledger.jsonl"),
        },
        "next_permitted_step": "A separately controlled sealed target join and acceptable-set audit may now be planned for the 1,065 reconciled V7 groups only. U0323 remains outside V7 frozen-library closure unless a prospective method amendment is approved.",
        "prohibited_in_this_package": ["target join", "acceptable-set creation", "library update", "retrieval or metric calculation", "thesis-result update", "K=8 change"],
    }
    return master_rows, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen master readiness package: {output}")
    rows, report = build_master_readiness()
    output.mkdir(parents=True)
    write_jsonl(output / "master_target_blind_group_reconciliation.jsonl", rows)
    write_json(output / "integrity_report.json", report)
    (output / "integrity_report.md").write_text(
        "# V7 master target-blind readiness\n\n"
        "- Mechanical integration scope: 1,066 groups\n- Reconciled and ready for a future sealed target join: 1,065 groups\n- Explicitly deferred/excluded from V7 frozen-library closure: U0323 (1 group)\n- Unresolved or blocked groups: 0\n\n"
        "This freezes evidence readiness, not an acceptable set or final library. The next step, if approved, is a separately controlled sealed target join for the 1,065 reconciled groups only.\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# V7 master target-blind readiness\n\n"
        "Verify the frozen package with:\n\n"
        "```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_master_target_blind_readiness.py\n```\n\n"
        "The materialiser refuses to overwrite the frozen package. It must not be used to derive an acceptable set, update the library, or report retrieval/thesis results.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(output), "scope": report["scope"]}, sort_keys=True))


if __name__ == "__main__":
    main()
