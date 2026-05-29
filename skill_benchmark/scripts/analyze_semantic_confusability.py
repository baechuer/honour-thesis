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
    "a",
    "about",
    "actually",
    "after",
    "all",
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
    "clear",
    "could",
    "do",
    "does",
    "doing",
    "for",
    "from",
    "has",
    "have",
    "help",
    "how",
    "if",
    "in",
    "include",
    "into",
    "is",
    "it",
    "its",
    "main",
    "make",
    "may",
    "me",
    "more",
    "not",
    "of",
    "on",
    "one",
    "or",
    "other",
    "out",
    "please",
    "rather",
    "result",
    "should",
    "skill",
    "so",
    "source",
    "specific",
    "task",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "this",
    "to",
    "up",
    "use",
    "user",
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
    "analyse": "analysis",
    "analyses": "analysis",
    "analyzing": "analysis",
    "analyze": "analysis",
    "extract": "extract",
    "extracting": "extract",
    "extraction": "extract",
    "pull": "extract",
    "pulled": "extract",
    "rewrite": "rewrite",
    "rewriting": "rewrite",
    "normalise": "normalize",
    "normalising": "normalize",
    "normalize": "normalize",
    "convert": "convert",
    "conversion": "convert",
    "compare": "compare",
    "comparison": "compare",
    "grounding": "ground",
    "grounded": "ground",
    "support": "support",
    "supported": "support",
    "supports": "support",
    "check": "check",
    "checking": "check",
    "verify": "check",
    "validate": "check",
    "monitor": "monitor",
    "monitoring": "monitor",
    "debug": "debug",
    "debugging": "debug",
    "test": "test",
    "testing": "test",
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
    bigrams = [f"{raw[i]}_{raw[i + 1]}" for i in range(len(raw) - 1)]
    trigrams = [f"{raw[i]}_{raw[i + 1]}_{raw[i + 2]}" for i in range(len(raw) - 2)]
    return raw + bigrams + trigrams


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
        self.requested_backend = backend
        self.model_name = model_name
        self.backend = "pure_tfidf"
        self.model = None

        if backend in {"auto", "embedding"} and importlib.util.find_spec("sentence_transformers"):
            try:
                from sentence_transformers import SentenceTransformer

                try:
                    self.model = SentenceTransformer(model_name, local_files_only=True)
                except Exception:
                    self.model = SentenceTransformer(model_name)
                self.backend = "embedding"
                return
            except Exception as exc:
                if backend == "embedding":
                    raise RuntimeError(f"Could not load sentence-transformer model {model_name!r}: {exc}") from exc

        if backend in {"auto", "tfidf"} and importlib.util.find_spec("sklearn"):
            self.backend = "sklearn_tfidf"
            return

        if backend == "embedding":
            raise RuntimeError("sentence_transformers is not available")

    def score_matrix(self, queries: list[str], docs: list[str]) -> list[list[float]]:
        if not queries or not docs:
            return [[] for _ in queries]

        if self.backend == "embedding":
            import numpy as np

            query_embeddings = self.model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
            doc_embeddings = self.model.encode(docs, normalize_embeddings=True, show_progress_bar=False)
            return np.matmul(query_embeddings, doc_embeddings.T).tolist()

        if self.backend == "sklearn_tfidf":
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                min_df=1,
            )
            matrix = vectorizer.fit_transform([*queries, *docs])
            query_matrix = matrix[: len(queries)]
            doc_matrix = matrix[len(queries) :]
            return cosine_similarity(query_matrix, doc_matrix).tolist()

        query_terms = [terms(query) for query in queries]
        doc_terms = [terms(doc) for doc in docs]
        idf = build_idf([*query_terms, *doc_terms])
        doc_vectors = [vectorize(doc, idf) for doc in doc_terms]
        return [
            [cosine(vectorize(query, idf), doc_vector) for doc_vector in doc_vectors]
            for query in query_terms
        ]

    def plausibility_thresholds(self) -> tuple[float, float, float]:
        if self.backend == "embedding":
            return 0.08, 0.85, 0.50
        return 0.04, 0.70, 0.12


def skill_card(row: dict[str, Any]) -> str:
    return f"{row.get('name', '')}\n{row.get('family', '')}\n{row.get('description', '')}"


def shared_terms(left_text: str, right_text: str, limit: int = 8) -> list[str]:
    left = Counter(term for term in terms(left_text) if "_" not in term)
    right = set(term for term in terms(right_text) if "_" not in term)
    return [term for term, _ in left.most_common() if term in right][:limit]


