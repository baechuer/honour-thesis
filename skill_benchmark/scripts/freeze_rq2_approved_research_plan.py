#!/usr/bin/env python3
"""Hash-bind the user-approved RQ2 plan; this never authorises model execution."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path("skill_benchmark/rq2b_naturalistic_confusability")
FIRST = BASE / "preparation/v7_first_matrix_2026_09_08_v1"
OUTPUT = BASE / "preparation/rq2_approved_research_plan_2026_09_08_v1"
FINAL = BASE / "manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1"
PLAN = Path("thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md")
PATHS = {
    "research_plan": PLAN,
    "core_conditions": FIRST / "first_matrix_conditions.jsonl",
    "bridge_conditions": FIRST / "fixed_candidate_bridge_conditions.jsonl",
    "source_manifest": FIRST / "source_manifest.jsonl",
    "final_prompts": FINAL / "final_library_prompt_manifest.jsonl",
    "exclusions": FINAL / "exclusion_and_limitation_ledger.jsonl",
    "scope_amendment": FINAL / "scope_amendment.json",
    "master_sop": BASE / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md",
}


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in (ROOT / path).read_bytes().splitlines()]


def build() -> bytes:
    core, bridge = rows(PATHS["core_conditions"]), rows(PATHS["bridge_conditions"])
    sources, prompts = rows(PATHS["source_manifest"]), rows(PATHS["final_prompts"])
    if len(core) != 36 or len(bridge) != 6 or len(sources) != 3798 or len(prompts) != 1077:
        raise ValueError("approved core scope mismatch")
    if len({r['sha256'] for r in sources}) != 3798 or len({r['prompt_id'] for r in prompts}) != 1077:
        raise ValueError("duplicate source/prompt identity")
    if any(r['execution_authorised'] or r['audit_main_k'] != 6 for r in core + bridge):
        raise ValueError("unexpected inference authorisation or audit depth")
    if len({r['condition_id'] for r in core + bridge}) != 42:
        raise ValueError("condition identity collision")
    if len(rows(PATHS['exclusions'])) != 149:
        raise ValueError("exclusion coverage mismatch")
    plan = (ROOT / PLAN).read_text(encoding="utf-8")
    if "FINAL_APPROVED_RESEARCH_PLAN" not in plan or "## 21. 未来 scale-out" not in plan:
        raise ValueError("approved plan/scope section absent")
    bindings = {key: {"path": str(path), "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
                for key, path in PATHS.items()}
    expected_prompt_sha = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"
    if bindings["final_prompts"]["sha256"] != expected_prompt_sha:
        raise ValueError("V7 final prompt hash drift")
    value = {
        "schema_version": "rq2-approved-research-plan-v1", "date": "2026-09-08",
        "status": "FINAL_APPROVED_RESEARCH_PLAN_NOT_RUNTIME_AUTHORISATION",
        "approval_basis": "User explicitly requested this updated version be finalised as the new RQ2 plan, with large-background scaling listed as future work, and experiment preparation started.",
        "bindings": bindings,
        "counts": {"queries": 1077, "source_candidates": 3798, "core_configurations": 36,
                   "bridge_new_configurations": 6, "excluded_or_deferred_queries": 149},
        "analysis": {"primary_scope": "NC lane; parent strata separately reported", "primary_comparisons": ["P1", "P2", "P3", "P4", "P5"],
                     "practical_quality_margin": 0.03, "efficiency_practical_reduction": 0.20,
                     "group_bootstrap_replicates": 10000, "group_bootstrap_seed": 2026090801,
                     "paired_group_sign_flip_replicates": 100000, "paired_group_sign_flip_seed": 2026090802,
                     "primary_per_comparison_alpha": 0.01, "details_authority": str(PLAN)},
        "future_scope": {"status": "DEFERRED_NOT_EXECUTED_NOT_REQUIRED_FOR_CORE",
                         "extra_background_candidate_target_approx": 20000,
                         "target_is_additional_not_final_library_count": True,
                         "admission_and_nested_scale_levels_not_sealed": True,
                         "architectures": ["wiki", "graph", "tree", "bounded agentic retrieval", "optional custom method"],
                         "assume_new_background_candidates_negative": False},
        "execution": {"local_preparation_authorised": True, "formal_selector_execution_authorised": False,
                      "runtime_root_sealed": False, "paid_or_external_payload_authorised_by_this_record": False,
                      "gate": "Complete Phase-7/8 QA and bind actual runtime root/model/length/cost scope under the master SOP."},
        "freeze_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    output = ROOT / OUTPUT / "plan_freeze.json"
    if args.verify:
        if output.read_bytes() != expected:
            raise ValueError("approved-plan freeze replay mismatch")
    else:
        output.parent.mkdir(parents=True, exist_ok=False)
        with output.open("xb") as handle:
            handle.write(expected)
    print(json.dumps({"status": "PASS_APPROVED_RESEARCH_PLAN_REPLAY" if args.verify else "PASS_APPROVED_RESEARCH_PLAN_FROZEN",
                      "plan_sha256": hashlib.sha256((ROOT / PLAN).read_bytes()).hexdigest(),
                      "formal_execution_authorised": False}, sort_keys=True))


if __name__ == "__main__":
    main()
