#!/usr/bin/env python3
"""Build an auditable RQ2a construction, query, cache, and latency ledger."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    PROTOCOL_VERSION,
    SERIALISER_VERSION,
    repo_root,
    sha256_file,
    sha256_json,
    utc_timestamp,
    write_json_atomic,
)


def run_role(manifest: dict[str, Any]) -> str:
    if manifest.get("clusters_per_field") is not None:
        return "smoke"
    return manifest.get("evidence_role", "primary")


def cache_storage(path: Path) -> dict[str, int]:
    files = [item for item in path.rglob("*") if item.is_file()] if path.exists() else []
    return {
        "file_count": len(files),
        "bytes": sum(item.stat().st_size for item in files),
    }


def guarded_attempt_history(path: Path) -> dict[str, Any]:
    if not path.is_dir():
        raise FileNotFoundError(f"Guarded attempt directory is missing: {path}")
    files: list[dict[str, Any]] = []
    seen_text_hashes: set[str] = set()
    provider_usage: dict[str, int | float] = defaultdict(int)
    local_audit_tokens = 0
    categories: dict[str, int] = defaultdict(int)
    for attempt_path in sorted(path.glob("*.json")):
        row = json.loads(attempt_path.read_text(encoding="utf-8"))
        if row.get("schema_version") != "rq2a-guarded-dashscope-attempt-v1":
            raise ValueError(f"Guarded attempt schema mismatch: {attempt_path}")
        if row.get("state") != "complete":
            raise ValueError(f"Guarded attempt is not complete: {attempt_path}")
        if row.get("url") != (
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings"
        ):
            raise ValueError(f"Guarded attempt endpoint mismatch: {attempt_path}")
        if row.get("model") != "text-embedding-v4" or row.get("dimensions") != 1024:
            raise ValueError(f"Guarded attempt model metadata mismatch: {attempt_path}")
        text_hashes = row.get("text_sha256")
        token_counts = row.get("audit_token_counts")
        if (
            not isinstance(text_hashes, list)
            or not text_hashes
            or not isinstance(token_counts, list)
            or len(token_counts) != len(text_hashes)
        ):
            raise ValueError(f"Guarded attempt payload metadata mismatch: {attempt_path}")
        if seen_text_hashes & set(text_hashes):
            raise ValueError("Guarded attempt history repeats an outbound text")
        seen_text_hashes.update(text_hashes)
        local_audit_tokens += sum(int(value) for value in token_counts)
        usage = row.get("response", {}).get("usage")
        if not isinstance(usage, dict) or not isinstance(usage.get("total_tokens"), int):
            raise ValueError(f"Guarded attempt has no provider usage: {attempt_path}")
        for key, value in usage.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                provider_usage[key] += value
        categories[str(row.get("category"))] += 1
        files.append(
            {
                "path": str(attempt_path),
                "sha256": sha256_file(attempt_path),
                "category": row.get("category"),
                "text_count": len(text_hashes),
                "local_audit_tokens": sum(int(value) for value in token_counts),
                "provider_total_tokens": int(usage["total_tokens"]),
            }
        )
    return {
        "state": "complete_guarded_history",
        "attempt_directory": str(path),
        "successful_api_calls": len(files),
        "outbound_request_attempts": len(files),
        "unique_external_texts": len(seen_text_hashes),
        "local_audit_tokens": local_audit_tokens,
        "provider_usage": dict(sorted(provider_usage.items())),
        "categories": dict(sorted(categories.items())),
        "files": files,
        "history_sha256": sha256_json(files),
    }


def embedding_stats(manifest: dict[str, Any]) -> dict[str, Any]:
    runtime = manifest.get("runtime", {})
    if "qwen-single-vector" in runtime:
        section = runtime["qwen-single-vector"]
        cumulative = section.get("cumulative_embedding_stats", {})
        return {
            "kind": "qwen_single_vector",
            "construction_wall_seconds": section.get(
                "document_prepare_wall_seconds", 0.0
            ),
            "query_prepare_wall_seconds": section.get(
                "query_prepare_wall_seconds", 0.0
            ),
            "score_wall_seconds": section.get("score_wall_seconds", 0.0),
            "embedding": cumulative,
            "construction_embedding": section.get(
                "document_embedding_stats", {}
            ),
            "query_embedding": section.get("query_embedding_stats", {}),
        }
    if "component_embedding_stats" in runtime:
        cumulative = runtime.get("cumulative_embedding_stats", {})
        return {
            "kind": "qwen_field_aware",
            "construction_wall_seconds": runtime.get(
                "component_prepare_wall_seconds", 0.0
            ),
            "query_prepare_wall_seconds": runtime.get(
                "query_prepare_wall_seconds", 0.0
            ),
            "score_wall_seconds": runtime.get("score_wall_seconds", 0.0),
            "embedding": cumulative,
            "construction_embedding": runtime.get(
                "component_embedding_stats", {}
            ),
            "query_embedding": runtime.get("query_embedding_stats", {}),
        }
    return {}


def run_record(run_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    rows_path = run_dir / "rows.jsonl"
    output = manifest.get("output_artifacts", {}).get("rows_jsonl", {})
    if not rows_path.exists():
        raise FileNotFoundError(f"{run_dir}: rows.jsonl is missing")
    if output.get("sha256") != sha256_file(rows_path):
        raise ValueError(f"{run_dir}: rows hash mismatch")
    runtime = manifest.get("runtime", {})
    qwen = embedding_stats(manifest)
    qwen_cumulative = qwen.get("embedding", {})
    skillrouter = runtime.get("skillrouter-cross-encoder", {})
    bm25 = runtime.get("bm25", {})
    prompt_count = int(manifest.get("prompt_count", 0))
    online_seconds = 0.0
    if qwen:
        online_seconds = float(qwen["query_prepare_wall_seconds"]) + float(
            qwen["score_wall_seconds"]
        )
    elif skillrouter:
        online_seconds = float(
            skillrouter.get("pair_prepare_and_model_wall_seconds", 0.0)
        ) + float(skillrouter.get("score_lookup_wall_seconds", 0.0))
    elif bm25:
        online_seconds = float(bm25.get("wall_seconds", 0.0))
    return {
        "run_id": manifest["run_id"],
        "run_dir": str(run_dir),
        "role": run_role(manifest),
        "split": manifest["split"],
        "prompt_count": prompt_count,
        "cluster_count": int(manifest.get("cluster_count", 0)),
        "row_count": int(output.get("row_count", 0)),
        "selectors": manifest.get("selectors") or [
            f"qwen-field-aware-{name}"
            for name in manifest.get("aggregations", [])
        ],
        "representations": manifest.get("representations")
        or [manifest.get("representation")],
        "total_wall_seconds": float(runtime.get("total_wall_seconds", 0.0)),
        "construction_wall_seconds": float(
            qwen.get("construction_wall_seconds", 0.0)
        ),
        "online_wall_seconds": online_seconds,
        "online_wall_seconds_per_prompt": (
            online_seconds / prompt_count if prompt_count else None
        ),
        "qwen": qwen,
        "provider_api_calls": int(qwen_cumulative.get("api_calls", 0)),
        "provider_api_elapsed_seconds": float(
            qwen_cumulative.get("api_elapsed_seconds", 0.0)
        ),
        "provider_prompt_tokens": int(
            qwen_cumulative.get("provider_usage", {}).get("prompt_tokens", 0)
        ),
        "provider_total_tokens": int(
            qwen_cumulative.get("provider_usage", {}).get("total_tokens", 0)
        ),
        "embedding_cache_hits": int(qwen_cumulative.get("cache_hits", 0)),
        "embedding_legacy_cache_hits": int(
            qwen_cumulative.get("legacy_cache_hits", 0)
        ),
        "embedding_cache_misses": int(qwen_cumulative.get("cache_misses", 0)),
        "skillrouter": skillrouter,
        "skillrouter_cache_hits": int(skillrouter.get("cache_hits", 0)),
        "skillrouter_cache_misses": int(skillrouter.get("cache_misses", 0)),
        "skillrouter_scored_pairs": int(skillrouter.get("scored_pairs", 0)),
        "skillrouter_model_seconds": float(
            skillrouter.get("model_elapsed_seconds", 0.0)
        ),
        "skillrouter_truncated_pairs": int(
            skillrouter.get("truncated_pairs", 0)
        ),
        "manifest_sha256": sha256_file(run_dir / "manifest.json"),
        "rows_sha256": sha256_file(rows_path),
    }


def role_totals(records: list[dict[str, Any]]) -> dict[str, Any]:
    totals: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "run_count": 0,
            "row_count": 0,
            "provider_api_calls": 0,
            "provider_prompt_tokens": 0,
            "provider_total_tokens": 0,
            "embedding_cache_hits": 0,
            "embedding_legacy_cache_hits": 0,
            "embedding_cache_misses": 0,
            "skillrouter_cache_hits": 0,
            "skillrouter_cache_misses": 0,
            "skillrouter_scored_pairs": 0,
            "skillrouter_model_seconds": 0.0,
            "total_wall_seconds": 0.0,
        }
    )
    for record in records:
        row = totals[record["role"]]
        row["run_count"] += 1
        for key in (
            "row_count",
            "provider_api_calls",
            "provider_prompt_tokens",
            "provider_total_tokens",
            "embedding_cache_hits",
            "embedding_legacy_cache_hits",
            "embedding_cache_misses",
            "skillrouter_cache_hits",
            "skillrouter_cache_misses",
            "skillrouter_scored_pairs",
        ):
            row[key] += record[key]
        row["skillrouter_model_seconds"] += record[
            "skillrouter_model_seconds"
        ]
        row["total_wall_seconds"] += record["total_wall_seconds"]
    return dict(sorted(totals.items()))


def render_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# RQ2a Cost and Latency Ledger",
        "",
        "Development values are engineering measurements, not confirmatory findings.",
        "",
        f"- Split: `{ledger['split']}`",
        f"- Runs scanned: {len(ledger['runs'])}",
        f"- Price conversion: `{ledger['pricing']['state']}`",
        "",
        "## Runs",
        "",
        "| Run | Role | Selectors | Rows | API calls | Provider tokens | Cache hit/miss | Model pairs | Total wall | Online per prompt |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in ledger["runs"]:
        cache = run["embedding_cache_hits"] + run["embedding_legacy_cache_hits"]
        online = run["online_wall_seconds_per_prompt"]
        lines.append(
            f"| `{run['run_id']}` | {run['role']} | "
            f"{', '.join(run['selectors'])} | {run['row_count']} | "
            f"{run['provider_api_calls']} | {run['provider_prompt_tokens']} | "
            f"{cache}/{run['embedding_cache_misses']} | "
            f"{run['skillrouter_scored_pairs']} | "
            f"{run['total_wall_seconds']:.3f}s | "
            f"{online:.6f}s |"
            if online is not None
            else ""
        )
    lines.extend(
        [
            "",
            "## Representation Size",
            "",
            "| Representation | Median audit tokens | Mean words | Mean characters |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in ledger["representation_sizes"]:
        lengths = row["length_summary"]
        lines.append(
            f"| `{row['representation']}` | "
            f"{lengths['audit_token_count']['median']:.1f} | "
            f"{lengths['word_count']['mean']:.1f} | "
            f"{lengths['character_count']['mean']:.1f} |"
        )
    lines.extend(
        [
            "",
            "The online-per-prompt column is selector compute observed in the run: "
            "BM25 scoring, Qwen query-vector lookup plus cosine scoring, or "
            "SkillRouter pair inference. Qwen document/component preparation is "
            "reported separately in JSON as construction cost. Exact cached query "
            "vectors do not establish uncached provider latency.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir", type=Path, default=root / "rq2a_matched_content"
    )
    parser.add_argument(
        "--run-root",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "development",
    )
    parser.add_argument("--split", choices=["development", "confirmatory"], default="development")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "analysis",
    )
    parser.add_argument("--ledger-id", required=True)
    parser.add_argument("--qwen-input-price-per-million", type=float)
    parser.add_argument("--price-currency", default="USD")
    parser.add_argument("--price-source")
    parser.add_argument("--price-date")
    parser.add_argument("--guard-attempt-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    representation_manifest_path = args.input_dir / "manifest.json"
    representation_manifest = json.loads(
        representation_manifest_path.read_text(encoding="utf-8")
    )
    if representation_manifest.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError("Representation manifest protocol mismatch")
    if representation_manifest.get("serialiser_version") != SERIALISER_VERSION:
        raise ValueError("Representation manifest serialiser mismatch")
    records: list[dict[str, Any]] = []
    for manifest_path in sorted(args.run_root.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("split") != args.split:
            continue
        if manifest.get("state") != "complete":
            raise ValueError(f"{manifest_path.parent}: incomplete run manifest")
        records.append(run_record(manifest_path.parent, manifest))
    if not records:
        raise ValueError(f"No complete {args.split} runs found in {args.run_root}")
    manifest_primary_tokens = sum(
        row["provider_prompt_tokens"]
        for row in records
        if row["role"] == "primary"
    )
    if args.split == "confirmatory":
        if args.guard_attempt_dir is None:
            raise ValueError(
                "Confirmatory cost accounting requires --guard-attempt-dir"
            )
        guarded_usage = guarded_attempt_history(args.guard_attempt_dir)
        primary_tokens = int(
            guarded_usage["provider_usage"].get(
                "prompt_tokens",
                guarded_usage["provider_usage"].get("total_tokens", 0),
            )
        )
    else:
        guarded_usage = {
            "state": "not_applicable_development",
            "files": [],
        }
        primary_tokens = manifest_primary_tokens
    if args.qwen_input_price_per_million is None:
        pricing = {
            "state": "not_computed_no_frozen_price_snapshot",
            "currency": None,
            "input_price_per_million_tokens": None,
            "primary_provider_token_cost": None,
            "source": None,
            "date": None,
        }
    else:
        if not args.price_source or not args.price_date:
            raise ValueError(
                "Price conversion requires --price-source and --price-date"
            )
        pricing = {
            "state": "computed_from_user_supplied_price_snapshot",
            "currency": args.price_currency,
            "input_price_per_million_tokens": args.qwen_input_price_per_million,
            "primary_provider_token_cost": (
                primary_tokens
                / 1_000_000
                * args.qwen_input_price_per_million
            ),
            "source": args.price_source,
            "date": args.price_date,
        }
    cache_root = repo_root() / "cache" / "rq2a"
    ledger = {
        "schema_version": "rq2a-cost-ledger-v1",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "ledger_id": args.ledger_id,
        "created_utc": utc_timestamp(),
        "split": args.split,
        "run_root": str(args.run_root),
        "representation_manifest": {
            "path": str(representation_manifest_path),
            "sha256": sha256_file(representation_manifest_path),
        },
        "representation_sizes": [
            {
                "representation": row["representation"],
                "length_summary": row["length_summary"],
            }
            for row in representation_manifest["representations"]
        ],
        "runs": records,
        "totals_by_role": role_totals(records),
        "guarded_attempt_history": guarded_usage,
        "cache_storage": {
            "qwen_embeddings": cache_storage(
                cache_root / "embeddings" / "qwen" / "text-embedding-v4" / "1024"
            ),
            "skillrouter_scores": cache_storage(cache_root / "cross_encoder"),
        },
        "pricing": pricing,
        "quality_checks": {
            "run_hashes": "pass",
            "roles_separated": "pass",
            "provider_usage_not_double_counted": (
                "pass_guarded_attempt_history_is_authoritative"
                if args.split == "confirmatory"
                else "pass_cumulative_stats_only"
            ),
            "manifest_primary_provider_tokens": manifest_primary_tokens,
            "currency_requires_frozen_price_snapshot": "pass",
            "thesis_write": "not_performed",
        },
    }
    output_dir = args.output_dir / args.ledger_id
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Ledger output already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_atomic(output_dir / "cost_ledger.json", ledger)
    (output_dir / "cost_ledger.md").write_text(
        render_markdown(ledger), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "ledger_id": args.ledger_id,
                "output_dir": str(output_dir),
                "runs": len(records),
                "totals_by_role": ledger["totals_by_role"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
