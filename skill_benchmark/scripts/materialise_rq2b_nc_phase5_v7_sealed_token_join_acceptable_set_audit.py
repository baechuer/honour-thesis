#!/usr/bin/env python3
"""Perform the V7 finaliser-only token join and stopping-rule audit.

This program is deliberately downstream of the all-scope target-blind
reconciliation.  It opens the frozen opaque map only after that reconciliation
passes, joins candidate tokens to canonical source hashes, and applies the
frozen K=6 plus two-tail rules.  It never retrieves, ranks, changes K, or
writes a final library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
V7 = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
V2 = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair"
PHASE3 = NC / "manifests" / "rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
PREJOIN = NC / "manifests" / "rq2b_nc_phase5_v7_all_scope_target_blind_prejoin_reconciliation_2026_09_08_v1"
SOP = NC / "review" / "RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
IDENTITY = WORKSPACE / "skill_benchmark" / "rq2b_full_library" / "rq2b-i3c-v3-2026-08-18" / "i3c_extraction" / "identity_manifest.jsonl"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit_2026_09_08_v1"

FINAL = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE"}
RECONCILED = "TARGET_BLIND_RECONCILED_READY_FOR_SEALED_TOKEN_JOIN"
EXCLUDED = "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE"


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def require_unique(rows: list[dict[str, Any]], field: str, label: str) -> dict[str, dict[str, Any]]:
    indexed = {row[field]: row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"{label} has duplicate {field}")
    return indexed


def replay_freeze() -> dict[str, Any]:
    v7_summary = load_json(V7 / "summary.json")
    if v7_summary.get("status") != "PASS_PHASE4_V7_STRICT_UNIFIED_BLIND_EXECUTION_FREEZE_PENDING_TWO_INDEPENDENT_RETURNS":
        raise ValueError("V7 freeze status drift")
    for relative, expected in v7_summary["outputs"].items():
        path = V7 / relative
        if not path.is_file() or sha_path(path) != expected:
            raise ValueError(f"V7 frozen output hash drift: {relative}")
    v2_summary = load_json(V2 / "summary.json")
    if v2_summary.get("status") != "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS":
        raise ValueError("V2 frozen input status drift")
    for relative, expected in v2_summary["outputs"].items():
        path = V2 / relative
        if not path.is_file() or sha_path(path) != expected:
            raise ValueError(f"V2 frozen output hash drift: {relative}")
    for relative, expected in v2_summary["bound_inputs"].items():
        path = WORKSPACE / relative
        if not path.is_file() or sha_path(path) != expected:
            raise ValueError(f"V2 bound-input hash drift: {relative}")
    return {"v7_summary": v7_summary, "v2_summary": v2_summary}


def validate_prejoin() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    report = load_json(PREJOIN / "integrity_report.json")
    if report.get("status") != "PASS_V7_ALL_SCOPE_TARGET_BLIND_PREJOIN_READY_FOR_SEALED_TOKEN_JOIN_EXCLUDING_U0323":
        raise ValueError("all-scope prejoin is not ready for token join")
    rows = load_jsonl(PREJOIN / "all_scope_target_blind_prejoin_reconciliation.jsonl")
    by_batch = require_unique(rows, "batch_id", "prejoin rows")
    if len(rows) != 1226:
        raise ValueError("all-scope prejoin count drift")
    reconciled = [row for row in rows if row.get("reconciliation_state") == RECONCILED]
    excluded = [row for row in rows if row.get("reconciliation_state") == EXCLUDED]
    if len(reconciled) != 1225 or len(excluded) != 1 or excluded[0].get("batch_id") != "RQ2B-P4-V7-U0323":
        raise ValueError("prejoin reconciled/excluded partition drift")
    if any(not isinstance(row.get("candidate_dispositions"), list) or len(row["candidate_dispositions"]) != 8 for row in reconciled):
        raise ValueError("prejoin candidate disposition cardinality drift")
    if any(decision.get("final_adequacy") not in FINAL for row in reconciled for decision in row["candidate_dispositions"]):
        raise ValueError("prejoin has unresolved final adequacy")
    if excluded[0].get("target_join_permitted") is not False:
        raise ValueError("U0323 exclusion is not sealed")
    return by_batch, reconciled


def source_metadata() -> tuple[dict[str, str], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    identities = load_jsonl(IDENTITY)
    skill_to_sha = {row["skill_id"]: row["source_sha256"] for row in identities}
    if len(skill_to_sha) != len(identities):
        raise ValueError("identity manifest has duplicate skill IDs")
    parents = load_jsonl(PHASE3 / "parent_prompt_manifest_for_phase5.jsonl")
    parent_by_sha = require_unique(parents, "prompt_sha256", "parent prompt manifest")
    ncs = load_jsonl(PHASE3 / "nc_prompt_manifest_for_phase4.jsonl")
    # The frozen NC manifest deliberately has two provenance-preserving shapes:
    # the earlier curated clusters name `prompt_id` and a local target, while
    # source-native additions name `audit_prompt_id` and an intended target.
    # Normalise only these schema aliases for the finaliser; retain the raw
    # manifest byte-for-byte and do not create a new gold label.
    for row in ncs:
        row["finalizer_prompt_id"] = row.get("prompt_id", row.get("audit_prompt_id"))
        row["finalizer_local_target_source_sha256"] = row.get(
            "cluster_local_most_suitable_source_sha256", row.get("intended_target_source_sha256")
        )
        if not row["finalizer_prompt_id"] or not row["finalizer_local_target_source_sha256"]:
            raise ValueError("NC frozen prompt lacks its identity/target provenance")
    nc_by_sha = require_unique(ncs, "prompt_text_sha256", "NC prompt manifest")
    if len(parents) != 372 or len(ncs) != 854:
        raise ValueError("frozen lane prompt counts drift")
    for row in parents:
        if row["gold_skill"] not in skill_to_sha:
            raise ValueError(f"unresolved historical parent gold: {row['prompt_id']}")
    return skill_to_sha, parent_by_sha, nc_by_sha


def review_packet_maps() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    opaque_rows = load_jsonl(V2 / "opaque_token_join.jsonl")
    opaque_by_token = require_unique(opaque_rows, "candidate_token", "opaque token join")
    review_rows = load_jsonl(V2 / "source_visible_review_pairs.jsonl")
    review_by_token = require_unique(review_rows, "candidate_token", "source-visible pair ledger")
    allocation_rows = load_jsonl(V2 / "prompt_k6_allocation_ledger.jsonl")
    allocation_by_sha = require_unique(allocation_rows, "prompt_sha256", "K=6 allocation ledger")
    if len(opaque_rows) != 9808 or len(review_rows) != 9808 or len(allocation_rows) != 1226:
        raise ValueError("V2 frozen source-visible/opaque packet cardinality drift")
    if set(opaque_by_token) != set(review_by_token):
        raise ValueError("opaque/source-visible token scope drift")
    for token, opaque in opaque_by_token.items():
        visible = review_by_token[token]
        if (opaque["canonical_source_sha256"], opaque["packet_kind"], opaque["prompt_id"]) != (visible["canonical_source_sha256"], visible["packet_kind"], visible["prompt_id"]):
            raise ValueError(f"opaque/source-visible pair binding drift: {token}")
    return opaque_by_token, review_by_token, allocation_by_sha


def packet_role(visible: dict[str, Any], allocation: dict[str, Any]) -> tuple[str, str | None]:
    source = visible["canonical_source_sha256"]
    if visible["packet_kind"] == "K6_MAIN":
        matches = [entry for entry in allocation["main_allocation"] if entry["canonical_source_sha256"] == source]
        if len(matches) != 1:
            raise ValueError(f"main allocation role drift: {visible['candidate_token']}")
        return matches[0]["slot"], None
    if visible["packet_kind"] == "TAIL_CHALLENGE":
        matches = [entry for entry in allocation["tail_allocation"] if entry["canonical_source_sha256"] == source]
        if len(matches) != 1:
            raise ValueError(f"tail allocation role drift: {visible['candidate_token']}")
        return "TAIL", matches[0]["tail_kind"]
    raise ValueError(f"unknown frozen packet kind: {visible['packet_kind']}")


def audit() -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    freeze = replay_freeze()
    prejoin_by_batch, reconciled_rows = validate_prejoin()
    skill_to_sha, parent_by_sha, nc_by_sha = source_metadata()
    opaque_by_token, review_by_token, allocation_by_sha = review_packet_maps()
    manifest_rows = load_jsonl(V7 / "unified_prompt_group_batch_manifest.jsonl")
    manifest_by_batch = require_unique(manifest_rows, "batch_id", "V7 unified manifest")
    if set(manifest_by_batch) != set(prejoin_by_batch):
        raise ValueError("V7/prejoin batch scope drift")

    joined_candidates: list[dict[str, Any]] = []
    group_audit: list[dict[str, Any]] = []
    positive_tail_docket: list[dict[str, Any]] = []
    partial_tail_docket: list[dict[str, Any]] = []
    blocked_or_excluded_docket: list[dict[str, Any]] = []
    lane_counts: Counter[str] = Counter()
    group_status_counts: Counter[str] = Counter()

    for prejoin in sorted(reconciled_rows, key=lambda row: row["batch_id"]):
        batch_id = prejoin["batch_id"]
        manifest = manifest_by_batch[batch_id]
        prompt_sha = manifest["prompt_sha256"]
        allocation = allocation_by_sha.get(prompt_sha)
        if allocation is None:
            raise ValueError(f"no frozen allocation for V7 batch: {batch_id}")
        lane = allocation["lane_id"]
        if lane == "A_PARENT_DELTA":
            prompt_meta = parent_by_sha.get(prompt_sha)
        elif lane == "B_NC_FULL_UNION":
            prompt_meta = nc_by_sha.get(prompt_sha)
        else:
            raise ValueError(f"unknown lane: {lane}")
        if prompt_meta is None:
            raise ValueError(f"lane/prompt metadata scope drift: {batch_id}")
        if allocation["prompt_id"] != (prompt_meta["prompt_id"] if lane == "A_PARENT_DELTA" else prompt_meta["finalizer_prompt_id"]):
            raise ValueError(f"prompt-id binding drift: {batch_id}")

        decisions = {row["candidate_token"]: row for row in prejoin["candidate_dispositions"]}
        tokens = sorted(decisions)
        if canonical_sha(tokens) != manifest["unified_candidate_tokens_sha256"]:
            raise ValueError(f"V7 token partition drift after prejoin: {batch_id}")
        per_group: list[dict[str, Any]] = []
        for token in tokens:
            opaque, visible = opaque_by_token.get(token), review_by_token.get(token)
            if opaque is None or visible is None:
                raise ValueError(f"token missing frozen opaque/visible binding: {batch_id}/{token}")
            if visible["prompt_sha256"] != prompt_sha or visible["prompt_id"] != allocation["prompt_id"]:
                raise ValueError(f"candidate prompt binding drift: {batch_id}/{token}")
            role, tail_kind = packet_role(visible, allocation)
            joined = {
                "batch_id": batch_id,
                "blind_packet_id": manifest["blind_packet_id"],
                "prompt_id": allocation["prompt_id"],
                "prompt_sha256": prompt_sha,
                "lane_id": lane,
                "reporting_group": allocation["reporting_group"],
                "reporting_stratum": allocation["reporting_stratum"],
                "candidate_token": token,
                "canonical_source_sha256": opaque["canonical_source_sha256"],
                "packet_id": opaque["packet_id"],
                "packet_kind": opaque["packet_kind"],
                "allocation_slot": role,
                "tail_kind": tail_kind,
                "final_adequacy": decisions[token]["final_adequacy"],
                "reconciliation_route": decisions[token].get("reconciliation_route"),
                "source_route": prejoin["source_route"],
            }
            joined_candidates.append(joined)
            per_group.append(joined)

        main = [row for row in per_group if row["packet_kind"] == "K6_MAIN"]
        tails = [row for row in per_group if row["packet_kind"] == "TAIL_CHALLENGE"]
        if len(main) != 6 or len(tails) != 2 or len({row["candidate_token"] for row in per_group}) != 8:
            raise ValueError(f"K=6/two-tail partition drift after token join: {batch_id}")
        full_main = sorted(row["canonical_source_sha256"] for row in main if row["final_adequacy"] == "FULLY_ACCEPTABLE")
        full_tails = [row for row in tails if row["final_adequacy"] == "FULLY_ACCEPTABLE"]
        partial_tails = [row for row in tails if row["final_adequacy"] == "PARTIALLY_ADEQUATE"]
        for tail in full_tails:
            positive_tail_docket.append({
                "batch_id": batch_id,
                "prompt_id": allocation["prompt_id"],
                "lane_id": lane,
                "reporting_group": allocation["reporting_group"],
                "reporting_stratum": allocation["reporting_stratum"],
                "candidate_token": tail["candidate_token"],
                "canonical_source_sha256": tail["canonical_source_sha256"],
                "tail_kind": tail["tail_kind"],
                "final_adequacy": "FULLY_ACCEPTABLE",
                "required_method_disposition": "METHOD_GATE_OPEN_FULLY_ACCEPTABLE_POSITIVE_TAIL_DO_NOT_AUTOEXPAND_K6",
            })
        for tail in partial_tails:
            partial_tail_docket.append({
                "batch_id": batch_id,
                "prompt_id": allocation["prompt_id"],
                "lane_id": lane,
                "reporting_group": allocation["reporting_group"],
                "reporting_stratum": allocation["reporting_stratum"],
                "candidate_token": tail["candidate_token"],
                "canonical_source_sha256": tail["canonical_source_sha256"],
                "tail_kind": tail["tail_kind"],
                "final_adequacy": "PARTIALLY_ADEQUATE",
                "recording_disposition": "RECORDED_NONADMISSION_PARTIAL_TAIL_NOT_A_FULLY_ACCEPTABLE_MEMBER",
            })

        historical_gold_sha: str | None = None
        local_target_sha: str | None = None
        if lane == "A_PARENT_DELTA":
            historical_gold_sha = skill_to_sha[prompt_meta["gold_skill"]]
            if historical_gold_sha in set(full_main):
                raise ValueError(f"parent-delta packet unexpectedly contains inherited historical gold: {batch_id}")
            provisional = sorted(set([historical_gold_sha, *full_main]))
            base_status = "STRICT_FINAL_CANDIDATE" if len(provisional) == 1 else "ACCEPTABLE_SET_FINAL_CANDIDATE"
            provenance_note = "Historical strict gold is preserved as an inherited V3 seed; newly FULLY_ACCEPTABLE K=6 main candidates are additions only. No V3 label is rewritten."
        else:
            local_target_sha = prompt_meta["finalizer_local_target_source_sha256"]
            provisional = full_main
            if not provisional:
                base_status = "BLOCK_OR_REJECT_NO_FULLY_ACCEPTABLE_K6_MAIN_CANDIDATE"
            elif len(provisional) >= 2:
                base_status = "ACCEPTABLE_SET_FINAL_CANDIDATE"
            elif provisional[0] == local_target_sha:
                base_status = "STRICT_FINAL_CANDIDATE"
            else:
                base_status = "BLOCK_OR_REJECT_SINGLE_EXTERNAL_FULLY_ACCEPTABLE_CANDIDATE"
            provenance_note = "NC finaliser uses the frozen whole-library K=6 main audit. A cluster-local singleton remains strict only when that singleton is the frozen local most-suitable candidate; multiple FULLY_ACCEPTABLE main candidates remain an acceptable-set candidate."

        final_status = base_status
        if full_tails:
            final_status = "METHOD_GATE_OPEN_FULLY_ACCEPTABLE_POSITIVE_TAIL"
        elif base_status.startswith("BLOCK_OR_REJECT"):
            blocked_or_excluded_docket.append({
                "batch_id": batch_id,
                "prompt_id": allocation["prompt_id"],
                "lane_id": lane,
                "reporting_group": allocation["reporting_group"],
                "reporting_stratum": allocation["reporting_stratum"],
                "reason": base_status,
                "provisional_fully_acceptable_main_source_sha256": provisional,
                "local_target_source_sha256": local_target_sha,
                "required_disposition": "REMEDIATION_OR_EXPLICIT_EXCLUSION_REQUIRED_BEFORE_FINAL_LIBRARY",
            })
        row = {
            "batch_id": batch_id,
            "blind_packet_id": manifest["blind_packet_id"],
            "prompt_id": allocation["prompt_id"],
            "prompt_sha256": prompt_sha,
            "lane_id": lane,
            "reporting_group": allocation["reporting_group"],
            "reporting_stratum": allocation["reporting_stratum"],
            "historical_strict_gold_source_sha256": historical_gold_sha,
            "cluster_local_most_suitable_source_sha256": local_target_sha,
            "fully_acceptable_k6_main_source_sha256": full_main,
            "fully_acceptable_tail_source_sha256": sorted(row["canonical_source_sha256"] for row in full_tails),
            "partially_adequate_tail_source_sha256": sorted(row["canonical_source_sha256"] for row in partial_tails),
            "provisional_acceptable_set_source_sha256": provisional,
            "base_stopping_rule_status": base_status,
            "finaliser_disposition": final_status,
            "closure_note": provenance_note,
        }
        group_audit.append(row)
        lane_counts[lane] += 1
        group_status_counts[final_status] += 1

    excluded_prejoin = prejoin_by_batch["RQ2B-P4-V7-U0323"]
    excluded_manifest = manifest_by_batch["RQ2B-P4-V7-U0323"]
    blocked_or_excluded_docket.append({
        "batch_id": "RQ2B-P4-V7-U0323",
        "blind_packet_id": excluded_manifest["blind_packet_id"],
        "reason": excluded_prejoin["exclusion_reason"],
        "required_disposition": "USER_APPROVED_DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE",
        "target_join_permitted": False,
    })
    group_status_counts[EXCLUDED] += 1

    if len(joined_candidates) != 9800 or len(group_audit) != 1225 or len({row["batch_id"] for row in group_audit}) != 1225:
        raise ValueError("finaliser coverage/cardinality drift")
    if len({row["candidate_token"] for row in joined_candidates}) != 9800:
        raise ValueError("finaliser candidate token duplicate")
    if any(row["final_adequacy"] not in FINAL for row in joined_candidates):
        raise ValueError("finaliser outcome drift")
    active_tokens = {row["candidate_token"] for row in joined_candidates}
    excluded_tokens = set(opaque_by_token) - active_tokens
    excluded_tokens_expected = set()
    for row in manifest_by_batch.values():
        if row["batch_id"] == "RQ2B-P4-V7-U0323":
            packet_tokens = [token for token, visible in review_by_token.items() if visible["prompt_sha256"] == row["prompt_sha256"]]
            excluded_tokens_expected.update(packet_tokens)
    if excluded_tokens != excluded_tokens_expected or len(excluded_tokens) != 8:
        raise ValueError("U0323 exclusion token scope drift")

    gate_count = len(positive_tail_docket)
    blocked_count = sum(1 for row in group_audit if row["base_stopping_rule_status"].startswith("BLOCK_OR_REJECT"))
    blocked_without_tail_gate = sum(
        1
        for row in group_audit
        if row["base_stopping_rule_status"].startswith("BLOCK_OR_REJECT")
        and row["finaliser_disposition"] != "METHOD_GATE_OPEN_FULLY_ACCEPTABLE_POSITIVE_TAIL"
    )
    tail_gate_with_underlying_block = blocked_count - blocked_without_tail_gate
    overall_status = (
        "BLOCKED_METHOD_GATE_OPEN_FULLY_ACCEPTABLE_POSITIVE_TAILS_DO_NOT_FINALISE_LIBRARY"
        if gate_count
        else "PASS_SEALED_JOIN_AUDIT_WITH_REMEDIATION_DOCKET_NO_FINAL_LIBRARY"
        if blocked_count
        else "PASS_SEALED_JOIN_AUDIT_READY_FOR_FINAL_LIBRARY_FREEZE"
    )
    report = {
        "schema_version": "rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit_v1",
        "status": overall_status,
        "claim_boundary": "Finaliser-only join and frozen stopping-rule audit. It maps reconciled opaque tokens to canonical source hashes after target-blind closure. It does not retrieve, embed, rerank, call a provider, compute any retrieval metric, change K=6, modify a historical V3 label, or write a final library.",
        "counts": {
            "v7_total_prompt_groups": 1226,
            "target_joined_reconciled_groups": 1225,
            "user_approved_excluded_groups": 1,
            "joined_candidate_dispositions": len(joined_candidates),
            "joined_main_candidates": sum(row["packet_kind"] == "K6_MAIN" for row in joined_candidates),
            "joined_tail_candidates": sum(row["packet_kind"] == "TAIL_CHALLENGE" for row in joined_candidates),
            "group_finaliser_dispositions": dict(sorted(group_status_counts.items())),
            "positive_fully_acceptable_tail_method_gates": gate_count,
            "partially_adequate_tails_recorded_nonadmission": len(partial_tail_docket),
            "base_block_or_reject_groups": blocked_count,
            "base_block_or_reject_groups_not_superseded_by_tail_gate": blocked_without_tail_gate,
            "positive_tail_gate_groups_with_underlying_block_or_reject": tail_gate_with_underlying_block,
            "lanes": dict(sorted(lane_counts.items())),
        },
        "hash_replay": {
            "v7_summary_sha256": sha_path(V7 / "summary.json"),
            "v7_unified_manifest_sha256": sha_path(V7 / "unified_prompt_group_batch_manifest.jsonl"),
            "v2_summary_sha256": sha_path(V2 / "summary.json"),
            "v2_opaque_token_join_sha256": sha_path(V2 / "opaque_token_join.jsonl"),
            "v2_source_visible_review_pairs_sha256": sha_path(V2 / "source_visible_review_pairs.jsonl"),
            "v2_prompt_k6_allocation_ledger_sha256": sha_path(V2 / "prompt_k6_allocation_ledger.jsonl"),
            "all_scope_prejoin_integrity_report_sha256": sha_path(PREJOIN / "integrity_report.json"),
            "master_sop_sha256": sha_path(SOP),
        },
        "frozen_input_replay": {
            "v7_output_hashes": "PASS",
            "v2_output_hashes": "PASS",
            "v2_bound_input_hashes": "PASS",
            "historical_v2_materialiser_source": "NOT_RERUN; frozen V2 outputs and their bound inputs are byte-hash replayed, while the current source file is not asserted to regenerate a historical freeze.",
        },
        "stopping_rule": {
            "k6_main": "Only FULLY_ACCEPTABLE K=6 main candidates may enter a provisional set.",
            "two_tails": "A fully acceptable tail opens a method gate and is never silently admitted or used to increase K. A partially adequate tail is recorded but is not a fully acceptable member.",
            "parent_delta": "The historical strict V3 gold is preserved as an inherited seed; reviewed fully acceptable main candidates are additions only and do not rewrite V3.",
            "nc_full_union": "All FULLY_ACCEPTABLE K=6 main candidates are retained provisionally. A one-member NC set is strict only if it is the frozen local most-suitable source; an external singleton is blocked for remediation rather than silently replacing the local target.",
        },
        "next_permitted_step": (
            "Author decision on every fully acceptable positive-tail method gate; do not expand K or finalise the library automatically."
            if gate_count
            else "Resolve the explicit block/reject docket before a final-library freeze."
            if blocked_count
            else "A separate final-library freeze may be prepared under the SOP; no retrieval experiment is authorised by this audit."
        ),
    }
    outputs = {
        "sealed_finalizer_candidate_join.jsonl": sorted(joined_candidates, key=lambda row: (row["batch_id"], row["candidate_token"])),
        "acceptable_set_audit_ledger.jsonl": sorted(group_audit, key=lambda row: row["batch_id"]),
        "positive_tail_method_gate_docket.jsonl": sorted(positive_tail_docket, key=lambda row: (row["batch_id"], row["candidate_token"])),
        "partial_tail_quality_docket.jsonl": sorted(partial_tail_docket, key=lambda row: (row["batch_id"], row["candidate_token"])),
        "blocked_or_excluded_docket.jsonl": sorted(blocked_or_excluded_docket, key=lambda row: row["batch_id"]),
    }
    return outputs, report


def write_package(output: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError(f"refusing to overwrite frozen sealed-join package: {output}")
    outputs, report = audit()
    output.mkdir(parents=True)
    for name, rows in outputs.items():
        write_jsonl(output / name, rows)
    report["output_hashes"] = {name: sha_path(output / name) for name in sorted(outputs)}
    write_json(output / "integrity_report.json", report)
    (output / "README.md").write_text(
        "# V7 sealed token join and acceptable-set stopping-rule audit\n\n"
        "This finaliser-only package opens the frozen opaque token map only after the complete 1,226-group target-blind reconciliation has passed. It is not a final library and it does not authorise an experiment. `U0323` remains excluded without a target join. A fully acceptable tail is a hard method gate: it is recorded in the docket and is never silently admitted or used to change K=6.\n\n"
        "Replay exactly from the repository root:\n\n"
        "```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit.py\n```\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    report = write_package(args.output.resolve())
    print(json.dumps({"status": report["status"], "counts": report["counts"], "output": str(args.output.resolve())}, sort_keys=True))


if __name__ == "__main__":
    main()
