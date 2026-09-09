#!/usr/bin/env python3
"""Focused no-inference tests for the V7 quality review docket v3 builder."""

from __future__ import annotations

import contextlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("build_rq2b_v7_phase8_quality_review_docket_v3.py")
SPEC = importlib.util.spec_from_file_location("quality_review_docket_v3", SCRIPT)
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


class Fixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.fixed: dict[str, builder.FixedArtifact] = {}
        self.prompt_manifest_sha = ""
        self.source_union_sha = ""
        self.phase3_bound: dict[str, str] = {}
        self._build()

    def add_fixed(self, role: str, path: Path, *, opaque: bool = False) -> None:
        self.fixed[role] = builder.FixedArtifact(path.relative_to(self.root).as_posix(), builder.file_sha256(path), opaque)

    def bound_file(self, relative_path: str, value: object, *, jsonl: bool = False) -> Path:
        path = self.root / relative_path
        if jsonl:
            assert isinstance(value, list)
            write_jsonl(path, value)
        else:
            write_json(path, value)
        self.phase3_bound[relative_path] = builder.file_sha256(path)
        return path

    def _build(self) -> None:
        plan = self.root / "authorities/plan.md"
        plan.parent.mkdir(parents=True, exist_ok=True)
        plan.write_text("approved plan\n", encoding="utf-8")
        self.add_fixed("approved_plan", plan)
        freeze = self.root / "authorities/plan_freeze.json"
        write_json(freeze, {"status": "synthetic"})
        self.add_fixed("plan_freeze", freeze)

        sop_rel = "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"
        sop = self.root / sop_rel
        sop.parent.mkdir(parents=True, exist_ok=True)
        sop.write_text("synthetic SOP\n", encoding="utf-8")
        self.add_fixed("master_sop", sop)
        self.phase3_bound[sop_rel] = builder.file_sha256(sop)

        source_rows = []
        bodies = [
            "---\nname: Shared Title\ndescription: shared workflow description\n---\nalpha workflow\n",
            "---\nname: Shared Title\ndescription: shared workflow description\n---\nbeta workflow\n",
            "---\nname: Independent Tool\ndescription: another task\n---\ngamma\n",
            "---\nname: Review Helper\ndescription: review a document\n---\ndelta\n",
        ]
        for index, body in enumerate(bodies):
            path = self.root / f"sources/source-{index}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            source_rows.append({"path": path.relative_to(self.root).as_posix(), "sha256": builder.file_sha256(path), "bytes": path.stat().st_size})
        source_manifest = self.root / "fixed/source_manifest.jsonl"
        write_jsonl(source_manifest, source_rows)
        self.add_fixed("source_manifest", source_manifest)

        prompt_texts = [
            "Prepare a shared title workflow with a weekly checklist and summary.",
            "Prepare the shared title workflow with a weekly checklist and concise summary.",
            "Draft an independent meeting plan.",
            "Review a SKILL.md file for structure.",
        ]
        prompts = [
            {"schema_version": "rq2b-v7-label-free-query-runtime-v1", "prompt_id": f"p{index + 1}", "prompt": text, "prompt_sha256": builder.text_sha256(text)}
            for index, text in enumerate(prompt_texts)
        ]
        runtime = self.root / "fixed/runtime.jsonl"
        write_jsonl(runtime, prompts)
        self.add_fixed("label_free_runtime", runtime)

        dependency_rows = []
        definitions = [
            ("p1", "B_NC_FULL_UNION", "D-MIXED", "nc-group", 0),
            ("p2", "A_PARENT_DELTA", "D-MIXED", "parent-group", 0),
            ("p3", "B_NC_FULL_UNION", "D-NC", "nc-other", 2),
            ("p4", "A_PARENT_DELTA", "D-PARENT", "parent-other", 3),
        ]
        by_prompt = {row["prompt_id"]: row for row in prompts}
        for prompt_id, lane, group, reporting, source_index in definitions:
            prompt = by_prompt[prompt_id]
            dependency_rows.append({
                "schema_version": "rq2b-v7-dependency-ledger-v1",
                "prompt_id": prompt_id,
                "prompt_sha256": prompt["prompt_sha256"],
                "dependency_group": group,
                "lane_id": lane,
                "reporting_group": reporting,
                "dependency_anchor_source_sha256": source_rows[source_index]["sha256"],
                "edge_policy": "synthetic-pre-outcome",
            })
        dependency = self.root / "fixed/dependency.jsonl"
        write_jsonl(dependency, dependency_rows)
        self.add_fixed("dependency_ledger", dependency)

        exposure = self.root / "fixed/exposure.jsonl"
        exposure.parent.mkdir(parents=True, exist_ok=True)
        exposure.write_bytes(b"not-json-and-must-remain-opaque\n")
        self.add_fixed("exposure_ledger", exposure, opaque=True)

        phase3_dir = self.root / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
        phase3_dir.mkdir(parents=True, exist_ok=True)
        union_rows = [{"canonical_source_sha256": row["sha256"]} for row in source_rows]
        union = phase3_dir / "candidate_source_union_for_phase4.jsonl"
        write_jsonl(union, union_rows)
        self.source_union_sha = builder.file_sha256(union)
        self.add_fixed("phase3_source_union", union)

        cross_prefix = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cross_cluster_reuse_adjudication_2026-09-05"
        self.bound_file(f"{cross_prefix}/summary.json", {"counts": {"admission_blocked": 8, "blocked_or_unclear": 2, "duplicate_cluster": 2, "related_but_distinct": 4, "reviewed_exact_reuses": 8}})
        self.bound_file(f"{cross_prefix}/final_cross_cluster_dispositions.jsonl", [{"phase3_admission_disposition": "BLOCKED_PENDING_EXCLUSION_OR_EXPLICIT_METHOD_DECISION"} for _ in range(8)], jsonl=True)

        semantic_prefix = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_semantic_qa_300plus_2026-09-05_v2"
        self.bound_file(f"{semantic_prefix}/source_relation_screen.jsonl", [{"screen_id": f"s{index}"} for index in range(8)], jsonl=True)

        cue_adjudication = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_prompt_cue_adjudication_2026-09-05_v2"
        cue_rows = [{"final_cue_decision": "AVOIDABLE_IDENTITY_CUE"} for _ in range(14)] + [{"final_cue_decision": "DECLARED_NECESSARY_CUE_STRATUM"} for _ in range(16)]
        relation_rows = [{"final_relation_decision": "RELATED_BUT_DISTINCT"} for _ in range(60)] + [{"final_relation_decision": "TRANSFORMED_DUPLICATE"}]
        self.bound_file(f"{cue_adjudication}/final_prompt_cue_dispositions.jsonl", cue_rows, jsonl=True)
        self.bound_file(f"{cue_adjudication}/final_prompt_relation_dispositions.jsonl", relation_rows, jsonl=True)

        cue1 = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_001_closure_2026-09-05"
        self.bound_file(f"{cue1}/summary.json", {"counts": {"deferred_local_families": 2, "cue_gate_failed_after_capped_remediation": 2}})
        self.bound_file(f"{cue1}/final_remediation_dispositions.jsonl", [{"opaque": True}], jsonl=True)
        cue2 = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_closure_2026-09-05"
        self.bound_file(f"{cue2}/summary.json", {"counts": {"cue_safe_after_resolution": 3, "reinstated_local_families": 2}})
        self.bound_file(f"{cue2}/final_remediation_dispositions.jsonl", [{"opaque": True}], jsonl=True)
        cue2_author = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_002_2026-09-05/author_return.jsonl"
        self.bound_file(cue2_author, [{"opaque": True}], jsonl=True)
        cue3 = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_closure_2026-09-05"
        self.bound_file(f"{cue3}/summary.json", {"counts": {"cue_safe_after_resolution": 1, "reinstated_local_families": 1}})
        self.bound_file(f"{cue3}/final_remediation_dispositions.jsonl", [{"opaque": True}], jsonl=True)
        cue3_author = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_cue_remediation_wave_003_2026-09-05/author_return.jsonl"
        self.bound_file(cue3_author, [{"opaque": True}], jsonl=True)

        parent_prefix = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_parent_v3_validity_audit_closure_2026-09-05"
        self.bound_file(f"{parent_prefix}/summary.json", {"counts": {"excluded_parent_prompt_ids": 9, "blocked_parent_prompt_ids": 0}})
        self.bound_file(f"{parent_prefix}/final_parent_v3_validity_dispositions.jsonl", [{"opaque": True}], jsonl=True)

        preflight = "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_source_union_preflight_300plus_2026-09-05_v2"
        for filename in ("candidate_source_union.jsonl", "nc_cluster_manifest.jsonl", "nc_prompt_manifest.jsonl", "parent_prompt_manifest.jsonl"):
            self.bound_file(f"{preflight}/{filename}", [{"opaque": True}], jsonl=True)
        self.bound_file(f"{preflight}/summary.json", {"status": "synthetic"})
        assert len(self.phase3_bound) == 21

        output_names = [
            "candidate_local_only_removed_phase3.jsonl",
            "candidate_local_origin_records_pruned_phase3.jsonl",
            "candidate_source_union_for_phase4.jsonl",
            "nc_cluster_deferred_phase3.jsonl",
            "nc_cluster_excluded_phase3.jsonl",
            "nc_cluster_manifest_for_phase4.jsonl",
            "nc_prompt_deferred_phase3.jsonl",
            "nc_prompt_excluded_phase3.jsonl",
            "nc_prompt_manifest_for_phase4.jsonl",
            "nc_prompt_superseded_phase3_remediation.jsonl",
            "parent_prompt_excluded_validity_phase3.jsonl",
            "parent_prompt_manifest_for_phase5.jsonl",
            "phase3_status_ledger.jsonl",
        ]
        outputs = {}
        for filename in output_names:
            path = phase3_dir / filename
            if filename == "candidate_source_union_for_phase4.jsonl":
                pass
            else:
                write_jsonl(path, [{"synthetic": filename}])
            outputs[filename] = builder.file_sha256(path)
        phase3_summary = phase3_dir / "summary.json"
        write_json(phase3_summary, {
            "status": "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE",
            "counts": {
                "historical_phase1_structural_progress_clusters": 304,
                "historical_phase3_preflight_nc_clusters": 304,
                "historical_phase3_preflight_nc_prompts": 875,
                "historical_preflight_canonical_candidates": 3810,
                "phase3_admitted_checkpoint_nc_clusters_for_phase4": 54,
                "phase3_admitted_nc_clusters_for_phase4": 297,
                "phase3_admitted_nc_prompts_for_phase4": 854,
                "phase3_admitted_source_native_nc_clusters_for_phase4": 243,
                "phase3_admitted_source_native_nc_prompts_for_phase4": 729,
                "phase3_cue_capped_deferred_nc_clusters": 2,
                "phase3_local_only_candidates_removed": 12,
                "phase3_local_origin_records_pruned": 21,
                "phase3_parent_v3_excluded_prompts": 9,
                "phase3_parent_v3_prompts_for_phase5": 372,
                "phase3_prospective_canonical_candidates_for_phase4": 3798,
                "phase3_remediated_active_nc_prompts_for_phase4": 4,
                "phase3_source_reuse_excluded_nc_clusters": 5,
            },
            "bound_inputs": self.phase3_bound,
            "outputs": outputs,
        })
        self.add_fixed("phase3_closure", phase3_summary)

        final_prompt = self.root / "fixed/final_prompt_manifest.jsonl"
        final_prompt.parent.mkdir(parents=True, exist_ok=True)
        final_prompt.write_bytes(b"opaque-label-bearing-manifest\n")
        self.prompt_manifest_sha = builder.file_sha256(final_prompt)
        self.add_fixed("final_prompt_manifest", final_prompt, opaque=True)
        final_freeze = self.root / "fixed/final_freeze.json"
        write_json(final_freeze, {"status": "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION", "counts": {"frozen_final_library_groups": 4}, "output_hashes": {"final_library_prompt_manifest.jsonl": self.prompt_manifest_sha}})
        self.add_fixed("final_freeze", final_freeze)
        matrix = self.root / "fixed/first_matrix.json"
        write_json(matrix, {"status": "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED", "counts": {"prompts": 4, "sources": 4}, "bindings": {"prompt_manifest_sha256": self.prompt_manifest_sha, "source_union_sha256": self.source_union_sha}})
        self.add_fixed("first_matrix_readiness", matrix)
        analysis = self.root / "fixed/analysis.json"
        write_json(analysis, {
            "status": "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE",
            "counts": {"prompts": 4, "candidates": 4},
            "artifacts": {
                "dependency_ledger.jsonl": {"rows": 4, "sha256": self.fixed["dependency_ledger"].sha256},
                "exposure_ledger.jsonl": {"rows": 4, "sha256": self.fixed["exposure_ledger"].sha256},
                "label_free_query_runtime.jsonl": {"rows": 4, "sha256": self.fixed["label_free_runtime"].sha256},
            },
            "label_isolation": {"runtime_file": "label_free_query_runtime.jsonl"},
        })
        self.add_fixed("analysis_freeze", analysis)

    @contextlib.contextmanager
    def patched(self):
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(builder, "FIXED_ARTIFACTS", self.fixed))
            stack.enter_context(patch.object(builder, "EXPECTED_PROMPTS", 4))
            stack.enter_context(patch.object(builder, "EXPECTED_SOURCES", 4))
            stack.enter_context(patch.object(builder, "EXPECTED_SOURCE_BYTES", sum((self.root / row["path"]).stat().st_size for row in builder.read_jsonl(self.root / self.fixed["source_manifest"].path))))
            stack.enter_context(patch.object(builder, "EXPECTED_DEPENDENCY_GROUPS", 3))
            stack.enter_context(patch.object(builder, "EXPECTED_PARENT_PROMPTS", 2))
            stack.enter_context(patch.object(builder, "EXPECTED_NC_PROMPTS", 2))
            stack.enter_context(patch.object(builder, "EXPECTED_PHASE3_BOUND_INPUTS", 21))
            stack.enter_context(patch.object(builder, "EXPECTED_MIXED_GROUPS", {"D-MIXED"}))
            stack.enter_context(patch.object(builder, "PROMPT_MANIFEST_SHA256", self.prompt_manifest_sha))
            stack.enter_context(patch.object(builder, "SOURCE_UNION_SHA256", self.source_union_sha))
            yield


