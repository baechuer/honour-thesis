#!/usr/bin/env python3
"""Focused no-inference tests for the V7 Phase-8 B2 dispatch builder."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import build_rq2b_v7_phase8_b2_dispatch as builder


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / (
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_b2_dispatch_builder_2026_09_09_v1"
)


def expected_official_report() -> dict[str, object]:
    return {
        "status": "PASS_LABEL_FREE_RUNNER_OUTPUT_VALIDATION",
        "queries": builder.EXPECTED_QUERIES,
        "b1_cells": builder.EXPECTED_B1_CELLS,
        "b2_materialised_conditions": builder.EXPECTED_B2_MATERIALISED_CONDITIONS,
        "outcome_conditions": builder.EXPECTED_CORE_OUTCOMES + builder.EXPECTED_DIAGNOSTIC_OUTCOMES,
        "b1_rows": builder.EXPECTED_B1_ROWS,
        "b2_rows": 0,
        "c2_alias_rows": 0,
        "complete_scope_required": False,
    }


def synthetic_representations() -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for representation, (_, protocol) in {
        **builder.I1_I2_ROOT_ROLES,
        **builder.I3_ROOT_ROLES,
    }.items():
        result[representation] = {
            "path": f"synthetic/{representation}.jsonl",
            "sha256": "a" * 64,
            "rows": builder.EXPECTED_SOURCES,
            "phase8_final": True,
            "extraction_protocol": protocol,
        }
    return result


class Phase8B2DispatchBuilderTests(unittest.TestCase):
    def test_self_test_is_no_inference(self) -> None:
        report = builder.self_test()
        self.assertEqual(
            report["status"],
            "PASS_PHASE8_B2_DISPATCH_BUILDER_SYNTHETIC_NO_INFERENCE",
        )
        self.assertEqual(report["network_calls"], 0)
        self.assertEqual(report["provider_calls"], 0)
        self.assertEqual(report["model_loads"], 0)
        self.assertEqual(report["model_forwards"], 0)

    def test_pending_approval_is_fail_closed(self) -> None:
        path = PACKAGE / "approval_record.pending.json"
        with self.assertRaisesRegex(ValueError, "has not been explicitly approved"):
            builder.validate_approval(ROOT, path)

    def test_payloads_reuse_runner_native_contracts(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "skill_benchmark/cache") as raw:
            receipt_path = Path(raw) / "b1_receipt.json"
            receipt_path.write_text("{}\n", encoding="utf-8")
            phase8_path = Path(raw) / "phase8.json"
            phase8_path.write_text("{}\n", encoding="utf-8")
            b1_receipt = {
                "b1_artifacts": [{"path": "synthetic/b1.jsonl", "sha256": "b" * 64, "rows": builder.EXPECTED_B1_ROWS}],
            }
            qwen = builder.build_payload(
                root=ROOT,
                role="qwen_reranker_b2",
                phase8_receipt_path=phase8_path,
                representations=synthetic_representations(),
                b1_receipt_path=receipt_path,
                b1_receipt=b1_receipt,
            )
            skillrouter = builder.build_payload(
                root=ROOT,
                role="skillrouter_reranker_b2",
                phase8_receipt_path=phase8_path,
                representations=synthetic_representations(),
                b1_receipt_path=receipt_path,
                b1_receipt=b1_receipt,
            )
        self.assertEqual(qwen["schema_version"], builder.RUNNER_SPECS["qwen_reranker_b2"]["payload_schema"])
        self.assertEqual(skillrouter["schema_version"], builder.RUNNER_SPECS["skillrouter_reranker_b2"]["payload_schema"])
        self.assertEqual(qwen["counts"]["materialised_b2_rows"], 15 * 1077)
        self.assertEqual(skillrouter["counts"]["materialised_b2_rows"], 15 * 1077)
        self.assertEqual(qwen["counts"]["c2_q_alias_rows"], 0)
        self.assertEqual(skillrouter["counts"]["c2_s_alias_rows"], 0)
        self.assertEqual(qwen["b1_validation"]["condition_ids"], list(builder.B1_CONDITIONS))
        self.assertFalse(qwen["label_isolation"]["b1_candidates_regenerated"])
        self.assertFalse(skillrouter["label_isolation"]["offline_scorer_run"])

    def test_fresh_b1_receipt_replays_current_validator_binding(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "skill_benchmark/cache") as raw:
            directory = Path(raw)
            phase8 = directory / "phase8.json"
            root_manifest = directory / "root.json"
            b1_artifact = directory / "b1.jsonl"
            receipt_path = directory / "receipt.json"
            phase8.write_text('{"phase8":true}\n', encoding="utf-8")
            root_manifest.write_text('{"root":true}\n', encoding="utf-8")
            b1_artifact.write_text('{}\n', encoding="utf-8")
            artifacts = [{
                "path": builder.relative(b1_artifact, ROOT),
                "sha256": builder.file_sha256(b1_artifact),
                "rows": builder.EXPECTED_B1_ROWS,
            }]
            receipt = {
                "schema_version": builder.B1_RECEIPT_SCHEMA,
                "status": "PASS_FRESH_OFFICIAL_LABEL_FREE_B1_VALIDATION",
                "phase8": {
                    "receipt": {"path": builder.relative(phase8, ROOT), "sha256": builder.file_sha256(phase8)},
                    "root_manifest": {"path": builder.relative(root_manifest, ROOT), "sha256": builder.file_sha256(root_manifest)},
                },
                "official_validator": builder.implementation_binding(ROOT, builder.VALIDATOR_REL),
                "b1_artifacts": artifacts,
                "b1_artifacts_bundle_sha256": builder.canonical_sha256(artifacts),
                "condition_ids": list(builder.B1_CONDITIONS),
                "b1_cells": builder.EXPECTED_B1_CELLS,
                "b1_rows": builder.EXPECTED_B1_ROWS,
                "official_report": expected_official_report(),
                "validation_mode": "CURRENT_VALIDATOR_REPLAY_COMPLETE_B1_WITH_EMPTY_B2",
                "validated_at_utc": "2026-09-09T00:00:00Z",
                "label_isolation": {
                    "label_files_read": False,
                    "acceptable_sets_read": False,
                    "b2_results_read": False,
                    "offline_scorer_run": False,
                },
            }
            receipt_path.write_text(json.dumps(receipt) + "\n", encoding="utf-8")
            with mock.patch.object(
                builder,
                "_official_b1_replay",
                return_value=(expected_official_report(), [{}]),
            ):
                validated, rows = builder.validate_b1_receipt(
                    ROOT,
                    receipt_path,
                    phase8_receipt_path=phase8,
                    root_manifest_path=root_manifest,
                )
                self.assertEqual(validated["b1_rows"], builder.EXPECTED_B1_ROWS)
                self.assertEqual(rows, [{}])
                drifted = dict(receipt)
                drifted["b1_artifacts_bundle_sha256"] = "f" * 64
                receipt_path.unlink()
                receipt_path.write_text(json.dumps(drifted) + "\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "bundle hash drift"):
                    builder.validate_b1_receipt(
                        ROOT,
                        receipt_path,
                        phase8_receipt_path=phase8,
                        root_manifest_path=root_manifest,
                    )

    def test_release_identity_and_namespaces_are_deterministic_and_distinct(self) -> None:
        root_sha = "1" * 64
        b1_sha = "2" * 64
        qwen = builder.deterministic_ids(root_sha, b1_sha, "qwen_reranker_b2")
        skillrouter = builder.deterministic_ids(root_sha, b1_sha, "skillrouter_reranker_b2")
        self.assertNotEqual(qwen["root_release_id"], skillrouter["root_release_id"])
        self.assertEqual(qwen, builder.deterministic_ids(root_sha, b1_sha, "qwen_reranker_b2"))
        prefix = builder.cache_prefix(root_sha, b1_sha)
        destinations = {
            f"{prefix}/qwen/output",
            f"{prefix}/qwen/attempt",
            f"{prefix}/skillrouter/output",
            f"{prefix}/skillrouter/score_cache",
            f"{prefix}/skillrouter/attempt",
        }
        self.assertEqual(len(destinations), 5)
        self.assertTrue(all(path.startswith("skill_benchmark/cache/") for path in destinations))

    def test_one_use_releases_bind_the_exact_execution_approval(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "skill_benchmark/cache") as raw:
            directory = Path(raw)
            payload_path = directory / "payload.json"
            pending_path = directory / "pending.json"
            preflight_path = directory / "preflight.json"
            approval_path = directory / "approval.json"
            for path in (payload_path, pending_path, preflight_path):
                path.write_text("{}\n", encoding="utf-8")
            approval = {
                "schema_version": builder.APPROVAL_SCHEMA,
                "decision": "APPROVED",
                "scope": {
                    "frozen_library": "V7_3798_SOURCES_1077_QUERIES",
                    "experiment": "B36_CORE_PLUS_C6_DIAGNOSTIC",
                    "phase8_b2_prerequisite": True,
                    "external_qwen_reranker": True,
                    "local_skillrouter_reranker": True,
                },
                "secrets_recorded": False,
                "user_instruction": {"verbatim": "批准36个核心配置+6个诊断"},
            }
            approval_path.write_text(json.dumps(approval) + "\n", encoding="utf-8")
            payload = {
                "phase8": {"receipt": {"sha256": "3" * 64}},
                "b1_validation": {"receipt": {"sha256": "4" * 64}},
            }
            qwen = builder.build_qwen_release(
                root=ROOT,
                payload_path=payload_path,
                payload=payload,
                pending_path=pending_path,
                preflight_path=preflight_path,
                ceilings={},
                destinations={"output_dir": "skill_benchmark/cache/qwen-out", "attempt_dir": "skill_benchmark/cache/qwen-attempt"},
                root_sha="1" * 64,
                b1_receipt_sha="2" * 64,
                approval_path=approval_path,
                approval=approval,
            )
            skillrouter = builder.build_skillrouter_release(
                root=ROOT,
                payload_path=payload_path,
                payload=payload,
                preflight={"model_snapshot": {}, "runtime": {}, "ceilings": {}},
                destinations={"output_dir": "skill_benchmark/cache/sr-out", "cache_dir": "skill_benchmark/cache/sr-cache", "attempt_dir": "skill_benchmark/cache/sr-attempt"},
                root_sha="1" * 64,
                b1_receipt_sha="2" * 64,
                approval_path=approval_path,
                approval=approval,
            )
            expected = {
                "path": builder.relative(approval_path, ROOT),
                "sha256": builder.file_sha256(approval_path),
                "decision": "APPROVED",
                "scope": approval["scope"],
            }
        self.assertEqual(qwen["approval"], expected)
        self.assertEqual(skillrouter["approval"], expected)

    def test_qwen_predictable_ceilings_are_exact_and_zero_retry_compatible(self) -> None:
        counts = {
            "requests": 19,
            "documents": 311,
            "proxy_tokens": 123_456,
            "utf8_bytes": 789_012,
        }
        ceilings = builder.qwen_ceilings(counts)
        self.assertEqual(ceilings["maximum_request_attempts"], counts["requests"])
        self.assertEqual(ceilings["maximum_successful_calls"], counts["requests"])
        self.assertEqual(ceilings["maximum_external_documents"], counts["documents"])
        self.assertEqual(ceilings["maximum_external_submission_proxy_tokens"], counts["proxy_tokens"])
        self.assertEqual(ceilings["maximum_external_submission_utf8_bytes"], counts["utf8_bytes"])
        self.assertEqual(ceilings["maximum_provider_total_tokens"], counts["proxy_tokens"] * 2)

    def test_runner_literals_and_implementation_boundary(self) -> None:
        source = (ROOT / "skill_benchmark/scripts/build_rq2b_v7_phase8_b2_dispatch.py").read_text(encoding="utf-8")
        self.assertNotIn("urllib.request", source)
        self.assertNotIn(".urlopen(", source)
        self.assertNotIn("AutoModel", source)
        self.assertNotIn("offline_label_adapter", source)
        self.assertNotIn("reviewed_confusable_neighbour", source)
        for role, expected in builder.RUNNER_SPECS.items():
            constants = builder.literal_constants(ROOT / expected["path"])
            self.assertEqual(constants["RUNNER_VERSION"], expected["runner_version"], role)
            self.assertEqual(constants["PAYLOAD_SCHEMA"], expected["payload_schema"], role)
            self.assertEqual(constants["AUTHORISATION_SCHEMA"], expected["authorisation_schema"], role)


if __name__ == "__main__":
    unittest.main(verbosity=2)
