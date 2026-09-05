#!/usr/bin/env python3
"""Offline regression tests for RQ2a evidence roles and stage gates."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from analyze_rq2a_matched_content import load_complete_runs
from build_rq2a_cost_ledger import run_role
from freeze_rq2a_confirmatory_protocol import (
    aggregation_choice_provenance_errors,
    load_full_development_rows,
    safety_amendment_errors,
)
from rq2a_selector_common import (
    CONFIRMATORY_FREEZE_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    RESULT_SCHEMA_VERSION,
    SERIALISER_VERSION,
    sha256_file,
    validate_confirmatory_freeze_manifest,
    write_json_atomic,
)


def write_run(
    root: Path,
    run_id: str,
    *,
    evidence_role: str | None,
) -> Path:
    run_dir = root / run_id
    run_dir.mkdir(parents=True)
    row = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "run_id": run_id,
        "split": "development",
        "selector": "bm25",
        "representation": "shared-only",
        "prompt_id": "prompt-1",
        "cluster_id": "cluster-1",
    }
    rows_path = run_dir / "rows.jsonl"
    rows_path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "rq2a-run-manifest-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "run_id": run_id,
        "state": "complete",
        "split": "development",
        "clusters_per_field": None,
        "output_artifacts": {
            "rows_jsonl": {
                "path": str(rows_path),
                "row_count": 1,
                "sha256": sha256_file(rows_path),
            }
        },
    }
    if evidence_role is not None:
        manifest["evidence_role"] = evidence_role
    write_json_atomic(run_dir / "manifest.json", manifest)
    return run_dir


def test_confirmatory_freeze_integrity(root: Path) -> None:
    input_dir = root / "frozen-input"
    representation_dir = input_dir / "representations"
    representation_dir.mkdir(parents=True)
    protocol_path = input_dir / "protocol.json"
    protocol_path.write_text("{}\n", encoding="utf-8")
    representation_path = representation_dir / "shared-only.jsonl"
    representation_path.write_text("{}\n", encoding="utf-8")
    implementation_path = root / "implementation.py"
    implementation_path.write_text("pass\n", encoding="utf-8")
    choice_path = root / "aggregation_choice.json"
    write_json_atomic(
        choice_path,
        {
            "state": "frozen_development_choice",
            "selected_selector": "qwen-field-aware-uniform-top-two",
        },
    )
    analysis_path = root / "development_analysis.json"
    analysis_path.write_text("{}\n", encoding="utf-8")
    development_dir = root / "development-primary"
    development_dir.mkdir()
    development_rows_path = development_dir / "rows.jsonl"
    development_rows_path.write_text('{"row": 1}\n', encoding="utf-8")
    development_manifest_path = development_dir / "manifest.json"
    write_json_atomic(
        development_manifest_path,
        {"run_id": "development-primary"},
    )
    output_dir = root / "confirmatory"
    freeze_path = root / "confirmatory_freeze_manifest.json"
    write_json_atomic(
        freeze_path,
        {
            "schema_version": CONFIRMATORY_FREEZE_SCHEMA_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "serialiser_version": SERIALISER_VERSION,
            "state": "frozen_before_confirmatory",
            "input_artifacts": {
                str(protocol_path): sha256_file(protocol_path),
            },
            "implementation_sha256": {
                str(implementation_path): sha256_file(implementation_path),
            },
            "representation_sha256": {
                "shared-only": sha256_file(representation_path),
            },
            "aggregation_choice": {
                "path": str(choice_path),
                "sha256": sha256_file(choice_path),
                "selected_selector": "qwen-field-aware-uniform-top-two",
            },
            "development_analysis": {
                "path": str(analysis_path),
                "sha256": sha256_file(analysis_path),
            },
            "development_runs": [
                {
                    "run_id": "development-primary",
                    "manifest_path": str(development_manifest_path),
                    "manifest_sha256": sha256_file(development_manifest_path),
                    "rows_path": str(development_rows_path),
                    "rows_sha256": sha256_file(development_rows_path),
                }
            ],
            "confirmatory_output_root": str(output_dir),
        },
    )
    validated = validate_confirmatory_freeze_manifest(
        freeze_path,
        input_dir=input_dir,
        output_dir=output_dir,
    )
    assert validated["state"] == "frozen_before_confirmatory"

    development_rows_path.write_text('{"row": 2}\n', encoding="utf-8")
    try:
        validate_confirmatory_freeze_manifest(
            freeze_path,
            input_dir=input_dir,
            output_dir=output_dir,
        )
    except ValueError as exc:
        assert "development-primary rows hash mismatch" in str(exc)
    else:
        raise AssertionError("Freeze validation accepted changed development rows")
    development_rows_path.write_text('{"row": 1}\n', encoding="utf-8")

    implementation_path.write_text("changed = True\n", encoding="utf-8")
    try:
        validate_confirmatory_freeze_manifest(
            freeze_path,
            input_dir=input_dir,
            output_dir=output_dir,
        )
    except ValueError as exc:
        assert "implementation hash mismatch" in str(exc)
    else:
        raise AssertionError("Freeze validation accepted changed implementation")


def test_aggregation_choice_provenance(root: Path) -> None:
    run_dir = root / "field-aware-primary"
    run_dir.mkdir()
    choice = {
        "state": "frozen_development_choice",
        "run_id": "field-aware-primary",
        "selected_aggregation": "uniform-top-two",
        "selected_selector": "qwen-field-aware-uniform-top-two",
        "candidates": [
            {"selector": "qwen-field-aware-maximum"},
            {"selector": "qwen-field-aware-uniform-top-two"},
        ],
    }
    choice_path = run_dir / "aggregation_choice.json"
    write_json_atomic(choice_path, choice)
    manifest_path = run_dir / "manifest.json"
    write_json_atomic(
        manifest_path,
        {
            "run_id": "field-aware-primary",
            "aggregations": ["maximum", "uniform-top-two"],
            "aggregation_choice": choice,
            "output_artifacts": {
                "aggregation_choice_json": {
                    "path": str(choice_path),
                    "sha256": sha256_file(choice_path),
                }
            },
        },
    )
    development_runs = [{"manifest_path": str(manifest_path)}]
    by_condition: dict[tuple[str, str], dict[str, dict[str, object]]] = {}
    for selector in (
        "qwen-field-aware-maximum",
        "qwen-field-aware-uniform-top-two",
    ):
        selected = selector == "qwen-field-aware-uniform-top-two"
        by_condition[(selector, "same-facts-fielded")] = {
            f"prompt-{index}": {
                "prompt_id": f"prompt-{index}",
                "cluster_id": f"cluster-{index % 70}",
                "is_selected_aggregation": selected,
                "aggregation_choice_state": "frozen_development_choice",
            }
            for index in range(150)
        }
    assert aggregation_choice_provenance_errors(
        choice_path,
        choice,
        development_runs,
        by_condition,
    ) == []

    copied_choice = root / "copied_choice.json"
    copied_choice.write_bytes(choice_path.read_bytes())
    errors = aggregation_choice_provenance_errors(
        copied_choice,
        choice,
        development_runs,
        by_condition,
    )
    assert any("not the canonical" in error for error in errors)


def test_safety_amendment_boundaries() -> None:
    v1 = {
        "schema_version": "rq2a-confirmatory-safety-amendment-v1",
        "state": "approved_for_pre_execution_safety_hardening",
        "scientific_state": {
            "confirmatory_scores_read": False,
            "confirmatory_external_requests": 0,
            "expected_condition_count": 22,
        },
    }
    assert safety_amendment_errors(v1) == []

    v2 = {
        "schema_version": "rq2a-confirmatory-safety-amendment-v2",
        "state": "approved_for_post_authorisation_safety_repair",
        "scientific_state": {
            "confirmatory_output_root_empty": True,
            "confirmatory_results_scientifically_interpreted": False,
            "confirmatory_external_requests": 0,
            "confirmatory_provider_tokens": 0,
            "expected_condition_count": 22,
        },
    }
    assert safety_amendment_errors(v2) == []
    v2["scientific_state"]["confirmatory_provider_tokens"] = 1
    assert "Confirmatory safety amendment boundary mismatch" in (
        safety_amendment_errors(v2)
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="rq2a-stage-gates-") as raw:
        root = Path(raw)
        primary = write_run(root, "primary", evidence_role="primary")
        verification = write_run(
            root, "verification", evidence_role="verification"
        )
        by_condition, manifests, smoke, skipped_verification = (
            load_full_development_rows(root)
        )
        assert len(by_condition[("bm25", "shared-only")]) == 1
        assert [row["run_id"] for row in manifests] == ["primary"]
        assert smoke == []
        assert skipped_verification == ["verification"]

        rows, loaded_manifests, split = load_complete_runs(
            [primary],
            allow_confirmatory=False,
            confirmatory_freeze_manifest=None,
        )
        assert len(rows) == 1
        assert len(loaded_manifests) == 1
        assert split == "development"
        try:
            load_complete_runs(
                [verification],
                allow_confirmatory=False,
                confirmatory_freeze_manifest=None,
            )
        except ValueError as exc:
            assert "accepts only primary evidence" in str(exc)
        else:
            raise AssertionError("Verification evidence entered formal analysis")

        assert run_role({"clusters_per_field": 1}) == "smoke"
        assert (
            run_role(
                {"clusters_per_field": None, "evidence_role": "verification"}
            )
            == "verification"
        )
        assert run_role({"clusters_per_field": None}) == "primary"

        test_confirmatory_freeze_integrity(root)
        test_aggregation_choice_provenance(root)
        test_safety_amendment_boundaries()

    print("RQ2a stage gate tests: PASS")


if __name__ == "__main__":
    main()
