#!/usr/bin/env python3
"""Offline-only V7 B36+C6 scorer and prespecified grouped analysis.

Runner output is validated before this module reads frozen offline labels.  The
CLI requires explicit runner paths and output path; it has no default selector
result location and makes no provider/model call.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from validate_rq2b_v7_runner_outputs import (
    ANALYSIS,
    ROOT,
    RunnerAuthority,
    file_sha256,
    read_jsonl,
    require,
    validate_outputs,
)


LABEL_PATH = ANALYSIS / "offline_label_adapter.jsonl"
DEPENDENCY_PATH = ANALYSIS / "dependency_ledger.jsonl"
EXPOSURE_PATH = ANALYSIS / "exposure_ledger.jsonl"
DQ_PATH = ANALYSIS / "reviewed_confusable_neighbour_ledger.jsonl"
QUALITY_RELATION_DIR = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_quality_relation_disposition_2026_09_09_v1"
QUALITY_CLOSURE_DIR = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_quality_closure_2026_09_09_v1"
SOURCE_EQUIVALENCE_PATH = QUALITY_RELATION_DIR / "source_equivalence_edges.jsonl"
PROMPT_DEPENDENCY_EDGE_PATH = QUALITY_RELATION_DIR / "prompt_dependency_edges.jsonl"
CUE_SENSITIVITY_PATH = QUALITY_CLOSURE_DIR / "cue_sensitivity_ledger.jsonl"
EXPECTED_OFFLINE_SHA256 = {
    LABEL_PATH: "cb11848e4a6d7938870e8bf5913335050538ac4f3c589ec9fe69bb303711357d",
    DEPENDENCY_PATH: "4226cfe2c9943d40026a4f1a9a38dbbc379ae9b8f39bd9b4c40aea8009e97fc7",
    EXPOSURE_PATH: "3749a72735a1c7034fd679fad24d4ce5ff40a8274144b15d8265bfb1c608dce3",
    DQ_PATH: "cb65d8dc40041630f201afc303604648fdc7ee5af270cbe877be33ab2a58dfb4",
}
EXPECTED_QUALITY_OVERLAY_SHA256 = {
    SOURCE_EQUIVALENCE_PATH: "c29e5868a39c943e3821a2408a6e8d6f2d3ef6cd2a73cb227fa05325e61ccb4f",
    PROMPT_DEPENDENCY_EDGE_PATH: "551201029e9a681ecc707a5357503c008c38c5e0a4220e86e4678e8775c01308",
    CUE_SENSITIVITY_PATH: "87eba0de1f8c15384df862b4652442f9b2410d216bbd2f17ca85d094df7e204f",
}

BOOTSTRAP_REPLICATES = 10_000
BOOTSTRAP_SEED = 2026090801
SIGN_FLIP_REPLICATES = 100_000
SIGN_FLIP_SEED = 2026090802
PRIMARY_ALPHA = 0.01
NONINFERIORITY_MARGIN = -0.03

ALIASES = {"C2-Q": "B05-GQ", "C2-S": "B05-GS"}
COMPARISONS = {
    "P1": ("B08-G0", "B02-G0", "candidate_hit_at_20", "SIGN_FLIP"),
    "P2": ("B08-G0", "B05-G0", "candidate_hit_at_20", "NONINFERIORITY"),
    "P3": ("B08-G0", "B11-G0", "known_a_hit_at_1", "SIGN_FLIP"),
    "P4": ("B05-GQ", "B05-G0", "known_a_hit_at_1", "SIGN_FLIP"),
    "P5": ("C3-Q", "C4-Q", "known_a_hit_at_1", "SIGN_FLIP"),
}
SCOPES: dict[str, Callable[[dict[str, Any]], bool]] = {
    "nc_primary": lambda row: row["lane_id"] == "B_NC_FULL_UNION" and not row["identity_cue_sensitivity"],
    "nc_full_descriptive": lambda row: row["lane_id"] == "B_NC_FULL_UNION",
    "nc_source_native_sensitivity": lambda row: row["reporting_stratum"] == "source_native_three_member",
    "nc_legacy_descriptive": lambda row: row["reporting_stratum"] == "legacy_2member_checkpoint",
    "parent_public_descriptive": lambda row: row["reporting_stratum"] == "public_gold",
    "parent_controlled_descriptive": lambda row: row["reporting_stratum"] == "controlled",
    "parent_delta_no_identity_cue_descriptive": lambda row: row["lane_id"] == "A_PARENT_DELTA" and not row["identity_cue_sensitivity"],
    "all_library_no_identity_cue_descriptive": lambda row: not row["identity_cue_sensitivity"],
    "identity_cue_sensitivity": lambda row: row["identity_cue_sensitivity"],
    "all_descriptive": lambda row: True,
}


@dataclass(frozen=True)
class OfflineAuthority:
    runner: RunnerAuthority
    labels: dict[str, dict[str, Any]]
    dependencies: dict[str, dict[str, Any]]
    exposures: dict[str, dict[str, Any]]
    dq_by_prompt: dict[str, dict[str, dict[str, Any]]]
    source_equivalence_edges: list[dict[str, Any]] = field(default_factory=list)
    cue_sensitivity_by_prompt: dict[str, dict[str, Any]] = field(default_factory=dict)
    prompt_dependency_edges: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def load(cls) -> "OfflineAuthority":
        runner = RunnerAuthority.load()
        for path, expected in {**EXPECTED_OFFLINE_SHA256, **EXPECTED_QUALITY_OVERLAY_SHA256}.items():
            actual = file_sha256(path)
            require(actual == expected, f"offline authority hash drift: {path}: {actual} != {expected}")
        label_rows = read_jsonl(LABEL_PATH)
        dependency_rows = read_jsonl(DEPENDENCY_PATH)
        exposure_rows = read_jsonl(EXPOSURE_PATH)
        dq_rows = read_jsonl(DQ_PATH)
        source_equivalence_edges = read_jsonl(SOURCE_EQUIVALENCE_PATH)
        cue_sensitivity_rows = read_jsonl(CUE_SENSITIVITY_PATH)
        prompt_dependency_edges = read_jsonl(PROMPT_DEPENDENCY_EDGE_PATH)
        labels = _unique_by_prompt(label_rows, "label adapter")
        dependencies = _unique_by_prompt(dependency_rows, "dependency ledger")
        exposures = _unique_by_prompt(exposure_rows, "exposure ledger")
        prompt_ids = set(runner.prompts)
        require(set(labels) == prompt_ids, "label adapter prompt coverage mismatch")
        require(set(dependencies) == prompt_ids, "dependency ledger prompt coverage mismatch")
        require(set(exposures) == prompt_ids, "exposure ledger prompt coverage mismatch")
        dq: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        for row in dq_rows:
            prompt_id = str(row["prompt_id"])
            source = str(row["candidate_source_sha256"])
            require(prompt_id in prompt_ids, f"D_q unknown prompt {prompt_id}")
            require(source not in dq[prompt_id], f"D_q duplicate relation {prompt_id}/{source}")
            dq[prompt_id][source] = row
        cue_sensitivity_by_prompt = _unique_by_prompt(cue_sensitivity_rows, "cue sensitivity ledger")
        require(len(source_equivalence_edges) == 25, "expected exactly 25 source-equivalence edges")
        require(len(cue_sensitivity_by_prompt) == 41, "expected exactly 41 cue-sensitivity prompts")
        require(len(prompt_dependency_edges) == 3, "expected exactly 3 prompt-dependency edges")
        authority = cls(
            runner, labels, dependencies, exposures, dict(dq),
            source_equivalence_edges, cue_sensitivity_by_prompt, prompt_dependency_edges,
        )
        authority.validate()
        return authority

    def validate(self) -> None:
        sources = self.runner.sources
        for prompt_id, runtime in self.runner.prompts.items():
            label = self.labels[prompt_id]
            dependency = self.dependencies[prompt_id]
            exposure = self.exposures[prompt_id]
            prompt_sha = runtime["prompt_sha256"]
            require(label["prompt_sha256"] == prompt_sha, f"label prompt hash drift: {prompt_id}")
            require(dependency["prompt_sha256"] == prompt_sha, f"dependency prompt hash drift: {prompt_id}")
            require(exposure["prompt_sha256"] == prompt_sha, f"exposure prompt hash drift: {prompt_id}")
            require(dependency["dependency_group"] == exposure["dependency_group"], f"dependency/exposure mismatch: {prompt_id}")
            acceptable = set(label["acceptable_set_source_sha256"])
            require(bool(acceptable) and acceptable <= sources, f"invalid A_q: {prompt_id}")
            judged_rows = label["judged_candidate_dispositions"]
            judged = {row["candidate_source_sha256"]: row["adequacy"] for row in judged_rows}
            require(len(judged) == len(judged_rows), f"duplicate J_q identity: {prompt_id}")
            require(set(judged) <= sources and acceptable <= set(judged), f"invalid J_q: {prompt_id}")
            fully_acceptable_dispositions = {
                "FULLY_ACCEPTABLE",
                "FULLY_ACCEPTABLE_INHERITED_HISTORICAL_STRICT_GOLD",
            }
            require(
                set(judged.values()) <= fully_acceptable_dispositions | {"PARTIALLY_ADEQUATE", "INADEQUATE"},
                f"unknown J_q disposition: {prompt_id}",
            )
            require(
                {source for source, disposition in judged.items() if disposition in fully_acceptable_dispositions} == acceptable,
                f"A_q/J_q disagreement: {prompt_id}",
            )
            require(label["library_source_count"] == len(sources), f"library count drift: {prompt_id}")
            require(label["unjudged_source_count"] == len(sources) - len(judged), f"U_q count drift: {prompt_id}")
            if label["final_label_type"] == "STRICT":
                require(len(acceptable) == 1, f"STRICT must have singleton A_q: {prompt_id}")
            else:
                require(label["final_label_type"] == "ACCEPTABLE_SET" and len(acceptable) > 1, f"invalid label type/cardinality: {prompt_id}")
            for source, dq_row in self.dq_by_prompt.get(prompt_id, {}).items():
                require(source in judged and source not in acceptable, f"D_q must be a subset of J_q minus A_q: {prompt_id}/{source}")
                require(dq_row["final_adequacy"] == judged[source], f"D_q disposition drift: {prompt_id}/{source}")
        _validate_source_equivalence_edges(self.source_equivalence_edges, sources)
        for prompt_id, row in self.cue_sensitivity_by_prompt.items():
            require(prompt_id in self.runner.prompts, f"cue ledger unknown prompt: {prompt_id}")
            require(row["schema_version"] == "rq2b-v7-phase8-cue-sensitivity-ledger-v1", f"cue ledger schema drift: {prompt_id}")
            require(row["prompt_sha256"] == self.runner.prompts[prompt_id]["prompt_sha256"], f"cue prompt hash drift: {prompt_id}")
            require(row["final_cue_decision"] == "AVOIDABLE_IDENTITY_CUE", f"cue disposition drift: {prompt_id}")
            require(row["analysis_disposition"] == "EXCLUDE_PRIMARY_INFERENTIAL_INCLUDE_SEPARATE_SENSITIVITY", f"cue analysis disposition drift: {prompt_id}")
            require(row["frozen_prompt_preserved"] is True, f"cue prompt was not preserved: {prompt_id}")
            require(row["primary_inferential_included"] is False and row["sensitivity_included"] is True, f"cue inclusion flags drift: {prompt_id}")
        _validate_prompt_dependency_edges(self.prompt_dependency_edges, self.runner.prompts, self.dependencies)

    def effective_sets(self, prompt_id: str) -> tuple[set[str], dict[str, str], dict[str, dict[str, Any]], str]:
        """Return prospective scoring sets without mutating the frozen label rows."""
        label = self.labels[prompt_id]
        frozen_acceptable = set(label["acceptable_set_source_sha256"])
        acceptable = set(frozen_acceptable)
        components = _source_equivalence_components(self.source_equivalence_edges)
        for source in frozen_acceptable:
            acceptable.update(components.get(source, {source}))
        judged = {
            item["candidate_source_sha256"]: item["adequacy"]
            for item in label["judged_candidate_dispositions"]
        }
        for source in acceptable - frozen_acceptable:
            judged[source] = "FULLY_ACCEPTABLE_EQUIVALENT_SOURCE"
        dq = {
            source: row for source, row in self.dq_by_prompt.get(prompt_id, {}).items()
            if source not in acceptable
        }
        effective_label_type = "STRICT" if len(acceptable) == 1 else "ACCEPTABLE_SET"
        return acceptable, judged, dq, effective_label_type


def _unique_by_prompt(rows: list[dict[str, Any]], name: str) -> dict[str, dict[str, Any]]:
    output = {str(row["prompt_id"]): row for row in rows}
    require(len(output) == len(rows), f"duplicate prompt in {name}")
    return output


def _source_equivalence_components(edges: list[dict[str, Any]]) -> dict[str, set[str]]:
    parent: dict[str, str] = {}

    def find(source: str) -> str:
        parent.setdefault(source, source)
        if parent[source] != source:
            parent[source] = find(parent[source])
        return parent[source]

    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for edge in edges:
        members = [str(member["source_sha256"]) for member in edge["members"]]
        for member in members[1:]:
            union(members[0], member)
    components: dict[str, set[str]] = defaultdict(set)
    for source in parent:
        components[find(source)].add(source)
    return {source: set(components[find(source)]) for source in parent}


def _validate_source_equivalence_edges(edges: list[dict[str, Any]], sources: set[str]) -> None:
    edge_ids: set[str] = set()
    for edge in edges:
        edge_id = str(edge["edge_id"])
        require(edge_id not in edge_ids, f"duplicate source-equivalence edge: {edge_id}")
        edge_ids.add(edge_id)
        require(edge["schema_version"] == "rq2b-v7-phase8-source-equivalence-edge-v1", f"source-equivalence schema drift: {edge_id}")
        require(edge["equivalence_scope"] == "acceptable_source_equivalence_and_offline_scoring", f"source-equivalence scope drift: {edge_id}")
        require(edge["relation"] in {"ALIAS_OR_FORK", "TRANSFORMED_COPY"}, f"invalid source equivalence relation: {edge_id}")
        require(edge["symmetric"] is True and edge["library_mutation"] is False, f"source-equivalence policy drift: {edge_id}")
        members = [str(member["source_sha256"]) for member in edge["members"]]
        require(len(members) >= 2 and len(set(members)) == len(members), f"invalid source-equivalence members: {edge_id}")
        require(set(members) <= sources, f"source-equivalence member outside frozen library: {edge_id}")


def _validate_prompt_dependency_edges(
    edges: list[dict[str, Any]], prompts: dict[str, dict[str, Any]], dependencies: dict[str, dict[str, Any]],
) -> None:
    edge_ids: set[str] = set()
    for edge in edges:
        edge_id = str(edge["edge_id"])
        require(edge_id not in edge_ids, f"duplicate prompt-dependency edge: {edge_id}")
        edge_ids.add(edge_id)
        require(edge["schema_version"] == "rq2b-v7-phase8-prompt-dependency-edge-v1", f"prompt-dependency schema drift: {edge_id}")
        require(edge["dependency_scope"] == "dependency_clustered_inference", f"prompt-dependency scope drift: {edge_id}")
        require(edge["relation"] == "TRANSFORMED_DUPLICATE", f"prompt-dependency relation drift: {edge_id}")
        require(edge["symmetric"] is True and edge["prompt_mutation"] is False, f"prompt-dependency policy drift: {edge_id}")
        member_ids = [str(member["prompt_id"]) for member in edge["members"]]
        require(len(member_ids) >= 2 and len(set(member_ids)) == len(member_ids), f"invalid prompt-dependency members: {edge_id}")
        for member in edge["members"]:
            prompt_id = str(member["prompt_id"])
            require(prompt_id in prompts, f"prompt-dependency member outside frozen scope: {edge_id}/{prompt_id}")
            require(member["prompt_sha256"] == prompts[prompt_id]["prompt_sha256"], f"prompt-dependency hash drift: {edge_id}/{prompt_id}")
        groups = {dependencies[prompt_id]["dependency_group"] for prompt_id in member_ids}
        require(len(groups) == 1, f"prompt-dependency edge crosses frozen components: {edge_id}")


def _first_reciprocal_rank(ranking: list[str], acceptable: set[str]) -> float:
    for index, source in enumerate(ranking, 1):
        if source in acceptable:
            return 1.0 / index
    return 0.0


def score_rows(
    b1_rows: list[dict[str, Any]], b2_rows: list[dict[str, Any]], authority: OfflineAuthority,
) -> list[dict[str, Any]]:
    validate_outputs(b1_rows, b2_rows, authority.runner, require_complete=True)
    b1 = {(row["condition_id"], row["prompt_id"]): row for row in b1_rows}
    output: list[dict[str, Any]] = []
    for row in [*b1_rows, *b2_rows]:
        prompt_id = str(row["prompt_id"])
        label = authority.labels[prompt_id]
        dependency = authority.dependencies[prompt_id]
        exposure = authority.exposures[prompt_id]
        frozen_acceptable = set(label["acceptable_set_source_sha256"])
        acceptable, judged, dq, effective_label_type = authority.effective_sets(prompt_id)
        if row["schema_version"].endswith("b1-runner-output-v1"):
            candidate_ranking = [item["source_sha256"] for item in row["ranked_candidates"][:20]]
            final_ranking = candidate_ranking
            stage = "B1"
            baseline = None
        else:
            candidate_ranking = [item["source_sha256"] for item in row["input_candidates"]]
            final_ranking = [item["source_sha256"] for item in row["reranked_candidates"]]
            stage = "B2"
            baseline_condition = f"{row['persisted_candidate_source']}-G0"
            baseline = b1[(baseline_condition, prompt_id)]["ranked_candidates"][0]["source_sha256"]
        top1 = final_ranking[0]
        candidate_hit = float(bool(set(candidate_ranking) & acceptable))
        known_hit = float(top1 in acceptable)
        top1_disposition = judged.get(top1, "UNJUDGED")
        cstar_eligible = bool(set(candidate_ranking) & acceptable) and bool(set(candidate_ranking) & set(dq))
        scored = {
            "condition_id": row["condition_id"],
            "stage": stage,
            "prompt_id": prompt_id,
            "prompt_sha256": row["prompt_sha256"],
            "lane_id": label["lane_id"],
            "reporting_stratum": label["reporting_stratum"],
            "dependency_group": dependency["dependency_group"],
            "analysis_disposition": exposure["analysis_disposition"],
            "identity_cue_sensitivity": prompt_id in authority.cue_sensitivity_by_prompt,
            "frozen_label_type": label["final_label_type"],
            "final_label_type": effective_label_type,
            "acceptable_set_size_frozen": len(frozen_acceptable),
            "acceptable_set_size_effective": len(acceptable),
            "source_equivalence_expansion_count": len(acceptable - frozen_acceptable),
            "known_a_hit_at_1": known_hit,
            "candidate_hit_at_20": candidate_hit,
            "set_recall_at_20": len(set(candidate_ranking) & acceptable) / len(acceptable),
            "mrr_at_20": _first_reciprocal_rank(final_ranking, acceptable),
            "unjudged_at_1": float(top1 not in judged),
            "unjudged_fraction_at_20": sum(source not in judged for source in final_ranking) / 20.0,
            "reviewed_error_at_1": float(top1 in judged and top1 not in acceptable),
            "reviewed_partial_at_1": float(top1_disposition == "PARTIALLY_ADEQUATE"),
            "reviewed_inadequate_at_1": float(top1_disposition == "INADEQUATE"),
            "dq_top1": float(top1 in dq),
            "dq_relation_rule_at_1": dq[top1]["relation_rule"] if top1 in dq else None,
            "cstar_eligible": cstar_eligible,
            "baseline_top1_known_a": None if baseline is None else float(baseline in acceptable),
            "baseline_top1_dq": None if baseline is None else float(baseline in dq),
            "acceptable_to_dq_regression": None if baseline is None or not cstar_eligible else float(baseline in acceptable and top1 in dq),
            "dq_to_acceptable_rescue": None if baseline is None or not cstar_eligible else float(baseline in dq and top1 in acceptable),
            "cost": row["cost"],
        }
        require(abs(known_hit - candidate_hit * (known_hit if candidate_hit else 0.0)) < 1e-12, f"row-level candidate/Hit identity failed: {row['condition_id']}/{prompt_id}")
        output.append(scored)
    return output


def _mean(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [float(row[key]) for row in rows if row[key] is not None]
    return None if not values else float(sum(values) / len(values))


def _metric_block(rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(bool(rows), "cannot summarise an empty endpoint")
    candidate_hits = sum(row["candidate_hit_at_20"] for row in rows)
    conditional = None if candidate_hits == 0 else sum(row["known_a_hit_at_1"] for row in rows) / candidate_hits
    hit = _mean(rows, "known_a_hit_at_1")
    candidate_hit = _mean(rows, "candidate_hit_at_20")
    require(hit is not None and candidate_hit is not None, "missing primary metrics")
    identity_rhs = None if conditional is None else candidate_hit * conditional
    require(identity_rhs is None or abs(hit - identity_rhs) < 1e-12, "Hit = CandidateHit * ConditionalHit identity failed")
    unknown = _mean(rows, "unjudged_at_1")
    return {
        "prompts": len(rows),
        "dependency_groups": len({row["dependency_group"] for row in rows}),
        "known_a_hit_at_1": hit,
        "candidate_hit_at_20": candidate_hit,
        "set_recall_at_20": _mean(rows, "set_recall_at_20"),
        "mrr_at_20": _mean(rows, "mrr_at_20"),
        "conditional_known_a_hit_at_1": conditional,
        "identity_residual": None if identity_rhs is None else hit - identity_rhs,
        "reviewed_error_at_1": _mean(rows, "reviewed_error_at_1"),
        "reviewed_partial_at_1": _mean(rows, "reviewed_partial_at_1"),
        "reviewed_inadequate_at_1": _mean(rows, "reviewed_inadequate_at_1"),
        "unjudged_at_1": unknown,
        "unjudged_fraction_at_20": _mean(rows, "unjudged_fraction_at_20"),
        "known_a_identification_interval_at_1": [hit, hit + (unknown or 0.0)],
    }


def _group_macro(rows: list[dict[str, Any]], key: str) -> float:
    values: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        values[row["dependency_group"]].append(float(row[key]))
    return sum(sum(group_values) / len(group_values) for group_values in values.values()) / len(values)


def percentile(values: list[float], quantile: float) -> float:
    require(bool(values), "percentile requires values")
    require(0.0 <= quantile <= 1.0, "invalid quantile")
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def _cost_block(rows: list[dict[str, Any]]) -> dict[str, Any]:
    latency = [float(row["cost"]["wall_time_ms"]) for row in rows]
    additive = ["provider_calls", "input_tokens", "output_tokens", "window_forwards", "cache_hits", "retry_count", "timeout_count", "failure_count"]
    return {
        "wall_time_ms_p50": percentile(latency, 0.50),
        "wall_time_ms_p95": percentile(latency, 0.95),
        **{f"{key}_total": int(sum(int(row["cost"][key]) for row in rows)) for key in additive},
    }


def condition_summaries(scored_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored_rows:
        by_condition[row["condition_id"]].append(row)
    summaries: dict[str, Any] = {}
    for condition_id, condition_rows in sorted(by_condition.items()):
        scope_output: dict[str, Any] = {}
        for scope_name, predicate in SCOPES.items():
            scope_rows = [row for row in condition_rows if predicate(row)]
            if not scope_rows:
                continue
            strict_rows = [row for row in scope_rows if row["final_label_type"] == "STRICT"]
            cstar = [row for row in scope_rows if row["cstar_eligible"]]
            scope_output[scope_name] = {
                "acceptable_known_a": _metric_block(scope_rows),
                "strict_singleton": None if not strict_rows else _metric_block(strict_rows),
                "equal_dependency_group_weighted_sensitivity": {
                    key: _group_macro(scope_rows, key)
                    for key in ("known_a_hit_at_1", "candidate_hit_at_20", "mrr_at_20", "unjudged_at_1")
                },
                "dq_diagnostic": {
                    "cstar_eligible_prompts": len(cstar),
                    "cstar_coverage": len(cstar) / len(scope_rows),
                    "dq_top1_rate_within_cstar": _mean(cstar, "dq_top1") if cstar else None,
                    "acceptable_to_dq_regression_rate": _mean(cstar, "acceptable_to_dq_regression") if cstar else None,
                    "dq_to_acceptable_rescue_rate": _mean(cstar, "dq_to_acceptable_rescue") if cstar else None,
                    "top1_relation_rule_counts": dict(sorted(Counter(row["dq_relation_rule_at_1"] for row in cstar if row["dq_relation_rule_at_1"]).items())),
                },
                "cost": _cost_block(scope_rows),
            }
        summaries[condition_id] = scope_output
    return summaries


def _paired_group_arrays(
    left: list[dict[str, Any]], right: list[dict[str, Any]], metric: str,
) -> tuple[list[str], list[float], list[int], list[dict[str, Any]], list[dict[str, Any]]]:
    left_map = {row["prompt_id"]: row for row in left}
    right_map = {row["prompt_id"]: row for row in right}
    require(len(left_map) == len(left) and len(right_map) == len(right), "duplicate prompt in comparison condition")
    require(set(left_map) == set(right_map), "paired conditions do not cover identical prompt IDs")
    prompt_ids = sorted(left_map)
    group_sums: dict[str, float] = defaultdict(float)
    group_counts: dict[str, int] = defaultdict(int)
    for prompt_id in prompt_ids:
        lrow, rrow = left_map[prompt_id], right_map[prompt_id]
        require(lrow["prompt_sha256"] == rrow["prompt_sha256"], f"paired prompt hash mismatch: {prompt_id}")
        require(lrow["dependency_group"] == rrow["dependency_group"], f"paired dependency mismatch: {prompt_id}")
        group = lrow["dependency_group"]
        group_sums[group] += float(lrow[metric]) - float(rrow[metric])
        group_counts[group] += 1
    groups = sorted(group_sums)
    return (
        groups,
        [group_sums[group] for group in groups],
        [group_counts[group] for group in groups],
        [left_map[prompt_id] for prompt_id in prompt_ids],
        [right_map[prompt_id] for prompt_id in prompt_ids],
    )


def grouped_bootstrap(
    sums: list[float], counts: list[int], *, replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
) -> list[float]:
    require(len(sums) > 0 and len(sums) == len(counts), "invalid dependency group arrays")
    rng = random.Random(seed)
    group_count = len(sums)
    draws: list[float] = []
    for _ in range(replicates):
        sampled = [rng.randrange(group_count) for _ in range(group_count)]
        draws.append(
            sum(sums[index] for index in sampled)
            / sum(counts[index] for index in sampled)
        )
    return draws


def grouped_sign_flip_pvalue(
    sums: list[float], total_prompts: int, *, replicates: int = SIGN_FLIP_REPLICATES,
    seed: int = SIGN_FLIP_SEED,
) -> float:
    observed = abs(sum(sums) / total_prompts)
    rng = random.Random(seed)
    exceed = 0
    group_count = len(sums)
    for _ in range(replicates):
        bits = rng.getrandbits(group_count)
        draw = sum(value if (bits >> index) & 1 else -value for index, value in enumerate(sums)) / total_prompts
        exceed += abs(draw) >= observed - 1e-15
    return (exceed + 1.0) / (replicates + 1.0)


def primary_comparisons(
    scored_rows: list[dict[str, Any]], *, bootstrap_replicates: int = BOOTSTRAP_REPLICATES,
    sign_flip_replicates: int = SIGN_FLIP_REPLICATES,
) -> dict[str, Any]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored_rows:
        if row["lane_id"] == "B_NC_FULL_UNION" and not row["identity_cue_sensitivity"]:
            by_condition[row["condition_id"]].append(row)
    output: dict[str, Any] = {}
    for comparison_id, (left_id, right_id, metric, test) in COMPARISONS.items():
        require(left_id in by_condition and right_id in by_condition, f"missing {comparison_id} condition")
        groups, sums, counts, left_rows, right_rows = _paired_group_arrays(by_condition[left_id], by_condition[right_id], metric)
        prompt_count = sum(counts)
        estimate = sum(sums) / prompt_count
        group_macro = sum(group_sum / group_count for group_sum, group_count in zip(sums, counts)) / len(sums)
        draws = grouped_bootstrap(sums, counts, replicates=bootstrap_replicates)
        lower95, upper95 = percentile(draws, 0.025), percentile(draws, 0.975)
        lower_terms = [
            lrow["known_a_hit_at_1"] - (rrow["known_a_hit_at_1"] + rrow["unjudged_at_1"])
            for lrow, rrow in zip(left_rows, right_rows)
        ] if metric == "known_a_hit_at_1" else []
        upper_terms = [
            (lrow["known_a_hit_at_1"] + lrow["unjudged_at_1"]) - rrow["known_a_hit_at_1"]
            for lrow, rrow in zip(left_rows, right_rows)
        ] if metric == "known_a_hit_at_1" else []
        pair_bounds_lower = sum(lower_terms) / len(lower_terms) if lower_terms else None
        pair_bounds_upper = sum(upper_terms) / len(upper_terms) if upper_terms else None
        record: dict[str, Any] = {
            "comparison_id": comparison_id,
            "left_condition": left_id,
            "right_condition": right_id,
            "metric": metric,
            "scope": "B_NC_FULL_UNION_EXCLUDING_IDENTITY_CUE_SENSITIVITY",
            "prompts": prompt_count,
            "dependency_groups": len(groups),
            "prompt_weighted_left_minus_right": estimate,
            "equal_dependency_group_weighted_sensitivity": group_macro,
            "descriptive_95_percent_group_bootstrap_ci": [float(lower95), float(upper95)],
            "bootstrap": {"replicates": bootstrap_replicates, "seed": BOOTSTRAP_SEED, "unit": "whole dependency_group"},
            "known_a_difference_identification_interval": None if pair_bounds_lower is None else [float(pair_bounds_lower), float(pair_bounds_upper)],
        }
        if test == "SIGN_FLIP":
            pvalue = grouped_sign_flip_pvalue(sums, prompt_count, replicates=sign_flip_replicates)
            record["paired_group_sign_flip"] = {
                "replicates": sign_flip_replicates,
                "seed": SIGN_FLIP_SEED,
                "two_sided_p_value": pvalue,
                "alpha": PRIMARY_ALPHA,
                "passes_prespecified_alpha": pvalue < PRIMARY_ALPHA,
                "unit": "whole dependency_group",
            }
        else:
            lower99 = percentile(draws, 0.01)
            record["noninferiority"] = {
                "one_sided_confidence": 0.99,
                "group_bootstrap_lower_bound": lower99,
                "margin": NONINFERIORITY_MARGIN,
                "established": lower99 > NONINFERIORITY_MARGIN,
                "strict_rule": "lower_bound > margin",
            }
        output[comparison_id] = record
    return output


def analyse(
    b1_rows: list[dict[str, Any]], b2_rows: list[dict[str, Any]], authority: OfflineAuthority,
    *, bootstrap_replicates: int = BOOTSTRAP_REPLICATES,
    sign_flip_replicates: int = SIGN_FLIP_REPLICATES,
) -> dict[str, Any]:
    scored = score_rows(b1_rows, b2_rows, authority)
    conditions = {row["condition_id"] for row in scored}
    require(len(conditions) == 42, f"expected 42 materialised outcomes, got {len(conditions)}")
    expected_rows = len(authority.runner.prompts) * 42
    require(len(scored) == expected_rows, f"expected {expected_rows} outcome rows, got {len(scored)}")
    candidate_hit_by_b1 = {
        (row["condition_id"].removesuffix("-G0"), row["prompt_id"]): row["candidate_hit_at_20"]
        for row in scored if row["stage"] == "B1"
    }
    for row in scored:
        if row["stage"] == "B2":
            source = authority.runner.b2_conditions[row["condition_id"]]["persisted_candidate_source"]
            require(row["candidate_hit_at_20"] == candidate_hit_by_b1[(source, row["prompt_id"])], f"B2 CandidateHit changed: {row['condition_id']}/{row['prompt_id']}")
    return {
        "schema_version": "rq2b-v7-offline-analysis-v2",
        "status": "PASS_COMPLETE_OFFLINE_SCORING_AND_PRESPECIFIED_ANALYSIS",
        "counts": {
            "queries": len(authority.runner.prompts),
            "b1_conditions": 12,
            "core_b2_conditions": 24,
            "bridge_b2_conditions": 6,
            "materialised_outcome_conditions": 42,
            "materialised_outcome_rows": len(scored),
            "c2_alias_input_rows": 0,
        },
        "aliases": ALIASES,
        "authority_hashes": {
            str(path.relative_to(ROOT)): sha
            for path, sha in {**EXPECTED_OFFLINE_SHA256, **EXPECTED_QUALITY_OVERLAY_SHA256}.items()
        },
        "quality_overlay_summary": {
            "source_equivalence_edges": len(authority.source_equivalence_edges),
            "source_equivalence_components": len({
                frozenset(component)
                for component in _source_equivalence_components(authority.source_equivalence_edges).values()
            }),
            "prompts_with_expanded_acceptable_sets": len({
                row["prompt_id"] for row in scored if row["source_equivalence_expansion_count"] > 0
            }),
            "cue_sensitivity_prompts": len(authority.cue_sensitivity_by_prompt),
            "all_library_no_identity_cue_prompts": len(authority.runner.prompts) - len(authority.cue_sensitivity_by_prompt),
            "nc_primary_prompts": sum(
                runtime_prompt_id not in authority.cue_sensitivity_by_prompt
                and authority.labels[runtime_prompt_id]["lane_id"] == "B_NC_FULL_UNION"
                for runtime_prompt_id in authority.runner.prompts
            ),
            "parent_delta_no_identity_cue_prompts": sum(
                runtime_prompt_id not in authority.cue_sensitivity_by_prompt
                and authority.labels[runtime_prompt_id]["lane_id"] == "A_PARENT_DELTA"
                for runtime_prompt_id in authority.runner.prompts
            ),
            "prompt_dependency_edges": len(authority.prompt_dependency_edges),
            "boundary": (
                "P1-P5 retain the approved NC primary estimand. The all-library no-cue scope is descriptive; "
                "identity-cue prompts are sensitivity-only, and source equivalence is an offline credit overlay."
            ),
        },
        "exposure_summary": {
            "analysis_disposition": dict(sorted(Counter(row["analysis_disposition"] for row in authority.exposures.values()).items())),
            "prompt_level_exposure": dict(sorted(Counter(row["prompt_level_exposure"] for row in authority.exposures.values()).items())),
            "global_design_exposure": dict(sorted(Counter(row["global_design_exposure"] for row in authority.exposures.values()).items())),
            "boundary": "Exposure is reported, not used to form outcome-conditioned dependency groups or exclusions.",
        },
        "condition_summaries": condition_summaries(scored),
        "primary_comparisons": primary_comparisons(scored, bootstrap_replicates=bootstrap_replicates, sign_flip_replicates=sign_flip_replicates),
        "scored_rows": scored,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--b1", type=Path, required=True, help="Explicit label-free B1 JSONL")
    parser.add_argument("--b2", type=Path, required=True, help="Explicit label-free B2 JSONL")
    parser.add_argument("--output", type=Path, required=True, help="New offline analysis JSON path")
    args = parser.parse_args()
    require(not args.output.exists(), f"refusing to overwrite {args.output}")
    report = analyse(read_jsonl(args.b1), read_jsonl(args.b2), OfflineAuthority.load())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(args.output), "counts": report["counts"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
