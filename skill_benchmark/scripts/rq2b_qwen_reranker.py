#!/usr/bin/env python3
"""Zero-network Qwen B2 contract helpers and synthetic fairness checks.

This module intentionally has no provider-execution entry point.  A later,
separately approved runner may use these deterministic payload and response
helpers only after B1 has persisted the exact candidate lists.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from typing import Any

from rq2b_common import require, sha256_json, sha256_text


RUNNER_CONTRACT_VERSION = "rq2b-qwen-reranker-contract-v1"
MODEL = "qwen3-rerank"
ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"
PRIMARY_K = 20
MAX_DOCUMENTS_PER_REQUEST = 500
MAX_TOKENS_PER_DOCUMENT = 4000
MAX_REQUEST_PROXY_TOKENS = 120000
WINDOW_PROXY_TOKENS = 3500
WINDOW_OVERLAP_PROXY_TOKENS = 256
REQUEST_FIXED_PROXY_TOKENS = 1000
ANCHOR_SCORE_ABS_TOLERANCE = 1e-6
INSTRUCTION = (
    "Rank the candidate skill documents by how well they satisfy the user request. "
    "Prefer the skill whose required inputs, intended outcome, process, constraints, "
    "and capability requirements are compatible with the request. Select the skill "
    "the agent should load first using only the supplied query and candidate text."
)

CONDITION_KEYS = {
    "schema_version",
    "condition_id",
    "first_stage_retriever",
    "representation",
    "prompt_id",
    "prompt_sha256",
    "query",
    "query_sha256",
    "candidate_skill_ids",
    "candidate_list_sha256",
    "candidate_windows",
}
WINDOW_KEYS = {
    "skill_id",
    "window_index",
    "text",
    "text_sha256",
    "proxy_tokens",
}
TRUSTED_BINDING_KEYS = {
    "condition_id",
    "first_stage_retriever",
    "representation",
    "prompt_id",
    "prompt_sha256",
    "query_sha256",
    "candidate_skill_ids",
    "candidate_list_sha256",
    "candidate_windows",
}
TRUSTED_WINDOW_KEYS = {"skill_id", "window_index", "text_sha256", "proxy_tokens"}


def candidate_list_sha256(candidate_skill_ids: list[str]) -> str:
    return sha256_json(candidate_skill_ids)


def trusted_binding_from_sources(
    *,
    condition_id: str,
    prompt: dict[str, Any],
    b1_row: dict[str, Any],
    candidate_windows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Bind a future Qwen payload to independent prompt, B1, and representation inputs.

    Callers must derive these values before payload construction from the frozen
    prompt record, persisted B1 row, and selector-visible representation windows.
    The binding deliberately stores window hashes, not label metadata.
    """
    require(isinstance(condition_id, str) and bool(condition_id), "Qwen binding condition ID is empty")
    query = prompt.get("prompt")
    prompt_sha256 = prompt.get("prompt_sha256")
    require(isinstance(query, str) and bool(query.strip()), "Qwen binding prompt text is empty")
    require(prompt_sha256 == sha256_text(query), "Qwen binding prompt hash does not match source prompt")
    require(b1_row.get("prompt_id") == prompt.get("prompt_id"), "Qwen binding B1 prompt ID drift")
    require(b1_row.get("prompt_sha256") == prompt_sha256, "Qwen binding B1 prompt hash drift")
    candidates = b1_row.get("top_20_skill_ids")
    require(
        isinstance(candidates, list)
        and len(candidates) == PRIMARY_K
        and all(isinstance(skill_id, str) and skill_id for skill_id in candidates)
        and len(set(candidates)) == PRIMARY_K,
        "Qwen binding B1 candidates are not an ordered Top-20",
    )
    require(isinstance(candidate_windows, list) and bool(candidate_windows), "Qwen binding has no representation windows")
    for window in candidate_windows:
        require(set(window) == WINDOW_KEYS, "Qwen binding source window key mismatch")
        require(window["skill_id"] in candidates, "Qwen binding source window is outside B1 Top-20")
        require(isinstance(window["window_index"], int) and window["window_index"] >= 0, "Qwen binding source window index is invalid")
        require(isinstance(window["text"], str) and bool(window["text"]), "Qwen binding source window text is empty")
        require(window["text_sha256"] == sha256_text(window["text"]), "Qwen binding source window hash mismatch")
        require(
            isinstance(window["proxy_tokens"], int) and 0 < window["proxy_tokens"] <= WINDOW_PROXY_TOKENS,
            "Qwen binding source window token count is invalid",
        )
    binding = {
        "condition_id": condition_id,
        "first_stage_retriever": b1_row["retriever"],
        "representation": b1_row["representation"],
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt_sha256,
        "query_sha256": sha256_text(query),
        "candidate_skill_ids": list(candidates),
        "candidate_list_sha256": candidate_list_sha256(candidates),
        "candidate_windows": [
            {
                "skill_id": window.get("skill_id"),
                "window_index": window.get("window_index"),
                "text_sha256": window.get("text_sha256"),
                "proxy_tokens": window.get("proxy_tokens"),
            }
            for window in candidate_windows
        ],
    }
    require(set(binding) == TRUSTED_BINDING_KEYS, "Qwen trusted binding key mismatch")
    require(
        all(set(window) == TRUSTED_WINDOW_KEYS for window in binding["candidate_windows"]),
        "Qwen trusted binding window key mismatch",
    )
    return binding


