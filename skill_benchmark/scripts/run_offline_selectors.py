#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "about",
    "after",
    "all",
    "already",
    "also",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "before",
    "between",
    "by",
    "can",
    "could",
    "do",
    "does",
    "doing",
    "for",
    "from",
    "has",
    "have",
    "help",
    "here",
    "how",
    "if",
    "in",
    "include",
    "into",
    "is",
    "it",
    "its",
    "keep",
    "main",
    "make",
    "me",
    "more",
    "my",
    "need",
    "needs",
    "not",
    "of",
    "on",
    "one",
    "only",
    "or",
    "our",
    "out",
    "please",
    "rather",
    "really",
    "same",
    "should",
    "so",
    "source",
    "that",
    "the",
    "their",
    "then",
    "there",
    "this",
    "to",
    "up",
    "use",
    "usable",
    "using",
    "want",
    "what",
    "when",
    "where",
    "which",
    "while",
    "with",
    "without",
    "you",
}


ALIASES = {
    "summarise": "summary",
    "summarises": "summary",
    "summarised": "summary",
    "summarising": "summary",
    "summarize": "summary",
    "summarizes": "summary",
    "summarized": "summary",
    "summarizing": "summary",
    "summary": "summary",
    "summaries": "summary",
    "analyse": "analysis",
    "analyses": "analysis",
    "analysing": "analysis",
    "analyze": "analysis",
    "analyzing": "analysis",
    "review": "review",
    "reviewing": "review",
    "reviewed": "review",
    "rewrite": "rewrite",
    "rewriting": "rewrite",
    "rewritten": "rewrite",
    "normalise": "normalize",
    "normalising": "normalize",
    "normalised": "normalize",
    "normalize": "normalize",
    "normalizing": "normalize",
    "convert": "convert",
    "converting": "convert",
    "converted": "convert",
    "conversion": "convert",
    "extract": "extract",
    "extracting": "extract",
    "extraction": "extract",
    "grounding": "ground",
    "grounded": "ground",
    "ground": "ground",
    "debug": "debug",
    "debugging": "debug",
    "test": "test",
    "testing": "test",
    "polish": "polish",
    "polished": "polish",
    "polishing": "polish",
    "refine": "refine",
    "refined": "refine",
    "refining": "refine",
    "draft": "draft",
    "drafting": "draft",
    "reply": "reply",
    "response": "reply",
    "respond": "reply",
    "diagnosis": "diagnose",
    "diagnose": "diagnose",
    "diagnosing": "diagnose",
    "cause": "cause",
    "causal": "cause",
    "model": "model",
    "modeling": "model",
    "modeler": "model",
}


METHODS = {
    "m1_bm25_flat",
    "m1_tfidf_flat",
    "m2a_minilm_description",
    "m2b_minilm_full_skill",
    "m3_tfidf_schema",
    "m3_minilm_schema",
    "m6_bm25_schema_rerank",
    "m6_tfidf_schema_rerank",
    "m6_minilm_full_schema_rerank",
}

RERANK_METHOD_BASE = {
    "m6_bm25_schema_rerank": "m1_bm25_flat",
    "m6_tfidf_schema_rerank": "m1_tfidf_flat",
    "m6_minilm_full_schema_rerank": "m2b_minilm_full_skill",
}


def load_acceptables(path: Path | None) -> dict[str, dict[str, set[str]]]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    output: dict[str, dict[str, set[str]]] = {}
    for prompt_id, row in data.items():
        output[prompt_id] = {
            "acceptable": set(row.get("acceptable", [])),
            "borderline": set(row.get("borderline", [])),
        }
    return output


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_prompts(path_glob: str) -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    for path_string in sorted(glob.glob(path_glob)):
        path = Path(path_string)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a JSON array")
        for row in data:
            row = dict(row)
            row["_source_file"] = str(path)
            prompts.append(row)
    return prompts


def instruction_text(prompt: str) -> str:
    text = prompt
    for marker in ["Source A:", "Source:", "Here is the source:", "Text:"]:
        if marker in text:
            text = text.split(marker, 1)[0]
    if ":" in text:
        before, after = text.split(":", 1)
        after_words = re.findall(r"\b\w+\b", after)
        before_words = re.findall(r"\b\w+\b", before)
        if len(after_words) >= 45 and len(before_words) >= 6:
            text = before
    text = re.sub(r"`/workspace/fixtures/([^`]+)`", lambda match: match.group(1).split("/")[-1], text)
    text = re.sub(r"/workspace/fixtures/\S+", lambda match: match.group(0).split("/")[-1], text)
    return text.strip()


