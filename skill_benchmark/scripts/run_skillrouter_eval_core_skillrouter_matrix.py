#!/usr/bin/env python3

from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import sys
import time
import traceback
from pathlib import Path
from typing import Any

import torch

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_skillrouter_eval_core_fts_ablation import (  # noqa: E402
    dcg,
    load_relevance,
    load_scored_tasks,
    summarize_task_rows,
)
from run_offline_selectors import approximate_tokens  # noqa: E402
from run_skillrouter_selectors import (  # noqa: E402
    QUERY_INSTRUCTION,
    SkillRouterEmbedder,
    SkillRouterReranker,
    load_dotenv,
    select_device,
    sha256_text,
)


ROOT = Path("skill_benchmark/external/skillrouter_eval_core")
RAW_DIR = ROOT / "raw"
DERIVED_DIR = ROOT / "derived"
OUTPUT_DIR = ROOT / "outputs"


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def iter_raw_tier_rows(raw_dir: Path, tier: str):
    for path in sorted((raw_dir / tier).glob("*.jsonl.gz")):
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)


def official_skillrouter_text(row: dict[str, Any], *, include_body: bool) -> str:
    name = str(row.get("name") or row.get("skill_id") or "")
    description = str(row.get("description") or "")
    if not include_body:
        return f"{name} | {description}".strip()
    body = str(row.get("body") or "")
    return f"{name} | {description} | {body}".strip()


def strip_i3c_header(text: str) -> str:
    lines = text.splitlines()
    index = 0
    if index < len(lines) and lines[index].startswith("name:"):
        index += 1
    if index < len(lines) and lines[index].startswith("description:"):
        index += 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    return "\n".join(lines[index:]).strip()


def strip_derived_metadata_header(text: str) -> str:
    lines = text.splitlines()
    index = 0
    metadata_prefixes = ("skill_id:", "name:", "source:", "description:")
    while index < len(lines) and lines[index].startswith(metadata_prefixes):
        index += 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    return "\n".join(lines[index:]).strip()


def derived_skillrouter_text(row: dict[str, Any], *, include_body: bool) -> str:
    name = str(row.get("name") or row.get("skill_id") or "")
    description = str(row.get("description") or "")
    if not include_body:
        return f"{name} | {description}".strip()
    body = strip_derived_metadata_header(str(row.get("text") or ""))
    return f"{name} | {description} | {body}".strip()


def i3c_skillrouter_text(row: dict[str, Any]) -> str:
    name = str(row.get("name") or row.get("skill_id") or "")
    description = str(row.get("description") or "")
    structured_body = strip_i3c_header(str(row.get("text") or ""))
    return f"{name} | {description} | {structured_body}".strip()


def load_derived_representation(
    path: Path,
    representation: str,
    max_docs: int | None = None,
) -> tuple[list[str], list[str], list[str]]:
    skill_ids: list[str] = []
    names: list[str] = []
    docs: list[str] = []
    for row in iter_jsonl(path):
        skill_ids.append(str(row["skill_id"]))
        names.append(str(row.get("name") or row["skill_id"]))
        if representation.upper() == "I3C":
            docs.append(i3c_skillrouter_text(row))
        elif representation.upper() in {"I1", "FULL", "I2"}:
            docs.append(derived_skillrouter_text(row, include_body=representation.upper() in {"FULL", "I2"}))
        else:
            docs.append(str(row.get("text") or ""))
        if max_docs and len(skill_ids) >= max_docs:
            break
    return skill_ids, names, docs


def load_raw_representation(
    raw_dir: Path,
    tier: str,
    representation: str,
    max_docs: int | None = None,
) -> tuple[list[str], list[str], list[str]]:
    skill_ids: list[str] = []
    names: list[str] = []
    docs: list[str] = []
    include_body = representation.upper() in {"FULL", "I2"}
    for row in iter_raw_tier_rows(raw_dir, tier):
        skill_ids.append(str(row["skill_id"]))
        names.append(str(row.get("name") or row["skill_id"]))
        docs.append(official_skillrouter_text(row, include_body=include_body))
        if max_docs and len(skill_ids) >= max_docs:
            break
    return skill_ids, names, docs


def load_representation(
    *,
    raw_dir: Path,
    derived_dir: Path,
    tier: str,
    representation: str,
    max_docs: int | None = None,
) -> tuple[list[str], list[str], list[str]]:
    rep = representation.upper()
    if rep in {"I1", "FULL", "I2"}:
        raw_paths = list((raw_dir / tier).glob("*.jsonl.gz"))
        if raw_paths:
            return load_raw_representation(raw_dir, tier, rep, max_docs=max_docs)
        derived_rep = "I2" if rep in {"FULL", "I2"} else "I1"
        return load_derived_representation(
            representation_path(derived_dir, tier, derived_rep),
            rep,
            max_docs=max_docs,
        )
    rep_path = representation_path(derived_dir, tier, rep)
    return load_derived_representation(rep_path, rep, max_docs=max_docs)


