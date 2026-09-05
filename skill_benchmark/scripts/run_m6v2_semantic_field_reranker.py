#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from field_aware_matching import (  # noqa: E402
    BROAD_ROLE_CUES,
    DEPENDENCY_CUES,
    INPUT_CUES,
    OUTPUT_CUES,
    WORKFLOW_CUES,
    extract_request_fields,
    skill_fields,
)
from run_m6v1_field_aware_reranker import guess_failure  # noqa: E402
from run_offline_selectors import evaluate_rows, load_acceptables, load_jsonl, minmax, tokenize  # noqa: E402
from run_provider_selectors import (  # noqa: E402
    EMBEDDING_PROVIDER_DEFAULTS,
    OpenAICompatibleEmbeddingClient,
    approximate_tokens,
    cosine,
    load_dotenv,
    slug,
)


POSITIVE_FIELDS = ["task", "input", "output", "workflow", "dependency"]
FIELD_WEIGHTS = {
    "task": 0.35,
    "input": 0.15,
    "output": 0.25,
    "workflow": 0.15,
    "dependency": 0.10,
}
FIELD_SET_ALIASES = {
    "task": {"task"},
    "task_output": {"task", "output"},
    "task_output_workflow": {"task", "output", "workflow"},
    "semantic_core": {"task", "input", "output", "workflow"},
    "semantic_core_boundary": {"task", "input", "output", "workflow", "boundary"},
    "semantic_all": {"task", "input", "output", "workflow", "dependency", "boundary"},
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_field_set(name: str) -> set[str]:
    if name in FIELD_SET_ALIASES:
        return set(FIELD_SET_ALIASES[name])
    if name.startswith("custom:"):
        fields = {part.strip() for part in name.split(":", 1)[1].split("+") if part.strip()}
        unknown = fields - {"task", "input", "output", "workflow", "dependency", "boundary"}
        if unknown:
            raise ValueError(f"Unknown custom fields: {sorted(unknown)}")
        return fields
    raise ValueError(f"Unknown M6-v2 field set: {name}")


def explain_field_set(name: str) -> str:
    return "+".join(sorted(parse_field_set(name)))


def normalize_source_row(row: dict[str, Any], rerank_candidates: int) -> list[tuple[str, float]]:
    candidates: list[tuple[str, float]] = []
    for item in row.get("ranking", [])[:rerank_candidates]:
        if isinstance(item, dict):
            candidates.append((item["skill"], float(item.get("score", 0.0))))
        else:
            candidates.append((str(item), 0.0))
    return candidates


def candidate_recall_from_rank(rows: list[dict[str, Any]], k: int) -> float:
    if not rows:
        return 0.0
    hits = 0
    for row in rows:
        rank = row.get("gold_first_stage_rank")
        if isinstance(rank, int) and rank <= k:
            hits += 1
    return hits / len(rows)


def compute_decomposition(
    rows: list[dict[str, Any]],
    r1: dict[str, dict[str, Any]],
    acceptable_by_prompt: dict[str, dict[str, set[str]]],
    candidate_budget: int,
) -> dict[str, Any]:
    total = len(rows)
    conditional_total = 0
    conditional_top1 = 0
    conditional_accept_top1 = 0
    reranker_loss = 0
    final_top1 = 0
    non_main_top1 = 0
    first_stage_top1 = 0
    failure_counts: dict[str, int] = {}

    for row in rows:
        gold = row["gold_skill"]
        acceptable = {gold, *acceptable_by_prompt.get(row["prompt_id"], {}).get("acceptable", set())}
        ranking = row.get("ranking", [])
        top = ranking[0]["skill"] if ranking else None
        if row.get("first_stage_top1") == gold:
            first_stage_top1 += 1
        if top == gold:
            final_top1 += 1
        if top and not r1[top].get("is_main_evaluated"):
            non_main_top1 += 1
        if gold in row.get("candidate_names", []):
            conditional_total += 1
            if top == gold:
                conditional_top1 += 1
            elif top in acceptable:
                conditional_accept_top1 += 1
            else:
                reranker_loss += 1
                key = row.get("failure_guess") or "unknown"
                failure_counts[key] = failure_counts.get(key, 0) + 1

    pct = lambda value: round(value / total, 4) if total else 0.0
    cpct = lambda value: round(value / conditional_total, 4) if conditional_total else 0.0
    return {
        "first_stage_top1_accuracy": pct(first_stage_top1),
        "candidate_recall": {
            f"recall@{candidate_budget}": candidate_recall_from_rank(rows, candidate_budget),
        },
        "conditional_gold_in_candidate_count": conditional_total,
        "conditional_reranker_top1": cpct(conditional_top1),
        "conditional_reranker_acceptable_top1": cpct(conditional_top1 + conditional_accept_top1),
        "reranker_loss_count": reranker_loss,
        "reranker_loss_rate_given_gold_in_candidates": cpct(reranker_loss),
        "final_top1_accuracy_check": pct(final_top1),
        "non_main_final_top1_rate": pct(non_main_top1),
        "failure_guess_counts": dict(sorted(failure_counts.items(), key=lambda item: (-item[1], item[0]))),
    }


def split_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    for raw_part in text.splitlines():
        part = raw_part.strip()
        if not part:
            continue
        part = part.lstrip("-*0123456789. )\t").strip()
        if not part:
            continue
        chunks.append(part)
    if chunks:
        return chunks
    stripped = text.strip()
    return [stripped] if stripped else []


def active_fields_for_query(query: str, enabled: set[str], activation_mode: str) -> set[str]:
    if activation_mode == "all_selected":
        return enabled & set(POSITIVE_FIELDS)
    tokens = set(tokenize(query))
    active = {"task"} if "task" in enabled else set()
    if "input" in enabled and tokens & INPUT_CUES:
        active.add("input")
    if "output" in enabled and tokens & OUTPUT_CUES:
        active.add("output")
    if "workflow" in enabled and tokens & WORKFLOW_CUES:
        active.add("workflow")
    if "dependency" in enabled and tokens & DEPENDENCY_CUES:
        active.add("dependency")
    return active


def thresholded(value: float, threshold: float) -> float:
    if value <= threshold:
        return 0.0
    if threshold >= 1.0:
        return 0.0
    return min(1.0, (value - threshold) / (1.0 - threshold))


def aggregate_similarity(
    query_text: str,
    chunks: list[str],
    vectors: dict[str, list[float]],
    aggregation: str,
) -> tuple[float, str | None]:
    if not query_text.strip() or not chunks:
        return 0.0, None
    query_vector = vectors[query_text]
    scored = sorted(
        ((cosine(query_vector, vectors[chunk]), chunk) for chunk in chunks if chunk in vectors),
        key=lambda item: item[0],
        reverse=True,
    )
    if not scored:
        return 0.0, None
    if aggregation == "max" or len(scored) == 1:
        return scored[0]
    if aggregation == "top2_average":
        top = scored[:2]
        return sum(score for score, _ in top) / len(top), top[0][1]
    raise ValueError(f"Unknown aggregation: {aggregation}")


def normalize_weights(active_fields: set[str]) -> dict[str, float]:
    total = sum(FIELD_WEIGHTS[field] for field in active_fields)
    if total <= 0:
        return {}
    return {field: FIELD_WEIGHTS[field] / total for field in active_fields}


def broad_skill_penalty(skill_name: str, query: str, skill_text: str, max_penalty: float) -> float:
    if max_penalty <= 0:
        return 0.0
    skill_terms = tokenize(f"{skill_name.replace('-', ' ')} {skill_text}")
    broad_count = sum(1 for token in skill_terms if token in BROAD_ROLE_CUES)
    if not broad_count:
        return 0.0
    query_terms = set(tokenize(query))
    if query_terms & {"route", "router", "select", "skill", "install", "orchestration", "catalog"}:
        return 0.0
    return min(max_penalty, 0.02 * broad_count)


def collect_candidate_field_chunks(
    source_rows: list[dict[str, Any]],
    field_sets: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
    rerank_candidates: int,
) -> dict[str, dict[str, list[str]]]:
    all_enabled: set[str] = set()
    for field_set in field_sets:
        all_enabled |= parse_field_set(field_set)

    candidate_names = {
        skill
        for row in source_rows
        for skill, _ in normalize_source_row(row, rerank_candidates)
    }
    cache: dict[str, dict[str, list[str]]] = {}
    for skill_name in sorted(candidate_names):
        fields = skill_fields(skill_name, r1, r2, r3)
        cache[skill_name] = {
            field: split_chunks(fields.get(field, ""))
            for field in sorted(all_enabled)
        }
    return cache


def embed_required_texts(
    client: OpenAICompatibleEmbeddingClient,
    source_rows: list[dict[str, Any]],
    field_cache: dict[str, dict[str, list[str]]],
    batch_size: int,
    text_window: int,
) -> dict[str, list[float]]:
    texts: set[str] = set()
    for row in source_rows:
        request = extract_request_fields(row["instruction_text"])
        for value in [
            request.positive,
            request.task,
            request.input,
            request.output,
            request.workflow,
            request.dependency,
            request.exclusions,
        ]:
            if value.strip():
                texts.add(value)
    for by_field in field_cache.values():
        for chunks in by_field.values():
            for chunk in chunks:
                if chunk.strip():
                    texts.add(chunk)

    ordered = sorted(texts)
    all_vectors: list[list[float]] = []
    for start in range(0, len(ordered), text_window):
        window = ordered[start : start + text_window]
        print(f"Embedding/cache window {start + 1}-{start + len(window)} of {len(ordered)} texts...")
        all_vectors.extend(embed_many_with_retry(client, window, batch_size))
    return dict(zip(ordered, all_vectors))


def embed_many_with_retry(
    client: OpenAICompatibleEmbeddingClient,
    texts: list[str],
    batch_size: int,
    retries: int = 2,
) -> list[list[float]]:
    for attempt in range(retries + 1):
        try:
            return client.embed_many(texts, batch_size)
        except RuntimeError as exc:
            if attempt < retries:
                print(f"Embedding provider error; retrying window in {1 + attempt}s: {exc}")
                time.sleep(1 + attempt)
                continue
            if len(texts) <= 1:
                raise
            midpoint = len(texts) // 2
            print(f"Embedding provider error persists; splitting {len(texts)} texts into smaller windows.")
            return embed_many_with_retry(client, texts[:midpoint], batch_size, retries) + embed_many_with_retry(
                client,
                texts[midpoint:],
                batch_size,
                retries,
            )
    raise RuntimeError("Unreachable embedding retry state.")


def query_text_for_field(request: Any, field: str, query_field_mode: str) -> str:
    if query_field_mode == "raw_positive":
        return request.positive if request.positive.strip() else ""
    if query_field_mode == "field_specific":
        if field == "task":
            return request.task if request.task.strip() else request.positive
        value = getattr(request, field, "")
        return value if value.strip() else ""
    raise ValueError(f"Unknown query field mode: {query_field_mode}")


def score_candidate(
    query: str,
    skill_name: str,
    enabled: set[str],
    field_cache: dict[str, dict[str, list[str]]],
    vectors: dict[str, list[float]],
    activation_mode: str,
    query_field_mode: str,
    workflow_aggregation: str,
    boundary_threshold: float,
    boundary_penalty_weight: float,
    exclusion_conflict_weight: float,
    exclusion_alignment_bonus_weight: float,
    broad_penalty_weight: float,
) -> dict[str, Any]:
    request = extract_request_fields(query)
    positive_query = request.positive if request.positive.strip() else query
    active = active_fields_for_query(positive_query, enabled, activation_mode)
    weights = normalize_weights(active)
    candidate_fields = field_cache[skill_name]

    components: dict[str, float] = {}
    best_chunks: dict[str, str | None] = {}
    positive_score = 0.0
    for field in POSITIVE_FIELDS:
        if field not in enabled:
            components[field] = 0.0
            best_chunks[field] = None
            continue
        aggregation = workflow_aggregation if field == "workflow" else "max"
        query_text = query_text_for_field(request, field, query_field_mode)
        score, best_chunk = aggregate_similarity(
            query_text,
            candidate_fields.get(field, []),
            vectors,
            aggregation,
        )
        components[field] = score
        best_chunks[field] = best_chunk
        if field in weights:
            positive_score += weights[field] * score

    boundary_score = 0.0
    boundary_chunk = None
    boundary_penalty = 0.0
    boundary_enabled = "boundary" in enabled
    if boundary_enabled:
        boundary_score, boundary_chunk = aggregate_similarity(
            positive_query,
            candidate_fields.get("boundary", []),
            vectors,
            "max",
        )
        boundary_penalty = boundary_penalty_weight * thresholded(boundary_score, boundary_threshold)

    exclusion_alignment = 0.0
    exclusion_bonus = 0.0
    exclusion_conflict = 0.0
    exclusion_penalty = 0.0
    if boundary_enabled and request.exclusions.strip():
        exclusion_alignment, _ = aggregate_similarity(
            request.exclusions,
            candidate_fields.get("boundary", []),
            vectors,
            "max",
        )
        exclusion_bonus = exclusion_alignment_bonus_weight * thresholded(exclusion_alignment, boundary_threshold)
        positive_chunks: list[str] = []
        for field in POSITIVE_FIELDS:
            positive_chunks.extend(candidate_fields.get(field, []))
        exclusion_conflict, _ = aggregate_similarity(
            request.exclusions,
            positive_chunks,
            vectors,
            "max",
        )
        exclusion_penalty = exclusion_conflict_weight * thresholded(exclusion_conflict, boundary_threshold)

    hierarchy_text = " ".join(candidate_fields.get("task", []))
    broad_penalty = broad_skill_penalty(skill_name, positive_query, hierarchy_text, broad_penalty_weight)
    total_penalty = boundary_penalty + exclusion_penalty + broad_penalty

    return {
        "positive_score": positive_score,
        "components": components,
        "active_fields": sorted(active),
        "field_weights": weights,
        "best_chunks": best_chunks,
        "boundary_score": boundary_score,
        "boundary_best_chunk": boundary_chunk,
        "boundary_penalty": boundary_penalty,
        "exclusion_alignment": exclusion_alignment,
        "exclusion_bonus": exclusion_bonus,
        "exclusion_conflict": exclusion_conflict,
        "exclusion_penalty": exclusion_penalty,
        "broad_penalty": broad_penalty,
        "total_penalty": total_penalty,
        "request_positive": positive_query,
        "request_exclusions": request.exclusions,
    }


def run_field_set(
    source_rows: list[dict[str, Any]],
    field_set_name: str,
    r1: dict[str, dict[str, Any]],
    field_cache: dict[str, dict[str, list[str]]],
    vectors: dict[str, list[float]],
    rerank_candidates: int,
    base_weight: float,
    field_weight: float,
    ranking_limit: int,
    activation_mode: str,
    query_field_mode: str,
    workflow_aggregation: str,
    boundary_threshold: float,
    boundary_penalty_weight: float,
    exclusion_conflict_weight: float,
    exclusion_alignment_bonus_weight: float,
    broad_penalty_weight: float,
) -> list[dict[str, Any]]:
    enabled = parse_field_set(field_set_name)
    output_rows: list[dict[str, Any]] = []
    for source in source_rows:
        query = source["instruction_text"]
        candidates = normalize_source_row(source, rerank_candidates)
        candidate_names = [skill for skill, _ in candidates]
        base_scores = [score for _, score in candidates]
        base_norm = minmax(base_scores)
        semantic_results = [
            score_candidate(
                query=query,
                skill_name=skill,
                enabled=enabled,
                field_cache=field_cache,
                vectors=vectors,
                activation_mode=activation_mode,
                query_field_mode=query_field_mode,
                workflow_aggregation=workflow_aggregation,
                boundary_threshold=boundary_threshold,
                boundary_penalty_weight=boundary_penalty_weight if "boundary" in enabled else 0.0,
                exclusion_conflict_weight=exclusion_conflict_weight if "boundary" in enabled else 0.0,
                exclusion_alignment_bonus_weight=(
                    exclusion_alignment_bonus_weight if "boundary" in enabled else 0.0
                ),
                broad_penalty_weight=broad_penalty_weight,
            )
            for skill in candidate_names
        ]
        positive_scores = [result["positive_score"] for result in semantic_results]
        field_norm = minmax(positive_scores)

        reranked: list[dict[str, Any]] = []
        for index, skill in enumerate(candidate_names):
            result = semantic_results[index]
            final_score = (
                base_weight * base_norm[index]
                + field_weight * field_norm[index]
                + result["exclusion_bonus"]
                - result["total_penalty"]
            )
            reranked.append(
                {
                    "skill": skill,
                    "score": round(final_score, 6),
                    "base_score": round(base_scores[index], 6),
                    "base_norm": round(base_norm[index], 6),
                    "semantic_positive_score": round(positive_scores[index], 6),
                    "semantic_positive_norm": round(field_norm[index], 6),
                    "components": {
                        key: round(value, 6) for key, value in result["components"].items()
                    },
                    "active_fields": result["active_fields"],
                    "field_weights": {
                        key: round(value, 6) for key, value in result["field_weights"].items()
                    },
                    "boundary_score": round(result["boundary_score"], 6),
                    "boundary_penalty": round(result["boundary_penalty"], 6),
                    "exclusion_alignment": round(result["exclusion_alignment"], 6),
                    "exclusion_bonus": round(result["exclusion_bonus"], 6),
                    "exclusion_conflict": round(result["exclusion_conflict"], 6),
                    "exclusion_penalty": round(result["exclusion_penalty"], 6),
                    "broad_penalty": round(result["broad_penalty"], 6),
                    "total_penalty": round(result["total_penalty"], 6),
                }
            )
        reranked.sort(key=lambda item: (-item["score"], item["skill"]))

        row = {
            "prompt_id": source["prompt_id"],
            "family": source["family"],
            "gold_skill": source["gold_skill"],
            "closest_alternatives": source.get("closest_alternatives", []),
            "instruction_text": query,
            "field_set": field_set_name,
            "field_set_groups": explain_field_set(field_set_name),
            "activation_mode": activation_mode,
            "query_field_mode": query_field_mode,
            "candidate_names": candidate_names,
            "first_stage_ranking": candidate_names,
            "first_stage_top1": source.get("first_stage_top1") or (candidate_names[0] if candidate_names else None),
            "gold_first_stage_rank": source.get("gold_first_stage_rank"),
            "ranking": reranked[:ranking_limit],
            "candidate_count": min(rerank_candidates, len(candidate_names)),
        }
        row["gold_final_rank"] = next(
            (index + 1 for index, item in enumerate(row["ranking"]) if item["skill"] == row["gold_skill"]),
            None,
        )
        row["failure_guess"] = guess_failure(row)
        output_rows.append(row)
    return output_rows


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# M6-v2 Semantic Field Rerank From Existing First-Stage Results",
        "",
        "This report applies a no-rewrite semantic field-aware reranker to a fixed first-stage candidate set. The raw request is embedded and compared against selector-visible skill fields; the method does not invent missing procedure steps or rewrite the user intent.",
        "",
        "## Configuration",
        "",
        f"- Source result: `{report['source_result']}`",
        f"- Source method: `{report.get('source_method', '')}`",
        f"- Prompt count: {report['prompt_count']}",
        f"- Skill count: {report['skill_count']}",
        f"- Candidate budget: {report['rerank_candidates']}",
        f"- Embedding provider/model: `{report['embedding_provider']}` / `{report['embedding_model']}`",
        f"- Activation mode: `{report['activation_mode']}`",
        f"- Query field mode: `{report['query_field_mode']}`",
        f"- Workflow aggregation: `{report['workflow_aggregation']}`",
        f"- Score blend: {report['base_weight']} first-stage + {report['field_weight']} semantic-field",
        "",
        "## API Usage Estimate",
        "",
        f"- Embedding API calls made in this run: {report['api_usage']['embedding_api_calls']}",
        f"- Embedding cache hits: {report['api_usage']['embedding_cache_hits']}",
        f"- Approx uncached embedding input tokens: {report['api_usage']['embedding_tokens_approx']}",
        f"- Unique embedded texts in method input: {report['api_usage']['unique_embedded_texts']}",
        "",
        "## Summary",
        "",
        "| Field set | Fields | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Candidate R@K | Conditional top-1 | Reranker loss | Non-main top-1 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report["summary"]:
        metrics = item["metrics"]
        decomp = item["decomposition"]
        recall_key = f"recall@{report['rerank_candidates']}"
        lines.append(
            f"| `{item['field_set']}` | {item['field_set_groups']} | "
            f"{metrics['top1_accuracy']:.1%} | {metrics['acceptable_top1_accuracy']:.1%} | "
            f"{metrics['top5_recall']:.1%} | {metrics['acceptable_top5_recall']:.1%} | "
            f"{metrics['mrr']:.3f} | {decomp['candidate_recall'][recall_key]:.1%} | "
            f"{decomp['conditional_reranker_top1']:.1%} | "
            f"{decomp['reranker_loss_rate_given_gold_in_candidates']:.1%} | "
            f"{metrics['non_main_top1_rate']:.1%} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply no-rewrite M6-v2 semantic field reranking.")
    parser.add_argument("--source-json", required=True)
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--acceptable-alternatives", default="")
    parser.add_argument(
        "--field-sets",
        default="task,task_output_workflow,semantic_core,semantic_core_boundary,semantic_all",
    )
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--base-weight", type=float, default=0.70)
    parser.add_argument("--field-weight", type=float, default=0.30)
    parser.add_argument("--ranking-limit", type=int, default=20)
    parser.add_argument("--activation-mode", choices=["cue_gated", "all_selected"], default="cue_gated")
    parser.add_argument("--query-field-mode", choices=["raw_positive", "field_specific"], default="raw_positive")
    parser.add_argument("--workflow-aggregation", choices=["max", "top2_average"], default="top2_average")
    parser.add_argument("--boundary-threshold", type=float, default=0.45)
    parser.add_argument("--boundary-penalty-weight", type=float, default=0.18)
    parser.add_argument("--exclusion-conflict-weight", type=float, default=0.16)
    parser.add_argument("--exclusion-alignment-bonus-weight", type=float, default=0.08)
    parser.add_argument("--broad-penalty-weight", type=float, default=0.06)
    parser.add_argument("--embedding-provider", default="qwen", choices=sorted(EMBEDDING_PROVIDER_DEFAULTS))
    parser.add_argument("--embedding-base-url")
    parser.add_argument("--embedding-key-env")
    parser.add_argument("--embedding-model")
    parser.add_argument("--embedding-dimensions", type=int)
    parser.add_argument("--embedding-batch-size", type=int)
    parser.add_argument("--embedding-text-window", type=int, default=500)
    parser.add_argument("--cache-dir", default="skill_benchmark/runtime/provider_cache")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--max-prompts", type=int)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))
    provider_defaults = EMBEDDING_PROVIDER_DEFAULTS[args.embedding_provider]
    embedding_base_url = args.embedding_base_url or provider_defaults["base_url"]
    embedding_key_env = args.embedding_key_env or provider_defaults["key_env"]
    embedding_model = args.embedding_model or provider_defaults["model"]
    embedding_batch_size = args.embedding_batch_size or provider_defaults["batch_size"]
    embedding_key = os.environ.get(embedding_key_env)
    if not embedding_key:
        raise SystemExit(f"Missing {embedding_key_env}; pass --dotenv .env or export the key.")

    source = load_json(Path(args.source_json))
    source_rows = source["results"]
    if args.max_prompts:
        source_rows = source_rows[: args.max_prompts]
    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    acceptable_path = Path(args.acceptable_alternatives) if args.acceptable_alternatives else None
    acceptable_by_prompt = load_acceptables(acceptable_path)
    field_sets = [part.strip() for part in args.field_sets.split(",") if part.strip()]

    embedding_client = OpenAICompatibleEmbeddingClient(
        provider=args.embedding_provider,
        base_url=embedding_base_url,
        api_key=embedding_key,
        model=embedding_model,
        cache_dir=Path(args.cache_dir),
        timeout=args.timeout,
        dimensions=args.embedding_dimensions,
    )

    start = time.perf_counter()
    field_cache = collect_candidate_field_chunks(
        source_rows=source_rows,
        field_sets=field_sets,
        r1=r1,
        r2=r2,
        r3=r3,
        rerank_candidates=args.rerank_candidates,
    )
    vectors = embed_required_texts(
        embedding_client,
        source_rows,
        field_cache,
        embedding_batch_size,
        args.embedding_text_window,
    )

    report: dict[str, Any] = {
        "method_id": "M6-v2-semantic-field",
        "source_result": args.source_json,
        "source_method": f"{source.get('embedding_model', '')} + embedding-only top-{args.rerank_candidates}",
        "prompt_count": len(source_rows),
        "skill_count": source.get("metrics", {}).get("scale_skill_count"),
        "source_metrics": source.get("metrics", {}),
        "rerank_candidates": args.rerank_candidates,
        "base_weight": args.base_weight,
        "field_weight": args.field_weight,
        "ranking_limit": args.ranking_limit,
        "activation_mode": args.activation_mode,
        "query_field_mode": args.query_field_mode,
        "workflow_aggregation": args.workflow_aggregation,
        "boundary_threshold": args.boundary_threshold,
        "boundary_penalty_weight": args.boundary_penalty_weight,
        "exclusion_conflict_weight": args.exclusion_conflict_weight,
        "exclusion_alignment_bonus_weight": args.exclusion_alignment_bonus_weight,
        "broad_penalty_weight": args.broad_penalty_weight,
        "embedding_provider": args.embedding_provider,
        "embedding_base_url": embedding_base_url,
        "embedding_model": embedding_model,
        "embedding_cache_namespace": f"embeddings/{slug(args.embedding_provider)}/{slug(embedding_model)}",
        "summary": [],
        "results": {},
    }

    for field_set in field_sets:
        rows = run_field_set(
            source_rows=source_rows,
            field_set_name=field_set,
            r1=r1,
            field_cache=field_cache,
            vectors=vectors,
            rerank_candidates=args.rerank_candidates,
            base_weight=args.base_weight,
            field_weight=args.field_weight,
            ranking_limit=args.ranking_limit,
            activation_mode=args.activation_mode,
            query_field_mode=args.query_field_mode,
            workflow_aggregation=args.workflow_aggregation,
            boundary_threshold=args.boundary_threshold,
            boundary_penalty_weight=args.boundary_penalty_weight,
            exclusion_conflict_weight=args.exclusion_conflict_weight,
            exclusion_alignment_bonus_weight=args.exclusion_alignment_bonus_weight,
            broad_penalty_weight=args.broad_penalty_weight,
        )
        selector_visible_tokens = source.get("metrics", {}).get("selector_visible_tokens_approx", 0)
        selector_visible_tokens += sum(approximate_tokens(text) for text in vectors)
        metrics = evaluate_rows(rows, r1, int(report["skill_count"] or 0), selector_visible_tokens, acceptable_by_prompt)
        decomp = compute_decomposition(rows, r1, acceptable_by_prompt, args.rerank_candidates)
        key = f"m6v2_semantic_field::{field_set}"
        report["results"][key] = rows
        report["summary"].append(
            {
                "field_set": field_set,
                "field_set_groups": explain_field_set(field_set),
                "result_key": key,
                "metrics": metrics,
                "decomposition": decomp,
            }
        )

    report["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 2)
    report["api_usage"] = {
        "embedding_api_calls": embedding_client.api_calls,
        "embedding_cache_hits": embedding_client.cache_hits,
        "embedding_tokens_approx": embedding_client.tokens_approx,
        "unique_embedded_texts": len(vectors),
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    for item in report["summary"]:
        metrics = item["metrics"]
        decomp = item["decomposition"]
        recall_key = f"recall@{args.rerank_candidates}"
        print(
            f"{Path(args.source_json).stem}/{item['field_set']}: "
            f"top1={metrics['top1_accuracy']:.1%}, "
            f"accept={metrics['acceptable_top1_accuracy']:.1%}, "
            f"top5={metrics['top5_recall']:.1%}, "
            f"mrr={metrics['mrr']:.3f}, "
            f"cand={decomp['candidate_recall'][recall_key]:.1%}, "
            f"cond={decomp['conditional_reranker_top1']:.1%}"
        )


if __name__ == "__main__":
    main()
