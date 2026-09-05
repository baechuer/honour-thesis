#!/usr/bin/env python3
"""Analyse paired RQ2a fixed-candidate results without retuning selectors."""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    PROTOCOL_VERSION,
    RESULT_SCHEMA_VERSION,
    SERIALISER_VERSION,
    read_jsonl,
    repo_root,
    sha256_file,
    sha256_json,
    summarise_result_rows,
    utc_timestamp,
    validate_confirmatory_execution_grant,
    validate_confirmatory_freeze_manifest,
    write_json_atomic,
)


ALL_REPRESENTATIONS = (
    "shared-only",
    "same-facts-fielded",
    "same-facts-flat",
    "same-facts-prose",
    "same-facts-order-controlled",
    "same-facts-diluted-1x",
    "same-facts-diluted-2x",
    "same-facts-diluted-4x",
)
CORE_REPRESENTATIONS = (
    "shared-only",
    "same-facts-fielded",
    "same-facts-flat",
    "same-facts-prose",
    "same-facts-diluted-2x",
)
EXPECTED_CONFIRMATORY_RUN_IDS = {
    "confirmatory-bm25-all-v1",
    "confirmatory-skillrouter-core-v1",
    "confirmatory-qwen-all-v1",
    "confirmatory-field-aware-v1",
}
EXPECTED_CONFIRMATORY_CONDITIONS = {
    ("bm25", representation) for representation in ALL_REPRESENTATIONS
} | {
    ("skillrouter-cross-encoder", representation)
    for representation in CORE_REPRESENTATIONS
} | {
    ("qwen-single-vector", representation)
    for representation in ALL_REPRESENTATIONS
} | {
    ("qwen-field-aware-uniform-top-two", "same-facts-fielded")
}


