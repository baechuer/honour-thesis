#!/usr/bin/env python3
"""Independently verify the completed strict-only RQ2b V3 Qwen B2 run locally."""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from prepare_rq2bv1_v3_b2_top20_preflight import (
    PREFLIGHT_DIR,
    ROOT,
    read_json,
    read_jsonl,
    relative,
    require,
    sha256_file,
    sha256_json,
    write_json,
)
from run_rq2bv1_v3_b2_qwen_reranker import (
    ENDPOINT,
    MODEL,
    OUTPUT_DIR,
    RUNNER_VERSION,
    aggregate,
    parse_scores,
    provider_payload,
)
from verify_rq2bv1_v3_b2_top20_preflight import verify as verify_preflight


VERIFICATION_NAME = "post_run_verification.json"
SUMMARY_NAME = "post_run_summary.json"


def _timing(values: list[float]) -> dict[str, float]:
    require(values and all(math.isfinite(value) and value >= 0.0 for value in values), "Invalid timing series")
    ordered = sorted(values)
    def percentile(q: float) -> float:
        return float(ordered[max(0, math.ceil(q * len(ordered)) - 1)])
    return {"mean_seconds": mean(values), "p50_seconds": percentile(0.50), "p95_seconds": percentile(0.95), "max_seconds": max(values)}


def _metric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    require(rows, "Cannot summarise empty B2 group")
    eligible = [row for row in rows if int(row["strict_candidate_positive"])]
    return {
        "conditions": len(rows),
        "first_stage_recall_at_20": mean(float(row["strict_candidate_positive"]) for row in rows),
        "conditional_strict_hit_at_1": None if not eligible else mean(float(row["reranked_strict_top1"]) for row in eligible),
        "conditional_denominator": len(eligible),
        "end_to_end_strict_hit_at_1": mean(float(row["end_to_end_strict_top1"]) for row in rows),
        "end_to_end_strict_mrr_at_20": mean(float(row["end_to_end_strict_mrr_at_20"]) for row in rows),
        "first_stage_strict_hit_at_1": mean(float(row["first_stage_strict_top1"]) for row in rows),
        "reranker_gains": sum(int(row["strict_reranker_gain"]) for row in rows),
        "reranker_regressions": sum(int(row["strict_reranker_regression"]) for row in rows),
        "rerank_latency": _timing([float(row["rerank_seconds"]) for row in rows]),
        "provider_windows": {
            "total": sum(int(row["provider_document_count"]) for row in rows),
            "mean_per_condition": mean(float(row["provider_document_count"]) for row in rows),
            "max_per_condition": max(int(row["provider_document_count"]) for row in rows),
        },
    }


def _load_bound(root: Path, binding: dict[str, Any], label: str) -> Path:
    path = root / str(binding["path"])
    require(path.is_file(), f"Missing {label}: {path}")
    require(sha256_file(path) == binding["sha256"], f"{label} hash drift")
    return path


