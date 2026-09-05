#!/usr/bin/env python3
"""Run local RQ1a field-discriminability ablations.

The runner is intentionally small and cluster-restricted. It answers:

If the prompt requires field value X, and candidate skills share the same
neutral context, does exposing the target skill-side field help rank the gold
sibling above near neighbours?
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_provider_selectors import (  # noqa: E402
    EMBEDDING_PROVIDER_DEFAULTS,
    OpenAICompatibleEmbeddingClient,
    load_dotenv,
)


TOKEN_RE = re.compile(r"[a-z0-9]+")
EPSILON = 1e-9


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def approximate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text.split()) * 1.3))


def cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def prompt_query_text(prompt: dict[str, Any]) -> str:
    parts = [str(prompt["prompt"])]
    routing_context = str(prompt.get("routing_context", "")).strip()
    if routing_context:
        parts.append("Routing context:\n" + routing_context)
    return "\n\n".join(parts)


def load_suite(suite_dir: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    prompts = read_jsonl(suite_dir / "prompts.jsonl")
    units = {
        unit["cluster_id"]: unit
        for unit_path in sorted((suite_dir / "clusters").glob("*/unit.json"))
        for unit in [json.loads(unit_path.read_text(encoding="utf-8"))]
    }
    return prompts, units


def skill_doc_text(suite_dir: Path, unit: dict[str, Any], skill: dict[str, Any]) -> str:
    path = suite_dir / "clusters" / unit["cluster_id"] / skill["skill_path"]
    return path.read_text(encoding="utf-8")


def shared_context_doc(unit: dict[str, Any]) -> str:
    parts = [
        unit["shared_context"],
        unit["shared_use_condition"],
    ]
    for optional_key in ("shared_input_precondition", "shared_output_artifact"):
        value = unit.get(optional_key)
        if value:
            parts.append(value)
    parts.extend(
        [
            "\n".join(unit["shared_workflow_steps"]),
            "\n".join(unit["shared_success_criteria"]),
            "\n".join(unit["shared_boundaries"]),
            "\n".join(unit["shared_dependencies"]),
        ]
    )
    return "\n".join(parts)


def shared_context_without_input_output_doc(unit: dict[str, Any]) -> str:
    parts = [
        unit["shared_context"],
        unit["shared_use_condition"],
        "\n".join(unit["shared_workflow_steps"]),
        "\n".join(unit["shared_success_criteria"]),
        "\n".join(unit["shared_boundaries"]),
        "\n".join(unit["shared_dependencies"]),
    ]
    return "\n".join(parts)


def field_label(field: str) -> str:
    return {
        "input_precondition": "Input / Precondition",
        "output_artifact": "Output Artifact",
        "use_condition": "Use Condition",
        "workflow_procedure": "Workflow / Procedure",
        "boundary_not_for": "Boundary / Not For",
        "dependency_resource": "Dependency / Resource",
        "success_verification": "Success / Verification",
        "examples_tests": "Examples / Tests",
    }.get(field, field.replace("_", " ").title())


def skill_field_value(unit: dict[str, Any], skill: dict[str, Any]) -> str:
    field = unit["field"]
    if field not in skill:
        raise KeyError(f"Skill {skill.get('skill_id')} missing field {field}")
    value = skill[field]
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value)


def doc_for_condition(suite_dir: Path, unit: dict[str, Any], skill: dict[str, Any], condition: str) -> str:
    if condition == "shared_context_only":
        return shared_context_doc(unit)
    if condition == "shared_context_no_input_output":
        return shared_context_without_input_output_doc(unit)
    if condition == "shared_context_no_input_output_plus_field":
        return shared_context_without_input_output_doc(unit) + f"\n{field_label(unit['field'])}: " + skill_field_value(unit, skill)
    if condition == "shared_context_plus_input_output":
        return shared_context_doc(unit)
    if condition == "shared_context_plus_input_output_field":
        return shared_context_doc(unit) + f"\n{field_label(unit['field'])}: " + skill_field_value(unit, skill)
    if condition == "field_only":
        return skill_field_value(unit, skill)
    if condition == "shared_context_plus_field":
        return shared_context_doc(unit) + f"\n{field_label(unit['field'])}: " + skill_field_value(unit, skill)
    if condition == "full_skill_doc":
        return skill_doc_text(suite_dir, unit, skill)
    raise ValueError(f"Unknown condition: {condition}")


def tfidf_scores(query: str, docs: list[str]) -> list[float]:
    doc_tokens = [tokens(doc) for doc in docs]
    query_tokens = tokens(query)
    vocabulary = sorted(set(query_tokens).union(*(set(row) for row in doc_tokens)))
    if not vocabulary:
        return [0.0 for _ in docs]
    doc_freq = Counter(term for term in vocabulary for row in doc_tokens if term in row)
    n_docs = len(docs)
    idf = {term: math.log((n_docs + 1) / (doc_freq[term] + 1)) + 1 for term in vocabulary}

    def vector(row: list[str]) -> dict[str, float]:
        counts = Counter(row)
        total = sum(counts.values()) or 1
        return {term: (count / total) * idf[term] for term, count in counts.items()}

    query_vec = vector(query_tokens)
    query_norm = math.sqrt(sum(value * value for value in query_vec.values()))
    scores = []
    for row in doc_tokens:
        doc_vec = vector(row)
        doc_norm = math.sqrt(sum(value * value for value in doc_vec.values()))
        if not query_norm or not doc_norm:
            scores.append(0.0)
            continue
        dot = sum(query_vec.get(term, 0.0) * doc_vec.get(term, 0.0) for term in query_vec)
        scores.append(dot / (query_norm * doc_norm))
    return scores


def bm25_scores(query: str, docs: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
    doc_tokens = [tokens(doc) for doc in docs]
    query_terms = tokens(query)
    n_docs = len(docs)
    avg_len = mean([len(row) for row in doc_tokens] or [1]) or 1
    doc_freq = Counter(term for term in set(query_terms) for row in doc_tokens if term in row)
    scores = []
    for row in doc_tokens:
        counts = Counter(row)
        doc_len = len(row) or 1
        score = 0.0
        for term in query_terms:
            df = doc_freq.get(term, 0)
            if not df:
                continue
            idf = math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
            tf = counts.get(term, 0)
            denom = tf + k1 * (1 - b + b * doc_len / avg_len)
            if denom:
                score += idf * (tf * (k1 + 1)) / denom
        scores.append(score)
    return scores


def score(query: str, docs: list[str], retriever: str) -> list[float]:
    if retriever == "tfidf":
        return tfidf_scores(query, docs)
    if retriever == "bm25":
        return bm25_scores(query, docs)
    raise ValueError(f"Unknown retriever: {retriever}")


def tie_aware_metrics(skill_ids: list[str], scores: list[float], gold: str) -> dict[str, Any]:
    gold_score = scores[skill_ids.index(gold)]
    greater = sum(1 for value in scores if value > gold_score + EPSILON)
    tied = sum(1 for value in scores if abs(value - gold_score) <= EPSILON)
    rank_min = greater + 1
    rank_max = greater + tied
    expected_top1 = (1 / tied) if greater == 0 and tied else 0.0
    expected_mrr = mean(1 / rank for rank in range(rank_min, rank_max + 1))
    ranking = [
        skill_id
        for skill_id, _score in sorted(
            zip(skill_ids, scores, strict=True),
            key=lambda item: (-item[1], item[0]),
        )
    ]
    return {
        "ranking": ranking,
        "top1_deterministic": 1.0 if ranking and ranking[0] == gold else 0.0,
        "top1_tie_adjusted": expected_top1,
        "mrr_tie_adjusted": expected_mrr,
        "gold_rank_min": rank_min,
        "gold_rank_max": rank_max,
        "gold_tie_size": tied,
    }


def run(
    suite_dir: Path,
    retrievers: list[str],
    conditions: list[str],
    embedding_client: OpenAICompatibleEmbeddingClient | None = None,
    embedding_batch_size: int = 10,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    prompts, units = load_suite(suite_dir)
    text_embeddings: dict[str, list[float]] = {}
    if "qwen_embedding" in retrievers:
        if embedding_client is None:
            raise ValueError("qwen_embedding retriever requires an embedding client.")
        unique_texts: list[str] = []
        seen: set[str] = set()

        def add_text(text: str) -> None:
            if text not in seen:
                seen.add(text)
                unique_texts.append(text)

        for prompt in prompts:
            add_text(prompt_query_text(prompt))
        for unit in units.values():
            for condition in conditions:
                for skill in unit["skills"]:
                    add_text(doc_for_condition(suite_dir, unit, skill, condition))
        vectors = embedding_client.embed_many(unique_texts, embedding_batch_size)
        text_embeddings = dict(zip(unique_texts, vectors, strict=True))

    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query_text = prompt_query_text(prompt)
        unit = units[prompt["cluster_id"]]
        skills = unit["skills"]
        skill_ids = [skill["skill_id"] for skill in skills]
        for condition in conditions:
            docs = [doc_for_condition(suite_dir, unit, skill, condition) for skill in skills]
            for retriever in retrievers:
                if retriever == "qwen_embedding":
                    query_vector = text_embeddings[query_text]
                    scores = [cosine(query_vector, text_embeddings[doc]) for doc in docs]
                else:
                    scores = score(query_text, docs, retriever)
                metrics = tie_aware_metrics(skill_ids, scores, prompt["gold_skill_id"])
                rows.append(
                    {
                        "prompt_id": prompt["prompt_id"],
                        "cluster_id": prompt["cluster_id"],
                        "field": prompt["field"],
                        "prompt_variant": prompt["prompt_variant"],
                        "retriever": retriever,
                        "condition": condition,
                        "gold_skill_id": prompt["gold_skill_id"],
                        "candidate_skill_ids": skill_ids,
                        "prompt": prompt["prompt"],
                        "routing_context": prompt.get("routing_context", ""),
                        "query_text": query_text,
                        "canonical_term_required": prompt.get("canonical_term_required", False),
                        "canonical_terms_retained": prompt.get("canonical_terms_retained", []),
                        "selector_visible_tokens": sum(approximate_tokens(doc) for doc in docs),
                        "scores": {
                            skill_id: round(float(value), 8)
                            for skill_id, value in zip(skill_ids, scores, strict=True)
                        },
                        **metrics,
                    }
                )

    summaries: list[dict[str, Any]] = []
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["retriever"], row["condition"], row["prompt_variant"])].append(row)
        groups[(row["retriever"], row["condition"], "all")].append(row)
    for (retriever, condition, prompt_variant), group_rows in sorted(groups.items()):
        n = len(group_rows)
        summaries.append(
            {
                "retriever": retriever,
                "condition": condition,
                "prompt_variant": prompt_variant,
                "n": n,
                "top1_tie_adjusted": mean(row["top1_tie_adjusted"] for row in group_rows),
                "top1_deterministic": mean(row["top1_deterministic"] for row in group_rows),
                "mrr_tie_adjusted": mean(row["mrr_tie_adjusted"] for row in group_rows),
                "mean_gold_tie_size": mean(row["gold_tie_size"] for row in group_rows),
                "selector_visible_tokens_mean": mean(row["selector_visible_tokens"] for row in group_rows),
            }
        )
    return rows, summaries


def render_markdown(suite_dir: Path, rows: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> str:
    field = rows[0]["field"] if rows else "unknown"
    field_title = field.replace("_", " ").title()

    def display_prompt_variant(prompt_variant: str) -> str:
        return "combined" if prompt_variant == "all" else prompt_variant

    variant_order = ["direct", "paraphrase", "contextual", "implicit_authority"]
    present_variants = {item["prompt_variant"] for item in summaries if item["prompt_variant"] != "all"}
    ordered_variants = [variant for variant in variant_order if variant in present_variants]
    ordered_variants.extend(sorted(present_variants.difference(ordered_variants)))

    lines = [
        f"# RQ1a {field_title} Local Field Ablation",
        "",
        f"- Suite: `{suite_dir}`",
        f"- Prompt rows: {len({row['prompt_id'] for row in rows})}",
        f"- Result rows: {len(rows)}",
        "- Metrics are tie-aware because hidden-field baselines intentionally create identical candidate text.",
        "- Prompt subset `combined` means all prompt-variant rows pooled together.",
        "",
        "## Summary",
        "",
        "| Retriever | Condition | Prompt Subset | n | Top-1 Tie-Adjusted | MRR Tie-Adjusted | Mean Gold Tie Size | Mean Visible Tokens |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for item in summaries:
        lines.append(
            f"| `{item['retriever']}` | `{item['condition']}` | `{display_prompt_variant(item['prompt_variant'])}` | "
            f"{item['n']} | {item['top1_tie_adjusted']:.3f} | {item['mrr_tie_adjusted']:.3f} | "
            f"{item['mean_gold_tie_size']:.2f} | {item['selector_visible_tokens_mean']:.1f} |"
        )

    by_key = {
        (item["retriever"], item["condition"], item["prompt_variant"]): item
        for item in summaries
    }
    contrast_pairs = [
        (
            "No-I/O context + field",
            "shared_context_no_input_output",
            "shared_context_no_input_output_plus_field",
        ),
        (
            "Identical I/O context + field",
            "shared_context_plus_input_output",
            "shared_context_plus_input_output_field",
        ),
        (
            "Canonical shared context + field",
            "shared_context_only",
            "shared_context_plus_field",
        ),
    ]
    lines.extend(
        [
            "",
            "## Field Lift",
            "",
            "Lift uses tie-adjusted top-1. Each row compares the same prompt set and candidate siblings under two selector-visible representations.",
            "",
            "| Contrast | Retriever | Prompt Subset | Baseline | +Field | Lift |",
            "|---|---|---|---:|---:|---:|",
        ]
    )
    any_lift = False
    for contrast_name, baseline_condition, exposed_condition in contrast_pairs:
        for retriever in sorted({item["retriever"] for item in summaries}):
            for variant in [*ordered_variants, "all"]:
                baseline = by_key.get((retriever, baseline_condition, variant))
                exposed = by_key.get((retriever, exposed_condition, variant))
                if not baseline or not exposed:
                    continue
                any_lift = True
                lift = exposed["top1_tie_adjusted"] - baseline["top1_tie_adjusted"]
                lines.append(
                    f"| {contrast_name} | `{retriever}` | `{display_prompt_variant(variant)}` | {baseline['top1_tie_adjusted']:.3f} | "
                    f"{exposed['top1_tie_adjusted']:.3f} | {lift:+.3f} |"
                )
    if not any_lift:
        lines.append("| No supported contrast in this run |  |  |  |  |  |")

    exposed_conditions = [
        "shared_context_plus_input_output_field",
        "shared_context_no_input_output_plus_field",
        "shared_context_plus_field",
    ]
    miss_condition = next(
        (
            condition
            for condition in exposed_conditions
            if any(row["condition"] == condition for row in rows)
        ),
        "shared_context_plus_field",
    )
    failures = [
        row
        for row in rows
        if row["condition"] == miss_condition
        and row["prompt_variant"] in present_variants
        and row["top1_tie_adjusted"] < 1
    ][:20]
    lines.extend(["", f"## First Field-Exposed Misses (`{miss_condition}`)", ""])
    if not failures:
        lines.append(f"- No misses under `{miss_condition}`.")
    else:
        lines.extend(
            [
                "| Prompt | Retriever | Variant | Gold Rank | Top Candidate | Scores |",
                "|---|---|---|---:|---|---|",
            ]
        )
        for row in failures:
            top_candidate = row["ranking"][0] if row["ranking"] else ""
            score_text = "; ".join(
                f"{skill}={score:.3f}" for skill, score in row["scores"].items()
            )
            lines.append(
                f"| `{row['prompt_id']}` | `{row['retriever']}` | `{row['prompt_variant']}` | "
                f"{row['gold_rank_min']}-{row['gold_rank_max']} | `{top_candidate}` | {score_text} |"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Run local RQ1a field ablation on generated cluster suites.")
    parser.add_argument(
        "--suite-dir",
        type=Path,
        default=root / "rq1a_field_discriminability" / "input_precondition",
        help="RQ1a field suite directory.",
    )
    parser.add_argument("--retrievers", default="tfidf,bm25", help="Comma-separated retrievers: tfidf,bm25,qwen_embedding.")
    parser.add_argument(
        "--conditions",
        default="shared_context_only,field_only,shared_context_plus_field,full_skill_doc",
        help="Comma-separated representation conditions.",
    )
    parser.add_argument(
        "--output-prefix",
        default="rq1a_input_precondition_local_lexical",
        help="Output filename prefix under skill_benchmark/outputs.",
    )
    parser.add_argument("--embedding-provider", default="qwen", choices=sorted(EMBEDDING_PROVIDER_DEFAULTS))
    parser.add_argument("--embedding-base-url")
    parser.add_argument("--embedding-key-env")
    parser.add_argument("--embedding-model")
    parser.add_argument("--embedding-dimensions", type=int)
    parser.add_argument("--embedding-batch-size", type=int)
    parser.add_argument("--cache-dir", default="skill_benchmark/runtime/provider_cache")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()

    suite_dir = args.suite_dir.resolve()
    retrievers = [item.strip() for item in args.retrievers.split(",") if item.strip()]
    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]

    embedding_client = None
    embedding_config: dict[str, Any] | None = None
    if "qwen_embedding" in retrievers:
        load_dotenv(Path(args.dotenv))
        provider_defaults = EMBEDDING_PROVIDER_DEFAULTS[args.embedding_provider]
        embedding_base_url = args.embedding_base_url or provider_defaults["base_url"]
        embedding_key_env = args.embedding_key_env or provider_defaults["key_env"]
        embedding_model = args.embedding_model or provider_defaults["model"]
        embedding_batch_size = args.embedding_batch_size or provider_defaults["batch_size"]
        embedding_key = os.environ.get(embedding_key_env)
        if not embedding_key:
            raise SystemExit(f"Missing {embedding_key_env} for qwen_embedding retriever.")
        embedding_client = OpenAICompatibleEmbeddingClient(
            provider=args.embedding_provider,
            base_url=embedding_base_url,
            api_key=embedding_key,
            model=embedding_model,
            cache_dir=Path(args.cache_dir),
            timeout=args.timeout,
            dimensions=args.embedding_dimensions,
        )
        embedding_config = {
            "embedding_provider": args.embedding_provider,
            "embedding_base_url": embedding_base_url,
            "embedding_model": embedding_model,
            "embedding_batch_size": embedding_batch_size,
            "embedding_dimensions": args.embedding_dimensions,
            "cache_dir": args.cache_dir,
        }
    else:
        embedding_batch_size = args.embedding_batch_size or 10

    rows, summaries = run(
        suite_dir=suite_dir,
        retrievers=retrievers,
        conditions=conditions,
        embedding_client=embedding_client,
        embedding_batch_size=embedding_batch_size,
    )

    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    jsonl_path = output_dir / f"{args.output_prefix}_rows.jsonl"
    md_path = output_dir / f"{args.output_prefix}.md"

    json_path.write_text(
        json.dumps(
            {
                "suite_dir": str(suite_dir),
                "retrievers": retrievers,
                "conditions": conditions,
                "embedding_config": embedding_config,
                "api_usage": {
                    "embedding_api_calls": embedding_client.api_calls if embedding_client else 0,
                    "embedding_cache_hits": embedding_client.cache_hits if embedding_client else 0,
                    "embedding_tokens_approx": embedding_client.tokens_approx if embedding_client else 0,
                },
                "summaries": summaries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    md_path.write_text(render_markdown(suite_dir, rows, summaries), encoding="utf-8")

    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {jsonl_path}")


if __name__ == "__main__":
    main()
