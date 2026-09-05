#!/usr/bin/env python3
"""Assemble the frozen RQ2b cost decomposition without changing conclusions."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any

from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    verify_i3c_retrieval_ready,
    version_root,
    write_json_new,
)


AMORTIZATION_QUERIES = (1, 10, 100, 1_000, 10_000, 100_000)
QWEN_ROLE_CATEGORIES = (
    "document_only",
    "query_only",
    "shared_document_and_query",
)


def amortized_cost(
    *,
    offline: float,
    document_indexing: float,
    query_embedding: float,
    search: float,
    rerank: float,
) -> list[dict[str, float]]:
    return [
        {
            "queries": count,
            "amortized_cost_per_query": (
                (offline + document_indexing) / count
                + query_embedding
                + search
                + rerank
            ),
        }
        for count in AMORTIZATION_QUERIES
    ]


def percentile(values: list[float], probability: float) -> float:
    require(bool(values), "Cannot compute an empty cost percentile")
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def distribution_summary(values: list[float]) -> dict[str, float | int]:
    require(bool(values), "Latency series is empty")
    return {
        "observations": len(values),
        "total": sum(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
    }


def latency_summary(values: list[float]) -> dict[str, float | int]:
    values_summary = distribution_summary(values)
    return {
        "observations": values_summary["observations"],
        "total_seconds": values_summary["total"],
        "mean_seconds": values_summary["mean"],
        "median_seconds": values_summary["median"],
        "p50_seconds": values_summary["p50"],
        "p95_seconds": values_summary["p95"],
    }


def run_manifests(root: Path, run_root: Path) -> list[tuple[Path, dict[str, Any]]]:
    values = [(path, read_json(path)) for path in sorted(run_root.glob("*/manifest.json"))]
    require(bool(values), f"No cost-ledger run manifests found: {run_root}")
    for path, manifest in values:
        require(manifest.get("version_id") == VERSION_ID, f"Cost-ledger run version mismatch: {path}")
    return values


def manifest_inventory(
    root: Path,
    manifests: list[tuple[Path, dict[str, Any]]],
) -> list[dict[str, str]]:
    return [
        {"path": relative(path, root), "sha256": sha256_file(path)}
        for path, _ in manifests
    ]


def verify_warm_input_bindings(
    warm: dict[str, Any],
    *,
    b1_inventory: list[dict[str, str]],
    b2_inventory: list[dict[str, str]],
) -> None:
    require(
        warm.get("inputs")
        == {
            "b1_manifests": b1_inventory,
            "b2_manifests": b2_inventory,
        },
        "Warm verification does not bind the current B1/B2 manifests",
    )


def verify_hash_binding(actual_sha256: str, expected_sha256: str, label: str) -> None:
    require(actual_sha256 == expected_sha256, f"{label} drift")


def qwen_embedding_role_accounting(
    text_rows: list[dict[str, Any]],
    request_records: list[dict[str, Any]],
) -> dict[str, Any]:
    rows_by_id = {row["text_id"]: row for row in text_rows}
    require(len(rows_by_id) == len(text_rows), "Qwen cost text IDs are not unique")
    category_by_id: dict[str, str] = {}
    categories = {
        name: {
            "inventory_texts": 0,
            "inventory_local_proxy_tokens": 0,
            "inventory_utf8_bytes": 0,
            "external_text_submissions": 0,
            "external_submission_local_proxy_tokens": 0,
            "external_submission_utf8_bytes": 0,
            "successful_calls_touching_category": 0,
            "provider_seconds_attributed_by_local_proxy_tokens": 0.0,
        }
        for name in QWEN_ROLE_CATEGORIES
    }
    for text_id, row in rows_by_id.items():
        kinds = {role["kind"] for role in row["roles"]}
        require(kinds <= {"document_chunk", "query"} and bool(kinds), "Unknown Qwen text role")
        category = (
            "shared_document_and_query"
            if kinds == {"document_chunk", "query"}
            else "query_only"
            if kinds == {"query"}
            else "document_only"
        )
        category_by_id[text_id] = category
        categories[category]["inventory_texts"] += 1
        categories[category]["inventory_local_proxy_tokens"] += int(row["local_proxy_tokens"])
        categories[category]["inventory_utf8_bytes"] += int(row["utf8_bytes"])

    submitted_role_text_pairs: set[tuple[str, str]] = set()
    submitted_ids: set[str] = set()
    query_seconds_by_text_id: dict[str, float] = {}
    document_request_calls = 0
    cold_query_request_calls = 0
    total_provider_seconds = 0.0
    for request in request_records:
        request_role = request.get("request_role")
        require(
            request_role in {"document_batch", "cold_query_single"},
            "Qwen request lacks a valid document/query role",
        )
        text_ids = list(request["text_ids"])
        require(bool(text_ids) and len(text_ids) == len(set(text_ids)), "Qwen request text IDs are invalid")
        require(set(text_ids) <= set(rows_by_id), "Qwen request references an unknown text ID")
        require(
            not ({(request_role, text_id) for text_id in text_ids} & submitted_role_text_pairs),
            "Qwen text was submitted more than once for the same execution role",
        )
        submitted_role_text_pairs.update((request_role, text_id) for text_id in text_ids)
        submitted_ids.update(text_ids)
        if request_role == "document_batch":
            document_request_calls += 1
            require(
                all(any(role["kind"] == "document_chunk" for role in rows_by_id[text_id]["roles"]) for text_id in text_ids),
                "Qwen document request contains a non-document text",
            )
        else:
            cold_query_request_calls += 1
            require(len(text_ids) == 1, "Qwen cold-query request batch size is not one")
            require(
                any(role["kind"] == "query" for role in rows_by_id[text_ids[0]]["roles"]),
                "Qwen cold-query request contains a non-query text",
            )
        request_seconds = float(request["request_seconds"])
        require(math.isfinite(request_seconds) and request_seconds >= 0.0, "Qwen request time is invalid")
        total_provider_seconds += request_seconds
        text_timings = request.get("text_timings")
        require(isinstance(text_timings, list) and len(text_timings) == len(text_ids), "Qwen request text timings are incomplete")
        timing_by_id = {row.get("text_id"): row for row in text_timings}
        require(set(timing_by_id) == set(text_ids), "Qwen request text-timing identity mismatch")
        require(
            abs(
                sum(float(row["allocated_request_seconds"]) for row in text_timings)
                - request_seconds
            )
            <= 1e-9,
            "Qwen request text timings do not conserve provider time",
        )
        touched = {category_by_id[text_id] for text_id in text_ids}
        for category in touched:
            categories[category]["successful_calls_touching_category"] += 1
        for text_id in text_ids:
            row = rows_by_id[text_id]
            category = category_by_id[text_id]
            timing = timing_by_id[text_id]
            require(
                int(timing["local_proxy_tokens"]) == int(row["local_proxy_tokens"]),
                "Qwen request text-timing token mismatch",
            )
            allocated_seconds = float(timing["allocated_request_seconds"])
            require(math.isfinite(allocated_seconds) and allocated_seconds >= 0.0, "Invalid Qwen allocated text time")
            categories[category]["external_text_submissions"] += 1
            categories[category]["external_submission_local_proxy_tokens"] += int(row["local_proxy_tokens"])
            categories[category]["external_submission_utf8_bytes"] += int(row["utf8_bytes"])
            categories[category]["provider_seconds_attributed_by_local_proxy_tokens"] += allocated_seconds
            if request_role == "cold_query_single":
                require(text_id not in query_seconds_by_text_id, "Qwen query has multiple cold-latency requests")
                query_seconds_by_text_id[text_id] = allocated_seconds
    expected_query_ids = {
        text_id
        for text_id, row in rows_by_id.items()
        if any(role["kind"] == "query" for role in row["roles"])
    }
    require(
        set(query_seconds_by_text_id) == expected_query_ids,
        "Qwen cold-query latency does not cover every unique query text",
    )
    attributed = sum(
        float(row["provider_seconds_attributed_by_local_proxy_tokens"])
        for row in categories.values()
    )
    external_submission_proxy_tokens = sum(
        int(row["external_submission_local_proxy_tokens"])
        for row in categories.values()
    )
    external_submission_utf8_bytes = sum(
        int(row["external_submission_utf8_bytes"])
        for row in categories.values()
    )
    require(abs(attributed - total_provider_seconds) <= 1e-9, "Qwen role-time attribution does not conserve time")
    return {
        "physical_unique_categories_no_double_count": categories,
        "allocation_policy": (
            "physical inventory is deduplicated by text ID; external submissions are counted by "
            "execution role, so a shared document/query text may be submitted once for document "
            "indexing and once for the mandatory cold-query measurement. Each request's wall time "
            "is conserved and allocated across its texts by local proxy-token share"
        ),
        "unique_physical_texts_submitted": len(submitted_ids),
        "external_text_submissions": len(submitted_role_text_pairs),
        "external_submission_local_proxy_tokens": external_submission_proxy_tokens,
        "external_submission_utf8_bytes": external_submission_utf8_bytes,
        "document_request_calls": document_request_calls,
        "cold_query_request_calls": cold_query_request_calls,
        "provider_seconds_total": total_provider_seconds,
        "provider_seconds_attributed_total": attributed,
        "cold_query_latency_contract": {
            "batch_size": 1,
            "unique_query_texts": len(expected_query_ids),
            "query_seconds_by_text_id": query_seconds_by_text_id,
        },
        "logical_views": {
            "document": {
                "inventory_texts_including_shared": (
                    categories["document_only"]["inventory_texts"]
                    + categories["shared_document_and_query"]["inventory_texts"]
                ),
                "inventory_local_proxy_tokens_including_shared": (
                    categories["document_only"]["inventory_local_proxy_tokens"]
                    + categories["shared_document_and_query"]["inventory_local_proxy_tokens"]
                ),
            },
            "query": {
                "inventory_texts_including_shared": (
                    categories["query_only"]["inventory_texts"]
                    + categories["shared_document_and_query"]["inventory_texts"]
                ),
                "inventory_local_proxy_tokens_including_shared": (
                    categories["query_only"]["inventory_local_proxy_tokens"]
                    + categories["shared_document_and_query"]["inventory_local_proxy_tokens"]
                ),
            },
        },
    }


def selected_i2_loading_summary(
    rows: list[dict[str, Any]],
    i2_costs: dict[str, dict[str, int]],
    *,
    stage: str,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, int]]] = {}
    for row in rows:
        if stage == "b1":
            retriever = row["retriever"]
            selected = row["top_5_skill_ids"][0]
        elif stage == "b2":
            retriever = row["first_stage_retriever"]
            selected = row["reranked_skill_ids"][0]
        else:
            raise ValueError(f"Unknown agent-loading stage: {stage}")
        require(selected in i2_costs, f"Selected skill lacks I2 loading cost: {selected}")
        key = f"{retriever}::{row['representation']}::{row['stratum']}"
        grouped.setdefault(key, []).append(i2_costs[selected])
    return {
        key: {
            "selections": len(values),
            "i2_utf8_bytes": distribution_summary([float(value["utf8_bytes"]) for value in values]),
            "i2_lexical_tokens": distribution_summary([float(value["lexical_tokens"]) for value in values]),
            "i2_qwen_proxy_tokens": distribution_summary([float(value["qwen_proxy_tokens"]) for value in values]),
        }
        for key, values in sorted(grouped.items())
    }


def self_test() -> dict[str, Any]:
    rows = amortized_cost(
        offline=100.0,
        document_indexing=50.0,
        query_embedding=1.0,
        search=0.1,
        rerank=2.0,
    )
    require(rows[0]["amortized_cost_per_query"] == 153.1, "Cost ledger N=1 self-test failed")
    require(rows[-1]["amortized_cost_per_query"] < rows[0]["amortized_cost_per_query"], "Cost amortization monotonicity failed")
    role_accounting = qwen_embedding_role_accounting(
        [
            {
                "text_id": "d",
                "local_proxy_tokens": 3,
                "utf8_bytes": 12,
                "roles": [{"kind": "document_chunk"}],
            },
            {
                "text_id": "q",
                "local_proxy_tokens": 1,
                "utf8_bytes": 4,
                "roles": [{"kind": "query"}],
            },
        ],
        [
            {
                "request_role": "document_batch",
                "text_ids": ["d"],
                "request_seconds": 3.0,
                "text_timings": [
                    {
                        "text_id": "d",
                        "local_proxy_tokens": 3,
                        "allocated_request_seconds": 3.0,
                    }
                ],
            },
            {
                "request_role": "cold_query_single",
                "text_ids": ["q"],
                "request_seconds": 1.0,
                "text_timings": [
                    {
                        "text_id": "q",
                        "local_proxy_tokens": 1,
                        "allocated_request_seconds": 1.0,
                    }
                ],
            },
        ],
    )
    require(role_accounting["provider_seconds_attributed_total"] == 4.0, "Qwen role accounting self-test failed")
    require(
        role_accounting["cold_query_latency_contract"]["query_seconds_by_text_id"] == {"q": 1.0},
        "Qwen cold query-latency self-test failed",
    )
    warm = {
        "inputs": {
            "b1_manifests": [{"path": "b1/manifest.json", "sha256": "a" * 64}],
            "b2_manifests": [{"path": "b2/manifest.json", "sha256": "b" * 64}],
        }
    }
    verify_warm_input_bindings(
        warm,
        b1_inventory=warm["inputs"]["b1_manifests"],
        b2_inventory=warm["inputs"]["b2_manifests"],
    )
    stale_warm_rejected = False
    try:
        verify_warm_input_bindings(
            warm,
            b1_inventory=[{"path": "b1/manifest.json", "sha256": "c" * 64}],
            b2_inventory=warm["inputs"]["b2_manifests"],
        )
    except ValueError:
        stale_warm_rejected = True
    require(stale_warm_rejected, "Stale warm-verification self-test failed")
    stale_qwen_rows_rejected = False
    try:
        verify_hash_binding("a" * 64, "b" * 64, "Qwen cost result rows")
    except ValueError:
        stale_qwen_rows_rejected = True
    require(stale_qwen_rows_rejected, "Stale Qwen result-row self-test failed")
    return {
        "state": "synthetic_cost_units_only",
        "queries": [row["queries"] for row in rows],
        "monotonic": True,
        "qwen_role_time_conserved": True,
        "qwen_cold_query_latency_complete": True,
        "stale_warm_verification_rejected": stale_warm_rejected,
        "stale_qwen_result_rows_rejected": stale_qwen_rows_rejected,
    }


def build(
    root: Path,
    output_path: Path,
    *,
    b1_root: Path,
    b2_root: Path,
    warm_path: Path,
    extraction_ledger_path: Path,
) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    frozen_root = version_root(root)
    representations = read_json(frozen_root / "representations" / "manifest.json")
    i3 = read_json(frozen_root / "i3c_merged" / "manifest.json")
    verify_i3c_retrieval_ready(root)
    require(
        set(representations.get("timing", {}))
        == {"source_read_decode_seconds", "i1_serialization_seconds", "i2_serialization_seconds"},
        "Representation cost timing is incomplete",
    )
    require(
        set(i3.get("timing", {}))
        == {"canonicalization_seconds", "i3c_serialization_seconds", "i3flat_serialization_seconds"},
        "I3 cost timing is incomplete",
    )
    require(not output_path.exists(), f"Refusing to overwrite RQ2b cost ledger: {output_path}")
    require(
        extraction_ledger_path.resolve()
        == (frozen_root / "i3c_extraction_execution_ledger.json").resolve(),
        "Cost ledger requires the canonical I3C execution ledger",
    )
    extraction = read_json(extraction_ledger_path)
    require(extraction.get("schema_version") == "rq2b-i3c-execution-ledger-v1", "I3C execution-ledger schema mismatch")
    require(extraction.get("state") == "complete_all_chunks_automatic_gates_passed", "I3C execution ledger is incomplete")
    require(extraction.get("version_id") == VERSION_ID, "I3C execution-ledger version mismatch")
    require(extraction.get("network_calls") == 0, "I3C execution ledger records network calls")
    for name in (
        "worker_events",
        "packet_manifest",
        "merge_manifest",
        "b1r_authorisation_packet",
        "b1r_approval_receipt",
    ):
        artifact = extraction.get(name, {})
        path = root / artifact.get("path", "")
        require(path.is_file(), f"I3C execution-ledger artifact missing: {name}")
        require(sha256_file(path) == artifact.get("sha256"), f"I3C execution-ledger artifact drift: {name}")
    b1 = run_manifests(root, b1_root)
    b2 = run_manifests(root, b2_root)
    warm = read_json(warm_path)
    require(warm.get("schema_version") == "rq2b-warm-state-verification-v1", "Warm verification schema mismatch")
    require(warm.get("version_id") == VERSION_ID, "Warm verification version mismatch")
    require(warm.get("state") == "complete_zero_external_calls_zero_model_forwards", "Warm verification is incomplete")
    require(warm.get("network_calls") == warm.get("api_calls") == warm.get("model_forwards") == 0, "Warm verification consumed compute")
    verify_warm_input_bindings(
        warm,
        b1_inventory=manifest_inventory(root, b1),
        b2_inventory=manifest_inventory(root, b2),
    )
    bm25_manifests = [(path, manifest) for path, manifest in b1 if manifest.get("schema_version") == "rq2b-bm25-run-manifest-v1"]
    qwen_manifests = [(path, manifest) for path, manifest in b1 if manifest.get("schema_version") == "rq2b-qwen-run-manifest-v1"]
    skillrouter_embedding_manifests = [
        (path, manifest)
        for path, manifest in b1
        if manifest.get("schema_version") == "rq2b-skillrouter-embedding-run-manifest-v1"
    ]
    skillrouter_manifests = [(path, manifest) for path, manifest in b2 if manifest.get("schema_version") == "rq2b-skillrouter-run-manifest-v1"]
    require(
        len(bm25_manifests) == 4
        and len(qwen_manifests)
        == len(skillrouter_embedding_manifests)
        == len(skillrouter_manifests)
        == 1,
        "Cost-ledger run matrix mismatch",
    )

    bm25_rows: dict[str, Any] = {}
    b1_selection_rows: list[dict[str, Any]] = []
    for manifest_path, manifest in bm25_manifests:
        require(manifest.get("state") == "complete_scientific_b1_local", f"Incomplete BM25 cost input: {manifest_path}")
        rows_path = root / manifest["artifacts"]["rows"]["path"]
        require(sha256_file(rows_path) == manifest["artifacts"]["rows"]["sha256"], "BM25 cost rows drift")
        rows = read_jsonl(rows_path)
        b1_selection_rows.extend(rows)
        bm25_rows[manifest["representation"]] = {
            "index_build_seconds": manifest["timing"]["index_build_seconds"],
            "index_utf8_bytes": manifest["artifacts"]["index"]["utf8_bytes"],
            "query_latency": latency_summary([float(row["query_seconds"]) for row in rows]),
        }

    qwen_manifest_path, qwen_manifest = qwen_manifests[0]
    require(qwen_manifest.get("state") == "complete_scientific_b1_external", "Incomplete Qwen cost input")
    require(qwen_manifest.get("automatic_retries") == 0, "Qwen cost input used automatic retries")
    qwen_request_artifacts = qwen_manifest["artifacts"]["request_records"]
    require(
        len(qwen_request_artifacts) == 3 * int(qwen_manifest["request_attempts"]),
        "Qwen request-ledger artifact count mismatch",
    )
    qwen_request_artifacts_by_name: dict[str, tuple[Path, dict[str, Any]]] = {}
    for artifact in qwen_request_artifacts:
        path = root / artifact["path"]
        require(sha256_file(path) == artifact["sha256"], "Qwen request-ledger artifact drift")
        require(path.name not in qwen_request_artifacts_by_name, "Duplicate Qwen request-ledger artifact name")
        qwen_request_artifacts_by_name[path.name] = (path, artifact)
    require(
        int(qwen_manifest["request_attempts"])
        == int(qwen_manifest["successful_api_calls"])
        == len(qwen_manifest["embedding_ledger"]["request_records"]),
        "Qwen completed-run request counts disagree",
    )
    for record in qwen_manifest["embedding_ledger"]["request_records"]:
        request_index = int(record["request_index"])
        artifact_names = {
            "attempt": f"request_{request_index:04d}_attempt.json",
            "response": f"request_{request_index:04d}_response.json",
            "commit": f"request_{request_index:04d}_cache_commit.json",
        }
        require(
            set(artifact_names.values()) <= set(qwen_request_artifacts_by_name),
            "Qwen request record lacks its exact attempt/response/commit artifacts",
        )
        attempt_path, _ = qwen_request_artifacts_by_name[artifact_names["attempt"]]
        response_path, response_artifact = qwen_request_artifacts_by_name[artifact_names["response"]]
        commit_path, commit_artifact = qwen_request_artifacts_by_name[artifact_names["commit"]]
        base_record = {
            key: record[key]
            for key in (
                "schema_version",
                "request_index",
                "request_role",
                "text_ids",
                "text_count",
                "local_proxy_tokens",
                "utf8_bytes",
                "automatic_retry",
            )
        }
        require(
            read_json(attempt_path) == {**base_record, "state": "attempt_started"},
            "Qwen request-attempt artifact differs from its embedded record",
        )
        response_record = {
            key: value
            for key, value in record.items()
            if key not in {"provider_response_sha256", "cache_commit_sha256", "cache_entries_written"}
        }
        require(read_json(response_path) == response_record, "Qwen response artifact differs from its embedded record")
        require(
            response_artifact["sha256"] == record["provider_response_sha256"],
            "Qwen response record is not bound to its exact artifact hash",
        )
        require(
            read_json(commit_path)
            == {
                **base_record,
                "state": "cache_commit_complete",
                "provider_response_sha256": record["provider_response_sha256"],
                "cache_entries_written": record["cache_entries_written"],
            },
            "Qwen cache-commit artifact differs from its embedded record",
        )
        require(
            commit_artifact["sha256"] == record["cache_commit_sha256"],
            "Qwen cache-commit record is not bound to its exact artifact hash",
        )
    qwen_payload_path = root / qwen_manifest["payload_manifest_path"]
    require(sha256_file(qwen_payload_path) == qwen_manifest["payload_manifest_sha256"], "Qwen cost payload drift")
    qwen_payload = read_json(qwen_payload_path)
    qwen_text_path = root / qwen_payload["text_inventory"]["path"]
    require(sha256_file(qwen_text_path) == qwen_payload["text_inventory"]["sha256"], "Qwen cost text inventory drift")
    qwen_text_rows = read_jsonl(qwen_text_path)
    document_tokens_by_representation = {name: 0 for name in ("i1-discovery", "i2-original", "i3c-fielded-evidence", "i3-flat-evidence")}
    for row in qwen_text_rows:
        for representation in {role["representation"] for role in row["roles"] if role["kind"] == "document_chunk"}:
            document_tokens_by_representation[representation] += int(row["local_proxy_tokens"])
    qwen_embedding_accounting = qwen_embedding_role_accounting(
        qwen_text_rows,
        qwen_manifest["embedding_ledger"]["request_records"],
    )
    qwen_ledger = qwen_manifest["embedding_ledger"]
    require(
        qwen_embedding_accounting["external_text_submissions"]
        == int(qwen_ledger["external_text_submissions"]),
        "Qwen role accounting does not match external submissions",
    )
    require(
        qwen_embedding_accounting["external_submission_local_proxy_tokens"]
        == int(qwen_ledger["external_submission_proxy_tokens"]),
        "Qwen role accounting does not match external submission tokens",
    )
    require(
        qwen_embedding_accounting["external_submission_utf8_bytes"]
        == int(qwen_ledger["external_submission_utf8_bytes"]),
        "Qwen role accounting does not match external submission bytes",
    )
    require(
        qwen_embedding_accounting["cold_query_request_calls"]
        == int(qwen_ledger["cold_query_requests"]),
        "Qwen role accounting does not match cold-query requests",
    )
    require(
        qwen_embedding_accounting["document_request_calls"]
        + qwen_embedding_accounting["cold_query_request_calls"]
        == int(qwen_ledger["request_attempts"]),
        "Qwen role accounting does not match request attempts",
    )
    require(
        qwen_ledger.get("cold_query_latency_contract")
        == {
            "required": True,
            "batch_size": 1,
            "one_provider_request_per_unique_query_text": True,
            "query_cache_is_not_used_to_skip_latency_measurement": True,
        },
        "Qwen cold-query latency contract mismatch",
    )
    require(
        bool(qwen_ledger["request_records"]),
        "Scientific Qwen run has no cold embedding requests for latency accounting",
    )
    qwen_embedding_overhead_seconds = (
        float(qwen_ledger["elapsed_seconds"])
        - float(qwen_embedding_accounting["provider_seconds_total"])
    )
    require(qwen_embedding_overhead_seconds >= -1e-9, "Qwen embedding wall-time decomposition is invalid")
    qwen_rows_path = root / qwen_manifest["artifacts"]["rows"]["path"]
    verify_hash_binding(
        sha256_file(qwen_rows_path),
        qwen_manifest["artifacts"]["rows"]["sha256"],
        "Qwen cost result rows",
    )
    qwen_all_rows = read_jsonl(qwen_rows_path)
    require(
        len(qwen_all_rows) == int(qwen_manifest["artifacts"]["rows"]["rows"]),
        "Qwen cost result row count drift",
    )
    qwen_rows = [row for row in qwen_all_rows if row["retriever"] == "qwen-max-chunk"]
    qwen_mean_rows = [row for row in qwen_all_rows if row["retriever"] == "qwen-mean-chunk-sensitivity"]
    query_text_ids = qwen_payload["query_text_ids"]
    require(
        set(query_text_ids.values())
        == set(qwen_embedding_accounting["cold_query_latency_contract"]["query_seconds_by_text_id"]),
        "Qwen payload queries and cold-query timing identities differ",
    )
    query_seconds_by_text_id = qwen_embedding_accounting["cold_query_latency_contract"]["query_seconds_by_text_id"]
    query_seconds_by_prompt_id = {
        prompt_id: float(query_seconds_by_text_id[text_id])
        for prompt_id, text_id in query_text_ids.items()
    }
    qwen_primary_prompt_ids = {row["prompt_id"] for row in qwen_rows}
    require(
        qwen_primary_prompt_ids == set(query_seconds_by_prompt_id),
        "Qwen primary result rows do not cover every prompt with cold-query timing",
    )
    qwen_cold_online_latency: dict[str, list[float]] = {}
    for row in qwen_rows:
        query_seconds = query_seconds_by_prompt_id[row["prompt_id"]]
        search_seconds = float(row["query_seconds"])
        require(
            math.isfinite(search_seconds) and search_seconds >= 0.0,
            "Invalid Qwen vector-search time",
        )
        key = f"{row['representation']}::{row['stratum']}"
        qwen_cold_online_latency.setdefault(key, []).append(query_seconds + search_seconds)
    b1_selection_rows.extend(qwen_rows)

    skillrouter_embedding_manifest_path, skillrouter_embedding_manifest = (
        skillrouter_embedding_manifests[0]
    )
    require(
        skillrouter_embedding_manifest.get("state")
        == "complete_scientific_b1_skillrouter_embedding",
        "Incomplete SkillRouter embedding cost input",
    )
    require(
        skillrouter_embedding_manifest.get("automatic_retries") == 0,
        "SkillRouter embedding cost input used automatic retries",
    )
    skillrouter_embedding_payload_path = root / skillrouter_embedding_manifest["payload_manifest_path"]
    require(
        sha256_file(skillrouter_embedding_payload_path)
        == skillrouter_embedding_manifest["payload_manifest_sha256"],
        "SkillRouter embedding cost payload drift",
    )
    skillrouter_embedding_payload = read_json(skillrouter_embedding_payload_path)
    skillrouter_embedding_text_path = root / skillrouter_embedding_payload["text_inventory"]["path"]
    require(
        sha256_file(skillrouter_embedding_text_path)
        == skillrouter_embedding_payload["text_inventory"]["sha256"],
        "SkillRouter embedding cost text inventory drift",
    )
    skillrouter_embedding_text_rows = read_jsonl(skillrouter_embedding_text_path)
    skillrouter_embedding_ledger_path = root / skillrouter_embedding_manifest["artifacts"]["embedding_ledger"]["path"]
    require(
        sha256_file(skillrouter_embedding_ledger_path)
        == skillrouter_embedding_manifest["artifacts"]["embedding_ledger"]["sha256"],
        "SkillRouter embedding cost ledger drift",
    )
    skillrouter_embedding_ledger = read_json(skillrouter_embedding_ledger_path)
    require(
        skillrouter_embedding_ledger == skillrouter_embedding_manifest["embedding_ledger"],
        "SkillRouter embedding manifest/ledger mismatch",
    )
    batch_records = skillrouter_embedding_ledger["batch_records"]
    require(
        len(batch_records) == int(skillrouter_embedding_ledger["model_forward_batches"]),
        "SkillRouter embedding batch-record count mismatch",
    )
    require(
        abs(
            sum(float(row["elapsed_seconds"]) for row in batch_records)
            - float(skillrouter_embedding_ledger["model_forward_seconds"])
        )
        <= 1e-9,
        "SkillRouter embedding forward-time decomposition drift",
    )
    forward_artifacts = {
        Path(artifact["path"]).name: artifact
        for artifact in skillrouter_embedding_manifest["artifacts"]["forward_records"]
    }
    require(
        len(forward_artifacts) == 2 * len(batch_records),
        "SkillRouter embedding forward-artifact count mismatch",
    )
    for record in batch_records:
        for path_key, hash_key in (
            ("attempt_path", "attempt_sha256"),
            ("success_path", "success_sha256"),
        ):
            name = record[path_key]
            require(name in forward_artifacts, f"SkillRouter embedding forward artifact missing: {name}")
            path = root / forward_artifacts[name]["path"]
            require(sha256_file(path) == record[hash_key], f"SkillRouter embedding forward artifact drift: {name}")
    skillrouter_embedding_rows_path = root / skillrouter_embedding_manifest["artifacts"]["rows"]["path"]
    require(
        sha256_file(skillrouter_embedding_rows_path)
        == skillrouter_embedding_manifest["artifacts"]["rows"]["sha256"],
        "SkillRouter embedding result rows drift",
    )
    skillrouter_embedding_rows = read_jsonl(skillrouter_embedding_rows_path)
    require(
        len(skillrouter_embedding_rows) == 4 * 401,
        "SkillRouter embedding result matrix is incomplete",
    )
    b1_selection_rows.extend(skillrouter_embedding_rows)
    skillrouter_embedding_document_tokens = {
        name: 0
        for name in ("i1-discovery", "i2-original", "i3c-fielded-evidence", "i3-flat-evidence")
    }
    for row in skillrouter_embedding_text_rows:
        for representation in {
            role["representation"]
            for role in row["roles"]
            if role["kind"] == "document"
        }:
            skillrouter_embedding_document_tokens[representation] += int(row["model_tokens"])
    skillrouter_embedding_query_tokens_workload = sum(
        int(row["model_tokens"])
        * sum(role["kind"] == "query" for role in row["roles"])
        for row in skillrouter_embedding_text_rows
    )
    skillrouter_embedding_query_seconds_by_text_id = {
        record["text_ids"][0]: float(record["elapsed_seconds"])
        for record in batch_records
        if record["role"] == "cold_query_single"
    }
    require(
        set(skillrouter_embedding_query_seconds_by_text_id)
        == set(skillrouter_embedding_payload["query_text_ids"].values()),
        "SkillRouter embedding cold-query timing coverage mismatch",
    )
    skillrouter_embedding_query_seconds_by_prompt_id = {
        prompt_id: skillrouter_embedding_query_seconds_by_text_id[text_id]
        for prompt_id, text_id in skillrouter_embedding_payload["query_text_ids"].items()
    }
    skillrouter_embedding_cold_online_latency: dict[str, list[float]] = {}
    for row in skillrouter_embedding_rows:
        search_seconds = float(row["query_seconds"])
        require(math.isfinite(search_seconds) and search_seconds >= 0.0, "Invalid SkillRouter embedding search time")
        key = f"{row['representation']}::{row['stratum']}"
        skillrouter_embedding_cold_online_latency.setdefault(key, []).append(
            skillrouter_embedding_query_seconds_by_prompt_id[row["prompt_id"]]
            + search_seconds
        )

    skillrouter_manifest_path, skillrouter_manifest = skillrouter_manifests[0]
    require(skillrouter_manifest.get("state") == "complete_scientific_b2", "Incomplete SkillRouter cost input")
    require(skillrouter_manifest.get("automatic_retries") == 0, "SkillRouter cost input used automatic retries")
    runtime_artifact = skillrouter_manifest["artifacts"]["runtime_ledger"]
    runtime_path = root / runtime_artifact["path"]
    require(sha256_file(runtime_path) == runtime_artifact["sha256"], "SkillRouter runtime-ledger drift")
    skillrouter_runtime = read_json(runtime_path)
    for manifest_key, runtime_key in (
        ("model_forward_batch_attempts", "model_forward_batch_attempts"),
        ("model_forward_batches", "model_forward_batch_successes"),
        ("model_scored_windows", "model_scored_windows"),
        ("new_model_input_tokens", "new_model_input_tokens"),
        ("model_load_seconds", "model_load_seconds"),
        ("input_preparation_seconds", "input_preparation_seconds"),
        ("model_forward_seconds", "model_forward_seconds"),
    ):
        require(skillrouter_manifest[manifest_key] == skillrouter_runtime[runtime_key], f"SkillRouter runtime count drift: {manifest_key}")
    require(
        len(skillrouter_runtime["batch_records"]) == skillrouter_manifest["model_forward_batches"],
        "SkillRouter runtime batch-record count mismatch",
    )
    require(
        bool(skillrouter_runtime["batch_records"]),
        "Scientific SkillRouter run has no cold model batches for latency accounting",
    )
    require(
        sum(int(row["window_count"]) for row in skillrouter_runtime["batch_records"])
        == skillrouter_manifest["model_scored_windows"],
        "SkillRouter runtime scored-window count mismatch",
    )
    require(
        sum(int(row["model_input_tokens"]) for row in skillrouter_runtime["batch_records"])
        == skillrouter_manifest["new_model_input_tokens"],
        "SkillRouter runtime model-input token count mismatch",
    )
    window_model_seconds: dict[str, float] = {}
    for record in skillrouter_runtime["batch_records"]:
        attempt_path = skillrouter_manifest_path.parent / record["attempt_path"]
        success_path = skillrouter_manifest_path.parent / record["success_path"]
        require(sha256_file(attempt_path) == record["attempt_sha256"], "SkillRouter batch-attempt drift")
        require(sha256_file(success_path) == record["success_sha256"], "SkillRouter batch-success drift")
        attempt = read_json(attempt_path)
        require(attempt["window_count"] == len(attempt["window_ids"]), "SkillRouter batch window-ID count drift")
        per_window_seconds = float(record["elapsed_seconds"]) / int(record["window_count"])
        for window_id in attempt["window_ids"]:
            require(window_id not in window_model_seconds, "SkillRouter window appears in multiple model batches")
            window_model_seconds[window_id] = per_window_seconds
    require(
        abs(
            float(skillrouter_runtime["model_forward_seconds"])
            - sum(float(row["elapsed_seconds"]) for row in skillrouter_runtime["batch_records"])
        )
        <= 1e-9,
        "SkillRouter forward-time decomposition drift",
    )
    skillrouter_model_overhead_seconds = (
        float(skillrouter_runtime["model_elapsed_seconds"])
        - float(skillrouter_runtime["model_load_seconds"])
        - float(skillrouter_runtime["input_preparation_seconds"])
        - float(skillrouter_runtime["model_forward_seconds"])
    )
    require(skillrouter_model_overhead_seconds >= -1e-9, "SkillRouter model wall-time decomposition is invalid")
    skillrouter_payload_path = root / skillrouter_manifest["payload_path"]
    require(sha256_file(skillrouter_payload_path) == skillrouter_manifest["payload_sha256"], "SkillRouter cost payload drift")
    skillrouter_payload = read_json(skillrouter_payload_path)
    condition_path = root / skillrouter_payload["condition_inventory"]["path"]
    pair_path = root / skillrouter_payload["pair_inventory"]["path"]
    window_path = root / skillrouter_payload["window_inventory"]["path"]
    for path, artifact in (
        (condition_path, skillrouter_payload["condition_inventory"]),
        (pair_path, skillrouter_payload["pair_inventory"]),
        (window_path, skillrouter_payload["window_inventory"]),
    ):
        require(sha256_file(path) == artifact["sha256"], f"SkillRouter cost artifact drift: {path}")
    pairs = {row["pair_id"]: row for row in read_jsonl(pair_path)}
    windows = {row["window_id"]: row for row in read_jsonl(window_path)}
    conditions = read_jsonl(condition_path)
    skillrouter_rows_path = root / skillrouter_manifest["artifacts"]["rows"]["path"]
    require(sha256_file(skillrouter_rows_path) == skillrouter_manifest["artifacts"]["rows"]["sha256"], "SkillRouter result rows drift")
    skillrouter_rows = read_jsonl(skillrouter_rows_path)
    require(len(skillrouter_rows) == len(conditions), "SkillRouter result/condition count drift")
    require(
        [row["condition_id"] for row in skillrouter_rows]
        == [row["condition_id"] for row in conditions],
        "SkillRouter result/condition identity drift",
    )
    rerank_tokens: dict[str, list[int]] = {}
    for condition in read_jsonl(condition_path):
        key = f"{condition['first_stage_retriever']}::{condition['representation']}"
        total = sum(
            int(windows[window_id]["model_input_tokens"])
            for pair_id in condition["pair_ids_by_skill"].values()
            for window_id in pairs[pair_id]["window_ids"]
        )
        rerank_tokens.setdefault(key, []).append(total)

    rerank_latency: dict[str, list[float]] = {}
    rerank_model_seconds: dict[str, list[float]] = {}
    rerank_aggregation_seconds: dict[str, list[float]] = {}
    for condition, result in zip(conditions, skillrouter_rows, strict=True):
        aggregation_seconds = float(result["rerank_aggregation_seconds"])
        require(math.isfinite(aggregation_seconds) and aggregation_seconds >= 0.0, "Invalid SkillRouter condition aggregation time")
        condition_windows = {
            window_id
            for pair_id in condition["pair_ids_by_skill"].values()
            for window_id in pairs[pair_id]["window_ids"]
        }
        attributed_model_seconds = sum(window_model_seconds.get(window_id, 0.0) for window_id in condition_windows)
        key = f"{condition['first_stage_retriever']}::{condition['representation']}::{condition['stratum']}"
        rerank_model_seconds.setdefault(key, []).append(attributed_model_seconds)
        rerank_aggregation_seconds.setdefault(key, []).append(aggregation_seconds)
        rerank_latency.setdefault(key, []).append(attributed_model_seconds + aggregation_seconds)
    require(
        sum(sum(values) for values in rerank_aggregation_seconds.values())
        <= float(skillrouter_manifest["aggregation_elapsed_seconds"]) + 1e-9,
        "SkillRouter per-condition aggregation exceeds total aggregation time",
    )

    i3_packet = read_json(frozen_root / "i3c_extraction" / "manifest.json")
    i3_identity_path = root / i3_packet["identity_manifest"]["path"]
    require(sha256_file(i3_identity_path) == i3_packet["identity_manifest"]["sha256"], "I3 identity manifest drift in cost ledger")
    i3_identity = {row["skill_id"]: row for row in read_jsonl(i3_identity_path)}
    i2_artifact = representations["artifacts"]["i2-original"]
    i2_path = root / i2_artifact["path"]
    require(sha256_file(i2_path) == i2_artifact["sha256"], "I2 representation drift in agent-loading cost")
    i2_rows = read_jsonl(i2_path)
    i2_costs = {
        row["skill_id"]: {
            "utf8_bytes": int(row["selector_visible_counts"]["utf8_bytes"]),
            "lexical_tokens": int(row["selector_visible_counts"]["lexical_tokens"]),
            "qwen_proxy_tokens": int(i3_identity[row["skill_id"]]["qwen_proxy_tokens"]),
        }
        for row in i2_rows
    }
    require(len(i2_costs) == 2433 == len(i3_identity), "I2 agent-loading identity coverage mismatch")
    agent_loading = {
        "policy": "load the complete selected I2 source artifact after selection; this is separate from selector-visible cost",
        "token_note": "Qwen proxy tokens are exact under the frozen local proxy tokenizer, not agent billing tokens",
        "b1_first_stage_top1": selected_i2_loading_summary(b1_selection_rows, i2_costs, stage="b1"),
        "b2_reranked_top1": selected_i2_loading_summary(skillrouter_rows, i2_costs, stage="b2"),
    }

    query_proxy_tokens_actual_unique = sum(
        int(row["local_proxy_tokens"])
        for row in qwen_text_rows
        if any(role["kind"] == "query" for role in row["roles"])
    )
    query_proxy_tokens_workload = sum(
        int(row["local_proxy_tokens"])
        * sum(role["kind"] == "query" for role in row["roles"])
        for row in qwen_text_rows
    )
    prompt_count = read_json(frozen_root / "manifest.json")["counts"]["prompts"]
    extraction_proxy_tokens = int(extraction["input_qwen_proxy_tokens"])
    amortization = {}
    for representation, document_tokens in document_tokens_by_representation.items():
        fixed_extraction = extraction_proxy_tokens if representation.startswith("i3") else 0
        amortization[representation] = [
            {
                "queries": count,
                "qwen_proxy_tokens_per_query": (fixed_extraction + document_tokens) / count + query_proxy_tokens_workload / prompt_count,
                "skillrouter_model_input_tokens_per_query_by_first_stage": {
                    retriever: statistics.mean(rerank_tokens[f"{retriever}::{representation}"])
                    for retriever in ("bm25", "qwen-max-chunk", "skillrouter-embedding")
                },
                "skillrouter_embedding_model_tokens_per_query": (
                    skillrouter_embedding_document_tokens[representation] / count
                    + skillrouter_embedding_query_tokens_workload / prompt_count
                ),
            }
            for count in AMORTIZATION_QUERIES
        ]

    report = {
        "schema_version": "rq2b-cost-ledger-v1",
        "version_id": VERSION_ID,
        "state": "complete_pending_user_review_not_for_thesis",
        "network_calls": 0,
        "amortization_query_counts": list(AMORTIZATION_QUERIES),
        "representation_preparation": {
            "i1_utf8_bytes": representations["summary"]["total_i1_utf8_bytes"],
            "i2_utf8_bytes": representations["summary"]["total_i2_utf8_bytes"],
            "i3c_utf8_bytes": i3["summary"]["i3c_selector_utf8_bytes"],
            "i3flat_utf8_bytes": i3["summary"]["i3flat_selector_utf8_bytes"],
            "base_representation_timing": representations["timing"],
            "i3_merge_and_serialization_timing": i3["timing"],
            "qwen_payload_preparation_timing": qwen_payload["preparation_timing"],
            "skillrouter_embedding_payload_preparation_timing": skillrouter_embedding_payload["preparation_timing"],
            "skillrouter_payload_preparation_timing": skillrouter_payload["preparation_timing"],
            "qwen_document_chunks": qwen_payload["counts"]["document_chunks"],
            "skillrouter_unique_windows": skillrouter_payload["counts"]["unique_windows"],
        },
        "offline_i3c_extraction": extraction,
        "bm25": bm25_rows,
        "qwen": {
            "manifest": {"path": relative(qwen_manifest_path, root), "sha256": sha256_file(qwen_manifest_path)},
            "embedding_ledger": qwen_ledger,
            "payload_counts": qwen_payload["counts"],
            "embedding_accounting_by_document_query_role": qwen_embedding_accounting,
            "embedding_elapsed_seconds": qwen_ledger["elapsed_seconds"],
            "embedding_non_provider_overhead_seconds": max(0.0, qwen_embedding_overhead_seconds),
            "provider_usage_total_unpartitioned": qwen_manifest["embedding_ledger"]["provider_usage"],
            "query_proxy_tokens_actual_unique_cache_workload": query_proxy_tokens_actual_unique,
            "query_proxy_tokens_prompt_instance_workload": query_proxy_tokens_workload,
            "document_proxy_tokens_by_representation": document_tokens_by_representation,
            "cold_query_embedding_latency_unique_texts": latency_summary(
                [float(value) for value in query_seconds_by_text_id.values()]
            ),
            "cold_query_embedding_latency_prompt_instances": latency_summary(
                [float(value) for value in query_seconds_by_prompt_id.values()]
            ),
            "primary_search_latency": latency_summary([float(row["query_seconds"]) for row in qwen_rows]),
            "mean_chunk_sensitivity_search_latency": latency_summary([float(row["query_seconds"]) for row in qwen_mean_rows]),
            "cold_online_first_stage_latency": {
                "method": (
                    "for each prompt and representation, add its hash-bound single-text cold query-embedding "
                    "request time to the directly measured maximum-chunk vector-search time"
                ),
                "groups": {
                    key: latency_summary(values)
                    for key, values in sorted(qwen_cold_online_latency.items())
                },
            },
        },
        "skillrouter_embedding": {
            "role": "first_stage_bi_encoder",
            "manifest": {
                "path": relative(skillrouter_embedding_manifest_path, root),
                "sha256": sha256_file(skillrouter_embedding_manifest_path),
            },
            "payload_counts": skillrouter_embedding_payload["counts"],
            "embedding_ledger": skillrouter_embedding_ledger,
            "document_model_tokens_by_representation": skillrouter_embedding_document_tokens,
            "query_model_tokens_prompt_instance_workload": skillrouter_embedding_query_tokens_workload,
            "model_load_seconds": skillrouter_embedding_ledger["model_load_seconds"],
            "model_forward_seconds": skillrouter_embedding_ledger["model_forward_seconds"],
            "vector_search_seconds": skillrouter_embedding_ledger["vector_search_seconds"],
            "cache_hits": skillrouter_embedding_ledger["cache_hits"],
            "cache_misses": skillrouter_embedding_ledger["cache_misses"],
            "cold_query_embedding_latency_unique_texts": latency_summary(
                list(skillrouter_embedding_query_seconds_by_text_id.values())
            ),
            "cold_query_embedding_latency_prompt_instances": latency_summary(
                list(skillrouter_embedding_query_seconds_by_prompt_id.values())
            ),
            "primary_search_latency": latency_summary(
                [float(row["query_seconds"]) for row in skillrouter_embedding_rows]
            ),
            "cold_online_first_stage_latency": {
                "method": "cold single-query encoder forward plus measured cosine-search time",
                "groups": {
                    key: latency_summary(values)
                    for key, values in sorted(skillrouter_embedding_cold_online_latency.items())
                },
            },
        },
        "skillrouter": {
            "role": "second_stage_cross_encoder_reranker",
            "manifest": {"path": relative(skillrouter_manifest_path, root), "sha256": sha256_file(skillrouter_manifest_path)},
            "payload_counts": skillrouter_payload["counts"],
            "cache_hits": skillrouter_manifest["cache_hits"],
            "cache_misses": skillrouter_manifest["cache_misses"],
            "model_forward_batch_attempts": skillrouter_manifest["model_forward_batch_attempts"],
            "model_forward_batches": skillrouter_manifest["model_forward_batches"],
            "model_scored_windows": skillrouter_manifest["model_scored_windows"],
            "new_model_input_tokens": skillrouter_manifest["new_model_input_tokens"],
            "model_elapsed_seconds": skillrouter_manifest["model_elapsed_seconds"],
            "model_load_seconds": skillrouter_manifest["model_load_seconds"],
            "input_preparation_seconds": skillrouter_manifest["input_preparation_seconds"],
            "model_forward_seconds": skillrouter_manifest["model_forward_seconds"],
            "model_non_load_non_preparation_non_forward_overhead_seconds": max(
                0.0, skillrouter_model_overhead_seconds
            ),
            "aggregation_elapsed_seconds": skillrouter_manifest["aggregation_elapsed_seconds"],
            "observed_model_batch_latency": latency_summary(
                [float(row["elapsed_seconds"]) for row in skillrouter_runtime["batch_records"]]
            ),
            "per_condition_attributed_model_latency": {
                key: latency_summary(values) for key, values in sorted(rerank_model_seconds.items())
            },
            "per_condition_aggregation_latency": {
                key: latency_summary(values) for key, values in sorted(rerank_aggregation_seconds.items())
            },
            "per_condition_total_reranking_latency": {
                "method": (
                    "observed batch elapsed time is allocated equally to its scored windows, then summed over "
                    "each immutable top-20 condition and added to directly timed condition aggregation"
                ),
                "groups": {
                    key: latency_summary(values) for key, values in sorted(rerank_latency.items())
                },
            },
            "runtime_ledger": {
                "path": relative(runtime_path, root),
                "sha256": sha256_file(runtime_path),
            },
            "per_condition_model_input_tokens": {
                key: distribution_summary([float(value) for value in values])
                for key, values in sorted(rerank_tokens.items())
            },
        },
        "agent_loading": agent_loading,
        "warm_verification": warm,
        "amortized_resource_curves": amortization,
        "unit_policy": (
            "tokens, bytes, calls, and model time are primary; monetary prices are "
            "date-stamped supplements and are never mixed with scientific accuracy"
        ),
        "monetary_supplement": {
            "included": False,
            "reason": "requires a separately date-stamped provider-price record",
        },
        "complete_runtime_values_pending": False,
        "thesis_write_authorized": False,
    }
    write_json_new(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--output", type=Path, default=Path("skill_benchmark/outputs/rq2b/analysis/cost_ledger.json"))
    parser.add_argument("--b1-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b1"))
    parser.add_argument("--b2-root", type=Path, default=Path("skill_benchmark/outputs/rq2b/b2"))
    parser.add_argument("--warm-verification", type=Path, default=Path("skill_benchmark/outputs/rq2b/analysis/warm_state_verification.json"))
    parser.add_argument("--extraction-ledger", type=Path, default=Path(f"skill_benchmark/rq2b_full_library/{VERSION_ID}/i3c_extraction_execution_ledger.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        root = args.root.resolve()
        output = args.output if args.output.is_absolute() else root / args.output
        b1_root = args.b1_root if args.b1_root.is_absolute() else root / args.b1_root
        b2_root = args.b2_root if args.b2_root.is_absolute() else root / args.b2_root
        warm = args.warm_verification if args.warm_verification.is_absolute() else root / args.warm_verification
        extraction = args.extraction_ledger if args.extraction_ledger.is_absolute() else root / args.extraction_ledger
        result = build(root, output, b1_root=b1_root, b2_root=b2_root, warm_path=warm, extraction_ledger_path=extraction)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
