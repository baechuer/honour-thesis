#!/usr/bin/env python3
"""Freeze the user-approved 1,077-group V7 acceptable-set library.

The scope decision is intentionally explicit: retain only groups that passed
the existing sealed K=6/two-tail stopping rules, and preserve every excluded
group with its reason.  This does not revise V7, call any model, or start an
experiment.
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
AUDIT = NC / "manifests" / "rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit_2026_09_08_v1"
SOP = NC / "review" / "RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
OUTPUT = NC / "manifests" / "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1"

RETAINED = {"STRICT_FINAL_CANDIDATE", "ACCEPTABLE_SET_FINAL_CANDIDATE"}
EXCLUDED = "DEFERRED_EXCLUDED_FROM_V7_FROZEN_LIBRARY_CLOSURE"


def sha_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def index_unique(rows: list[dict[str, Any]], field: str, label: str) -> dict[str, dict[str, Any]]:
    index = {row[field]: row for row in rows}
    if len(index) != len(rows):
        raise ValueError(f"{label} has duplicate {field}")
    return index


def build_freeze() -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any], dict[str, Any]]:
    audit_report = load_json(AUDIT / "integrity_report.json")
    if audit_report.get("status") != "BLOCKED_METHOD_GATE_OPEN_FULLY_ACCEPTABLE_POSITIVE_TAILS_DO_NOT_FINALISE_LIBRARY":
        raise ValueError("sealed audit status is not the expected pre-author-decision state")
    audit_ledger = load_jsonl(AUDIT / "acceptable_set_audit_ledger.jsonl")
    blocked_ledger = load_jsonl(AUDIT / "blocked_or_excluded_docket.jsonl")
    v7_summary = load_json(V7 / "summary.json")
    if len(audit_ledger) != 1225 or len(blocked_ledger) != 127:
        raise ValueError("sealed audit input cardinality drift")
    if sha_path(AUDIT / "acceptable_set_audit_ledger.jsonl") != audit_report["output_hashes"]["acceptable_set_audit_ledger.jsonl"]:
        raise ValueError("acceptable-set audit ledger hash drift")
    if sha_path(AUDIT / "blocked_or_excluded_docket.jsonl") != audit_report["output_hashes"]["blocked_or_excluded_docket.jsonl"]:
        raise ValueError("blocked/excluded docket hash drift")
    for relative, expected in v7_summary["outputs"].items():
        if sha_path(V7 / relative) != expected:
            raise ValueError(f"V7 frozen output hash drift: {relative}")

    retained = [row for row in audit_ledger if row["finaliser_disposition"] in RETAINED]
    nonretained = [row for row in audit_ledger if row["finaliser_disposition"] not in RETAINED]
    if len(retained) != 1077 or len(nonretained) != 148:
        raise ValueError("author-approved 1077/148 decision scope drift")
    if len({row["batch_id"] for row in retained}) != 1077 or len({row["batch_id"] for row in nonretained}) != 148:
        raise ValueError("acceptable-set audit group identity drift")
    if set(row["batch_id"] for row in retained) & set(row["batch_id"] for row in nonretained):
        raise ValueError("retained/nonretained overlap")

    final_library: list[dict[str, Any]] = []
    for row in retained:
        members = row["provisional_acceptable_set_source_sha256"]
        if not members or len(members) != len(set(members)):
            raise ValueError(f"invalid acceptable set: {row['batch_id']}")
        if row["fully_acceptable_tail_source_sha256"]:
            raise ValueError(f"positive tail accidentally retained: {row['batch_id']}")
        if row["finaliser_disposition"] == "STRICT_FINAL_CANDIDATE" and len(members) != 1:
            raise ValueError(f"strict label cardinality drift: {row['batch_id']}")
        if row["finaliser_disposition"] == "ACCEPTABLE_SET_FINAL_CANDIDATE" and len(members) < 2:
            raise ValueError(f"acceptable-set cardinality drift: {row['batch_id']}")
        final_library.append({
            "batch_id": row["batch_id"],
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "lane_id": row["lane_id"],
            "reporting_group": row["reporting_group"],
            "reporting_stratum": row["reporting_stratum"],
            "final_label_type": "STRICT" if row["finaliser_disposition"] == "STRICT_FINAL_CANDIDATE" else "ACCEPTABLE_SET",
            "acceptable_set_source_sha256": members,
            "historical_strict_gold_source_sha256": row["historical_strict_gold_source_sha256"],
            "cluster_local_most_suitable_source_sha256": row["cluster_local_most_suitable_source_sha256"],
            "frozen_k6_main_fully_acceptable_source_sha256": row["fully_acceptable_k6_main_source_sha256"],
            "partially_adequate_tail_source_sha256_recorded": row["partially_adequate_tail_source_sha256"],
            "source_audit_batch_id": row["batch_id"],
            "source_audit_ledger_sha256": audit_report["output_hashes"]["acceptable_set_audit_ledger.jsonl"],
            "scope_freeze_authority": "USER_APPROVED_V7_1077_GROUP_ACCEPTABLE_SET_FREEZE_2026_09_08",
        })
    final_library.sort(key=lambda row: row["batch_id"])

    exclusion_ledger: list[dict[str, Any]] = []
    for row in nonretained:
        reasons = [row["finaliser_disposition"]]
        exclusion_ledger.append({
            "batch_id": row["batch_id"],
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "lane_id": row["lane_id"],
            "reporting_group": row["reporting_group"],
            "reporting_stratum": row["reporting_stratum"],
            "exclusion_reasons": reasons,
            "underlying_main_pool_status": (
                row["base_stopping_rule_status"]
                if row["base_stopping_rule_status"].startswith("BLOCK_OR_REJECT")
                else None
            ),
            "action": "DEFERRED_EXCLUDED_FROM_V7_1077_GROUP_ACCEPTABLE_SET_FREEZE",
            "limitation_statement": "Excluded from the frozen V7 benchmark because the sealed audit either found a fully acceptable tail requiring a prospective method decision, found no fully acceptable K=6 main candidate, or found only a singleton external to the frozen NC local target. This exclusion is not an inadequacy label for unreviewed sources and does not alter K=6.",
            "source_audit_batch_id": row["batch_id"],
        })
    u0323 = [row for row in blocked_ledger if row["batch_id"] == "RQ2B-P4-V7-U0323"]
    if len(u0323) != 1 or set(u0323[0]) != {"batch_id", "blind_packet_id", "reason", "required_disposition", "target_join_permitted"}:
        raise ValueError("U0323 historical exclusion provenance drift")
    exclusion_ledger.append({
        "batch_id": "RQ2B-P4-V7-U0323",
        "prompt_id": None,
        "prompt_sha256": None,
        "lane_id": None,
        "reporting_group": None,
        "reporting_stratum": None,
        "exclusion_reasons": [u0323[0]["required_disposition"], u0323[0]["reason"]],
        "action": "DEFERRED_EXCLUDED_FROM_V7_1077_GROUP_ACCEPTABLE_SET_FREEZE",
        "limitation_statement": "Previously user-approved substantive construct-method exclusion; no target join was performed and the original frozen packet is retained unchanged.",
        "source_audit_batch_id": "RQ2B-P4-V7-U0323",
    })
    exclusion_ledger.sort(key=lambda row: row["batch_id"])
    if len(exclusion_ledger) != 149 or set(row["batch_id"] for row in exclusion_ledger) & set(row["batch_id"] for row in final_library):
        raise ValueError("final exclusion coverage/disjointness drift")
    if len(final_library) + len(exclusion_ledger) != 1226:
        raise ValueError("final scope completeness drift")

    label_counts = Counter(row["final_label_type"] for row in final_library)
    exclusion_counts = Counter(row["exclusion_reasons"][0] for row in exclusion_ledger)
    underlying_counts = Counter(
        row["underlying_main_pool_status"]
        for row in exclusion_ledger
        if row["exclusion_reasons"][0] == "METHOD_GATE_OPEN_FULLY_ACCEPTABLE_POSITIVE_TAIL"
        and row.get("underlying_main_pool_status") is not None
    )
    decision = {
        "schema_version": "rq2b_nc_v7_acceptable_set_final_library_scope_amendment_v1",
        "decision": "FREEZE_V7_1077_GROUP_ACCEPTABLE_SET_LIBRARY",
        "authority": "User instruction: freeze 1077 groups and perform acceptable-set freeze.",
        "date": "2026-09-08",
        "scope": {
            "v7_total_groups": 1226,
            "retained": 1077,
            "excluded_or_deferred": 149,
            "retained_label_counts": dict(sorted(label_counts.items())),
        },
        "method_boundary": "No change to V7 packets or K=6. Fully acceptable tails remain evidence of a prospective-method limitation and are excluded from this frozen V7 scope rather than silently admitted. This decision does not authorise retrieval, metrics, or thesis-result updates.",
        "supersession_boundary": "V7 frozen package, raw reviewer returns, reconciliation artefacts, and prior two-machine handoff remain immutable historical evidence. This is a downstream final-library scope decision only.",
    }
    report = {
        "schema_version": "rq2b_nc_v7_acceptable_set_final_library_freeze_v1",
        "status": "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION",
        "claim_boundary": "This package is a final V7 benchmark-library freeze after the user-approved exclusion/defer decision. It is not a retrieval run, an embedding/reranking/provider call, a metric, or a thesis-result update.",
        "counts": {
            "v7_total_groups": 1226,
            "frozen_final_library_groups": len(final_library),
            "frozen_strict_labels": label_counts["STRICT"],
            "frozen_acceptable_sets": label_counts["ACCEPTABLE_SET"],
            "excluded_or_deferred_groups": len(exclusion_ledger),
            "primary_exclusion_dispositions": dict(sorted(exclusion_counts.items())),
            "underlying_main_pool_block_within_positive_tail_gate": dict(sorted(underlying_counts.items())),
        },
        "input_hashes": {
            "v7_summary_sha256": sha_path(V7 / "summary.json"),
            "v7_unified_manifest_sha256": sha_path(V7 / "unified_prompt_group_batch_manifest.jsonl"),
            "sealed_audit_integrity_report_sha256": sha_path(AUDIT / "integrity_report.json"),
            "sealed_audit_ledger_sha256": sha_path(AUDIT / "acceptable_set_audit_ledger.jsonl"),
            "sealed_audit_exclusion_docket_sha256": sha_path(AUDIT / "blocked_or_excluded_docket.jsonl"),
            "master_sop_sha256": sha_path(SOP),
        },
        "integrity_assertions": {
            "retained_plus_excluded_equals_v7_scope": "PASS",
            "retained_excluded_disjoint": "PASS",
            "retained_has_no_positive_fully_acceptable_tail": "PASS",
            "strict_labels_have_exactly_one_member": "PASS",
            "acceptable_sets_have_at_least_two_members": "PASS",
            "u0323_remains_excluded_without_target_join": "PASS",
            "v7_frozen_output_hashes": "PASS",
        },
        "limitation": "The freeze intentionally excludes rather than resolves 22 positive-tail method-gate groups, 126 main-pool block groups, and U0323. Results must be reported as applying to the 1,077-group V7 frozen library only, not to deferred additions or all originally queued prompts.",
        "next_permitted_step": "Prepare an experiment execution plan with this exact manifest and an explicit authorisation. Do not recompute the acceptable set from result data.",
    }
    return {
        "final_library_prompt_manifest.jsonl": final_library,
        "exclusion_and_limitation_ledger.jsonl": exclusion_ledger,
    }, decision, report


def write_package(output: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError(f"refusing to overwrite frozen final-library package: {output}")
    outputs, decision, report = build_freeze()
    output.mkdir(parents=True)
    for name, rows in outputs.items():
        write_jsonl(output / name, rows)
    write_json(output / "scope_amendment.json", decision)
    report["output_hashes"] = {
        **{name: sha_path(output / name) for name in sorted(outputs)},
        "scope_amendment.json": sha_path(output / "scope_amendment.json"),
    }
    write_json(output / "integrity_report.json", report)
    (output / "README.md").write_text(
        "# V7 1,077-group acceptable-set final-library freeze\n\n"
        "This is the user-approved downstream V7 scope freeze: 881 strict labels and 196 acceptable sets. The 149 remaining V7 groups are retained only in the exclusion-and-limitation ledger. The package does not revise V7, change K=6, or authorise retrieval experimentation.\n\n"
        "Replay exactly from the repository root:\n\n"
        "```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_v7_acceptable_set_final_library_freeze.py\n```\n",
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
