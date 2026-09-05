#!/usr/bin/env python3
# /// script
# dependencies = [
#   "huggingface-hub",
#   "transformers",
#   "torch",
#   "accelerate",
#   "safetensors",
#   "scikit-learn",
#   "rank-bm25",
#   "numpy",
# ]
# ///

from __future__ import annotations

import gzip
import hashlib
import json
import os
import shutil
import sys
import tarfile
import time
import traceback
from pathlib import Path
from typing import Any

import torch
from huggingface_hub import HfApi, hf_hub_download, whoami


SNAPSHOT_REPO_ID = "baechuer1/honour-thesis-skillrouter-benchmark-snapshot"
OUTPUT_REPO_ID = "baechuer1/honour-thesis-skillrouter-checkpoints"
UPSTREAM_REPO_ID = "pipizhao/SkillRouter-Eval-Core"
SNAPSHOT_NAME = "skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz"
RUN_ID = "skillrouter_eval_core_i2_fullcontext_checkpointed_2026_06_22_v2"
HUB_OUTPUT_DIR = f"outputs/{RUN_ID}"
OUT_PREFIX = "skillrouter_eval_core_skillrouter_neural_i2_fullcontext_checkpointed_2026_06_22_v2"
WORK_DIR = Path("/tmp/skillrouter_i2_fullcontext_checkpointed_2026_06_22_v2")

ROOT = Path("skill_benchmark/external/skillrouter_eval_core")
RAW_DIR = ROOT / "raw"
DERIVED_DIR = ROOT / "derived"
OUTPUT_DIR = ROOT / "outputs"

EMBEDDING_MODEL = "pipizhao/SkillRouter-Embedding-0.6B"
RERANKER_MODEL = "pipizhao/SkillRouter-Reranker-0.6B"
EMBEDDING_MAX_LENGTH = 32768
RERANKER_MAX_LENGTH = 40960
RERANK_CANDIDATES = 20
RANKING_LIMIT = 50
CUTOFFS = [5, 10, 20, 50]
SHARD_SIZE = 1000
EMBEDDING_BATCH_SIZE = 1


