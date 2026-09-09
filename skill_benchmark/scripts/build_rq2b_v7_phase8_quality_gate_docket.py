#!/usr/bin/env python3
"""Replay mechanical V7 quality evidence and emit a fail-closed docket.

This builder never creates a Phase-8 quality PASS report.  It hashes the final
prompt manifest without parsing it, and reads only label-free runtime,
dependency, exposure, source, and aggregate freeze records.  Missing semantic
review/adjudication evidence is recorded as a blocker rather than inferred
from an aggregate PASS sentence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


QUALITY_BUILDER_VERSION = "rq2b-v7-phase8-quality-gate-docket-builder-v1"
DOCKET_SCHEMA = "rq2b-v7-phase8-quality-gate-blocking-docket-v1"
INTEGRITY_SCHEMA = "rq2b-v7-phase8-quality-gate-docket-integrity-v1"
REQUIREMENT_SCHEMA = "rq2b-v7-phase8-quality-review-requirement-v1"
QUALITY_REPORT_SCHEMA = "rq2b-v7-phase8-quality-gate-v2"
BLOCKED_STATUS = "BLOCKED_PHASE8_QUALITY_REPORTS_REQUIRE_FINAL_REPLAYABLE_EVIDENCE"

EXPECTED_PROMPTS = 1077
EXPECTED_SOURCES = 3798
EXPECTED_DEPENDENCY_GROUPS = 355
EXPECTED_PARENT_PROMPTS = 363
EXPECTED_NC_PROMPTS = 714
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"

QUALITY_ASSERTIONS = {
    "split": [
        "prompt_scope_identity_replayed",
        "dependency_and_exposure_coverage_complete",
        "dependency_components_respected",
        "cross_lane_components_dispositioned",
        "no_unresolved_split_leakage",
    ],
    "cue": [
        "final_prompt_scope_reviewed",
        "target_title_repository_provider_path_and_literal_source_cues_checked",
        "unavoidable_cues_stratified",
        "remediations_and_exclusions_replayed",
        "no_unresolved_cue_findings",
    ],
    "duplication": [
        "source_sha_unique",
        "prompt_sha_unique",
        "aliases_forks_and_transformed_copies_reviewed",
        "dependency_edges_or_exclusions_bound",
        "no_unresolved_duplication",
    ],
    "semantic_near_copy": [
        "final_prompt_scope_reviewed",
        "final_source_scope_reviewed",
        "semantic_near_copy_relations_adjudicated",
        "dependency_edges_or_exclusions_bound",
        "no_unresolved_semantic_near_copy",
    ],
    "coverage": [
        "source_manifest_3798_replayed",
        "prompt_scope_1077_replayed",
        "dependency_exposure_1077_replayed",
        "source_bytes_replayed",
        "final_freeze_scope_and_exclusions_bound",
    ],
}
SEMANTIC_GATES = {"split", "cue", "duplication", "semantic_near_copy"}


@dataclass(frozen=True)
class FixedArtifact:
    path: str
    sha256: str
    opaque: bool = False


FIXED_ARTIFACTS = {
    "approved_plan": FixedArtifact(
        "thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md",
        "b54d3d8c6816b2bb5f75b2b946448063fcc800c1f9927e27babd767e3468d4d8",
    ),
    "master_sop": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md",
        "68f7a8e4e802317208d72155b6b3490d0f3587324aaebb67cfac0341241b8835",
    ),
    "plan_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/rq2_approved_research_plan_2026_09_08_v1/plan_freeze.json",
        "c91b459babec83409b5b17d254cc299a77081afc94fc813173ad3ae7f80eb097",
    ),
    "phase3_closure": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05/summary.json",
        "469363a5ef69c5d1a35b8724967f98d485cb4d4ac0ddae3778b2a43454d2238a",
    ),
    "final_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/integrity_report.json",
        "f77df13f55fd151a2831ba448c6efa4bf760942f9e925f837eeb9a365c8eed4a",
    ),
    "final_prompt_manifest": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/final_library_prompt_manifest.jsonl",
        PROMPT_MANIFEST_SHA256,
        opaque=True,
    ),
    "first_matrix_readiness": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/readiness_report.json",
        "55f666bc3daa96f3e37f7209761b4a0c06eb7aaf14484db0a4b7d6aea94725e0",
    ),
    "source_manifest": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_2026_09_08_v1/source_manifest.jsonl",
        "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    ),
    "analysis_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/freeze_report.json",
        "1b27a1a6f7423871c7e9b7206736d60e3838e405af1cf2f5b078f0db58f784f7",
    ),
    "dependency_ledger": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/dependency_ledger.jsonl",
        "4226cfe2c9943d40026a4f1a9a38dbbc379ae9b8f39bd9b4c40aea8009e97fc7",
    ),
    "exposure_ledger": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/exposure_ledger.jsonl",
        "3749a72735a1c7034fd679fad24d4ce5ff40a8274144b15d8265bfb1c608dce3",
    ),
    "label_free_runtime": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl",
        "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def rows_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(row) for row in rows)


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def root_path(root: Path, value: str, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: path missing")
    raw = Path(value)
    path = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def exact_keys(value: Any, expected: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: expected object")
    require(set(value) == expected, f"{field}: key drift: {sorted(set(value) ^ expected)}")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected object: {path}:{line_number}")
            rows.append(value)
    return rows


def validate_fixed(root: Path, fixed: dict[str, FixedArtifact]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role, artifact in fixed.items():
        path = root_path(root, artifact.path, field=role)
        require(path.is_file(), f"Missing fixed artifact: {role}")
        require(file_sha256(path) == artifact.sha256, f"Fixed artifact hash drift: {role}")
        result[role] = {
            "path": artifact.path,
            "sha256": artifact.sha256,
            "bytes": path.stat().st_size,
            "content_access": "HASH_ONLY_OPAQUE_PROVENANCE" if artifact.opaque else "PARSED_MECHANICAL_REPLAY",
        }
    return result


def validate_runtime(path: Path) -> tuple[list[dict[str, Any]], dict[str, str]]:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_PROMPTS, "Runtime prompt count drift")
    by_id: dict[str, str] = {}
    prompt_hashes: set[str] = set()
    for index, row in enumerate(rows, 1):
        exact_keys(row, {"schema_version", "prompt_id", "prompt_sha256", "prompt"}, f"runtime[{index}]")
        require(row["schema_version"] == "rq2b-v7-label-free-query-runtime-v1", f"runtime[{index}]: schema drift")
        require(isinstance(row["prompt_id"], str) and row["prompt_id"], f"runtime[{index}]: prompt ID drift")
        require(row["prompt_sha256"] == text_sha256(row["prompt"]), f"runtime[{index}]: prompt hash drift")
        require(row["prompt_id"] not in by_id and row["prompt_sha256"] not in prompt_hashes, "Exact prompt identity/text duplicate")
        by_id[row["prompt_id"]] = row["prompt_sha256"]
        prompt_hashes.add(row["prompt_sha256"])
    return rows, by_id


def validate_sources(root: Path, path: Path) -> tuple[list[dict[str, Any]], int]:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_SOURCES, "Source count drift")
    hashes: set[str] = set()
    paths: set[str] = set()
    total_bytes = 0
    for index, row in enumerate(rows, 1):
        exact_keys(row, {"path", "sha256", "bytes"}, f"source[{index}]")
        require(re.fullmatch(r"[0-9a-f]{64}", str(row["sha256"])) is not None, f"source[{index}]: invalid SHA")
        require(row["sha256"] not in hashes and row["path"] not in paths, "Exact source identity/path duplicate")
        source_path = root_path(root, row["path"], field=f"source[{index}].path")
        require(source_path.is_file(), f"source[{index}]: source file missing")
        require(source_path.stat().st_size == row["bytes"], f"source[{index}]: byte count drift")
        require(file_sha256(source_path) == row["sha256"], f"source[{index}]: SHA drift")
        hashes.add(row["sha256"])
        paths.add(row["path"])
        total_bytes += row["bytes"]
    return rows, total_bytes


def validate_dependency_and_exposure(
    dependency_path: Path, exposure_path: Path, prompt_by_id: dict[str, str]
) -> dict[str, Any]:
    dependencies = read_jsonl(dependency_path)
    exposures = read_jsonl(exposure_path)
    require(len(dependencies) == len(exposures) == EXPECTED_PROMPTS, "Dependency/exposure coverage drift")
    dep_by_prompt: dict[str, dict[str, Any]] = {}
    lanes_by_group: dict[str, set[str]] = defaultdict(set)
    for index, row in enumerate(dependencies, 1):
        exact_keys(row, {"schema_version", "prompt_id", "prompt_sha256", "dependency_group", "lane_id", "reporting_group", "dependency_anchor_source_sha256", "edge_policy"}, f"dependency[{index}]")
        require(row["schema_version"] == "rq2b-v7-dependency-ledger-v1", f"dependency[{index}]: schema drift")
        require(prompt_by_id.get(row["prompt_id"]) == row["prompt_sha256"], f"dependency[{index}]: prompt binding drift")
        require(row["prompt_id"] not in dep_by_prompt, f"dependency[{index}]: duplicate prompt")
        dep_by_prompt[row["prompt_id"]] = row
        lanes_by_group[row["dependency_group"]].add(row["lane_id"])
    require(set(dep_by_prompt) == set(prompt_by_id), "Dependency prompt scope drift")
    require(len(lanes_by_group) == EXPECTED_DEPENDENCY_GROUPS, "Dependency-group count drift")

    exp_by_prompt: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(exposures, 1):
        exact_keys(row, {"schema_version", "prompt_id", "prompt_sha256", "dependency_group", "prompt_level_exposure", "historical_selector_outcome_evidence", "global_design_exposure", "analysis_disposition"}, f"exposure[{index}]")
        require(row["schema_version"] == "rq2b-v7-exposure-ledger-v1", f"exposure[{index}]: schema drift")
        dependency = dep_by_prompt.get(row["prompt_id"])
        require(dependency is not None and row["prompt_sha256"] == dependency["prompt_sha256"] and row["dependency_group"] == dependency["dependency_group"], f"exposure[{index}]: dependency binding drift")
        require(row["prompt_id"] not in exp_by_prompt, f"exposure[{index}]: duplicate prompt")
        exp_by_prompt[row["prompt_id"]] = row
    require(set(exp_by_prompt) == set(prompt_by_id), "Exposure prompt scope drift")
    disposition_counts = Counter(row["analysis_disposition"] for row in exposures)
    require(disposition_counts == {"NC_PRIMARY_WITH_SOURCE_NATIVE_SENSITIVITY": EXPECTED_NC_PROMPTS, "PARENT_ROBUSTNESS_ONLY": EXPECTED_PARENT_PROMPTS}, "Exposure disposition count drift")
    mixed = sorted(group for group, lanes in lanes_by_group.items() if len(lanes) > 1)
    return {
        "dependency_groups": len(lanes_by_group),
        "mixed_lane_dependency_groups": len(mixed),
        "mixed_lane_dependency_group_ids": mixed,
        "exposure_dispositions": dict(sorted(disposition_counts.items())),
    }


def validate_reports(root: Path, fixed: dict[str, FixedArtifact]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    final_freeze = read_json(root / fixed["final_freeze"].path)
    require(final_freeze.get("status") == "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION", "Final freeze status drift")
    require(final_freeze.get("counts", {}).get("frozen_final_library_groups") == EXPECTED_PROMPTS, "Final freeze prompt count drift")
    require(final_freeze.get("output_hashes", {}).get("final_library_prompt_manifest.jsonl") == PROMPT_MANIFEST_SHA256, "Final freeze prompt hash drift")

    matrix = read_json(root / fixed["first_matrix_readiness"].path)
    require(matrix.get("status") == "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED", "First-matrix status drift")
    require(matrix.get("counts", {}).get("prompts") == EXPECTED_PROMPTS and matrix.get("counts", {}).get("sources") == EXPECTED_SOURCES, "First-matrix coverage drift")
    require(matrix.get("bindings", {}).get("prompt_manifest_sha256") == PROMPT_MANIFEST_SHA256 and matrix.get("bindings", {}).get("source_union_sha256") == SOURCE_UNION_SHA256, "First-matrix root binding drift")

    analysis = read_json(root / fixed["analysis_freeze"].path)
    require(analysis.get("status") == "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE", "Analysis-freeze status drift")
    require(analysis.get("counts", {}).get("prompts") == EXPECTED_PROMPTS and analysis.get("counts", {}).get("candidates") == EXPECTED_SOURCES, "Analysis-freeze coverage drift")
    for role, filename in (("dependency_ledger", "dependency_ledger.jsonl"), ("exposure_ledger", "exposure_ledger.jsonl"), ("label_free_runtime", "label_free_query_runtime.jsonl")):
        item = analysis.get("artifacts", {}).get(filename, {})
        require(item.get("rows") == EXPECTED_PROMPTS and item.get("sha256") == fixed[role].sha256, f"Analysis-freeze artifact binding drift: {filename}")
    require(analysis.get("label_isolation", {}).get("runtime_file") == "label_free_query_runtime.jsonl", "Analysis-freeze runtime isolation drift")

    phase3 = read_json(root / fixed["phase3_closure"].path)
    require(phase3.get("status") == "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE", "Phase-3 closure status drift")
    bound_inputs = phase3.get("bound_inputs")
    require(isinstance(bound_inputs, dict) and bound_inputs, "Phase-3 closure lacks bound inputs")
    replay: list[dict[str, Any]] = []
    for path_value, expected_sha in sorted(bound_inputs.items()):
        path = root_path(root, path_value, field="phase3 bound input")
        exists = path.is_file()
        actual_sha = file_sha256(path) if exists else None
        replay.append({"path": path_value, "expected_sha256": expected_sha, "exists": exists, "hash_matches": exists and actual_sha == expected_sha})
    return {"final_freeze": final_freeze, "first_matrix": matrix, "analysis_freeze": analysis, "phase3_closure": phase3}, replay


def quality_report_contract() -> dict[str, Any]:
    return {
        "schema_version": "rq2b-v7-phase8-quality-report-contract-v2",
        "accepted_report_schema": QUALITY_REPORT_SCHEMA,
        "required_gates": sorted(QUALITY_ASSERTIONS),
        "required_assertions": QUALITY_ASSERTIONS,
        "semantic_review_required_for": sorted(SEMANTIC_GATES),
        "semantic_receipt_access": "HASH_ONLY_OPAQUE_FINAL_ADJUDICATION_PROVENANCE",
        "rule": "No report may say PASS unless every named assertion is mechanically replayed from available path-and-hash-bound evidence and every required semantic review has a final receipt.",
    }


def audit_canonical(root: Path, fixed: dict[str, FixedArtifact] | None = None) -> dict[str, Any]:
    fixed = FIXED_ARTIFACTS if fixed is None else fixed
    fixed_bindings = validate_fixed(root, fixed)
    reports, upstream_replay = validate_reports(root, fixed)
    runtime_rows, prompt_by_id = validate_runtime(root / fixed["label_free_runtime"].path)
    source_rows, source_bytes = validate_sources(root, root / fixed["source_manifest"].path)
    dependency = validate_dependency_and_exposure(root / fixed["dependency_ledger"].path, root / fixed["exposure_ledger"].path, prompt_by_id)
    missing = [item for item in upstream_replay if not item["exists"]]
    drifted = [item for item in upstream_replay if item["exists"] and not item["hash_matches"]]
    require(not drifted, "A present Phase-3 upstream evidence artifact has hash drift")

    common_mechanical = [
        "All fixed authorities match exact SHA-256 bindings.",
        f"Label-free runtime has {len(runtime_rows)} unique prompt IDs and unique exact prompt hashes.",
        f"Source manifest has {len(source_rows)} unique source hashes and paths; {source_bytes} bytes replay exactly.",
        f"Dependency and exposure ledgers each cover {len(prompt_by_id)} prompts and agree on prompt/hash/group identity.",
    ]
    gate_rows = [
        {
            "gate": "split",
            "status": "BLOCKED_FINAL_SPLIT_LEAKAGE_DISPOSITION_NOT_REPLAYABLE",
            "semantic_judgment_required": True,
            "mechanically_established": common_mechanical + [f"There are {dependency['mixed_lane_dependency_groups']} dependency components spanning parent and NC reporting lanes; their IDs are enumerated in mechanical findings."],
            "blockers": ["No final scope-specific split-leakage adjudication receipt is present.", "Mixed-lane dependency components must be explicitly dispositioned and kept intact in any inferential split/resampling plan."],
        },
        {
            "gate": "cue",
            "status": "BLOCKED_FINAL_CUE_REVIEW_NOT_REPLAYABLE",
            "semantic_judgment_required": True,
            "mechanically_established": common_mechanical,
            "blockers": ["The Phase-3 aggregate closure binds cue-review and remediation artifacts, but those bound artifacts are absent from this clean worktree.", "Exact text hashes cannot establish whether a framework/artifact phrase is necessary or an avoidable target/source-unique cue."],
        },
        {
            "gate": "duplication",
            "status": "BLOCKED_ALIAS_FORK_TRANSFORMED_COPY_REVIEW_NOT_REPLAYABLE",
            "semantic_judgment_required": True,
            "mechanically_established": common_mechanical + ["Exact source-hash, source-path, prompt-ID and prompt-text duplicates are zero."],
            "blockers": ["Exact-hash uniqueness does not rule out aliases, forks or transformed copies.", "The Phase-3 cross-cluster/source-relation evidence bound by the closure summary is absent from this clean worktree."],
        },
        {
            "gate": "semantic_near_copy",
            "status": "BLOCKED_FINAL_SEMANTIC_NEAR_COPY_REVIEW_NOT_REPLAYABLE",
            "semantic_judgment_required": True,
            "mechanically_established": common_mechanical,
            "blockers": ["The analysis-freeze D_q ledger is explicitly a reviewed diagnostic subset, not a complete semantic-neighbour graph or final near-copy audit.", "No final 1,077-prompt/3,798-source semantic-near-copy disposition receipt is present."],
        },
        {
            "gate": "coverage",
            "status": "MECHANICAL_CORE_COVERAGE_PASS_FORMAL_QUALITY_PASS_BLOCKED",
            "semantic_judgment_required": False,
            "mechanically_established": common_mechanical + ["The final-freeze and first-matrix aggregate reports bind the 1,077-prompt/3,798-source scope and exclusions."],
            "blockers": ["Coverage cannot become a Phase-8 PASS while the cue, split, duplication and semantic-near-copy dispositions are unresolved or unreplayable.", "The final quality package must bind declared limitations and all prerequisite receipts, not only aggregate counts."],
        },
    ]
    require({row["gate"] for row in gate_rows} == set(QUALITY_ASSERTIONS), "Quality gate roster drift")
    return {
        "schema_version": DOCKET_SCHEMA,
        "status": BLOCKED_STATUS,
        "formal_execution_ready": False,
        "quality_pass_reports_emitted": 0,
        "labels_or_results_content_read": False,
        "selector_provider_metric_runs": 0,
        "scope": {"prompts": EXPECTED_PROMPTS, "sources": EXPECTED_SOURCES, "source_union_sha256": SOURCE_UNION_SHA256, "prompt_manifest_sha256": PROMPT_MANIFEST_SHA256},
        "fixed_artifacts": fixed_bindings,
        "mechanical_findings": {
            "exact_source_hash_duplicates": 0,
            "exact_source_path_duplicates": 0,
            "exact_prompt_id_duplicates": 0,
            "exact_prompt_text_hash_duplicates": 0,
            "source_bytes_replayed": source_bytes,
            **dependency,
            "phase3_bound_inputs": len(upstream_replay),
            "phase3_bound_inputs_present_and_hash_matching": sum(item["hash_matches"] for item in upstream_replay),
            "phase3_bound_inputs_missing": len(missing),
        },
        "missing_phase3_evidence": missing,
        "gates": gate_rows,
        "quality_report_contract": quality_report_contract(),
        "boundary": "This docket is not a PASS quality report and cannot satisfy the Phase-8 root builder.",
    }


def review_requirements(docket: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "schema_version": REQUIREMENT_SCHEMA,
            "gate": row["gate"],
            "current_status": row["status"],
            "semantic_judgment_required": row["semantic_judgment_required"],
            "required_assertions_for_future_pass": QUALITY_ASSERTIONS[row["gate"]],
            "blockers": row["blockers"],
            "permitted_inputs": "Frozen canonical source/prompt evidence and pre-outcome review lineage only; no selector outcomes, targets or metrics may influence disposition.",
            "required_output": "Versioned final path-and-SHA-bound receipt with zero unresolved findings; preserve original evidence and disagreements.",
        }
        for row in docket["gates"]
    ]


def render_readme() -> str:
    return f"""# V7 Phase-8 quality-gate blocking docket v1

