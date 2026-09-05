#!/usr/bin/env python3
"""Create a frozen deterministic descriptive RQ2a failure report."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    read_jsonl,
    repo_root,
    sha256_file,
    validate_confirmatory_freeze_manifest,
    write_json_atomic,
)

from audit_rq2a_qwen_cache import ALL_REPRESENTATIONS
from run_rq2a_fixed_candidate_matrix import CORE_REPRESENTATIONS


CONDITIONS = {
    "qwen_fielded": ("qwen-single-vector", "same-facts-fielded"),
    "qwen_flat": ("qwen-single-vector", "same-facts-flat"),
    "field_aware": (
        "qwen-field-aware-uniform-top-two",
        "same-facts-fielded",
    ),
}
EXPECTED_PRIMARY_RUN_IDS = {
    "confirmatory-bm25-all-v1",
    "confirmatory-skillrouter-core-v1",
    "confirmatory-qwen-all-v1",
    "confirmatory-field-aware-v1",
}
EXPECTED_PRIMARY_CONDITIONS = {
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


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, action="append", required=True)
    parser.add_argument(
        "--failure-spec",
        type=Path,
        default=root / "rq2a_matched_content" / "confirmatory_failure_spec.json",
    )
    parser.add_argument(
        "--confirmatory-freeze-manifest", type=Path, required=True
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "analysis",
    )
    parser.add_argument("--analysis-id", default="confirmatory-failures-v1")
    return parser.parse_args()


def load_primary_rows(
    run_dirs: list[Path],
    freeze_sha256: str,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    rows: list[dict[str, Any]] = []
    provenance: list[dict[str, str]] = []
    run_ids: set[str] = set()
    for run_dir in run_dirs:
        manifest_path = run_dir / "manifest.json"
        rows_path = run_dir / "rows.jsonl"
        if not manifest_path.is_file() or not rows_path.is_file():
            raise FileNotFoundError(f"Incomplete primary run: {run_dir}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("split") != "confirmatory":
            raise ValueError(f"Non-confirmatory run: {run_dir}")
        if manifest.get("evidence_role", "primary") != "primary":
            raise ValueError(f"Non-primary run: {run_dir}")
        run_id = manifest.get("run_id")
        if run_id in run_ids:
            raise ValueError(f"Duplicate primary run ID: {run_id}")
        run_ids.add(run_id)
        frozen = manifest.get("input_artifacts", {}).get(
            "confirmatory_freeze_manifest", {}
        )
        if frozen.get("sha256") != freeze_sha256:
            raise ValueError(f"Freeze reference mismatch: {run_dir}")
        recorded = manifest.get("output_artifacts", {}).get("rows_jsonl", {})
        if recorded.get("sha256") != sha256_file(rows_path):
            raise ValueError(f"Rows hash mismatch: {run_dir}")
        rows.extend(read_jsonl(rows_path))
        provenance.append(
            {
                "run_id": run_id,
                "run_dir": str(run_dir),
                "manifest_sha256": sha256_file(manifest_path),
                "rows_sha256": sha256_file(rows_path),
            }
        )
    if run_ids != EXPECTED_PRIMARY_RUN_IDS:
        raise ValueError(
            "Failure report requires exactly the four frozen primary runs"
        )
    return rows, sorted(provenance, key=lambda row: row["run_id"])


def is_correct(row: dict[str, Any]) -> bool:
    return abs(float(row["top1_tie_adjusted"]) - 1.0) <= 1e-12


def example(
    category: str,
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    return {
        "category": category,
        "cluster_id": left["cluster_id"],
        "prompt_id": left["prompt_id"],
        "field": left["field"],
        "prompt_variant": left["prompt_variant"],
        "query_text": left["query_text"],
        "gold_skill_id": left["gold_skill_id"],
        "candidate_skill_ids": left["candidate_skill_ids"],
        "left_condition": {
            "selector": left["selector"],
            "representation": left["representation"],
        },
        "right_condition": {
            "selector": right["selector"],
            "representation": right["representation"],
        },
        "left_top1_tie_adjusted": left["top1_tie_adjusted"],
        "right_top1_tie_adjusted": right["top1_tie_adjusted"],
        "left_gold_margin": left["gold_margin"],
        "right_gold_margin": right["gold_margin"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# RQ2a Confirmatory Failure Decomposition",
        "",
        "**Deterministic descriptive supporting evidence only.**",
        "",
        f"- Primary rows validated: {report['primary_row_count']}",
        f"- Prompts: {report['prompt_count']}",
        f"- Failure spec SHA-256: `{report['failure_spec_sha256']}`",
        "",
        "## Category Counts",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in report["category_counts"].items():
        lines.append(f"| `{category}` | {count} |")
    lines.extend(["", "## Frozen Examples", ""])
    for row in report["examples"]:
        lines.extend(
            [
                f"### {row['category']} / {row['field']} / {row['prompt_id']}",
                "",
                f"- Query: {row['query_text']}",
                f"- Gold: `{row['gold_skill_id']}`",
                f"- Left Top-1/margin: {row['left_top1_tie_adjusted']:.3f} / {row['left_gold_margin']:.6f}",
                f"- Right Top-1/margin: {row['right_top1_tie_adjusted']:.3f} / {row['right_gold_margin']:.6f}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    freeze = validate_confirmatory_freeze_manifest(
        args.confirmatory_freeze_manifest
    )
    spec = json.loads(args.failure_spec.read_text(encoding="utf-8"))
    if spec.get("state") != "frozen_before_confirmatory":
        raise ValueError("Failure specification is not frozen")
    freeze_sha256 = sha256_file(args.confirmatory_freeze_manifest)
    rows, primary_runs = load_primary_rows(args.run_dir, freeze_sha256)
    if len(rows) != int(spec["required_primary_row_count"]):
        raise ValueError(
            f"Expected {spec['required_primary_row_count']} primary rows, got {len(rows)}"
        )
    identities = {
        (row["selector"], row["representation"], row["prompt_id"])
        for row in rows
    }
    if len(identities) != len(rows):
        raise ValueError("Duplicate primary condition-prompt rows")
    condition_counts = Counter(
        (row["selector"], row["representation"]) for row in rows
    )
    if set(condition_counts) != EXPECTED_PRIMARY_CONDITIONS:
        raise ValueError("Failure report primary condition set mismatch")
    if any(count != int(spec["required_prompt_count"]) for count in condition_counts.values()):
        raise ValueError("Failure report has an incomplete primary condition")
    by_condition: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_condition[(row["selector"], row["representation"])][
            row["prompt_id"]
        ] = row
    missing_conditions = [
        condition for condition in CONDITIONS.values() if condition not in by_condition
    ]
    if missing_conditions:
        raise ValueError(f"Failure conditions are missing: {missing_conditions}")
    selected = {name: by_condition[condition] for name, condition in CONDITIONS.items()}
    prompt_ids = set(selected["qwen_fielded"])
    if any(set(condition_rows) != prompt_ids for condition_rows in selected.values()):
        raise ValueError("Failure conditions do not have identical prompt identities")
    if len(prompt_ids) != int(spec["required_prompt_count"]):
        raise ValueError("Failure conditions do not cover all confirmatory prompts")

    cases: list[dict[str, Any]] = []
    for prompt_id in sorted(prompt_ids):
        fielded = selected["qwen_fielded"][prompt_id]
        flat = selected["qwen_flat"][prompt_id]
        aware = selected["field_aware"][prompt_id]
        fielded_ok = is_correct(fielded)
        flat_ok = is_correct(flat)
        aware_ok = is_correct(aware)
        if fielded_ok and not flat_ok:
            cases.append(example("qwen_fielded_help", fielded, flat))
        if flat_ok and not fielded_ok:
            cases.append(example("qwen_fielded_harm", fielded, flat))
        if not fielded_ok and not flat_ok:
            cases.append(
                example("qwen_fielded_and_flat_both_fail", fielded, flat)
            )
        if aware_ok and not fielded_ok:
            cases.append(example("field_aware_recovery", aware, fielded))
        if fielded_ok and not aware_ok:
            cases.append(example("field_aware_harm", aware, fielded))

    category_counts = Counter(row["category"] for row in cases)
    per_field_counts = Counter((row["category"], row["field"]) for row in cases)
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in cases:
        grouped[(row["category"], row["field"])].append(row)
    limit = int(spec["sampling"]["examples_per_group"])
    examples: list[dict[str, Any]] = []
    for key in sorted(grouped):
        ordered = sorted(
            grouped[key], key=lambda row: (row["cluster_id"], row["prompt_id"])
        )
        examples.extend(ordered[:limit])

    report = {
        "schema_version": "rq2a-confirmatory-failure-report-v1",
        "split": "confirmatory",
        "role": spec["role"],
        "primary_row_count": len(rows),
        "prompt_count": len(prompt_ids),
        "freeze_manifest_sha256": freeze_sha256,
        "freeze_state": freeze["state"],
        "failure_spec_sha256": sha256_file(args.failure_spec),
        "primary_runs": primary_runs,
        "category_counts": {
            category: category_counts.get(category, 0)
            for category in spec["categories"]
        },
        "per_field_counts": [
            {"category": category, "field": field, "count": count}
            for (category, field), count in sorted(per_field_counts.items())
        ],
        "examples": examples,
        "quality_checks": {
            "complete_primary_matrix": "pass",
            "exact_primary_run_set": "pass",
            "exact_primary_condition_set": "pass",
            "paired_prompt_identities": "pass",
            "deterministic_sampling": "pass",
            "inferential_claims": "not_performed",
            "thesis_write": "not_performed",
        },
    }
    output_dir = args.output_dir / args.analysis_id
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Failure output already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_atomic(output_dir / "failure_report.json", report)
    (output_dir / "failure_report.md").write_text(
        render_markdown(report), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "output_dir": str(output_dir),
                "primary_rows": len(rows),
                "examples": len(examples),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
