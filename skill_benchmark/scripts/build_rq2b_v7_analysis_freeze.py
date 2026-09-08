#!/usr/bin/env python3
"""Build or replay the pre-outcome V7 query, scoring and dependency freeze.

The runtime query file is label-free.  Acceptable/judged labels and diagnostic
neighbour sets are kept in offline-only ledgers and must never be loaded by a
retrieval or reranking process.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
BASE = Path("skill_benchmark/rq2b_naturalistic_confusability")
OUTPUT = BASE / "preparation/v7_analysis_freeze_2026_09_08_v1"
FINAL = BASE / "manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/final_library_prompt_manifest.jsonl"
JOIN = BASE / "manifests/rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit_2026_09_08_v1/sealed_finalizer_candidate_join.jsonl"
PHASE3 = BASE / "manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
NC_PROMPTS = PHASE3 / "nc_prompt_manifest_for_phase4.jsonl"
PARENT_PROMPTS = PHASE3 / "parent_prompt_manifest_for_phase5.jsonl"
ALLOCATION = BASE / "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v2_blind-order-repair/prompt_k6_allocation_ledger.jsonl"
SOURCE_MANIFEST = BASE / "preparation/v7_first_matrix_2026_09_08_v1/source_manifest.jsonl"
CORE_CONDITIONS = BASE / "preparation/v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl"
BRIDGE_CONDITIONS = BASE / "preparation/v7_first_matrix_2026_09_08_v1/fixed_candidate_bridge_conditions.jsonl"
PLAN_FREEZE = BASE / "preparation/rq2_approved_research_plan_2026_09_08_v1/plan_freeze.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def any_positive(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return value > 0
    if isinstance(value, list):
        return any(any_positive(item) for item in value)
    return False


class UnionFind:
    def __init__(self, values: Iterable[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: str, right: str) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[max(left_root, right_root)] = min(left_root, right_root)


def dependency_rows(final_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt_ids = [row["prompt_id"] for row in final_rows]
    uf = UnionFind(prompt_ids)
    buckets: dict[tuple[str, str], list[str]] = defaultdict(list)
    anchors: dict[str, list[str]] = defaultdict(list)
    for row in final_rows:
        buckets[(row["lane_id"], row["reporting_group"])].append(row["prompt_id"])
        anchor = row.get("cluster_local_most_suitable_source_sha256") or row.get("historical_strict_gold_source_sha256")
        require(isinstance(anchor, str) and len(anchor) == 64, f"missing dependency anchor: {row['prompt_id']}")
        anchors[anchor].append(row["prompt_id"])
    for members in [*buckets.values(), *anchors.values()]:
        for member in members[1:]:
            uf.union(members[0], member)
    components: dict[str, list[str]] = defaultdict(list)
    for prompt_id in prompt_ids:
        components[uf.find(prompt_id)].append(prompt_id)
    group_for: dict[str, str] = {}
    for members in components.values():
        ordered = sorted(members)
        group_id = "D-" + sha_bytes("\n".join(ordered).encode())[:16].upper()
        group_for.update({member: group_id for member in ordered})
    return [
        {
            "schema_version": "rq2b-v7-dependency-ledger-v1",
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "dependency_group": group_for[row["prompt_id"]],
            "lane_id": row["lane_id"],
            "reporting_group": row["reporting_group"],
            "dependency_anchor_source_sha256": row.get("cluster_local_most_suitable_source_sha256") or row.get("historical_strict_gold_source_sha256"),
            "edge_policy": "connected_component_of_same_lane_reporting_group_or_same_designated_source; exact-prompt-hash also checked but unique; no distractor or result edge",
        }
        for row in final_rows
    ]


def build() -> dict[str, bytes]:
    final_rows = read_rows(ROOT / FINAL)
    join_rows = read_rows(ROOT / JOIN)
    nc_rows = read_rows(ROOT / NC_PROMPTS)
    parent_rows = read_rows(ROOT / PARENT_PROMPTS)
    allocation_rows = read_rows(ROOT / ALLOCATION)
    sources = read_rows(ROOT / SOURCE_MANIFEST)
    require(len(final_rows) == 1077 and len({row["prompt_id"] for row in final_rows}) == 1077, "final prompt scope mismatch")
    require(len(sources) == 3798 and len({row["sha256"] for row in sources}) == 3798, "source scope mismatch")
    source_hashes = {row["sha256"] for row in sources}

    prompt_text_by_sha: dict[str, dict[str, Any]] = {}
    for origin, rows in (("NC_PHASE3", nc_rows), ("PARENT_PHASE3", parent_rows)):
        for row in rows:
            digest = row.get("prompt_text_sha256") or row.get("prompt_sha256")
            prompt = row["prompt"]
            require(sha_bytes(prompt.encode()) == digest, f"upstream prompt hash drift: {digest}")
            require(digest not in prompt_text_by_sha, f"duplicate upstream prompt hash: {digest}")
            upstream_prompt_id = row.get("prompt_id") or row.get("audit_prompt_id")
            require(isinstance(upstream_prompt_id, str) and upstream_prompt_id, f"upstream prompt ID missing: {digest}")
            prompt_text_by_sha[digest] = {"prompt": prompt, "origin": origin, "upstream_prompt_id": upstream_prompt_id}

    runtime_rows = []
    for row in final_rows:
        matched = prompt_text_by_sha.get(row["prompt_sha256"])
        require(matched is not None, f"final prompt text not found: {row['prompt_id']}")
        runtime_rows.append({
            "schema_version": "rq2b-v7-label-free-query-runtime-v1",
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "prompt": matched["prompt"],
        })

    retained_ids = {row["prompt_id"] for row in final_rows}
    joined_by_prompt: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in join_rows:
        if row["prompt_id"] in retained_ids:
            joined_by_prompt[row["prompt_id"]].append(row)
    require(sum(map(len, joined_by_prompt.values())) == 8616, "retained joined scope mismatch")

    label_rows = []
    for final in final_rows:
        prompt_id = final["prompt_id"]
        joined = joined_by_prompt[prompt_id]
        require(len(joined) == 8 and len({row["canonical_source_sha256"] for row in joined}) == 8, f"joined K6+two-tail mismatch: {prompt_id}")
        joined_dispositions = {row["canonical_source_sha256"]: row["final_adequacy"] for row in joined}
        acceptable = set(final["acceptable_set_source_sha256"])
        historical = final.get("historical_strict_gold_source_sha256")
        if historical:
            require(historical not in joined_dispositions, f"parent historical gold unexpectedly in delta audit: {prompt_id}")
            joined_dispositions[historical] = "FULLY_ACCEPTABLE_INHERITED_HISTORICAL_STRICT_GOLD"
        fully_acceptable = {digest for digest, value in joined_dispositions.items() if value.startswith("FULLY_ACCEPTABLE")}
        require(acceptable == fully_acceptable, f"acceptable/judgement mismatch: {prompt_id}")
        require(set(joined_dispositions) <= source_hashes, f"judged source outside library: {prompt_id}")
        label_rows.append({
            "schema_version": "rq2b-v7-offline-label-adapter-v1",
            "prompt_id": prompt_id,
            "prompt_sha256": final["prompt_sha256"],
            "lane_id": final["lane_id"],
            "reporting_stratum": final["reporting_stratum"],
            "final_label_type": final["final_label_type"],
            "acceptable_set_source_sha256": sorted(acceptable),
            "judged_candidate_dispositions": [
                {"candidate_source_sha256": digest, "adequacy": joined_dispositions[digest]}
                for digest in sorted(joined_dispositions)
            ],
            "library_source_count": 3798,
            "unjudged_source_count": 3798 - len(joined_dispositions),
        })

    deps = dependency_rows(final_rows)
    dependency_by_prompt = {row["prompt_id"]: row for row in deps}
    exposure_rows = []
    for row in final_rows:
        parent = row["lane_id"] == "A_PARENT_DELTA"
        exposure_rows.append({
            "schema_version": "rq2b-v7-exposure-ledger-v1",
            "prompt_id": row["prompt_id"],
            "prompt_sha256": row["prompt_sha256"],
            "dependency_group": dependency_by_prompt[row["prompt_id"]]["dependency_group"],
            "prompt_level_exposure": "HISTORICAL_RQ2B_SELECTOR_OUTCOME_EXPOSED" if parent else "CURRENT_V7_BENCHMARK_CURATION_AND_ACCEPTABILITY_REVIEW_EXPOSED",
            "historical_selector_outcome_evidence": "BOUND_BY_PARENT_LINEAGE" if parent else "NOT_BOUND_FOR_NC_IN_THIS_FREEZE_DO_NOT_INTERPRET_AS_PROVEN_ABSENCE",
            "global_design_exposure": "P1_P5_AND_MATRIX_INFORMED_BY_PRIOR_RQ2A_AND_HISTORICAL_RQ2B_RESULTS",
            "analysis_disposition": "PARENT_ROBUSTNESS_ONLY" if parent else "NC_PRIMARY_WITH_SOURCE_NATIVE_SENSITIVITY",
        })

    allocation_by_sha = {row["prompt_sha256"]: row for row in allocation_rows}
    dq_rows = []
    for final in final_rows:
        allocation = allocation_by_sha.get(final["prompt_sha256"])
        require(allocation is not None, f"allocation not found: {final['prompt_id']}")
        dispositions = {row["canonical_source_sha256"]: row for row in joined_by_prompt[final["prompt_id"]]}
        acceptable = set(final["acceptable_set_source_sha256"])
        selected: dict[str, dict[str, Any]] = {}
        for item in allocation["main_allocation"]:
            digest = item["canonical_source_sha256"]
            if digest in acceptable:
                continue
            rule = None
            if final["lane_id"] == "B_NC_FULL_UNION" and str(item["slot"]).startswith("LOCAL_"):
                rule = "NC_LOCAL_CLUSTER_MEMBER_IN_J_MINUS_A"
            elif not item["zero_score_coverage_fallback"] and any_positive(item.get("score")):
                rule = "POSITIVE_NAVIGATION_MAIN_IN_J_MINUS_A"
            if rule:
                selected[digest] = {"allocation": item, "rule": rule, "packet_kind": "K6_MAIN", "tail_kind": None}
        for item in allocation["tail_allocation"]:
            digest = item["canonical_source_sha256"]
            if digest not in acceptable and item.get("tail_kind") == "PHRASE_H_POSITIVE":
                selected[digest] = {"allocation": item, "rule": "PHRASE_H_POSITIVE_TAIL_IN_J_MINUS_A", "packet_kind": "TAIL_CHALLENGE", "tail_kind": item["tail_kind"]}
        for digest, selected_row in sorted(selected.items()):
            joined = dispositions.get(digest)
            require(joined is not None, f"D_q candidate missing final disposition: {final['prompt_id']}/{digest}")
            require(joined["final_adequacy"] != "FULLY_ACCEPTABLE", f"D_q contains A member: {final['prompt_id']}/{digest}")
            allocation_item = selected_row["allocation"]
            dq_rows.append({
                "schema_version": "rq2b-v7-reviewed-confusable-neighbour-ledger-v1",
                "prompt_id": final["prompt_id"],
                "prompt_sha256": final["prompt_sha256"],
                "candidate_source_sha256": digest,
                "final_adequacy": joined["final_adequacy"],
                "allocation_slot": allocation_item.get("slot") or "TAIL",
                "selection_channel": allocation_item["selection_channel"],
                "packet_kind": selected_row["packet_kind"],
                "tail_kind": selected_row["tail_kind"],
                "zero_score_coverage_fallback": allocation_item["zero_score_coverage_fallback"],
                "relation_rule": selected_row["rule"],
                "scope_boundary": "D_q is a predefined reviewed diagnostic subset of J_q minus A_q, not all semantic neighbours in the library",
            })

    files: dict[str, bytes] = {
        "label_free_query_runtime.jsonl": rows_bytes(runtime_rows),
        "offline_label_adapter.jsonl": rows_bytes(label_rows),
        "dependency_ledger.jsonl": rows_bytes(deps),
        "exposure_ledger.jsonl": rows_bytes(exposure_rows),
        "reviewed_confusable_neighbour_ledger.jsonl": rows_bytes(dq_rows),
    }
    dep_sizes = Counter(row["dependency_group"] for row in deps)
    d_per_prompt = Counter(row["prompt_id"] for row in dq_rows)
    bindings = {
        str(path): sha_path(ROOT / path)
        for path in (FINAL, JOIN, NC_PROMPTS, PARENT_PROMPTS, ALLOCATION, SOURCE_MANIFEST, CORE_CONDITIONS, BRIDGE_CONDITIONS, PLAN_FREEZE)
    }
    report = {
        "schema_version": "rq2b-v7-pre-outcome-analysis-freeze-report-v1",
        "status": "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE",
        "retrieval_or_reranking_runs": 0,
        "provider_calls": 0,
        "scientific_results_observed": False,
        "counts": {
            "prompts": len(runtime_rows),
            "candidates": len(sources),
            "acceptable_relations": sum(len(row["acceptable_set_source_sha256"]) for row in label_rows),
            "judged_relations": sum(len(row["judged_candidate_dispositions"]) for row in label_rows),
            "dependency_groups": len(dep_sizes),
            "dependency_singletons": sum(size == 1 for size in dep_sizes.values()),
            "dependency_max_group_size": max(dep_sizes.values()),
            "reviewed_confusable_neighbour_relations": len(dq_rows),
            "prompts_with_reviewed_confusable_neighbours": len(d_per_prompt),
            "prompts_without_reviewed_confusable_neighbours": len(runtime_rows) - len(d_per_prompt),
        },
        "dependency_group_size_distribution": dict(sorted(Counter(dep_sizes.values()).items())),
        "dq_relation_rule_counts": dict(sorted(Counter(row["relation_rule"] for row in dq_rows).items())),
        "bindings": bindings,
        "label_isolation": {
            "runtime_file": "label_free_query_runtime.jsonl",
            "runtime_top_level_keys": sorted(runtime_rows[0]),
            "offline_only_files": ["offline_label_adapter.jsonl", "reviewed_confusable_neighbour_ledger.jsonl"],
            "prohibited_in_runner": ["acceptable sets", "judgement dispositions", "D_q", "targets", "review outcomes"],
        },
        "statistical_contract": {
            "primary_scope": "714 B_NC_FULL_UNION prompts",
            "prespecified_sensitivity": "649 source-native NC prompts",
            "parent_reporting": "127 public and 236 controlled, separately, robustness only",
            "bootstrap": {"replicates": 10000, "unit": "whole dependency group", "seed": 2026090801},
            "paired_sign_flip": {"comparisons": ["P1", "P3", "P4", "P5"], "replicates": 100000, "unit": "whole dependency group", "seed": 2026090802, "two_sided_alpha": 0.01},
            "noninferiority": {"comparison": "P2", "one_sided_confidence": 0.99, "margin_absolute": -0.03},
        },
        "boundaries": [
            "The dependency components use only pre-outcome reporting groups and designated-source lineage; audited distractors and selector results do not create edges.",
            "The NC exposure ledger does not claim that absence of a bound historical outcome proves no human exposure.",
            "D_q is a reviewed diagnostic subset; it is not a complete semantic-neighbour graph and cannot be used as retrieval input.",
        ],
    }
    report["artifacts"] = {name: {"sha256": sha_bytes(data), "rows": len(data.splitlines())} for name, data in files.items()}
    report["builder_sha256"] = sha_path(Path(__file__).resolve())
    files["freeze_report.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 pre-outcome analysis freeze\n\n"
        "This package seals the 1,077 label-free runtime queries and keeps labels in offline-only ledgers before any V7 selector outcome is observed. "
        "Retrieval/reranking code may read only `label_free_query_runtime.jsonl`; it must not read the label adapter or reviewed-neighbour ledger.\n\n"
        "Dependency groups are connected components of same-lane reporting-group edges and shared designated-source lineage. No reviewed distractor or model result creates an edge. "
        "The exposure ledger conservatively records prior human/result exposure, and the D_q ledger is only a predefined reviewed diagnostic subset.\n\n"
        "Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_analysis_freeze.py --verify`\n"
    ).encode()
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = build()
    output = ROOT / OUTPUT
    if args.verify:
        require(output.is_dir(), "analysis freeze is not materialised")
        require({path.name for path in output.iterdir()} == set(expected), "analysis freeze file-set drift")
        for name, data in expected.items():
            require((output / name).read_bytes() == data, f"analysis freeze artifact drift: {name}")
        status = "PASS_PRE_OUTCOME_ANALYSIS_FREEZE_REPLAY"
    else:
        require(not output.exists(), "refusing to overwrite versioned analysis freeze")
        output.mkdir(parents=True)
        for name, data in expected.items():
            (output / name).write_bytes(data)
        status = "PASS_PRE_OUTCOME_ANALYSIS_FREEZE_CREATED"
    print(json.dumps({"status": status, "output": str(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