def evaluate(prompts: list[dict[str, Any]], skills: list[dict[str, Any]], scorer: SimilarityScorer) -> list[dict[str, Any]]:
    skill_texts = {row["skill"]: skill_card(row) for row in skills}
    skill_ids = [row["skill"] for row in skills]
    skill_cards = [skill_texts[skill] for skill in skill_ids]
    prompt_instructions = [instruction_text(prompt["prompt"]) for prompt in prompts]
    prompt_skill_matrix = scorer.score_matrix(prompt_instructions, skill_cards)
    skill_skill_matrix = scorer.score_matrix(skill_cards, skill_cards)
    skill_index = {skill: index for index, skill in enumerate(skill_ids)}
    near_margin, near_ratio, skill_threshold = scorer.plausibility_thresholds()

    results: list[dict[str, Any]] = []
    for prompt_index, prompt in enumerate(prompts):
        prompt_instruction = prompt_instructions[prompt_index]
        all_scores = {
            skill: float(prompt_skill_matrix[prompt_index][skill_index[skill]])
            for skill in skill_ids
        }
        ranked_all = sorted(all_scores, key=all_scores.get, reverse=True)
        gold = prompt["gold_skill"]
        gold_score = all_scores[gold]
        pair_results = []
        plausible_count = 0
        for alternative in prompt.get("closest_alternatives", []):
            prompt_alt_score = all_scores[alternative]
            skill_skill_score = float(skill_skill_matrix[skill_index[gold]][skill_index[alternative]])
            near_gold = prompt_alt_score >= max(0.01, gold_score - near_margin) or (
                gold_score > 0 and prompt_alt_score / gold_score >= near_ratio
            )
            similar_skill_card = skill_skill_score >= skill_threshold
            plausible = near_gold or similar_skill_card
            if plausible:
                plausible_count += 1
            pair_results.append(
                {
                    "alternative_skill": alternative,
                    "prompt_gold_score": round(gold_score, 4),
                    "prompt_alternative_score": round(prompt_alt_score, 4),
                    "skill_card_similarity": round(skill_skill_score, 4),
                    "near_gold_prompt_score": near_gold,
                    "similar_skill_card": similar_skill_card,
                    "plausible_confusion": plausible,
                    "shared_prompt_alt_terms": shared_terms(prompt_instruction, skill_texts[alternative]),
                    "shared_gold_alt_terms": shared_terms(skill_texts[gold], skill_texts[alternative]),
                }
            )
        results.append(
            {
                "id": prompt["id"],
                "family": prompt.get("family"),
                "gold_skill": gold,
                "similarity_backend": scorer.backend,
                "embedding_model": scorer.model_name if scorer.backend == "embedding" else "",
                "instruction_text": prompt_instruction,
                "gold_rank_all_skills": ranked_all.index(gold) + 1,
                "top10_all_skills": [
                    {"skill": skill, "score": round(all_scores[skill], 4)}
                    for skill in ranked_all[:10]
                ],
                "plausible_alternative_count": plausible_count,
                "pass_semantic_confusability": plausible_count >= min(2, len(prompt.get("closest_alternatives", []))),
                "pairs": pair_results,
            }
        )
    return results


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/0"
    return f"{numerator}/{denominator} ({numerator / denominator:.1%})"


def status_label(prompt_pass: int, prompt_total: int) -> str:
    rate = prompt_pass / prompt_total if prompt_total else 0.0
    if rate >= 0.85:
        return "PASS"
    if rate >= 0.70:
        return "WARN"
    return "FAIL"