def verify(root: Path, output_dir: Path, preflight_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    preflight = verify_preflight(root, preflight_dir)
    manifest_path = output_dir / "manifest.json"
    manifest = read_json(manifest_path)
    require(manifest["state"] == "completed_pending_local_verification", "Unexpected B2 Qwen run state")
    require(manifest["method"] == {"model": MODEL, "endpoint": ENDPOINT, "instruct": "Given a user request, rank skill documents by their usefulness for completing the request.", "window_aggregation": "maximum_window_score"}, "B2 Qwen method drift")
    require(manifest["thesis_result_writing"] is False, "B2 run must not write thesis results")

    bound_preflight = manifest["preflight_manifest"]
    require(bound_preflight["path"] == relative(preflight_dir / "manifest.json", root), "B2 preflight path drift")
    require(bound_preflight["sha256"] == sha256_file(preflight_dir / "manifest.json"), "B2 preflight hash drift")
    rows_path = _load_bound(root, manifest["artifacts"]["rows"], "B2 result rows")
    ledger_path = _load_bound(root, manifest["artifacts"]["ledger"], "B2 ledger")
    rows, ledger = read_jsonl(rows_path), read_json(ledger_path)
    conditions = read_jsonl(preflight_dir / "conditions.jsonl")
    strict_bindings = read_jsonl(preflight_dir / "strict_bindings.jsonl")
    require(len(rows) == len(conditions) == len(strict_bindings) == 4572, "B2 completion coverage drift")

    strict_by_id = {row["condition_id"]: row for row in strict_bindings}
    condition_by_key = {
        (row["first_stage_retriever"], row["representation"], row["prompt_id"]): row
        for row in conditions
    }
    require(len(condition_by_key) == len(conditions), "Duplicate B2 condition key")
    seen: set[tuple[str, str, str]] = set()
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row["first_stage_retriever"], row["representation"], row["prompt_id"])
        require(key in condition_by_key and key not in seen, f"Unbound or duplicate B2 result: {key}")
        seen.add(key)
        condition = condition_by_key[key]
        strict = strict_by_id[condition["condition_id"]]
        require(row["schema_version"] == "rq2bv1-v3-b2-strict-result-row-v1", "B2 row schema drift")
        require(row["runner_version"] == RUNNER_VERSION and row["reranker"] == MODEL, "B2 runner/model drift")
        require(row["candidate_skill_ids"] == condition["candidate_skill_ids"], "B2 candidate order drift")
        require(row["candidate_list_sha256"] == condition["candidate_list_sha256"], "B2 candidate hash drift")
        require(row["prompt_sha256"] == condition["prompt_sha256"], "B2 prompt hash drift")
        require(row["gold_skill"] == strict["gold_skill"] and row["stratum"] == strict["stratum"] and row["group"] == strict["group"], "B2 strict binding drift")
        require(set(row["reranked_skill_ids"]) == set(row["candidate_skill_ids"]) and len(row["reranked_skill_ids"]) == 20, "B2 reranked candidate coverage drift")
        payload, windows = provider_payload(condition)
        require(row["provider_document_count"] == len(windows), "B2 provider window count drift")
        require(row["provider_request_sha256"] == sha256_json(payload), "B2 provider payload drift")
        gold_rank = row["reranked_skill_ids"].index(row["gold_skill"]) + 1 if row["gold_skill"] in row["reranked_skill_ids"] else None
        require(row["strict_candidate_positive"] == int(row["gold_skill"] in row["candidate_skill_ids"]), "B2 candidate-positive drift")
        require(row["end_to_end_strict_top1"] == int(row["reranked_skill_ids"][0] == row["gold_skill"]), "B2 end-to-end hit drift")
        require(abs(float(row["end_to_end_strict_mrr_at_20"]) - (0.0 if gold_rank is None else 1.0 / gold_rank)) <= 1e-12, "B2 MRR drift")
        require(row["conditional_strict_top1_denominator"] == row["strict_candidate_positive"], "B2 conditional denominator drift")
        groups[(row["first_stage_retriever"], row["representation"], row["stratum"])].append(row)
    require(len(seen) == 4572, "B2 matrix coverage drift")

    records = output_dir / "records"
    attempts = sorted(records.glob("*_attempt.json"))
    successes = sorted(records.glob("*_success.json"))
    failures = sorted(records.glob("*_failure.json"))
    require(len(attempts) == len(successes) == len(rows) and not failures, "B2 request-record completion drift")
    for index, (row, condition, strict) in enumerate(zip(rows, conditions, strict_bindings, strict=True), start=1):
        base = records / f"{index:05d}"
        attempt, success = read_json(base.with_name(base.name + "_attempt.json")), read_json(base.with_name(base.name + "_success.json"))
        payload, windows = provider_payload(condition)
        require(attempt == {"state": "persisted_before_provider_call", "automatic_retry": False, "condition_id": condition["condition_id"], "payload": payload}, "B2 persisted attempt drift")
        scores = parse_scores(success["response"], len(windows))
        replay = aggregate(condition, strict, scores, float(success["elapsed_seconds"]))
        require(replay == row, f"B2 warm replay mismatch: {index}")
    require(ledger == {"network_calls": 4572, "successful_calls": 4572, "automatic_retries": 0, "provider_total_tokens": ledger["provider_total_tokens"]}, "B2 ledger contract drift")
    require(isinstance(ledger["provider_total_tokens"], int) and ledger["provider_total_tokens"] >= 0, "B2 token ledger drift")

    verification = {
        "schema_version": "rq2bv1-v3-b2-qwen-post-run-verification-v1",
        "state": "passed_local_post_run_integrity_verification",
        "run_manifest": {"path": relative(manifest_path, root), "sha256": sha256_file(manifest_path)},
        "preflight": {"path": relative(preflight_dir / "manifest.json", root), "sha256": sha256_file(preflight_dir / "manifest.json")},
        "checks": {
            **preflight["checks"],
            "strict_b2_rows_validated": len(rows),
            "request_attempt_records": len(attempts),
            "successful_response_records": len(successes),
            "failure_records": 0,
            "automatic_retries": 0,
            "warm_replay_conditions": len(rows),
        },
        "thesis_result_writing": False,
    }
    summary = {
        "schema_version": "rq2bv1-v3-b2-qwen-post-run-summary-v1",
        "state": "completed_pending_user_result_review",
        "scope": {"reranker": MODEL, "top_k": 20, "conditions": len(rows), "representations": ["i1-discovery", "i2-original", "i3-flat-evidence", "i3c-fielded-evidence"], "first_stage_retrievers": ["bm25", "qwen-text-embedding-v4", "skillrouter-embedding"], "window_aggregation": "maximum_window_score"},
        "provider_execution": ledger,
        "by_first_stage_and_representation": {
            f"{retriever}/{representation}": {
                "overall": _metric([row for row in rows if row["first_stage_retriever"] == retriever and row["representation"] == representation]),
                "controlled": _metric(groups[(retriever, representation, "controlled")]),
                "public_gold": _metric(groups[(retriever, representation, "public_gold")]),
            }
            for retriever in ("bm25", "qwen-text-embedding-v4", "skillrouter-embedding-0.6b")
            for representation in ("i1-discovery", "i2-original", "i3-flat-evidence", "i3c-fielded-evidence")
        },
        "interpretation_boundary": "This validates Qwen B2 reranking over frozen B1 Top-20 candidates only. It does not establish full RQ2b completion, paired significance, downstream execution success, or the separately planned SkillRouter B2 reranker.",
        "thesis_result_writing": False,
    }
    return verification, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path(OUTPUT_DIR))
    parser.add_argument("--preflight-dir", type=Path, default=Path(PREFLIGHT_DIR))
    args = parser.parse_args()
    require(args.verify, "Pass --verify to run the local post-run verifier")
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    preflight_dir = args.preflight_dir if args.preflight_dir.is_absolute() else ROOT / args.preflight_dir
    verification_path, summary_path = output_dir / VERIFICATION_NAME, output_dir / SUMMARY_NAME
    require(not verification_path.exists() and not summary_path.exists(), "Refusing to overwrite B2 Qwen verification artifacts")
    verification, summary = verify(ROOT, output_dir, preflight_dir)
    write_json(verification_path, verification)
    write_json(summary_path, summary)
    print({"state": verification["state"], "verification": relative(verification_path, ROOT), "summary": relative(summary_path, ROOT)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
