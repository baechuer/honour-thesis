#!/usr/bin/env python3
"""Focused no-inference tests for the V7 Phase-8 root builder."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("build_rq2b_v7_phase8_execution_root.py")
SPEC = importlib.util.spec_from_file_location("phase8_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


class SyntheticFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.fixed: dict[str, builder.FixedArtifact] = {}
        self.dynamic: dict[str, dict[str, str]] = {}
        self.quality: dict[str, dict[str, str]] = {}
        self.runners: dict[str, dict[str, object]] = {}
        self.output = root / "skill_benchmark/final/RQ2b-NC-final-2026-09-09-v1"
        self.bindings_path = root / "skill_benchmark/cache/synthetic_phase8_bindings.json"
        self.source_ids = [f"{index + 1:064x}" for index in range(3)]
        self._fixed_files()
        self._dynamic_files()
        self.canonical_dynamic_paths = {role: value["path"] for role, value in self.dynamic.items()}
        self._quality_files()
        self.canonical_quality_report_paths = {role: value["path"] for role, value in self.quality.items()}
        self._runner_files()
        self.write_bindings()

    def _fixed(self, role: str, value: object, *, opaque: bool = False, suffix: str = ".json") -> None:
        path = self.root / "fixed" / f"{role}{suffix}"
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, bytes):
            path.write_bytes(value)
        elif suffix == ".jsonl":
            assert isinstance(value, list)
            write_jsonl(path, value)
        elif suffix == ".json":
            write_json(path, value)
        else:
            path.write_text(str(value), encoding="utf-8")
        self.fixed[role] = builder.FixedArtifact(
            path.relative_to(self.root).as_posix(), builder.file_sha256(path), opaque=opaque
        )

    def _fixed_files(self) -> None:
        arbitrary = {
            "approved_plan": ("plan", ".md", False),
            "master_sop": ("sop", ".md", False),
            "approved_plan_freeze": ({}, ".json", False),
            "final_library_prompt_manifest_review_provenance": (b"not-json-and-never-parsed\n", ".jsonl", True),
            "exclusion_ledger_review_provenance": (b"also-opaque\n", ".jsonl", True),
            "scope_amendment": ({}, ".json", False),
            "u0323_exclusion_note": ("excluded without target join", ".md", False),
            "core_conditions": ([{}], ".jsonl", False),
            "bridge_conditions": ([{}], ".jsonl", False),
            "label_free_runtime": ([{}], ".jsonl", False),
            "dependency_ledger": ([{}], ".jsonl", False),
            "exposure_ledger": ([{}], ".jsonl", False),
            "offline_label_adapter_review_provenance": (b"opaque-label-bytes\n", ".jsonl", True),
            "reviewed_neighbour_ledger_review_provenance": (b"opaque-review-bytes\n", ".jsonl", True),
            "i1_discovery_v2": ([{}], ".jsonl", False),
            "i2_original_v2": ([{}], ".jsonl", False),
            "qwen_b1_preflight_integrity_v2_lineage": ({}, ".json", False),
            "qwen_b1_preflight_report_v2_lineage": ({}, ".json", False),
            "analysis_contract": ({}, ".json", False),
            "b1_output_schema": ({}, ".json", False),
            "b2_output_schema": ({}, ".json", False),
            "official_output_validator": ("# validator\n", ".py", False),
        }
        for role, (value, suffix, opaque) in arbitrary.items():
            self._fixed(role, value, opaque=opaque, suffix=suffix)
        self._fixed("final_library_freeze_report", {
            "status": "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION",
            "counts": {"frozen_final_library_groups": 2},
            "integrity_assertions": {"u0323_remains_excluded_without_target_join": "PASS"},
            "output_hashes": {"final_library_prompt_manifest.jsonl": builder.PROMPT_MANIFEST_SHA256},
        })
        self._fixed("first_matrix_readiness", {
            "status": "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED",
            "counts": {"sources": 3, "prompts": 2},
        })
        self._fixed("source_manifest", [{"sha256": value} for value in self.source_ids], suffix=".jsonl")
        self._fixed("analysis_freeze_report", {
            "status": "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE",
            "counts": {"prompts": 2},
            "provider_calls": 0,
            "retrieval_or_reranking_runs": 0,
        })
        self._fixed("i1_i2_v2_report", {
            "status": "PASS_I1_IDENTITY_OVERLAY_AND_I2_BYTE_PRESERVATION_PENDING_I3_V4_AND_FRESH_QA",
            "counts": {"i1_rows": 3, "i2_exact_byte_rows": 3},
        })
        self._fixed("runtime_preflight_integrity", {
            "status": "PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY",
            "checks": {"zero_model_forward": True, "zero_network": True},
        })
        local_models = {}
        for role, expected in builder.EXPECTED_LOCAL_MODELS.items():
            snapshot = self.root / "skill_benchmark/cache/huggingface" / role
            snapshot.mkdir(parents=True, exist_ok=True)
            model_file = snapshot / "config.json"
            model_file.write_text(f"synthetic {role}\n", encoding="utf-8")
            local_models[role] = {
                "repository": expected["repository"],
                "revision": expected["revision"],
                "snapshot_path": snapshot.relative_to(self.root).as_posix(),
                "files": {"config.json": builder.file_sha256(model_file)},
            }
        self.local_models = local_models
        self._fixed("runtime_inventory", {
            "schema_version": "rq2b-v7-b36-c6-runtime-preflight-v1",
            "status": "PASS_ZERO_INFERENCE_RUNTIME_INVENTORY_EXECUTION_NOT_AUTHORISED",
            "local_models": local_models,
            "dashscope_contracts": {
                "embedding": {
                    "endpoint": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings",
                    "model": "text-embedding-v4",
                },
                "reranker": {
                    "endpoint": "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
                    "model": "qwen3-rerank",
                },
            },
            "environment": {"python": "synthetic"},
            "scientific_runtime_contract": {"device": "synthetic-no-forward"},
        })

    def _bind(self, role: str, path: Path) -> None:
        self.dynamic[role] = {
            "path": path.relative_to(self.root).as_posix(),
            "sha256": builder.file_sha256(path),
        }

    def _dynamic_files(self) -> None:
        dynamic_root = self.root / "dynamic"
        selection_ledger = dynamic_root / "selection_ledger.jsonl"
        write_jsonl(selection_ledger, [{"batch": 1}, {"batch": 2}])
        warning_ledger = dynamic_root / "warning_ledger.jsonl"
        write_jsonl(warning_ledger, [{"warning": "accepted"}])
        repair_ledger = dynamic_root / "class_repair_ledger.jsonl"
        write_jsonl(repair_ledger, [{"changed": True} for _ in self.source_ids])
        canonical = dynamic_root / "canonical.jsonl"
        write_jsonl(canonical, [{"source_sha256": value} for value in self.source_ids])
        i3c = dynamic_root / "i3c.jsonl"
        i3f = dynamic_root / "i3f.jsonl"
        for path, representation in ((i3c, "I3C-fielded"), (i3f, "I3-flat")):
            write_jsonl(path, [
                {
                    "representation": representation,
                    "source_sha256": source,
                    "selector_text": f"{representation}-{source}",
                    "selector_text_sha256": builder.hashlib.sha256(f"{representation}-{source}".encode()).hexdigest(),
                }
                for source in self.source_ids
            ])
        selection = dynamic_root / "selection.json"
        write_json(selection, {
            "schema_version": "rq2b-v7-i3-v4.1.3-warning-repair-integration-report-v1",
            "state": "PASS_95_BATCHES_V4_1_3_REPAIR_INTEGRATED_PENDING_FRESH_WARNING_AUDIT",
            "counts": {"batches": 2, "rows": 3},
            "output_bindings": {"selection_v3_ledger": {"sha256": builder.file_sha256(selection_ledger)}},
        })
        warning_build = dynamic_root / "warning_build.json"
        write_json(warning_build, {
            "schema_version": "rq2b-v7-i3-v4.1-warning-audit-build-report-v1",
            "state": "MATERIALISED_PENDING_SOURCE_ONLY_WARNING_RETURNS",
            "counts": {"selected_batches": 2, "sources": 3},
            "bindings": {
                "warning_docket_sha256": "a" * 64,
                "integration_report_sha256": builder.file_sha256(selection),
                "selection_ledger_sha256": builder.file_sha256(selection_ledger),
            },
        })
        warning_final = dynamic_root / "warning_final.json"
        write_json(warning_final, {
            "schema_version": "rq2b-v7-i3-v4.1-warning-audit-final-report-v1",
            "state": "PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA",
            "formal_execution_ready": False,
            "bindings": {
                "warning_docket_sha256": "a" * 64,
                "warning_build_report_sha256": builder.file_sha256(warning_build),
                "final_ledger_sha256": builder.file_sha256(warning_ledger),
            },
        })
        preclass_merge = dynamic_root / "preclass_merge.json"
        write_json(preclass_merge, {
            "schema_version": "rq2b-v7-phase7-i3-full-corpus-merged-v4.1",
            "state": "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING",
            "counts": {"sources": 3, "fresh_full_corpus": 3, "batches": 2},
            "bindings": {
                "assignment_manifest_sha256": "assignment-sha",
                "selection_report_sha256": builder.file_sha256(selection),
                "selection_ledger_sha256": builder.file_sha256(selection_ledger),
                "warning_audit_final_report_sha256": builder.file_sha256(warning_final),
                "i1_i2_v2_report_sha256": builder.file_sha256(self.root / self.fixed["i1_i2_v2_report"].path),
            },
            "artifacts": {
                "canonical_extractions.jsonl": {"sha256": builder.file_sha256(canonical), "rows": 3},
                "i3c_fielded.jsonl": {"sha256": builder.file_sha256(i3c), "rows": 3},
                "i3_flat.jsonl": {"sha256": builder.file_sha256(i3f), "rows": 3},
            },
        })
        failed_qa_v4 = dynamic_root / "failed_qa_v4.json"
        write_json(failed_qa_v4, {
            "schema_version": "rq2b-v7-i3-full-corpus-v4.1-blinded-qa-final-v3",
            "state": "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE",
            "formal_execution_ready": False,
            "counts": {"critical_error_rows": 0, "major_error_rows": 18},
        })
        intermediate_merge = dynamic_root / "intermediate_merge_v4_1_4.json"
        write_json(intermediate_merge, {
            "schema_version": "rq2b-v7-phase7-i3-class-repair-v4.1.4",
            "state": "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING",
            "counts": {"sources": 3, "fresh_full_corpus": 3, "batches": 2},
            "bindings": {
                "source_v4_1_3_manifest_sha256": builder.file_sha256(preclass_merge),
                "failed_fresh_qa_v4_report_sha256": builder.file_sha256(failed_qa_v4),
                "assignment_manifest_sha256": "assignment-sha",
            },
            "class_repair": {"rows_processed": 3, "failed_qa_sources_changed": 18},
            "artifacts": {
                "canonical_extractions.jsonl": {"sha256": builder.file_sha256(canonical), "rows": 3},
                "i3c_fielded.jsonl": {"sha256": builder.file_sha256(i3c), "rows": 3},
                "i3_flat.jsonl": {"sha256": builder.file_sha256(i3f), "rows": 3},
                "class_repair_ledger.jsonl": {"sha256": builder.file_sha256(repair_ledger), "rows": 3},
            },
        })
        failed_qa_v5_packet = dynamic_root / "failed_qa_v5_packet.json"
        write_json(failed_qa_v5_packet, {
            "schema_version": "rq2b-v7-i3-full-corpus-v4.1.4-blinded-qa-v1",
            "state": "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS",
            "sample_size": 2,
            "previous_samples_excluded": 240,
            "bindings": {"merged_manifest_sha256": builder.file_sha256(intermediate_merge)},
        })
        failed_qa_v5 = dynamic_root / "failed_qa_v5.json"
        write_json(failed_qa_v5, {
            "schema_version": "rq2b-v7-i3-full-corpus-v4.1.4-blinded-qa-final-v1",
            "state": "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE",
            "formal_execution_ready": False,
            "counts": {"critical_error_rows": 0, "major_error_rows": 13},
            "bindings": {
                "qa_packet_manifest_sha256": builder.file_sha256(failed_qa_v5_packet),
                "failed_qa_v4_report_sha256": builder.file_sha256(failed_qa_v4),
            },
        })
        merge = dynamic_root / "merge_v4_1_5.json"
        write_json(merge, {
            "schema_version": "rq2b-v7-phase7-i3-class-repair-v4.1.5",
            "state": "AUTOMATIC_INTEGRITY_PASS_FRESH_BLINDED_QA_PENDING",
            "counts": {"sources": 3, "fresh_full_corpus": 3, "batches": 2},
            "bindings": {
                "source_v4_1_4_manifest_sha256": builder.file_sha256(intermediate_merge),
                "source_v4_1_4_canonical_extractions_sha256": builder.file_sha256(canonical),
                "failed_fresh_qa_v5_report_sha256": builder.file_sha256(failed_qa_v5),
                "assignment_manifest_sha256": "assignment-sha",
            },
            "class_repair": {
                "rows_processed": 3,
                "failed_qa_v5_sources_bound": 13,
                "failed_qa_v5_sources_changed": 13,
            },
            "artifacts": {
                "canonical_extractions.jsonl": {"sha256": builder.file_sha256(canonical), "rows": 3},
                "i3c_fielded.jsonl": {"sha256": builder.file_sha256(i3c), "rows": 3},
                "i3_flat.jsonl": {"sha256": builder.file_sha256(i3f), "rows": 3},
                "class_repair_ledger.jsonl": {"sha256": builder.file_sha256(repair_ledger), "rows": 3},
            },
        })
        qa_packet = dynamic_root / "qa_packet_v6.json"
        write_json(qa_packet, {
            "schema_version": "rq2b-v7-i3-full-corpus-v4.1.5-blinded-qa-v1",
            "state": "FROZEN_PENDING_THREE_FRESH_CROSS_ASSIGNED_REVIEWER_GROUPS",
            "sample_size": 2,
            "previous_samples_excluded": 360,
            "bindings": {"merged_manifest_sha256": builder.file_sha256(merge)},
        })
        qa_finalizer = self.root / "skill_benchmark/scripts/finalize_rq2b_v7_i3_blinded_qa_v6.py"
        qa_finalizer.parent.mkdir(parents=True, exist_ok=True)
        qa_finalizer.write_text("# synthetic frozen QA-v6 finalizer\n", encoding="utf-8")
        reviewer_return_artifacts = {}
        for name, count in {
            **{f"reviewer_returns/calibration_group_{group}.jsonl": 8 for group in (1, 2, 3)},
            **{f"reviewer_returns/qa_slot_{slot:02d}_return.jsonl": 20 for slot in range(1, 7)},
        }.items():
            path = dynamic_root / name
            write_jsonl(path, [{"synthetic": index} for index in range(count)])
            reviewer_return_artifacts[name] = {"sha256": builder.file_sha256(path), "rows": count}
        qa_final = dynamic_root / "qa_final.json"
        write_json(qa_final, {
            "schema_version": "rq2b-v7-i3-full-corpus-v4.1.5-blinded-qa-final-v1",
            "state": "PASS_CURRENT_I1_I3_SEMANTIC_QA",
            "formal_execution_ready": True,
            "sample_size": 2,
            "counts": {"critical_error_rows": 0, "major_error_rows": 0},
            "major_error_rate": 0.0,
            "bindings": {
                "qa_packet_manifest_sha256": builder.file_sha256(qa_packet),
                "failed_qa_v5_report_sha256": builder.file_sha256(failed_qa_v5),
                "finalizer_sha256": builder.file_sha256(qa_finalizer),
            },
            "calibration": {"1": "PASS_EXACT_8_OF_8", "2": "PASS_EXACT_8_OF_8", "3": "PASS_EXACT_8_OF_8"},
            "pass_rule_replay": {
                "critical_error_rows": 0,
                "maximum_field_major_error_rate": 0.05,
                "maximum_major_error_rate": 0.05,
                "maximum_major_error_rows": 6,
                "represented_field_minimum_for_threshold": 20,
            },
            "field_strata": {
                field: {
                    "represented_or_missing_error_rows": 20,
                    "major_error_rows": 0,
                    "major_error_rate": 0.0,
                    "threshold_applies": True,
                }
                for field in builder.I3_FIELDS
            },
            "reviewer_return_artifacts": reviewer_return_artifacts,
            "error_review_ids": [],
        })
        amendment = dynamic_root / "amendment.json"
        write_json(amendment, {
            "schema_version": "rq2b-v7-skillrouter-embedding-window-method-amendment-v1",
            "proposal": {"window_tokens": 7500, "overlap_tokens": 256, "aggregation": "maximum query-to-window cosine per source"},
        })
        approval = dynamic_root / "approval.json"
        write_json(approval, {
            "schema_version": "rq2b-v7-skillrouter-window-approval-v1",
            "status": "APPROVED_FOR_PHASE8_ROOT_BINDING_NOT_EXECUTION",
            "execution_authorised": False,
            "method_amendment": amendment.relative_to(self.root).as_posix(),
            "method_amendment_sha256": builder.file_sha256(amendment),
            "approved_research_plan": self.fixed["approved_plan"].path,
            "approved_research_plan_sha256": self.fixed["approved_plan"].sha256,
            "plan_freeze": self.fixed["approved_plan_freeze"].path,
            "plan_freeze_sha256": self.fixed["approved_plan_freeze"].sha256,
            "approved_method": {
                "window_tokens": 7500,
                "window_token_basis": "content_tokens_add_special_tokens_false",
                "overlap_tokens": 256,
                "overlap_token_basis": "content_tokens_add_special_tokens_false",
                "coverage": "exact_lossless_character_coverage",
                "aggregation": "maximum_query_to_window_cosine",
            },
        })
        role_paths = {
            "i3_selection_report": selection,
            "i3_selection_ledger": selection_ledger,
            "i3_warning_build_report": warning_build,
            "i3_warning_final_report": warning_final,
            "i3_warning_disposition_ledger": warning_ledger,
            "i3_preclass_merge_manifest": preclass_merge,
            "i3_failed_qa_v4_report": failed_qa_v4,
            "i3_intermediate_merge_v4_1_4_manifest": intermediate_merge,
            "i3_intermediate_canonical_v4_1_4": canonical,
            "i3_failed_qa_v5_packet_manifest": failed_qa_v5_packet,
            "i3_failed_qa_v5_report": failed_qa_v5,
            "i3_merge_manifest": merge,
            "i3_class_repair_ledger": repair_ledger,
            "i3_canonical_extractions": canonical,
            "i3c_fielded": i3c,
            "i3_flat": i3f,
            "i3_qa_packet_manifest": qa_packet,
            "i3_qa_final_report": qa_final,
            "i3_qa_finalizer": qa_finalizer,
            "window_method_amendment": amendment,
            "window_method_approval": approval,
        }
        for role, path in role_paths.items():
            self._bind(role, path)

    def _quality_files(self) -> None:
        quality_builder = self.root / "skill_benchmark/scripts/synthetic_quality_builder.py"
        quality_builder.parent.mkdir(parents=True, exist_ok=True)
        quality_builder.write_text("QUALITY_BUILDER_VERSION = 'synthetic-quality-builder-v1'\n", encoding="utf-8")
        for role in builder.REQUIRED_QUALITY_REPORTS:
            path = self.root / "quality" / f"{role}.json"
            if role in builder.QUALITY_SEMANTIC_GATES:
                receipt = self.root / "quality" / f"{role}.final-adjudication-receipt"
                receipt.parent.mkdir(parents=True, exist_ok=True)
                receipt.write_bytes(f"opaque final adjudication provenance for {role}\n".encode())
                review = {
                    "semantic_judgment_required": True,
                    "final_adjudication_receipt": {"path": receipt.relative_to(self.root).as_posix(), "sha256": builder.file_sha256(receipt)},
                    "content_access": "HASH_ONLY_OPAQUE_FINAL_ADJUDICATION_PROVENANCE",
                }
            else:
                review = {"semantic_judgment_required": False, "final_adjudication_receipt": None, "content_access": "NOT_APPLICABLE_MECHANICAL_GATE"}
            write_json(path, {
                "schema_version": builder.QUALITY_SCHEMA,
                "gate": role,
                "status": "PASS",
                "formal_execution_ready": True,
                "source_union_sha256": builder.SOURCE_UNION_SHA256,
                "prompt_manifest_sha256": builder.PROMPT_MANIFEST_SHA256,
                "counts": {"prompts": 2, "sources": 3, "unresolved_findings": 0},
                "assertions": {assertion: "PASS" for assertion in builder.QUALITY_ASSERTIONS[role]},
                "evidence": [
                    {"path": self.fixed["source_manifest"].path, "sha256": self.fixed["source_manifest"].sha256, "content_access": "PARSED_MECHANICAL_REPLAY"},
                    {"path": self.fixed["final_library_prompt_manifest_review_provenance"].path, "sha256": self.fixed["final_library_prompt_manifest_review_provenance"].sha256, "content_access": "HASH_ONLY_OPAQUE_PROVENANCE"},
                ],
                "review_provenance": review,
                "quality_builder": {"path": quality_builder.relative_to(self.root).as_posix(), "sha256": builder.file_sha256(quality_builder), "version": "synthetic-quality-builder-v1"},
            })
            self.quality[role] = {"path": path.relative_to(self.root).as_posix(), "sha256": builder.file_sha256(path)}

    def _runner_files(self) -> None:
        for role in builder.REQUIRED_RUNNERS:
            expected = builder.EXPECTED_RUNNER_SPECS[role]
            path = self.root / expected["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            constants = (
                f"RUNNER_VERSION = {expected['runner_version']!r}\n"
                f"PAYLOAD_SCHEMA = {expected['payload_schema']!r}\n"
                f"AUTHORISATION_SCHEMA = {expected['authorisation_schema']!r}\n"
            )
            model_role = {
                "skillrouter_embedding_b1": "skillrouter_embedding",
                "skillrouter_reranker_b2": "skillrouter_reranker",
            }.get(role)
            if model_role is not None:
                snapshot = self.local_models[model_role]
                constants += (
                    f"MODEL = {snapshot['repository']!r}\n"
                    f"REVISION = {snapshot['revision']!r}\n"
                    f"MODEL_FILE_SHA256 = {snapshot['files']!r}\n"
                )
            path.write_text(constants, encoding="utf-8")
            self.runners[role] = {
                "path": path.relative_to(self.root).as_posix(),
                "sha256": builder.file_sha256(path),
                "runner_version": expected["runner_version"],
                "payload_schema": expected["payload_schema"],
                "authorisation_schema": expected["authorisation_schema"],
                "root_binding_mode": "PHASE8_RECEIPT_AND_FINAL_REPRESENTATION_HASHES",
            }

    def write_bindings(self) -> None:
        write_json(self.bindings_path, {
            "schema_version": builder.BINDINGS_SCHEMA,
            "package_id": "RQ2b-NC-final-2026-09-09-v1",
            "dynamic_artifacts": self.dynamic,
            "quality_reports": self.quality,
            "runners": self.runners,
        })

    def refresh_dynamic_hash(self, role: str) -> None:
        path = self.root / self.dynamic[role]["path"]
        self.dynamic[role]["sha256"] = builder.file_sha256(path)
        self.write_bindings()

    def build(self) -> dict:
        synthetic_builder = self.root / "skill_benchmark/scripts/build_rq2b_v7_phase8_execution_root.py"
        if not synthetic_builder.exists():
            synthetic_builder.parent.mkdir(parents=True, exist_ok=True)
            synthetic_builder.write_text("# synthetic builder identity\n", encoding="utf-8")
        with (
            patch.object(builder, "FIXED_ARTIFACTS", self.fixed),
            patch.object(builder, "EXPECTED_SOURCES", 3),
            patch.object(builder, "EXPECTED_QUERIES", 2),
            patch.object(builder, "EXPECTED_SELECTION_BATCHES", 2),
            patch.object(builder, "EXPECTED_QA_ROWS", 2),
            patch.object(builder, "CANONICAL_DYNAMIC_PATHS", self.canonical_dynamic_paths),
            patch.object(builder, "CANONICAL_QUALITY_REPORT_PATHS", self.canonical_quality_report_paths),
        ):
            return builder.build(
                root=self.root,
                bindings_path=self.bindings_path,
                output_dir=self.output,
                fixed=self.fixed,
                builder_path=synthetic_builder,
            )


class Phase8BuilderTests(unittest.TestCase):
    def fixture(self, directory: str) -> SyntheticFixture:
        return SyntheticFixture(Path(directory))

    def test_success_creates_pending_templates_without_parsing_opaque_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            report = fixture.build()
            self.assertEqual(report["authorisation_templates"], 5)
            self.assertFalse(json.loads((fixture.output / "phase8_readiness_receipt.json").read_text())["execution_authorised"])
            manifest = json.loads((fixture.output / "root_manifest.json").read_text())
            self.assertFalse(manifest["labels_or_results_content_read"])
            self.assertEqual(
                manifest["fixed_artifacts"]["offline_label_adapter_review_provenance"]["content_access"],
                "HASH_ONLY_OPAQUE_REVIEW_PROVENANCE",
            )
            for path in (fixture.output / "authorisations").glob("*.json"):
                template = json.loads(path.read_text())
                self.assertEqual(template["state"], builder.PENDING_STATE)
                self.assertFalse(template["execution_authorised"])
                self.assertTrue(all(value is None for value in template["release_fields"].values()))

    def test_warning_final_nonpass_blocks_without_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            path = fixture.root / fixture.dynamic["i3_warning_final_report"]["path"]
            report = json.loads(path.read_text())
            report["state"] = "BLOCKED_TRACEABLE_REISSUE_REQUIRED_NEW_SELECTION_AND_WARNING_AUDIT_VERSION"
            write_json(path, report)
            fixture.refresh_dynamic_hash("i3_warning_final_report")
            with self.assertRaisesRegex(ValueError, "required state=PASS_ALL_WARNINGS"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_preclass_lineage_splice_blocks_without_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            path = fixture.root / fixture.dynamic["i3_preclass_merge_manifest"]["path"]
            report = json.loads(path.read_text())
            report["bindings"]["selection_report_sha256"] = "0" * 64
            write_json(path, report)
            fixture.refresh_dynamic_hash("i3_preclass_merge_manifest")
            with self.assertRaisesRegex(ValueError, "V4.1.3 selection-report binding drift"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_fresh_qa_nonpass_blocks_without_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            path = fixture.root / fixture.dynamic["i3_qa_final_report"]["path"]
            report = json.loads(path.read_text())
            report["state"] = "FAIL_REPAIR_AFFECTED_CLASS_AND_DRAW_FRESH_VERSIONED_SAMPLE"
            report["formal_execution_ready"] = False
            write_json(path, report)
            fixture.refresh_dynamic_hash("i3_qa_final_report")
            with self.assertRaisesRegex(ValueError, "required state=PASS_CURRENT"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_fresh_qa_reviewer_return_drift_blocks_without_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            report_path = fixture.root / fixture.dynamic["i3_qa_final_report"]["path"]
            report = json.loads(report_path.read_text())
            name = "reviewer_returns/qa_slot_01_return.jsonl"
            return_path = report_path.parent / name
            return_path.write_text(return_path.read_text() + '{"tampered":true}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "reviewer-return artifact drift"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_runner_without_one_use_gate_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            binding = fixture.runners["bm25_b1"]
            path = fixture.root / str(binding["path"])
            path.write_text(f"RUNNER_VERSION = {binding['runner_version']!r}\nPAYLOAD_SCHEMA = {binding['payload_schema']!r}\n", encoding="utf-8")
            binding["sha256"] = builder.file_sha256(path)
            fixture.write_bindings()
            with self.assertRaisesRegex(ValueError, "one-use authorisation schema"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_hash_drift_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            fixture.dynamic["i3_selection_report"]["sha256"] = "0" * 64
            fixture.write_bindings()
            with self.assertRaisesRegex(ValueError, "hash drift"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_dynamic_artifact_noncanonical_path_blocks_even_when_self_consistent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            role = "i3_selection_report"
            original_path = fixture.root / fixture.dynamic[role]["path"]
            alternate_path = fixture.root / "alternate" / original_path.name
            alternate_path.parent.mkdir(parents=True, exist_ok=True)
            alternate_path.write_bytes(original_path.read_bytes())
            fixture.dynamic[role] = {
                "path": alternate_path.relative_to(fixture.root).as_posix(),
                "sha256": builder.file_sha256(alternate_path),
            }
            fixture.write_bindings()
            with self.assertRaisesRegex(ValueError, "canonical path drift"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_local_runner_model_file_map_drift_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            binding = fixture.runners["skillrouter_embedding_b1"]
            path = fixture.root / str(binding["path"])
            content = path.read_text(encoding="utf-8").replace(
                repr(fixture.local_models["skillrouter_embedding"]["files"]),
                repr({"config.json": "0" * 64}),
            )
            path.write_text(content, encoding="utf-8")
            binding["sha256"] = builder.file_sha256(path)
            fixture.write_bindings()
            with self.assertRaisesRegex(ValueError, "runtime model file-map drift"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_legacy_minimal_quality_report_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            binding = fixture.quality["cue"]
            path = fixture.root / binding["path"]
            write_json(path, {
                "schema_version": "rq2b-v7-phase8-quality-gate-v1",
                "gate": "cue",
                "status": "PASS",
                "formal_execution_ready": True,
                "source_union_sha256": builder.SOURCE_UNION_SHA256,
                "prompt_manifest_sha256": builder.PROMPT_MANIFEST_SHA256,
            })
            binding["sha256"] = builder.file_sha256(path)
            fixture.write_bindings()
            with self.assertRaisesRegex(ValueError, "key drift|schema drift"):
                fixture.build()
            self.assertFalse(fixture.output.exists())

    def test_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.fixture(tmp)
            fixture.output.mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                fixture.build()


if __name__ == "__main__":
    unittest.main()