def validate_condition(condition: dict[str, Any], trusted_binding: dict[str, Any]) -> None:
    require(
        set(condition) == CONDITION_KEYS,
        "Qwen reranker condition key mismatch or forbidden metadata leakage",
    )
    require(set(trusted_binding) == TRUSTED_BINDING_KEYS, "Qwen trusted binding key mismatch")
    require(
        condition["schema_version"] == "rq2b-qwen-reranker-condition-payload-v1",
        "Qwen reranker condition schema mismatch",
    )
    require(
        isinstance(condition["query"], str) and bool(condition["query"].strip()),
        "Qwen reranker query is empty",
    )
    require(
        condition["query_sha256"] == sha256_text(condition["query"]),
        "Qwen reranker query hash mismatch",
    )
    for key in ("condition_id", "first_stage_retriever", "representation", "prompt_id", "prompt_sha256", "query_sha256"):
        require(condition[key] == trusted_binding[key], f"Qwen reranker trusted {key} drift")
    candidates = condition["candidate_skill_ids"]
    require(
        isinstance(candidates, list)
        and len(candidates) == PRIMARY_K
        and all(isinstance(skill_id, str) and skill_id for skill_id in candidates)
        and len(set(candidates)) == PRIMARY_K,
        "Qwen reranker candidate list is not an ordered Top-20",
    )
    require(
        condition["candidate_list_sha256"] == candidate_list_sha256(candidates),
        "Qwen reranker candidate-order hash mismatch",
    )
    require(candidates == trusted_binding["candidate_skill_ids"], "Qwen reranker candidates drift from persisted B1 Top-20")
    require(
        condition["candidate_list_sha256"] == trusted_binding["candidate_list_sha256"],
        "Qwen reranker candidate hash drift from persisted B1 Top-20",
    )
    windows = condition["candidate_windows"]
    require(isinstance(windows, list) and bool(windows), "Qwen reranker has no candidate windows")
    windows_by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_window_keys: set[tuple[str, int]] = set()
    for window in windows:
        require(set(window) == WINDOW_KEYS, "Qwen reranker window key mismatch")
        skill_id = window["skill_id"]
        index = window["window_index"]
        text = window["text"]
        proxy_tokens = window["proxy_tokens"]
        require(skill_id in candidates, "Qwen reranker window is outside persisted Top-20")
        require(isinstance(index, int) and index >= 0, "Qwen reranker window index is invalid")
        require(isinstance(text, str) and bool(text), "Qwen reranker window text is empty")
        require(window["text_sha256"] == sha256_text(text), "Qwen reranker window hash mismatch")
        require(
            isinstance(proxy_tokens, int)
            and 0 < proxy_tokens <= WINDOW_PROXY_TOKENS
            and proxy_tokens <= MAX_TOKENS_PER_DOCUMENT,
            "Qwen reranker window exceeds the frozen safe document limit",
        )
        key = (skill_id, index)
        require(key not in seen_window_keys, "Qwen reranker duplicate candidate window")
        seen_window_keys.add(key)
        windows_by_skill[skill_id].append(window)
    require(
        set(windows_by_skill) == set(candidates),
        "Qwen reranker candidate-window coverage does not match persisted Top-20",
    )
    for skill_id, skill_windows in windows_by_skill.items():
        require(
            [window["window_index"] for window in sorted(skill_windows, key=lambda row: row["window_index"])]
            == list(range(len(skill_windows))),
            f"Qwen reranker windows are not contiguous for {skill_id}",
        )
    observed_windows = [
        {
            "skill_id": window["skill_id"],
            "window_index": window["window_index"],
            "text_sha256": window["text_sha256"],
            "proxy_tokens": window["proxy_tokens"],
        }
        for window in windows
    ]
    require(
        observed_windows == trusted_binding["candidate_windows"],
        "Qwen reranker selector-visible window binding drift",
    )


