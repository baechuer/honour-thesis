#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from field_aware_matching import (  # noqa: E402
    explain_field_set,
    field_aware_pair_score,
    parse_field_set,
)
from run_offline_selectors import (  # noqa: E402
    TfIdfScorer,
    approximate_tokens,
    bm25_scores,
    build_scale_skill_names,
    docs_for_method,
    evaluate_rows,
    instruction_text,
    load_acceptables,
    load_full_skill_texts,
    load_jsonl,
    load_prompts,
    minmax,
    rank_scores,
)


FIRST_STAGE_METHODS = {
    "bm25_flat": "m1_bm25_flat",
    "tfidf_flat": "m1_tfidf_flat",
    "tfidf_schema": "m3_tfidf_schema",
    "qwen_full": "qwen_full",
    "skillrouter_full": "skillrouter_full",
}

DEFAULT_FIELD_SET_ORDER = [
    "task",
    "task_output",
    "task_output_workflow",
    "core",
    "core_dependency",
    "core_boundary",
    "all",
]


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_prompts_many(raw: str) -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        prompts.extend(load_prompts(part))
    return prompts


def docs_for_first_stage(
    first_stage: str,
    skill_names: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    full_skill_texts: dict[str, str],
) -> list[str]:
    if first_stage == "bm25_flat":
        return docs_for_method("m1_bm25_flat", skill_names, r1, r2, full_skill_texts)
    if first_stage == "tfidf_flat":
        return docs_for_method("m1_tfidf_flat", skill_names, r1, r2, full_skill_texts)
    if first_stage == "tfidf_schema":
        return docs_for_method("m3_tfidf_schema", skill_names, r1, r2, full_skill_texts)
    if first_stage == "qwen_full":
        return [full_skill_texts.get(name) or r2[name]["text"] for name in skill_names]
    if first_stage == "skillrouter_full":
        return [
            f"{name} | {r1[name].get('description', '')} | {full_skill_texts.get(name) or r2[name]['text']}"
            for name in skill_names
        ]
    raise ValueError(f"Unknown first-stage method: {first_stage}")