def representation_path(derived_dir: Path, tier: str, representation: str) -> Path:
    return derived_dir / "representations" / f"{tier}_{representation.upper()}.jsonl"


def evaluate_ranking(
    ranked_ids: list[str],
    relevance_row: dict[str, Any],
    cutoffs: list[int],
) -> dict[str, Any]:
    gold_ids = set(relevance_row.get("core_gt_ids") or relevance_row.get("gt_skill_ids") or [])
    graded_relevance = {
        str(skill_id): float(grade)
        for skill_id, grade in (relevance_row.get("relevance") or {}).items()
    }
    if not gold_ids:
        return {
            "hit_at_1": 0.0,
            "mrr_at_10": 0.0,
            "recall": {str(k): 0.0 for k in cutoffs},
            "full_coverage": {str(k): 0.0 for k in cutoffs},
            "ndcg_at_10": 0.0,
        }

    hit_at_1 = float(bool(ranked_ids and ranked_ids[0] in gold_ids))
    first_rank = next((index + 1 for index, skill_id in enumerate(ranked_ids[:10]) if skill_id in gold_ids), None)
    recall = {
        str(k): len(gold_ids & set(ranked_ids[:k])) / len(gold_ids)
        for k in cutoffs
    }
    full_coverage = {
        str(k): float(gold_ids.issubset(set(ranked_ids[:k])))
        for k in cutoffs
    }
    grades = [graded_relevance.get(skill_id, 0.0) for skill_id in ranked_ids[:10]]
    ideal_grades = sorted(graded_relevance.values(), reverse=True)[:10]
    ideal = dcg(ideal_grades)
    return {
        "hit_at_1": hit_at_1,
        "mrr_at_10": 1.0 / first_rank if first_rank else 0.0,
        "recall": recall,
        "full_coverage": full_coverage,
        "ndcg_at_10": dcg(grades) / ideal if ideal else 0.0,
    }


def topk_from_scores(
    skill_ids: list[str],
    names: list[str],
    scores: torch.Tensor,
    limit: int,
) -> list[list[dict[str, Any]]]:
    limit = min(limit, len(skill_ids))
    values, indices = torch.topk(scores, k=limit, dim=1, largest=True, sorted=True)
    rankings: list[list[dict[str, Any]]] = []
    for row_values, row_indices in zip(values.tolist(), indices.tolist()):
        rankings.append(
            [
                {
                    "skill_id": skill_ids[index],
                    "name": names[index],
                    "score": round(float(score), 6),
                }
                for score, index in zip(row_values, row_indices)
            ]
        )
    return rankings


def doc_embedding_cache_prefix(output_prefix: str, tier: str, representation: str) -> str:
    return f"{output_prefix}_docemb_{tier}_{representation.upper()}"


def doc_embedding_manifest_path(output_dir: Path, output_prefix: str, tier: str, representation: str) -> Path:
    return output_dir / f"{doc_embedding_cache_prefix(output_prefix, tier, representation)}_manifest.json"


def doc_embedding_shard_path(
    output_dir: Path,
    output_prefix: str,
    tier: str,
    representation: str,
    start: int,
    end: int,
) -> Path:
    prefix = doc_embedding_cache_prefix(output_prefix, tier, representation)
    return output_dir / f"{prefix}_shard_{start:06d}_{end:06d}.pt"


def load_valid_doc_shard(
    path: Path,
    *,
    expected_skill_ids: list[str],
    expected_hashes: list[str],
    embedding_model: str,
    embedding_max_length: int,
) -> tuple[torch.Tensor, dict[str, Any]] | None:
    if not path.exists():
        return None
    try:
        payload = torch.load(path, map_location="cpu")
    except Exception as exc:
        print(f"[doc-cache] ignoring unreadable shard {path.name}: {exc}", flush=True)
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("skill_ids") != expected_skill_ids:
        print(f"[doc-cache] ignoring shard with mismatched skill ids: {path.name}", flush=True)
        return None
    if payload.get("text_hashes") != expected_hashes:
        print(f"[doc-cache] ignoring shard with mismatched text hashes: {path.name}", flush=True)
        return None
    if payload.get("embedding_model") != embedding_model:
        print(f"[doc-cache] ignoring shard with mismatched embedding model: {path.name}", flush=True)
        return None
    if int(payload.get("embedding_max_length", -1)) != embedding_max_length:
        print(f"[doc-cache] ignoring shard with mismatched max length: {path.name}", flush=True)
        return None
    embeddings = payload.get("embeddings")
    if not isinstance(embeddings, torch.Tensor):
        return None
    if embeddings.shape[0] != len(expected_skill_ids):
        print(f"[doc-cache] ignoring shard with wrong row count: {path.name}", flush=True)
        return None
    return embeddings.float(), payload


