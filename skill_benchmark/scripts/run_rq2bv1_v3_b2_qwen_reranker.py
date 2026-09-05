#!/usr/bin/env python3
"""Run the strict-only V3 B2 Qwen Top-20 reranker from frozen conditions."""

from __future__ import annotations

import argparse
import json
import math
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
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
    sha256_text,
    write_json,
    write_jsonl,
)
from verify_rq2bv1_v3_b2_top20_preflight import verify as verify_preflight


MODEL = "qwen3-rerank"
# The international DashScope qwen3-rerank API uses this endpoint with nested
# input/parameters objects.  The workspace-scoped OpenAI-compatible endpoint
# documented elsewhere is not available on the generic international host.
ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"
INSTRUCT = "Given a user request, rank skill documents by their usefulness for completing the request."
MAX_DOCUMENTS = 500
MAX_REQUEST_PROXY_TOKENS = 120000
OUTPUT_DIR = "skill_benchmark/rq2bv1/results/qwen_reranker_top20_v3"
RUNNER_VERSION = "rq2bv1-v3-b2-qwen-reranker-v3"


def load_key(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    for dotenv in (ROOT / ".env", ROOT / "skill_benchmark" / ".env"):
        if not dotenv.is_file():
            continue
        for raw in dotenv.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, candidate = line.split("=", 1)
            if key.strip() == name and candidate.strip():
                return candidate.strip().strip('"').strip("'")
    raise RuntimeError(f"Missing {name}; no provider request was made")


def provider_payload(condition: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    windows = [window for candidate in condition["candidates"] for window in candidate["windows"]]
    require(windows and len(windows) <= MAX_DOCUMENTS, "Qwen B2 document count limit exceeded")
    pair_proxy_tokens = sum(int(window.get("skillrouter_window_tokens", 0)) + int(condition["skillrouter_empty_pair_tokens"]) for window in windows)
    require(pair_proxy_tokens <= MAX_REQUEST_PROXY_TOKENS, "Qwen B2 conservative request token limit exceeded")
    payload = {
        "model": MODEL,
        "input": {
            "query": condition["query"],
            "documents": [window["text"] for window in windows],
        },
        "parameters": {
            "return_documents": False,
            "top_n": len(windows),
            "instruct": INSTRUCT,
        },
    }
    return payload, windows


def parse_scores(response: dict[str, Any], document_count: int) -> list[float]:
    results = response.get("output", {}).get("results")
    require(isinstance(results, list), "Qwen qwen3-rerank response has no output.results array")
    scores: list[float | None] = [None] * document_count
    for result in results:
        require(isinstance(result, dict), "Qwen qwen3-rerank response result is not an object")
        index, score = result.get("index"), result.get("relevance_score")
        require(isinstance(index, int) and 0 <= index < document_count, "Qwen qwen3-rerank result index is invalid")
        require(scores[index] is None, "Qwen qwen3-rerank repeats a document index")
        require(isinstance(score, (int, float)) and math.isfinite(float(score)), "Qwen qwen3-rerank score is invalid")
        scores[index] = float(score)
    require(all(score is not None for score in scores), "Qwen qwen3-rerank response omitted a requested document")
    return [float(score) for score in scores]


def aggregate(condition: dict[str, Any], strict: dict[str, Any], scores: list[float], elapsed: float) -> dict[str, Any]:
    payload, windows = provider_payload(condition)
    require(len(windows) == len(scores), "Qwen score/window length mismatch")
    by_skill: dict[str, list[float]] = {skill_id: [] for skill_id in condition["candidate_skill_ids"]}
    pair_skill = {
        window["pair_id"]: candidate["skill_id"]
        for candidate in condition["candidates"]
        for window in candidate["windows"]
    }
    require(len(pair_skill) == len(windows), "Qwen condition repeats a pair ID")
    for window, score in zip(windows, scores, strict=True):
        by_skill[pair_skill[window["pair_id"]]].append(score)
    require(all(by_skill[skill_id] for skill_id in by_skill), "Qwen score coverage missing a Top-20 candidate")
    first_rank = {skill_id: index for index, skill_id in enumerate(condition["candidate_skill_ids"], start=1)}
    ranked = sorted(
        ((skill_id, max(values)) for skill_id, values in by_skill.items()),
        key=lambda row: (-row[1], first_rank[row[0]], row[0]),
    )
    reranked_ids = [skill_id for skill_id, _ in ranked]
    gold = strict["gold_skill"]
    gold_rank = reranked_ids.index(gold) + 1 if gold in reranked_ids else None
    candidate_positive = int(gold in condition["candidate_skill_ids"])
    first_top1 = int(condition["candidate_skill_ids"][0] == gold)
    reranked_top1 = int(reranked_ids[0] == gold)
    return {
        "schema_version": "rq2bv1-v3-b2-strict-result-row-v1",
        "runner_version": RUNNER_VERSION,
        "reranker": MODEL,
        "first_stage_retriever": condition["first_stage_retriever"],
        "representation": condition["representation"],
        "prompt_id": condition["prompt_id"],
        "prompt_sha256": condition["prompt_sha256"],
        "stratum": strict["stratum"],
        "group": strict["group"],
        "gold_skill": gold,
        "candidate_skill_ids": condition["candidate_skill_ids"],
        "candidate_list_sha256": condition["candidate_list_sha256"],
        "reranked_skill_ids": reranked_ids,
        "reranked_scores": [score for _, score in ranked],
        "strict_candidate_positive": candidate_positive,
        "first_stage_strict_top1": first_top1,
        "reranked_strict_top1": reranked_top1,
        "conditional_strict_top1_numerator": int(candidate_positive and reranked_top1),
        "conditional_strict_top1_denominator": candidate_positive,
        "end_to_end_strict_top1": reranked_top1,
        "end_to_end_strict_mrr_at_20": 0.0 if gold_rank is None else 1.0 / gold_rank,
        "strict_reranker_gain": int(candidate_positive and reranked_top1 and not first_top1),
        "strict_reranker_regression": int(first_top1 and not reranked_top1),
        "rerank_seconds": elapsed,
        "primary_window_aggregation": "maximum_window_score",
        "provider_document_count": len(windows),
        "provider_request_sha256": sha256_json(payload),
    }


class ProviderRequestError(RuntimeError):
    """A single provider attempt failed; callers must not retry automatically."""

    def __init__(self, *, status: int | None, body: str, cause: str) -> None:
        super().__init__(cause)
        self.status = status
        self.body = body


def request_once(payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise ProviderRequestError(status=error.code, body=body, cause=str(error)) from error
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        raise ProviderRequestError(status=None, body="", cause=str(error)) from error


def self_test() -> dict[str, Any]:
    condition = {"query": "q", "skillrouter_empty_pair_tokens": 4, "candidates": [{"skill_id": "a", "windows": [{"text": "a", "pair_id": "p1", "skillrouter_window_tokens": 2}]}, {"skill_id": "b", "windows": [{"text": "b", "pair_id": "p2", "skillrouter_window_tokens": 2}]}]}
    condition.update({"candidate_skill_ids": ["a", "b"], "candidate_list_sha256": sha256_json(["a", "b"]), "first_stage_retriever": "synthetic", "representation": "i1-discovery", "prompt_id": "p", "prompt_sha256": sha256_text("q")})
    payload, _ = provider_payload(condition)
    require(
        ENDPOINT == "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
        "Qwen qwen3-rerank must use the international DashScope rerank endpoint",
    )
    require(set(payload) == {"model", "input", "parameters"}, "Qwen payload must use the DashScope nested shape")
    require(set(payload["input"]) == {"query", "documents"}, "Qwen payload input contract drift")
    require(payload["parameters"]["return_documents"] is False, "Qwen payload must not return selector text")
    scores = parse_scores({"output": {"results": [{"index": 1, "relevance_score": 0.9}, {"index": 0, "relevance_score": 0.1}]}}, 2)
    row = aggregate(condition, {"gold_skill": "b", "stratum": "controlled", "group": "synthetic"}, scores, 0.0)
    require(row["reranked_skill_ids"][0] == "b", "Qwen aggregate synthetic ranking failed")
    return {
        "state": "pass_synthetic_zero_network_no_provider_call",
        "network_calls": 0,
        "endpoint": ENDPOINT,
        "nested_qwen3_rerank_body": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--preflight-dir", type=Path, default=Path(PREFLIGHT_DIR))
    parser.add_argument("--output-dir", type=Path, default=Path(OUTPUT_DIR))
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True)); return 0
    require(args.execute, "Qwen reranker requires explicit --execute")
    preflight_dir = args.preflight_dir if args.preflight_dir.is_absolute() else ROOT / args.preflight_dir
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    require(not output_dir.exists(), f"Refusing to overwrite Qwen B2 output: {output_dir}")
    verify_preflight(ROOT, preflight_dir)
    api_key = load_key(args.api_key_env)
    conditions = read_jsonl(preflight_dir / "conditions.jsonl")
    strict_by_id = {row["condition_id"]: row for row in read_jsonl(preflight_dir / "strict_bindings.jsonl")}
    require(len(conditions) == len(strict_by_id) == 4572, "Qwen B2 preflight coverage drift")
    staging = output_dir.with_name(f".{output_dir.name}.staging")
    require(not staging.exists(), f"Stale Qwen B2 staging requires inspection: {staging}")
    staging.mkdir(parents=True)
    (staging / "records").mkdir()
    result_rows: list[dict[str, Any]] = []
    usage_tokens = 0
    for index, condition in enumerate(conditions, start=1):
        strict = strict_by_id[condition["condition_id"]]
        payload, windows = provider_payload(condition)
        record_base = staging / "records" / f"{index:05d}"
        attempt = {"state": "persisted_before_provider_call", "automatic_retry": False, "condition_id": condition["condition_id"], "payload": payload}
        write_json(record_base.with_name(record_base.name + "_attempt.json"), attempt)
        started = time.perf_counter()
        try:
            response = request_once(payload, api_key)
        except ProviderRequestError as error:
            write_json(
                record_base.with_name(record_base.name + "_failure.json"),
                {
                    "state": "failed_no_retry",
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "http_status": error.status,
                    "provider_response_body": error.body,
                },
            )
            raise RuntimeError(f"Qwen B2 stopped at condition {index}; no retry was sent") from error
        scores = parse_scores(response, len(windows))
        elapsed = time.perf_counter() - started
        write_json(record_base.with_name(record_base.name + "_success.json"), {"state": "completed", "response": response, "elapsed_seconds": elapsed})
        result_rows.append(aggregate(condition, strict, scores, elapsed))
        usage_tokens += int(response.get("usage", {}).get("total_tokens", 0))
        if index % 25 == 0 or index == len(conditions):
            print(f"Qwen B2: completed {index}/{len(conditions)} conditions", flush=True)
    rows_path = staging / "rows.jsonl"; write_jsonl(rows_path, result_rows)
    ledger = {"network_calls": len(conditions), "successful_calls": len(conditions), "automatic_retries": 0, "provider_total_tokens": usage_tokens}
    ledger_path = staging / "ledger.json"; write_json(ledger_path, ledger)
    manifest = {"schema_version": "rq2bv1-v3-b2-qwen-run-manifest-v1", "state": "completed_pending_local_verification", "method": {"model": MODEL, "endpoint": ENDPOINT, "instruct": INSTRUCT, "window_aggregation": "maximum_window_score"}, "preflight_manifest": {"path": relative(preflight_dir / "manifest.json", ROOT), "sha256": sha256_file(preflight_dir / "manifest.json")}, "artifacts": {"rows": {"path": relative(output_dir / "rows.jsonl", ROOT), "sha256": sha256_file(rows_path), "rows": len(result_rows)}, "ledger": {"path": relative(output_dir / "ledger.json", ROOT), "sha256": sha256_file(ledger_path)}}, "thesis_result_writing": False}
    write_json(staging / "manifest.json", manifest)
    staging.replace(output_dir)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