def log(message: str) -> None:
    print(message, flush=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def pct(value: float) -> str:
    return f"{value:.1%}"


def iter_jsonl_gz(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def iter_raw_tier_rows(tier: str):
    for path in sorted((RAW_DIR / tier).glob("*.jsonl.gz")):
        yield from iter_jsonl_gz(path)


def i2_doc(row: dict[str, Any]) -> str:
    name = str(row.get("name") or row.get("skill_id") or "")
    description = str(row.get("description") or "")
    body = str(row.get("body") or "")
    return f"{name} | {description} | {body}".strip()


def load_i2_docs(tier: str, approximate_tokens) -> tuple[list[str], list[str], list[str], dict[str, Any]]:
    skill_ids: list[str] = []
    names: list[str] = []
    docs: list[str] = []
    token_total = 0
    max_doc_tokens = 0
    max_doc_skill_id = ""
    for row in iter_raw_tier_rows(tier):
        skill_id = str(row["skill_id"])
        doc = i2_doc(row)
        tokens = approximate_tokens(doc)
        token_total += tokens
        if tokens > max_doc_tokens:
            max_doc_tokens = tokens
            max_doc_skill_id = skill_id
        skill_ids.append(skill_id)
        names.append(str(row.get("name") or skill_id))
        docs.append(doc)
    stats = {
        "selector_visible_tokens_approx": token_total,
        "max_doc_tokens_approx": max_doc_tokens,
        "max_doc_tokens_skill_id": max_doc_skill_id,
    }
    return skill_ids, names, docs, stats


def doc_cache_prefix(tier: str) -> str:
    return f"{OUT_PREFIX}_docemb_{tier}_I2"


def shard_path(tier: str, start: int, end: int) -> Path:
    return OUTPUT_DIR / f"{doc_cache_prefix(tier)}_shard_{start:06d}_{end:06d}.pt"


def manifest_path(tier: str) -> Path:
    return OUTPUT_DIR / f"{doc_cache_prefix(tier)}_manifest.json"


def valid_shard(
    path: Path,
    *,
    expected_skill_ids: list[str],
    expected_hashes: list[str],
) -> tuple[torch.Tensor, dict[str, Any]] | None:
    if not path.exists():
        return None
    try:
        payload = torch.load(path, map_location="cpu")
    except Exception as exc:
        log(f"[doc-cache] unreadable shard {path.name}: {type(exc).__name__}: {exc}")
        return None
    if not isinstance(payload, dict):
        return None
    checks = [
        payload.get("cache_version") == 1,
        payload.get("skill_ids") == expected_skill_ids,
        payload.get("text_hashes") == expected_hashes,
        payload.get("embedding_model") == EMBEDDING_MODEL,
        int(payload.get("embedding_max_length", -1)) == EMBEDDING_MAX_LENGTH,
    ]
    embeddings = payload.get("embeddings")
    if not all(checks) or not isinstance(embeddings, torch.Tensor):
        log(f"[doc-cache] invalid or stale shard {path.name}; recomputing")
        return None
    if embeddings.shape[0] != len(expected_skill_ids):
        log(f"[doc-cache] wrong row count in {path.name}; recomputing")
        return None
    return embeddings.float(), payload


def write_manifest(
    tier: str,
    skill_ids: list[str],
    text_hashes: list[str],
    shard_records: list[dict[str, Any]],
) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = manifest_path(tier)
    payload = {
        "cache_version": 1,
        "run_id": RUN_ID,
        "tier": tier,
        "representation": "I2",
        "representation_policy": "name | description | body from raw SkillRouter-Eval-Core rows",
        "embedding_model": EMBEDDING_MODEL,
        "embedding_max_length": EMBEDDING_MAX_LENGTH,
        "skill_count": len(skill_ids),
        "skill_ids_hash": sha256_text("\n".join(skill_ids)),
        "text_hashes_hash": sha256_text("\n".join(text_hashes)),
        "shard_size": SHARD_SIZE,
        "complete_shard_count": len(shard_records),
        "shards": shard_records,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def upload_files(api: HfApi, paths: list[Path], condition: str) -> None:
    for path in paths:
        if not path.exists():
            continue
        path_in_repo = f"{HUB_OUTPUT_DIR}/{path.name}"
        for attempt in range(1, 4):
            try:
                log(f"UPLOAD_START {condition} {path_in_repo} attempt={attempt}")
                api.upload_file(
                    path_or_fileobj=str(path),
                    path_in_repo=path_in_repo,
                    repo_id=OUTPUT_REPO_ID,
                    repo_type="dataset",
                    commit_message=f"Upload checkpointed SkillRouter I2 artifact {condition}",
                )
                log(f"UPLOAD_DONE {condition} {path_in_repo}")
                break
            except Exception as exc:
                log(f"UPLOAD_FAILED_NONFATAL {condition} {path_in_repo}: {type(exc).__name__}: {exc}")
                if attempt < 3:
                    time.sleep(10 * attempt)


def download_existing_artifacts(api: HfApi, token: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    remote_prefix = f"{HUB_OUTPUT_DIR}/"
    try:
        files = api.list_repo_files(repo_id=OUTPUT_REPO_ID, repo_type="dataset")
    except Exception as exc:
        log(f"[resume] cannot list Hub artifacts: {type(exc).__name__}: {exc}")
        return
    downloaded = 0
    for path_in_repo in files:
        name = Path(path_in_repo).name
        if not path_in_repo.startswith(remote_prefix) or not name.startswith(OUT_PREFIX):
            continue
        local_path = OUTPUT_DIR / name
        if local_path.exists():
            continue
        try:
            cached = hf_hub_download(
                repo_id=OUTPUT_REPO_ID,
                filename=path_in_repo,
                repo_type="dataset",
                token=token,
            )
            shutil.copyfile(cached, local_path)
            downloaded += 1
            log(f"[resume] downloaded {path_in_repo}")
        except Exception as exc:
            log(f"[resume] cannot download {path_in_repo}: {type(exc).__name__}: {exc}")
    log(f"[resume] downloaded {downloaded} existing checkpoint artifacts")


def load_or_compute_doc_embeddings(
    *,
    tier: str,
    skill_ids: list[str],
    docs: list[str],
    embedder,
    api: HfApi,
) -> tuple[torch.Tensor, dict[str, Any]]:
    text_hashes = [sha256_text(doc) for doc in docs]
    tensors: list[torch.Tensor] = []
    shard_records: list[dict[str, Any]] = []
    compute_ms = 0.0
    load_ms = 0.0
    hits = 0
    misses = 0
    runtime_start = time.perf_counter()
    total_shards = (len(docs) + SHARD_SIZE - 1) // SHARD_SIZE

    for shard_index, start in enumerate(range(0, len(docs), SHARD_SIZE), start=1):
        end = min(start + SHARD_SIZE, len(docs))
        path = shard_path(tier, start, end)
        expected_skill_ids = skill_ids[start:end]
        expected_hashes = text_hashes[start:end]
        load_start = time.perf_counter()
        loaded = valid_shard(path, expected_skill_ids=expected_skill_ids, expected_hashes=expected_hashes)
        if loaded is not None:
            embeddings, payload = loaded
            shard_compute_ms = float(payload.get("compute_elapsed_ms", 0.0))
            compute_ms += shard_compute_ms
            load_ms += (time.perf_counter() - load_start) * 1000
            hits += 1
            log(
                f"[{tier}_I2_doc_cache] shard {shard_index}/{total_shards} "
                f"{start}-{end} loaded; original_compute_ms={shard_compute_ms:.1f}"
            )
        else:
            misses += 1
            log(f"[{tier}_I2_doc_cache] shard {shard_index}/{total_shards} {start}-{end} embedding start")
            shard_start = time.perf_counter()
            embeddings = embedder.encode(docs[start:end], EMBEDDING_BATCH_SIZE)
            shard_compute_ms = (time.perf_counter() - shard_start) * 1000
            compute_ms += shard_compute_ms
            payload = {
                "cache_version": 1,
                "run_id": RUN_ID,
                "tier": tier,
                "representation": "I2",
                "embedding_model": EMBEDDING_MODEL,
                "embedding_max_length": EMBEDDING_MAX_LENGTH,
                "start": start,
                "end": end,
                "skill_ids": expected_skill_ids,
                "text_hashes": expected_hashes,
                "compute_elapsed_ms": round(shard_compute_ms, 2),
                "embeddings": embeddings.cpu(),
            }
            torch.save(payload, path)
            log(
                f"[{tier}_I2_doc_cache] shard {shard_index}/{total_shards} "
                f"{start}-{end} saved {path.name}; compute_ms={shard_compute_ms:.1f}"
            )
        tensors.append(embeddings.cpu())
        shard_records.append(
            {
                "path": path.name,
                "start": start,
                "end": end,
                "row_count": end - start,
                "text_hashes_hash": sha256_text("\n".join(expected_hashes)),
                "compute_elapsed_ms": round(shard_compute_ms, 2),
            }
        )
        current_manifest = write_manifest(tier, skill_ids, text_hashes, shard_records)
        if loaded is None:
            upload_files(api, [path, current_manifest], f"{tier}_I2_doc_cache")

    runtime_ms = (time.perf_counter() - runtime_start) * 1000
    return torch.cat(tensors, dim=0), {
        "doc_embedding_elapsed_ms": compute_ms,
        "doc_embedding_compute_elapsed_ms": compute_ms,
        "doc_embedding_runtime_elapsed_ms": runtime_ms,
        "doc_embedding_load_elapsed_ms": load_ms,
        "doc_embedding_cache_shards_hit": hits,
        "doc_embedding_cache_shards_missed": misses,
        "doc_embedding_shard_size": SHARD_SIZE,
    }


def evaluate_ranking(ranked_ids: list[str], relevance_row: dict[str, Any], cutoffs: list[int]) -> dict[str, Any]:
    from run_skillrouter_eval_core_fts_ablation import dcg

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
    first_rank = next((index + 1 for index, skill_id in enumerate(ranked_ids[:10]) if skill_id in gold_ids), None)
    recall = {str(k): len(gold_ids & set(ranked_ids[:k])) / len(gold_ids) for k in cutoffs}
    full_coverage = {str(k): float(gold_ids.issubset(set(ranked_ids[:k]))) for k in cutoffs}
    grades = [graded_relevance.get(skill_id, 0.0) for skill_id in ranked_ids[:10]]
    ideal_grades = sorted(graded_relevance.values(), reverse=True)[:10]
    ideal = dcg(ideal_grades)
    return {
        "hit_at_1": float(bool(ranked_ids and ranked_ids[0] in gold_ids)),
        "mrr_at_10": 1.0 / first_rank if first_rank else 0.0,
        "recall": recall,
        "full_coverage": full_coverage,
        "ndcg_at_10": dcg(grades) / ideal if ideal else 0.0,
    }


def topk_from_scores(skill_ids: list[str], names: list[str], scores: torch.Tensor, limit: int) -> list[list[dict[str, Any]]]:
    limit = min(limit, len(skill_ids))
    values, indices = torch.topk(scores, k=limit, dim=1, largest=True, sorted=True)
    rankings: list[list[dict[str, Any]]] = []
    for row_values, row_indices in zip(values.tolist(), indices.tolist()):
        rankings.append(
            [
                {"skill_id": skill_ids[index], "name": names[index], "score": round(float(score), 6)}
                for score, index in zip(row_values, row_indices)
            ]
        )
    return rankings


def condition_key(tier: str, mode: str) -> str:
    return f"{tier}_I2_{mode}"


def compact_paths() -> tuple[Path, Path, Path]:
    return (
        OUTPUT_DIR / f"{OUT_PREFIX}.json",
        OUTPUT_DIR / f"{OUT_PREFIX}.md",
        OUTPUT_DIR / f"{OUT_PREFIX}_compact_summary.json",
    )


def load_completed_rows() -> list[dict[str, Any]]:
    _json_path, _md_path, compact_path = compact_paths()
    if not compact_path.exists():
        return []
    try:
        payload = json.loads(compact_path.read_text(encoding="utf-8"))
        rows = payload.get("summary") or []
        if isinstance(rows, list):
            log(f"[resume] loaded {len(rows)} completed summary rows from {compact_path.name}")
            return [dict(row) for row in rows if isinstance(row, dict)]
    except Exception:
        log("[resume] failed to load compact summary")
        traceback.print_exc()
    return []


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# SkillRouter-Eval-Core I2 Full-Context Checkpointed Neural Run",
        "",
        "Representation policy: I2 is the raw full skill body serialized as `name | description | body`.",
        f"Embedding max length: {EMBEDDING_MAX_LENGTH}. Reranker max length: {RERANKER_MAX_LENGTH}. Rerank candidates: top-{RERANK_CANDIDATES}.",
        "",
        "| Condition | Hit@1 | MRR@10 | Recall@20 | FullCov@20 | Tokens | Doc compute ms | Doc runtime ms | Query total ms | Cache hit/miss |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        recall20 = row.get("recall", {}).get("20", 0.0) if isinstance(row.get("recall"), dict) else 0.0
        full20 = row.get("full_coverage", {}).get("20", 0.0) if isinstance(row.get("full_coverage"), dict) else 0.0
        lines.append(
            "| {condition} | {hit} | {mrr:.3f} | {recall} | {full} | {tokens} | {doc_compute:.1f} | {doc_runtime:.1f} | {query:.1f} | {hits}/{misses} |".format(
                condition=row.get("condition", ""),
                hit=pct(float(row.get("hit_at_1", 0.0))),
                mrr=float(row.get("mrr_at_10", 0.0)),
                recall=pct(float(recall20)),
                full=pct(float(full20)),
                tokens=row.get("selector_visible_tokens_approx", ""),
                doc_compute=float(row.get("doc_embedding_compute_elapsed_ms", row.get("doc_embedding_elapsed_ms", 0.0))),
                doc_runtime=float(row.get("doc_embedding_runtime_elapsed_ms", 0.0)),
                query=float(row.get("query_total_elapsed_ms", 0.0)),
                hits=row.get("doc_embedding_cache_shards_hit", 0),
                misses=row.get("doc_embedding_cache_shards_missed", 0),
            )
        )
    return "\n".join(lines) + "\n"


def write_outputs(rows_by_condition: dict[str, dict[str, Any]]) -> list[Path]:
    rows = [rows_by_condition[key] for key in sorted(rows_by_condition)]
    json_path, md_path, compact_path = compact_paths()
    payload = {
        "source": "pipizhao/SkillRouter-Eval-Core",
        "run_id": RUN_ID,
        "representation_policy": "I2 full skill body from raw rows: name | description | body",
        "embedding_model": EMBEDDING_MODEL,
        "reranker_model": RERANKER_MODEL,
        "embedding_max_length": EMBEDDING_MAX_LENGTH,
        "reranker_max_length": RERANKER_MAX_LENGTH,
        "rerank_candidates": RERANK_CANDIDATES,
        "ranking_limit": RANKING_LIMIT,
        "summary": rows,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    compact_path.write_text(json.dumps({"run_id": RUN_ID, "summary": rows}, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(rows), encoding="utf-8")
    log("COMPACT_SUMMARY_JSON " + json.dumps({"run_id": RUN_ID, "summary": rows}, sort_keys=True))
    return [json_path, md_path, compact_path]


def summarize_rows(
    *,
    rows: list[dict[str, Any]],
    tier: str,
    mode: str,
    doc_stats: dict[str, Any],
    doc_load_stats: dict[str, Any],
    query_embedding_ms: float,
    retrieval_ms: float,
    rerank_ms: float,
    elapsed_wall_sec: float,
) -> dict[str, Any]:
    from run_skillrouter_eval_core_fts_ablation import summarize_task_rows

    summary = summarize_task_rows(rows, CUTOFFS)
    query_total_ms = query_embedding_ms + retrieval_ms + rerank_ms
    summary.update(
        {
            "condition": condition_key(tier, mode),
            "tier": tier,
            "representation": "I2",
            "mode": mode,
            "retriever": "SkillRouter embedding",
            "reranker": "SkillRouter reranker" if mode == "rerank" else "none",
            "ranking_limit": RANKING_LIMIT,
            "rerank_candidates": RERANK_CANDIDATES if mode == "rerank" else 0,
            "skill_count": doc_load_stats["skill_count"],
            "selector_visible_tokens_approx": doc_load_stats["selector_visible_tokens_approx"],
            "max_doc_tokens_approx": doc_load_stats["max_doc_tokens_approx"],
            "max_doc_tokens_skill_id": doc_load_stats["max_doc_tokens_skill_id"],
            "doc_embedding_elapsed_ms": round(float(doc_stats["doc_embedding_elapsed_ms"]), 2),
            "doc_embedding_compute_elapsed_ms": round(float(doc_stats["doc_embedding_compute_elapsed_ms"]), 2),
            "doc_embedding_runtime_elapsed_ms": round(float(doc_stats["doc_embedding_runtime_elapsed_ms"]), 2),
            "doc_embedding_load_elapsed_ms": round(float(doc_stats["doc_embedding_load_elapsed_ms"]), 2),
            "doc_embedding_cache_shards_hit": doc_stats["doc_embedding_cache_shards_hit"],
            "doc_embedding_cache_shards_missed": doc_stats["doc_embedding_cache_shards_missed"],
            "doc_embedding_shard_size": doc_stats["doc_embedding_shard_size"],
            "query_embedding_elapsed_ms": round(query_embedding_ms, 2),
            "retrieval_elapsed_ms": round(retrieval_ms, 2),
            "rerank_elapsed_ms": round(rerank_ms, 2),
            "query_total_elapsed_ms": round(query_total_ms, 2),
            "elapsed_sec_wall": round(elapsed_wall_sec, 2),
        }
    )
    return summary


def build_rows(
    *,
    tasks: list[dict[str, Any]],
    relevance: dict[str, Any],
    hard_only_ids: set[str],
    ranking_lists: list[list[dict[str, Any]]],
    mode: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task, ranking in zip(tasks, ranking_lists):
        task_id = task["task_id"]
        rel = relevance[task_id]
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
                "top1_hard_only": bool(ranking and ranking[0]["skill_id"] in hard_only_ids),
                "metrics": evaluate_ranking(ranked_ids, rel, CUTOFFS),
                "mode": mode,
            }
        )
    return rows


def run_tier(
    *,
    tier: str,
    tasks: list[dict[str, Any]],
    relevance: dict[str, Any],
    hard_only_ids: set[str],
    rows_by_condition: dict[str, dict[str, Any]],
    embedder,
    reranker_holder: dict[str, Any],
    api: HfApi,
) -> None:
    needs_embedding = condition_key(tier, "embedding") not in rows_by_condition
    needs_rerank = condition_key(tier, "rerank") not in rows_by_condition
    if not needs_embedding and not needs_rerank:
        log(f"[{tier}_I2] both conditions already complete; skipping tier")
        return

    from run_offline_selectors import approximate_tokens
    from run_skillrouter_selectors import QUERY_INSTRUCTION, SkillRouterReranker

    tier_start = time.perf_counter()
    log(f"[{tier}_I2] loading raw full-body I2 documents")
    skill_ids, names, docs, doc_load_stats = load_i2_docs(tier, approximate_tokens)
    doc_load_stats["skill_count"] = len(skill_ids)
    log(
        f"[{tier}_I2] loaded {len(skill_ids)} docs; "
        f"approx_tokens={doc_load_stats['selector_visible_tokens_approx']} "
        f"max_doc_tokens={doc_load_stats['max_doc_tokens_approx']} "
        f"max_doc_skill={doc_load_stats['max_doc_tokens_skill_id']}"
    )
    doc_by_skill_id = dict(zip(skill_ids, docs))

    doc_embeddings, doc_stats = load_or_compute_doc_embeddings(
        tier=tier,
        skill_ids=skill_ids,
        docs=docs,
        embedder=embedder,
        api=api,
    )
    log(
        f"[{tier}_I2] doc embeddings ready; "
        f"compute_ms={doc_stats['doc_embedding_compute_elapsed_ms']:.1f} "
        f"runtime_ms={doc_stats['doc_embedding_runtime_elapsed_ms']:.1f} "
        f"cache_hit/miss={doc_stats['doc_embedding_cache_shards_hit']}/{doc_stats['doc_embedding_cache_shards_missed']}"
    )

    query_texts = [QUERY_INSTRUCTION + str(task["instruction_text"]) for task in tasks]
    query_start = time.perf_counter()
    log(f"[{tier}_I2] embedding {len(query_texts)} queries")
    query_embeddings = embedder.encode(query_texts, EMBEDDING_BATCH_SIZE)
    query_embedding_ms = (time.perf_counter() - query_start) * 1000

    retrieval_start = time.perf_counter()
    log(f"[{tier}_I2] computing first-stage dense scores")
    scores = query_embeddings @ doc_embeddings.T
    first_stage = topk_from_scores(
        skill_ids,
        names,
        scores,
        limit=max(RANKING_LIMIT, RERANK_CANDIDATES),
    )
    retrieval_ms = (time.perf_counter() - retrieval_start) * 1000

    if needs_embedding:
        rows = build_rows(
            tasks=tasks,
            relevance=relevance,
            hard_only_ids=hard_only_ids,
            ranking_lists=[ranking[:RANKING_LIMIT] for ranking in first_stage],
            mode="embedding",
        )
        summary = summarize_rows(
            rows=rows,
            tier=tier,
            mode="embedding",
            doc_stats=doc_stats,
            doc_load_stats=doc_load_stats,
            query_embedding_ms=query_embedding_ms,
            retrieval_ms=retrieval_ms,
            rerank_ms=0.0,
            elapsed_wall_sec=time.perf_counter() - tier_start,
        )
        rows_by_condition[condition_key(tier, "embedding")] = summary
        progress = OUTPUT_DIR / f"{OUT_PREFIX}_{condition_key(tier, 'embedding')}_rows.json"
        progress.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        paths = write_outputs(rows_by_condition) + [progress]
        upload_files(api, paths, condition_key(tier, "embedding"))
        log("RESULT_JSON " + json.dumps(summary, sort_keys=True))

    if needs_rerank:
        if reranker_holder.get("model") is None:
            log(f"[{tier}_I2_rerank] loading reranker")
            reranker_holder["model"] = SkillRouterReranker(
                model_id=RERANKER_MODEL,
                cache_dir=Path("skill_benchmark/runtime/provider_cache_i2_fullcontext_checkpointed_2026_06_22_v2"),
                device="cuda",
                max_length=RERANKER_MAX_LENGTH,
                token=os.environ.get("HF_TOKEN"),
                quiet=False,
            )
        reranker = reranker_holder["model"]
        rerank_start_all = time.perf_counter()
        reranked_lists: list[list[dict[str, Any]]] = []
        for index, (task, candidates) in enumerate(zip(tasks, first_stage), start=1):
            if index == 1 or index % 10 == 0 or index == len(tasks):
                log(f"[{tier}_I2_rerank] reranking task {index}/{len(tasks)} top-{RERANK_CANDIDATES}")
            candidate_rows = candidates[:RERANK_CANDIDATES]
            candidate_docs = [doc_by_skill_id[row["skill_id"]] for row in candidate_rows]
            scores = reranker.score_many(str(task["instruction_text"]), candidate_docs)
            reranked = [
                {
                    "skill_id": row["skill_id"],
                    "name": row["name"],
                    "score": round(float(score), 6),
                    "first_stage_score": row["score"],
                }
                for row, score in zip(candidate_rows, scores)
            ]
            reranked.sort(key=lambda item: (-float(item["score"]), item["skill_id"]))
            reranked_lists.append(reranked[:RANKING_LIMIT])
        rerank_ms = (time.perf_counter() - rerank_start_all) * 1000
        rows = build_rows(
            tasks=tasks,
            relevance=relevance,
            hard_only_ids=hard_only_ids,
            ranking_lists=reranked_lists,
            mode="rerank",
        )
        summary = summarize_rows(
            rows=rows,
            tier=tier,
            mode="rerank",
            doc_stats=doc_stats,
            doc_load_stats=doc_load_stats,
            query_embedding_ms=query_embedding_ms,
            retrieval_ms=retrieval_ms,
            rerank_ms=rerank_ms,
            elapsed_wall_sec=time.perf_counter() - tier_start,
        )
        rows_by_condition[condition_key(tier, "rerank")] = summary
        progress = OUTPUT_DIR / f"{OUT_PREFIX}_{condition_key(tier, 'rerank')}_rows.json"
        progress.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        paths = write_outputs(rows_by_condition) + [progress]
        upload_files(api, paths, condition_key(tier, "rerank"))
        log("RESULT_JSON " + json.dumps(summary, sort_keys=True))


def extract_snapshot(token: str) -> None:
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    log(f"downloading snapshot {SNAPSHOT_NAME}")
    archive = hf_hub_download(repo_id=SNAPSHOT_REPO_ID, filename=SNAPSHOT_NAME, repo_type="dataset", token=token)
    log(f"extracting snapshot to {WORK_DIR}")
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(WORK_DIR)
    os.chdir(WORK_DIR)
    sys.path.append(str((WORK_DIR / "skill_benchmark/scripts").resolve()))
    log(f"cwd={Path.cwd()}")


def ensure_raw_skillrouter_eval_core(api: HfApi, token: str) -> None:
    if any((RAW_DIR / "easy").glob("*.jsonl.gz")) and any((RAW_DIR / "hard").glob("*.jsonl.gz")):
        log("[raw] snapshot already contains raw easy/hard shards")
        return
    log(f"[raw] downloading raw full-body shards from {UPSTREAM_REPO_ID}")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    files = api.list_repo_files(repo_id=UPSTREAM_REPO_ID, repo_type="dataset")
    wanted = [
        path
        for path in files
        if path in {"tasks.jsonl", "manifest.json", "relevance.json"}
        or path.startswith("easy/")
        or path.startswith("hard/")
    ]
    for index, path_in_repo in enumerate(sorted(wanted), start=1):
        target = RAW_DIR / path_in_repo
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        log(f"[raw] download {index}/{len(wanted)} {path_in_repo}")
        cached = hf_hub_download(
            repo_id=UPSTREAM_REPO_ID,
            filename=path_in_repo,
            repo_type="dataset",
            token=token,
        )
        shutil.copyfile(cached, target)


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is required")
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
    api = HfApi(token=token)
    log(f"whoami={whoami(token=token).get('name')}")
    api.create_repo(repo_id=OUTPUT_REPO_ID, repo_type="dataset", exist_ok=True)
    extract_snapshot(token)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_raw_skillrouter_eval_core(api, token)
    download_existing_artifacts(api, token)

    from run_skillrouter_eval_core_fts_ablation import load_relevance, load_scored_tasks
    from run_skillrouter_selectors import SkillRouterEmbedder

    tasks = load_scored_tasks(DERIVED_DIR)
    relevance = load_relevance(RAW_DIR)
    hard_only_path = DERIVED_DIR / "hard_only_skill_ids.txt"
    hard_only_ids = set(hard_only_path.read_text(encoding="utf-8").split()) if hard_only_path.exists() else set()

    rows_by_condition = {row["condition"]: row for row in load_completed_rows() if row.get("condition")}
    log(f"completed conditions from checkpoints: {sorted(rows_by_condition)}")

    log("loading SkillRouter embedder")
    embedder = SkillRouterEmbedder(
        model_id=EMBEDDING_MODEL,
        cache_dir=Path("skill_benchmark/runtime/provider_cache_i2_fullcontext_checkpointed_2026_06_22_v2"),
        device="cuda",
        max_length=EMBEDDING_MAX_LENGTH,
        token=token,
        quiet=True,
    )
    reranker_holder: dict[str, Any] = {"model": None}

    failed: list[str] = []
    for tier in ["easy", "hard"]:
        try:
            run_tier(
                tier=tier,
                tasks=tasks,
                relevance=relevance,
                hard_only_ids=hard_only_ids,
                rows_by_condition=rows_by_condition,
                embedder=embedder,
                reranker_holder=reranker_holder,
                api=api,
            )
        except Exception as exc:
            failed.append(tier)
            failure_path = OUTPUT_DIR / f"{OUT_PREFIX}_{tier}_failure.json"
            failure_path.write_text(
                json.dumps({"tier": tier, "error_type": type(exc).__name__, "error": str(exc)}, indent=2),
                encoding="utf-8",
            )
            upload_files(api, [failure_path, *write_outputs(rows_by_condition)], f"{tier}_failure")
            log(f"FAILED_TIER_JSON {json.dumps({'tier': tier, 'error_type': type(exc).__name__, 'error': str(exc)}, sort_keys=True)}")
            traceback.print_exc()
            break

    final_paths = write_outputs(rows_by_condition)
    upload_files(api, final_paths, "final")
    final_payload = {
        "run_id": RUN_ID,
        "failed_tiers": failed,
        "summary": [rows_by_condition[key] for key in sorted(rows_by_condition)],
    }
    log("FINAL_COMPACT_SUMMARY_JSON " + json.dumps(final_payload, sort_keys=True))
    if failed:
        raise SystemExit(f"Failed tiers: {failed}")
    if len(rows_by_condition) < 4:
        raise SystemExit(f"Missing conditions after run: {sorted(rows_by_condition)}")
    log("ALL_I2_FULL_CONTEXT_CHECKPOINTED_CONDITIONS_COMPLETE")


if __name__ == "__main__":
    main()