def write_doc_embedding_manifest(
    *,
    output_dir: Path,
    output_prefix: str,
    tier: str,
    representation: str,
    embedding_model: str,
    embedding_max_length: int,
    skill_ids: list[str],
    text_hashes: list[str],
    shard_size: int,
    shard_records: list[dict[str, Any]],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = doc_embedding_manifest_path(output_dir, output_prefix, tier, representation)
    manifest = {
        "cache_version": 1,
        "output_prefix": output_prefix,
        "tier": tier,
        "representation": representation.upper(),
        "embedding_model": embedding_model,
        "embedding_max_length": embedding_max_length,
        "skill_count": len(skill_ids),
        "skill_ids_hash": sha256_text("\n".join(skill_ids)),
        "text_hashes_hash": sha256_text("\n".join(text_hashes)),
        "shard_size": shard_size,
        "complete_shard_count": len(shard_records),
        "shards": shard_records,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def load_or_compute_doc_embeddings(
    *,
    tier: str,
    representation: str,
    skill_ids: list[str],
    docs: list[str],
    embedder: SkillRouterEmbedder,
    embedding_batch_size: int,
    embedding_model: str,
    embedding_max_length: int,
    output_dir: Path,
    output_prefix: str,
    doc_embedding_shard_size: int,
    hub_repo_id: str,
    hub_repo_type: str,
    hub_output_dir: str,
    hub_token_env: str,
    upload_shards: bool,
) -> tuple[torch.Tensor, dict[str, Any]]:
    if doc_embedding_shard_size <= 0:
        doc_start = time.perf_counter()
        print(f"[{tier}_{representation.upper()}] embedding documents without shard cache...", flush=True)
        embeddings = embedder.encode(docs, embedding_batch_size)
        elapsed_ms = (time.perf_counter() - doc_start) * 1000
        return embeddings, {
            "doc_embedding_elapsed_ms": elapsed_ms,
            "doc_embedding_runtime_elapsed_ms": elapsed_ms,
            "doc_embedding_compute_elapsed_ms": elapsed_ms,
            "doc_embedding_load_elapsed_ms": 0.0,
            "doc_embedding_cache_shards_hit": 0,
            "doc_embedding_cache_shards_missed": 0,
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    text_hashes = [sha256_text(doc) for doc in docs]
    shard_tensors: list[torch.Tensor] = []
    shard_records: list[dict[str, Any]] = []
    compute_elapsed_ms = 0.0
    load_elapsed_ms = 0.0
    runtime_start = time.perf_counter()
    cache_hits = 0
    cache_misses = 0
    condition = f"{tier}_{representation.upper()}_doc_cache"

    for start in range(0, len(docs), doc_embedding_shard_size):
        end = min(start + doc_embedding_shard_size, len(docs))
        shard_path = doc_embedding_shard_path(output_dir, output_prefix, tier, representation, start, end)
        expected_skill_ids = skill_ids[start:end]
        expected_hashes = text_hashes[start:end]
        load_start = time.perf_counter()
        loaded = load_valid_doc_shard(
            shard_path,
            expected_skill_ids=expected_skill_ids,
            expected_hashes=expected_hashes,
            embedding_model=embedding_model,
            embedding_max_length=embedding_max_length,
        )
        if loaded is not None:
            embeddings, payload = loaded
            cache_hits += 1
            load_elapsed_ms += (time.perf_counter() - load_start) * 1000
            shard_compute_ms = float(payload.get("compute_elapsed_ms", 0.0))
            compute_elapsed_ms += shard_compute_ms
            print(
                f"[{condition}] loaded shard {start}-{end} from cache "
                f"(original_compute_ms={shard_compute_ms:.1f})",
                flush=True,
            )
        else:
            cache_misses += 1
            print(f"[{condition}] embedding shard {start}-{end}...", flush=True)
            shard_start = time.perf_counter()
            embeddings = embedder.encode(docs[start:end], embedding_batch_size)
            shard_compute_ms = (time.perf_counter() - shard_start) * 1000
            compute_elapsed_ms += shard_compute_ms
            payload = {
                "cache_version": 1,
                "tier": tier,
                "representation": representation.upper(),
                "embedding_model": embedding_model,
                "embedding_max_length": embedding_max_length,
                "start": start,
                "end": end,
                "skill_ids": expected_skill_ids,
                "text_hashes": expected_hashes,
                "compute_elapsed_ms": round(shard_compute_ms, 2),
                "embeddings": embeddings.cpu(),
            }
            torch.save(payload, shard_path)
            print(
                f"[{condition}] saved shard {shard_path.name} "
                f"compute_ms={shard_compute_ms:.1f}",
                flush=True,
            )

        shard_tensors.append(embeddings.cpu())
        shard_records.append(
            {
                "path": shard_path.name,
                "start": start,
                "end": end,
                "row_count": end - start,
                "text_hashes_hash": sha256_text("\n".join(expected_hashes)),
                "compute_elapsed_ms": round(shard_compute_ms, 2),
            }
        )
        manifest_path = write_doc_embedding_manifest(
            output_dir=output_dir,
            output_prefix=output_prefix,
            tier=tier,
            representation=representation,
            embedding_model=embedding_model,
            embedding_max_length=embedding_max_length,
            skill_ids=skill_ids,
            text_hashes=text_hashes,
            shard_size=doc_embedding_shard_size,
            shard_records=shard_records,
        )
        if upload_shards and hub_repo_id and hub_output_dir and loaded is None:
            upload_progress_files(
                repo_id=hub_repo_id,
                repo_type=hub_repo_type,
                output_dir=hub_output_dir,
                paths=[shard_path, manifest_path],
                token_env=hub_token_env,
                condition=condition,
            )

    runtime_elapsed_ms = (time.perf_counter() - runtime_start) * 1000
    return torch.cat(shard_tensors, dim=0), {
        "doc_embedding_elapsed_ms": compute_elapsed_ms,
        "doc_embedding_runtime_elapsed_ms": runtime_elapsed_ms,
        "doc_embedding_compute_elapsed_ms": compute_elapsed_ms,
        "doc_embedding_load_elapsed_ms": load_elapsed_ms,
        "doc_embedding_cache_shards_hit": cache_hits,
        "doc_embedding_cache_shards_missed": cache_misses,
        "doc_embedding_shard_size": doc_embedding_shard_size,
    }


def run_condition(
    *,
    tier: str,
    representation: str,
    mode: str,
    tasks: list[dict[str, Any]],
    relevance: dict[str, Any],
    raw_dir: Path,
    derived_dir: Path,
    ranking_limit: int,
    cutoffs: list[int],
    hard_only_ids: set[str],
    embedder: SkillRouterEmbedder,
    reranker: SkillRouterReranker | None,
    embedding_batch_size: int,
    embedding_model: str,
    embedding_max_length: int,
    rerank_candidates: int,
    max_docs: int | None,
    output_dir: Path,
    output_prefix: str,
    doc_embedding_shard_size: int,
    hub_repo_id: str,
    hub_repo_type: str,
    hub_output_dir: str,
    hub_token_env: str,
    upload_doc_embedding_shards: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    condition_label = f"{tier}_{representation.upper()}_{mode}"
    print(f"[{condition_label}] loading {tier}/{representation.upper()} documents...", flush=True)
    skill_ids, names, docs = load_representation(
        raw_dir=raw_dir,
        derived_dir=derived_dir,
        tier=tier,
        representation=representation,
        max_docs=max_docs,
    )
    if not skill_ids:
        raise RuntimeError(f"No docs loaded for {tier}/{representation}")
    print(
        f"[{condition_label}] loaded {len(skill_ids)} documents; "
        f"approx selector-visible tokens={sum(approximate_tokens(doc) for doc in docs)}",
        flush=True,
    )
    doc_by_skill_id = dict(zip(skill_ids, docs))

    print(f"[{condition_label}] preparing document embeddings...", flush=True)
    doc_embeddings, doc_embedding_stats = load_or_compute_doc_embeddings(
        tier=tier,
        representation=representation,
        skill_ids=skill_ids,
        docs=docs,
        embedder=embedder,
        embedding_batch_size=embedding_batch_size,
        embedding_model=embedding_model,
        embedding_max_length=embedding_max_length,
        output_dir=output_dir,
        output_prefix=output_prefix,
        doc_embedding_shard_size=doc_embedding_shard_size,
        hub_repo_id=hub_repo_id,
        hub_repo_type=hub_repo_type,
        hub_output_dir=hub_output_dir,
        hub_token_env=hub_token_env,
        upload_shards=upload_doc_embedding_shards,
    )
    print(
        f"[{condition_label}] document embeddings ready; "
        f"fixed_compute_ms={doc_embedding_stats['doc_embedding_compute_elapsed_ms']:.1f} "
        f"runtime_ms={doc_embedding_stats['doc_embedding_runtime_elapsed_ms']:.1f}",
        flush=True,
    )

    query_texts = [QUERY_INSTRUCTION + str(task["instruction_text"]) for task in tasks]
    query_start = time.perf_counter()
    print(f"[{condition_label}] embedding {len(query_texts)} queries...", flush=True)
    query_embeddings = embedder.encode(query_texts, embedding_batch_size)
    query_embedding_elapsed_ms = (time.perf_counter() - query_start) * 1000
    print(f"[{condition_label}] query embeddings complete in {query_embedding_elapsed_ms:.1f} ms", flush=True)

    retrieval_start = time.perf_counter()
    print(f"[{condition_label}] computing dense retrieval scores...", flush=True)
    scores = query_embeddings @ doc_embeddings.T
    first_stage_rankings = topk_from_scores(
        skill_ids,
        names,
        scores,
        limit=max(ranking_limit, rerank_candidates if mode == "rerank" else 0),
    )
    retrieval_elapsed_ms = (time.perf_counter() - retrieval_start) * 1000
    print(f"[{condition_label}] dense retrieval complete in {retrieval_elapsed_ms:.1f} ms", flush=True)

    rerank_elapsed_ms = 0.0
    rows: list[dict[str, Any]] = []
    for task_index, (task, first_stage) in enumerate(zip(tasks, first_stage_rankings), start=1):
        task_id = task["task_id"]
        rel = relevance[task_id]
        ranking = first_stage[:ranking_limit]
        if mode == "rerank":
            if reranker is None:
                raise RuntimeError("mode=rerank requires a reranker")
            if task_index == 1 or task_index % 10 == 0 or task_index == len(tasks):
                print(
                    f"[{condition_label}] reranking task {task_index}/{len(tasks)} "
                    f"with top-{rerank_candidates} candidates...",
                    flush=True,
                )
            rerank_start = time.perf_counter()
            candidate_count = min(rerank_candidates, len(first_stage))
            candidate_rows = first_stage[:candidate_count]
            candidate_docs = [doc_by_skill_id[row["skill_id"]] for row in candidate_rows]
            rerank_scores = reranker.score_many(str(task["instruction_text"]), candidate_docs)
            rerank_elapsed_ms += (time.perf_counter() - rerank_start) * 1000
            reranked = [
                {
                    "skill_id": row["skill_id"],
                    "name": row["name"],
                    "score": round(float(score), 6),
                    "first_stage_score": row["score"],
                }
                for row, score in zip(candidate_rows, rerank_scores)
            ]
            reranked.sort(key=lambda item: (-float(item["score"]), item["skill_id"]))
            ranking = reranked[:ranking_limit]

        ranked_ids = [row["skill_id"] for row in ranking]
        gold_ids = rel.get("core_gt_ids") or rel.get("gt_skill_ids") or []
        rows.append(
            {
                "task_id": task_id,
                "domain": task.get("domain"),
                "difficulty": task.get("difficulty"),
                "task_type": rel.get("task_type"),
                "num_gold_skills": len(gold_ids),
                "gold_skill_ids": gold_ids,
                "instruction_text": task.get("instruction_text"),
                "ranking": ranking,
                "first_stage_ranking": first_stage[:ranking_limit],
                "top1_hard_only": bool(ranking and ranking[0]["skill_id"] in hard_only_ids),
                "metrics": evaluate_ranking(ranked_ids, rel, cutoffs),
            }
        )

    summary = summarize_task_rows(rows, cutoffs)
    query_total_elapsed_ms = query_embedding_elapsed_ms + retrieval_elapsed_ms + rerank_elapsed_ms
    summary.update(
        {
            "tier": tier,
            "representation": representation.upper(),
            "mode": mode,
            "retriever": "SkillRouter embedding",
            "reranker": "SkillRouter reranker" if mode == "rerank" else "none",
            "ranking_limit": ranking_limit,
            "rerank_candidates": rerank_candidates if mode == "rerank" else 0,
            "skill_count": len(skill_ids),
            "selector_visible_tokens_approx": sum(approximate_tokens(doc) for doc in docs),
            "doc_embedding_elapsed_ms": round(float(doc_embedding_stats["doc_embedding_elapsed_ms"]), 2),
            "doc_embedding_runtime_elapsed_ms": round(float(doc_embedding_stats["doc_embedding_runtime_elapsed_ms"]), 2),
            "doc_embedding_compute_elapsed_ms": round(float(doc_embedding_stats["doc_embedding_compute_elapsed_ms"]), 2),
            "doc_embedding_load_elapsed_ms": round(float(doc_embedding_stats["doc_embedding_load_elapsed_ms"]), 2),
            "doc_embedding_cache_shards_hit": doc_embedding_stats["doc_embedding_cache_shards_hit"],
            "doc_embedding_cache_shards_missed": doc_embedding_stats["doc_embedding_cache_shards_missed"],
            "doc_embedding_shard_size": doc_embedding_stats.get("doc_embedding_shard_size", 0),
            "query_embedding_elapsed_ms": round(query_embedding_elapsed_ms, 2),
            "retrieval_elapsed_ms": round(retrieval_elapsed_ms, 2),
            "rerank_elapsed_ms": round(rerank_elapsed_ms, 2),
            "query_total_elapsed_ms": round(query_total_elapsed_ms, 2),
        }
    )
    return rows, summary


def pct(value: float) -> str:
    return f"{value:.1%}"


def render_markdown(report: dict[str, Any]) -> str:
    cutoffs = [str(value) for value in report["cutoffs"]]
    headers = [
        "Tier",
        "Layer",
        "Mode",
        "N",
        "Hit@1",
        "MRR@10",
        "nDCG@10",
        *[f"Recall@{value}" for value in cutoffs],
        *[f"FullCov@{value}" for value in cutoffs],
        "Hard-only top1",
        "Tokens",
        "Doc emb ms",
        "Query total ms",
    ]
    lines = [
        "# SkillRouter-Eval-Core External SkillRouter Neural Matrix",
        "",
        "This report runs the released SkillRouter embedding model, and optionally the released SkillRouter reranker, over the external SkillRouter-Eval-Core representation layers.",
        "",
        "`embedding` means SkillRouter embedding-only retrieval. `rerank` means SkillRouter embedding retrieval followed by SkillRouter reranking over the top candidates.",
        "",
        "`FULL` is serialized as the official full-skill document shape: `name | description | body`. `I1` uses `name | description`. `I3C` uses `name | description | cleaned I3C fields`.",
        "",
        f"- Source: `{report['source']}`",
        f"- Embedding model: `{report['embedding_model']}`",
        f"- Reranker model: `{report['reranker_model']}`",
        f"- Device: `{report['device']}`",
        f"- Scored tasks: {report['task_count']}",
        f"- Ranking limit: top-{report['ranking_limit']}",
        f"- Rerank candidates: top-{report['rerank_candidates']}",
        "",
        "## Summary",
        "",
        "| " + " | ".join(headers) + " |",
        "|---|---|---|" + "|".join(["---:"] * (len(headers) - 3)) + "|",
    ]
    for row in report["summary"]:
        values = [
            row["tier"],
            row["representation"],
            row["mode"],
            str(row["task_count"]),
            pct(row["hit_at_1"]),
            f"{row['mrr_at_10']:.3f}",
            f"{row['ndcg_at_10']:.3f}",
            *[pct(row["recall"][value]) for value in cutoffs],
            *[pct(row["full_coverage"][value]) for value in cutoffs],
            pct(row["hard_only_top1_rate"]),
            str(row["selector_visible_tokens_approx"] or ""),
            f"{row['doc_embedding_elapsed_ms']:.1f}",
            f"{row['query_total_elapsed_ms']:.1f}",
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            "## Metric Notes",
            "",
            "- `Hit@1` is the external analogue of strict top-1.",
            "- `MRR@10` is reciprocal rank of the first core gold skill.",
            "- `Recall@k` and `FullCov@k` are multi-skill metrics; they should be secondary for thesis comparison against the local single-gold benchmark.",
            "- `Doc emb ms` is fixed document-embedding compute cost; resumed runs also record `doc_embedding_runtime_elapsed_ms` for actual cache load/recompute time.",
            "- `Query total ms` includes query embedding, dense retrieval, and reranking for all scored tasks in the condition.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def condition_key(tier: str, representation: str, mode: str) -> str:
    return f"{tier}_{representation.upper()}_{mode}"


def parse_condition_set(raw_value: str | None) -> set[str]:
    if not raw_value:
        return set()
    return {value.strip() for value in raw_value.split(",") if value.strip()}


def upload_progress_files(
    *,
    repo_id: str,
    repo_type: str,
    output_dir: str,
    paths: list[Path],
    token_env: str,
    condition: str,
) -> None:
    token = os.environ.get(token_env)
    if not token:
        print(
            f"[{condition}] WARNING: {token_env} is unset; skipping Hub progress upload",
            flush=True,
        )
        return
    try:
        from huggingface_hub import HfApi
    except Exception as exc:
        print(f"[{condition}] WARNING: cannot import huggingface_hub: {exc}", flush=True)
        return
    api = HfApi(token=token)
    for path in paths:
        if not path.exists():
            continue
        path_in_repo = f"{output_dir.rstrip('/')}/{path.name}"
        print(f"[{condition}] uploading progress artifact {path_in_repo}...", flush=True)
        try:
            api.upload_file(
                path_or_fileobj=str(path),
                path_in_repo=path_in_repo,
                repo_id=repo_id,
                repo_type=repo_type,
                commit_message=f"Upload SkillRouter neural progress {condition}",
            )
            print(f"[{condition}] uploaded {path_in_repo}", flush=True)
        except Exception as exc:
            print(
                f"[{condition}] WARNING: Hub upload failed nonfatally for {path_in_repo}: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )


def download_hub_artifacts(
    *,
    repo_id: str,
    repo_type: str,
    output_dir: str,
    local_output_dir: Path,
    output_prefix: str,
    token_env: str,
) -> None:
    token = os.environ.get(token_env)
    if not token or not repo_id or not output_dir:
        return
    try:
        from huggingface_hub import HfApi, hf_hub_download
    except Exception as exc:
        print(f"[resume] WARNING: cannot import huggingface_hub for download: {exc}", flush=True)
        return
    local_output_dir.mkdir(parents=True, exist_ok=True)
    api = HfApi(token=token)
    remote_prefix = output_dir.rstrip("/") + "/"
    try:
        files = api.list_repo_files(repo_id=repo_id, repo_type=repo_type)
    except Exception as exc:
        print(f"[resume] WARNING: cannot list Hub artifacts: {type(exc).__name__}: {exc}", flush=True)
        return

    downloaded = 0
    for path_in_repo in files:
        if not path_in_repo.startswith(remote_prefix):
            continue
        name = Path(path_in_repo).name
        if not name.startswith(output_prefix):
            continue
        local_path = local_output_dir / name
        if local_path.exists():
            continue
        try:
            cached_path = hf_hub_download(
                repo_id=repo_id,
                filename=path_in_repo,
                repo_type=repo_type,
                token=token,
            )
            shutil.copyfile(cached_path, local_path)
            downloaded += 1
            print(f"[resume] downloaded {path_in_repo} -> {local_path}", flush=True)
        except Exception as exc:
            print(
                f"[resume] WARNING: cannot download {path_in_repo}: {type(exc).__name__}: {exc}",
                flush=True,
            )
    print(f"[resume] downloaded {downloaded} matching Hub artifacts", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run external SkillRouter-Eval-Core matrix with released SkillRouter models.")
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--derived-dir", type=Path, default=DERIVED_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--tiers", default="easy,hard")
    parser.add_argument("--representations", default="I1,FULL,I3C")
    parser.add_argument("--modes", default="embedding,rerank")
    parser.add_argument("--ranking-limit", type=int, default=50)
    parser.add_argument("--cutoffs", default="5,10,20,50")
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--embedding-model", default="pipizhao/SkillRouter-Embedding-0.6B")
    parser.add_argument("--reranker-model", default="pipizhao/SkillRouter-Reranker-0.6B")
    parser.add_argument("--embedding-batch-size", type=int, default=8)
    parser.add_argument("--embedding-max-length", type=int, default=4096)
    parser.add_argument("--reranker-max-length", type=int, default=4096)
    parser.add_argument("--cache-dir", type=Path, default=Path("skill_benchmark/runtime/provider_cache"))
    parser.add_argument("--dotenv", type=Path, default=Path(".env"))
    parser.add_argument("--device", choices=["auto", "cpu", "mps", "cuda"], default="auto")
    parser.add_argument("--output-prefix", default="skillrouter_eval_core_skillrouter_neural_i3c_v2")
    parser.add_argument("--max-tasks", type=int)
    parser.add_argument("--max-docs", type=int)
    parser.add_argument("--quiet-progress", action="store_true")
    parser.add_argument("--skip-conditions", default="")
    parser.add_argument("--hub-repo-id", default="")
    parser.add_argument("--hub-repo-type", default="dataset")
    parser.add_argument("--hub-output-dir", default="")
    parser.add_argument("--hub-token-env", default="HF_TOKEN")
    parser.add_argument("--upload-each-condition", action="store_true")
    parser.add_argument("--download-hub-artifacts", action="store_true")
    parser.add_argument("--resume-completed", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--doc-embedding-shard-size", type=int, default=0)
    parser.add_argument("--upload-doc-embedding-shards", action="store_true")
    args = parser.parse_args()

    load_dotenv(args.dotenv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.download_hub_artifacts:
        download_hub_artifacts(
            repo_id=args.hub_repo_id,
            repo_type=args.hub_repo_type,
            output_dir=args.hub_output_dir,
            local_output_dir=args.output_dir,
            output_prefix=args.output_prefix,
            token_env=args.hub_token_env,
        )
    device = select_device() if args.device == "auto" else args.device
    tasks = load_scored_tasks(args.derived_dir)
    if args.max_tasks:
        tasks = tasks[: args.max_tasks]
    relevance = load_relevance(args.raw_dir)
    hard_only_path = args.derived_dir / "hard_only_skill_ids.txt"
    hard_only_ids = set(hard_only_path.read_text(encoding="utf-8").split()) if hard_only_path.exists() else set()
    cutoffs = [int(value) for value in args.cutoffs.split(",") if value.strip()]
    tiers = [value.strip().lower() for value in args.tiers.split(",") if value.strip()]
    representations = [value.strip().upper() for value in args.representations.split(",") if value.strip()]
    modes = [value.strip().lower() for value in args.modes.split(",") if value.strip()]
    skip_conditions = parse_condition_set(args.skip_conditions)
    if skip_conditions:
        print(f"Skipping completed conditions: {', '.join(sorted(skip_conditions))}", flush=True)

    embedder = SkillRouterEmbedder(
        model_id=args.embedding_model,
        cache_dir=args.cache_dir,
        device=device,
        max_length=args.embedding_max_length,
        token=None,
        quiet=args.quiet_progress,
    )
    reranker = None
    if "rerank" in modes:
        reranker = SkillRouterReranker(
            model_id=args.reranker_model,
            cache_dir=args.cache_dir,
            device=device,
            max_length=args.reranker_max_length,
            token=None,
            quiet=args.quiet_progress,
        )

    report: dict[str, Any] = {
        "source": "pipizhao/SkillRouter-Eval-Core",
        "embedding_model": args.embedding_model,
        "reranker_model": args.reranker_model if "rerank" in modes else "none",
        "device": device,
        "task_count": len(tasks),
        "ranking_limit": args.ranking_limit,
        "rerank_candidates": args.rerank_candidates,
        "cutoffs": cutoffs,
        "summary": [],
        "results": {},
        "failed_conditions": [],
    }

    completed_conditions: set[str] = set()
    json_path = args.output_dir / f"{args.output_prefix}.json"
    if args.resume_completed and json_path.exists():
        try:
            existing_report = json.loads(json_path.read_text(encoding="utf-8"))
            if isinstance(existing_report.get("summary"), list):
                report["summary"] = existing_report["summary"]
            if isinstance(existing_report.get("results"), dict):
                report["results"] = existing_report["results"]
                completed_conditions = set(report["results"])
            if isinstance(existing_report.get("failed_conditions"), list):
                report["failed_conditions"] = existing_report["failed_conditions"]
            print(
                f"Resume loaded {len(completed_conditions)} completed conditions from {json_path}",
                flush=True,
            )
        except Exception:
            print(f"WARNING: could not resume from {json_path}", flush=True)
            traceback.print_exc()

    for tier in tiers:
        for representation in representations:
            for mode in modes:
                key = condition_key(tier, representation, mode)
                if key in skip_conditions:
                    print(f"SKIP {key}: already recovered from previous run", flush=True)
                    continue
                if key in completed_conditions:
                    print(f"SKIP {key}: completed in resumed output report", flush=True)
                    continue
                print(f"\n=== START {key} ===", flush=True)
                try:
                    rows, summary = run_condition(
                        tier=tier,
                        representation=representation,
                        mode=mode,
                        tasks=tasks,
                        relevance=relevance,
                        raw_dir=args.raw_dir,
                        derived_dir=args.derived_dir,
                        ranking_limit=args.ranking_limit,
                        cutoffs=cutoffs,
                        hard_only_ids=hard_only_ids,
                        embedder=embedder,
                        reranker=reranker,
                        embedding_batch_size=args.embedding_batch_size,
                        embedding_model=args.embedding_model,
                        embedding_max_length=args.embedding_max_length,
                        rerank_candidates=args.rerank_candidates,
                        max_docs=args.max_docs,
                        output_dir=args.output_dir,
                        output_prefix=args.output_prefix,
                        doc_embedding_shard_size=args.doc_embedding_shard_size,
                        hub_repo_id=args.hub_repo_id,
                        hub_repo_type=args.hub_repo_type,
                        hub_output_dir=args.hub_output_dir,
                        hub_token_env=args.hub_token_env,
                        upload_doc_embedding_shards=args.upload_doc_embedding_shards,
                    )
                except Exception as exc:
                    report["failed_conditions"].append(key)
                    failure_path = args.output_dir / f"{args.output_prefix}_{key}_failure.json"
                    failure_payload = {
                        "condition": key,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                    failure_path.write_text(json.dumps(failure_payload, indent=2), encoding="utf-8")
                    print(
                        f"FAILED_CONDITION_JSON {json.dumps(failure_payload, sort_keys=True)}",
                        flush=True,
                    )
                    traceback.print_exc()
                    if args.upload_each_condition and args.hub_repo_id and args.hub_output_dir:
                        upload_progress_files(
                            repo_id=args.hub_repo_id,
                            repo_type=args.hub_repo_type,
                            output_dir=args.hub_output_dir,
                            paths=[failure_path],
                            token_env=args.hub_token_env,
                            condition=key,
                        )
                    if args.continue_on_error:
                        continue
                    raise
                report["summary"].append(summary)
                report["results"][key] = rows
                json_path = args.output_dir / f"{args.output_prefix}.json"
                md_path = args.output_dir / f"{args.output_prefix}.md"
                json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
                md_path.write_text(render_markdown(report), encoding="utf-8")
                progress_path = args.output_dir / f"{args.output_prefix}_{key}_progress.json"
                progress_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
                print(
                    f"{key}: Hit@1={summary['hit_at_1']:.1%} "
                    f"MRR@10={summary['mrr_at_10']:.3f} "
                    f"R@20={summary['recall']['20']:.1%} "
                    f"FullCov@20={summary['full_coverage']['20']:.1%} "
                    f"query_total_ms={summary['query_total_elapsed_ms']:.1f}",
                    flush=True,
                )
                print("RESULT_JSON " + json.dumps(summary, sort_keys=True), flush=True)
                if args.upload_each_condition and args.hub_repo_id and args.hub_output_dir:
                    upload_progress_files(
                        repo_id=args.hub_repo_id,
                        repo_type=args.hub_repo_type,
                        output_dir=args.hub_output_dir,
                        paths=[md_path, json_path, progress_path],
                        token_env=args.hub_token_env,
                        condition=key,
                    )
                print(f"=== DONE {key} ===\n", flush=True)

    json_path = args.output_dir / f"{args.output_prefix}.json"
    md_path = args.output_dir / f"{args.output_prefix}.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {md_path}", flush=True)
    print(f"Wrote {json_path}", flush=True)
    compact = {
        "output_prefix": args.output_prefix,
        "failed_conditions": report.get("failed_conditions", []),
        "summary": report.get("summary", []),
    }
    print("FINAL_COMPACT_SUMMARY_JSON " + json.dumps(compact, sort_keys=True), flush=True)
    if args.hub_repo_id and args.hub_output_dir:
        upload_progress_files(
            repo_id=args.hub_repo_id,
            repo_type=args.hub_repo_type,
            output_dir=args.hub_output_dir,
            paths=[md_path, json_path],
            token_env=args.hub_token_env,
            condition="final",
        )
    if report.get("failed_conditions"):
        raise SystemExit(f"Failed conditions: {report['failed_conditions']}")


if __name__ == "__main__":
    main()
