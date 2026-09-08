#!/usr/bin/env python3
"""Consolidate every V7 group before the sealed token join.

The package joins no opaque candidate token to a source identity.  It merely
combines the 160 historically finalised V7 dispositions with the 1,065 newly
reconciled groups and the user-approved U0323 exclusion, so that the later
finaliser cannot accidentally construct a partial-library acceptable set.
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
V7 = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
V2 = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
STATE = NC / "manifests" / "rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_v20_v7_dispatch_freshness_replay" / "execution_state_reconciliation.json"
LEGACY = NC / "review" / "RQ2B-NC-phase4-v7-strict-unified-reconciliation-2026-09-05"
NEW = NC / "manifests" / "rq2b_nc_phase5_v7_master_target_blind_readiness_2026_09_08_v1"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_all_scope_target_blind_prejoin_reconciliation_2026_09_08_v1"
FINAL = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE"}


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def manifest_packet_fields(manifest: dict[str, Any]) -> dict[str, Any]:
    main, tails = manifest["sealed_main_packet"], manifest["sealed_tail_packets"]
    if main.get("candidate_count") != 6 or len(tails) != 2 or any(tail.get("candidate_count") != 1 for tail in tails):
        raise ValueError(f"K=6/two-tail drift: {manifest['batch_id']}")
    return {
        "blind_packet_id": manifest["blind_packet_id"],
        "v7_main_packet_id": main["packet_id"],
        "v7_main_packet_sha256": main["packet_sha256"],
        "v7_tail_packet_ids": [tail["packet_id"] for tail in tails],
        "v7_tail_packet_sha256s": [tail["packet_sha256"] for tail in tails],
    }


def validate_v7_freeze() -> dict[str, dict[str, Any]]:
    summary = json.loads((V7 / "summary.json").read_text(encoding="utf-8"))
    if summary.get("status") != "PASS_PHASE4_V7_STRICT_UNIFIED_BLIND_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS":
        raise ValueError("V7 summary status drift")
    for relative, expected in summary["outputs"].items():
        path = V7 / relative
        if not path.is_file() or sha_path(path) != expected:
            raise ValueError(f"V7 frozen output hash drift: {relative}")
    v2_summary = json.loads((V2 / "summary.json").read_text(encoding="utf-8"))
    if v2_summary.get("status") != "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS":
        raise ValueError("V2 audit-input status drift")
    for relative, expected in v2_summary["bound_inputs"].items():
        path = WORKSPACE / relative
        if not path.is_file() or sha_path(path) != expected:
            raise ValueError(f"V2 bound-input hash drift: {relative}")
    manifests = load_jsonl(V7 / "unified_prompt_group_batch_manifest.jsonl")
    by_id = {row["batch_id"]: row for row in manifests}
    if len(manifests) != 1226 or len(by_id) != 1226:
        raise ValueError("V7 manifest cardinality/identity drift")
    return by_id


def validate_dispositions(row: dict[str, Any], manifest: dict[str, Any]) -> None:
    if row.get("blind_packet_id") != manifest["blind_packet_id"]:
        raise ValueError(f"blind-packet drift: {manifest['batch_id']}")
    decisions = row.get("candidate_dispositions")
    if not isinstance(decisions, list) or len(decisions) != 8 or len({item.get("candidate_token") for item in decisions}) != 8:
        raise ValueError(f"candidate disposition partition drift: {manifest['batch_id']}")
    if any(item.get("final_adequacy") not in FINAL for item in decisions):
        raise ValueError(f"unresolved adequacy in reconciled group: {manifest['batch_id']}")
    tokens = sorted(item["candidate_token"] for item in decisions)
    if canonical_sha(tokens) != manifest["unified_candidate_tokens_sha256"]:
        raise ValueError(f"candidate token-manifest binding drift: {manifest['batch_id']}")


def normalise_reconciled(row: dict[str, Any], manifest: dict[str, Any], route: str) -> dict[str, Any]:
    validate_dispositions(row, manifest)
    return {
        "batch_id": row["batch_id"],
        **manifest_packet_fields(manifest),
        "source_route": route,
        "reconciliation_state": "TARGET_BLIND_RECONCILED_READY_FOR_SEALED_TOKEN_JOIN",
        "candidate_dispositions": row["candidate_dispositions"],
    }


def build_prejoin() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest_by_id = validate_v7_freeze()
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("state_counts") != {"FINALISED": 160, "STARTED_INCOMPLETE": 1, "UNSTARTED": 1065} or len(state.get("records", [])) != 1226:
        raise ValueError("official V20 historical execution-state snapshot drift")
    records = {row["batch_id"]: row for row in state["records"]}
    if set(records) != set(manifest_by_id):
        raise ValueError("execution-state/V7 manifest scope drift")
    legacy_ids = {bid for bid, row in records.items() if row["state"] == "FINALISED"}
    pending_ids = {bid for bid, row in records.items() if row["state"] in {"UNSTARTED", "STARTED_INCOMPLETE"}}
    if len(legacy_ids) != 160 or len(pending_ids) != 1066:
        raise ValueError("historical execution-state scope drift")

    legacy_rows: list[dict[str, Any]] = []
    found_final_ids = {path.parent.name for path in LEGACY.glob("RQ2B-P4-V7-U*/final_disposition.json")}
    if found_final_ids != legacy_ids:
        raise ValueError("historical final-disposition file scope drift")
    for batch_id in sorted(legacy_ids):
        final = json.loads((LEGACY / batch_id / "final_disposition.json").read_text(encoding="utf-8"))
        if final.get("status") != "PASS_V7_VALIDATED_BATCH_DISPOSITIONS_PENDING_LIBRARY_LEVEL_CLOSURE":
            raise ValueError(f"historical final-disposition status drift: {batch_id}")
        legacy_rows.append(normalise_reconciled(final, manifest_by_id[batch_id], "HISTORICAL_V7_VALIDATED_FINAL_DISPOSITION"))

    new_rows = load_jsonl(NEW / "master_target_blind_group_reconciliation.jsonl")
    if len(new_rows) != 1066 or len({row["batch_id"] for row in new_rows}) != 1066 or {row["batch_id"] for row in new_rows} != pending_ids:
        raise ValueError("new master readiness/pending historical scope drift")
    reconciled_new = [row for row in new_rows if row["reconciliation_state"] == "TARGET_BLIND_RECONCILED_READY_FOR_SEALED_TARGET_JOIN"]
    excluded_new = [row for row in new_rows if row["reconciliation_state"] == "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE"]
    if len(reconciled_new) != 1065 or len(excluded_new) != 1 or excluded_new[0]["batch_id"] != "RQ2B-P4-V7-U0323":
        raise ValueError("new master readiness disposition drift")
    merged = legacy_rows + [normalise_reconciled(row, manifest_by_id[row["batch_id"]], "V7_PHASE5_RECONCILIATION") for row in reconciled_new]
    excluded = excluded_new[0]
    if excluded["blind_packet_id"] != manifest_by_id[excluded["batch_id"]]["blind_packet_id"] or excluded.get("target_join_permitted") is not False:
        raise ValueError("U0323 sealed exclusion binding drift")
    merged.append({
        "batch_id": excluded["batch_id"],
        **manifest_packet_fields(manifest_by_id[excluded["batch_id"]]),
        "source_route": "USER_APPROVED_METHOD_GATE_DISPOSITION",
        "reconciliation_state": "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE",
        "exclusion_authority": excluded["exclusion_authority"],
        "exclusion_reason": excluded["exclusion_reason"],
        "target_join_permitted": False,
    })
    merged.sort(key=lambda row: row["batch_id"])
    if len(merged) != 1226 or len({row["batch_id"] for row in merged}) != 1226 or {row["batch_id"] for row in merged} != set(manifest_by_id):
        raise ValueError("all-scope prejoin coverage/disjointness drift")
    reconciled = [row for row in merged if row["reconciliation_state"] == "TARGET_BLIND_RECONCILED_READY_FOR_SEALED_TOKEN_JOIN"]
    if len(reconciled) != 1225 or sum(len(row["candidate_dispositions"]) for row in reconciled) != 9800:
        raise ValueError("all-scope prejoin candidate cardinality drift")
    outcomes = Counter(item["final_adequacy"] for row in reconciled for item in row["candidate_dispositions"])
    report = {
        "schema_version": "rq2b_nc_phase5_v7_all_scope_target_blind_prejoin_v1",
        "status": "PASS_V7_ALL_SCOPE_TARGET_BLIND_PREJOIN_READY_FOR_SEALED_TOKEN_JOIN_EXCLUDING_U0323",
        "claim_boundary": "All-scope target-blind mechanical consolidation only. It does not open an opaque token join, identify a source/target, determine an acceptable set, update the final library, run retrieval/metrics, or change K=6.",
        "counts": {"v7_prompt_groups": 1226, "historically_finalised_replayed": 160, "phase5_reconciled_replayed": 1065, "explicitly_deferred_excluded": 1, "reconciled_candidate_dispositions": 9800, "unresolved_groups": 0, "target_blind_outcome_counts": dict(sorted(outcomes.items()))},
        "bound_inputs": {"v7_summary_sha256": sha_path(V7 / "summary.json"), "v7_manifest_sha256": sha_path(V7 / "unified_prompt_group_batch_manifest.jsonl"), "v2_audit_summary_sha256": sha_path(V2 / "summary.json"), "official_v20_execution_state_sha256": sha_path(STATE), "master_target_blind_readiness_sha256": sha_path(NEW / "integrity_report.json")},
        "scope_transition": {"historical_v20_state_counts": state["state_counts"], "closure_dispositions": {"RECONCILED_READY_FOR_SEALED_TOKEN_JOIN": 1225, "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE": 1}},
        "next_permitted_step": "Run a sealed finaliser-only opaque token/source join and apply the frozen FULLY_ACCEPTABLE acceptable-set and positive-tail stopping rules. U0323 remains excluded.",
    }
    return merged, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen all-scope prejoin package: {output}")
    rows, report = build_prejoin()
    output.mkdir(parents=True)
    write_jsonl(output / "all_scope_target_blind_prejoin_reconciliation.jsonl", rows)
    write_json(output / "integrity_report.json", report)
    (output / "README.md").write_text(
        "# V7 all-scope target-blind prejoin\n\n"
        "This replay confirms that all 1,226 V7 groups are either reconciled or explicitly excluded before the finaliser may open the sealed token map. It contains no source or target identity.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "counts": report["counts"], "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
