#!/usr/bin/env python3
"""Run leakage-free seven-field Qwen scoring for RQ2a."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import run_rq2a_fixed_candidate_matrix as fixed_runner

from rq2a_selector_common import (
    EPSILON,
    FIELD_ORDER,
    PROTOCOL_VERSION,
    RUN_MANIFEST_SCHEMA_VERSION,
    SERIALISER_VERSION,
    build_result_row,
    cosine,
    load_run_data,
    mean,
    render_summary_markdown,
    representation_documents,
    repo_root,
    self_test,
    sha256_file,
    sha256_json,
    sha256_text,
    summarise_result_rows,
    utc_timestamp,
    validate_confirmatory_execution_grant,
    validate_confirmatory_freeze_manifest,
    write_json_atomic,
    write_jsonl_atomic,
)
from run_rq2a_fixed_candidate_matrix import (
    QWEN_BASE_URL,
    QWEN_DIMENSIONS,
    QWEN_MODEL,
    RQ2aEmbeddingClient,
    load_dotenv,
    stats_delta,
)


REPRESENTATION = "same-facts-fielded"
AGGREGATIONS = ["maximum", "uniform-top-two"]
FIELD_AWARE_COMPONENT_VERSION = "rq2a-field-block-v1"


def format_field_value(field: str, items: list[str]) -> str:
    if len(items) == 1:
        return items[0]
    if field == "workflow_procedure":
        return "\n".join(
            f"{index}. {item}"
            for index, item in enumerate(items, start=1)
        )
    return "\n".join(f"- {item}" for item in items)


def field_component_text(
    field: str,
    items: list[str],
    field_labels: dict[str, str],
) -> str:
    """Render the exact labelled field block visible in the fielded document."""
    return f"{field_labels[field]}\n{format_field_value(field, items)}"


def aggregate(component_scores: list[float], aggregation: str) -> float:
    if len(component_scores) != len(FIELD_ORDER):
        raise ValueError(
            "Field-aware aggregation requires exactly "
            f"{len(FIELD_ORDER)} component scores"
        )
    ordered = sorted(component_scores, reverse=True)
    if aggregation == "maximum":
        return ordered[0]
    if aggregation == "uniform-top-two":
        return statistics.mean(ordered[:2])
    raise ValueError(f"Unsupported field-aware aggregation: {aggregation}")


def cluster_weighted_metric(
    rows: list[dict[str, Any]],
    selector: str,
    metric: str,
) -> float:
    by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["selector"] == selector:
            by_cluster[row["cluster_id"]].append(row)
    return mean(
        mean(row[metric] for row in cluster_rows)
        for cluster_rows in by_cluster.values()
    )


def choose_aggregation(rows: list[dict[str, Any]]) -> dict[str, Any]:
    identities_by_selector: dict[str, set[tuple[str, str]]] = {}
    for aggregation in AGGREGATIONS:
        selector = f"qwen-field-aware-{aggregation}"
        selector_rows = [row for row in rows if row["selector"] == selector]
        identities = {
            (row["cluster_id"], row["prompt_id"]) for row in selector_rows
        }
        if not identities or len(identities) != len(selector_rows):
            raise ValueError(
                f"{selector}: missing or duplicate aggregation-choice rows"
            )
        identities_by_selector[selector] = identities
    identity_sets = list(identities_by_selector.values())
    if any(identities != identity_sets[0] for identities in identity_sets[1:]):
        raise ValueError(
            "Field-aware aggregations must be compared on identical prompts"
        )

    candidates: list[dict[str, Any]] = []
    for aggregation in AGGREGATIONS:
        selector = f"qwen-field-aware-{aggregation}"
        candidates.append(
            {
                "aggregation": aggregation,
                "selector": selector,
                "cluster_weighted_top1_tie_adjusted": cluster_weighted_metric(
                    rows,
                    selector,
                    "top1_tie_adjusted",
                ),
                "cluster_weighted_mrr_tie_adjusted": cluster_weighted_metric(
                    rows,
                    selector,
                    "mrr_tie_adjusted",
                ),
            }
        )
    preference = {"uniform-top-two": 1, "maximum": 0}
    selected = max(
        candidates,
        key=lambda item: (
            item["cluster_weighted_top1_tie_adjusted"],
            item["cluster_weighted_mrr_tie_adjusted"],
            preference[item["aggregation"]],
        ),
    )
    return {
        "schema_version": "rq2a-field-aware-aggregation-choice-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "decision_rule": (
            "Higher development cluster-weighted tie-adjusted Top-1; "
            "exact tie by higher cluster-weighted tie-adjusted MRR; "
            "remaining exact tie prefers uniform-top-two."
        ),
        "candidates": candidates,
        "selected_aggregation": selected["aggregation"],
        "selected_selector": selected["selector"],
    }


def confirmatory_invocation(args: argparse.Namespace) -> dict[str, Any]:
    freeze_sha256 = (
        sha256_file(args.confirmatory_freeze_manifest)
        if args.confirmatory_freeze_manifest is not None
        and args.confirmatory_freeze_manifest.is_file()
        else None
    )
    choice_sha256 = (
        sha256_file(args.aggregation_choice_file)
        if args.aggregation_choice_file is not None
        and args.aggregation_choice_file.is_file()
        else None
    )
    return {
        "entry_point": "run_rq2a_field_aware_selector.py",
        "split": args.split,
        "output_dir": str(args.output_dir.resolve()),
        "run_id": args.run_id,
        "evidence_role": args.evidence_role,
        "aggregations": list(args.aggregations),
        "representation": REPRESENTATION,
        "clusters_per_field": args.clusters_per_field,
        "overwrite": bool(args.overwrite),
        "freeze_aggregation_choice": bool(args.freeze_aggregation_choice),
        "aggregation_choice_sha256": choice_sha256,
        "confirmatory_freeze_sha256": freeze_sha256,
        "qwen_base_url": args.qwen_base_url,
        "qwen_model": args.qwen_model,
        "qwen_dimensions": args.qwen_dimensions,
        "qwen_batch_size": args.qwen_batch_size,
        "max_audit_tokens": args.max_audit_tokens,
    }


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=root / "rq2a_matched_content",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "development",
    )
    parser.add_argument(
        "--split",
        choices=["development", "confirmatory"],
        default="development",
    )
    parser.add_argument("--clusters-per-field", type=int)
    parser.add_argument(
        "--aggregations",
        nargs="+",
        choices=AGGREGATIONS,
        default=AGGREGATIONS,
    )
    parser.add_argument("--run-id")
    parser.add_argument(
        "--evidence-role",
        choices=["primary", "verification"],
        default="primary",
        help=(
            "Whether this run supplies the canonical development comparison "
            "or only verifies reproducibility/cache behaviour."
        ),
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--freeze-aggregation-choice",
        action="store_true",
        help="Write a final development aggregation choice; disallowed for smoke subsets.",
    )
    parser.add_argument(
        "--aggregation-choice-file",
        type=Path,
        help="Required for confirmatory scoring and must name one frozen rule.",
    )
    parser.add_argument(
        "--confirmatory-freeze-manifest",
        type=Path,
        help="Required for confirmatory scoring after the development gate.",
    )
    parser.add_argument(
        "--confirmatory-controller-grant",
        type=Path,
        help="Required exact-invocation grant for every confirmatory run.",
    )
    parser.add_argument("--dotenv", type=Path, default=root.parent / ".env")
    parser.add_argument("--cache-dir", type=Path, default=root / "cache" / "rq2a")
    parser.add_argument(
        "--legacy-cache-dir",
        type=Path,
        default=root / "runtime" / "provider_cache",
        help="Read-only exact-key fallback for earlier provider embeddings.",
    )
    parser.add_argument("--qwen-base-url", default=QWEN_BASE_URL)
    parser.add_argument("--qwen-api-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--qwen-model", default=QWEN_MODEL)
    parser.add_argument("--qwen-dimensions", type=int, default=QWEN_DIMENSIONS)
    parser.add_argument("--qwen-batch-size", type=int, default=10)
    parser.add_argument("--qwen-timeout-seconds", type=int, default=180)
    parser.add_argument("--max-audit-tokens", type=int, default=8192)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    self_test()
    component_probe = [0.4, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3]
    assert aggregate(component_probe, "maximum") == 0.4
    assert abs(aggregate(component_probe, "uniform-top-two") - 0.3) < 1e-12
    if args.self_test:
        print("RQ2a field-aware self-test: PASS")
        return

    if args.freeze_aggregation_choice:
        if args.split != "development" or args.clusters_per_field is not None:
            raise ValueError(
                "Aggregation choice can be frozen only on the complete development split"
            )
        if set(args.aggregations) != set(AGGREGATIONS):
            raise ValueError(
                "Both preregistered aggregations are required before freezing"
            )

    frozen_choice: dict[str, Any] | None = None
    confirmatory_freeze: dict[str, Any] | None = None
    confirmatory_grant: dict[str, Any] | None = None
    if args.split == "confirmatory":
        if (
            args.confirmatory_freeze_manifest is None
            or not args.confirmatory_freeze_manifest.exists()
        ):
            raise ValueError(
                "Confirmatory scoring requires the development freeze manifest"
            )
        if (
            args.aggregation_choice_file is None
            or not args.aggregation_choice_file.exists()
        ):
            raise ValueError(
                "Confirmatory field-aware scoring requires a frozen aggregation choice"
            )
        confirmatory_freeze = validate_confirmatory_freeze_manifest(
            args.confirmatory_freeze_manifest,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
        )
        frozen_choice = json.loads(
            args.aggregation_choice_file.read_text(encoding="utf-8")
        )
        frozen_aggregation = confirmatory_freeze["aggregation_choice"]
        if (
            Path(frozen_aggregation["path"]).resolve()
            != args.aggregation_choice_file.resolve()
        ):
            raise ValueError(
                "Confirmatory aggregation choice path differs from the freeze manifest"
            )
        if (
            sha256_file(args.aggregation_choice_file)
            != frozen_aggregation["sha256"]
        ):
            raise ValueError(
                "Confirmatory aggregation choice hash differs from the freeze manifest"
            )
        selected = frozen_choice["selected_aggregation"]
        if (
            frozen_choice.get("selected_selector")
            != confirmatory_freeze["aggregation_choice"]["selected_selector"]
        ):
            raise ValueError(
                "Confirmatory aggregation selector differs from the freeze manifest"
            )
        if args.aggregations != [selected]:
            raise ValueError(
                f"Confirmatory aggregation must be exactly the frozen rule {selected}"
            )
        confirmatory_grant = validate_confirmatory_execution_grant(
            args.confirmatory_controller_grant,
            action="field_aware_scoring",
            invocation=confirmatory_invocation(args),
        )
        expected_guard = sha256_file(args.confirmatory_controller_grant)
        if (
            getattr(
                fixed_runner.post_json,
                "_rq2a_confirmatory_grant_sha256",
                None,
            )
            != expected_guard
        ):
            raise ValueError(
                "Confirmatory field-aware scoring requires the "
                "controller-installed guarded transport"
            )

    load_dotenv(args.dotenv)
    api_key = os.environ.get(args.qwen_api_key_env)
    if not api_key:
        raise RuntimeError(
            f"Qwen selector requires environment variable {args.qwen_api_key_env}"
        )

    run_id = args.run_id or (
        f"rq2a-field-aware-{args.split}-"
        f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    )
    run_dir = args.output_dir / run_id
    if run_dir.exists() and any(run_dir.iterdir()) and not args.overwrite:
        raise FileExistsError(
            f"Run directory already contains artifacts: {run_dir}"
        )
    run_dir.mkdir(parents=True, exist_ok=True)

    started_utc = utc_timestamp()
    wall_started = time.perf_counter()
    protocol, prompts, indexes = load_run_data(
        args.input_dir,
        args.split,
        [REPRESENTATION],
        args.clusters_per_field,
    )
    field_labels = protocol["field_labels"]
    index = indexes[REPRESENTATION]

    component_texts: set[str] = set()
    component_by_candidate: dict[
        tuple[str, str],
        dict[str, str],
    ] = {}
    for key, row in index.items():
        components: dict[str, str] = {}
        for field in FIELD_ORDER:
            text = field_component_text(
                field,
                row["canonical_fields"][field],
                field_labels,
            )
            if text not in row["selector_visible_text"]:
                raise ValueError(
                    f"{key}/{field}: component is not an exact fielded-text block"
                )
            components[field] = text
            component_texts.add(text)
        component_by_candidate[key] = components

    client = RQ2aEmbeddingClient(
        provider="qwen",
        base_url=args.qwen_base_url,
        api_key=api_key,
        model=args.qwen_model,
        dimensions=args.qwen_dimensions,
        cache_dir=args.cache_dir,
        timeout_seconds=args.qwen_timeout_seconds,
        max_audit_tokens=args.max_audit_tokens,
        legacy_cache_dir=args.legacy_cache_dir,
    )
    before_components = client.snapshot()
    components_started = time.perf_counter()
    component_vectors = client.embed_many(
        sorted(component_texts),
        batch_size=args.qwen_batch_size,
        progress_label="RQ2a field components",
    )
    components_wall = time.perf_counter() - components_started
    after_components = client.snapshot()
    query_texts = sorted({prompt["query_text"] for prompt in prompts})
    queries_started = time.perf_counter()
    query_vectors = client.embed_many(
        query_texts,
        batch_size=args.qwen_batch_size,
        progress_label="RQ2a field-aware queries",
    )
    queries_wall = time.perf_counter() - queries_started
    after_queries = client.snapshot()

    selector_configs = {
        aggregation: {
            "selector": f"qwen-field-aware-{aggregation}",
            "provider": "qwen",
            "base_url": args.qwen_base_url,
            "model": args.qwen_model,
            "dimensions": args.qwen_dimensions,
            "representation": REPRESENTATION,
            "component_version": FIELD_AWARE_COMPONENT_VERSION,
            "component_text": "exact_labelled_field_block_from_fielded_representation",
            "fields": FIELD_ORDER,
            "aggregation": aggregation,
            "first_stage_score": None,
            "field_specific_weights": None,
            "score": "cosine",
            "truncation": False,
            "epsilon": EPSILON,
        }
        for aggregation in args.aggregations
    }

    rows: list[dict[str, Any]] = []
    scoring_started = time.perf_counter()
    for prompt in prompts:
        _, candidate_rows = representation_documents(prompt, index)
        query_vector = query_vectors[prompt["query_text"]]
        candidate_component_scores: list[dict[str, float]] = []
        candidate_component_hashes: list[dict[str, str]] = []
        for candidate in candidate_rows:
            key = (prompt["cluster_id"], candidate["skill_id"])
            components = component_by_candidate[key]
            field_scores = {
                field: cosine(query_vector, component_vectors[components[field]])
                for field in FIELD_ORDER
            }
            candidate_component_scores.append(field_scores)
            candidate_component_hashes.append(
                {
                    field: sha256_text(components[field])
                    for field in FIELD_ORDER
                }
            )
        for aggregation_name in args.aggregations:
            score_started = time.perf_counter()
            scores = [
                aggregate(
                    [field_scores[field] for field in FIELD_ORDER],
                    aggregation_name,
                )
                for field_scores in candidate_component_scores
            ]
            selector = f"qwen-field-aware-{aggregation_name}"
            rows.append(
                build_result_row(
                    run_id=run_id,
                    selector=selector,
                    selector_config=selector_configs[aggregation_name],
                    representation=REPRESENTATION,
                    prompt=prompt,
                    candidate_rows=candidate_rows,
                    scores=scores,
                    score_latency_seconds=time.perf_counter() - score_started,
                    extra={
                        "aggregation_rule": aggregation_name,
                        "field_component_scores": candidate_component_scores,
                        "field_component_text_sha256": candidate_component_hashes,
                        "field_order": FIELD_ORDER,
                        "first_stage_score_used": False,
                        "field_specific_weights_used": False,
                    },
                )
            )
    score_wall = time.perf_counter() - scoring_started

    expected_rows = len(prompts) * len(args.aggregations)
    if len(rows) != expected_rows:
        raise RuntimeError(
            f"Field-aware row count {len(rows)} != expected {expected_rows}"
        )
    unique_identities = {
        (row["selector"], row["prompt_id"]) for row in rows
    }
    if len(unique_identities) != expected_rows:
        raise RuntimeError("Duplicate field-aware result identities")

    choice = choose_aggregation(rows) if set(args.aggregations) == set(AGGREGATIONS) else None
    if choice is not None:
        choice["state"] = (
            "frozen_development_choice"
            if args.freeze_aggregation_choice
            else "provisional_smoke_choice_not_frozen"
        )
        choice["run_id"] = run_id
        choice["split"] = args.split
        choice["cluster_count"] = len({prompt["cluster_id"] for prompt in prompts})
        choice["prompt_count"] = len(prompts)
        selected_selector = choice["selected_selector"]
        for row in rows:
            row["is_selected_aggregation"] = row["selector"] == selected_selector
            row["aggregation_choice_state"] = choice["state"]
    elif frozen_choice is not None:
        for row in rows:
            row["is_selected_aggregation"] = True
            row["aggregation_choice_state"] = "frozen_before_confirmatory"

    rows.sort(key=lambda row: (row["selector"], row["prompt_id"]))
    rows_path = run_dir / "rows.jsonl"
    write_jsonl_atomic(rows_path, rows)
    choice_path: Path | None = None
    if choice is not None:
        choice_path = run_dir / "aggregation_choice.json"
        write_json_atomic(choice_path, choice)

    summary = summarise_result_rows(rows)
    manifest = {
        "schema_version": RUN_MANIFEST_SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "run_id": run_id,
        "state": "complete",
        "started_utc": started_utc,
        "finished_utc": utc_timestamp(),
        "split": args.split,
        "clusters_per_field": args.clusters_per_field,
        "evidence_role": args.evidence_role,
        "prompt_count": len(prompts),
        "cluster_count": len({prompt["cluster_id"] for prompt in prompts}),
        "representation": REPRESENTATION,
        "aggregations": args.aggregations,
        "aggregation_choice": choice,
        "selector_configurations": selector_configs,
        "input_artifacts": {
            "protocol_json": {
                "path": str(args.input_dir / "protocol.json"),
                "sha256": sha256_file(args.input_dir / "protocol.json"),
            },
            "prompts_jsonl": {
                "path": str(args.input_dir / "prompts.jsonl"),
                "sha256": sha256_file(args.input_dir / "prompts.jsonl"),
            },
            "fielded_representation": {
                "path": str(
                    args.input_dir
                    / "representations"
                    / f"{REPRESENTATION}.jsonl"
                ),
                "sha256": sha256_file(
                    args.input_dir
                    / "representations"
                    / f"{REPRESENTATION}.jsonl"
                ),
            },
            **(
                {
                    "confirmatory_freeze_manifest": {
                        "path": str(args.confirmatory_freeze_manifest),
                        "sha256": sha256_file(
                            args.confirmatory_freeze_manifest
                        ),
                        "state": confirmatory_freeze["state"],
                    },
                    "frozen_aggregation_choice": {
                        "path": str(args.aggregation_choice_file),
                        "sha256": sha256_file(args.aggregation_choice_file),
                        "selected_selector": frozen_choice["selected_selector"],
                    },
                }
                if confirmatory_freeze is not None
                else {}
            ),
            **(
                {
                    "confirmatory_controller_grant": {
                        "path": str(args.confirmatory_controller_grant),
                        "sha256": sha256_file(
                            args.confirmatory_controller_grant
                        ),
                        "action": confirmatory_grant["action"],
                        "invocation_sha256": confirmatory_grant[
                            "invocation_sha256"
                        ],
                    }
                }
                if confirmatory_grant is not None
                else {}
            ),
        },
        "output_artifacts": {
            "rows_jsonl": {
                "path": str(rows_path),
                "sha256": sha256_file(rows_path),
                "row_count": len(rows),
            },
            **(
                {
                    "aggregation_choice_json": {
                        "path": str(choice_path),
                        "sha256": sha256_file(choice_path),
                    }
                }
                if choice_path is not None
                else {}
            ),
        },
        "runtime": {
            "component_prepare_wall_seconds": components_wall,
            "query_prepare_wall_seconds": queries_wall,
            "score_wall_seconds": score_wall,
            "component_embedding_stats": stats_delta(
                after_components,
                before_components,
            ),
            "query_embedding_stats": stats_delta(
                after_queries,
                after_components,
            ),
            "cumulative_embedding_stats": after_queries,
            "total_wall_seconds": time.perf_counter() - wall_started,
        },
        "quality_checks": {
            "common_self_test": "pass",
            "exact_fielded_component_blocks": "pass",
            "component_field_count": len(FIELD_ORDER),
            "first_stage_score_absent": "pass",
            "field_specific_weights_absent": "pass",
            "row_count_expected": expected_rows,
            "row_count_actual": len(rows),
            "unique_result_identities": len(unique_identities),
            "candidate_alignment": "pass",
            "finite_scores": "pass",
            "no_thesis_write": bool(
                protocol["thesis_write_blocked_pending_user_review"]
            ),
        },
    }
    write_json_atomic(run_dir / "summary.json", summary)
    write_json_atomic(run_dir / "manifest.json", manifest)
    (run_dir / "summary.md").write_text(
        render_summary_markdown(summary, manifest),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "run_id": run_id,
                "run_dir": str(run_dir),
                "prompt_count": len(prompts),
                "cluster_count": manifest["cluster_count"],
                "row_count": len(rows),
                "aggregation_choice": choice,
                "conditions": summary["conditions"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
