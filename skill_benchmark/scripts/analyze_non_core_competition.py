#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a", "about", "after", "all", "also", "an", "and", "any", "are", "as", "at",
    "be", "because", "before", "between", "by", "can", "could", "do", "does",
    "doing", "for", "from", "has", "have", "help", "how", "if", "in", "include",
    "into", "is", "it", "its", "make", "me", "more", "not", "of", "on", "one",
    "or", "please", "rather", "should", "skill", "so", "source", "specific",
    "task", "than", "that", "the", "their", "then", "this", "to", "up", "use",
    "user", "using", "want", "what", "when", "where", "which", "while", "with",
    "without", "you",
}


ALIASES = {
    "summarise": "summary",
    "summarize": "summary",
    "summarising": "summary",
    "summarizing": "summary",
    "summaries": "summary",
    "analyse": "analysis",
    "analyze": "analysis",
    "analysing": "analysis",
    "analyzing": "analysis",
    "extracting": "extract",
    "extraction": "extract",
    "checking": "check",
    "validate": "check",
    "validation": "check",
    "reviewing": "review",
    "rewriting": "rewrite",
    "conversion": "convert",
}


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


def terms(text: str) -> list[str]:
    raw = [normalize_token(token) for token in re.findall(r"[a-z0-9][a-z0-9_\-']*", text.lower())]
    raw = [token for token in raw if len(token) > 2 and token not in STOPWORDS]
    bigrams = [f"{raw[index]}_{raw[index + 1]}" for index in range(len(raw) - 1)]
    return raw + bigrams


def build_idf(docs: list[list[str]]) -> dict[str, float]:
    df: Counter[str] = Counter()
    for doc in docs:
        df.update(set(doc))
    total = len(docs)
    return {term: math.log((total + 1) / (count + 1)) + 1.0 for term, count in df.items()}


def vectorize(doc_terms: list[str], idf: dict[str, float]) -> dict[str, float]:
    counts = Counter(doc_terms)
    return {term: (1.0 + math.log(count)) * idf.get(term, 1.0) for term, count in counts.items()}


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    common = set(left) & set(right)
    numerator = sum(left[term] * right[term] for term in common)
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


class SimilarityScorer:
    def __init__(self, backend: str, model_name: str):
        self.backend = "pure_tfidf"
        self.model_name = model_name
        self.model = None
        if backend in {"auto", "embedding"} and importlib.util.find_spec("sentence_transformers"):
            try:
                from sentence_transformers import SentenceTransformer

                try:
                    self.model = SentenceTransformer(model_name, local_files_only=True)
                except TypeError:
                    self.model = SentenceTransformer(model_name)
                self.backend = "embedding"
                return
            except Exception as exc:
                if backend == "embedding":
                    raise RuntimeError(f"Could not load model {model_name!r}: {exc}") from exc
        if backend in {"auto", "tfidf"} and importlib.util.find_spec("sklearn"):
            self.backend = "sklearn_tfidf"
            return
        if backend == "embedding":
            raise RuntimeError("sentence_transformers is not available")

    def score_matrix(self, queries: list[str], docs: list[str]) -> list[list[float]]:
        if self.backend == "embedding":
            import numpy as np

            query_embeddings = self.model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
            doc_embeddings = self.model.encode(docs, normalize_embeddings=True, show_progress_bar=False)
            return np.matmul(query_embeddings, doc_embeddings.T).tolist()
        if self.backend == "sklearn_tfidf":
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), min_df=1)
            matrix = vectorizer.fit_transform([*queries, *docs])
            return cosine_similarity(matrix[: len(queries)], matrix[len(queries) :]).tolist()
        query_terms = [terms(query) for query in queries]
        doc_terms = [terms(doc) for doc in docs]
        idf = build_idf([*query_terms, *doc_terms])
        doc_vectors = [vectorize(doc, idf) for doc in doc_terms]
        return [[cosine(vectorize(query, idf), doc_vector) for doc_vector in doc_vectors] for query in query_terms]


def skill_card(row: dict[str, Any]) -> str:
    return f"{row.get('name', '')}\n{row.get('family', '')}\n{row.get('description', '')}"


def evaluate(prompts: list[dict[str, Any]], skills: list[dict[str, Any]], scorer: SimilarityScorer) -> list[dict[str, Any]]:
    skill_ids = [row["skill"] for row in skills]
    skill_by_id = {row["skill"]: row for row in skills}
    docs = [skill_card(row) for row in skills]
    queries = [instruction_text(prompt["prompt"]) for prompt in prompts]
    matrix = scorer.score_matrix(queries, docs)
    results = []
    for prompt_index, prompt in enumerate(prompts):
        scores = dict(zip(skill_ids, matrix[prompt_index]))
        ranked = sorted(skill_ids, key=lambda skill: scores[skill], reverse=True)
        gold = prompt["gold_skill"]
        non_core_ranked = [skill for skill in ranked if not skill_by_id[skill].get("is_main_evaluated")]
        best_non_core = non_core_ranked[0] if non_core_ranked else None
        top1 = ranked[0]
        results.append(
            {
                "id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": gold,
                "gold_score": round(float(scores[gold]), 6),
                "gold_rank": ranked.index(gold) + 1,
                "top1_skill": top1,
                "top1_family": skill_by_id[top1]["family"],
                "top1_is_non_core": not skill_by_id[top1].get("is_main_evaluated"),
                "best_non_core_skill": best_non_core,
                "best_non_core_family": skill_by_id[best_non_core]["family"] if best_non_core else None,
                "best_non_core_score": round(float(scores[best_non_core]), 6) if best_non_core else None,
                "best_non_core_rank": ranked.index(best_non_core) + 1 if best_non_core else None,
                "best_non_core_beats_gold": bool(best_non_core and scores[best_non_core] > scores[gold]),
                "top10": [
                    {
                        "skill": skill,
                        "family": skill_by_id[skill]["family"],
                        "is_non_core": not skill_by_id[skill].get("is_main_evaluated"),
                        "score": round(float(scores[skill]), 6),
                    }
                    for skill in ranked[:10]
                ],
            }
        )
    return results


