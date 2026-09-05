#!/usr/bin/env python3

from __future__ import annotations

import argparse
import math
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_offline_selectors import (  # noqa: E402
    TfIdfScorer,
    approximate_tokens,
    build_scale_skill_names,
    evaluate_rows,
    instruction_text,
    load_acceptables,
    load_full_skill_texts,
    load_jsonl,
    load_prompts,
    rank_scores,
    tokenize,
)


class CachedBm25Scorer:
    def __init__(self, docs: list[str]) -> None:
        self.doc_terms = [tokenize(doc) for doc in docs]
        self.doc_lens = [len(terms) for terms in self.doc_terms]
        self.avg_len = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 0.0
        self.doc_tf = [Counter(terms) for terms in self.doc_terms]
        self.df: Counter[str] = Counter()
        for terms in self.doc_terms:
            self.df.update(set(terms))
        self.n_docs = len(docs)
        self.k1 = 1.5
        self.b = 0.75

    def scores(self, query: str) -> list[float]:
        query_terms = tokenize(query)
        scores: list[float] = []
        for tf, doc_len in zip(self.doc_tf, self.doc_lens):
            score = 0.0
            for term in query_terms:
                if term not in tf:
                    continue
                idf = math.log(1 + (self.n_docs - self.df[term] + 0.5) / (self.df[term] + 0.5))
                denom = tf[term] + self.k1 * (
                    1 - self.b + self.b * (doc_len / self.avg_len if self.avg_len else 0)
                )
                score += idf * (tf[term] * (self.k1 + 1)) / denom
            scores.append(score)
        return scores


def docs_for_representation(
    representation: str,
    skill_names: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
    full_skill_texts: dict[str, str],
) -> list[str]:
    if representation == "r1":
        return [r1[name]["text"] for name in skill_names]
    if representation == "r2":
        return [r2[name]["text"] for name in skill_names]
    if representation == "r3":
        return [r3[name]["text"] for name in skill_names]
    if representation == "full":
        return [full_skill_texts.get(name) or r2[name]["text"] for name in skill_names]
    raise ValueError(f"Unknown representation: {representation}")