def write_markdown(results: list[dict[str, Any]], path: Path, scorer: SimilarityScorer) -> None:
    prompt_total = len(results)
    prompt_pass = sum(1 for row in results if row["pass_semantic_confusability"])
    pair_total = sum(len(row["pairs"]) for row in results)
    plausible_pairs = sum(1 for row in results for pair in row["pairs"] if pair["plausible_confusion"])
    gold_top1 = sum(1 for row in results if row["gold_rank_all_skills"] == 1)
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        by_family[row["family"]].append(row)

    weak_prompts = [row for row in results if not row["pass_semantic_confusability"]]

    lines = [
        "# Semantic Confusability Report",
        "",
        "This report implements Step 3 of the benchmark rubric: listed alternatives should be semantically plausible neighbours, not random unrelated distractors.",
        "",
        f"Similarity backend: **{scorer.backend}**"
        + (f" using `{scorer.model_name}`." if scorer.backend == "embedding" else "."),
        "",
        "Interpretation: this is an offline similarity diagnostic. It is enough to flag obviously non-confusable pairs, but final thesis evidence should still report actual selector results for M1-M6.",
        "",
        "## Overall Status",
        "",
        f"- Step 3 status: **{status_label(prompt_pass, prompt_total)}**",
        f"- Prompts with at least two plausible listed alternatives: {pct(prompt_pass, prompt_total)}",
        f"- Gold/alternative pairs marked plausible: {pct(plausible_pairs, pair_total)}",
        f"- Gold skill ranked top-1 among all skills by this backend: {pct(gold_top1, prompt_total)}",
        "",
        "Pass rule used here: each prompt should have at least two alternatives whose description-card score is close to the gold prompt score, or whose skill card is similar to the gold skill card.",
        "",
        "## Family Summary",
        "",
        "| Family | Prompts | Prompt pass | Gold top-1 by similarity backend |",
        "|---|---:|---:|---:|",
    ]
    for family in sorted(by_family):
        rows = by_family[family]
        lines.append(
            f"| {family} | {len(rows)} | "
            f"{sum(1 for row in rows if row['pass_semantic_confusability'])}/{len(rows)} | "
            f"{sum(1 for row in rows if row['gold_rank_all_skills'] == 1)}/{len(rows)} |"
        )

    lines.extend(["", "## Weak Semantic-Confusability Prompts", ""])
    if not weak_prompts:
        lines.append("- No weak prompts under this fallback similarity check.")
    else:
        lines.extend(["| Prompt | Gold | Plausible alternatives | Gold all-skill rank |", "|---|---|---:|---:|"])
        for row in weak_prompts:
            lines.append(
                f"| `{row['id']}` | `{row['gold_skill']}` | "
                f"{row['plausible_alternative_count']} | {row['gold_rank_all_skills']} |"
            )

    lines.extend(["", "## Prompt Detail", ""])
    for row in sorted(results, key=lambda item: (item["family"], item["id"])):
        lines.extend(
            [
                f"### `{row['id']}`",
                "",
                f"- Family: `{row['family']}`",
                f"- Gold skill: `{row['gold_skill']}`",
                f"- Plausible listed alternatives: {row['plausible_alternative_count']}",
                f"- Gold rank among all skills by similarity backend: {row['gold_rank_all_skills']}",
                "",
                "| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |",
                "|---|---:|---:|---:|---|---|---|",
            ]
        )
        for pair in row["pairs"]:
            prompt_terms = ", ".join(pair["shared_prompt_alt_terms"]) or "-"
            skill_terms = ", ".join(pair["shared_gold_alt_terms"]) or "-"
            lines.append(
                f"| `{pair['alternative_skill']}` | {pair['prompt_gold_score']:.4f} | "
                f"{pair['prompt_alternative_score']:.4f} | {pair['skill_card_similarity']:.4f} | "
                f"{'yes' if pair['plausible_confusion'] else 'no'} | {prompt_terms} | {skill_terms} |"
            )
        top10 = ", ".join(f"`{item['skill']}` ({item['score']:.3f})" for item in row["top10_all_skills"][:5])
        lines.extend(["", f"Top similarity neighbours: {top10}", ""])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Analyze semantic confusability of gold skills and listed alternatives.")
    parser.add_argument(
        "--prompts-glob",
        default=str(repo_root / "prompts" / "*_confusability.json"),
        help="Glob for prompt JSON files.",
    )
    parser.add_argument(
        "--representations",
        type=Path,
        default=repo_root / "representations",
        help="Representation output directory.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=repo_root / "outputs" / "semantic_confusability_report.md",
        help="Markdown report path.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=repo_root / "outputs" / "semantic_confusability_report.json",
        help="Machine-readable report path.",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "embedding", "tfidf", "pure_tfidf"],
        default="auto",
        help="Similarity backend. `auto` prefers sentence-transformer embeddings, then sklearn TF-IDF, then pure Python TF-IDF.",
    )
    parser.add_argument(
        "--model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence-transformer model name used for embedding backend.",
    )
    args = parser.parse_args()

    skills = load_jsonl(args.representations / "R1_flat_metadata.jsonl")
    prompts = load_prompts(args.prompts_glob)
    scorer = SimilarityScorer(args.backend, args.model)
    results = evaluate(prompts, skills, scorer)

    write_markdown(results, args.markdown_output, scorer)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    prompt_pass = sum(1 for row in results if row["pass_semantic_confusability"])
    print(f"Wrote {args.markdown_output}")
    print(f"Wrote {args.json_output}")
    print(f"Similarity backend: {scorer.backend}")
    print(f"Prompt pass: {prompt_pass}/{len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
