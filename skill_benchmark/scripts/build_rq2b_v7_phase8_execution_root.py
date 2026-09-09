#!/usr/bin/env python3
"""Build the V7 Phase-8 execution root without running a selector.

The builder has two kinds of intake.  Approved, already frozen authorities are
fixed below by repository path and SHA-256.  Artifacts that do not yet exist
(final V4.1.5 I3, fresh QA v6, the Phase-8 quality reports, and runnable scripts)
must be supplied in one explicit hash-bound bindings file.  Label and review
provenance files are opaque: this program streams them only to compute SHA-256.

A successful root says READY_FOR_FORMAL_EXPERIMENT, not AUTHORISED.  Every
generated per-run record remains a deliberately non-executable PENDING
template until the user separately issues a one-use authorisation.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT_SCHEMA = "rq2b-v7-phase8-final-execution-root-v1"
BINDINGS_SCHEMA = "rq2b-v7-phase8-root-build-bindings-v1"
RECEIPT_SCHEMA = "rq2b-v7-phase8-readiness-receipt-v1"
TEMPLATE_SCHEMA = "rq2b-v7-phase8-one-use-authorisation-template-v1"
QUALITY_SCHEMA = "rq2b-v7-phase8-quality-gate-v2"
READY_STATUS = "READY_FOR_FORMAL_EXPERIMENT"
PENDING_STATE = "PENDING_EXPLICIT_USER_ONE_USE_AUTHORISATION"

EXPECTED_SOURCES = 3798
EXPECTED_QUERIES = 1077
EXPECTED_SELECTION_BATCHES = 95
EXPECTED_QA_ROWS = 120
SOURCE_UNION_SHA256 = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"
PROMPT_MANIFEST_SHA256 = "3fbc73f87c264c069e54d9001f24a5687075fdbcfd91ec969e24bceec83ee128"

REQUIRED_DYNAMIC_ARTIFACTS = {
    "i3_selection_report",
    "i3_selection_ledger",
    "i3_warning_build_report",
    "i3_warning_final_report",
    "i3_warning_disposition_ledger",
    "i3_preclass_merge_manifest",
    "i3_failed_qa_v4_report",
    "i3_intermediate_merge_v4_1_4_manifest",
    "i3_intermediate_canonical_v4_1_4",
    "i3_failed_qa_v5_packet_manifest",
    "i3_failed_qa_v5_report",
    "i3_merge_manifest",
    "i3_class_repair_ledger",
    "i3_canonical_extractions",
    "i3c_fielded",
    "i3_flat",
    "i3_qa_packet_manifest",
    "i3_qa_final_report",
    "i3_qa_finalizer",
    "window_method_amendment",
    "window_method_approval",
}
CANONICAL_DYNAMIC_PATHS = {
    "i3_selection_report": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_3_warning_repair_integration_2026_09_09_v3/integrity_report.json",
    "i3_selection_ledger": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_3_warning_repair_integration_2026_09_09_v3/selection_v3_ledger.jsonl",
    "i3_warning_build_report": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_3_warning_audit_2026_09_09_v4/integrity_report.json",
    "i3_warning_final_report": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_3_warning_audit_final_2026_09_09_v4/integrity_report.json",
    "i3_warning_disposition_ledger": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_v4_1_3_warning_audit_final_2026_09_09_v4/warning_disposition_ledger.jsonl",
    "i3_preclass_merge_manifest": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_merged_2026_09_09_v4_1_3/manifest.json",
    "i3_failed_qa_v4_report": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v4/qa_final_report.json",
    "i3_intermediate_merge_v4_1_4_manifest": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_4/manifest.json",
    "i3_intermediate_canonical_v4_1_4": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_4/canonical_extractions.jsonl",
    "i3_failed_qa_v5_packet_manifest": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v5/manifest.json",
    "i3_failed_qa_v5_report": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v5/qa_final_report.json",
    "i3_merge_manifest": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_5/manifest.json",
    "i3_class_repair_ledger": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_5/class_repair_ledger.jsonl",
    "i3_canonical_extractions": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_5/canonical_extractions.jsonl",
    "i3c_fielded": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_5/i3c_fielded.jsonl",
    "i3_flat": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_class_repair_2026_09_09_v4_1_5/i3_flat.jsonl",
    "i3_qa_packet_manifest": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_2026_09_09_v6/manifest.json",
    "i3_qa_final_report": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i3_blinded_qa_final_2026_09_09_v6/qa_final_report.json",
    "i3_qa_finalizer": "skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa_v6.py",
    "window_method_amendment": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_skillrouter_embedding_window_amendment_2026_09_09_v1/method_amendment.json",
    "window_method_approval": "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_skillrouter_embedding_window_approval_2026_09_09_v1/method_approval.json",
}
REQUIRED_QUALITY_REPORTS = {
    "split",
    "cue",
    "duplication",
    "semantic_near_copy",
    "coverage",
}
CANONICAL_QUALITY_REPORT_PATHS = {
    role: (
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        f"v7_phase8_quality_closure_2026_09_09_v1/{role}_quality_report.json"
    )
    for role in REQUIRED_QUALITY_REPORTS
}
QUALITY_SEMANTIC_GATES = {"split", "cue", "duplication", "semantic_near_copy"}
QUALITY_ASSERTIONS = {
    "split": {"prompt_scope_identity_replayed", "dependency_and_exposure_coverage_complete", "dependency_components_respected", "cross_lane_components_dispositioned", "no_unresolved_split_leakage"},
    "cue": {"final_prompt_scope_reviewed", "target_title_repository_provider_path_and_literal_source_cues_checked", "unavoidable_cues_stratified", "remediations_and_exclusions_replayed", "no_unresolved_cue_findings"},
    "duplication": {"source_sha_unique", "prompt_sha_unique", "aliases_forks_and_transformed_copies_reviewed", "dependency_edges_or_exclusions_bound", "no_unresolved_duplication"},
    "semantic_near_copy": {"final_prompt_scope_reviewed", "final_source_scope_reviewed", "semantic_near_copy_relations_adjudicated", "dependency_edges_or_exclusions_bound", "no_unresolved_semantic_near_copy"},
    "coverage": {"source_manifest_3798_replayed", "prompt_scope_1077_replayed", "dependency_exposure_1077_replayed", "source_bytes_replayed", "final_freeze_scope_and_exclusions_bound"},
}
REQUIRED_RUNNERS = {
    "bm25_b1",
    "qwen_embedding_b1",
    "skillrouter_embedding_b1",
    "qwen_reranker_b2",
    "skillrouter_reranker_b2",
}
EXPECTED_RUNNER_SPECS = {
    "bm25_b1": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1_v2.py",
        "runner_version": "rq2b-v7-first-matrix-bm25-b1-runner-v2",
        "payload_schema": "rq2b-v7-bm25-b1-phase8-payload-v2",
        "authorisation_schema": "rq2b-v7-bm25-b1-root-release-v2",
    },
    "qwen_embedding_b1": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_qwen_b1_phase8_v3.py",
        "runner_version": "rq2b-v7-qwen-b1-phase8-runner-v3",
        "payload_schema": "rq2b-v7-qwen-b1-phase8-payload-v3",
        "authorisation_schema": "rq2b-v7-qwen-b1-phase8-root-release-v3",
    },
    "skillrouter_embedding_b1": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_skillrouter_embedding_b1.py",
        "runner_version": "rq2b-v7-skillrouter-embedding-b1-runner-v1",
        "payload_schema": "rq2b-v7-skillrouter-embedding-b1-phase8-payload-v1",
        "authorisation_schema": "rq2b-v7-skillrouter-embedding-b1-root-release-v1",
    },
    "qwen_reranker_b2": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_qwen_reranker_b2.py",
        "runner_version": "rq2b-v7-qwen-reranker-b2-runner-v1",
        "payload_schema": "rq2b-v7-qwen-reranker-b2-phase8-payload-v1",
        "authorisation_schema": "rq2b-v7-qwen-reranker-b2-root-release-v1",
    },
    "skillrouter_reranker_b2": {
        "path": "skill_benchmark/scripts/run_rq2b_v7_skillrouter_reranker_b2.py",
        "runner_version": "rq2b-v7-skillrouter-reranker-b2-runner-v1",
        "payload_schema": "rq2b-v7-skillrouter-reranker-b2-phase8-payload-v1",
        "authorisation_schema": "rq2b-v7-skillrouter-reranker-b2-root-release-v1",
    },
}
EXPECTED_LOCAL_MODELS = {
    "skillrouter_embedding": {
        "repository": "pipizhao/SkillRouter-Embedding-0.6B",
        "revision": "c03c9bcee9fce92ab0262bb6dcf54d174a8ba558",
    },
    "skillrouter_reranker": {
        "repository": "pipizhao/SkillRouter-Reranker-0.6B",
        "revision": "78986e1142d12857cfd85b8005e62902cd42d858",
    },
}
I3_FIELDS = {
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "dependencies_resources",
    "constraints_boundaries",
    "success_criteria",
}


@dataclass(frozen=True)
class FixedArtifact:
    path: str
    sha256: str
    opaque: bool = False


FIXED_ARTIFACTS: dict[str, FixedArtifact] = {
    "approved_plan": FixedArtifact(
        "thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md",
        "b54d3d8c6816b2bb5f75b2b946448063fcc800c1f9927e27babd767e3468d4d8",
    ),
    "master_sop": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/review/"
        "RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md",
        "68f7a8e4e802317208d72155b6b3490d0f3587324aaebb67cfac0341241b8835",
    ),
    "approved_plan_freeze": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "rq2_approved_research_plan_2026_09_08_v1/plan_freeze.json",
        "c91b459babec83409b5b17d254cc299a77081afc94fc813173ad3ae7f80eb097",
    ),
    "final_library_freeze_report": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/integrity_report.json",
        "f77df13f55fd151a2831ba448c6efa4bf760942f9e925f837eeb9a365c8eed4a",
    ),
    # The next two files can contain review/label provenance.  They are never
    # parsed, counted, searched, or copied by this builder.
    "final_library_prompt_manifest_review_provenance": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/"
        "final_library_prompt_manifest.jsonl",
        PROMPT_MANIFEST_SHA256,
        opaque=True,
    ),
    "exclusion_ledger_review_provenance": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/"
        "exclusion_and_limitation_ledger.jsonl",
        "a9cd699abf3260130558729df3c323c1d2e6621946b96b11cc62b4a622df0791",
        opaque=True,
    ),
    "scope_amendment": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_v7_acceptable_set_final_library_freeze_2026_09_08_v1/scope_amendment.json",
        "90b3e20120d5a547b6664096ab585fefce254c9ed6ece09b8355be6eff53aa7a",
    ),
    "u0323_exclusion_note": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/manifests/"
        "rq2b_nc_phase5_v7_sealed_coordinator_dispatch_2026_09_08_v2/"
        "U0323_method_gate_note.md",
        "8f162078a1cdd56c95627f9e5c0cafd5784409341e207eed898b146026bfc913",
    ),
    "first_matrix_readiness": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_2026_09_08_v1/readiness_report.json",
        "55f666bc3daa96f3e37f7209761b4a0c06eb7aaf14484db0a4b7d6aea94725e0",
    ),
    "source_manifest": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_2026_09_08_v1/source_manifest.jsonl",
        "92c0746a1236e7005e71a43366ca163ce9d394a55c354f6c6d4c1bfadd2e6225",
    ),
    "core_conditions": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_2026_09_08_v1/first_matrix_conditions.jsonl",
        "b66c0dfd23c5fb96869a548f038cd8afa6fc0f99c253f0fe98a66656510e167f",
    ),
    "bridge_conditions": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_2026_09_08_v1/fixed_candidate_bridge_conditions.jsonl",
        "d659ff98a5a2534478f68ab44794e4df7d89b23eb3a44a2fbf335cdca42366f7",
    ),
    "analysis_freeze_report": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/freeze_report.json",
        "1b27a1a6f7423871c7e9b7206736d60e3838e405af1cf2f5b078f0db58f784f7",
    ),
    "label_free_runtime": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/label_free_query_runtime.jsonl",
        "07029e02454ff35efd8c0018a1aea93ef41fc0135dfc0cf78bac7af4e22ace84",
    ),
    "dependency_ledger": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/dependency_ledger.jsonl",
        "4226cfe2c9943d40026a4f1a9a38dbbc379ae9b8f39bd9b4c40aea8009e97fc7",
    ),
    "exposure_ledger": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/exposure_ledger.jsonl",
        "3749a72735a1c7034fd679fad24d4ce5ff40a8274144b15d8265bfb1c608dce3",
    ),
    "offline_label_adapter_review_provenance": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/offline_label_adapter.jsonl",
        "cb11848e4a6d7938870e8bf5913335050538ac4f3c589ec9fe69bb303711357d",
        opaque=True,
    ),
    "reviewed_neighbour_ledger_review_provenance": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_analysis_freeze_2026_09_08_v1/reviewed_confusable_neighbour_ledger.jsonl",
        "cb65d8dc40041630f201afc303604648fdc7ee5af270cbe877be33ab2a58dfb4",
        opaque=True,
    ),
    "i1_i2_v2_report": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_phase7_i1_i2_2026_09_09_v2/mechanical_report.json",
        "30d532415a675143585c524f8ca9b68cafe8b73f28518913d25d3f227fa89b89",
    ),
    "i1_discovery_v2": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i1-discovery.jsonl",
        "0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd",
    ),
    "i2_original_v2": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase7_i1_i2_runtime_artifacts_2026_09_09_v1/i2-original.jsonl",
        "8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec",
    ),
    "runtime_preflight_integrity": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_runtime_preflight_2026_09_09_v1/integrity_report.json",
        "93e047af9e92ead168b53a1b47b17ff5839b36ee3f900d47e5254e2694214279",
    ),
    "runtime_inventory": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_first_matrix_runtime_preflight_2026_09_09_v1/runtime_inventory.json",
        "3bc874eaa23ed699c71ee7007039374868cb65ab69ce05823b67ea3a5b955b54",
    ),
    # This is lineage/preflight evidence only.  Its old representation payload
    # is deliberately not accepted as a Phase-8 runnable payload.
    "qwen_b1_preflight_integrity_v2_lineage": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_qwen_b1_preflight_2026_09_09_v2/integrity_report.json",
        "469ac723c68bf04349507733be897bdf1d8c453d972466cb871792bd746e421c",
    ),
    "qwen_b1_preflight_report_v2_lineage": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_qwen_b1_preflight_2026_09_09_v2/preflight_report.json",
        "15bcae21fccda48f155d83471bb91409ce8437688a3e2cd04509280a1d3aa546",
    ),
    "analysis_contract": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_runner_output_analysis_contract_2026_09_09_v1/analysis_contract.json",
        "719f7a007b046c754ceeb8579bc637298b92ab810d6e3f9a1059e97614e6d14c",
    ),
    "b1_output_schema": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_runner_output_analysis_contract_2026_09_09_v1/b1_runner_output_schema.json",
        "e9af1eb941ef95d9ce65f7edec7f88320cd9b2d879b66163250d767f39af906b",
    ),
    "b2_output_schema": FixedArtifact(
        "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
        "v7_runner_output_analysis_contract_2026_09_09_v1/b2_runner_output_schema.json",
        "fd92fa4b8ba3b0366c9a1debf647efd704a98466dc30fd85a4e1c030cd1753a9",
    ),
    "official_output_validator": FixedArtifact(
        "skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py",
        "d1b85f962af670f1bdd0631e71c08008db5ab65b48a0c66ffffcc1d5241035d7",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact_keys(value: Any, expected: set[str], field: str) -> None:
    require(isinstance(value, dict), f"{field}: expected object")
    require(set(value) == expected, f"{field}: key drift: {sorted(set(value) ^ expected)}")


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            require(bool(raw.strip()), f"Blank JSONL row: {path}:{line_number}")
            value = json.loads(raw)
            require(isinstance(value, dict), f"Expected JSON object: {path}:{line_number}")
            values.append(value)
    return values


def root_path(root: Path, value: str, *, field: str) -> Path:
    require(isinstance(value, str) and value, f"{field}: empty path")
    supplied = Path(value)
    path = supplied.resolve() if supplied.is_absolute() else (root / supplied).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{field}: path escapes repository root") from error
    return path


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def artifact_binding(path: Path, root: Path, *, opaque: bool = False) -> dict[str, Any]:
    return {
        "path": relative(path, root),
        "sha256": file_sha256(path),
        "bytes": path.stat().st_size,
        "content_access": "HASH_ONLY_OPAQUE_REVIEW_PROVENANCE" if opaque else "STRUCTURAL_VALIDATION_ONLY",
    }


def validate_fixed_artifacts(
    root: Path, fixed: dict[str, FixedArtifact] = FIXED_ARTIFACTS
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role, spec in fixed.items():
        path = root_path(root, spec.path, field=f"fixed.{role}")
        require(path.is_file(), f"Missing fixed authority: {spec.path}")
        actual = file_sha256(path)
        require(actual == spec.sha256, f"Fixed authority hash drift: {spec.path}: {actual} != {spec.sha256}")
        result[role] = artifact_binding(path, root, opaque=spec.opaque)
    return result


def validate_bound_file(root: Path, value: Any, *, field: str) -> Path:
    require(isinstance(value, dict) and set(value) == {"path", "sha256"}, f"{field}: expected path+sha256")
    require(is_sha256(value["sha256"]), f"{field}: invalid SHA-256")
    path = root_path(root, value["path"], field=f"{field}.path")
    require(path.is_file(), f"{field}: missing file")
    actual = file_sha256(path)
    require(actual == value["sha256"], f"{field}: hash drift: {actual} != {value['sha256']}")
    return path


def expect_report(path: Path, *, schema: str, state_key: str, state: str, field: str) -> dict[str, Any]:
    report = read_json(path)
    require(report.get("schema_version") == schema, f"{field}: schema drift")
    require(report.get(state_key) == state, f"{field}: required {state_key}={state}")
    return report


def validate_authority_reports(root: Path) -> tuple[set[str], dict[str, Any]]:
    final_freeze = read_json(root / FIXED_ARTIFACTS["final_library_freeze_report"].path)
    require(final_freeze.get("status") == "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION", "Final library freeze is not PASS")
    require(final_freeze.get("counts", {}).get("frozen_final_library_groups") == EXPECTED_QUERIES, "Final library query count drift")
    require(final_freeze.get("integrity_assertions", {}).get("u0323_remains_excluded_without_target_join") == "PASS", "U0323 exclusion gate is not PASS")
    require(final_freeze.get("output_hashes", {}).get("final_library_prompt_manifest.jsonl") == PROMPT_MANIFEST_SHA256, "Prompt freeze binding drift")

    first_matrix = read_json(root / FIXED_ARTIFACTS["first_matrix_readiness"].path)
    require(first_matrix.get("status") == "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED", "First-matrix preparation is not PASS")
    require(first_matrix.get("counts", {}).get("sources") == EXPECTED_SOURCES, "First-matrix source count drift")
    require(first_matrix.get("counts", {}).get("prompts") == EXPECTED_QUERIES, "First-matrix prompt count drift")

    source_rows = read_jsonl(root / FIXED_ARTIFACTS["source_manifest"].path)
    source_ids = {row.get("sha256") for row in source_rows}
    require(len(source_rows) == len(source_ids) == EXPECTED_SOURCES, "Source manifest coverage drift")
    require(all(is_sha256(value) for value in source_ids), "Invalid source identity")

    analysis = read_json(root / FIXED_ARTIFACTS["analysis_freeze_report"].path)
    require(analysis.get("status") == "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE", "Analysis freeze is not PASS")
    require(analysis.get("counts", {}).get("prompts") == EXPECTED_QUERIES, "Analysis prompt count drift")
    require(analysis.get("provider_calls") == 0 and analysis.get("retrieval_or_reranking_runs") == 0, "Analysis freeze observed execution")

    i1_i2 = read_json(root / FIXED_ARTIFACTS["i1_i2_v2_report"].path)
    require(i1_i2.get("status") == "PASS_I1_IDENTITY_OVERLAY_AND_I2_BYTE_PRESERVATION_PENDING_I3_V4_AND_FRESH_QA", "Authoritative I1/I2 v2 report drift")
    require(i1_i2.get("counts", {}).get("i1_rows") == EXPECTED_SOURCES, "I1 v2 row count drift")
    require(i1_i2.get("counts", {}).get("i2_exact_byte_rows") == EXPECTED_SOURCES, "I2 v2 row count drift")

    runtime = read_json(root / FIXED_ARTIFACTS["runtime_preflight_integrity"].path)
    require(runtime.get("status") == "PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY", "Runtime preflight is not PASS")
    require(runtime.get("checks", {}).get("zero_model_forward") is True, "Runtime preflight model-forward boundary drift")
    require(runtime.get("checks", {}).get("zero_network") is True, "Runtime preflight network boundary drift")
    inventory = read_json(root / FIXED_ARTIFACTS["runtime_inventory"].path)
    require(inventory.get("schema_version") == "rq2b-v7-b36-c6-runtime-preflight-v1", "Runtime inventory schema drift")
    require(inventory.get("status") == "PASS_ZERO_INFERENCE_RUNTIME_INVENTORY_EXECUTION_NOT_AUTHORISED", "Runtime inventory state drift")
    local_models = inventory.get("local_models")
    require(isinstance(local_models, dict), "Runtime inventory local-model section missing")
    for role, expected in EXPECTED_LOCAL_MODELS.items():
        snapshot = local_models.get(role)
        require(isinstance(snapshot, dict), f"Runtime inventory missing local model: {role}")
        require(snapshot.get("repository") == expected["repository"] and snapshot.get("revision") == expected["revision"], f"Runtime inventory local-model identity drift: {role}")
        snapshot_path = root_path(root, snapshot.get("snapshot_path"), field=f"runtime_inventory.local_models.{role}.snapshot_path")
        require(relative(snapshot_path, root).startswith("skill_benchmark/cache/huggingface/"), f"Runtime inventory local-model path drift: {role}")
        require(snapshot_path.is_dir(), f"Pinned local-model snapshot missing: {role}")
        files = snapshot.get("files")
        require(isinstance(files, dict) and files, f"Runtime inventory local-model files missing: {role}")
        for name, expected_sha in files.items():
            require(isinstance(name, str) and is_sha256(expected_sha), f"Runtime inventory invalid local-model file binding: {role}/{name}")
            file_path = snapshot_path / name
            require(file_path.is_file() and file_sha256(file_path) == expected_sha, f"Pinned local-model file drift: {role}/{name}")
    dashscope = inventory.get("dashscope_contracts")
    require(isinstance(dashscope, dict), "Runtime inventory DashScope contract missing")
    require(dashscope.get("embedding", {}).get("endpoint") == "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings" and dashscope.get("embedding", {}).get("model") == "text-embedding-v4", "DashScope embedding contract drift")
    require(dashscope.get("reranker", {}).get("endpoint") == "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank" and dashscope.get("reranker", {}).get("model") == "qwen3-rerank", "DashScope reranker contract drift")
    return {str(value) for value in source_ids}, {
        "final_library": final_freeze,
        "first_matrix": first_matrix,
        "analysis": analysis,
        "i1_i2": i1_i2,
        "runtime_inventory": inventory,
    }


def validate_representation(path: Path, *, representation: str, source_ids: set[str]) -> None:
    rows = read_jsonl(path)
    require(len(rows) == EXPECTED_SOURCES, f"{representation}: expected {EXPECTED_SOURCES} rows")
    actual: set[str] = set()
    for row in rows:
        source_sha = row.get("source_sha256")
        require(row.get("representation") == representation, f"{representation}: representation drift")
        require(source_sha in source_ids and source_sha not in actual, f"{representation}: source identity drift")
        selector_text = row.get("selector_text")
        require(isinstance(selector_text, str), f"{representation}: selector_text missing")
        require(row.get("selector_text_sha256") == hashlib.sha256(selector_text.encode()).hexdigest(), f"{representation}: selector text hash drift")
        actual.add(source_sha)
    require(actual == source_ids, f"{representation}: source coverage mismatch")


def validate_dynamic_artifacts(
    root: Path, bindings: dict[str, Any], source_ids: set[str]
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    artifacts = bindings.get("dynamic_artifacts")
    require(isinstance(artifacts, dict) and set(artifacts) == REQUIRED_DYNAMIC_ARTIFACTS, "Dynamic artifact roles are incomplete or unexpected")
    for role, value in artifacts.items():
        require(isinstance(value, dict), f"dynamic_artifacts.{role}: expected object")
        require(value.get("path") == CANONICAL_DYNAMIC_PATHS[role], f"Dynamic artifact canonical path drift: {role}")
    paths = {role: validate_bound_file(root, value, field=f"dynamic_artifacts.{role}") for role, value in artifacts.items()}

    selection = expect_report(paths["i3_selection_report"], schema="rq2b-v7-i3-v4.1.3-warning-repair-integration-report-v1", state_key="state", state="PASS_95_BATCHES_V4_1_3_REPAIR_INTEGRATED_PENDING_FRESH_WARNING_AUDIT", field="i3_selection_report")
    require(selection.get("counts", {}).get("batches") == EXPECTED_SELECTION_BATCHES, "I3 selection batch count drift")
    require(selection.get("counts", {}).get("rows") == EXPECTED_SOURCES, "I3 selection row count drift")
    require(selection.get("output_bindings", {}).get("selection_v3_ledger", {}).get("sha256") == file_sha256(paths["i3_selection_ledger"]), "I3 selection ledger binding drift")
    require(len(read_jsonl(paths["i3_selection_ledger"])) == EXPECTED_SELECTION_BATCHES, "I3 selection ledger coverage drift")

    warning_build = read_json(paths["i3_warning_build_report"])
    require(warning_build.get("schema_version") == "rq2b-v7-i3-v4.1-warning-audit-build-report-v1", "Warning-build schema drift")
    require(warning_build.get("state") in {"MATERIALISED_PENDING_SOURCE_ONLY_WARNING_RETURNS", "PASS_NO_WARNINGS_REQUIRING_DISPOSITION"}, "Warning-build state drift")
    require(warning_build.get("counts", {}).get("selected_batches") == EXPECTED_SELECTION_BATCHES, "Warning-build batch count drift")
    require(warning_build.get("counts", {}).get("sources") == EXPECTED_SOURCES, "Warning-build source count drift")
    require(warning_build.get("bindings", {}).get("integration_report_sha256") == file_sha256(paths["i3_selection_report"]), "Warning-build selection-report binding drift")
    require(warning_build.get("bindings", {}).get("selection_ledger_sha256") == file_sha256(paths["i3_selection_ledger"]), "Warning-build selection-ledger binding drift")

    warning_final = expect_report(paths["i3_warning_final_report"], schema="rq2b-v7-i3-v4.1-warning-audit-final-report-v1", state_key="state", state="PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA", field="i3_warning_final_report")
    require(warning_final.get("bindings", {}).get("warning_docket_sha256") == warning_build.get("bindings", {}).get("warning_docket_sha256"), "Warning docket cross-binding drift")
    require(warning_final.get("bindings", {}).get("warning_build_report_sha256") == file_sha256(paths["i3_warning_build_report"]), "Warning-final build-report binding drift")
    require(warning_final.get("bindings", {}).get("final_ledger_sha256") == file_sha256(paths["i3_warning_disposition_ledger"]), "Warning final-ledger binding drift")

    preclass_merge = expect_report(paths["i3_preclass_merge_manifest"], schema="rq2b-v7-phase7-i3-full-corpus-merged-v4.1", state_key="state", state="AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", field="i3_preclass_merge_manifest")
    require(preclass_merge.get("bindings", {}).get("selection_report_sha256") == file_sha256(paths["i3_selection_report"]), "I3 V4.1.3 selection-report binding drift")
    require(preclass_merge.get("bindings", {}).get("selection_ledger_sha256") == file_sha256(paths["i3_selection_ledger"]), "I3 V4.1.3 selection-ledger binding drift")
    require(preclass_merge.get("bindings", {}).get("warning_audit_final_report_sha256") == file_sha256(paths["i3_warning_final_report"]), "I3 V4.1.3 warning-final binding drift")
    require(preclass_merge.get("bindings", {}).get("i1_i2_v2_report_sha256") == file_sha256(root / FIXED_ARTIFACTS["i1_i2_v2_report"].path), "I3 V4.1.3 I1/I2 binding drift")
    failed_qa_v4 = expect_report(paths["i3_failed_qa_v4_report"], schema="rq2b-v7-i3-full-corpus-v4.1-blinded-qa-final-v3", state_key="state", state="FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE", field="i3_failed_qa_v4_report")
    require(failed_qa_v4.get("formal_execution_ready") is False, "Failed I3 QA v4 was treated as execution-ready")
    require(failed_qa_v4.get("counts", {}).get("critical_error_rows") == 0 and failed_qa_v4.get("counts", {}).get("major_error_rows") == 18, "Failed I3 QA v4 disposition/count drift")

    intermediate_merge = expect_report(paths["i3_intermediate_merge_v4_1_4_manifest"], schema="rq2b-v7-phase7-i3-class-repair-v4.1.4", state_key="state", state="AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", field="i3_intermediate_merge_v4_1_4_manifest")
    require(intermediate_merge.get("counts") == {"sources": EXPECTED_SOURCES, "fresh_full_corpus": EXPECTED_SOURCES, "batches": EXPECTED_SELECTION_BATCHES}, "I3 V4.1.4 intermediate coverage drift")
    require(intermediate_merge.get("bindings", {}).get("source_v4_1_3_manifest_sha256") == file_sha256(paths["i3_preclass_merge_manifest"]), "I3 V4.1.4 predecessor binding drift")
    require(intermediate_merge.get("bindings", {}).get("failed_fresh_qa_v4_report_sha256") == file_sha256(paths["i3_failed_qa_v4_report"]), "I3 V4.1.4 failed-QA-v4 binding drift")
    require(intermediate_merge.get("artifacts", {}).get("canonical_extractions.jsonl", {}).get("sha256") == file_sha256(paths["i3_intermediate_canonical_v4_1_4"]), "I3 V4.1.4 canonical hash drift")

    failed_qa_v5_packet = expect_report(paths["i3_failed_qa_v5_packet_manifest"], schema="rq2b-v7-i3-full-corpus-v4.1.4-blinded-qa-v1", state_key="state", state="FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS", field="i3_failed_qa_v5_packet_manifest")
    require(failed_qa_v5_packet.get("sample_size") == EXPECTED_QA_ROWS and failed_qa_v5_packet.get("previous_samples_excluded") == 240, "Failed QA v5 packet scope drift")
    require(failed_qa_v5_packet.get("bindings", {}).get("merged_manifest_sha256") == file_sha256(paths["i3_intermediate_merge_v4_1_4_manifest"]), "Failed QA v5 intermediate-merge binding drift")

    failed_qa_v5 = expect_report(paths["i3_failed_qa_v5_report"], schema="rq2b-v7-i3-full-corpus-v4.1.4-blinded-qa-final-v1", state_key="state", state="FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE", field="i3_failed_qa_v5_report")
    require(failed_qa_v5.get("formal_execution_ready") is False, "Failed I3 QA v5 was treated as execution-ready")
    require(failed_qa_v5.get("counts", {}).get("critical_error_rows") == 0 and failed_qa_v5.get("counts", {}).get("major_error_rows") == 13, "Failed I3 QA v5 disposition/count drift")
    require(failed_qa_v5.get("bindings", {}).get("qa_packet_manifest_sha256") == file_sha256(paths["i3_failed_qa_v5_packet_manifest"]), "Failed QA v5 packet binding drift")
    require(failed_qa_v5.get("bindings", {}).get("failed_qa_v4_report_sha256") == file_sha256(paths["i3_failed_qa_v4_report"]), "Failed QA v5 failed-QA-v4 binding drift")

    merge = expect_report(paths["i3_merge_manifest"], schema="rq2b-v7-phase7-i3-class-repair-v4.1.5", state_key="state", state="AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING", field="i3_merge_manifest")
    require(merge.get("counts") == {"sources": EXPECTED_SOURCES, "fresh_full_corpus": EXPECTED_SOURCES, "batches": EXPECTED_SELECTION_BATCHES}, "I3 merge coverage drift")
    require(merge.get("bindings", {}).get("source_v4_1_4_manifest_sha256") == file_sha256(paths["i3_intermediate_merge_v4_1_4_manifest"]), "I3 class-repair V4.1.4 manifest binding drift")
    require(merge.get("bindings", {}).get("source_v4_1_4_canonical_extractions_sha256") == file_sha256(paths["i3_intermediate_canonical_v4_1_4"]), "I3 class-repair V4.1.4 canonical binding drift")
    require(merge.get("bindings", {}).get("failed_fresh_qa_v5_report_sha256") == file_sha256(paths["i3_failed_qa_v5_report"]), "I3 class-repair failed-QA-v5 binding drift")
    require(merge.get("bindings", {}).get("assignment_manifest_sha256") == preclass_merge.get("bindings", {}).get("assignment_manifest_sha256"), "I3 class-repair assignment lineage drift")
    repair_ledger = read_jsonl(paths["i3_class_repair_ledger"])
    require(len(repair_ledger) == EXPECTED_SOURCES, "I3 class-repair ledger coverage drift")
    require(merge.get("artifacts", {}).get("class_repair_ledger.jsonl", {}).get("sha256") == file_sha256(paths["i3_class_repair_ledger"]), "I3 class-repair ledger hash drift")
    require(merge.get("class_repair", {}).get("rows_processed") == EXPECTED_SOURCES and merge.get("class_repair", {}).get("failed_qa_v5_sources_bound") == 13 and merge.get("class_repair", {}).get("failed_qa_v5_sources_changed") == 13, "I3 class-repair coverage/disposition drift")
    merge_artifacts = merge.get("artifacts", {})
    for role, filename in (("i3_canonical_extractions", "canonical_extractions.jsonl"), ("i3c_fielded", "i3c_fielded.jsonl"), ("i3_flat", "i3_flat.jsonl")):
        item = merge_artifacts.get(filename, {})
        require(item.get("sha256") == file_sha256(paths[role]), f"I3 merge artifact hash drift: {filename}")
        require(item.get("rows") == EXPECTED_SOURCES, f"I3 merge artifact row drift: {filename}")
    validate_representation(paths["i3c_fielded"], representation="I3C-fielded", source_ids=source_ids)
    validate_representation(paths["i3_flat"], representation="I3-flat", source_ids=source_ids)

    qa_packet = expect_report(paths["i3_qa_packet_manifest"], schema="rq2b-v7-i3-full-corpus-v4.1.5-blinded-qa-v1", state_key="state", state="FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS", field="i3_qa_packet_manifest")
    require(qa_packet.get("sample_size") == EXPECTED_QA_ROWS and qa_packet.get("previous_samples_excluded") == 360, "Fresh QA v6 packet scope drift")
    require(qa_packet.get("bindings", {}).get("merged_manifest_sha256") == file_sha256(paths["i3_merge_manifest"]), "Fresh QA v6 merge binding drift")

    qa_final = expect_report(paths["i3_qa_final_report"], schema="rq2b-v7-i3-full-corpus-v4.1.5-blinded-qa-final-v1", state_key="state", state="PASS_CURRENT_I1_I3_SEMANTIC_QA", field="i3_qa_final_report")
    require(qa_final.get("formal_execution_ready") is True, "Fresh QA v6 is not formal-execution ready")
    require(qa_final.get("sample_size") == EXPECTED_QA_ROWS, "Fresh QA v6 final sample-size drift")
    require(qa_final.get("counts", {}).get("critical_error_rows") == 0, "Fresh QA v6 has critical errors")
    require(qa_final.get("counts", {}).get("major_error_rows", EXPECTED_QA_ROWS + 1) <= 6, "Fresh QA v6 has too many major errors")
    require(qa_final.get("major_error_rate", 1.0) <= 0.05, "Fresh QA v6 major-error rate exceeds 5%")
    require(qa_final.get("bindings", {}).get("qa_packet_manifest_sha256") == file_sha256(paths["i3_qa_packet_manifest"]), "Fresh QA v6 packet binding drift")
    require(qa_final.get("bindings", {}).get("failed_qa_v5_report_sha256") == file_sha256(paths["i3_failed_qa_v5_report"]), "Fresh QA v6 failed-QA-v5 binding drift")
    require(relative(paths["i3_qa_finalizer"], root) == "skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa_v6.py", "Fresh QA v6 finalizer path drift")
    require(qa_final.get("bindings", {}).get("finalizer_sha256") == file_sha256(paths["i3_qa_finalizer"]), "Fresh QA v6 finalizer binding drift")
    require(qa_final.get("calibration") == {"1": "PASS_EXACT_8_OF_8", "2": "PASS_EXACT_8_OF_8", "3": "PASS_EXACT_8_OF_8"}, "Fresh QA v6 calibration gate drift")
    require(qa_final.get("pass_rule_replay") == {
        "critical_error_rows": 0,
        "maximum_field_major_error_rate": 0.05,
        "maximum_major_error_rate": 0.05,
        "maximum_major_error_rows": 6,
        "represented_field_minimum_for_threshold": 20,
    }, "Fresh QA v6 pass-rule replay drift")
    field_strata = qa_final.get("field_strata")
    require(isinstance(field_strata, dict) and set(field_strata) == I3_FIELDS, "Fresh QA v6 field-strata roster drift")
    for field, row in field_strata.items():
        require(set(row) == {"represented_or_missing_error_rows", "major_error_rows", "major_error_rate", "threshold_applies"}, f"Fresh QA v6 field-strata fields drift: {field}")
        require(isinstance(row["represented_or_missing_error_rows"], int) and row["represented_or_missing_error_rows"] >= 0, f"Fresh QA v6 field denominator drift: {field}")
        require(isinstance(row["major_error_rows"], int) and 0 <= row["major_error_rows"] <= row["represented_or_missing_error_rows"], f"Fresh QA v6 field numerator drift: {field}")
        require(row["threshold_applies"] is (row["represented_or_missing_error_rows"] >= 20), f"Fresh QA v6 field threshold flag drift: {field}")
        if row["threshold_applies"]:
            require(isinstance(row["major_error_rate"], (int, float)) and row["major_error_rate"] <= 0.05, f"Fresh QA v6 field major-error rate exceeds 5%: {field}")
    expected_returns = {
        **{f"reviewer_returns/calibration_group_{group}.jsonl": 8 for group in (1, 2, 3)},
        **{f"reviewer_returns/qa_slot_{slot:02d}_return.jsonl": 20 for slot in range(1, 7)},
    }
    return_artifacts = qa_final.get("reviewer_return_artifacts")
    require(isinstance(return_artifacts, dict) and set(return_artifacts) == set(expected_returns), "Fresh QA v6 reviewer-return roster drift")
    final_root = paths["i3_qa_final_report"].parent
    for name, expected_rows in expected_returns.items():
        item = return_artifacts[name]
        require(set(item) == {"sha256", "rows"} and item["rows"] == expected_rows and is_sha256(item["sha256"]), f"Fresh QA v6 reviewer-return binding drift: {name}")
        return_path = final_root / name
        require(return_path.is_file() and file_sha256(return_path) == item["sha256"] and len(return_path.read_bytes().splitlines()) == expected_rows, f"Fresh QA v6 reviewer-return artifact drift: {name}")
    error_ids = qa_final.get("error_review_ids")
    require(isinstance(error_ids, list) and len(error_ids) == len(set(error_ids)) == qa_final["counts"]["critical_error_rows"] + qa_final["counts"]["major_error_rows"], "Fresh QA v6 error identity/count drift")

    amendment = read_json(paths["window_method_amendment"])
    require(amendment.get("schema_version") == "rq2b-v7-skillrouter-embedding-window-method-amendment-v1", "Window amendment schema drift")
    proposal = amendment.get("proposal", {})
    require(proposal.get("window_tokens") == 7500 and proposal.get("overlap_tokens") == 256, "Window amendment parameter drift")
    require(proposal.get("aggregation") == "maximum query-to-window cosine per source", "Window amendment aggregation drift")
    approval = read_json(paths["window_method_approval"])
    require(approval.get("schema_version") == "rq2b-v7-skillrouter-window-approval-v1", "Window approval schema drift")
    require(approval.get("status") == "APPROVED_FOR_PHASE8_ROOT_BINDING_NOT_EXECUTION", "Window amendment is not explicitly approved")
    require(approval.get("execution_authorised") is False, "Window approval must not authorise execution")
    require(approval.get("method_amendment_sha256") == file_sha256(paths["window_method_amendment"]), "Window approval method hash drift")
    require(root_path(root, approval.get("method_amendment"), field="window approval method_amendment") == paths["window_method_amendment"], "Window approval method path drift")
    require(root_path(root, approval.get("approved_research_plan"), field="window approval approved_research_plan") == (root / FIXED_ARTIFACTS["approved_plan"].path).resolve(), "Window approval plan path drift")
    require(approval.get("approved_research_plan_sha256") == FIXED_ARTIFACTS["approved_plan"].sha256, "Window approval plan hash drift")
    require(root_path(root, approval.get("plan_freeze"), field="window approval plan_freeze") == (root / FIXED_ARTIFACTS["approved_plan_freeze"].path).resolve(), "Window approval plan-freeze path drift")
    require(approval.get("plan_freeze_sha256") == FIXED_ARTIFACTS["approved_plan_freeze"].sha256, "Window approval plan-freeze hash drift")
    require(approval.get("approved_method") == {
        "window_tokens": 7500,
        "window_token_basis": "content_tokens_add_special_tokens_false",
        "overlap_tokens": 256,
        "overlap_token_basis": "content_tokens_add_special_tokens_false",
        "coverage": "exact_lossless_character_coverage",
        "aggregation": "maximum_query_to_window_cosine",
    }, "Window approval method contract drift")

    bound = {role: artifact_binding(path, root) for role, path in paths.items()}
    return bound, {
        "selection": selection,
        "warning_final": warning_final,
        "preclass_merge": preclass_merge,
        "failed_qa_v4": failed_qa_v4,
        "intermediate_merge_v4_1_4": intermediate_merge,
        "failed_qa_v5": failed_qa_v5,
        "merge": merge,
        "qa_final": qa_final,
        "window_amendment": amendment,
    }


def validate_quality_reports(root: Path, bindings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    reports = bindings.get("quality_reports")
    require(isinstance(reports, dict) and set(reports) == REQUIRED_QUALITY_REPORTS, "Quality report roles are incomplete or unexpected")
    result: dict[str, dict[str, Any]] = {}
    for role, value in reports.items():
        require(isinstance(value, dict), f"quality_reports.{role}: expected object")
        require(value.get("path") == CANONICAL_QUALITY_REPORT_PATHS[role], f"Quality report canonical path drift: {role}")
        path = validate_bound_file(root, value, field=f"quality_reports.{role}")
        report = read_json(path)
        exact_keys(report, {"schema_version", "gate", "status", "formal_execution_ready", "source_union_sha256", "prompt_manifest_sha256", "counts", "assertions", "evidence", "review_provenance", "quality_builder"}, f"quality report {role}")
        require(report["schema_version"] == QUALITY_SCHEMA, f"Quality report schema drift: {role}")
        require(report["gate"] == role, f"Quality report role drift: {role}")
        require(report["status"] == "PASS" and report["formal_execution_ready"] is True, f"Quality report is not a final PASS: {role}")
        require(report["source_union_sha256"] == SOURCE_UNION_SHA256, f"Quality report source binding drift: {role}")
        require(report["prompt_manifest_sha256"] == PROMPT_MANIFEST_SHA256, f"Quality report prompt binding drift: {role}")
        require(report["counts"] == {"prompts": EXPECTED_QUERIES, "sources": EXPECTED_SOURCES, "unresolved_findings": 0}, f"Quality report counts/unresolved drift: {role}")
        assertions = report["assertions"]
        require(isinstance(assertions, dict) and set(assertions) == QUALITY_ASSERTIONS[role], f"Quality report assertion roster drift: {role}")
        require(all(value == "PASS" for value in assertions.values()), f"Quality report has a non-PASS assertion: {role}")

        evidence = report["evidence"]
        require(isinstance(evidence, list) and evidence, f"Quality report lacks bound evidence: {role}")
        evidence_bound: list[dict[str, Any]] = []
        for index, item in enumerate(evidence):
            exact_keys(item, {"path", "sha256", "content_access"}, f"quality report {role}.evidence[{index}]")
            require(item["content_access"] in {"PARSED_MECHANICAL_REPLAY", "HASH_ONLY_OPAQUE_PROVENANCE"}, f"Quality evidence access mode drift: {role}")
            evidence_path = validate_bound_file(root, {"path": item["path"], "sha256": item["sha256"]}, field=f"quality report {role}.evidence[{index}]")
            evidence_bound.append({"path": relative(evidence_path, root), "sha256": item["sha256"], "content_access": item["content_access"]})

        review = report["review_provenance"]
        exact_keys(review, {"semantic_judgment_required", "final_adjudication_receipt", "content_access"}, f"quality report {role}.review_provenance")
        semantic_required = role in QUALITY_SEMANTIC_GATES
        require(review["semantic_judgment_required"] is semantic_required, f"Quality report semantic-review boundary drift: {role}")
        if semantic_required:
            require(review["content_access"] == "HASH_ONLY_OPAQUE_FINAL_ADJUDICATION_PROVENANCE", f"Quality review provenance access drift: {role}")
            receipt_path = validate_bound_file(root, review["final_adjudication_receipt"], field=f"quality report {role}.final_adjudication_receipt")
            review_bound: dict[str, Any] | None = artifact_binding(receipt_path, root)
        else:
            require(review["final_adjudication_receipt"] is None and review["content_access"] == "NOT_APPLICABLE_MECHANICAL_GATE", f"Mechanical quality gate review provenance drift: {role}")
            review_bound = None

        implementation = report["quality_builder"]
        exact_keys(implementation, {"path", "sha256", "version"}, f"quality report {role}.quality_builder")
        implementation_path = validate_bound_file(root, {"path": implementation["path"], "sha256": implementation["sha256"]}, field=f"quality report {role}.quality_builder")
        require(relative(implementation_path, root).startswith("skill_benchmark/scripts/"), f"Quality builder path drift: {role}")
        tree = ast.parse(implementation_path.read_text(encoding="utf-8"), filename=str(implementation_path))
        versions = [ast.literal_eval(node.value) for node in tree.body if isinstance(node, (ast.Assign, ast.AnnAssign)) for target in (node.targets if isinstance(node, ast.Assign) else [node.target]) if isinstance(target, ast.Name) and target.id == "QUALITY_BUILDER_VERSION" and isinstance(node.value, ast.Constant)]
        require(versions == [implementation["version"]], f"Quality builder version drift: {role}")
        result[role] = {
            **artifact_binding(path, root),
            "assertions": sorted(assertions),
            "evidence": evidence_bound,
            "semantic_adjudication_receipt": review_bound,
            "quality_builder": {"path": relative(implementation_path, root), "sha256": implementation["sha256"], "version": implementation["version"]},
        }
    return result


def literal_constants(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values: dict[str, Any] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value_node = node.value
        for target in targets:
            if isinstance(target, ast.Name) and target.id in {"RUNNER_VERSION", "PAYLOAD_SCHEMA", "AUTHORISATION_SCHEMA", "MODEL", "REVISION", "MODEL_FILE_SHA256"}:
                try:
                    values[target.id] = ast.literal_eval(value_node)
                except (ValueError, TypeError):
                    pass
    return values


def validate_runners(root: Path, bindings: dict[str, Any], runtime_inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    runners = bindings.get("runners")
    require(isinstance(runners, dict) and set(runners) == REQUIRED_RUNNERS, "Runner roles are incomplete or unexpected")
    result: dict[str, dict[str, Any]] = {}
    for role, value in runners.items():
        expected = EXPECTED_RUNNER_SPECS[role]
        require(isinstance(value, dict), f"runners.{role}: expected object")
        require(set(value) == {"path", "sha256", "runner_version", "payload_schema", "authorisation_schema", "root_binding_mode"}, f"runners.{role}: fields drift")
        for key in ("path", "runner_version", "payload_schema", "authorisation_schema"):
            require(value.get(key) == expected[key], f"runners.{role}: Phase-8/B1-B2 compatibility drift: {key}")
        path = validate_bound_file(root, {"path": value["path"], "sha256": value["sha256"]}, field=f"runners.{role}")
        require(relative(path, root).startswith("skill_benchmark/scripts/"), f"runners.{role}: runner must be under skill_benchmark/scripts")
        constants = literal_constants(path)
        require(constants.get("RUNNER_VERSION") == value["runner_version"], f"runners.{role}: runner version drift")
        require(constants.get("PAYLOAD_SCHEMA") == value["payload_schema"], f"runners.{role}: missing/mismatched Phase-8 payload schema")
        require(constants.get("AUTHORISATION_SCHEMA") == value["authorisation_schema"], f"runners.{role}: missing/mismatched one-use authorisation schema")
        require(value["root_binding_mode"] == "PHASE8_RECEIPT_AND_FINAL_REPRESENTATION_HASHES", f"runners.{role}: root-binding mode drift")
        model_role = {
            "skillrouter_embedding_b1": "skillrouter_embedding",
            "skillrouter_reranker_b2": "skillrouter_reranker",
        }.get(role)
        if model_role is not None:
            snapshot = runtime_inventory["local_models"][model_role]
            require(constants.get("MODEL") == snapshot["repository"], f"runners.{role}: runtime model repository drift")
            require(constants.get("REVISION") == snapshot["revision"], f"runners.{role}: runtime model revision drift")
            require(constants.get("MODEL_FILE_SHA256") == snapshot["files"], f"runners.{role}: runtime model file-map drift")
        result[role] = {
            "path": relative(path, root),
            "sha256": file_sha256(path),
            "runner_version": value["runner_version"],
            "payload_schema": value["payload_schema"],
            "authorisation_schema": value["authorisation_schema"],
            "root_binding_mode": value["root_binding_mode"],
            "inspection": "AST_LITERAL_CONSTANTS_ONLY_RUNNER_NOT_IMPORTED",
        }
    return result


def validate_bindings_header(bindings: dict[str, Any]) -> str:
    require(set(bindings) == {"schema_version", "package_id", "dynamic_artifacts", "quality_reports", "runners"}, "Bindings top-level fields drift")
    require(bindings.get("schema_version") == BINDINGS_SCHEMA, "Bindings schema drift")
    package_id = bindings.get("package_id")
    require(isinstance(package_id, str) and re.fullmatch(r"RQ2b-NC-final-\d{4}-\d{2}-\d{2}-v\d+", package_id) is not None, "Package ID must be versioned")
    return package_id


def pending_template(*, role: str, runner: dict[str, Any], root_manifest_sha256: str, root_manifest_path: str) -> dict[str, Any]:
    phase = "B1" if role.endswith("b1") else "B2"
    prerequisites = [
        "explicit_user_approval",
        "unique_run_id_and_attempt_id",
        "exact_payload_path_and_sha256",
        "output_cache_attempt_destinations",
        "run_specific_time_call_token_and_cost_ceilings",
    ]
    if phase == "B2":
        prerequisites.extend(["complete_persisted_b1_top20_artifacts", "fresh_official_b1_validation_receipt_sha256"])
    return {
        "schema_version": TEMPLATE_SCHEMA,
        "state": PENDING_STATE,
        "execution_authorised": False,
        "one_use": True,
        "consumed": False,
        "target": role,
        "phase": phase,
        "target_authorisation_schema": runner["authorisation_schema"],
        "runner": {key: runner[key] for key in ("path", "sha256", "runner_version", "payload_schema")},
        "phase8_root": {"path": root_manifest_path, "sha256": root_manifest_sha256, "status": READY_STATUS},
        "required_before_release": prerequisites,
        "release_fields": {
            "root_release_id": None,
            "run_id": None,
            "attempt_id": None,
            "payload_path": None,
            "payload_sha256": None,
            "destinations": None,
            "ceilings": None,
            "explicit_user_approval_record": None,
        },
        "note": "Template only. Its PENDING state and null release fields are intentionally non-executable.",
    }


def render_readiness(package_id: str, root_sha: str) -> str:
    return f"""# RQ2b-NC V7 Phase-8 formal experiment readiness