class QualityReviewDocketTests(unittest.TestCase):
    def test_self_test_never_emits_quality_pass(self) -> None:
        result = builder.self_test()
        self.assertEqual(result["quality_pass_reports_emitted"], 0)
        self.assertFalse(result["formal_execution_ready"])

    def test_reaudits_complete_bound_chain_but_remains_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            with fixture.patched():
                docket, packets, decision = builder.audit_canonical(fixture.root)
            self.assertEqual(docket["status"], builder.BLOCKED_STATUS)
            self.assertEqual(docket["restored_phase3_evidence_assessment"]["phase3_bound_inputs_hash_matching"], 21)
            self.assertEqual(len(packets["mixed_lane_split_review_packets.jsonl"]), 1)
            self.assertGreater(len(packets["prompt_relation_review_packets.jsonl"]), 0)
            self.assertGreater(len(packets["cue_review_packets.jsonl"]), 0)
            self.assertGreater(len(packets["source_relation_review_packets.jsonl"]), 0)
            self.assertEqual(decision["status"], "PENDING_REVIEW_NOT_A_QUALITY_PASS")

    def test_missing_restored_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            path = fixture.root / next(value for value in fixture.phase3_bound if value.endswith("source_relation_screen.jsonl"))
            path.unlink()
            with fixture.patched(), self.assertRaisesRegex(ValueError, "evidence missing"):
                builder.audit_canonical(fixture.root)

    def test_missing_auxiliary_phase3_output_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            phase3_dir = fixture.root / "skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase3_admission_closure_300plus_2026-09-05"
            (phase3_dir / "candidate_local_only_removed_phase3.jsonl").unlink()
            with fixture.patched(), self.assertRaisesRegex(ValueError, "not 13/13"):
                builder.audit_canonical(fixture.root)

    def test_source_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            (fixture.root / "sources/source-0.md").write_text("changed\n", encoding="utf-8")
            with fixture.patched(), self.assertRaisesRegex(ValueError, "byte count drift|SHA drift"):
                builder.audit_canonical(fixture.root)

    def test_exposure_content_is_hash_only_and_never_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            with fixture.patched():
                docket, _, _ = builder.audit_canonical(fixture.root)
            self.assertEqual(docket["fixed_artifacts"]["exposure_ledger"]["content_access"], "HASH_ONLY_OPAQUE_PROVENANCE")

    def test_materialize_refuses_overwrite_and_emits_no_pass_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            synthetic_builder = fixture.root / "skill_benchmark/scripts/build_rq2b_v7_phase8_quality_review_docket_v3.py"
            synthetic_builder.parent.mkdir(parents=True, exist_ok=True)
            synthetic_builder.write_text("BUILDER_VERSION = 'synthetic'\n", encoding="utf-8")
            output = fixture.root / "package"
            with fixture.patched():
                result = builder.materialize(fixture.root, output, builder_path=synthetic_builder)
                self.assertEqual(result["quality_pass_reports_emitted"], 0)
                self.assertNotIn("split.json", {path.name for path in output.iterdir()})
                with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                    builder.materialize(fixture.root, output, builder_path=synthetic_builder)

    def test_packets_exclude_hidden_identity_and_result_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            with fixture.patched():
                _, packets, _ = builder.audit_canonical(fixture.root)
            prohibited = {"target", "gold", "acceptable_set", "selector_result", "metric", "outcome"}

            def walk(value: object) -> None:
                if isinstance(value, dict):
                    self.assertFalse(set(value) & prohibited)
                    for nested in value.values():
                        walk(nested)
                elif isinstance(value, list):
                    for nested in value:
                        walk(nested)

            walk(packets)


if __name__ == "__main__":
    unittest.main(verbosity=2)
