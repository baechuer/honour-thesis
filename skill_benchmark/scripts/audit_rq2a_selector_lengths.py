#!/usr/bin/env python3
"""Audit every RQ2a selector input against frozen no-truncation limits."""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    FIELD_ORDER,
    PROTOCOL_VERSION,
    SERIALISER_VERSION,
    audit_token_count,
    load_protocol,
    read_jsonl,
    repo_root,
    sha256_file,
    utc_timestamp,
    write_json_atomic,
)
from run_rq2a_field_aware_selector import field_component_text
from run_rq2a_fixed_candidate_matrix import (
    SKILLROUTER_MODEL,
    SKILLROUTER_REVISION,
    SkillRouterCrossEncoder,
)


def percentile(values: list[int], probability: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def distribution(values: list[int]) -> dict[str, Any]:
    return {
        "count": len(values),
        "minimum": min(values) if values else 0,
        "median": statistics.median(values) if values else 0,
        "p95": percentile(values, 0.95),
        "maximum": max(values) if values else 0,
        "mean": statistics.mean(values) if values else 0,
    }


def local_snapshot_path(model_id: str, revision: str) -> Path:
    hub_root = Path(
        os.environ.get(
            "HF_HOME",
            str(Path.home() / ".cache" / "huggingface"),
        )
    ) / "hub"
    path = (
        hub_root
        / ("models--" + model_id.replace("/", "--"))
        / "snapshots"
        / revision
    )
    if not path.is_dir():
        raise FileNotFoundError(f"Pinned local model snapshot is missing: {path}")
    return path


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=root / "rq2a_matched_content",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=root / "rq2a_matched_content" / "selector_length_audit.json",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=root / "rq2a_matched_content" / "selector_length_audit.md",
    )
    parser.add_argument("--qwen-audit-limit", type=int, default=8192)
    parser.add_argument("--skillrouter-token-limit", type=int, default=2048)
    parser.add_argument("--skillrouter-model", default=SKILLROUTER_MODEL)
    parser.add_argument("--skillrouter-revision", default=SKILLROUTER_REVISION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise RuntimeError(
            "Run this audit with the workspace-local RQ2a model environment"
        ) from exc

    protocol = load_protocol(args.input_dir)
    prompts = read_jsonl(args.input_dir / "prompts.jsonl")
    query_by_id = {row["prompt_id"]: row for row in prompts}
    if len(query_by_id) != 750:
        raise ValueError(f"Expected 750 prompts, found {len(query_by_id)}")

    representation_indexes: dict[
        str,
        dict[tuple[str, str], dict[str, Any]],
    ] = {}
    all_document_rows: list[dict[str, Any]] = []
    for representation in protocol["representations"]:
        rows = read_jsonl(
            args.input_dir
            / "representations"
            / f"{representation}.jsonl"
        )
        if len(rows) != 1050:
            raise ValueError(
                f"{representation}: expected 1,050 rows, found {len(rows)}"
            )
        representation_indexes[representation] = {
            (row["cluster_id"], row["skill_id"]): row for row in rows
        }
        all_document_rows.extend(rows)

    qwen_queries = [audit_token_count(row["query_text"]) for row in prompts]
    qwen_documents = [
        audit_token_count(row["selector_visible_text"])
        for row in all_document_rows
    ]
    fielded_rows = list(
        representation_indexes["same-facts-fielded"].values()
    )
    field_labels = protocol["field_labels"]
    component_lengths = [
        audit_token_count(
            field_component_text(
                field,
                row["canonical_fields"][field],
                field_labels,
            )
        )
        for row in fielded_rows
        for field in FIELD_ORDER
    ]

    snapshot_path = local_snapshot_path(
        args.skillrouter_model,
        args.skillrouter_revision,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        snapshot_path,
        padding_side="left",
        local_files_only=True,
    )
    scorer = object.__new__(SkillRouterCrossEncoder)
    scorer.tokenizer = tokenizer
    scorer.max_length = args.skillrouter_token_limit
    scorer.stats = {
        "maximum_model_tokens": 0,
        "minimum_model_tokens": None,
    }

    model_lengths: list[int] = []
    violations: list[dict[str, Any]] = []
    worst_pairs: list[dict[str, Any]] = []
    for representation in protocol["representations"]:
        index = representation_indexes[representation]
        for prompt in prompts:
            for skill_id in prompt["candidate_skill_ids"]:
                document_row = index[(prompt["cluster_id"], skill_id)]
                try:
                    input_ids = scorer.build_input_ids(
                        prompt["query_text"],
                        document_row["selector_visible_text"],
                    )
                    token_count = len(input_ids)
                except ValueError:
                    formatted = scorer.format_prompt(
                        prompt["query_text"],
                        document_row["selector_visible_text"],
                    )
                    prefix = (
                        "<|im_start|>system\nJudge whether the Document meets the "
                        "requirements based on the Query and the Instruct provided. "
                        'Note that the answer can only be "yes" or "no".'
                        "<|im_end|>\n<|im_start|>user\n"
                    )
                    suffix = (
                        "<|im_end|>\n<|im_start|>assistant\n"
                        "<think>\n\n</think>\n\n"
                    )
                    token_count = len(
                        tokenizer.encode(
                            prefix + formatted + suffix,
                            add_special_tokens=False,
                        )
                    )
                    violations.append(
                        {
                            "representation": representation,
                            "prompt_id": prompt["prompt_id"],
                            "cluster_id": prompt["cluster_id"],
                            "skill_id": skill_id,
                            "model_token_count": token_count,
                        }
                    )
                model_lengths.append(token_count)
                worst_pairs.append(
                    {
                        "representation": representation,
                        "prompt_id": prompt["prompt_id"],
                        "cluster_id": prompt["cluster_id"],
                        "skill_id": skill_id,
                        "model_token_count": token_count,
                    }
                )

    qwen_violations = {
        "queries": sum(
            value > args.qwen_audit_limit for value in qwen_queries
        ),
        "documents": sum(
            value > args.qwen_audit_limit for value in qwen_documents
        ),
        "field_components": sum(
            value > args.qwen_audit_limit for value in component_lengths
        ),
    }
    report = {
        "schema_version": "rq2a-selector-length-audit-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "created_utc": utc_timestamp(),
        "status": (
            "pass"
            if not violations and not any(qwen_violations.values())
            else "fail"
        ),
        "qwen": {
            "audit_tokenizer": r"\w+|[^\w\s]",
            "audit_limit": args.qwen_audit_limit,
            "queries": distribution(qwen_queries),
            "documents": distribution(qwen_documents),
            "field_components": distribution(component_lengths),
            "violations": qwen_violations,
            "note": (
                "The fixed audit tokenizer is a conservative reproducibility "
                "guard, not the provider billing tokenizer."
            ),
        },
        "skillrouter": {
            "model": args.skillrouter_model,
            "revision": args.skillrouter_revision,
            "snapshot_path": str(snapshot_path),
            "maximum_input_tokens": args.skillrouter_token_limit,
            "pair_count": len(model_lengths),
            "lengths": distribution(model_lengths),
            "violation_count": len(violations),
            "violations": violations[:100],
            "ten_longest_pairs": sorted(
                worst_pairs,
                key=lambda row: (
                    -row["model_token_count"],
                    row["representation"],
                    row["prompt_id"],
                    row["skill_id"],
                ),
            )[:10],
            "truncation": False,
        },
        "input_artifacts": {
            "protocol_json_sha256": sha256_file(
                args.input_dir / "protocol.json"
            ),
            "prompts_jsonl_sha256": sha256_file(
                args.input_dir / "prompts.jsonl"
            ),
            "representation_sha256": {
                representation: sha256_file(
                    args.input_dir
                    / "representations"
                    / f"{representation}.jsonl"
                )
                for representation in protocol["representations"]
            },
        },
    }
    write_json_atomic(args.output_json, report)
    lines = [
        "# RQ2a Selector Length Audit",
        "",
        f"- Status: **{report['status'].upper()}**",
        f"- Protocol: `{PROTOCOL_VERSION}`",
        f"- Serialiser: `{SERIALISER_VERSION}`",
        "",
        "## Qwen Audit Guard",
        "",
        "| Input class | Count | Median | P95 | Maximum | Violations |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, key in (
        ("Queries", "queries"),
        ("Complete representations", "documents"),
        ("Field-aware components", "field_components"),
    ):
        values = report["qwen"][key]
        lines.append(
            f"| {label} | {values['count']} | {values['median']:.1f} | "
            f"{values['p95']:.1f} | {values['maximum']} | "
            f"{qwen_violations[key]} |"
        )
    model_distribution = report["skillrouter"]["lengths"]
    lines.extend(
        [
            "",
            "## SkillRouter Model Tokens",
            "",
            f"- Pinned model: `{args.skillrouter_model}@{args.skillrouter_revision}`",
            f"- Pair count: {len(model_lengths):,}",
            f"- Limit: {args.skillrouter_token_limit}",
            f"- Minimum: {model_distribution['minimum']}",
            f"- Median: {model_distribution['median']:.1f}",
            f"- P95: {model_distribution['p95']:.1f}",
            f"- Maximum: {model_distribution['maximum']}",
            f"- Violations/truncations: {len(violations)}",
            "",
            "The audit constructs the same complete query-document prompt as the "
            "direct scorer and fails rather than truncating decisive text.",
            "",
        ]
    )
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