def ordered_windows_by_skill(
    condition: dict[str, Any], trusted_binding: dict[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    validate_condition(condition, trusted_binding)
    by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for window in condition["candidate_windows"]:
        by_skill[window["skill_id"]].append(window)
    return {
        skill_id: sorted(by_skill[skill_id], key=lambda row: row["window_index"])
        for skill_id in condition["candidate_skill_ids"]
    }


def batch_proxy_tokens(entries: list[dict[str, Any]]) -> int:
    return REQUEST_FIXED_PROXY_TOKENS + sum(
        int(entry["window"]["proxy_tokens"]) for entry in entries
    )


def build_request_batches(condition: dict[str, Any], trusted_binding: dict[str, Any]) -> list[dict[str, Any]]:
    """Partition complete candidates, adding a duplicate anchor after a split."""
    windows_by_skill = ordered_windows_by_skill(condition, trusted_binding)
    candidates = condition["candidate_skill_ids"]
    anchor_windows = windows_by_skill[candidates[0]]
    batches: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for candidate_index, skill_id in enumerate(candidates):
        candidate_entries = [
            {"window": window, "is_anchor_duplicate": False}
            for window in windows_by_skill[skill_id]
        ]
        require(
            len(candidate_entries) <= MAX_DOCUMENTS_PER_REQUEST
            and batch_proxy_tokens(candidate_entries) <= MAX_REQUEST_PROXY_TOKENS,
            f"Qwen reranker cannot fit one complete candidate: {skill_id}",
        )
        proposed = [*current, *candidate_entries]
        if current and (
            len(proposed) > MAX_DOCUMENTS_PER_REQUEST
            or batch_proxy_tokens(proposed) > MAX_REQUEST_PROXY_TOKENS
        ):
            batches.append(current)
            current = [
                {"window": window, "is_anchor_duplicate": True}
                for window in anchor_windows
            ]
            proposed = [*current, *candidate_entries]
        require(
            len(proposed) <= MAX_DOCUMENTS_PER_REQUEST
            and batch_proxy_tokens(proposed) <= MAX_REQUEST_PROXY_TOKENS,
            f"Qwen reranker cannot fit candidate with required anchor: {skill_id}",
        )
        current = proposed
        require(candidate_index == 0 or bool(current), "Qwen reranker batch construction lost a candidate")
    require(bool(current), "Qwen reranker batch construction produced no requests")
    batches.append(current)
    output: list[dict[str, Any]] = []
    for batch_index, entries in enumerate(batches):
        payload = {
            "model": MODEL,
            "input": {
                "query": condition["query"],
                "documents": [entry["window"]["text"] for entry in entries],
            },
            "parameters": {
                "return_documents": False,
                "top_n": len(entries),
                "instruct": INSTRUCTION,
            },
        }
        output.append(
            {
                "batch_index": batch_index,
                "payload": payload,
                "entries": entries,
                "request_proxy_tokens": batch_proxy_tokens(entries),
                "anchor_duplicate_window_count": sum(
                    1 for entry in entries if entry["is_anchor_duplicate"]
                ),
            }
        )
    require(
        all(
            len(batch["entries"]) <= MAX_DOCUMENTS_PER_REQUEST
            and batch["request_proxy_tokens"] <= MAX_REQUEST_PROXY_TOKENS
            for batch in output
        ),
        "Qwen reranker batch limit enforcement failed",
    )
    return output


def build_request_payload(
    condition: dict[str, Any], trusted_binding: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Build one provider-shaped request only when no cross-request comparison is needed."""
    batches = build_request_batches(condition, trusted_binding)
    require(
        len(batches) == 1,
        "Qwen reranker condition requires multiple requests and duplicate-anchor validation",
    )
    batch = batches[0]
    return batch["payload"], [entry["window"] for entry in batch["entries"]]


def request_cache_key(condition: dict[str, Any], trusted_binding: dict[str, Any]) -> str:
    validate_condition(condition, trusted_binding)
    return sha256_json(
        {
            "runner_contract_version": RUNNER_CONTRACT_VERSION,
            "endpoint": ENDPOINT,
            "model": MODEL,
            "instruction": INSTRUCTION,
            "query_sha256": condition["query_sha256"],
            "candidate_list_sha256": condition["candidate_list_sha256"],
            "request_batches": [
                {
                    "batch_index": batch["batch_index"],
                    "anchor_duplicate_window_count": batch["anchor_duplicate_window_count"],
                    "windows": [
                        {
                            "skill_id": entry["window"]["skill_id"],
                            "window_index": entry["window"]["window_index"],
                            "text_sha256": entry["window"]["text_sha256"],
                            "is_anchor_duplicate": entry["is_anchor_duplicate"],
                        }
                        for entry in batch["entries"]
                    ],
                }
                for batch in build_request_batches(condition, trusted_binding)
            ],
        }
    )


def parse_response_scores(response: dict[str, Any], window_count: int) -> list[float]:
    results = response.get("output", {}).get("results")
    require(isinstance(results, list), "Qwen reranker response has no results list")
    scores: list[float | None] = [None] * window_count
    for result in results:
        require(isinstance(result, dict), "Qwen reranker result is not an object")
        index = result.get("index")
        score = result.get("relevance_score")
        require(isinstance(index, int) and 0 <= index < window_count, "Qwen reranker response index is invalid")
        require(scores[index] is None, "Qwen reranker response repeats an index")
        require(isinstance(score, (int, float)) and math.isfinite(float(score)), "Qwen reranker response score is invalid")
        scores[index] = float(score)
    require(all(score is not None for score in scores), "Qwen reranker response omits a requested window")
    return [float(score) for score in scores]


def verify_duplicate_anchor_scores(
    batches: list[dict[str, Any]],
    score_batches: list[list[float]],
) -> int:
    """Fail closed when copied anchor windows are not scored comparably."""
    require(len(batches) == len(score_batches), "Qwen reranker batch-score count mismatch")
    canonical_scores: dict[tuple[str, int, str], float] = {}
    comparisons = 0
    for batch, scores in zip(batches, score_batches, strict=True):
        entries = batch["entries"]
        require(len(entries) == len(scores), "Qwen reranker anchor score length mismatch")
        for entry, score in zip(entries, scores, strict=True):
            require(isinstance(score, (int, float)) and math.isfinite(float(score)), "Qwen reranker anchor score is invalid")
            window = entry["window"]
            key = (window["skill_id"], window["window_index"], window["text_sha256"])
            if entry["is_anchor_duplicate"]:
                require(key in canonical_scores, "Qwen reranker duplicate anchor lacks a canonical score")
                require(
                    abs(float(score) - canonical_scores[key]) <= ANCHOR_SCORE_ABS_TOLERANCE,
                    "Qwen reranker duplicate anchor is not score-comparable across requests",
                )
                comparisons += 1
            else:
                require(key not in canonical_scores, "Qwen reranker repeats a canonical window")
                canonical_scores[key] = float(score)
    if len(batches) > 1:
        require(comparisons > 0, "Qwen reranker split requests lack duplicate-anchor checks")
    return comparisons


def aggregate_candidate_scores(
    condition: dict[str, Any],
    trusted_binding: dict[str, Any],
    windows: list[dict[str, Any]],
    scores: list[float],
) -> list[dict[str, Any]]:
    validate_condition(condition, trusted_binding)
    require(len(windows) == len(scores), "Qwen reranker window-score length mismatch")
    require(all(isinstance(score, (int, float)) and math.isfinite(float(score)) for score in scores), "Qwen reranker aggregate score is invalid")
    by_skill: dict[str, list[float]] = defaultdict(list)
    for window, score in zip(windows, scores, strict=True):
        by_skill[window["skill_id"]].append(score)
    candidate_order = {skill_id: index for index, skill_id in enumerate(condition["candidate_skill_ids"], start=1)}
    require(set(by_skill) == set(candidate_order), "Qwen reranker score coverage mismatch")
    rows = [
        {
            "skill_id": skill_id,
            "first_stage_rank": candidate_order[skill_id],
            "maximum_window_score": max(by_skill[skill_id]),
            "mean_window_score": sum(by_skill[skill_id]) / len(by_skill[skill_id]),
            "window_count": len(by_skill[skill_id]),
        }
        for skill_id in condition["candidate_skill_ids"]
    ]
    return sorted(
        rows,
        key=lambda row: (-row["maximum_window_score"], row["first_stage_rank"], row["skill_id"]),
    )


def synthetic_condition() -> dict[str, Any]:
    candidates = [f"synthetic-skill-{index:02d}" for index in range(PRIMARY_K)]
    windows: list[dict[str, Any]] = []
    for candidate_index, skill_id in enumerate(candidates):
        count = 2 if candidate_index == 0 else 1
        for window_index in range(count):
            text = f"Synthetic candidate {candidate_index}, window {window_index}."
            windows.append(
                {
                    "skill_id": skill_id,
                    "window_index": window_index,
                    "text": text,
                    "text_sha256": sha256_text(text),
                    "proxy_tokens": 12,
                }
            )
    query = "Synthetic request"
    return {
        "schema_version": "rq2b-qwen-reranker-condition-payload-v1",
        "condition_id": "synthetic-condition",
        "first_stage_retriever": "bm25",
        "representation": "i3c-fielded-evidence",
        "prompt_id": "synthetic-prompt",
        "prompt_sha256": sha256_text(query),
        "query": query,
        "query_sha256": sha256_text(query),
        "candidate_skill_ids": candidates,
        "candidate_list_sha256": candidate_list_sha256(candidates),
        "candidate_windows": windows,
    }


def synthetic_split_condition() -> dict[str, Any]:
    condition = synthetic_condition()
    expanded_windows: list[dict[str, Any]] = []
    for skill_id in condition["candidate_skill_ids"]:
        for window_index in range(3):
            text = f"Large synthetic candidate {skill_id}, window {window_index}."
            expanded_windows.append(
                {
                    "skill_id": skill_id,
                    "window_index": window_index,
                    "text": text,
                    "text_sha256": sha256_text(text),
                    "proxy_tokens": WINDOW_PROXY_TOKENS,
                }
            )
    return {**condition, "candidate_windows": expanded_windows}


def synthetic_trusted_binding(condition: dict[str, Any]) -> dict[str, Any]:
    """Build a synthetic stand-in for the three independent future sources."""
    return trusted_binding_from_sources(
        condition_id=condition["condition_id"],
        prompt={
            "prompt_id": condition["prompt_id"],
            "prompt": condition["query"],
            "prompt_sha256": condition["prompt_sha256"],
        },
        b1_row={
            "retriever": condition["first_stage_retriever"],
            "representation": condition["representation"],
            "prompt_id": condition["prompt_id"],
            "prompt_sha256": condition["prompt_sha256"],
            "top_20_skill_ids": condition["candidate_skill_ids"],
        },
        candidate_windows=condition["candidate_windows"],
    )


def self_test() -> dict[str, Any]:
    condition = synthetic_condition()
    trusted_binding = synthetic_trusted_binding(condition)
    payload, windows = build_request_payload(condition, trusted_binding)
    require(payload["input"]["query"] == condition["query"], "Synthetic Qwen query drift")
    require(payload["input"]["documents"] == [row["text"] for row in windows], "Synthetic Qwen document-order drift")
    scores = [float(index) for index in range(len(windows))]
    parsed = parse_response_scores(
        {
            "output": {
                "results": [
                    {"index": index, "relevance_score": score}
                    for index, score in enumerate(scores)
                ]
            }
        },
        len(windows),
    )
    ranked = aggregate_candidate_scores(condition, trusted_binding, windows, parsed)
    require(ranked[0]["skill_id"] == condition["candidate_skill_ids"][-1], "Synthetic Qwen ranking aggregation failed")
    order_drift_rejected = False
    try:
        reversed_candidates = list(reversed(condition["candidate_skill_ids"]))
        validate_condition(
            {
                **condition,
                "candidate_skill_ids": reversed_candidates,
                "candidate_list_sha256": candidate_list_sha256(reversed_candidates),
            },
            trusted_binding,
        )
    except ValueError:
        order_drift_rejected = True
    require(order_drift_rejected, "Synthetic candidate-order drift was accepted")
    coverage_drift_rejected = False
    try:
        validate_condition({**condition, "candidate_windows": condition["candidate_windows"][1:]}, trusted_binding)
    except ValueError:
        coverage_drift_rejected = True
    require(coverage_drift_rejected, "Synthetic candidate coverage drift was accepted")
    label_leakage_rejected = False
    try:
        validate_condition({**condition, "gold_skill": condition["candidate_skill_ids"][0]}, trusted_binding)
    except ValueError:
        label_leakage_rejected = True
    require(label_leakage_rejected, "Synthetic gold-label leakage was accepted")
    incomplete_response_rejected = False
    try:
        parse_response_scores({"output": {"results": [{"index": 0, "relevance_score": 1.0}]}}, len(windows))
    except ValueError:
        incomplete_response_rejected = True
    require(incomplete_response_rejected, "Synthetic incomplete provider response was accepted")
    query_drift_rejected = False
    changed_query = "Changed synthetic request"
    try:
        validate_condition(
            {**condition, "query": changed_query, "query_sha256": sha256_text(changed_query)},
            trusted_binding,
        )
    except ValueError:
        query_drift_rejected = True
    require(query_drift_rejected, "Synthetic source-bound query drift was accepted")
    text_drift_rejected = False
    changed_windows = [dict(window) for window in condition["candidate_windows"]]
    changed_windows[0]["text"] = "Changed synthetic candidate text."
    changed_windows[0]["text_sha256"] = sha256_text(changed_windows[0]["text"])
    try:
        validate_condition({**condition, "candidate_windows": changed_windows}, trusted_binding)
    except ValueError:
        text_drift_rejected = True
    require(text_drift_rejected, "Synthetic source-bound document drift was accepted")
    split_condition = synthetic_split_condition()
    split_binding = synthetic_trusted_binding(split_condition)
    split_batches = build_request_batches(split_condition, split_binding)
    require(len(split_batches) > 1, "Synthetic split fixture did not exercise multiple requests")
    require(
        all(
            batch["anchor_duplicate_window_count"] == 3
            for batch in split_batches[1:]
        ),
        "Synthetic split fixture lacks a complete duplicate anchor",
    )
    canonical_scores = {
        (window["skill_id"], window["window_index"], window["text_sha256"]): float(index)
        for index, window in enumerate(split_condition["candidate_windows"])
    }
    split_score_batches = [
        [
            canonical_scores[
                (
                    entry["window"]["skill_id"],
                    entry["window"]["window_index"],
                    entry["window"]["text_sha256"],
                )
            ]
            for entry in batch["entries"]
        ]
        for batch in split_batches
    ]
    anchor_comparisons = verify_duplicate_anchor_scores(split_batches, split_score_batches)
    anchor_drift_rejected = False
    drifted_batches = [list(scores) for scores in split_score_batches]
    for batch_index, batch in enumerate(split_batches):
        for entry_index, entry in enumerate(batch["entries"]):
            if entry["is_anchor_duplicate"]:
                drifted_batches[batch_index][entry_index] += 0.01
                break
        else:
            continue
        break
    try:
        verify_duplicate_anchor_scores(split_batches, drifted_batches)
    except ValueError:
        anchor_drift_rejected = True
    require(anchor_drift_rejected, "Synthetic duplicate-anchor drift was accepted")
    return {
        "state": "synthetic_no_network_no_provider_payload",
        "network_calls": 0,
        "texts_transmitted": 0,
        "scientific_selector_runs": 0,
        "thesis_results_written": False,
        "candidate_count": PRIMARY_K,
        "window_count": len(windows),
        "request_cache_key": request_cache_key(condition, trusted_binding),
        "candidate_order_drift_rejected": order_drift_rejected,
        "candidate_coverage_drift_rejected": coverage_drift_rejected,
        "source_bound_query_drift_rejected": query_drift_rejected,
        "source_bound_window_text_drift_rejected": text_drift_rejected,
        "label_leakage_rejected": label_leakage_rejected,
        "incomplete_response_rejected": incomplete_response_rejected,
        "split_request_count": len(split_batches),
        "duplicate_anchor_comparisons": anchor_comparisons,
        "duplicate_anchor_drift_rejected": anchor_drift_rejected,
        "primary_aggregation": "maximum_window_score",
        "sensitivity_aggregation": "mean_window_score",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    require(args.self_test, "This zero-network contract helper supports only --self-test")
    print(json.dumps(self_test(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