def qwen_rankings(
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    docs: list[str],
    cache_dir: Path,
    dotenv_path: Path,
    batch_size: int,
    model: str,
    base_url: str,
    timeout: int,
) -> tuple[dict[str, list[tuple[str, float]]], dict[str, Any]]:
    from run_provider_selectors import OpenAICompatibleEmbeddingClient, cosine

    load_dotenv(dotenv_path)
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise SystemExit("Missing DASHSCOPE_API_KEY for --first-stage qwen_full.")
    client = OpenAICompatibleEmbeddingClient(
        provider="qwen",
        base_url=base_url,
        api_key=api_key,
        model=model,
        cache_dir=cache_dir,
        timeout=timeout,
        dimensions=None,
    )
    doc_embeddings = client.embed_many(docs, batch_size)
    rankings: dict[str, list[tuple[str, float]]] = {}
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        query_embedding = client.embed_many([query], 1)[0]
        scores = [cosine(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]
        rankings[prompt["id"]] = rank_scores(skill_names, scores)
    return rankings, {
        "embedding_api_calls": client.api_calls,
        "embedding_cache_hits": client.cache_hits,
        "embedding_tokens_approx": client.tokens_approx,
        "embedding_model": model,
    }


def skillrouter_rankings(
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    docs: list[str],
    cache_dir: Path,
    dotenv_path: Path,
    batch_size: int,
    model: str,
    device: str,
    max_length: int,
    quiet_progress: bool,
) -> tuple[dict[str, list[tuple[str, float]]], dict[str, Any]]:
    from run_skillrouter_selectors import QUERY_INSTRUCTION, SkillRouterEmbedder, load_dotenv as load_sr_dotenv, select_device

    load_sr_dotenv(dotenv_path)
    token = os.environ.get("HF_TOKEN")
    resolved_device = select_device() if device == "auto" else device
    embedder = SkillRouterEmbedder(
        model_id=model,
        cache_dir=cache_dir,
        device=resolved_device,
        max_length=max_length,
        token=token,
        quiet=quiet_progress,
    )
    doc_embeddings = embedder.encode(docs, batch_size)
    rankings: dict[str, list[tuple[str, float]]] = {}
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        query_embedding = embedder.encode([QUERY_INSTRUCTION + query], 1)[0]
        scores = (query_embedding.unsqueeze(0) @ doc_embeddings.T).squeeze(0).tolist()
        rankings[prompt["id"]] = rank_scores(skill_names, [float(score) for score in scores])
    return rankings, {
        "embedding_model": model,
        "embedding_cache_hits": embedder.cache_hits,
        "embedding_items_encoded": embedder.encoded_items,
        "device": resolved_device,
        "embedding_max_length": max_length,
    }


def local_rankings(
    first_stage: str,
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    docs: list[str],
) -> tuple[dict[str, list[tuple[str, float]]], dict[str, Any]]:
    start = time.perf_counter()
    scorer: Any = None
    if first_stage in {"tfidf_flat", "tfidf_schema"}:
        scorer = TfIdfScorer(docs)
    rankings: dict[str, list[tuple[str, float]]] = {}
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        if first_stage == "bm25_flat":
            scores = bm25_scores(query, docs)
        elif first_stage in {"tfidf_flat", "tfidf_schema"}:
            scores = scorer.scores(query)
        else:
            raise ValueError(f"Unsupported local first-stage method: {first_stage}")
        rankings[prompt["id"]] = rank_scores(skill_names, scores)
    return rankings, {"first_stage_elapsed_ms": round((time.perf_counter() - start) * 1000, 2)}


def reciprocal_rank(ranking: list[str], targets: set[str]) -> float:
    for index, skill in enumerate(ranking, start=1):
        if skill in targets:
            return 1 / index
    return 0.0


def compute_decomposition(
    rows: list[dict[str, Any]],
    r1: dict[str, dict[str, Any]],
    acceptable_by_prompt: dict[str, dict[str, set[str]]],
) -> dict[str, Any]:
    total = len(rows)
    candidate_recall = Counter()
    acceptable_candidate_recall = Counter()
    conditional_total = 0
    conditional_top1 = 0
    conditional_accept_top1 = 0
    reranker_loss = 0
    first_stage_top1 = 0
    final_top1 = 0
    non_main_final_top1 = 0
    field_failure = Counter()

    for row in rows:
        gold = row["gold_skill"]
        acceptable = {gold, *acceptable_by_prompt.get(row["prompt_id"], {}).get("acceptable", set())}
        first_stage_ranking = row["first_stage_ranking"]
        final_ranking = [item["skill"] for item in row["ranking"]]
        first_stage_top = first_stage_ranking[0] if first_stage_ranking else None
        final_top = final_ranking[0] if final_ranking else None
        if first_stage_top == gold:
            first_stage_top1 += 1
        if final_top == gold:
            final_top1 += 1
        if final_top and not r1[final_top].get("is_main_evaluated"):
            non_main_final_top1 += 1
        for k in [20, 50, 100]:
            if gold in first_stage_ranking[:k]:
                candidate_recall[k] += 1
            if any(skill in acceptable for skill in first_stage_ranking[:k]):
                acceptable_candidate_recall[k] += 1
        if gold in row["candidate_names"]:
            conditional_total += 1
            if final_top == gold:
                conditional_top1 += 1
            elif final_top in acceptable:
                conditional_accept_top1 += 1
            else:
                reranker_loss += 1
                reason = row.get("failure_guess") or "unknown"
                field_failure[reason] += 1

    pct = lambda value: round(value / total, 4) if total else 0.0
    cond_pct = lambda value: round(value / conditional_total, 4) if conditional_total else 0.0
    return {
        "first_stage_top1_accuracy": pct(first_stage_top1),
        "final_top1_accuracy_check": pct(final_top1),
        "candidate_recall": {f"recall@{k}": pct(candidate_recall[k]) for k in [20, 50, 100]},
        "acceptable_candidate_recall": {
            f"acceptable_recall@{k}": pct(acceptable_candidate_recall[k]) for k in [20, 50, 100]
        },
        "conditional_gold_in_candidate_count": conditional_total,
        "conditional_reranker_top1": cond_pct(conditional_top1),
        "conditional_reranker_acceptable_top1": cond_pct(conditional_top1 + conditional_accept_top1),
        "reranker_loss_count": reranker_loss,
        "reranker_loss_rate_given_gold_in_candidates": cond_pct(reranker_loss),
        "non_main_final_top1_rate": pct(non_main_final_top1),
        "failure_guess_counts": dict(field_failure.most_common()),
    }


def guess_failure(row: dict[str, Any]) -> str:
    if row["gold_skill"] not in row["candidate_names"]:
        return "first_stage_candidate_miss"
    ranking = row["ranking"]
    if not ranking:
        return "empty_ranking"
    top = ranking[0]
    if top["skill"] == row["gold_skill"]:
        return "correct"
    if top.get("hierarchy_penalty", 0) > 0:
        return "broad_or_hierarchical_competitor"
    if top.get("boundary_penalty", 0) > 0.04:
        return "boundary_conflict"
    components = top.get("components", {})
    if components:
        best_field = max(components.items(), key=lambda item: item[1])[0]
        return f"reranker_overweighted_{best_field}"
    return "reranker_misorder"


def run_field_set(
    field_set_name: str,
    prompts: list[dict[str, Any]],
    first_stage_rankings: dict[str, list[tuple[str, float]]],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
    rerank_candidates: int,
    base_weight: float,
    field_weight: float,
    ranking_limit: int,
) -> list[dict[str, Any]]:
    enabled = parse_field_set(field_set_name)
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        first_stage = first_stage_rankings[prompt["id"]]
        candidates = first_stage[: min(rerank_candidates, len(first_stage))]
        candidate_names = [skill for skill, _ in candidates]
        base_scores = [score for _, score in candidates]
        base_norm = minmax(base_scores)
        field_results = [
            field_aware_pair_score(query, skill, r1, r2, r3, enabled_fields=enabled)
            for skill in candidate_names
        ]
        field_scores = [result["score"] for result in field_results]
        field_norm = minmax(field_scores)
        reranked: list[dict[str, Any]] = []
        for index, skill in enumerate(candidate_names):
            final_score = base_weight * base_norm[index] + field_weight * field_norm[index]
            reranked.append(
                {
                    "skill": skill,
                    "score": round(final_score, 6),
                    "base_score": round(base_scores[index], 6),
                    "field_score": round(field_scores[index], 6),
                    "components": {
                        key: round(value, 6) for key, value in field_results[index]["components"].items()
                    },
                    "boundary_penalty": round(field_results[index]["boundary_penalty"], 6),
                    "hierarchy_penalty": round(field_results[index]["hierarchy_penalty"], 6),
                }
            )
        reranked.sort(key=lambda item: (-item["score"], item["skill"]))
        row = {
            "prompt_id": prompt["id"],
            "family": prompt["family"],
            "gold_skill": prompt["gold_skill"],
            "closest_alternatives": prompt.get("closest_alternatives", []),
            "instruction_text": query,
            "field_set": field_set_name,
            "field_set_groups": explain_field_set(field_set_name),
            "candidate_names": candidate_names,
            "first_stage_ranking": [skill for skill, _ in first_stage[: max(100, rerank_candidates)]],
            "first_stage_top1": first_stage[0][0] if first_stage else None,
            "gold_first_stage_rank": next(
                (index + 1 for index, (skill, _) in enumerate(first_stage) if skill == prompt["gold_skill"]),
                None,
            ),
            "ranking": reranked[:ranking_limit],
        }
        row["failure_guess"] = guess_failure(row)
        rows.append(row)
    return rows


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# M6-v1 Field-Aware Reranker Evaluation",
        "",
        "This report evaluates a first M6-v1 prototype. It fixes the candidate generator and varies the skill information fields used by the reranker. The current matcher is transparent and lexical/field-aware; the architecture is designed so the field matcher can later be replaced by a stronger neural or LLM matcher.",
        "",
        "## Configuration",
        "",
        f"- Prompts: {report['prompt_count']}",
        f"- Skills: {report['skill_count']}",
        f"- First-stage method: `{report['first_stage']}`",
        f"- Rerank candidates: {report['rerank_candidates']}",
        f"- Score blend: {report['base_weight']} first-stage + {report['field_weight']} field-aware",
        "",
        "## Summary",
        "",
        "| Field set | Fields | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Candidate R@20 | Candidate R@50 | Candidate R@100 | Conditional top-1 | Reranker loss | Non-main top-1 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report["summary"]:
        metrics = item["metrics"]
        decomp = item["decomposition"]
        lines.append(
            f"| `{item['field_set']}` | {item['field_set_groups']} | "
            f"{metrics['top1_accuracy']:.1%} | {metrics['acceptable_top1_accuracy']:.1%} | "
            f"{metrics['top5_recall']:.1%} | {metrics['acceptable_top5_recall']:.1%} | "
            f"{metrics['mrr']:.3f} | "
            f"{decomp['candidate_recall']['recall@20']:.1%} | "
            f"{decomp['candidate_recall']['recall@50']:.1%} | "
            f"{decomp['candidate_recall']['recall@100']:.1%} | "
            f"{decomp['conditional_reranker_top1']:.1%} | "
            f"{decomp['reranker_loss_rate_given_gold_in_candidates']:.1%} | "
            f"{metrics['non_main_top1_rate']:.1%} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- A field set only supports the thesis if it improves final ranking without relying on prompt leakage.",
            "- Dependency/resource and boundary fields should not be treated as simple positive text; they are mainly feasibility and exclusion signals.",
            "- If candidate recall is low, the problem is first-stage retrieval rather than reranking.",
            "- If candidate recall is high but conditional reranker top-1 is low, the field matcher or field extraction is the bottleneck.",
            "",
            "## Prompt-Level Results",
        ]
    )
    acceptable_by_prompt = report.get("acceptable_alternatives", {})
    for item in report["summary"]:
        key = item["result_key"]
        lines.extend(["", f"### `{item['field_set']}`", ""])
        lines.append("| Prompt | Gold | First-stage rank | Final rank | Top-1 | Status | Failure guess | Top-5 |")
        lines.append("|---|---|---:|---:|---|---|---|---|")
        for row in report["results"][key]:
            ranking = [entry["skill"] for entry in row["ranking"]]
            gold = row["gold_skill"]
            prompt_acceptables = acceptable_by_prompt.get(row["prompt_id"], {})
            acceptable = {gold, *prompt_acceptables.get("acceptable", [])}
            borderline = set(prompt_acceptables.get("borderline", []))
            final_rank = ranking.index(gold) + 1 if gold in ranking else "-"
            top1 = ranking[0] if ranking else "-"
            if top1 == gold:
                status = "gold"
            elif top1 in acceptable:
                status = "acceptable"
            elif top1 in borderline:
                status = "borderline"
            else:
                status = "wrong"
            lines.append(
                f"| `{row['prompt_id']}` | `{gold}` | {row['gold_first_stage_rank']} | {final_rank} | "
                f"`{top1}` | {status} | {row['failure_guess']} | {', '.join(ranking[:5])} |"
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run M6-v1 field-aware procedural reranking.")
    parser.add_argument("--prompts", default="skill_benchmark/prompts/*.json")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--skills-root", default="skill_benchmark/skills")
    parser.add_argument("--acceptable-alternatives", default="skill_benchmark/annotations/acceptable_alternatives.json")
    parser.add_argument("--scale", default="current_full", choices=["core", "current_full"])
    parser.add_argument("--first-stage", default="tfidf_flat", choices=sorted(FIRST_STAGE_METHODS))
    parser.add_argument("--field-sets", default=",".join(DEFAULT_FIELD_SET_ORDER))
    parser.add_argument("--rerank-candidates", type=int, default=100)
    parser.add_argument("--base-weight", type=float, default=0.30)
    parser.add_argument("--field-weight", type=float, default=0.70)
    parser.add_argument("--ranking-limit", type=int, default=100)
    parser.add_argument("--cache-dir", default="skill_benchmark/runtime/provider_cache")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--qwen-model", default="text-embedding-v4")
    parser.add_argument("--qwen-base-url", default="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
    parser.add_argument("--qwen-batch-size", type=int, default=10)
    parser.add_argument("--skillrouter-model", default="pipizhao/SkillRouter-Embedding-0.6B")
    parser.add_argument("--skillrouter-batch-size", type=int, default=4)
    parser.add_argument("--skillrouter-max-length", type=int, default=1024)
    parser.add_argument("--skillrouter-device", choices=["auto", "cpu", "mps", "cuda"], default="auto")
    parser.add_argument("--quiet-progress", action="store_true")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--output-md", default="skill_benchmark/outputs/m6v1_field_aware_reranker.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/m6v1_field_aware_reranker.json")
    args = parser.parse_args()

    prompts = load_prompts_many(args.prompts)
    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    skill_names = build_scale_skill_names(args.scale, r1_rows)
    full_skill_texts = load_full_skill_texts(Path(args.skills_root), sorted(r1))
    docs = docs_for_first_stage(args.first_stage, skill_names, r1, r2, full_skill_texts)
    acceptable_by_prompt = load_acceptables(Path(args.acceptable_alternatives) if args.acceptable_alternatives else None)

    start = time.perf_counter()
    if args.first_stage == "qwen_full":
        first_stage_rankings, first_stage_runtime = qwen_rankings(
            prompts=prompts,
            skill_names=skill_names,
            docs=docs,
            cache_dir=Path(args.cache_dir),
            dotenv_path=Path(args.dotenv),
            batch_size=args.qwen_batch_size,
            model=args.qwen_model,
            base_url=args.qwen_base_url,
            timeout=args.timeout,
        )
    elif args.first_stage == "skillrouter_full":
        first_stage_rankings, first_stage_runtime = skillrouter_rankings(
            prompts=prompts,
            skill_names=skill_names,
            docs=docs,
            cache_dir=Path(args.cache_dir),
            dotenv_path=Path(args.dotenv),
            batch_size=args.skillrouter_batch_size,
            model=args.skillrouter_model,
            device=args.skillrouter_device,
            max_length=args.skillrouter_max_length,
            quiet_progress=args.quiet_progress,
        )
    else:
        first_stage_rankings, first_stage_runtime = local_rankings(args.first_stage, prompts, skill_names, docs)

    field_sets = [part.strip() for part in args.field_sets.split(",") if part.strip()]
    report: dict[str, Any] = {
        "prompt_count": len(prompts),
        "skill_count": len(skill_names),
        "scale": args.scale,
        "first_stage": args.first_stage,
        "rerank_candidates": args.rerank_candidates,
        "base_weight": args.base_weight,
        "field_weight": args.field_weight,
        "ranking_limit": args.ranking_limit,
        "first_stage_runtime": first_stage_runtime,
        "elapsed_ms": None,
        "summary": [],
        "results": {},
        "acceptable_alternatives": {
            prompt_id: {
                "acceptable": sorted(values.get("acceptable", set())),
                "borderline": sorted(values.get("borderline", set())),
            }
            for prompt_id, values in sorted(acceptable_by_prompt.items())
        },
    }

    selector_visible_tokens = sum(approximate_tokens(doc) for doc in docs)
    for field_set in field_sets:
        rows = run_field_set(
            field_set_name=field_set,
            prompts=prompts,
            first_stage_rankings=first_stage_rankings,
            r1=r1,
            r2=r2,
            r3=r3,
            rerank_candidates=args.rerank_candidates,
            base_weight=args.base_weight,
            field_weight=args.field_weight,
            ranking_limit=args.ranking_limit,
        )
        metrics = evaluate_rows(rows, r1, len(skill_names), selector_visible_tokens, acceptable_by_prompt)
        decomposition = compute_decomposition(rows, r1, acceptable_by_prompt)
        key = f"{args.first_stage}::{field_set}"
        report["results"][key] = rows
        report["summary"].append(
            {
                "field_set": field_set,
                "field_set_groups": explain_field_set(field_set),
                "result_key": key,
                "metrics": metrics,
                "decomposition": decomposition,
            }
        )

    report["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 2)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    for row in report["summary"]:
        metrics = row["metrics"]
        decomp = row["decomposition"]
        print(
            f"{args.first_stage}/{row['field_set']}: "
            f"top1={metrics['top1_accuracy']:.1%}, top5={metrics['top5_recall']:.1%}, "
            f"mrr={metrics['mrr']:.3f}, cand@100={decomp['candidate_recall']['recall@100']:.1%}, "
            f"cond_top1={decomp['conditional_reranker_top1']:.1%}, non_main={metrics['non_main_top1_rate']:.1%}"
        )


if __name__ == "__main__":
    main()
