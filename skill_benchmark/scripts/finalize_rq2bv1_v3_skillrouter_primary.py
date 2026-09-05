#!/usr/bin/env python3
"""Score and verify returned V3 SkillRouter embeddings locally, with no network."""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from rq2bv1_v3_skillrouter_primary_constants import (
    CACHE_ROOT,
    DIMENSIONS,
    MODEL,
    PREFLIGHT_ROOT,
    REPRESENTATIONS,
    RESULT_ROOT,
    REVISION,
)
from rq2b_common import read_json, read_jsonl, relative, repo_root, require, sha256_file, write_json_new, write_jsonl_new
from rq2b_v11_execution_contract import B1_SCHEMA, validate_b1_row
from run_rq2bv1_v3_skillrouter_primary import ExactEmbeddingCache


FINALIZER_VERSION = "rq2bv1-v3-skillrouter-primary-local-finalizer-v1"
HOSTED_ROOT = f"{RESULT_ROOT}/hosted_embedding"
LOCAL_OUTPUT_ROOT = f"{RESULT_ROOT}/local_scoring"


def _normalise(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in values))
    require(math.isfinite(norm) and norm > 0.0, "Invalid SkillRouter vector norm")
    return [value / norm for value in values]


def _load_payload(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    path = root / PREFLIGHT_ROOT / "payload_manifest.json"
    payload = read_json(path)
    require(payload.get("state") == "sealed_not_executed", "SkillRouter payload state drift")
    inventory_path = root / payload["text_inventory"]["path"]
    require(sha256_file(inventory_path) == payload["text_inventory"]["sha256"], "SkillRouter inventory drift")
    rows = read_jsonl(inventory_path)
    require(len(rows) == int(payload["text_inventory"]["rows"]), "SkillRouter inventory count drift")
    return payload, rows


def _load_hosted_run(root: Path) -> dict[str, Any]:
    path = root / HOSTED_ROOT / "manifest.json"
    manifest = read_json(path)
    require(manifest.get("state") == "hosted_embedding_complete_pending_local_scoring", "Hosted SkillRouter embedding is incomplete")
    require(manifest.get("hosted_scoring") is False and manifest.get("gold_labels_transferred") is False, "Hosted scope drift")
    return manifest


def _forward_timings(root: Path, manifest: dict[str, Any]) -> dict[str, float]:
    timings: dict[str, float] = {}
    for binding in manifest["forward_records"]:
        path = root / binding["path"]
        require(sha256_file(path) == binding["sha256"], f"Forward record drift: {path}")
        record = read_json(path)
        elapsed = float(record["elapsed_seconds"])
        require(math.isfinite(elapsed) and elapsed >= 0.0, f"Forward timing invalid: {path}")
        per_item = elapsed / int(record["items"])
        for text_id in record["text_ids"]:
            require(text_id not in timings, f"Duplicate forward timing: {text_id}")
            timings[text_id] = per_item
    return timings


def _row(
    prompt: dict[str, Any],
    ranking: list[tuple[str, float]],
    *,
    representation: str,
    selector_tokens: int,
    document_seconds: float,
    cold_query_seconds: float,
    cache_shared_texts: int,
) -> dict[str, Any]:
    rank_by_skill = {skill_id: index for index, (skill_id, _) in enumerate(ranking, start=1)}
    strict_rank = rank_by_skill[prompt["gold_skill"]]
    top100 = ranking[:100]
    row = {
        "schema_version": B1_SCHEMA,
        "version_id": "rq2b-full-library-v1.1-2026-08-15",
        "runner_version": FINALIZER_VERSION,
        "retriever": "skillrouter-embedding-0.6b",
        "representation": representation,
        "prompt_id": prompt["prompt_id"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
        "strict_gold_rank": strict_rank,
        "strict_hit_at_1": int(strict_rank == 1),
        "strict_recall_at_5": int(strict_rank <= 5),
        "strict_recall_at_20": int(strict_rank <= 20),
        "strict_recall_at_50": int(strict_rank <= 50),
        "strict_recall_at_100": int(strict_rank <= 100),
        "strict_mrr_at_10": 0.0 if strict_rank > 10 else 1.0 / strict_rank,
        "top_5_skill_ids": [skill_id for skill_id, _ in ranking[:5]],
        "top_20_skill_ids": [skill_id for skill_id, _ in ranking[:20]],
        "top_50_skill_ids": [skill_id for skill_id, _ in ranking[:50]],
        "top_100": [
            {"rank": index, "skill_id": skill_id, "score": float(score)}
            for index, (skill_id, score) in enumerate(top100, start=1)
        ],
        "query_seconds": 0.0,
        "selector_visible_tokens": selector_tokens,
        "one_time_document_embedding_or_index_seconds": document_seconds,
        "retriever_metadata": {
            "model": MODEL,
            "revision": REVISION,
            "dimensions": DIMENSIONS,
            "document_aggregation": "single_full_context_cosine",
            "cold_query_embedding_seconds": cold_query_seconds,
            "shared_document_cache_texts": cache_shared_texts,
        },
    }
    validate_b1_row(row, prompt, f"skillrouter-v3:{representation}:{prompt['prompt_id']}")
    return row


def _score(payload: dict[str, Any], vectors: dict[str, list[float]], prompts: list[dict[str, Any]], timings: dict[str, float]) -> list[dict[str, Any]]:
    import numpy as np

    prompt_by_id = {str(prompt["prompt_id"]): prompt for prompt in prompts}
    require(len(prompt_by_id) == 381, "Strict prompt identity drift")
    rows: list[dict[str, Any]] = []
    for representation in REPRESENTATIONS:
        documents = payload["documents"][representation]
        require(len(documents) == 2433, f"Candidate count drift: {representation}")
        skill_ids = [str(document["skill_id"]) for document in documents]
        require(len(skill_ids) == len(set(skill_ids)), f"Candidate IDs drift: {representation}")
        document_text_ids = [str(document["text_id"]) for document in documents]
        matrix = np.asarray([vectors[text_id] for text_id in document_text_ids], dtype=np.float64)
        matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
        selector_tokens = sum(
            int(payload["_inventory_by_id"][text_id]["model_tokens"])
            for text_id in document_text_ids
        )
        document_seconds = sum(timings[text_id] for text_id in document_text_ids)
        shared_texts = len(document_text_ids) - len(set(document_text_ids))
        for prompt_id, query_text_id in payload["query_text_ids"].items():
            query = np.asarray(_normalise(vectors[query_text_id]), dtype=np.float64)
            started = time.perf_counter()
            scores = matrix @ query
            ranking = list(zip(skill_ids, (float(score) for score in scores), strict=True))
            ranking.sort(key=lambda item: (-item[1], item[0]))
            row = _row(
                prompt_by_id[prompt_id],
                ranking,
                representation=representation,
                selector_tokens=selector_tokens,
                document_seconds=document_seconds,
                cold_query_seconds=timings[query_text_id],
                cache_shared_texts=shared_texts,
            )
            row["query_seconds"] = time.perf_counter() - started
            validate_b1_row(row, prompt_by_id[prompt_id], f"skillrouter-v3:{representation}:{prompt_id}")
            rows.append(row)
    require(len(rows) == 1524, "SkillRouter primary row-count drift")
    return rows


def _warm_replay(payload: dict[str, Any], vectors: dict[str, list[float]], prompts: list[dict[str, Any]], timings: dict[str, float], rows: list[dict[str, Any]]) -> dict[str, Any]:
    expected = {(row["representation"], row["prompt_id"]): row for row in rows}
    replay = _score(payload, vectors, prompts, timings)
    require(len(replay) == len(expected), "Warm replay row count drift")
    for row in replay:
        actual = expected[(row["representation"], row["prompt_id"])]
        require(row["strict_gold_rank"] == actual["strict_gold_rank"], "Warm replay rank drift")
        require(row["top_100"] == actual["top_100"], "Warm replay ranking drift")
    return {"state": "passed_zero_forward_warm_replay", "verified_conditions": len(replay)}


def finalise(root: Path) -> dict[str, Any]:
    payload, inventory = _load_payload(root)
    hosted = _load_hosted_run(root)
    timings = _forward_timings(root, hosted)
    require(set(timings) == {row["text_id"] for row in inventory}, "Forward timing coverage drift")
    cache = ExactEmbeddingCache(root / CACHE_ROOT)
    vectors = {str(row["text_id"]): cache.load(str(row["text"])) for row in inventory}
    require(all(vector is not None for vector in vectors.values()), "Returned cache coverage incomplete")
    vectors = {text_id: vector for text_id, vector in vectors.items() if vector is not None}
    payload["_inventory_by_id"] = {str(row["text_id"]): row for row in inventory}
    prompt_path = root / payload["prompt_artifact"]["path"]
    require(sha256_file(prompt_path) == payload["prompt_artifact"]["sha256"], "Strict prompt artifact drift")
    prompts = read_jsonl(prompt_path)
    output_root = root / LOCAL_OUTPUT_ROOT
    require(not output_root.exists(), f"Refusing to overwrite local SkillRouter scoring output: {output_root}")
    output_root.mkdir(parents=True, exist_ok=False)
    rows = _score(payload, vectors, prompts, timings)
    warm = _warm_replay(payload, vectors, prompts, timings, rows)
    rows_path = output_root / "skillrouter_primary_strict_results.jsonl"
    write_jsonl_new(rows_path, rows)
    manifest = {
        "schema_version": "rq2bv1-v3-skillrouter-primary-local-scoring-manifest-v1",
        "state": "completed_pending_user_result_review",
        "runner_version": FINALIZER_VERSION,
        "method": {
            "retriever": "skillrouter-embedding-0.6b",
            "document_aggregation": "single_full_context_cosine",
            "field_aware": False,
            "reranking": False,
        },
        "hosted_embedding": {"path": relative(root / HOSTED_ROOT / "manifest.json", root), "sha256": sha256_file(root / HOSTED_ROOT / "manifest.json")},
        "rows": {"path": relative(rows_path, root), "sha256": sha256_file(rows_path), "rows": len(rows)},
        "warm_replay": warm,
        "network_calls": 0,
        "thesis_result_writing": False,
    }
    write_json_new(output_root / "manifest.json", manifest)
    return manifest


def self_test() -> dict[str, Any]:
    prompt = {"prompt_id": "p", "prompt_sha256": "h", "stratum": "controlled", "group": "g", "gold_skill": "a"}
    row = _row(prompt, [("a", 1.0), ("b", 0.0), *[(f"x{i}", -float(i)) for i in range(2, 2433)]], representation="i1-discovery", selector_tokens=1, document_seconds=0.0, cold_query_seconds=0.0, cache_shared_texts=0)
    require(row["strict_hit_at_1"] == 1 and len(row["top_100"]) == 100, "Synthetic scoring regression")
    return {"state": "self_test_passed_no_network", "network_calls": 0, "scientific_retrieval_or_reranking": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--finalise", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.finalise, "Choose exactly one of --self-test or --finalise")
    result = self_test() if args.self_test else finalise(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