def run_lexical_selector(
    *,
    method: str,
    representation: str,
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    docs: list[str],
    ranking_limit: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    start = time.perf_counter()
    scorer: Any = None
    if method == "tfidf":
        scorer = TfIdfScorer(docs)
    elif method == "bm25":
        scorer = CachedBm25Scorer(docs)
    else:
        raise ValueError(f"Unknown method: {method}")

    rows: list[dict[str, Any]] = []
    gold_rank_at_20 = 0
    gold_rank_at_100 = 0
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        scores = scorer.scores(query)
        ranked = rank_scores(skill_names, scores)
        gold_rank = next(
            (index + 1 for index, (skill, _) in enumerate(ranked) if skill == prompt["gold_skill"]),
            None,
        )
        if isinstance(gold_rank, int) and gold_rank <= 20:
            gold_rank_at_20 += 1
        if isinstance(gold_rank, int) and gold_rank <= 100:
            gold_rank_at_100 += 1
        rows.append(
            {
                "prompt_id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": prompt["gold_skill"],
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "instruction_text": query,
                "method": method,
                "representation": representation,
                "gold_first_stage_rank": gold_rank,
                "ranking": [
                    {"skill": skill, "score": round(score, 6)}
                    for skill, score in ranked[:ranking_limit]
                ],
            }
        )

    elapsed_ms = (time.perf_counter() - start) * 1000
    total = len(prompts) or 1
    return rows, {
        "elapsed_ms": round(elapsed_ms, 2),
        "gold_recall_at_20": round(gold_rank_at_20 / total, 4),
        "gold_recall_at_100": round(gold_rank_at_100 / total, 4),
    }


def pct(value: float) -> str:
    return f"{value:.1%}"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Frozen v0.4 Crossed Lexical Representation Matrix",
        "",
        "This report runs the same lexical retrievers over the same representation layers. It is intended as a representation-layer control: BM25/TF-IDF are weak modern retrievers, but they help identify whether gains come from exposing different skill information rather than changing the model.",
        "",
        f"- Benchmark version: `{report['benchmark_version']}`",
        f"- Skill scale: `{report['scale']}` ({report['skill_count']} skills)",
        f"- Ranking limit stored per prompt: top-{report['ranking_limit']}",
        "",
        "## Summary",
        "",
        "| Stratum | Retriever | Representation | N | Top-1 | Accept Top-1 | Top-5 | MRR | Cand R@20 | Cand R@100 | Tokens | Latency ms |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["summary"]:
        metrics = row["metrics"]
        run = row["run_metrics"]
        lines.append(
            f"| {row['stratum']} | {row['retriever'].upper()} | {row['representation'].upper()} | "
            f"{metrics['total_prompts']} | {pct(metrics['top1_accuracy'])} | "
            f"{pct(metrics['acceptable_top1_accuracy'])} | {pct(metrics['top5_recall'])} | "
            f"{metrics['mrr']:.3f} | {pct(run['gold_recall_at_20'])} | "
            f"{pct(run['gold_recall_at_100'])} | {metrics['selector_visible_tokens_approx']} | "
            f"{run['elapsed_ms']:.1f} |"
        )

    lines.extend(
        [
            "",
            "## Reading Guide",
            "",
            "- Compare rows with the same stratum and retriever to isolate the effect of representation text.",
            "- `Cand R@20` and `Cand R@100` are first-stage gold recall at candidate budgets. They matter for later rerankers because a reranker cannot recover a gold skill that was never shortlisted.",
            "- RFULL is not automatically better: it exposes more text, but also more noise and much higher token cost.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run lexical retrievers over R1/R2/R3/full representations.")
    parser.add_argument("--benchmark-version", default="benchmark-v0.4-2026-06-16")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--skills-root", default="skill_benchmark/skills")
    parser.add_argument("--scale", default="current_full", choices=["core", "current_full"])
    parser.add_argument("--representations", default="r1,r2,full")
    parser.add_argument("--retrievers", default="bm25,tfidf")
    parser.add_argument("--controlled-prompts", default="skill_benchmark/prompts/*.json")
    parser.add_argument("--public-prompts", default="skill_benchmark/prompts_public_gold/*.json")
    parser.add_argument("--controlled-acceptables", default="skill_benchmark/annotations/acceptable_alternatives.json")
    parser.add_argument(
        "--public-acceptables",
        default="skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    )
    parser.add_argument("--ranking-limit", type=int, default=100)
    parser.add_argument("--output-md", default="skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.json")
    args = parser.parse_args()

    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    skill_names = build_scale_skill_names(args.scale, r1_rows)
    full_skill_texts = load_full_skill_texts(Path(args.skills_root), sorted(r1))

    strata = [
        (
            "controlled",
            load_prompts(args.controlled_prompts),
            load_acceptables(Path(args.controlled_acceptables)),
        ),
        (
            "public_gold",
            load_prompts(args.public_prompts),
            load_acceptables(Path(args.public_acceptables)),
        ),
    ]
    representations = [item.strip() for item in args.representations.split(",") if item.strip()]
    retrievers = [item.strip() for item in args.retrievers.split(",") if item.strip()]

    report: dict[str, Any] = {
        "benchmark_version": args.benchmark_version,
        "scale": args.scale,
        "skill_count": len(skill_names),
        "ranking_limit": args.ranking_limit,
        "summary": [],
        "results": {},
    }

    docs_by_rep: dict[str, list[str]] = {}
    tokens_by_rep: dict[str, int] = {}
    for representation in representations:
        docs = docs_for_representation(representation, skill_names, r1, r2, r3, full_skill_texts)
        docs_by_rep[representation] = docs
        tokens_by_rep[representation] = sum(approximate_tokens(doc) for doc in docs)

    for stratum, prompts, acceptable_by_prompt in strata:
        for retriever in retrievers:
            for representation in representations:
                rows, run_metrics = run_lexical_selector(
                    method=retriever,
                    representation=representation,
                    prompts=prompts,
                    skill_names=skill_names,
                    docs=docs_by_rep[representation],
                    ranking_limit=args.ranking_limit,
                )
                metrics = evaluate_rows(
                    rows,
                    r1,
                    len(skill_names),
                    tokens_by_rep[representation],
                    acceptable_by_prompt,
                )
                key = f"{stratum}_{retriever}_{representation}"
                report["results"][key] = rows
                report["summary"].append(
                    {
                        "key": key,
                        "stratum": stratum,
                        "retriever": retriever,
                        "representation": representation,
                        "metrics": metrics,
                        "run_metrics": run_metrics,
                    }
                )
                print(
                    f"{key}: top1={metrics['top1_accuracy']:.1%} "
                    f"top5={metrics['top5_recall']:.1%} "
                    f"r20={run_metrics['gold_recall_at_20']:.1%}"
                )

    Path(args.output_json).write_text(json.dumps(report, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {args.output_md}")
    print(f"Wrote {args.output_json}")


if __name__ == "__main__":
    main()
