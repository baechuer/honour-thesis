#!/usr/bin/env python3
"""Focused no-inference tests for the V7 Phase-8 B1 dispatch builder."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import build_rq2b_v7_phase8_b1_dispatch as builder


APPROVAL_REL = Path(
    "skill_benchmark/rq2b_naturalistic_confusability/preparation/"
    "v7_phase8_b1_dispatch_builder_2026_09_09_v1/approval_record.pending.json"
)


def expect_failure(callable_: Any, fragment: str) -> None:
    try:
        callable_()
    except ValueError as error:
        if fragment not in str(error):
            raise AssertionError(f"Wrong failure: {error}") from error
    else:
        raise AssertionError(f"Expected failure containing: {fragment}")


def synthetic_representations() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
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


def approval_test(root: Path) -> None:
    approval_path = root / APPROVAL_REL
    pending = json.loads(approval_path.read_text(encoding="utf-8"))
    assert pending["decision"] == "PENDING_CAPTURE_FROM_AUTHORISED_PARENT_TASK"
    expect_failure(
        lambda: builder.validate_approval(root, approval_path),
        "Execution has not been explicitly approved",
    )


def payload_shape_test(root: Path) -> None:
    receipt_path = root / APPROVAL_REL
    representations = synthetic_representations()
    bm25 = builder.build_bm25_payload(
        root=root,
        receipt_path=receipt_path,
        representations=representations,
    )
    skillrouter = builder.build_skillrouter_payload(
        root=root,
        receipt_path=receipt_path,
        representations=representations,
    )
    assert bm25["schema_version"] == builder.RUNNER_SPECS["bm25_b1"]["payload_schema"]
    assert skillrouter["schema_version"] == builder.RUNNER_SPECS["skillrouter_embedding_b1"]["payload_schema"]
    assert bm25["state"] == skillrouter["state"] == "SEALED_LABEL_FREE_PHASE8_PAYLOAD"
    assert bm25["inputs"]["representations"] == representations
    assert skillrouter["inputs"]["representations"] == representations
    assert bm25["counts"]["b1_output_rows"] == skillrouter["counts"]["b1_output_rows"] == 4308
    assert bm25["isolation"]["labels_or_results_read"] is False
    assert skillrouter["label_isolation"]["labels_or_results_read"] is False


def deterministic_release_policy_test(root: Path) -> None:
    root_sha = "b" * 64
    with tempfile.TemporaryDirectory(dir=root / "skill_benchmark/cache") as directory:
        payload_path = Path(directory) / "payload.json"
        preflight_path = Path(directory) / "preflight.json"
        payload_path.write_text("{}\n", encoding="utf-8")
        preflight_path.write_text("{}\n", encoding="utf-8")
        phase8 = {
            "receipt": {"sha256": "c" * 64},
            "root_manifest": {"sha256": root_sha},
        }
        qwen_payload = {
            "phase8": phase8,
            "predictable_ceilings": {
                key: 17
                for key in __import__(
                    "build_rq2b_v7_qwen_b1_phase8_v3_preflight"
                ).PREDICTABLE_CEILING_KEYS
            },
        }
        qwen = builder.build_qwen_release(
            root=root,
            root_sha256=root_sha,
            payload_path=payload_path,
            preflight_path=preflight_path,
            payload=qwen_payload,
            timeout_seconds=120,
        )
        assert qwen["one_use"] is True and qwen["consumed"] is False
        assert qwen["ceilings"]["maximum_provider_reported_total_tokens"] == 34
        assert qwen["provider"]["automatic_retries"] == 0
        assert qwen["destinations"]["output_dir"].startswith(builder.cache_prefix(root_sha))

        bm25_payload = {"phase8": {"receipt": {"sha256": "c" * 64}}}
        bm25 = builder.build_bm25_release(
            root=root,
            root_sha256=root_sha,
            payload_path=payload_path,
            payload=bm25_payload,
        )
        assert bm25["ceilings"] == {
            "maximum_queries": 1077,
            "maximum_sources": 3798,
            "maximum_output_rows": 4308,
            "maximum_ranked_candidates": 430800,
            "maximum_wall_time_seconds": builder.BM25_WALL_SECONDS,
        }
        assert bm25["root_release_id"] == builder.deterministic_ids(root_sha, "bm25_b1")["root_release_id"]


def incomplete_root_gate_test(root: Path) -> None:
    with tempfile.TemporaryDirectory(dir=root / "skill_benchmark/cache") as directory:
        receipt = Path(directory) / "incomplete_phase8.json"
        receipt.write_text("{}\n", encoding="utf-8")
        expect_failure(
            lambda: builder.validate_phase8(root, receipt),
            "Phase-8 receipt schema drift",
        )


def implementation_boundary_test(root: Path) -> None:
    source = (root / "skill_benchmark/scripts/build_rq2b_v7_phase8_b1_dispatch.py").read_text(
        encoding="utf-8"
    )
    assert "urllib.request" not in source
    assert ".urlopen(" not in source
    assert "run_preflight(" in source
    for role, expected in builder.RUNNER_SPECS.items():
        path = root / expected["path"]
        constants = builder.literal_constants(path)
        assert constants["RUNNER_VERSION"] == expected["runner_version"], role
        assert constants["PAYLOAD_SCHEMA"] == expected["payload_schema"], role
        assert constants["AUTHORISATION_SCHEMA"] == expected["authorisation_schema"], role


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    self_test = builder.self_test()
    approval_test(root)
    payload_shape_test(root)
    deterministic_release_policy_test(root)
    incomplete_root_gate_test(root)
    implementation_boundary_test(root)
    print(json.dumps({
        "status": "PASS_PHASE8_B1_DISPATCH_BUILDER_FOCUSED_NO_INFERENCE_TESTS",
        "builder_self_test": self_test["status"],
        "network_calls": 0,
        "provider_calls": 0,
        "model_forwards": 0,
        "checks": {
            "explicit_approval_required": True,
            "incomplete_phase8_root_fails_closed": True,
            "three_runner_literals_bound": True,
            "bm25_and_skillrouter_payload_shapes": True,
            "deterministic_release_identity": True,
            "bounded_ceiling_policy": True,
            "no_provider_client_in_builder": True,
        },
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