def percentile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("Cannot compute a percentile of an empty sequence")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def average(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def bootstrap_cluster_mean(
    cluster_values: list[float],
    *,
    resamples: int,
    seed: int,
) -> tuple[float, float]:
    if not cluster_values:
        raise ValueError("No cluster values supplied to bootstrap")
    randomiser = random.Random(seed)
    size = len(cluster_values)
    draws = [
        average(
            [
                cluster_values[randomiser.randrange(size)]
                for _ in range(size)
            ]
        )
        for _ in range(resamples)
    ]
    return percentile(draws, 0.025), percentile(draws, 0.975)


def paired_sign_flip_p_value(
    cluster_values: list[float],
    *,
    resamples: int,
    seed: int,
) -> float:
    if not cluster_values:
        raise ValueError("No cluster values supplied to sign-flip test")
    observed = abs(average(cluster_values))
    randomiser = random.Random(seed)
    extreme = 0
    for _ in range(resamples):
        statistic = abs(
            average(
                [
                    value if randomiser.random() < 0.5 else -value
                    for value in cluster_values
                ]
            )
        )
        if statistic >= observed - 1e-15:
            extreme += 1
    return (extreme + 1) / (resamples + 1)


def condition_key(selector: str, representation: str) -> tuple[str, str]:
    return selector, representation


def load_complete_runs(
    run_dirs: list[Path],
    *,
    allow_confirmatory: bool,
    confirmatory_freeze_manifest: Path | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    if not run_dirs:
        raise ValueError("At least one --run-dir is required")
    all_rows: list[dict[str, Any]] = []
    manifests: list[dict[str, Any]] = []
    splits: set[str] = set()
    identities: set[tuple[str, str, str]] = set()
    for run_dir in run_dirs:
        manifest_path = run_dir / "manifest.json"
        rows_path = run_dir / "rows.jsonl"
        if not manifest_path.exists() or not rows_path.exists():
            raise FileNotFoundError(
                f"{run_dir}: expected manifest.json and rows.jsonl"
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("state") != "complete":
            raise ValueError(f"{run_dir}: run is not marked complete")
        evidence_role = manifest.get("evidence_role", "primary")
        if evidence_role != "primary":
            raise ValueError(
                f"{run_dir}: analysis accepts only primary evidence, got "
                f"{evidence_role!r}"
            )
        if manifest.get("protocol_version") != PROTOCOL_VERSION:
            raise ValueError(f"{run_dir}: protocol version mismatch")
        if manifest.get("serialiser_version") != SERIALISER_VERSION:
            raise ValueError(f"{run_dir}: serialiser version mismatch")
        expected_hash = (
            manifest.get("output_artifacts", {})
            .get("rows_jsonl", {})
            .get("sha256")
        )
        if expected_hash != sha256_file(rows_path):
            raise ValueError(f"{run_dir}: rows.jsonl hash mismatch")
        rows = read_jsonl(rows_path)
        expected_count = (
            manifest.get("output_artifacts", {})
            .get("rows_jsonl", {})
            .get("row_count")
        )
        if expected_count != len(rows):
            raise ValueError(f"{run_dir}: row count does not match manifest")
        split = manifest["split"]
        splits.add(split)
        for row in rows:
            if row.get("schema_version") != RESULT_SCHEMA_VERSION:
                raise ValueError(
                    f"{run_dir}/{row.get('prompt_id')}: result schema mismatch"
                )
            if row.get("split") != split:
                raise ValueError(
                    f"{run_dir}/{row['prompt_id']}: split mismatch"
                )
            identity = (
                row["selector"],
                row["representation"],
                row["prompt_id"],
            )
            if identity in identities:
                raise ValueError(
                    "Duplicate condition/prompt result across supplied runs: "
                    f"{identity}"
                )
            identities.add(identity)
        all_rows.extend(rows)
        manifests.append(
            {
                **manifest,
                "_run_dir": str(run_dir),
                "_manifest_sha256": sha256_file(manifest_path),
                "_rows_sha256": sha256_file(rows_path),
            }
        )
    if len(splits) != 1:
        raise ValueError(f"Cannot mix RQ2a splits in one analysis: {splits}")
    split = next(iter(splits))
    if split == "confirmatory":
        if not allow_confirmatory:
            raise ValueError(
                "Confirmatory analysis is blocked without --allow-confirmatory"
            )
        if (
            confirmatory_freeze_manifest is None
            or not confirmatory_freeze_manifest.exists()
        ):
            raise ValueError(
                "Confirmatory analysis requires the frozen pre-score manifest"
            )
        freeze = validate_confirmatory_freeze_manifest(
            confirmatory_freeze_manifest
        )
        freeze_hash = sha256_file(confirmatory_freeze_manifest)
        for manifest in manifests:
            reference = (
                manifest.get("input_artifacts", {})
                .get("confirmatory_freeze_manifest", {})
            )
            if reference.get("sha256") != freeze_hash:
                raise ValueError(
                    f"{manifest['_run_dir']}: result does not reference the "
                    "supplied confirmatory freeze manifest"
                )
            if reference.get("state") != freeze["state"]:
                raise ValueError(
                    f"{manifest['_run_dir']}: confirmatory freeze state mismatch"
                )
        if {manifest["run_id"] for manifest in manifests} != (
            EXPECTED_CONFIRMATORY_RUN_IDS
        ):
            raise ValueError(
                "Confirmatory inference requires exactly the four frozen primary runs"
            )
        if len(all_rows) != 13_200:
            raise ValueError(
                f"Confirmatory inference requires 13200 rows, got {len(all_rows)}"
            )
        condition_counts: dict[tuple[str, str], int] = defaultdict(int)
        prompt_ids: set[str] = set()
        cluster_ids: set[str] = set()
        for row in all_rows:
            condition_counts[(row["selector"], row["representation"])] += 1
            prompt_ids.add(row["prompt_id"])
            cluster_ids.add(row["cluster_id"])
        if set(condition_counts) != EXPECTED_CONFIRMATORY_CONDITIONS:
            raise ValueError("Confirmatory inference condition set mismatch")
        if any(count != 600 for count in condition_counts.values()):
            raise ValueError("Confirmatory inference has an incomplete condition")
        if len(prompt_ids) != 600 or len(cluster_ids) != 280:
            raise ValueError(
                "Confirmatory inference requires 600 prompts and 280 clusters"
            )
    return all_rows, manifests, split


def resolve_field_aware_selector(rows: list[dict[str, Any]]) -> str | None:
    selected = {
        row["selector"]
        for row in rows
        if row["selector"].startswith("qwen-field-aware-")
        and row.get("is_selected_aggregation")
    }
    if len(selected) > 1:
        raise ValueError(f"Multiple selected field-aware aggregations: {selected}")
    return next(iter(selected)) if selected else None


def paired_contrast(
    contrast: dict[str, Any],
    row_index: dict[tuple[str, str], dict[str, dict[str, Any]]],
    *,
    field_aware_selector: str | None,
    bootstrap_resamples: int,
    bootstrap_seed: int,
    permutation_resamples: int,
    permutation_seed: int,
    smallest_effect: float,
) -> dict[str, Any]:
    def resolve(condition: dict[str, str]) -> tuple[str, str] | None:
        selector = condition["selector"]
        if selector == "__frozen_field_aware_selector__":
            if field_aware_selector is None:
                return None
            selector = field_aware_selector
        return condition_key(selector, condition["representation"])

    left_key = resolve(contrast["left"])
    right_key = resolve(contrast["right"])
    base = {
        "id": contrast["id"],
        "family": contrast["family"],
        "purpose": contrast["purpose"],
        "expected_direction": contrast["expected_direction"],
        "left": (
            {
                "selector": left_key[0],
                "representation": left_key[1],
            }
            if left_key
            else contrast["left"]
        ),
        "right": (
            {
                "selector": right_key[0],
                "representation": right_key[1],
            }
            if right_key
            else contrast["right"]
        ),
    }
    if (
        left_key is None
        or right_key is None
        or left_key not in row_index
        or right_key not in row_index
    ):
        return {
            **base,
            "status": "unavailable_in_supplied_runs",
        }
    left_rows = row_index[left_key]
    right_rows = row_index[right_key]
    if set(left_rows) != set(right_rows):
        missing_left = sorted(set(right_rows) - set(left_rows))
        missing_right = sorted(set(left_rows) - set(right_rows))
        raise ValueError(
            f"{contrast['id']}: unpaired prompt sets; "
            f"left missing {missing_left[:5]}, right missing {missing_right[:5]}"
        )
    by_cluster: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = (
        defaultdict(list)
    )
    for prompt_id in sorted(left_rows):
        left = left_rows[prompt_id]
        right = right_rows[prompt_id]
        for identity_field in (
            "cluster_id",
            "field",
            "prompt_variant",
            "gold_skill_id",
            "candidate_skill_ids",
            "query_text_sha256",
        ):
            if left[identity_field] != right[identity_field]:
                raise ValueError(
                    f"{contrast['id']}/{prompt_id}: paired identity mismatch "
                    f"for {identity_field}"
                )
        by_cluster[left["cluster_id"]].append((left, right))

    cluster_top1_differences = [
        average(
            [
                left["top1_tie_adjusted"]
                - right["top1_tie_adjusted"]
                for left, right in pairs
            ]
        )
        for _, pairs in sorted(by_cluster.items())
    ]
    cluster_mrr_differences = [
        average(
            [
                left["mrr_tie_adjusted"] - right["mrr_tie_adjusted"]
                for left, right in pairs
            ]
        )
        for _, pairs in sorted(by_cluster.items())
    ]
    id_seed = int(sha256_json(contrast["id"])[:8], 16)
    ci_lower, ci_upper = bootstrap_cluster_mean(
        cluster_top1_differences,
        resamples=bootstrap_resamples,
        seed=bootstrap_seed + id_seed,
    )
    p_value = paired_sign_flip_p_value(
        cluster_top1_differences,
        resamples=permutation_resamples,
        seed=permutation_seed + id_seed,
    )
    effect = average(cluster_top1_differences)
    direction_met = (
        effect > 0
        if contrast["expected_direction"] == "positive"
        else effect < 0
    )
    return {
        **base,
        "status": "available",
        "prompt_count": len(left_rows),
        "cluster_count": len(by_cluster),
        "top1_difference_cluster_weighted": effect,
        "top1_bootstrap_ci_95": [ci_lower, ci_upper],
        "top1_paired_sign_flip_p_value_two_sided": p_value,
        "mrr_difference_cluster_weighted_descriptive": average(
            cluster_mrr_differences
        ),
        "expected_direction_met": direction_met,
        "practical_threshold": smallest_effect,
        "practical_support": bool(
            contrast["expected_direction"] == "positive"
            and effect >= smallest_effect
            and ci_lower > 0
        ),
        "cluster_top1_differences": cluster_top1_differences,
    }


def apply_holm(
    contrasts: list[dict[str, Any]],
    *,
    full_secondary_family_size: int,
) -> None:
    available = sorted(
        [
            contrast
            for contrast in contrasts
            if contrast["family"] == "secondary"
            and contrast["status"] == "available"
        ],
        key=lambda item: (
            item["top1_paired_sign_flip_p_value_two_sided"],
            item["id"],
        ),
    )
    previous = 0.0
    for rank, contrast in enumerate(available, start=1):
        raw = contrast["top1_paired_sign_flip_p_value_two_sided"]
        adjusted = min(
            1.0,
            max(previous, (full_secondary_family_size - rank + 1) * raw),
        )
        contrast["holm_adjusted_p_value"] = adjusted
        contrast["holm_reject_at_0_05"] = adjusted <= 0.05
        contrast["holm_family_size"] = full_secondary_family_size
        previous = adjusted


def render_markdown(report: dict[str, Any]) -> str:
    mode_warning = (
        "**Smoke/development analysis only. These values are implementation "
        "evidence and must not be reported as confirmatory findings.**"
        if report["split"] == "development"
        else "**Frozen confirmatory analysis.**"
    )
    lines = [
        "# RQ2a Matched-Content Analysis",
        "",
        mode_warning,
        "",
        f"- Split: `{report['split']}`",
        f"- Runs: {len(report['runs'])}",
        f"- Result rows: {report['row_count']}",
        f"- Bootstrap resamples: {report['analysis_settings']['bootstrap_resamples']:,}",
        f"- Sign-flip resamples: {report['analysis_settings']['permutation_resamples']:,}",
        "",
        "## Conditions",
        "",
        "| Selector | Representation | Prompts | Clusters | Top-1 | MRR | Margin | Strict confusion | Tie rate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for condition in report["condition_summary"]["conditions"]:
        lines.append(
            "| `{selector}` | `{representation}` | {prompts} | {clusters} | "
            "{top1:.3f} | {mrr:.3f} | {margin:.4f} | {confusion:.3f} | "
            "{ties:.3f} |".format(
                selector=condition["selector"],
                representation=condition["representation"],
                prompts=condition["prompt_count"],
                clusters=condition["cluster_count"],
                top1=condition["top1_tie_adjusted_cluster_weighted"],
                mrr=condition["mrr_tie_adjusted_prompt_weighted"],
                margin=condition["gold_margin_mean"],
                confusion=condition[
                    "near_neighbour_strict_confusion_rate"
                ],
                ties=condition["top_tie_rate"],
            )
        )
    lines.extend(
        [
            "",
            "## Preregistered Contrasts",
            "",
            "| Family | Contrast | Status | Paired Top-1 difference | 95% cluster-bootstrap CI | Raw p | Holm p | Practical support |",
            "|---|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for contrast in report["contrasts"]:
        if contrast["status"] != "available":
            lines.append(
                f"| {contrast['family']} | `{contrast['id']}` | unavailable | "
                "— | — | — | — | — |"
            )
            continue
        lower, upper = contrast["top1_bootstrap_ci_95"]
        raw_p = contrast["top1_paired_sign_flip_p_value_two_sided"]
        holm = contrast.get("holm_adjusted_p_value")
        lines.append(
            f"| {contrast['family']} | `{contrast['id']}` | available | "
            f"{contrast['top1_difference_cluster_weighted']:+.3f} | "
            f"[{lower:+.3f}, {upper:+.3f}] | {raw_p:.4f} | "
            f"{holm:.4f} | {str(contrast['practical_support']).lower()} |"
            if holm is not None
            else (
                f"| {contrast['family']} | `{contrast['id']}` | available | "
                f"{contrast['top1_difference_cluster_weighted']:+.3f} | "
                f"[{lower:+.3f}, {upper:+.3f}] | {raw_p:.4f} | — | "
                f"{str(contrast['practical_support']).lower()} |"
            )
        )
    lines.extend(
        [
            "",
            "Top-1 differences are paired within prompt, averaged within cluster, "
            "then averaged across clusters. MRR, margin, field/variant slices, "
            "and runtime are descriptive supporting evidence.",
            "",
            "## Runtime Provenance",
            "",
        ]
    )
    for run in report["runs"]:
        lines.append(
            f"- `{run['run_id']}`: `{run['run_dir']}`; "
            f"wall `{run.get('runtime', {}).get('total_wall_seconds', 0):.3f}s`."
        )
    lines.append("")
    return "\n".join(lines)


def confirmatory_invocation(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "entry_point": "analyze_rq2a_matched_content.py",
        "run_dirs": sorted(str(path.resolve()) for path in args.run_dir),
        "analysis_spec_sha256": sha256_file(args.analysis_spec),
        "output_dir": str(args.output_dir.resolve()),
        "analysis_id": args.analysis_id,
        "allow_confirmatory": bool(args.allow_confirmatory),
        "confirmatory_freeze_sha256": (
            sha256_file(args.confirmatory_freeze_manifest)
            if args.confirmatory_freeze_manifest is not None
            and args.confirmatory_freeze_manifest.is_file()
            else None
        ),
    }


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, action="append", required=True)
    parser.add_argument(
        "--analysis-spec",
        type=Path,
        default=root / "rq2a_matched_content" / "analysis_spec.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "analysis",
    )
    parser.add_argument("--analysis-id")
    parser.add_argument("--allow-confirmatory", action="store_true")
    parser.add_argument("--confirmatory-freeze-manifest", type=Path)
    parser.add_argument("--confirmatory-controller-grant", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec = json.loads(args.analysis_spec.read_text(encoding="utf-8"))
    if spec.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError("Analysis specification protocol mismatch")
    if spec.get("serialiser_version") != SERIALISER_VERSION:
        raise ValueError("Analysis specification serialiser mismatch")
    rows, manifests, split = load_complete_runs(
        args.run_dir,
        allow_confirmatory=args.allow_confirmatory,
        confirmatory_freeze_manifest=args.confirmatory_freeze_manifest,
    )
    if split == "confirmatory":
        validate_confirmatory_execution_grant(
            args.confirmatory_controller_grant,
            action="confirmatory_analysis",
            invocation=confirmatory_invocation(args),
        )
    row_index: dict[
        tuple[str, str],
        dict[str, dict[str, Any]],
    ] = defaultdict(dict)
    for row in rows:
        row_index[(row["selector"], row["representation"])][
            row["prompt_id"]
        ] = row

    field_aware_selector = resolve_field_aware_selector(rows)
    settings = {
        "bootstrap_resamples": int(spec["bootstrap"]["resamples"]),
        "bootstrap_seed": int(spec["bootstrap"]["seed"]),
        "permutation_resamples": int(
            spec["permutation_test"]["resamples"]
        ),
        "permutation_seed": int(spec["permutation_test"]["seed"]),
        "smallest_effect_of_practical_interest": float(
            spec["smallest_effect_of_practical_interest"]
        ),
    }
    contrasts = [
        paired_contrast(
            contrast,
            row_index,
            field_aware_selector=field_aware_selector,
            bootstrap_resamples=settings["bootstrap_resamples"],
            bootstrap_seed=settings["bootstrap_seed"],
            permutation_resamples=settings["permutation_resamples"],
            permutation_seed=settings["permutation_seed"],
            smallest_effect=settings[
                "smallest_effect_of_practical_interest"
            ],
        )
        for contrast in spec["contrasts"]
    ]
    secondary_family_size = sum(
        contrast["family"] == "secondary"
        for contrast in spec["contrasts"]
    )
    apply_holm(
        contrasts,
        full_secondary_family_size=secondary_family_size,
    )

    analysis_id = args.analysis_id or (
        f"rq2a-analysis-{split}-"
        f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    )
    output_dir = args.output_dir / analysis_id
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Analysis output already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": "rq2a-analysis-report-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "analysis_id": analysis_id,
        "created_utc": utc_timestamp(),
        "split": split,
        "analysis_spec": {
            "path": str(args.analysis_spec),
            "sha256": sha256_file(args.analysis_spec),
        },
        "analysis_settings": settings,
        "row_count": len(rows),
        "condition_summary": summarise_result_rows(rows),
        "field_aware_selector": field_aware_selector,
        "contrasts": contrasts,
        "holm_secondary_family_size": secondary_family_size,
        "runs": [
            {
                "run_id": manifest["run_id"],
                "run_dir": manifest["_run_dir"],
                "manifest_sha256": manifest["_manifest_sha256"],
                "rows_sha256": manifest["_rows_sha256"],
                "runtime": manifest.get("runtime", {}),
            }
            for manifest in manifests
        ],
        "quality_checks": {
            "run_hashes": "pass",
            "primary_evidence_only": "pass",
            "unique_condition_prompt_rows": "pass",
            "paired_identity_alignment": "pass_for_available_contrasts",
            "confirmatory_guard": (
                "pass_with_freeze_manifest"
                if split == "confirmatory"
                else "not_applicable_development"
            ),
            "thesis_write": "not_performed",
        },
    }
    write_json_atomic(output_dir / "analysis.json", report)
    (output_dir / "analysis.md").write_text(
        render_markdown(report),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "analysis_id": analysis_id,
                "output_dir": str(output_dir),
                "split": split,
                "row_count": len(rows),
                "available_contrasts": [
                    contrast["id"]
                    for contrast in contrasts
                    if contrast["status"] == "available"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
