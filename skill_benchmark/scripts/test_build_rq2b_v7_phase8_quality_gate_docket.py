#!/usr/bin/env python3
"""Focused no-inference tests for the V7 Phase-8 quality docket builder."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("build_rq2b_v7_phase8_quality_gate_docket.py")
SPEC = importlib.util.spec_from_file_location("quality_docket", SCRIPT)
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
        self.prompt_manifest_sha = builder.text_sha256("opaque-final-prompt-provenance\n")
        self.source_union_sha = "a" * 64
        self._build()

    def add(self, role: str, value: object, *, suffix: str = ".json", opaque: bool = False) -> Path:
        path = self.root / "fixed" / f"{role}{suffix}"
        if isinstance(value, bytes):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
        elif suffix == ".jsonl":
            assert isinstance(value, list)
            write_jsonl(path, value)
        elif suffix == ".json":
            write_json(path, value)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(value), encoding="utf-8")
        self.fixed[role] = builder.FixedArtifact(path.relative_to(self.root).as_posix(), builder.file_sha256(path), opaque)
        return path

    def _build(self) -> None:
        self.add("approved_plan", "plan", suffix=".md")
        sop = self.add("master_sop", "sop", suffix=".md")
        self.add("plan_freeze", {})
        final_prompt = self.add("final_prompt_manifest", b"opaque-final-prompt-provenance\n", suffix=".jsonl", opaque=True)
        assert builder.file_sha256(final_prompt) == self.prompt_manifest_sha

        source_rows = []
        for index in range(3):
            path = self.root / "sources" / f"{index}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"source {index}\n", encoding="utf-8")
            source_rows.append({"path": path.relative_to(self.root).as_posix(), "sha256": builder.file_sha256(path), "bytes": path.stat().st_size})
        self.add("source_manifest", source_rows, suffix=".jsonl")

        prompts = [
            {"schema_version": "rq2b-v7-label-free-query-runtime-v1", "prompt_id": "p-nc", "prompt": "first prompt", "prompt_sha256": builder.text_sha256("first prompt")},
            {"schema_version": "rq2b-v7-label-free-query-runtime-v1", "prompt_id": "p-parent", "prompt": "second prompt", "prompt_sha256": builder.text_sha256("second prompt")},
        ]
        self.add("label_free_runtime", prompts, suffix=".jsonl")
        dependencies = []
        exposures = []
        for prompt, lane, disposition in (
            (prompts[0], "B_NC_FULL_UNION", "NC_PRIMARY_WITH_SOURCE_NATIVE_SENSITIVITY"),
            (prompts[1], "A_PARENT_DELTA", "PARENT_ROBUSTNESS_ONLY"),
        ):
            dependencies.append({
                "schema_version": "rq2b-v7-dependency-ledger-v1",
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
                "dependency_group": "D-MIXED",
                "lane_id": lane,
                "reporting_group": "synthetic",
                "dependency_anchor_source_sha256": source_rows[0]["sha256"],
                "edge_policy": "synthetic-pre-outcome",
            })
            exposures.append({
                "schema_version": "rq2b-v7-exposure-ledger-v1",
                "prompt_id": prompt["prompt_id"],
                "prompt_sha256": prompt["prompt_sha256"],
                "dependency_group": "D-MIXED",
                "prompt_level_exposure": "synthetic",
                "historical_selector_outcome_evidence": "synthetic",
                "global_design_exposure": "synthetic",
                "analysis_disposition": disposition,
            })
        self.add("dependency_ledger", dependencies, suffix=".jsonl")
        self.add("exposure_ledger", exposures, suffix=".jsonl")
        self.add("analysis_freeze", {
            "status": "PASS_PRE_OUTCOME_QUERY_LABEL_DEPENDENCY_EXPOSURE_AND_DQ_FREEZE",
            "counts": {"prompts": 2, "candidates": 3},
            "artifacts": {
                "dependency_ledger.jsonl": {"rows": 2, "sha256": self.fixed["dependency_ledger"].sha256},
                "exposure_ledger.jsonl": {"rows": 2, "sha256": self.fixed["exposure_ledger"].sha256},
                "label_free_query_runtime.jsonl": {"rows": 2, "sha256": self.fixed["label_free_runtime"].sha256},
            },
            "label_isolation": {"runtime_file": "label_free_query_runtime.jsonl"},
        })
        self.add("first_matrix_readiness", {
            "status": "PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED",
            "counts": {"prompts": 2, "sources": 3},
            "bindings": {"prompt_manifest_sha256": self.prompt_manifest_sha, "source_union_sha256": self.source_union_sha},
        })
        self.add("final_freeze", {
            "status": "PASS_V7_1077_GROUP_ACCEPTABLE_SET_FINAL_LIBRARY_FROZEN_PENDING_EXPERIMENT_AUTHORISATION",
            "counts": {"frozen_final_library_groups": 2},
            "output_hashes": {"final_library_prompt_manifest.jsonl": self.prompt_manifest_sha},
        })
        missing = "missing/final_semantic_receipt.json"
        self.add("phase3_closure", {
            "status": "PASS_PHASE3_CLOSED_READY_FOR_PHASE4_AUDIT_INPUT_METHOD_FREEZE",
            "bound_inputs": {
                sop.relative_to(self.root).as_posix(): self.fixed["master_sop"].sha256,
                missing: "f" * 64,
            },
        })

    def context(self):
        return (
            patch.object(builder, "FIXED_ARTIFACTS", self.fixed),
            patch.object(builder, "EXPECTED_PROMPTS", 2),
            patch.object(builder, "EXPECTED_SOURCES", 3),
            patch.object(builder, "EXPECTED_DEPENDENCY_GROUPS", 1),
            patch.object(builder, "EXPECTED_PARENT_PROMPTS", 1),
            patch.object(builder, "EXPECTED_NC_PROMPTS", 1),
            patch.object(builder, "PROMPT_MANIFEST_SHA256", self.prompt_manifest_sha),
            patch.object(builder, "SOURCE_UNION_SHA256", self.source_union_sha),
        )


class QualityDocketTests(unittest.TestCase):
    def test_self_test_never_emits_scientific_pass(self) -> None:
        report = builder.self_test()
        self.assertEqual(report["quality_pass_reports_emitted"], 0)
        self.assertFalse(report["formal_execution_ready"])

    def test_missing_semantic_evidence_yields_blocking_docket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            with fixture.context()[0], fixture.context()[1], fixture.context()[2], fixture.context()[3], fixture.context()[4], fixture.context()[5], fixture.context()[6], fixture.context()[7]:
                docket = builder.audit_canonical(fixture.root, fixture.fixed)
            self.assertEqual(docket["status"], builder.BLOCKED_STATUS)
            self.assertEqual(docket["quality_pass_reports_emitted"], 0)
            self.assertEqual(docket["mechanical_findings"]["phase3_bound_inputs_missing"], 1)
            self.assertEqual(docket["mechanical_findings"]["mixed_lane_dependency_groups"], 1)
            self.assertTrue(all(row["status"] != "PASS" for row in docket["gates"]))

    def test_source_hash_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            source = fixture.root / "sources/0.md"
            source.write_text("changed\n", encoding="utf-8")
            contexts = fixture.context()
            with contexts[0], contexts[1], contexts[2], contexts[3], contexts[4], contexts[5], contexts[6], contexts[7]:
                with self.assertRaisesRegex(ValueError, "byte count drift|SHA drift"):
                    builder.audit_canonical(fixture.root, fixture.fixed)

    def test_materialize_is_blocking_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            output = fixture.root / "quality-docket"
            synthetic_builder = fixture.root / "skill_benchmark/scripts/build_rq2b_v7_phase8_quality_gate_docket.py"
            synthetic_builder.parent.mkdir(parents=True, exist_ok=True)
            synthetic_builder.write_text("QUALITY_BUILDER_VERSION = 'synthetic'\n", encoding="utf-8")
            contexts = fixture.context()
            with contexts[0], contexts[1], contexts[2], contexts[3], contexts[4], contexts[5], contexts[6], contexts[7]:
                report = builder.materialize(fixture.root, output, builder_path=synthetic_builder)
                self.assertEqual(report["quality_pass_reports_emitted"], 0)
                self.assertFalse(report["formal_execution_ready"])
                with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                    builder.materialize(fixture.root, output, builder_path=synthetic_builder)

    def test_prompt_dependency_identity_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp))
            path = fixture.root / fixture.fixed["dependency_ledger"].path
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            rows[0]["prompt_sha256"] = "0" * 64
            write_jsonl(path, rows)
            fixture.fixed["dependency_ledger"] = builder.FixedArtifact(fixture.fixed["dependency_ledger"].path, builder.file_sha256(path))
            analysis_path = fixture.root / fixture.fixed["analysis_freeze"].path
            analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
            analysis["artifacts"]["dependency_ledger.jsonl"]["sha256"] = fixture.fixed["dependency_ledger"].sha256
            write_json(analysis_path, analysis)
            fixture.fixed["analysis_freeze"] = builder.FixedArtifact(fixture.fixed["analysis_freeze"].path, builder.file_sha256(analysis_path))
            contexts = fixture.context()
            with contexts[0], contexts[1], contexts[2], contexts[3], contexts[4], contexts[5], contexts[6], contexts[7]:
                with self.assertRaisesRegex(ValueError, "prompt binding drift"):
                    builder.audit_canonical(fixture.root, fixture.fixed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