def render_markdown(results: list[dict[str, Any]], scorer: SimilarityScorer) -> str:
    total = len(results)
    top1_non_core = sum(1 for row in results if row["top1_is_non_core"])
    best_non_core_beats_gold = sum(1 for row in results if row["best_non_core_beats_gold"])
    gold_top1 = sum(1 for row in results if row["gold_rank"] == 1)
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    non_core_family_counts = Counter(row["best_non_core_family"] for row in results if row["best_non_core_beats_gold"])
    for row in results:
        by_family[row["family"]].append(row)

    lines = [
        "# Non-Core Semantic Competition Report",
        "",
        "This report checks whether background/public/support skills look more semantically similar to benchmark prompts than the gold core skill under a description-card similarity backend.",
        "",
        f"Similarity backend: **{scorer.backend}**"
        + (f" using `{scorer.model_name}`." if scorer.backend == "embedding" else "."),
        "",
        "## Overall Status",
        "",
        f"- Prompts: {total}",
        f"- Gold ranked top-1 among all skills: {gold_top1}/{total} ({gold_top1 / total:.1%})",
        f"- Non-core skill ranked top-1: {top1_non_core}/{total} ({top1_non_core / total:.1%})",
        f"- Best non-core skill scores above gold: {best_non_core_beats_gold}/{total} ({best_non_core_beats_gold / total:.1%})",
        "",
        "Interpretation: a non-core skill beating the gold does not automatically mean the gold label is wrong. It means the compressed semantic representation has a plausible scale distractor that may need reranking or richer procedural representation.",
        "",
        "## Family Summary",
        "",
        "| Prompt family | Prompts | Non-core top-1 | Best non-core beats gold |",
        "|---|---:|---:|---:|",
    ]
    for family in sorted(by_family):
        rows = by_family[family]
        lines.append(
            f"| `{family}` | {len(rows)} | "
            f"{sum(1 for row in rows if row['top1_is_non_core'])}/{len(rows)} | "
            f"{sum(1 for row in rows if row['best_non_core_beats_gold'])}/{len(rows)} |"
        )

    lines.extend(["", "## Non-Core Families That Beat Gold", "", "| Non-core family | Count |", "|---|---:|"])
    for family, count in non_core_family_counts.most_common():
        lines.append(f"| `{family}` | {count} |")

    attention = [row for row in results if row["best_non_core_beats_gold"]]
    lines.extend(["", "## Prompts Where Non-Core Beats Gold", ""])
    if not attention:
        lines.append("- No non-core description-card neighbour scored above the gold skill.")
    else:
        lines.append("| Prompt | Gold | Gold rank | Best non-core | Non-core rank | Scores |")
        lines.append("|---|---|---:|---|---:|---|")
        for row in attention:
            lines.append(
                f"| `{row['id']}` | `{row['gold_skill']}` | {row['gold_rank']} | "
                f"`{row['best_non_core_skill']}` (`{row['best_non_core_family']}`) | "
                f"{row['best_non_core_rank']} | gold {row['gold_score']:.3f}; non-core {row['best_non_core_score']:.3f} |"
            )

    lines.extend(["", "## Prompt Detail", ""])
    for row in results:
        top10 = ", ".join(
            f"`{item['skill']}`/{item['family']} ({item['score']:.3f})" for item in row["top10"][:5]
        )
        lines.extend(
            [
                f"### `{row['id']}`",
                "",
                f"- Gold: `{row['gold_skill']}`; rank {row['gold_rank']}; score {row['gold_score']:.3f}",
                f"- Best non-core: `{row['best_non_core_skill']}`; rank {row['best_non_core_rank']}; score {row['best_non_core_score']:.3f}",
                f"- Top neighbours: {top10}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Analyze whether non-core skills semantically compete with gold skills.")
    parser.add_argument("--prompts", default=str(repo_root / "prompts" / "*.json"))
    parser.add_argument("--representations", default=str(repo_root / "representations" / "R1_flat_metadata.jsonl"))
    parser.add_argument("--backend", choices=["auto", "embedding", "tfidf", "pure_tfidf"], default="auto")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "non_core_semantic_competition_report.md"))
    parser.add_argument("--output-json", default=str(repo_root / "outputs" / "non_core_semantic_competition_report.json"))
    args = parser.parse_args()

    prompts = load_prompts(args.prompts)
    skills = load_jsonl(Path(args.representations))
    scorer = SimilarityScorer(args.backend, args.model)
    results = evaluate(prompts, skills, scorer)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(results, scorer), encoding="utf-8")

    top1_non_core = sum(1 for row in results if row["top1_is_non_core"])
    best_non_core_beats_gold = sum(1 for row in results if row["best_non_core_beats_gold"])
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"Similarity backend: {scorer.backend}")
    print(f"Non-core top-1: {top1_non_core}/{len(results)}")
    print(f"Best non-core beats gold: {best_non_core_beats_gold}/{len(results)}")


if __name__ == "__main__":
    main()
