#!/usr/bin/env python3
"""Rerank immutable RQ2b B1 candidates with the pinned SkillRouter model."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
import time
from pathlib import Path
from typing import Any

from audit_rq2b_token_limits import BODY_FORMAT, INSTRUCTION, PREFIX, SUFFIX
from rq2b_common import (
    VERSION_ID,
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    sha256_file,
    sha256_json,
    sha256_text,
    verify_frozen_manifest,
    verify_b1s_implementation_seal,
    write_json_new,
    write_jsonl_new,
)


RUNNER_VERSION = "rq2b-skillrouter-fixed-candidate-runner-v1"
MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
REVISION = "78986e1142d12857cfd85b8005e62902cd42d858"
PROMPT_VERSION = "skillrouter-reranker-prompt-v1"
PROMPT_SHA256 = "face140f238119fc19ba12de90131d1031ada388f08f73e641d0dffd6a00817e"
TOKENIZER_SHA256 = "ab19c66299579df20542864f9e27b79898ca05f35acc97fd9259aee385a07d4a"
MODEL_WEIGHTS_SHA256 = "34064850b1b512168309481a9cebe4ecaf55d0821bf22608f657b40033ed36d7"
MODEL_CONFIG_SHA256 = "17f3b5063350823bfda01f740ac14b9d1cd9cb80c738cbe0d9939c4988ac6b39"
MAX_PAIR_TOKENS = 2048
PRIMARY_K = 20
SENSITIVITY_K = 5


def build_input_ids(tokenizer: Any, query: str, document: str) -> list[int]:
    body = BODY_FORMAT.format(
        instruction=INSTRUCTION,
        query=query,
        document=document,
    )
    input_ids = (
        tokenizer.encode(PREFIX, add_special_tokens=False)
        + tokenizer.encode(body, add_special_tokens=False)
        + tokenizer.encode(SUFFIX, add_special_tokens=False)
    )
    require(len(input_ids) <= MAX_PAIR_TOKENS, "SkillRouter pair exceeds 2,048 tokens")
    return input_ids


def window_cache_key(
    *,
    representation: str,
    query: str,
    document_window: str,
) -> str:
    return sha256_json(
        {
            "model": MODEL,
            "revision": REVISION,
            "prompt_version": PROMPT_VERSION,
            "prompt_sha256": PROMPT_SHA256,
            "tokenizer_sha256": TOKENIZER_SHA256,
            "maximum_pair_tokens": MAX_PAIR_TOKENS,
            "representation": representation,
            "query_sha256": sha256_text(query),
            "document_window_sha256": sha256_text(document_window),
        }
    )


class WindowScoreCache:
    def __init__(self, root: Path) -> None:
        self.root = root / "skillrouter" / REVISION / PROMPT_VERSION
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, *, representation: str, query: str, document_window: str) -> Path:
        return self.root / f"{window_cache_key(representation=representation, query=query, document_window=document_window)}.json"

    def load(
        self,
        *,
        representation: str,
        query: str,
        document_window: str,
    ) -> float | None:
        path = self.path(
            representation=representation,
            query=query,
            document_window=document_window,
        )
        if not path.exists():
            return None
        payload = read_json(path)
        expected = {
            "schema_version": "rq2b-skillrouter-window-cache-v1",
            "model": MODEL,
            "revision": REVISION,
            "prompt_version": PROMPT_VERSION,
            "prompt_sha256": PROMPT_SHA256,
            "tokenizer_sha256": TOKENIZER_SHA256,
            "representation": representation,
            "query_sha256": sha256_text(query),
            "document_window_sha256": sha256_text(document_window),
        }
        for key, value in expected.items():
            require(payload.get(key) == value, f"SkillRouter cache mismatch for {key}: {path}")
        score = float(payload["score"])
        require(math.isfinite(score), f"SkillRouter cache has non-finite score: {path}")
        return score

    def store(
        self,
        *,
        representation: str,
        query: str,
        document_window: str,
        model_token_count: int,
        score: float,
    ) -> None:
        path = self.path(
            representation=representation,
            query=query,
            document_window=document_window,
        )
        require(not path.exists(), f"Refusing to overwrite SkillRouter cache entry: {path}")
        write_json_new(
            path,
            {
                "schema_version": "rq2b-skillrouter-window-cache-v1",
                "model": MODEL,
                "revision": REVISION,
                "prompt_version": PROMPT_VERSION,
                "prompt_sha256": PROMPT_SHA256,
                "tokenizer_sha256": TOKENIZER_SHA256,
                "representation": representation,
                "query_sha256": sha256_text(query),
                "document_window_sha256": sha256_text(document_window),
                "model_token_count": model_token_count,
                "score": score,
            },
        )


def validate_authorisation(
    path: Path,
    payload_path: Path,
    *,
    root: Path,
    run_id: str,
    output_dir: Path,
    batch_size: int,
) -> dict[str, Any]:
    require(path.exists(), f"SkillRouter execution authorisation missing: {path}")
    authorisation = read_json(path)
    require(authorisation.get("schema_version") == "rq2b-skillrouter-execution-authorisation-v1", "SkillRouter authorisation schema mismatch")
    require(authorisation.get("state") == "explicitly_authorised_for_one_execution", "SkillRouter execution is not authorised")
    require(authorisation.get("model") == MODEL, "SkillRouter authorised model mismatch")
    require(authorisation.get("revision") == REVISION, "SkillRouter authorised revision mismatch")
    require(authorisation.get("model_weights_sha256") == MODEL_WEIGHTS_SHA256, "SkillRouter authorised weights mismatch")
    require(authorisation.get("model_config_sha256") == MODEL_CONFIG_SHA256, "SkillRouter authorised config mismatch")
    require(authorisation.get("payload_manifest_sha256") == sha256_file(payload_path), "SkillRouter payload is not authorised")
    require(authorisation.get("run_id") == run_id, "SkillRouter authorised run ID mismatch")
    require(authorisation.get("output_dir") == relative(output_dir, root), "SkillRouter authorised output directory mismatch")
    require(authorisation.get("batch_size") == batch_size, "SkillRouter authorised batch size mismatch")
    require(authorisation.get("automatic_retries") == 0, "SkillRouter authorisation must forbid retries")
    for key in (
        "maximum_new_windows",
        "maximum_model_forward_batches",
        "maximum_new_model_input_tokens",
    ):
        require(isinstance(authorisation.get(key), int) and authorisation[key] >= 0, f"SkillRouter authorisation lacks {key}")
    return authorisation


def load_local_model(device: str) -> tuple[Any, Any, Any, int, int, int]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    snapshot = (
        Path.home()
        / ".cache/huggingface/hub/models--pipizhao--SkillRouter-Reranker-0.6B/snapshots"
        / REVISION
    )
    require(snapshot.is_dir(), f"Pinned local SkillRouter snapshot is missing: {snapshot}")
    require(sha256_file(snapshot / "tokenizer.json") == TOKENIZER_SHA256, "SkillRouter tokenizer hash drift")
    require(sha256_file(snapshot / "model.safetensors") == MODEL_WEIGHTS_SHA256, "SkillRouter model-weight hash drift")
    require(sha256_file(snapshot / "config.json") == MODEL_CONFIG_SHA256, "SkillRouter model-config hash drift")
    tokenizer = AutoTokenizer.from_pretrained(snapshot, padding_side="left", local_files_only=True)
    resolved_device = device
    if device == "auto":
        if torch.cuda.is_available():
            resolved_device = "cuda"
        elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            resolved_device = "mps"
        else:
            resolved_device = "cpu"
    dtype = torch.bfloat16 if resolved_device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(snapshot, dtype=dtype, local_files_only=True).eval()
    model.to(resolved_device)
    yes = tokenizer.encode("yes", add_special_tokens=False)
    no = tokenizer.encode("no", add_special_tokens=False)
    require(len(yes) == len(no) == 1, "SkillRouter yes/no tokens are not singular")
    pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    require(pad is not None, "SkillRouter tokenizer has no padding token")
    return torch, tokenizer, model, yes[0], no[0], pad


def score_missing_windows(
    missing: list[dict[str, Any]],
    *,
    cache: WindowScoreCache,
    device: str,
    batch_size: int,
    authorisation: dict[str, Any],
    progress_dir: Path,
) -> tuple[dict[str, float], dict[str, Any]]:
    require(batch_size > 0, "SkillRouter batch size must be positive")
    require(len(missing) <= int(authorisation["maximum_new_windows"]), "SkillRouter window ceiling exceeded")
    expected_batches = (len(missing) + batch_size - 1) // batch_size
    require(
        expected_batches <= int(authorisation["maximum_model_forward_batches"]),
        "SkillRouter model-forward batch ceiling exceeded",
    )
    model_input_tokens = sum(int(row["model_input_tokens"]) for row in missing)
    require(
        model_input_tokens <= int(authorisation["maximum_new_model_input_tokens"]),
        "SkillRouter model-input token ceiling exceeded",
    )
    progress_dir.mkdir(parents=True, exist_ok=False)
    if not missing:
        return {}, {
            "schema_version": "rq2b-skillrouter-model-ledger-v1",
            "model_forward_batch_attempts": 0,
            "model_forward_batch_successes": 0,
            "model_scored_windows": 0,
            "new_model_input_tokens": 0,
            "model_elapsed_seconds": 0.0,
            "model_load_seconds": 0.0,
            "input_preparation_seconds": 0.0,
            "model_forward_seconds": 0.0,
            "resolved_device": None,
            "model_dtype": None,
            "batch_size": batch_size,
            "batch_records": [],
        }
    model_started = time.perf_counter()
    load_started = time.perf_counter()
    torch, tokenizer, model, yes_token, no_token, pad_token = load_local_model(device)
    model_load_seconds = time.perf_counter() - load_started
    resolved_device = str(model.device)
    model_dtype = str(model.dtype)
    input_preparation_started = time.perf_counter()
    prepared: list[tuple[dict[str, Any], list[int]]] = []
    for row in missing:
        input_ids = build_input_ids(tokenizer, row["query"], row["document_window"])
        require(len(input_ids) == int(row["model_input_tokens"]), "SkillRouter payload/model token-count drift")
        prepared.append((row, input_ids))
    input_preparation_seconds = time.perf_counter() - input_preparation_started
    scores: dict[str, float] = {}
    batch_records: list[dict[str, Any]] = []
    for start in range(0, len(prepared), batch_size):
        batch = prepared[start : start + batch_size]
        batch_index = len(batch_records)
        batch_tokens = sum(len(input_ids) for _, input_ids in batch)
        attempt_path = progress_dir / f"batch_{batch_index:06d}_attempt.json"
        success_path = progress_dir / f"batch_{batch_index:06d}_success.json"
        attempt = {
            "schema_version": "rq2b-skillrouter-model-batch-attempt-v1",
            "batch_index": batch_index,
            "window_count": len(batch),
            "model_input_tokens": batch_tokens,
            "window_ids": [row["window_id"] for row, _ in batch],
            "automatic_retry": False,
        }
        write_json_new(attempt_path, attempt)
        print(f"SkillRouter: windows {start + 1}-{start + len(batch)} of {len(prepared)}", flush=True)
        batch_started = time.perf_counter()
        maximum = max(len(input_ids) for _, input_ids in batch)
        inputs = torch.full((len(batch), maximum), pad_token, dtype=torch.long, device=model.device)
        attention = torch.zeros_like(inputs)
        for index, (_, input_ids) in enumerate(batch):
            length = len(input_ids)
            inputs[index, -length:] = torch.tensor(input_ids, dtype=torch.long, device=model.device)
            attention[index, -length:] = 1
        with torch.no_grad():
            logits = model(input_ids=inputs, attention_mask=attention).logits[:, -1, :]
        batch_scores = (logits[:, yes_token] - logits[:, no_token]).detach().float().cpu().tolist()
        for (row, input_ids), score in zip(batch, batch_scores, strict=True):
            score = float(score)
            cache.store(
                representation=row["representation"],
                query=row["query"],
                document_window=row["document_window"],
                model_token_count=len(input_ids),
                score=score,
            )
            scores[row["window_id"]] = score
        success = {
            "schema_version": "rq2b-skillrouter-model-batch-success-v1",
            "batch_index": batch_index,
            "attempt_sha256": sha256_file(attempt_path),
            "window_count": len(batch),
            "model_input_tokens": batch_tokens,
            "elapsed_seconds": time.perf_counter() - batch_started,
            "cache_entries_written": len(batch),
        }
        write_json_new(success_path, success)
        batch_records.append(
            {
                "batch_index": batch_index,
                "attempt_path": f"model_batches/{attempt_path.name}",
                "attempt_sha256": sha256_file(attempt_path),
                "success_path": f"model_batches/{success_path.name}",
                "success_sha256": sha256_file(success_path),
                "window_count": len(batch),
                "model_input_tokens": batch_tokens,
                "elapsed_seconds": success["elapsed_seconds"],
            }
        )
    require(len(batch_records) == expected_batches, "SkillRouter model batch count drift")
    return scores, {
        "schema_version": "rq2b-skillrouter-model-ledger-v1",
        "model_forward_batch_attempts": len(batch_records),
        "model_forward_batch_successes": len(batch_records),
        "model_scored_windows": len(missing),
        "new_model_input_tokens": model_input_tokens,
        "model_elapsed_seconds": time.perf_counter() - model_started,
        "model_load_seconds": model_load_seconds,
        "input_preparation_seconds": input_preparation_seconds,
        "model_forward_seconds": sum(float(row["elapsed_seconds"]) for row in batch_records),
        "resolved_device": resolved_device,
        "model_dtype": model_dtype,
        "batch_size": batch_size,
        "batch_records": batch_records,
    }


def rerank_one(
    condition: dict[str, Any],
    pair_scores: dict[str, dict[str, float]],
    prompt: dict[str, Any],
) -> dict[str, Any]:
    candidates = condition["candidate_skill_ids"]
    require(len(candidates) == PRIMARY_K and len(set(candidates)) == PRIMARY_K, "SkillRouter requires immutable unique top-20 candidates")
    gold_skill = prompt["gold_skill"]
    valid_skills = set(prompt["valid_skills"])
    ranked: list[tuple[str, float, int]] = []
    mean_ranked: list[tuple[str, float, int]] = []
    for first_stage_rank, skill_id in enumerate(candidates, start=1):
        scores = pair_scores[condition["pair_ids_by_skill"][skill_id]]
        ranked.append((skill_id, float(scores["maximum_window_score"]), first_stage_rank))
        mean_ranked.append((skill_id, float(scores["mean_window_score"]), first_stage_rank))
    ranked.sort(key=lambda item: (-item[1], item[2], item[0]))
    mean_ranked.sort(key=lambda item: (-item[1], item[2], item[0]))

    strict_candidate_positive = gold_skill in candidates
    acceptable_candidate_positive = any(skill_id in valid_skills for skill_id in candidates)
    first_stage_strict_top1 = candidates[0] == gold_skill
    first_stage_valid_top1 = candidates[0] in valid_skills
    reranked_strict_top1 = ranked[0][0] == gold_skill
    reranked_valid_top1 = ranked[0][0] in valid_skills
    top5_candidates = candidates[:SENSITIVITY_K]
    top5_scored = [row for row in ranked if row[0] in set(top5_candidates)]
    top5_scored.sort(key=lambda item: (-item[1], item[2], item[0]))

    def metrics(order: list[tuple[str, float, int]]) -> dict[str, Any]:
        ids = [skill_id for skill_id, _, _ in order]
        strict_rank = ids.index(gold_skill) + 1 if gold_skill in ids else None
        acceptable_ranks = [ids.index(skill_id) + 1 for skill_id in valid_skills if skill_id in ids]
        acceptable_rank = min(acceptable_ranks) if acceptable_ranks else None
        return {
            "strict_top1": int(strict_rank == 1),
            "acceptable_top1": int(acceptable_rank == 1),
            "strict_rank": strict_rank,
            "acceptable_rank": acceptable_rank,
            "strict_reciprocal_rank": 0.0 if strict_rank is None else 1.0 / strict_rank,
            "acceptable_reciprocal_rank": 0.0 if acceptable_rank is None else 1.0 / acceptable_rank,
        }

    primary_metrics = metrics(ranked)
    mean_metrics = metrics(mean_ranked)
    k5_metrics = metrics(top5_scored)
    return {
        **condition,
        "schema_version": "rq2b-b2-result-row-v1",
        "runner_version": RUNNER_VERSION,
        "gold_skill": gold_skill,
        "valid_skills": sorted(valid_skills),
        "strict_candidate_positive": int(strict_candidate_positive),
        "acceptable_candidate_positive": int(acceptable_candidate_positive),
        "candidate_positive": int(acceptable_candidate_positive),
        "first_stage_strict_top1": int(first_stage_strict_top1),
        "first_stage_acceptable_top1": int(first_stage_valid_top1),
        "reranked_strict_top1": primary_metrics["strict_top1"],
        "reranked_acceptable_top1": int(reranked_valid_top1),
        "conditional_strict_top1_numerator": int(strict_candidate_positive and reranked_strict_top1),
        "conditional_strict_top1_denominator": int(strict_candidate_positive),
        "conditional_acceptable_top1_numerator": int(acceptable_candidate_positive and reranked_valid_top1),
        "conditional_acceptable_top1_denominator": int(acceptable_candidate_positive),
        "end_to_end_strict_top1": primary_metrics["strict_top1"],
        "end_to_end_acceptable_top1": int(reranked_valid_top1),
        "end_to_end_strict_reciprocal_rank": primary_metrics["strict_reciprocal_rank"],
        "end_to_end_acceptable_reciprocal_rank": primary_metrics["acceptable_reciprocal_rank"],
        "reranker_strict_gain": int(strict_candidate_positive and reranked_strict_top1 and not first_stage_strict_top1),
        "reranker_acceptable_gain": int(acceptable_candidate_positive and reranked_valid_top1 and not first_stage_valid_top1),
        "reranker_gain": int(acceptable_candidate_positive and reranked_valid_top1 and not first_stage_valid_top1),
        "reranker_strict_regression": int(first_stage_strict_top1 and not reranked_strict_top1),
        "reranker_acceptable_regression": int(first_stage_valid_top1 and not reranked_valid_top1),
        "reranker_regression": int(first_stage_valid_top1 and not reranked_valid_top1),
        "strict_unrecoverable_exclusion": int(not strict_candidate_positive),
        "acceptable_unrecoverable_exclusion": int(not acceptable_candidate_positive),
        "unrecoverable_exclusion": int(not acceptable_candidate_positive),
        "reranked_skill_ids": [skill_id for skill_id, _, _ in ranked],
        "reranked_scores": [score for _, score, _ in ranked],
        "mean_window_sensitivity_skill_ids": [skill_id for skill_id, _, _ in mean_ranked],
        "mean_window_sensitivity_metrics": mean_metrics,
        "k5_sensitivity_skill_ids": [skill_id for skill_id, _, _ in top5_scored],
        "k5_sensitivity_metrics": k5_metrics,
        "k5_new_model_forwards": 0,
    }


def verify_denominator_identity(rows: list[dict[str, Any]]) -> None:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in rows:
        key = (row["first_stage_retriever"], row["representation"], row["stratum"])
        groups.setdefault(key, []).append(row)
    for key, group_rows in groups.items():
        total = len(group_rows)
        for label in ("strict", "acceptable"):
            candidates_positive = sum(row[f"{label}_candidate_positive"] for row in group_rows)
            reranked_positive = sum(row[f"end_to_end_{label}_top1"] for row in group_rows)
            recall = candidates_positive / total
            conditional = reranked_positive / candidates_positive if candidates_positive else 0.0
            end_to_end = reranked_positive / total
            require(abs(end_to_end - recall * conditional) <= 1e-12, f"B2 {label} denominator identity failed: {key}")


def run(
    root: Path,
    payload_path: Path,
    authorisation_path: Path,
    output_dir: Path,
    run_id: str,
    device: str,
    batch_size: int,
) -> dict[str, Any]:
    verify_frozen_manifest(root)
    verify_b1s_implementation_seal(root)
    require(not output_dir.exists(), f"Refusing to overwrite SkillRouter run: {output_dir}")
    payload = read_json(payload_path)
    require(payload.get("schema_version") == "rq2b-skillrouter-payload-manifest-v1", "SkillRouter payload schema mismatch")
    require(payload.get("state") == "sealed_not_executed", "SkillRouter payload is not sealed")
    authorisation = validate_authorisation(
        authorisation_path,
        payload_path,
        root=root,
        run_id=run_id,
        output_dir=output_dir,
        batch_size=batch_size,
    )
    windows_path = root / payload["window_inventory"]["path"]
    pairs_path = root / payload["pair_inventory"]["path"]
    conditions_path = root / payload["condition_inventory"]["path"]
    for path, artifact in (
        (windows_path, payload["window_inventory"]),
        (pairs_path, payload["pair_inventory"]),
        (conditions_path, payload["condition_inventory"]),
    ):
        require(sha256_file(path) == artifact["sha256"], f"SkillRouter payload artifact drift: {path}")
    windows = read_jsonl(windows_path)
    pairs = read_jsonl(pairs_path)
    conditions = read_jsonl(conditions_path)
    staging = output_dir.parent / f".{output_dir.name}.staging"
    require(not staging.exists(), f"Stale SkillRouter run staging directory: {staging}")
    staging.mkdir(parents=True, exist_ok=False)
    run_started_path = staging / "run_started.json"
    write_json_new(
        run_started_path,
        {
            "schema_version": "rq2b-skillrouter-run-start-v1",
            "version_id": VERSION_ID,
            "run_id": run_id,
            "payload_sha256": sha256_file(payload_path),
            "authorisation_sha256": sha256_file(authorisation_path),
            "windows": len(windows),
            "pairs": len(pairs),
            "conditions": len(conditions),
            "batch_size": batch_size,
            "automatic_retries": 0,
        },
    )
    cache = WindowScoreCache(root / "skill_benchmark/cache/rq2b/reranker")
    window_scores: dict[str, float] = {}
    missing: list[dict[str, Any]] = []
    for window in windows:
        score = cache.load(
            representation=window["representation"],
            query=window["query"],
            document_window=window["document_window"],
        )
        if score is None:
            missing.append(window)
        else:
            window_scores[window["window_id"]] = score
    newly_scored, model_ledger = score_missing_windows(
        missing,
        cache=cache,
        device=device,
        batch_size=batch_size,
        authorisation=authorisation,
        progress_dir=staging / "model_batches",
    )
    window_scores.update(newly_scored)
    aggregation_started = time.perf_counter()
    pair_scores: dict[str, dict[str, float]] = {}
    for pair in pairs:
        scores = [window_scores[window_id] for window_id in pair["window_ids"]]
        pair_scores[pair["pair_id"]] = {
            "maximum_window_score": max(scores),
            "mean_window_score": sum(scores) / len(scores),
            "winning_window_index": max(range(len(scores)), key=lambda index: (scores[index], -index)),
        }
    prompt_manifest = read_jsonl(root / payload["prompt_manifest"]["path"])
    prompt_by_id = {row["prompt_id"]: row for row in prompt_manifest}
    result_rows: list[dict[str, Any]] = []
    for condition in conditions:
        condition_started = time.perf_counter()
        result = rerank_one(condition, pair_scores, prompt_by_id[condition["prompt_id"]])
        result["rerank_aggregation_seconds"] = time.perf_counter() - condition_started
        result_rows.append(result)
    verify_denominator_identity(result_rows)
    aggregation_elapsed_seconds = time.perf_counter() - aggregation_started
    rows_path = staging / "rows.jsonl"
    pair_scores_path = staging / "pair_scores.json"
    runtime_ledger_path = staging / "runtime_ledger.json"
    write_jsonl_new(rows_path, result_rows)
    write_json_new(pair_scores_path, pair_scores)
    write_json_new(
        runtime_ledger_path,
        {
            **model_ledger,
            "aggregation_elapsed_seconds": aggregation_elapsed_seconds,
            "cache_hits": len(windows) - len(missing),
            "cache_misses": len(missing),
            "automatic_retries": 0,
        },
    )
    manifest = {
        "schema_version": "rq2b-skillrouter-run-manifest-v1",
        "version_id": VERSION_ID,
        "state": "complete_scientific_b2",
        "run_id": run_id,
        "runner_version": RUNNER_VERSION,
        "model": MODEL,
        "revision": REVISION,
        "prompt_sha256": PROMPT_SHA256,
        "tokenizer_sha256": TOKENIZER_SHA256,
        "model_weights_sha256": MODEL_WEIGHTS_SHA256,
        "model_config_sha256": MODEL_CONFIG_SHA256,
        "payload_sha256": sha256_file(payload_path),
        "payload_path": relative(payload_path, root),
        "authorisation_sha256": sha256_file(authorisation_path),
        "authorisation_path": relative(authorisation_path, root),
        "cache_hits": len(windows) - len(missing),
        "cache_misses": len(missing),
        "model_forward_batch_attempts": model_ledger["model_forward_batch_attempts"],
        "model_forward_batches": model_ledger["model_forward_batch_successes"],
        "model_scored_windows": model_ledger["model_scored_windows"],
        "new_model_input_tokens": model_ledger["new_model_input_tokens"],
        "model_elapsed_seconds": model_ledger["model_elapsed_seconds"],
        "model_load_seconds": model_ledger["model_load_seconds"],
        "input_preparation_seconds": model_ledger["input_preparation_seconds"],
        "model_forward_seconds": model_ledger["model_forward_seconds"],
        "aggregation_elapsed_seconds": aggregation_elapsed_seconds,
        "requested_device": device,
        "resolved_device": model_ledger.get("resolved_device"),
        "model_dtype": model_ledger.get("model_dtype"),
        "batch_size": batch_size,
        "automatic_retries": 0,
        "denominator_identity_passed": True,
        "artifacts": {
            "rows": {"path": relative(output_dir / rows_path.name, root), "sha256": sha256_file(rows_path), "rows": len(result_rows)},
            "pair_scores": {"path": relative(output_dir / pair_scores_path.name, root), "sha256": sha256_file(pair_scores_path), "pairs": len(pair_scores)},
            "run_started": {"path": relative(output_dir / run_started_path.name, root), "sha256": sha256_file(run_started_path)},
            "runtime_ledger": {"path": relative(output_dir / runtime_ledger_path.name, root), "sha256": sha256_file(runtime_ledger_path)},
        },
    }
    write_json_new(staging / "manifest.json", manifest)
    staging.replace(output_dir)
    return manifest


def self_test() -> dict[str, Any]:
    candidates = [f"s{index:02d}" for index in range(PRIMARY_K)]
    condition = {
        "condition_id": "synthetic",
        "first_stage_retriever": "qwen-max-chunk",
        "representation": "i3c-fielded-evidence",
        "prompt_id": "p1",
        "stratum": "controlled",
        "candidate_skill_ids": candidates,
        "pair_ids_by_skill": {skill_id: f"pair-{skill_id}" for skill_id in candidates},
    }
    scores = {
        f"pair-{skill_id}": {
            "maximum_window_score": float(index),
            "mean_window_score": float(index) - 0.1,
        }
        for index, skill_id in enumerate(candidates)
    }
    prompt = {"gold_skill": candidates[-1], "valid_skills": [candidates[-1]]}
    row = rerank_one(condition, scores, prompt)
    require(row["candidate_positive"] == 1, "SkillRouter candidate-positive self-test failed")
    require(row["reranked_acceptable_top1"] == 1, "SkillRouter rerank self-test failed")
    require(row["reranker_gain"] == 1, "SkillRouter gain self-test failed")
    require(row["reranked_strict_top1"] == 1, "SkillRouter strict rerank self-test failed")
    require(row["end_to_end_strict_reciprocal_rank"] == 1.0, "SkillRouter strict MRR self-test failed")
    verify_denominator_identity([row])
    with tempfile.TemporaryDirectory() as directory:
        cache = WindowScoreCache(Path(directory))
        require(cache.load(representation="i3c-fielded-evidence", query="q", document_window="d") is None, "SkillRouter empty cache self-test failed")
        cache.store(representation="i3c-fielded-evidence", query="q", document_window="d", model_token_count=10, score=0.5)
        require(cache.load(representation="i3c-fielded-evidence", query="q", document_window="d") == 0.5, "SkillRouter cache round-trip failed")
        empty_scores, empty_ledger = score_missing_windows(
            [],
            cache=cache,
            device="cpu",
            batch_size=8,
            authorisation={
                "maximum_new_windows": 0,
                "maximum_model_forward_batches": 0,
                "maximum_new_model_input_tokens": 0,
            },
            progress_dir=Path(directory) / "empty-progress",
        )
        require(empty_scores == {}, "SkillRouter empty scoring self-test failed")
        require(
            empty_ledger["model_forward_batch_attempts"]
            == empty_ledger["model_forward_batch_successes"]
            == empty_ledger["model_scored_windows"]
            == 0,
            "SkillRouter empty model-ledger self-test failed",
        )
    return {
        "state": "synthetic_no_model_forward_no_scientific_result",
        "network_calls": 0,
        "candidate_count": PRIMARY_K,
        "reranked_top1": row["reranked_skill_ids"][0],
        "k5_new_model_forwards": row["k5_new_model_forwards"],
        "denominator_identity_passed": True,
        "cache_roundtrip": True,
        "empty_model_ledger": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--payload-manifest", type=Path)
    parser.add_argument("--authorisation", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        require(args.execute, "SkillRouter execution requires --execute and a separate authorisation")
        require(args.payload_manifest is not None, "--payload-manifest is required")
        require(args.authorisation is not None, "--authorisation is required")
        require(args.output_dir is not None, "--output-dir is required")
        require(args.run_id is not None, "--run-id is required")
        root = args.root.resolve()
        payload = args.payload_manifest if args.payload_manifest.is_absolute() else root / args.payload_manifest
        authorisation = args.authorisation if args.authorisation.is_absolute() else root / args.authorisation
        output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
        result = run(root, payload, authorisation, output_dir, args.run_id, args.device, args.batch_size)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