def normalize_token(token: str) -> str:
    token = token.lower().strip("_-'")
    token = ALIASES.get(token, token)
    if len(token) > 5 and token.endswith("ing"):
        token = token[:-3]
    elif len(token) > 4 and token.endswith("ed"):
        token = token[:-2]
    elif len(token) > 4 and token.endswith("s"):
        token = token[:-1]
    return ALIASES.get(token, token)


def tokenize(text: str) -> list[str]:
    output: list[str] = []
    for raw in re.findall(r"[a-zA-Z][a-zA-Z0-9_'-]*", text.lower()):
        token = normalize_token(raw)
        if len(token) < 3 or token in STOPWORDS:
            continue
        output.append(token)
    return output


def approximate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def find_skill_files(skills_root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in sorted(skills_root.glob("*/*/SKILL.md")):
        mapping[path.parent.name] = path
    return mapping


def load_full_skill_texts(skills_root: Path, skill_names: list[str]) -> dict[str, str]:
    files = find_skill_files(skills_root)
    full: dict[str, str] = {}
    for skill in skill_names:
        path = files.get(skill)
        if path and path.exists():
            full[skill] = path.read_text(encoding="utf-8")
    return full


def parse_methods(raw: str) -> list[str]:
    if raw == "all":
        return [
            "m1_bm25_flat",
            "m1_tfidf_flat",
            "m2a_minilm_description",
            "m2b_minilm_full_skill",
            "m3_tfidf_schema",
            "m3_minilm_schema",
            "m6_bm25_schema_rerank",
            "m6_tfidf_schema_rerank",
            "m6_minilm_full_schema_rerank",
        ]
    methods = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = sorted(set(methods) - METHODS)
    if unknown:
        raise ValueError(f"Unknown methods: {unknown}")
    return methods


def parse_scales(raw: str) -> list[str]:
    if raw == "all":
        return ["core", "current_full"]
    scales = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = sorted(set(scales) - {"core", "current_full"})
    if unknown:
        raise ValueError(f"Unknown scales: {unknown}")
    return scales


def build_scale_skill_names(scale: str, r1_rows: list[dict[str, Any]]) -> list[str]:
    if scale == "core":
        return sorted(row["name"] for row in r1_rows if row.get("is_main_evaluated"))
    if scale == "current_full":
        return sorted(row["name"] for row in r1_rows)
    raise ValueError(f"Unknown scale: {scale}")


def rank_scores(skill_names: list[str], scores: list[float]) -> list[tuple[str, float]]:
    return sorted(zip(skill_names, scores), key=lambda item: (-item[1], item[0]))


def counter_cosine(left: list[str], right: list[str]) -> float:
    if not left or not right:
        return 0.0
    left_counts = Counter(left)
    right_counts = Counter(right)
    shared = set(left_counts) & set(right_counts)
    numerator = sum(left_counts[token] * right_counts[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def field_text(row: dict[str, Any], *keys: str) -> str:
    parts: list[str] = []
    for key in keys:
        value = row.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif value:
            parts.append(str(value))
    return "\n".join(parts)


def schema_pair_score(
    query: str,
    skill_name: str,
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
) -> float:
    query_terms = tokenize(query)
    r1_row = r1[skill_name]
    r2_row = r2[skill_name]
    r3_row = r3.get(skill_name, {})

    field_weights = [
        (0.08, skill_name.replace("-", " ")),
        (0.20, field_text(r1_row, "description")),
        (0.30, field_text(r2_row, "use_when")),
        (0.22, field_text(r2_row, "output_shape")),
        (0.10, field_text(r2_row, "preconditions")),
        (0.06, field_text(r2_row, "workflow")),
        (0.04, field_text(r3_row, "dependency_profile", "external_dependencies", "resource_signals")),
    ]
    raw_score = 0.0
    for weight, text in field_weights:
        raw_score += weight * counter_cosine(query_terms, tokenize(text))

    not_for_score = counter_cosine(query_terms, tokenize(field_text(r2_row, "not_for")))
    return max(0.0, raw_score - 0.12 * not_for_score)


def minmax(values: list[float]) -> list[float]:
    if not values:
        return []
    low = min(values)
    high = max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def bm25_scores(query: str, docs: list[str]) -> list[float]:
    query_terms = tokenize(query)
    doc_terms = [tokenize(doc) for doc in docs]
    doc_lens = [len(terms) for terms in doc_terms]
    avg_len = sum(doc_lens) / len(doc_lens) if doc_lens else 0.0
    df: Counter[str] = Counter()
    for terms in doc_terms:
        df.update(set(terms))
    n_docs = len(docs)
    k1 = 1.5
    b = 0.75
    scores: list[float] = []
    for terms, doc_len in zip(doc_terms, doc_lens):
        tf = Counter(terms)
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = math.log(1 + (n_docs - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf[term] + k1 * (1 - b + b * (doc_len / avg_len if avg_len else 0))
            score += idf * (tf[term] * (k1 + 1)) / denom
        scores.append(score)
    return scores


class TfIdfScorer:
    def __init__(self, docs: list[str]) -> None:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
        except Exception as exc:  # pragma: no cover - fallback for missing optional dependency
            raise RuntimeError("scikit-learn is required for TF-IDF selectors") from exc
        self._cosine_similarity = cosine_similarity
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        self.doc_matrix = self.vectorizer.fit_transform(docs)

    def scores(self, query: str) -> list[float]:
        query_matrix = self.vectorizer.transform([query])
        return self._cosine_similarity(query_matrix, self.doc_matrix)[0].tolist()


class MiniLmScorer:
    def __init__(self, docs: list[str], model_name: str) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("sentence-transformers is required for MiniLM selectors") from exc
        try:
            self.model = SentenceTransformer(model_name, local_files_only=True)
        except TypeError:
            self.model = SentenceTransformer(model_name)
        self.doc_embeddings = self.model.encode(docs, normalize_embeddings=True, show_progress_bar=False)

    def scores(self, query: str) -> list[float]:
        query_embedding = self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)
        values = query_embedding @ self.doc_embeddings.T
        return values[0].tolist()


def docs_for_method(
    method: str,
    skill_names: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    full_skill_texts: dict[str, str],
) -> list[str]:
    if method in {"m1_bm25_flat", "m1_tfidf_flat", "m2a_minilm_description"}:
        return [r1[name]["text"] for name in skill_names]
    if method == "m2b_minilm_full_skill":
        return [full_skill_texts.get(name) or r2[name]["text"] for name in skill_names]
    if method in {"m3_tfidf_schema", "m3_minilm_schema"}:
        return [r2[name]["text"] for name in skill_names]
    if method in RERANK_METHOD_BASE:
        return docs_for_method(RERANK_METHOD_BASE[method], skill_names, r1, r2, full_skill_texts)
    raise ValueError(f"Unknown method: {method}")


def run_selector(
    method: str,
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    docs: list[str],
    model_name: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    start = time.perf_counter()
    scorer: Any = None
    if method == "m1_tfidf_flat" or method == "m3_tfidf_schema":
        scorer = TfIdfScorer(docs)
    elif method in {"m2a_minilm_description", "m2b_minilm_full_skill", "m3_minilm_schema"}:
        scorer = MiniLmScorer(docs, model_name)

    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        if method == "m1_bm25_flat":
            scores = bm25_scores(query, docs)
        else:
            scores = scorer.scores(query)
        ranked = rank_scores(skill_names, scores)
        rows.append(
            {
                "prompt_id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": prompt["gold_skill"],
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "instruction_text": query,
                "ranking": [{"skill": skill, "score": round(score, 6)} for skill, score in ranked[:20]],
            }
        )
    elapsed_ms = (time.perf_counter() - start) * 1000
    return rows, {"elapsed_ms": round(elapsed_ms, 2)}


def run_hybrid_rerank_selector(
    method: str,
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
    full_skill_texts: dict[str, str],
    model_name: str,
    rerank_candidates: int,
    base_weight: float,
    schema_weight: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    start = time.perf_counter()
    base_method = RERANK_METHOD_BASE[method]
    base_docs = docs_for_method(base_method, skill_names, r1, r2, full_skill_texts)
    scorer: Any = None
    if base_method in {"m1_tfidf_flat", "m3_tfidf_schema"}:
        scorer = TfIdfScorer(base_docs)
    elif base_method in {"m2a_minilm_description", "m2b_minilm_full_skill", "m3_minilm_schema"}:
        scorer = MiniLmScorer(base_docs, model_name)

    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        if base_method == "m1_bm25_flat":
            base_scores = bm25_scores(query, base_docs)
        else:
            base_scores = scorer.scores(query)
        first_stage = rank_scores(skill_names, base_scores)
        candidates = first_stage[: min(rerank_candidates, len(first_stage))]
        candidate_names = [skill for skill, _ in candidates]
        candidate_base_scores = [score for _, score in candidates]
        candidate_schema_scores = [
            schema_pair_score(query, skill, r1, r2, r3) for skill in candidate_names
        ]
        base_norm = minmax(candidate_base_scores)
        schema_norm = minmax(candidate_schema_scores)

        reranked: list[tuple[str, float, float, float]] = []
        for index, skill in enumerate(candidate_names):
            final_score = base_weight * base_norm[index] + schema_weight * schema_norm[index]
            reranked.append((skill, final_score, candidate_base_scores[index], candidate_schema_scores[index]))
        reranked.sort(key=lambda item: (-item[1], item[0]))

        rows.append(
            {
                "prompt_id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": prompt["gold_skill"],
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "instruction_text": query,
                "ranking": [
                    {
                        "skill": skill,
                        "score": round(final_score, 6),
                        "base_score": round(base_score, 6),
                        "schema_score": round(schema_score, 6),
                    }
                    for skill, final_score, base_score, schema_score in reranked[:20]
                ],
            }
        )
    elapsed_ms = (time.perf_counter() - start) * 1000
    return rows, {
        "elapsed_ms": round(elapsed_ms, 2),
        "first_stage": base_method,
        "rerank_candidates": rerank_candidates,
        "base_weight": base_weight,
        "schema_weight": schema_weight,
    }


def evaluate_rows(
    rows: list[dict[str, Any]],
    r1: dict[str, dict[str, Any]],
    scale_skill_count: int,
    selector_visible_tokens: int,
    acceptable_by_prompt: dict[str, dict[str, set[str]]],
) -> dict[str, Any]:
    total = len(rows)
    top1_hits = 0
    acceptable_top1_hits = 0
    borderline_top1_hits = 0
    top3_hits = 0
    acceptable_top3_hits = 0
    top5_hits = 0
    acceptable_top5_hits = 0
    reciprocal_sum = 0.0
    acceptable_reciprocal_sum = 0.0
    ranks: list[int] = []
    acceptable_ranks: list[int] = []
    listed_alt_top1 = 0
    background_top1 = 0
    public_top1 = 0
    non_main_top1 = 0
    wrong_top1 = 0
    unacceptable_top1 = 0
    by_family: dict[str, Counter[str]] = defaultdict(Counter)
    confusion: Counter[str] = Counter()
    unacceptable_confusion: Counter[str] = Counter()

    for row in rows:
        gold = row["gold_skill"]
        ranking = [item["skill"] for item in row["ranking"]]
        top1 = ranking[0] if ranking else None
        rank = ranking.index(gold) + 1 if gold in ranking else None
        prompt_acceptables = acceptable_by_prompt.get(row["prompt_id"], {})
        acceptable_skills = {gold, *prompt_acceptables.get("acceptable", set())}
        borderline_skills = prompt_acceptables.get("borderline", set())
        acceptable_rank = next(
            (index + 1 for index, skill in enumerate(ranking) if skill in acceptable_skills),
            None,
        )

        if top1 == gold:
            top1_hits += 1
        else:
            wrong_top1 += 1
            confusion[f"{gold} -> {top1}"] += 1
        if top1 in acceptable_skills:
            acceptable_top1_hits += 1
        elif top1 in borderline_skills:
            borderline_top1_hits += 1
        else:
            unacceptable_top1 += 1
            unacceptable_confusion[f"{gold} -> {top1}"] += 1
        if gold in ranking[:3]:
            top3_hits += 1
        if any(skill in acceptable_skills for skill in ranking[:3]):
            acceptable_top3_hits += 1
        if gold in ranking[:5]:
            top5_hits += 1
        if any(skill in acceptable_skills for skill in ranking[:5]):
            acceptable_top5_hits += 1
        if rank:
            ranks.append(rank)
            reciprocal_sum += 1 / rank
        if acceptable_rank:
            acceptable_ranks.append(acceptable_rank)
            acceptable_reciprocal_sum += 1 / acceptable_rank
        if top1 in row.get("closest_alternatives", []):
            listed_alt_top1 += 1
        if top1:
            top1_row = r1[top1]
            family = top1_row.get("family")
            if family == "background_scale":
                background_top1 += 1
            if family == "public_imported_background":
                public_top1 += 1
            if not top1_row.get("is_main_evaluated"):
                non_main_top1 += 1

        family_counter = by_family[row["family"]]
        family_counter["total"] += 1
        if top1 == gold:
            family_counter["top1"] += 1
        if top1 in acceptable_skills:
            family_counter["acceptable_top1"] += 1
        if gold in ranking[:3]:
            family_counter["top3"] += 1
        if any(skill in acceptable_skills for skill in ranking[:3]):
            family_counter["acceptable_top3"] += 1
        if gold in ranking[:5]:
            family_counter["top5"] += 1
        if any(skill in acceptable_skills for skill in ranking[:5]):
            family_counter["acceptable_top5"] += 1

    def pct(value: int) -> float:
        return round(value / total, 4) if total else 0.0

    return {
        "total_prompts": total,
        "scale_skill_count": scale_skill_count,
        "selector_visible_tokens_approx": selector_visible_tokens,
        "top1_accuracy": pct(top1_hits),
        "top1_hits": top1_hits,
        "acceptable_top1_accuracy": pct(acceptable_top1_hits),
        "acceptable_top1_hits": acceptable_top1_hits,
        "borderline_top1": borderline_top1_hits,
        "borderline_top1_rate": pct(borderline_top1_hits),
        "top3_recall": pct(top3_hits),
        "top3_hits": top3_hits,
        "acceptable_top3_recall": pct(acceptable_top3_hits),
        "acceptable_top3_hits": acceptable_top3_hits,
        "top5_recall": pct(top5_hits),
        "top5_hits": top5_hits,
        "acceptable_top5_recall": pct(acceptable_top5_hits),
        "acceptable_top5_hits": acceptable_top5_hits,
        "mrr": round(reciprocal_sum / total, 4) if total else 0.0,
        "acceptable_mrr": round(acceptable_reciprocal_sum / total, 4) if total else 0.0,
        "mean_gold_rank": round(sum(ranks) / len(ranks), 2) if ranks else None,
        "mean_acceptable_rank": round(sum(acceptable_ranks) / len(acceptable_ranks), 2) if acceptable_ranks else None,
        "wrong_top1": wrong_top1,
        "unacceptable_top1": unacceptable_top1,
        "unacceptable_top1_rate": pct(unacceptable_top1),
        "listed_alternative_top1": listed_alt_top1,
        "listed_alternative_top1_rate": pct(listed_alt_top1),
        "non_main_top1": non_main_top1,
        "non_main_top1_rate": pct(non_main_top1),
        "background_top1": background_top1,
        "background_top1_rate": pct(background_top1),
        "public_import_top1": public_top1,
        "public_import_top1_rate": pct(public_top1),
        "by_family": {
            family: {
                "total": counts["total"],
                "top1_accuracy": round(counts["top1"] / counts["total"], 4),
                "acceptable_top1_accuracy": round(counts["acceptable_top1"] / counts["total"], 4),
                "top3_recall": round(counts["top3"] / counts["total"], 4),
                "acceptable_top3_recall": round(counts["acceptable_top3"] / counts["total"], 4),
                "top5_recall": round(counts["top5"] / counts["total"], 4),
                "acceptable_top5_recall": round(counts["acceptable_top5"] / counts["total"], 4),
            }
            for family, counts in sorted(by_family.items())
        },
        "top_confusions": [{"pair": pair, "count": count} for pair, count in confusion.most_common(20)],
        "top_unacceptable_confusions": [
            {"pair": pair, "count": count} for pair, count in unacceptable_confusion.most_common(20)
        ],
    }


def parse_selected_skills(raw: str) -> list[str]:
    if not raw:
        return []
    return [part for part in raw.split("|") if part]


def load_m0_manifest(path: Path, r1: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    total = len(rows)
    if not total:
        return {"available": True, "total_runs": 0}
    top1 = 0
    any_hit = 0
    no_selection = 0
    docs_loaded_total = 0
    by_prompt: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_prompt[row["prompt_id"]].append(row)
        selected = parse_selected_skills(row.get("selected_skills", ""))
        docs_loaded_total += len(selected)
        gold = row.get("gold_skill")
        if not selected:
            no_selection += 1
        if selected and selected[0] == gold:
            top1 += 1
        if gold in selected:
            any_hit += 1
    return {
        "available": True,
        "source": str(path),
        "total_runs": total,
        "unique_prompts": len(by_prompt),
        "top1_accuracy": round(top1 / total, 4),
        "any_hit": round(any_hit / total, 4),
        "no_explicit_skill_rate": round(no_selection / total, 4),
        "mean_full_docs_loaded": round(docs_loaded_total / total, 2),
        "note": "Loaded from the supplied M0 manifest. Use the dedicated M0 report for no-skill and prompt-level failure breakdown.",
    }


def summarize_pressure(summary_rows: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for row in summary_rows:
        metrics = row["metrics"]
        method = row["method"]
        scale = row["scale"]
        top1 = metrics["top1_accuracy"]
        top5 = metrics["top5_recall"]
        bg = metrics["non_main_top1_rate"]
        if top1 >= 0.9 and top5 >= 0.98:
            label = "possibly too easy"
        elif top1 < 0.3 and top5 < 0.6:
            label = "possibly ambiguous or too noisy"
        else:
            label = "useful pressure"
        if scale == "current_full" and bg == 0 and metrics["wrong_top1"] > 0:
            label += "; background distractors not yet competing"
        lines.append(f"- `{method}` on `{scale}`: {label}")
    return lines


def summarize_scale_sensitivity(summary_rows: list[dict[str, Any]]) -> list[str]:
    by_method_scale = {(row["method"], row["scale"]): row for row in summary_rows}
    methods = sorted({row["method"] for row in summary_rows})
    lines = [
        "| Method | Core Top-1 | Full Top-1 | Full Accept Top-1 | Top-1 Delta | Core Top-5 | Full Top-5 | Full Accept Top-5 | Top-5 Delta | Core MRR | Full MRR | Full Accept MRR | Non-Core Top-1 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method in methods:
        core = by_method_scale.get((method, "core"))
        full = by_method_scale.get((method, "current_full"))
        if not core or not full:
            continue
        core_metrics = core["metrics"]
        full_metrics = full["metrics"]
        top1_delta = full_metrics["top1_accuracy"] - core_metrics["top1_accuracy"]
        top5_delta = full_metrics["top5_recall"] - core_metrics["top5_recall"]
        mrr_delta = full_metrics["mrr"] - core_metrics["mrr"]
        lines.append(
            f"| `{method}` | {core_metrics['top1_accuracy']:.1%} | {full_metrics['top1_accuracy']:.1%} | "
            f"{full_metrics['acceptable_top1_accuracy']:.1%} | {top1_delta:+.1%} | "
            f"{core_metrics['top5_recall']:.1%} | {full_metrics['top5_recall']:.1%} | "
            f"{full_metrics['acceptable_top5_recall']:.1%} | {top5_delta:+.1%} | "
            f"{core_metrics['mrr']:.3f} | {full_metrics['mrr']:.3f} | "
            f"{full_metrics['acceptable_mrr']:.3f} | {full_metrics['non_main_top1_rate']:.1%} |"
        )
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Offline Selector Evaluation Report")
    lines.append("")
    lines.append("This report evaluates deterministic selector baselines over the benchmark prompts. It also records the M0 progressive-disclosure trace schema so later agent runs can be compared with the same metrics.")
    lines.append("")
    lines.append("## Scale Regimes")
    lines.append("")
    for scale, meta in report["scales"].items():
        lines.append(
            f"- `{scale}`: {meta['skill_count']} skills, approx selector-visible tokens per method vary by representation."
        )
    lines.append("")
    lines.append("## Method Summary")
    lines.append("")
    lines.append("| Method | Scale | Skills | Visible Tokens | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 | MRR | Accept MRR | Mean Rank | Listed Alt Top-1 | Non-Core Top-1 | Runtime ms |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in report["summary"]:
        metrics = row["metrics"]
        runtime = row["runtime"].get("elapsed_ms")
        lines.append(
            f"| `{row['method']}` | `{row['scale']}` | {metrics['scale_skill_count']} | {metrics['selector_visible_tokens_approx']} | "
            f"{metrics['top1_accuracy']:.1%} | {metrics['acceptable_top1_accuracy']:.1%} | "
            f"{metrics['top3_recall']:.1%} | {metrics['acceptable_top3_recall']:.1%} | "
            f"{metrics['top5_recall']:.1%} | {metrics['acceptable_top5_recall']:.1%} | "
            f"{metrics['mrr']:.3f} | {metrics['acceptable_mrr']:.3f} | "
            f"{metrics['mean_gold_rank']} | {metrics['listed_alternative_top1_rate']:.1%} | "
            f"{metrics['non_main_top1_rate']:.1%} | {runtime} |"
        )
    lines.append("")
    lines.append("Accept metrics count documented acceptable alternatives as correct, while strict metrics require the controlled gold label.")
    lines.append("")
    lines.append("## Benchmark Pressure Read")
    lines.append("")
    lines.extend(summarize_pressure(report["summary"]))
    lines.append("")
    lines.append("## Scale Sensitivity")
    lines.append("")
    lines.append("This table compares the controlled core with the current full library. A useful scale condition should create some degradation or non-core false positives without making retrieval random.")
    lines.append("")
    lines.extend(summarize_scale_sensitivity(report["summary"]))
    lines.append("")
    lines.append("## M0 Progressive Disclosure Baseline")
    lines.append("")
    m0 = report.get("m0_trace")
    if m0 and m0.get("available"):
        lines.append(f"- Existing trace manifest: `{m0['source']}`")
        lines.append(f"- Runs: {m0['total_runs']}; prompts: {m0['unique_prompts']}")
        lines.append(f"- Top-1 accuracy: {m0['top1_accuracy']:.1%}")
        lines.append(f"- Any-hit rate: {m0['any_hit']:.1%}")
        lines.append(f"- No explicit skill loaded: {m0.get('no_explicit_skill_rate', 0):.1%}")
        lines.append(f"- Mean full docs loaded: {m0['mean_full_docs_loaded']}")
        lines.append(f"- Note: {m0['note']}")
    else:
        lines.append("- No M0 trace manifest was loaded.")
    lines.append("")
    lines.append("Required M0 trace fields for future runs:")
    lines.append("")
    lines.append("- `prompt_id`, `gold_skill`, `selected_skills`, `full_docs_loaded`, `selector_visible_tokens`, `final_context_tokens`, `latency_ms`, `cost_estimate`, `failure_mode`")
    lines.append("")
    lines.append("## Family Breakdown")
    for row in report["summary"]:
        lines.append("")
        lines.append(f"### `{row['method']}` on `{row['scale']}`")
        lines.append("")
        lines.append("| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for family, metrics in row["metrics"]["by_family"].items():
            lines.append(
                f"| `{family}` | {metrics['total']} | {metrics['top1_accuracy']:.1%} | "
                f"{metrics['acceptable_top1_accuracy']:.1%} | {metrics['top3_recall']:.1%} | "
                f"{metrics['acceptable_top3_recall']:.1%} | {metrics['top5_recall']:.1%} | "
                f"{metrics['acceptable_top5_recall']:.1%} |"
            )
        if row["metrics"]["top_confusions"]:
            lines.append("")
            lines.append("Top confusions:")
            for confusion in row["metrics"]["top_confusions"][:8]:
                lines.append(f"- `{confusion['pair']}`: {confusion['count']}")
    lines.append("")
    lines.append("## Prompt-Level Results")
    for row in report["summary"]:
        key = f"{row['method']}::{row['scale']}"
        lines.append("")
        lines.append(f"### `{row['method']}` on `{row['scale']}`")
        lines.append("")
        lines.append("| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |")
        lines.append("|---|---|---:|---:|---|---|---|")
        for result in report["results"][key]:
            ranking = [item["skill"] for item in result["ranking"]]
            gold = result["gold_skill"]
            prompt_acceptables = report.get("acceptable_alternatives", {}).get(result["prompt_id"], {})
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
            top5 = ", ".join(ranking[:5])
            lines.append(
                f"| `{result['prompt_id']}` | `{gold}` | {rank} | {acceptable_rank} | `{top1}` | {status} | {top5} |"
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run offline skill selector baselines.")
    parser.add_argument("--prompts", default="skill_benchmark/prompts/*.json")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--skills-root", default="skill_benchmark/skills")
    parser.add_argument(
        "--methods",
        default="m1_bm25_flat,m1_tfidf_flat,m2a_minilm_description,m2b_minilm_full_skill,m3_tfidf_schema,m6_bm25_schema_rerank,m6_tfidf_schema_rerank,m6_minilm_full_schema_rerank",
    )
    parser.add_argument("--scales", default="core,current_full")
    parser.add_argument("--embedding-model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--rerank-base-weight", type=float, default=0.40)
    parser.add_argument("--rerank-schema-weight", type=float, default=0.60)
    parser.add_argument("--m0-manifest", default="skill_benchmark/runtime/confusability_results/manifest.csv")
    parser.add_argument("--acceptable-alternatives", default="skill_benchmark/annotations/acceptable_alternatives.json")
    parser.add_argument("--output-md", default="skill_benchmark/outputs/offline_selector_evaluation.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/offline_selector_evaluation.json")
    args = parser.parse_args()

    prompts = load_prompts(args.prompts)
    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    missing_r2 = sorted(set(r1) - set(r2))
    if missing_r2:
        raise ValueError(f"Missing R2 rows for skills: {missing_r2[:20]}")

    full_skill_texts = load_full_skill_texts(Path(args.skills_root), sorted(r1))
    methods = parse_methods(args.methods)
    scales = parse_scales(args.scales)
    acceptable_by_prompt = load_acceptables(Path(args.acceptable_alternatives) if args.acceptable_alternatives else None)

    report: dict[str, Any] = {
        "methods": methods,
        "scales": {},
        "summary": [],
        "results": {},
        "acceptable_alternatives": {
            prompt_id: {
                "acceptable": sorted(values.get("acceptable", set())),
                "borderline": sorted(values.get("borderline", set())),
            }
            for prompt_id, values in sorted(acceptable_by_prompt.items())
        },
        "m0_trace": load_m0_manifest(Path(args.m0_manifest), r1),
    }

    for scale in scales:
        skill_names = build_scale_skill_names(scale, r1_rows)
        report["scales"][scale] = {
            "skill_count": len(skill_names),
            "main_evaluated_count": sum(1 for name in skill_names if r1[name].get("is_main_evaluated")),
            "non_main_count": sum(1 for name in skill_names if not r1[name].get("is_main_evaluated")),
        }
        for method in methods:
            docs = docs_for_method(method, skill_names, r1, r2, full_skill_texts)
            if method in RERANK_METHOD_BASE:
                rerank_token_budget = sum(
                    approximate_tokens(r2[name]["text"]) for name in skill_names[: min(args.rerank_candidates, len(skill_names))]
                )
                selector_visible_tokens = sum(approximate_tokens(doc) for doc in docs) + rerank_token_budget
                rows, runtime = run_hybrid_rerank_selector(
                    method=method,
                    prompts=prompts,
                    skill_names=skill_names,
                    r1=r1,
                    r2=r2,
                    r3=r3,
                    full_skill_texts=full_skill_texts,
                    model_name=args.embedding_model,
                    rerank_candidates=args.rerank_candidates,
                    base_weight=args.rerank_base_weight,
                    schema_weight=args.rerank_schema_weight,
                )
            else:
                selector_visible_tokens = sum(approximate_tokens(doc) for doc in docs)
                rows, runtime = run_selector(method, prompts, skill_names, docs, args.embedding_model)
            metrics = evaluate_rows(rows, r1, len(skill_names), selector_visible_tokens, acceptable_by_prompt)
            key = f"{method}::{scale}"
            report["results"][key] = rows
            report["summary"].append(
                {
                    "method": method,
                    "scale": scale,
                    "metrics": metrics,
                    "runtime": runtime,
                }
            )

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
        print(
            f"{row['method']} on {row['scale']}: "
            f"top1={metrics['top1_accuracy']:.1%}, top5={metrics['top5_recall']:.1%}, "
            f"mrr={metrics['mrr']:.3f}, non_main_top1={metrics['non_main_top1_rate']:.1%}"
        )


if __name__ == "__main__":
    main()
