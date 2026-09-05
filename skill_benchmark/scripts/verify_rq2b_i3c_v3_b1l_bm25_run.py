#!/usr/bin/env python3
"""Fail-closed post-run verification for the local-only RQ2b V3 B1L BM25 run."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from prepare_rq2b_i3c_v3_b1l_preflight import PREFLIGHT_ROOT, REPRESENTATIONS
from rq2b_common import read_json, relative, repo_root, require, sha256_file, write_json_new
from rq2b_v11_execution_contract import validate_b1_row
from run_rq2b_i3c_v3_b1l_bm25 import (
    EXECUTION_RECEIPT,
    RUNNER_VERSION,
    RUN_ROOT,
    GlobalBM25,
    verify_preflight,
)


VERSION = "rq2b-i3c-v3-b1l-bm25-postrun-verifier-v1"
SUMMARY_NAME = "b1l_bm25_run_summary.json"
RESULTS_NAME = "b1l_strict_results.jsonl"
REPORT_NAME = "b1l_bm25_postrun_integrity_report.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        require(bool(raw), f"blank JSONL line: {path}:{line_number}")
        value = json.loads(raw)
        require(isinstance(value, dict), f"non-object JSONL row: {path}:{line_number}")
        rows.append(value)
    return rows


def latency(values: list[float]) -> dict[str, float | int]:
    require(bool(values), "empty latency distribution")
    ordered = sorted(values)
    return {
        "observations": len(values),
        "total_seconds": sum(values),
        "mean_seconds": statistics.mean(values),
        "median_seconds": statistics.median(values),
        "p95_seconds": ordered[round((len(ordered) - 1) * 0.95)],
    }


def metric_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(bool(rows), "cannot summarise empty row set")
    return {
        "prompts": len(rows),
        "strict_hit_at_1": sum(int(row["strict_hit_at_1"]) for row in rows) / len(rows),
        "strict_recall_at_5": sum(int(row["strict_recall_at_5"]) for row in rows) / len(rows),
        "strict_recall_at_20": sum(int(row["strict_recall_at_20"]) for row in rows) / len(rows),
        "strict_recall_at_50": sum(int(row["strict_recall_at_50"]) for row in rows) / len(rows),
        "strict_recall_at_100": sum(int(row["strict_recall_at_100"]) for row in rows) / len(rows),
        "strict_mrr_at_10": sum(float(row["strict_mrr_at_10"]) for row in rows) / len(rows),
        "query_latency": latency([float(row["query_seconds"]) for row in rows]),
    }


def verify(root: Path) -> dict[str, Any]:
    preflight, representations, prompts = verify_preflight(root)
    prompt_by_id = {str(prompt["prompt_id"]): prompt for prompt in prompts}
    require(len(prompt_by_id) == 381, "strict prompt identity drift")

    run_root = root / RUN_ROOT
    summary_path = run_root / SUMMARY_NAME
    results_path = run_root / RESULTS_NAME
    require(run_root.is_dir() and summary_path.is_file() and results_path.is_file(), "B1L run artifacts are absent")
    summary = read_json(summary_path)
    require(summary.get("state") == "local_b1l_bm25_completed_pending_warm_verification_and_user_result_review", "B1L run state mismatch")
    require(summary.get("network_calls") == 0 and summary.get("external_api_calls") == 0, "B1L run used external calls")
    require(summary.get("thesis_result_writing") is False, "B1L run wrote thesis results")
    require(summary.get("results", {}).get("sha256") == sha256_file(results_path), "B1L result hash drift")
    require(int(summary.get("results", {}).get("rows", -1)) == preflight["b1l_expected_result_rows"] == 1524, "B1L result count binding mismatch")

    receipt_path = root / EXECUTION_RECEIPT
    require(receipt_path.is_file(), "B1L execution receipt absent")
    receipt = read_json(receipt_path)
    require(receipt.get("state") == "explicitly_approved_for_v3_b1l_local_bm25_once", "B1L execution receipt state mismatch")

    rows = read_jsonl(results_path)
    require(len(rows) == 1524, "B1L JSONL row count mismatch")
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        require(row.get("runner_version") == RUNNER_VERSION and row.get("retriever") == "bm25", "B1L runner/retriever drift")
        prompt_id = str(row.get("prompt_id"))
        require(prompt_id in prompt_by_id, f"unknown B1L prompt: {prompt_id}")
        validate_b1_row(row, prompt_by_id[prompt_id], f"b1l:{row.get('representation')}:{prompt_id}")
        key = (str(row["representation"]), prompt_id)
        require(key not in indexed, f"duplicate B1L row: {key}")
        indexed[key] = row
    expected = {(representation, prompt_id) for representation in REPRESENTATIONS for prompt_id in prompt_by_id}
    require(set(indexed) == expected, "B1L representation/prompt matrix is incomplete or has extras")

    by_condition: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_representation: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_condition[(str(row["representation"]), str(row["stratum"]))].append(row)
        by_representation[str(row["representation"])].append(row)

    expected_strata = {"controlled": 243, "public_gold": 138}
    strict_summary: dict[str, Any] = {}
    for representation in REPRESENTATIONS:
        for stratum, expected_count in expected_strata.items():
            condition_rows = by_condition[(representation, stratum)]
            require(len(condition_rows) == expected_count, f"B1L stratum count mismatch: {representation}/{stratum}")
            strict_summary[f"{representation}/{stratum}"] = metric_summary(condition_rows)
        strict_summary[f"{representation}/combined"] = metric_summary(by_representation[representation])

    index_report: dict[str, Any] = {}
    for representation in REPRESENTATIONS:
        artifact = summary["indexes"][representation]
        index_path = root / artifact["path"]
        require(index_path.is_file() and sha256_file(index_path) == artifact["sha256"], f"B1L index hash drift: {representation}")
        warm = summary["warm_verification"][representation]
        require(warm.get("persisted_index_sha256") == artifact["sha256"], f"B1L warm/index hash mismatch: {representation}")
        require(int(warm.get("verified_prompts", -1)) == len(prompts), f"B1L warm verification coverage mismatch: {representation}")
        index = GlobalBM25.from_persisted(read_json(index_path))
        for prompt in prompts:
            expected_top100 = [entry["skill_id"] for entry in indexed[(representation, prompt["prompt_id"])]["top_100"]]
            actual_top100 = [skill_id for skill_id, _ in index.rank(prompt["prompt"])[:100]]
            require(actual_top100 == expected_top100, f"B1L post-run replay mismatch: {representation}:{prompt['prompt_id']}")
        index_report[representation] = {
            "index_sha256": artifact["sha256"],
            "build_seconds": artifact["build_seconds"],
            "selector_visible_tokens": artifact["selector_visible_tokens"],
            "warm_replay_prompts": len(prompts),
            "warm_replay_seconds_recorded_by_runner": warm["warm_query_seconds"],
        }

    return {
        "schema_version": VERSION,
        "state": "postrun_integrity_verified_pending_user_result_review",
        "version_id": preflight["version_id"],
        "inputs": {
            "preflight_report": preflight["state"],
            "execution_receipt": {"path": relative(receipt_path, root), "sha256": sha256_file(receipt_path)},
            "results": {"path": relative(results_path, root), "sha256": sha256_file(results_path), "rows": len(rows)},
        },
        "matrix": {"representations": list(REPRESENTATIONS), "strict_prompts": len(prompts), "rows": len(rows)},
        "strict_gold_metrics": strict_summary,
        "local_cost_and_warm_replay": index_report,
        "network_calls": 0,
        "external_api_calls": 0,
        "thesis_result_writing": False,
    }


def self_test() -> dict[str, Any]:
    values = metric_summary([
        {"strict_hit_at_1": 1, "strict_recall_at_5": 1, "strict_recall_at_20": 1, "strict_recall_at_50": 1, "strict_recall_at_100": 1, "strict_mrr_at_10": 1.0, "query_seconds": 0.1},
        {"strict_hit_at_1": 0, "strict_recall_at_5": 1, "strict_recall_at_20": 1, "strict_recall_at_50": 1, "strict_recall_at_100": 1, "strict_mrr_at_10": 0.5, "query_seconds": 0.2},
    ])
    require(values["strict_hit_at_1"] == 0.5 and values["strict_mrr_at_10"] == 0.75, "post-run metric self-test failed")
    return {"schema_version": VERSION, "state": "self_test_passed", "network_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.verify, "choose exactly one of --self-test or --verify")
    if args.self_test:
        result = self_test()
    else:
        root = args.root.resolve()
        result = verify(root)
        output = root / RUN_ROOT / REPORT_NAME
        require(not output.exists(), "refusing to overwrite post-run integrity report")
        write_json_new(output, result)
        result = {**result, "report": {"path": relative(output, root), "sha256": sha256_file(output)}}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