Status: `{READY_STATUS}`.

Package: `{package_id}`

Root-manifest SHA-256: `{root_sha}`

This status means the frozen source, prompt, representation, QA, quality,
analysis, matrix, model, script and environment bindings passed the Phase-8
mechanical gates. It is not permission to run BM25, a provider, an embedding
model, a reranker, or offline outcome analysis.

The five authorisation files in `authorisations/` are PENDING templates. A
separate explicit user decision must fill a unique run/attempt identity,
payload hash, destinations and ceilings for one run. B2 additionally requires
complete persisted B1 Top-20 artifacts and a fresh official validation receipt.

Label/acceptable-set/reviewed-neighbour artifacts were bound by path, byte size
and SHA-256 only. Their content was not parsed, counted, copied or interpreted.
"""


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def build(
    *, root: Path, bindings_path: Path, output_dir: Path,
    fixed: dict[str, FixedArtifact] = FIXED_ARTIFACTS,
    builder_path: Path | None = None,
) -> dict[str, Any]:
    require(not output_dir.exists(), f"Refusing to overwrite output: {output_dir}")
    bindings_path = bindings_path.resolve()
    try:
        bindings_path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Bindings file must be inside repository root") from error
    bindings = read_json(bindings_path)
    package_id = validate_bindings_header(bindings)
    fixed_bound = validate_fixed_artifacts(root, fixed)
    source_ids, authority_reports = validate_authority_reports(root)
    dynamic_bound, dynamic_reports = validate_dynamic_artifacts(root, bindings, source_ids)
    quality_bound = validate_quality_reports(root, bindings)
    runner_bound = validate_runners(root, bindings, authority_reports["runtime_inventory"])

    inventory = authority_reports["runtime_inventory"]
    implementation_path = (builder_path or Path(__file__)).resolve()
    try:
        implementation_path.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Builder implementation must be inside repository root") from error
    root_manifest = {
        "schema_version": ROOT_SCHEMA,
        "status": READY_STATUS,
        "package_id": package_id,
        "execution_authorised": False,
        "labels_or_results_content_read": False,
        "selector_provider_or_model_runs": 0,
        "scope": {
            "queries": EXPECTED_QUERIES,
            "sources": EXPECTED_SOURCES,
            "source_union_sha256": SOURCE_UNION_SHA256,
            "prompt_manifest_sha256": PROMPT_MANIFEST_SHA256,
            "representations": ["I1-discovery", "I2-original", "I3C-fielded", "I3-flat"],
            "core_conditions": 36,
            "bridge_conditions": 6,
            "u0323_excluded": True,
        },
        "fixed_artifacts": fixed_bound,
        "final_phase7_artifacts": dynamic_bound,
        "phase8_quality_reports": quality_bound,
        "runners": runner_bound,
        "models": inventory["local_models"],
        "provider_contracts": inventory["dashscope_contracts"],
        "environment": inventory["environment"],
        "scientific_runtime_contract": inventory["scientific_runtime_contract"],
        "gates": {
            "final_library_freeze": authority_reports["final_library"]["status"],
            "i1_i2_v2": authority_reports["i1_i2"]["status"],
            "i3_selection": dynamic_reports["selection"]["state"],
            "i3_warning_final": dynamic_reports["warning_final"]["state"],
            "i3_merge": dynamic_reports["merge"]["state"],
            "i3_failed_qa_v4_preserved": dynamic_reports["failed_qa_v4"]["state"],
            "i3_intermediate_v4_1_4_preserved": dynamic_reports["intermediate_merge_v4_1_4"]["state"],
            "i3_failed_qa_v5_preserved": dynamic_reports["failed_qa_v5"]["state"],
            "i3_full_class_repair": dynamic_reports["merge"]["state"],
            "fresh_i3_qa_v6": dynamic_reports["qa_final"]["state"],
            "quality": {role: "PASS" for role in sorted(REQUIRED_QUALITY_REPORTS)},
        },
        "replay": {
            "builder": relative(implementation_path, root),
            "builder_sha256": file_sha256(implementation_path),
            "bindings": relative(bindings_path, root),
            "command": f"python3 -B {relative(implementation_path, root)} --root {root} --bindings {relative(bindings_path, root)} --output-dir {relative(output_dir, root)}",
        },
        "authorisation_boundary": "STOP_AFTER_ROOT_BUILD_REQUIRE_NEW_EXPLICIT_ONE_USE_AUTHORISATION_PER_RUN",
    }
    root_bytes = canonical_bytes(root_manifest)
    root_sha = hashlib.sha256(root_bytes).hexdigest()
    root_rel = relative(output_dir / "root_manifest.json", root)
    templates = {
        role: pending_template(role=role, runner=runner_bound[role], root_manifest_sha256=root_sha, root_manifest_path=root_rel)
        for role in sorted(REQUIRED_RUNNERS)
    }
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "status": "PASS_PHASE8_ROOT_READY_PENDING_EXPLICIT_PER_RUN_AUTHORISATION",
        "package_id": package_id,
        "root_manifest": {"path": root_rel, "sha256": root_sha, "rows": 1},
        "execution_authorised": False,
        "authorisation_templates": {
            role: {
                "path": relative(output_dir / "authorisations" / f"{role}.pending.json", root),
                "sha256": canonical_sha256(template),
                "state": PENDING_STATE,
            }
            for role, template in templates.items()
        },
        "external_activity": {"network_calls": 0, "selector_runs": 0, "provider_calls": 0, "model_forward_passes": 0, "offline_analysis_runs": 0},
        "label_provenance_access": "HASH_ONLY_NO_CONTENT_PARSE",
    }

    staging = output_dir.parent / f".{output_dir.name}.staging-{os.getpid()}"
    require(not staging.exists(), f"Stale staging directory: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    try:
        write_new(staging / "build_attempt.json", canonical_bytes({
            "schema_version": "rq2b-v7-phase8-root-build-attempt-v1",
            "package_id": package_id,
            "bindings": {"path": relative(bindings_path, root), "sha256": file_sha256(bindings_path)},
            "state": "VALIDATED_READY_TO_MATERIALISE",
            "execution_authorised": False,
        }))
        write_new(staging / "root_manifest.json", root_bytes)
        write_new(staging / "root_manifest.sha256", f"{root_sha}  root_manifest.json\n".encode())
        write_new(staging / "phase8_readiness_receipt.json", canonical_bytes(receipt))
        for role, template in templates.items():
            write_new(staging / "authorisations" / f"{role}.pending.json", canonical_bytes(template))
        write_new(staging / "FORMAL_EXPERIMENT_READINESS_REPORT.md", render_readiness(package_id, root_sha).encode())
        staging.rename(output_dir)
    except Exception:
        # Preserve the attempt directory for traceability.  It never becomes
        # the requested immutable root unless the final rename succeeds.
        raise
    return {
        "status": "PASS_PHASE8_ROOT_PACKAGE_CREATED_EXECUTION_NOT_AUTHORISED",
        "package_id": package_id,
        "output_dir": relative(output_dir, root),
        "root_manifest_sha256": root_sha,
        "authorisation_templates": len(templates),
        "network_calls": 0,
        "model_forward_passes": 0,
    }


def bindings_template() -> dict[str, Any]:
    return {
        "schema_version": BINDINGS_SCHEMA,
        "package_id": "RQ2b-NC-final-YYYY-MM-DD-vN",
        "dynamic_artifacts": {role: {"path": CANONICAL_DYNAMIC_PATHS[role], "sha256": None} for role in sorted(REQUIRED_DYNAMIC_ARTIFACTS)},
        "quality_reports": {role: {"path": CANONICAL_QUALITY_REPORT_PATHS[role], "sha256": None} for role in sorted(REQUIRED_QUALITY_REPORTS)},
        "runners": {
            role: {
                "path": EXPECTED_RUNNER_SPECS[role]["path"],
                "sha256": None,
                "runner_version": EXPECTED_RUNNER_SPECS[role]["runner_version"],
                "payload_schema": EXPECTED_RUNNER_SPECS[role]["payload_schema"],
                "authorisation_schema": EXPECTED_RUNNER_SPECS[role]["authorisation_schema"],
                "root_binding_mode": "PHASE8_RECEIPT_AND_FINAL_REPRESENTATION_HASHES",
            }
            for role in sorted(REQUIRED_RUNNERS)
        },
    }


def self_test() -> dict[str, Any]:
    require(PENDING_STATE != "EXPLICITLY_AUTHORISED", "Pending state must not be executable")
    sample = pending_template(
        role="bm25_b1",
        runner={"path": "skill_benchmark/scripts/future.py", "sha256": "0" * 64, "runner_version": "v", "payload_schema": "p", "authorisation_schema": "a"},
        root_manifest_sha256="1" * 64,
        root_manifest_path="skill_benchmark/final/root_manifest.json",
    )
    require(sample["execution_authorised"] is False and sample["state"] == PENDING_STATE, "Pending template self-test failed")
    require(all(value is None for value in sample["release_fields"].values()), "Pending release fields must be empty")
    template = bindings_template()
    require(set(template["dynamic_artifacts"]) == REQUIRED_DYNAMIC_ARTIFACTS, "Bindings template role drift")
    require(
        template["dynamic_artifacts"]["window_method_approval"]["path"]
        == "skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_skillrouter_embedding_window_approval_2026_09_09_v1/method_approval.json",
        "Canonical method-only approval template path drift",
    )
    require(template["dynamic_artifacts"]["window_method_approval"]["sha256"] is None, "Method-only approval SHA must remain an explicit final binding")
    return {
        "status": "PASS_PHASE8_ROOT_BUILDER_SYNTHETIC_SELF_TEST",
        "scientific_root_created": False,
        "execution_authorised": False,
        "network_calls": 0,
        "model_forward_passes": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--print-bindings-template", action="store_true")
    mode.add_argument("--build", action="store_true")
    parser.add_argument("--bindings", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    elif args.print_bindings_template:
        result = bindings_template()
    else:
        require(args.bindings is not None, "--bindings is required with --build")
        require(args.output_dir is not None, "--output-dir is required with --build")
        root = args.root.resolve()
        bindings = args.bindings if args.bindings.is_absolute() else root / args.bindings
        output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        try:
            output.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError("Output directory must be inside repository root") from error
        result = build(root=root, bindings_path=bindings, output_dir=output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
