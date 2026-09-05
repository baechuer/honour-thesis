#!/usr/bin/env python3
"""Audit RQ2a development completion and freeze confirmatory inputs/settings."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    PROTOCOL_VERSION,
    SERIALISER_VERSION,
    read_jsonl,
    repo_root,
    sha256_file,
    utc_timestamp,
    write_json_atomic,
)


ALL_REPRESENTATIONS = [
    "shared-only",
    "same-facts-fielded",
    "same-facts-flat",
    "same-facts-prose",
    "same-facts-order-controlled",
    "same-facts-diluted-1x",
    "same-facts-diluted-2x",
    "same-facts-diluted-4x",
]
CORE_REPRESENTATIONS = [
    "shared-only",
    "same-facts-fielded",
    "same-facts-flat",
    "same-facts-prose",
    "same-facts-diluted-2x",
]
FIELD_AWARE_SELECTORS = {
    "qwen-field-aware-maximum",
    "qwen-field-aware-uniform-top-two",
}


def expected_conditions(
    frozen_field_aware_selector: str | None,
) -> set[tuple[str, str]]:
    conditions = {
        (selector, representation)
        for selector in ("bm25", "qwen-single-vector")
        for representation in ALL_REPRESENTATIONS
    }
    conditions.update(
        {
            ("skillrouter-cross-encoder", representation)
            for representation in CORE_REPRESENTATIONS
        }
    )
    if frozen_field_aware_selector:
        conditions.add(
            (frozen_field_aware_selector, "same-facts-fielded")
        )
    return conditions


def load_full_development_rows(
    development_root: Path,
) -> tuple[
    dict[tuple[str, str], dict[str, dict[str, Any]]],
    list[dict[str, Any]],
    list[str],
    list[str],
]:
    by_condition: dict[
        tuple[str, str],
        dict[str, dict[str, Any]],
    ] = defaultdict(dict)
    manifests: list[dict[str, Any]] = []
    skipped_smoke_runs: list[str] = []
    skipped_verification_runs: list[str] = []
    for manifest_path in sorted(development_root.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        run_dir = manifest_path.parent
        if manifest.get("split") != "development":
            continue
        if manifest.get("clusters_per_field") is not None:
            skipped_smoke_runs.append(manifest["run_id"])
            continue
        evidence_role = manifest.get("evidence_role", "primary")
        if evidence_role == "verification":
            skipped_verification_runs.append(manifest["run_id"])
            continue
        if evidence_role != "primary":
            raise ValueError(
                f"{run_dir}: unsupported evidence_role {evidence_role!r}"
            )
        rows_path = run_dir / "rows.jsonl"
        if not rows_path.exists():
            raise FileNotFoundError(f"{run_dir}: rows.jsonl is missing")
        if (
            manifest.get("output_artifacts", {})
            .get("rows_jsonl", {})
            .get("sha256")
            != sha256_file(rows_path)
        ):
            raise ValueError(f"{run_dir}: rows hash mismatch")
        manifest_record = {
            "run_id": manifest["run_id"],
            "manifest_path": str(manifest_path),
            "manifest_sha256": sha256_file(manifest_path),
            "rows_path": str(rows_path),
            "rows_sha256": sha256_file(rows_path),
        }
        manifests.append(manifest_record)
        for row in read_jsonl(rows_path):
            key = (row["selector"], row["representation"])
            prompt_id = row["prompt_id"]
            if prompt_id in by_condition[key]:
                raise ValueError(
                    f"Duplicate full-development row for {key}/{prompt_id}"
                )
            by_condition[key][prompt_id] = row
    return (
        by_condition,
        manifests,
        skipped_smoke_runs,
        skipped_verification_runs,
    )


def aggregation_choice_provenance_errors(
    aggregation_choice_path: Path,
    aggregation_choice: dict[str, Any],
    development_runs: list[dict[str, Any]],
    by_condition: dict[
        tuple[str, str],
        dict[str, dict[str, Any]],
    ],
) -> list[str]:
    """Prove the frozen choice came from one canonical primary development run."""
    errors: list[str] = []
    selected_selector = aggregation_choice.get("selected_selector")
    candidate_selectors = {
        row.get("selector")
        for row in aggregation_choice.get("candidates", [])
        if isinstance(row, dict)
    }
    if selected_selector not in FIELD_AWARE_SELECTORS:
        errors.append("Frozen field-aware selector is not preregistered")
    if candidate_selectors != FIELD_AWARE_SELECTORS:
        errors.append(
            "Aggregation choice did not compare both preregistered selectors"
        )

    field_aware_runs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for record in development_runs:
        manifest_path = Path(record["manifest_path"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("aggregations") is not None:
            field_aware_runs.append((record, manifest))
    if len(field_aware_runs) != 1:
        errors.append(
            "Expected exactly one canonical primary field-aware development run; "
            f"found {len(field_aware_runs)}"
        )
        return errors

    record, manifest = field_aware_runs[0]
    canonical_choice_path = (
        Path(record["manifest_path"]).parent / "aggregation_choice.json"
    )
    if not canonical_choice_path.exists():
        errors.append("Canonical field-aware aggregation_choice.json is missing")
        return errors
    if canonical_choice_path.resolve() != aggregation_choice_path.resolve():
        errors.append(
            "Supplied aggregation choice is not the canonical primary run artifact"
        )
    if sha256_file(canonical_choice_path) != sha256_file(
        aggregation_choice_path
    ):
        errors.append("Supplied and canonical aggregation-choice hashes differ")
    if manifest.get("aggregation_choice") != aggregation_choice:
        errors.append(
            "Aggregation choice differs from the canonical run manifest"
        )
    if aggregation_choice.get("run_id") != manifest.get("run_id"):
        errors.append("Aggregation choice run ID does not match its manifest")
    artifact = (
        manifest.get("output_artifacts", {})
        .get("aggregation_choice_json", {})
    )
    if artifact.get("sha256") != sha256_file(canonical_choice_path):
        errors.append(
            "Canonical run manifest does not hash its aggregation choice"
        )

    for selector in sorted(FIELD_AWARE_SELECTORS):
        rows = by_condition.get((selector, "same-facts-fielded"), {})
        cluster_count = len({row["cluster_id"] for row in rows.values()})
        if len(rows) != 150 or cluster_count != 70:
            errors.append(
                f"{selector}: aggregation comparison has {len(rows)} prompts/"
                f"{cluster_count} clusters instead of 150/70"
            )
            continue
        expected_selected = selector == selected_selector
        for row in rows.values():
            if row.get("is_selected_aggregation") is not expected_selected:
                errors.append(
                    f"{selector}: selected-aggregation row flags are inconsistent"
                )
                break
            if (
                row.get("aggregation_choice_state")
                != "frozen_development_choice"
            ):
                errors.append(
                    f"{selector}: row aggregation choice is not frozen"
                )
                break
    return errors


def safety_amendment_errors(amendment: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    amendment_identity = (
        amendment.get("schema_version"),
        amendment.get("state"),
    )
    pre_execution_v1 = amendment_identity == (
        "rq2a-confirmatory-safety-amendment-v1",
        "approved_for_pre_execution_safety_hardening",
    )
    post_authorisation_v2 = amendment_identity == (
        "rq2a-confirmatory-safety-amendment-v2",
        "approved_for_post_authorisation_safety_repair",
    )
    if not (pre_execution_v1 or post_authorisation_v2):
        errors.append("Confirmatory safety amendment is invalid")
    scientific = amendment.get("scientific_state", {})
    common_boundary_passes = (
        scientific.get("confirmatory_external_requests") == 0
        and scientific.get("expected_condition_count") == 22
    )
    pre_execution_boundary_passes = (
        scientific.get("confirmatory_scores_read") is False
    )
    post_authorisation_boundary_passes = (
        scientific.get("confirmatory_output_root_empty") is True
        and scientific.get("confirmatory_results_scientifically_interpreted")
        is False
        and scientific.get("confirmatory_provider_tokens") == 0
    )
    if not common_boundary_passes or (
        pre_execution_v1 and not pre_execution_boundary_passes
    ) or (
        post_authorisation_v2
        and not post_authorisation_boundary_passes
    ):
        errors.append("Confirmatory safety amendment boundary mismatch")
    return errors


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=root / "rq2a_matched_content",
    )
    parser.add_argument(
        "--development-root",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "development",
    )
    parser.add_argument(
        "--confirmatory-root",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "confirmatory",
    )
    parser.add_argument("--aggregation-choice", type=Path)
    parser.add_argument("--development-analysis", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            root
            / "rq2a_matched_content"
            / "confirmatory_freeze_manifest.json"
        ),
    )
    parser.add_argument(
        "--freeze",
        action="store_true",
        help="Write the immutable freeze manifest only if every gate passes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    protocol_path = args.input_dir / "protocol.json"
    validation_path = args.input_dir / "validation_report.json"
    length_audit_path = args.input_dir / "selector_length_audit.json"
    analysis_spec_path = args.input_dir / "analysis_spec.json"
    safety_amendment_path = (
        args.input_dir / "confirmatory_safety_amendment.json"
    )
    required_artifacts = [
        protocol_path,
        validation_path,
        length_audit_path,
        analysis_spec_path,
        safety_amendment_path,
    ]
    for path in required_artifacts:
        if not path.exists():
            errors.append(f"Missing required artifact: {path}")

    protocol: dict[str, Any] = {}
    if protocol_path.exists():
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        if protocol.get("protocol_version") != PROTOCOL_VERSION:
            errors.append("Protocol version mismatch")
        if protocol.get("serialiser_version") != SERIALISER_VERSION:
            errors.append("Serialiser version mismatch")
    if validation_path.exists():
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if str(validation.get("status", "")).lower() != "pass":
            errors.append("Representation validation is not PASS")
    if length_audit_path.exists():
        length_audit = json.loads(
            length_audit_path.read_text(encoding="utf-8")
        )
        if length_audit.get("status") != "pass":
            errors.append("Selector length audit is not PASS")
    if safety_amendment_path.exists():
        amendment = json.loads(
            safety_amendment_path.read_text(encoding="utf-8")
        )
        errors.extend(safety_amendment_errors(amendment))

    frozen_field_aware_selector: str | None = None
    aggregation_choice: dict[str, Any] | None = None
    if args.aggregation_choice is None or not args.aggregation_choice.exists():
        errors.append("Frozen full-development aggregation choice is missing")
    else:
        aggregation_choice = json.loads(
            args.aggregation_choice.read_text(encoding="utf-8")
        )
        if aggregation_choice.get("state") != "frozen_development_choice":
            errors.append("Field-aware aggregation choice is not frozen")
        if aggregation_choice.get("cluster_count") != 70:
            errors.append("Aggregation choice did not use 70 development clusters")
        if aggregation_choice.get("prompt_count") != 150:
            errors.append("Aggregation choice did not use 150 development prompts")
        frozen_field_aware_selector = aggregation_choice.get(
            "selected_selector"
        )

    development_analysis: dict[str, Any] | None = None
    if (
        args.development_analysis is None
        or not args.development_analysis.exists()
    ):
        errors.append("Complete development analysis report is missing")
    else:
        development_analysis = json.loads(
            args.development_analysis.read_text(encoding="utf-8")
        )
        if development_analysis.get("split") != "development":
            errors.append("Development analysis has the wrong split")
        if (
            development_analysis.get("condition_summary", {})
            .get("cluster_count")
            != 70
        ):
            errors.append("Development analysis does not cover 70 clusters")

    try:
        (
            by_condition,
            development_runs,
            skipped_smoke_runs,
            skipped_verification_runs,
        ) = (
            load_full_development_rows(args.development_root)
        )
    except (FileNotFoundError, ValueError) as exc:
        errors.append(str(exc))
        by_condition = {}
        development_runs = []
        skipped_smoke_runs = []
        skipped_verification_runs = []

    if aggregation_choice is not None and args.aggregation_choice is not None:
        errors.extend(
            aggregation_choice_provenance_errors(
                args.aggregation_choice,
                aggregation_choice,
                development_runs,
                by_condition,
            )
        )

    expected = expected_conditions(frozen_field_aware_selector)
    if development_analysis is not None:
        analysis_conditions = {
            (row["selector"], row["representation"])
            for row in development_analysis.get("condition_summary", {}).get(
                "conditions", []
            )
        }
        missing_analysis_conditions = sorted(expected - analysis_conditions)
        if missing_analysis_conditions:
            errors.append(
                "Development analysis is missing conditions: "
                + ", ".join(
                    f"{selector}/{representation}"
                    for selector, representation in missing_analysis_conditions
                )
            )
        unexpected_analysis_conditions = sorted(
            condition
            for condition in analysis_conditions - expected
            if not condition[0].startswith("qwen-field-aware-")
        )
        if unexpected_analysis_conditions:
            errors.append(
                "Development analysis contains unexpected conditions: "
                + ", ".join(
                    f"{selector}/{representation}"
                    for selector, representation in unexpected_analysis_conditions
                )
            )
        canonical_runs = {
            (
                row["run_id"],
                row["manifest_sha256"],
                row["rows_sha256"],
            )
            for row in development_runs
        }
        analysis_runs = {
            (
                row["run_id"],
                row["manifest_sha256"],
                row["rows_sha256"],
            )
            for row in development_analysis.get("runs", [])
        }
        if analysis_runs != canonical_runs:
            missing_runs = sorted(canonical_runs - analysis_runs)
            extra_runs = sorted(analysis_runs - canonical_runs)
            errors.append(
                "Development analysis run provenance does not match canonical "
                f"primary runs; missing={missing_runs}, extra={extra_runs}"
            )
    missing_conditions: list[str] = []
    incomplete_conditions: list[str] = []
    for selector, representation in sorted(expected):
        rows = by_condition.get((selector, representation))
        label = f"{selector}/{representation}"
        if rows is None:
            missing_conditions.append(label)
            continue
        cluster_count = len(
            {row["cluster_id"] for row in rows.values()}
        )
        if len(rows) != 150 or cluster_count != 70:
            incomplete_conditions.append(
                f"{label}: {len(rows)} prompts/{cluster_count} clusters"
            )
    if missing_conditions:
        errors.append(
            "Missing full-development conditions: "
            + ", ".join(missing_conditions)
        )
    if incomplete_conditions:
        errors.append(
            "Incomplete full-development conditions: "
            + ", ".join(incomplete_conditions)
        )

    unexpected_conditions = sorted(
        f"{selector}/{representation}"
        for selector, representation in set(by_condition) - expected
        if not selector.startswith("qwen-field-aware-")
    )
    if unexpected_conditions:
        errors.append(
            "Unexpected full-development conditions: "
            + ", ".join(unexpected_conditions)
        )

    existing_confirmatory_files = (
        sorted(
            str(path)
            for path in args.confirmatory_root.rglob("*")
            if path.is_file()
        )
        if args.confirmatory_root.exists()
        else []
    )
    if existing_confirmatory_files:
        errors.append(
            "Confirmatory output directory is not empty before freeze"
        )

    code_paths = [
        repo_root() / "scripts" / "rq2a_selector_common.py",
        repo_root() / "scripts" / "run_rq2a_fixed_candidate_matrix.py",
        repo_root() / "scripts" / "run_rq2a_field_aware_selector.py",
        repo_root() / "scripts" / "analyze_rq2a_matched_content.py",
        repo_root() / "scripts" / "audit_rq2a_selector_lengths.py",
        repo_root() / "scripts" / "validate_rq2a_matched_representations.py",
        repo_root() / "scripts" / "freeze_rq2a_confirmatory_protocol.py",
    ]
    for path in code_paths:
        if not path.exists():
            errors.append(f"Missing frozen implementation file: {path}")

    audit = {
        "schema_version": "rq2a-confirmatory-freeze-audit-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "created_utc": utc_timestamp(),
        "state": (
            "ready_to_freeze" if not errors else "not_ready_to_freeze"
        ),
        "errors": errors,
        "expected_condition_count": len(expected),
        "complete_condition_count": sum(
            condition in by_condition
            and len(by_condition[condition]) == 150
            and len(
                {
                    row["cluster_id"]
                    for row in by_condition[condition].values()
                }
            )
            == 70
            for condition in expected
        ),
        "missing_conditions": missing_conditions,
        "incomplete_conditions": incomplete_conditions,
        "frozen_field_aware_selector": frozen_field_aware_selector,
        "development_runs": development_runs,
        "skipped_smoke_runs": skipped_smoke_runs,
        "skipped_verification_runs": skipped_verification_runs,
        "existing_confirmatory_files": existing_confirmatory_files,
    }
    if args.freeze:
        if errors:
            print(json.dumps(audit, indent=2))
            raise SystemExit(1)
        freeze_manifest = {
            **audit,
            "schema_version": "rq2a-confirmatory-freeze-manifest-v1",
            "state": "frozen_before_confirmatory",
            "input_artifacts": {
                str(path): sha256_file(path)
                for path in required_artifacts
            },
            "aggregation_choice": {
                "path": str(args.aggregation_choice),
                "sha256": sha256_file(args.aggregation_choice),
                "selected_selector": frozen_field_aware_selector,
            },
            "development_analysis": {
                "path": str(args.development_analysis),
                "sha256": sha256_file(args.development_analysis),
            },
            "implementation_sha256": {
                str(path): sha256_file(path) for path in code_paths
            },
            "representation_sha256": {
                representation: sha256_file(
                    args.input_dir
                    / "representations"
                    / f"{representation}.jsonl"
                )
                for representation in ALL_REPRESENTATIONS
            },
            "confirmatory_output_root": str(args.confirmatory_root),
        }
        write_json_atomic(args.output, freeze_manifest)
        print(
            json.dumps(
                {
                    "status": "FROZEN",
                    "path": str(args.output),
                    "sha256": sha256_file(args.output),
                },
                indent=2,
            )
        )
        return
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
