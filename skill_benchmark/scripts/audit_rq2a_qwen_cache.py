#!/usr/bin/env python3
"""Audit exact RQ2a Qwen payload/cache coverage without network access."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from rq2a_selector_common import (
    FIELD_ORDER,
    PROTOCOL_VERSION,
    SERIALISER_VERSION,
    audit_token_count,
    load_run_data,
    repo_root,
    sha256_file,
    sha256_text,
    utc_timestamp,
    write_json_atomic,
)
from run_rq2a_field_aware_selector import field_component_text
from run_rq2a_fixed_candidate_matrix import (
    QWEN_BASE_URL,
    QWEN_DIMENSIONS,
    QWEN_MODEL,
    RQ2aEmbeddingClient,
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


def validate_legacy_cache_payload(
    path: Path,
    *,
    text: str,
    dimensions: int,
) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    vector = payload.get("embedding")
    if not isinstance(vector, list) or len(vector) != dimensions:
        raise ValueError(f"Invalid {dimensions}-dimension cache entry: {path}")
    converted = [float(value) for value in vector]
    if any(not math.isfinite(value) for value in converted):
        raise ValueError(f"Non-finite legacy cache entry: {path}")
    recorded_hash = payload.get("text_sha256")
    if recorded_hash is not None and recorded_hash != sha256_text(text):
        raise ValueError(f"Cache text hash mismatch: {path}")


def cache_state(
    client: RQ2aEmbeddingClient,
    text: str,
) -> tuple[str, str | None]:
    current = client.cache_path(text)
    if current.exists():
        client.load_current_cache(text, current)
        return "current", str(current)
    for legacy, _ in client.legacy_cache_paths(text):
        if legacy.exists():
            validate_legacy_cache_payload(
                legacy, text=text, dimensions=client.dimensions
            )
            return "legacy", str(legacy)
    return "missing", None


def category_summary(
    client: RQ2aEmbeddingClient,
    texts: set[str],
    *,
    batch_size: int,
) -> dict[str, Any]:
    counts = {"current": 0, "legacy": 0, "missing": 0}
    missing_hashes: list[str] = []
    current_entries: list[dict[str, str]] = []
    legacy_entries: list[dict[str, str]] = []
    missing_tokens = 0
    maximum_tokens = 0
    for text in sorted(texts):
        token_count = audit_token_count(text)
        maximum_tokens = max(maximum_tokens, token_count)
        state, raw_path = cache_state(client, text)
        counts[state] += 1
        if state in {"current", "legacy"}:
            if raw_path is None:
                raise ValueError("Cache state has no backing path")
            entry = {
                "text_sha256": sha256_text(text),
                "path": raw_path,
                "file_sha256": sha256_file(Path(raw_path)),
            }
            if state == "current":
                current_entries.append(entry)
            else:
                legacy_entries.append(entry)
        if state == "missing":
            missing_hashes.append(sha256_text(text))
            missing_tokens += token_count
    return {
        "unique_text_count": len(texts),
        "current_cache_hits": counts["current"],
        "legacy_exact_hits": counts["legacy"],
        "cache_misses": counts["missing"],
        "estimated_api_calls": math.ceil(counts["missing"] / batch_size),
        "missing_audit_tokens": missing_tokens,
        "maximum_audit_tokens": maximum_tokens,
        "missing_text_sha256": sorted(missing_hashes),
        "current_cache_entries": sorted(
            current_entries, key=lambda row: row["text_sha256"]
        ),
        "legacy_cache_entries": sorted(
            legacy_entries, key=lambda row: row["text_sha256"]
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# RQ2a Qwen Exact-Cache Audit",
        "",
        "This audit performs no network request and stores no plaintext payload.",
        "",
        f"- Split: `{report['split']}`",
        f"- Clusters/prompts: {report['cluster_count']}/{report['prompt_count']}",
        f"- Model/dimension: `{report['model']}`/{report['dimensions']}",
        "",
        "| Category | Unique | Current | Legacy | Missing | Estimated calls | Missing audit tokens | Max audit tokens |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, row in report["categories"].items():
        lines.append(
            f"| `{name}` | {row['unique_text_count']} | "
            f"{row['current_cache_hits']} | {row['legacy_exact_hits']} | "
            f"{row['cache_misses']} | {row['estimated_api_calls']} | "
            f"{row['missing_audit_tokens']} | {row['maximum_audit_tokens']} |"
        )
    lines.extend(
        [
            "",
            "Estimated calls use the frozen batch size. Audit-token counts are a "
            "local no-truncation/accounting measure, not provider billing tokens.",
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
        "--split", choices=["development", "confirmatory"], default="development"
    )
    parser.add_argument(
        "--representations", nargs="+", default=ALL_REPRESENTATIONS
    )
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--cache-dir", type=Path, default=root / "cache" / "rq2a")
    parser.add_argument(
        "--legacy-cache-dir",
        type=Path,
        default=root / "runtime" / "provider_cache",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs" / "rq2a_matched_content" / "analysis",
    )
    parser.add_argument("--audit-id", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.batch_size < 1:
        raise ValueError("--batch-size must be positive")
    protocol, prompts, indexes = load_run_data(
        args.input_dir,
        args.split,
        args.representations,
        None,
    )
    client = RQ2aEmbeddingClient(
        provider="qwen",
        base_url=QWEN_BASE_URL,
        api_key="unused-offline-audit",
        model=QWEN_MODEL,
        dimensions=QWEN_DIMENSIONS,
        cache_dir=args.cache_dir,
        timeout_seconds=1,
        max_audit_tokens=8192,
        legacy_cache_dir=args.legacy_cache_dir,
    )
    documents = {
        row["selector_visible_text"]
        for index in indexes.values()
        for row in index.values()
    }
    queries = {row["query_text"] for row in prompts}
    fielded = indexes["same-facts-fielded"]
    components: set[str] = set()
    for key, row in fielded.items():
        for field in FIELD_ORDER:
            text = field_component_text(
                field,
                row["canonical_fields"][field],
                protocol["field_labels"],
            )
            if text not in row["selector_visible_text"]:
                raise ValueError(
                    f"{key}/{field}: component is not an exact fielded block"
                )
            components.add(text)
    categories = {
        "single_vector_documents": category_summary(
            client, documents, batch_size=args.batch_size
        ),
        "queries": category_summary(client, queries, batch_size=args.batch_size),
        "field_components": category_summary(
            client, components, batch_size=args.batch_size
        ),
        "combined_unique_payload": category_summary(
            client, documents | queries | components, batch_size=args.batch_size
        ),
    }
    report = {
        "schema_version": "rq2a-qwen-cache-audit-v2",
        "protocol_version": PROTOCOL_VERSION,
        "serialiser_version": SERIALISER_VERSION,
        "audit_id": args.audit_id,
        "created_utc": utc_timestamp(),
        "network_requests": 0,
        "split": args.split,
        "cluster_count": len({row["cluster_id"] for row in prompts}),
        "prompt_count": len(prompts),
        "representations": args.representations,
        "model": QWEN_MODEL,
        "dimensions": QWEN_DIMENSIONS,
        "base_url": QWEN_BASE_URL,
        "batch_size": args.batch_size,
        "input_artifacts": {
            "protocol": sha256_file(args.input_dir / "protocol.json"),
            "prompts": sha256_file(args.input_dir / "prompts.jsonl"),
            "representations": {
                name: sha256_file(
                    args.input_dir / "representations" / f"{name}.jsonl"
                )
                for name in args.representations
            },
        },
        "categories": categories,
        "quality_checks": {
            "exact_cache_keys": "pass",
            "embedding_dimensions": "pass_for_existing_entries",
            "current_cache_metadata": "pass_exact_provider_endpoint_model_dimension_text",
            "existing_cache_file_hashes_frozen": "pass",
            "field_components_are_exact_substrings": "pass",
            "no_network": "pass",
            "plaintext_payload_written": False,
            "confirmatory_scores_read": False,
            "thesis_write": "not_performed",
        },
    }
    output_dir = args.output_dir / args.audit_id
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Audit output already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_atomic(output_dir / "qwen_cache_audit.json", report)
    (output_dir / "qwen_cache_audit.md").write_text(
        render_markdown(report), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "audit_id": args.audit_id,
                "output_dir": str(output_dir),
                "network_requests": 0,
                "categories": {
                    name: {
                        key: value
                        for key, value in row.items()
                        if key not in {
                            "missing_text_sha256",
                            "current_cache_entries",
                            "legacy_cache_entries",
                        }
                    }
                    for name, row in categories.items()
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