Status: `{BLOCKED_STATUS}`.

This package replays only label-free/mechanical facts. It hashes the final
prompt manifest as opaque provenance and does not parse target, gold,
acceptable-set or result content. It ran no retrieval, provider, model, metric
or experiment.

The replay establishes exact 1,077-prompt and 3,798-source coverage, exact
source bytes, unique exact prompt/source identities, 355 dependency groups and
complete exposure-ledger binding. It cannot promote the five Phase-8 quality
gates to PASS: four gates require final semantic disposition evidence, and the
Phase-3 closure's bound cue/relation/preflight evidence is not present in this
clean worktree. Six dependency components span parent and NC reporting lanes
and require explicit final split treatment.

`blocking_docket.json` records the findings and missing path/hash bindings.
`quality_review_requirements.jsonl` defines the five bounded next receipts.
`quality_report_contract.json` is the strengthened schema contract enforced by
the Phase-8 root builder. No `rq2b-v7-phase8-quality-gate-v2` PASS report is
created here.

Replay without writing:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_gate_docket.py --audit
```

Verify this immutable package:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_gate_docket.py \
  --verify --output-dir skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_quality_gate_blocking_docket_2026_09_09_v1
```
"""


def expected_files(root: Path, *, builder_path: Path | None = None) -> dict[str, bytes]:
    docket = audit_canonical(root)
    implementation = (builder_path or Path(__file__)).resolve()
    try:
        implementation.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Builder implementation must be inside repository root") from error
    files = {
        "blocking_docket.json": canonical_bytes(docket),
        "quality_review_requirements.jsonl": rows_bytes(review_requirements(docket)),
        "quality_report_contract.json": canonical_bytes(quality_report_contract()),
        "README.md": render_readme().encode("utf-8"),
    }
    integrity = {
        "schema_version": INTEGRITY_SCHEMA,
        "status": BLOCKED_STATUS,
        "formal_execution_ready": False,
        "quality_pass_reports_emitted": 0,
        "builder": {"path": relative(implementation, root), "sha256": file_sha256(implementation), "version": QUALITY_BUILDER_VERSION},
        "artifacts": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for name, data in sorted(files.items())},
        "external_activity": {"network_calls": 0, "selector_runs": 0, "provider_calls": 0, "model_forwards": 0, "metric_runs": 0},
    }
    files["integrity_report.json"] = canonical_bytes(integrity)
    return files


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def materialize(root: Path, output_dir: Path, *, builder_path: Path | None = None) -> dict[str, Any]:
    require(not output_dir.exists(), f"Refusing to overwrite output: {output_dir}")
    files = expected_files(root, builder_path=builder_path)
    staging = output_dir.parent / f".{output_dir.name}.staging-{os.getpid()}"
    require(not staging.exists(), f"Stale staging directory: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    try:
        for name, data in files.items():
            write_new(staging / name, data)
        staging.rename(output_dir)
    except Exception:
        raise
    return {"status": BLOCKED_STATUS, "output": relative(output_dir, root), "files": len(files), "quality_pass_reports_emitted": 0, "formal_execution_ready": False}


def verify(root: Path, output_dir: Path, *, builder_path: Path | None = None) -> dict[str, Any]:
    require(output_dir.is_dir(), "Docket package is missing")
    expected = expected_files(root, builder_path=builder_path)
    require({path.name for path in output_dir.iterdir()} == set(expected), "Docket package file-set drift")
    for name, data in expected.items():
        require((output_dir / name).read_bytes() == data, f"Docket package drift: {name}")
    return {"status": "PASS_BLOCKING_DOCKET_EXACT_REPLAY_STILL_NOT_A_QUALITY_PASS", "output": relative(output_dir, root), "quality_pass_reports_emitted": 0, "formal_execution_ready": False}


def self_test() -> dict[str, Any]:
    contract = quality_report_contract()
    require(set(contract["required_gates"]) == set(QUALITY_ASSERTIONS), "Contract gate roster drift")
    require(SEMANTIC_GATES < set(QUALITY_ASSERTIONS), "Coverage must remain a separate mechanical gate")
    require("PASS" not in BLOCKED_STATUS, "Blocked status must not masquerade as PASS")
    return {"status": "PASS_QUALITY_DOCKET_SYNTHETIC_SELF_TEST_NO_SCIENTIFIC_PASS", "quality_pass_reports_emitted": 0, "formal_execution_ready": False, "network_calls": 0, "selector_runs": 0, "metric_runs": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--audit", action="store_true")
    mode.add_argument("--materialize", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.self_test:
        result = self_test()
    elif args.audit:
        result = audit_canonical(root)
    else:
        require(args.output_dir is not None, "--output-dir is required")
        output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        output = output.resolve()
        try:
            output.relative_to(root)
        except ValueError as error:
            raise ValueError("Output directory must be inside repository root") from error
        result = materialize(root, output) if args.materialize else verify(root, output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
