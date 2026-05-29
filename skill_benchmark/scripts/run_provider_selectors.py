#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_offline_selectors import (  # noqa: E402
    approximate_tokens,
    build_scale_skill_names,
    evaluate_rows,
    instruction_text,
    load_acceptables,
    load_full_skill_texts,
    load_jsonl,
    load_prompts,
    minmax,
    schema_pair_score,
)


EMBEDDING_PROVIDER_DEFAULTS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "key_env": "OPENAI_API_KEY",
        "model": "text-embedding-3-small",
        "batch_size": 96,
    },
    "qwen": {
        "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "key_env": "DASHSCOPE_API_KEY",
        "model": "text-embedding-v4",
        "batch_size": 10,
    },
    "openai-compatible": {
        "base_url": "",
        "key_env": "PROVIDER_API_KEY",
        "model": "",
        "batch_size": 32,
    },
}

QWEN_RERANK_ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"


def slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-._" else "_" for char in value)
    return cleaned.strip("_") or "default"


def sha256_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def post_json(url: str, api_key: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{url} returned HTTP {exc.code}: {detail[:1000]}") from exc


class OpenAICompatibleEmbeddingClient:
    def __init__(
        self,
        provider: str,
        base_url: str,
        api_key: str,
        model: str,
        cache_dir: Path,
        timeout: int,
        dimensions: int | None,
    ) -> None:
        if not base_url:
            raise ValueError("An embedding base URL is required.")
        if not model:
            raise ValueError("An embedding model is required.")
        self.provider = provider
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.dimensions = dimensions
        self.cache_dir = cache_dir / "embeddings" / slug(provider) / slug(model)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.tokens_approx = 0
        self.api_calls = 0
        self.cache_hits = 0

    def cache_path(self, text: str) -> Path:
        key = sha256_json(
            {
                "provider": self.provider,
                "base_url": self.base_url,
                "model": self.model,
                "dimensions": self.dimensions,
                "text": text,
            }
        )
        return self.cache_dir / f"{key}.json"

    def embed_many(self, texts: list[str], batch_size: int) -> list[list[float]]:
        vectors: list[list[float] | None] = [None for _ in texts]
        missing: list[tuple[int, str, Path]] = []
        for index, text in enumerate(texts):
            path = self.cache_path(text)
            if path.exists():
                vectors[index] = json.loads(path.read_text(encoding="utf-8"))["embedding"]
                self.cache_hits += 1
            else:
                missing.append((index, text, path))

        for start in range(0, len(missing), batch_size):
            batch = missing[start : start + batch_size]
            payload: dict[str, Any] = {
                "model": self.model,
                "input": [text for _, text, _ in batch],
            }
            if self.dimensions is not None:
                payload["dimensions"] = self.dimensions
            response = post_json(f"{self.base_url}/embeddings", self.api_key, payload, self.timeout)
            data = sorted(response.get("data", []), key=lambda row: row.get("index", 0))
            if len(data) != len(batch):
                raise RuntimeError(f"Expected {len(batch)} embeddings, received {len(data)}")
            self.api_calls += 1
            for (index, text, path), item in zip(batch, data):
                embedding = item.get("embedding")
                if not isinstance(embedding, list):
                    raise RuntimeError(f"Embedding response missing vector for item {index}")
                vectors[index] = embedding
                path.write_text(json.dumps({"embedding": embedding}), encoding="utf-8")
                self.tokens_approx += approximate_tokens(text)

        return [vector for vector in vectors if vector is not None]


class QwenRerankClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        cache_dir: Path,
        timeout: int,
        instruct: str | None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.instruct = instruct
        self.cache_dir = cache_dir / "rerank" / "qwen" / slug(model)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.tokens_approx = 0
        self.api_calls = 0
        self.cache_hits = 0

    def rerank(self, query: str, documents: list[str]) -> list[float]:
        key = sha256_json(
            {
                "provider": "qwen-rerank",
                "model": self.model,
                "query": query,
                "documents": documents,
                "instruct": self.instruct,
            }
        )
        path = self.cache_dir / f"{key}.json"
        if path.exists():
            self.cache_hits += 1
            return json.loads(path.read_text(encoding="utf-8"))["scores"]

        parameters: dict[str, Any] = {
            "return_documents": False,
            "top_n": len(documents),
        }
        if self.instruct:
            parameters["instruct"] = self.instruct
        payload = {
            "model": self.model,
            "input": {
                "query": query,
                "documents": documents,
            },
            "parameters": parameters,
        }
        response = post_json(QWEN_RERANK_ENDPOINT, self.api_key, payload, self.timeout)
        results = response.get("output", {}).get("results", [])
        scores = [0.0 for _ in documents]
        for item in results:
            index = item.get("index")
            if isinstance(index, int) and 0 <= index < len(scores):
                scores[index] = float(item.get("relevance_score", 0.0))
        path.write_text(json.dumps({"scores": scores}), encoding="utf-8")
        self.api_calls += 1
        self.tokens_approx += approximate_tokens(query) * len(documents)
        self.tokens_approx += sum(approximate_tokens(document) for document in documents)
        return scores


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def docs_for_representation(
    representation: str,
    skill_names: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    full_skill_texts: dict[str, str],
) -> list[str]:
    if representation == "r1":
        return [r1[name]["text"] for name in skill_names]
    if representation == "r2":
        return [r2[name]["text"] for name in skill_names]
    if representation == "full":
        return [full_skill_texts.get(name) or r2[name]["text"] for name in skill_names]
    raise ValueError(f"Unknown representation: {representation}")


def rank_with_scores(skill_names: list[str], scores: list[float]) -> list[tuple[str, float]]:
    return sorted(zip(skill_names, scores), key=lambda item: (-item[1], item[0]))


def render_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    lines = [
        "# Provider Selector Evaluation Report",
        "",
        "This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.",
        "",
        "## Configuration",
        "",
        f"- Embedding provider: `{report['embedding_provider']}`",
        f"- Embedding model: `{report['embedding_model']}`",
        f"- Embedding representation: `{report['embedding_representation']}`",
        f"- Scale: `{report['scale']}` ({metrics['scale_skill_count']} skills)",
        f"- Reranker: `{report['reranker_provider']}`",
        f"- Rerank candidates: {report['rerank_candidates']}",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Top-1 accuracy | {metrics['top1_accuracy']:.1%} |",
        f"| Acceptable top-1 accuracy | {metrics['acceptable_top1_accuracy']:.1%} |",
        f"| Top-3 recall | {metrics['top3_recall']:.1%} |",
        f"| Top-5 recall | {metrics['top5_recall']:.1%} |",
        f"| Acceptable top-5 recall | {metrics['acceptable_top5_recall']:.1%} |",
        f"| MRR | {metrics['mrr']:.3f} |",
        f"| Non-main top-1 | {metrics['non_main_top1_rate']:.1%} |",
        f"| Approx selector-visible tokens | {metrics['selector_visible_tokens_approx']} |",
        "",
        "## API Usage Estimate",
        "",
        f"- Embedding API calls made in this run: {report['api_usage']['embedding_api_calls']}",
        f"- Embedding cache hits: {report['api_usage']['embedding_cache_hits']}",
        f"- Approx uncached embedding input tokens: {report['api_usage']['embedding_tokens_approx']}",
        f"- Rerank API calls made in this run: {report['api_usage']['rerank_api_calls']}",
        f"- Rerank cache hits: {report['api_usage']['rerank_cache_hits']}",
        f"- Approx uncached rerank input tokens: {report['api_usage']['rerank_tokens_approx']}",
        "",
        "## Prompt-Level Results",
        "",
        "| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |",
        "|---|---|---:|---:|---|---|---|",
    ]
    acceptable_by_prompt = report.get("acceptable_alternatives", {})
    for row in report["results"]:
        ranking = [item["skill"] for item in row["ranking"]]
        gold = row["gold_skill"]
        prompt_acceptables = acceptable_by_prompt.get(row["prompt_id"], {})
        acceptable = {gold, *prompt_acceptables.get("acceptable", [])}
        borderline = set(prompt_acceptables.get("borderline", []))
        rank = ranking.index(gold) + 1 if gold in ranking else "-"
        acceptable_rank = next((index + 1 for index, skill in enumerate(ranking) if skill in acceptable), "-")
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
            f"| `{row['prompt_id']}` | `{gold}` | {rank} | {acceptable_rank} | `{top1}` | {status} | {', '.join(ranking[:5])} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run API-backed embedding and reranking selector baselines.")
    parser.add_argument("--prompts", default="skill_benchmark/prompts/*.json")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--skills-root", default="skill_benchmark/skills")
    parser.add_argument("--acceptable-alternatives", default="skill_benchmark/annotations/acceptable_alternatives.json")
    parser.add_argument("--scale", default="current_full", choices=["core", "current_full"])
    parser.add_argument("--embedding-representation", default="full", choices=["r1", "r2", "full"])
    parser.add_argument("--embedding-provider", default="qwen", choices=sorted(EMBEDDING_PROVIDER_DEFAULTS))
    parser.add_argument("--embedding-base-url")
    parser.add_argument("--embedding-key-env")
    parser.add_argument("--embedding-model")
    parser.add_argument("--embedding-dimensions", type=int)
    parser.add_argument("--embedding-batch-size", type=int)
    parser.add_argument("--reranker-provider", default="qwen", choices=["none", "qwen", "local-schema"])
    parser.add_argument("--reranker-key-env", default="DASHSCOPE_API_KEY")
    parser.add_argument("--reranker-model", default="qwen3-rerank")
    parser.add_argument(
        "--reranker-instruct",
        default="Given a user request and candidate agent skill documents, rank skills by procedural suitability. Prefer the skill whose inputs, workflow, outputs, dependencies, and constraints match the request.",
    )
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--local-schema-base-weight", type=float, default=0.40)
    parser.add_argument("--local-schema-weight", type=float, default=0.60)
    parser.add_argument("--cache-dir", default="skill_benchmark/runtime/provider_cache")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--max-prompts", type=int)
    parser.add_argument("--ranking-limit", type=int, default=20)
    parser.add_argument("--output-md", default="skill_benchmark/outputs/provider_selector_evaluation.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/provider_selector_evaluation.json")
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))
    provider_defaults = EMBEDDING_PROVIDER_DEFAULTS[args.embedding_provider]
    embedding_base_url = args.embedding_base_url or provider_defaults["base_url"]
    embedding_key_env = args.embedding_key_env or provider_defaults["key_env"]
    embedding_model = args.embedding_model or provider_defaults["model"]
    embedding_batch_size = args.embedding_batch_size or provider_defaults["batch_size"]
    embedding_key = os.environ.get(embedding_key_env)
    if not embedding_key:
        raise SystemExit(
            f"Missing {embedding_key_env}. Copy .env.example to .env, set {embedding_key_env}, "
            f"then run `source .env` or pass --dotenv .env."
        )
    reranker_key = None
    if args.reranker_provider == "qwen":
        reranker_key = os.environ.get(args.reranker_key_env)
        if not reranker_key:
            raise SystemExit(f"Missing {args.reranker_key_env} for --reranker-provider {args.reranker_provider}.")

    prompts = load_prompts(args.prompts)
    if args.max_prompts:
        prompts = prompts[: args.max_prompts]
    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    skill_names = build_scale_skill_names(args.scale, r1_rows)
    full_skill_texts = load_full_skill_texts(Path(args.skills_root), sorted(r1))
    docs = docs_for_representation(args.embedding_representation, skill_names, r1, r2, full_skill_texts)
    acceptable_by_prompt = load_acceptables(Path(args.acceptable_alternatives) if args.acceptable_alternatives else None)
    cache_dir = Path(args.cache_dir)

    embedding_client = OpenAICompatibleEmbeddingClient(
        provider=args.embedding_provider,
        base_url=embedding_base_url,
        api_key=embedding_key,
        model=embedding_model,
        cache_dir=cache_dir,
        timeout=args.timeout,
        dimensions=args.embedding_dimensions,
    )
    rerank_client = (
        QwenRerankClient(
            api_key=reranker_key or "",
            model=args.reranker_model,
            cache_dir=cache_dir,
            timeout=args.timeout,
            instruct=args.reranker_instruct,
        )
        if args.reranker_provider == "qwen"
        else None
    )

    start = time.perf_counter()
    doc_embeddings = embedding_client.embed_many(docs, embedding_batch_size)

    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        query_embedding = embedding_client.embed_many([query], 1)[0]
        first_stage_scores = [cosine(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]
        first_stage = rank_with_scores(skill_names, first_stage_scores)
        first_stage_ranking = [skill for skill, _ in first_stage]
        gold_skill = prompt["gold_skill"]
        gold_first_stage_rank = (
            first_stage_ranking.index(gold_skill) + 1 if gold_skill in first_stage_ranking else None
        )

        if rerank_client:
            candidate_count = min(args.rerank_candidates, len(first_stage))
            candidate_names = [name for name, _ in first_stage[:candidate_count]]
            candidate_docs = [docs[skill_names.index(name)] for name in candidate_names]
            rerank_scores = rerank_client.rerank(query, candidate_docs)
            ranked = rank_with_scores(candidate_names, rerank_scores)
        elif args.reranker_provider == "local-schema":
            candidate_count = min(args.rerank_candidates, len(first_stage))
            candidate_names = [name for name, _ in first_stage[:candidate_count]]
            candidate_base_scores = [score for _, score in first_stage[:candidate_count]]
            candidate_schema_scores = [
                schema_pair_score(query, name, r1, r2, r3) for name in candidate_names
            ]
            base_norm = minmax(candidate_base_scores)
            schema_norm = minmax(candidate_schema_scores)
            combined_scores = [
                args.local_schema_base_weight * base_norm[index]
                + args.local_schema_weight * schema_norm[index]
                for index in range(len(candidate_names))
            ]
            ranked = rank_with_scores(candidate_names, combined_scores)
        else:
            ranked = first_stage
            candidate_count = len(first_stage)

        final_ranking = [skill for skill, _ in ranked]
        gold_final_rank = final_ranking.index(gold_skill) + 1 if gold_skill in final_ranking else None

        rows.append(
            {
                "prompt_id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": gold_skill,
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "instruction_text": query,
                "gold_first_stage_rank": gold_first_stage_rank,
                "gold_final_rank": gold_final_rank,
                "first_stage_top1": first_stage[0][0] if first_stage else None,
                "candidate_count": candidate_count,
                "ranking": [
                    {"skill": skill, "score": round(score, 6)}
                    for skill, score in ranked[: args.ranking_limit]
                ],
            }
        )

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    selector_visible_tokens = sum(approximate_tokens(doc) for doc in docs)
    if rerank_client:
        selector_visible_tokens += rerank_client.tokens_approx
    metrics = evaluate_rows(rows, r1, len(skill_names), selector_visible_tokens, acceptable_by_prompt)
    report = {
        "embedding_provider": args.embedding_provider,
        "embedding_base_url": embedding_base_url,
        "embedding_model": embedding_model,
        "embedding_representation": args.embedding_representation,
        "scale": args.scale,
        "reranker_provider": args.reranker_provider,
        "reranker_model": args.reranker_model if rerank_client else None,
        "rerank_candidates": args.rerank_candidates if args.reranker_provider != "none" else 0,
        "local_schema_base_weight": args.local_schema_base_weight if args.reranker_provider == "local-schema" else None,
        "local_schema_weight": args.local_schema_weight if args.reranker_provider == "local-schema" else None,
        "elapsed_ms": elapsed_ms,
        "metrics": metrics,
        "api_usage": {
            "embedding_api_calls": embedding_client.api_calls,
            "embedding_cache_hits": embedding_client.cache_hits,
            "embedding_tokens_approx": embedding_client.tokens_approx,
            "rerank_api_calls": rerank_client.api_calls if rerank_client else 0,
            "rerank_cache_hits": rerank_client.cache_hits if rerank_client else 0,
            "rerank_tokens_approx": rerank_client.tokens_approx if rerank_client else 0,
        },
        "acceptable_alternatives": {
            prompt_id: {
                "acceptable": sorted(values.get("acceptable", set())),
                "borderline": sorted(values.get("borderline", set())),
            }
            for prompt_id, values in sorted(acceptable_by_prompt.items())
        },
        "results": rows,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(
        f"{args.embedding_provider}/{embedding_model}"
        f" + {args.reranker_provider}: top1={metrics['top1_accuracy']:.1%}, "
        f"top5={metrics['top5_recall']:.1%}, mrr={metrics['mrr']:.3f}, "
        f"non_main_top1={metrics['non_main_top1_rate']:.1%}"
    )


if __name__ == "__main__":
    main()
