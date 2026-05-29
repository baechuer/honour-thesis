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
    "could",
    "do",
    "does",
    "doing",
    "for",
    "from",
    "give",
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
    "later",
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
    "or",
    "our",
    "out",
    "please",
    "rather",
    "really",
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
    "pull": "extract",
    "pulled": "extract",
    "compare": "compare",
    "comparison": "compare",
    "comparing": "compare",
    "check": "check",
    "checking": "check",
    "verify": "check",
    "validate": "check",
    "validation": "check",
    "grounding": "ground",
    "grounded": "ground",
    "ground": "ground",
    "support": "support",
    "supported": "support",
    "supports": "support",
    "plan": "plan",
    "planning": "plan",
    "draft": "draft",
    "drafting": "draft",
    "reply": "reply",
    "respond": "reply",
    "response": "reply",
    "monitor": "monitor",
    "monitoring": "monitor",
    "debug": "debug",
    "debugging": "debug",
    "test": "test",
    "testing": "test",
}


POSITIVE_FIELDS = [
    "name",
    "description",
    "use_when",
    "preconditions",
    "workflow",
    "output_shape",
    "writing_rules",
    "dependency_profile",
    "external_dependencies",
    "resource_signals",
    "resource_files",
]


NEGATIVE_FIELDS = ["not_for"]


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


def flatten(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten(item))
        return out
    if isinstance(value, dict):
        return [json.dumps(value, sort_keys=True)]
    return [str(value)]


def field_text(row: dict[str, Any], fields: list[str]) -> str:
    chunks: list[str] = []
    for field in fields:
        chunks.extend(flatten(row.get(field)))
    return "\n".join(chunks)


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
        if not docs:
            return [[] for _ in queries]
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


def overlap_terms(prompt: str, skill_text: str, limit: int = 8) -> list[str]:
    prompt_terms = Counter(term for term in terms(prompt) if "_" not in term)
    skill_terms = set(term for term in terms(skill_text) if "_" not in term)
    return [term for term, _ in prompt_terms.most_common() if term in skill_terms][:limit]


def evaluate(prompts: list[dict[str, Any]], rows: list[dict[str, Any]], scorer: SimilarityScorer) -> list[dict[str, Any]]:
    rows_by_skill = {row["skill"]: row for row in rows}
    non_core_rows = [row for row in rows if not row.get("is_main_evaluated")]
    non_core_skills = [row["skill"] for row in non_core_rows]
    non_core_texts = [field_text(row, POSITIVE_FIELDS) for row in non_core_rows]
    queries = [instruction_text(prompt["prompt"]) for prompt in prompts]
    non_core_scores_matrix = scorer.score_matrix(queries, non_core_texts)

    results: list[dict[str, Any]] = []
    for prompt_index, prompt in enumerate(prompts):
        gold = rows_by_skill[prompt["gold_skill"]]
        gold_text = field_text(gold, POSITIVE_FIELDS)
        gold_boundary_text = field_text(gold, NEGATIVE_FIELDS)
        query = queries[prompt_index]
        gold_score = scorer.score_matrix([query], [gold_text])[0][0]
        gold_boundary_score = scorer.score_matrix([query], [gold_boundary_text])[0][0] if gold_boundary_text else 0.0

        competitors = []
        for skill, row, score, text in zip(non_core_skills, non_core_rows, non_core_scores_matrix[prompt_index], non_core_texts):
            margin = float(score) - float(gold_score)
            if margin >= -0.02:
                status = "above_gold" if margin > 0 else "near_gold"
                competitors.append(
                    {
                        "skill": skill,
                        "family": row["family"],
                        "score": round(float(score), 6),
                        "margin_vs_gold": round(margin, 6),
                        "status": status,
                        "shared_terms": overlap_terms(query, text),
                    }
                )
        competitors.sort(key=lambda row: (-row["score"], row["skill"]))
        above_gold = [row for row in competitors if row["margin_vs_gold"] > 0]
        near_gold = [row for row in competitors if row["margin_vs_gold"] <= 0]
        results.append(
            {
                "id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": prompt["gold_skill"],
                "instruction_text": query,
                "gold_score": round(float(gold_score), 6),
                "gold_boundary_score": round(float(gold_boundary_score), 6),
                "non_core_competitor_count": len(competitors),
                "non_core_above_gold_count": len(above_gold),
                "non_core_near_gold_count": len(near_gold),
                "top_non_core_competitors": competitors[:10],
            }
        )
    return results


def render_markdown(results: list[dict[str, Any]], scorer: SimilarityScorer) -> str:
    total = len(results)
    prompts_with_above = sum(1 for row in results if row["non_core_above_gold_count"])
    prompts_with_near = sum(1 for row in results if row["non_core_competitor_count"])
    above_pairs = sum(row["non_core_above_gold_count"] for row in results)
    near_pairs = sum(row["non_core_near_gold_count"] for row in results)
    family_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    competitor_families: Counter[str] = Counter()
    for row in results:
        family_rows[row["family"]].append(row)
        for competitor in row["top_non_core_competitors"]:
            if competitor["status"] == "above_gold":
                competitor_families[competitor["family"]] += 1

    lines = [
        "# All Non-Core Procedural Competition Report",
        "",
        "This report applies the Step 2 requirement-alignment idea against every non-core skill, not only the listed closest alternatives. It asks whether a background/public/support skill looks procedurally competitive with the gold skill under structured procedural fields.",
        "",
        f"Similarity backend: **{scorer.backend}**"
        + (f" using `{scorer.model_name}`." if scorer.backend == "embedding" else "."),
        "",
        "Important limitation: this is a heuristic procedural-fit screen, not a human adjudication. A non-core score above gold means it deserves review; it does not automatically mean the gold label is wrong.",
        "",
        "## Overall Status",
        "",
        f"- Prompts checked: {total}",
        f"- Non-core skills checked per prompt: 939",
        f"- Gold/non-core prompt-skill comparisons: {total * 939}",
        f"- Prompts with at least one non-core skill above gold: {prompts_with_above}/{total} ({prompts_with_above / total:.1%})",
        f"- Prompts with at least one non-core skill near or above gold: {prompts_with_near}/{total} ({prompts_with_near / total:.1%})",
        f"- Above-gold non-core comparisons: {above_pairs}",
        f"- Near-gold non-core comparisons within 0.02 margin: {near_pairs}",
        "",
        "## Family Summary",
        "",
        "| Prompt family | Prompts | With non-core above gold | Above-gold pairs | Near/above pairs |",
        "|---|---:|---:|---:|---:|",
    ]
    for family in sorted(family_rows):
        rows = family_rows[family]
        lines.append(
            f"| `{family}` | {len(rows)} | "
            f"{sum(1 for row in rows if row['non_core_above_gold_count'])}/{len(rows)} | "
            f"{sum(row['non_core_above_gold_count'] for row in rows)} | "
            f"{sum(row['non_core_competitor_count'] for row in rows)} |"
        )

    lines.extend(["", "## Above-Gold Competitor Families", "", "| Non-core family | Top-10 appearances above gold |", "|---|---:|"])
    for family, count in competitor_families.most_common():
        lines.append(f"| `{family}` | {count} |")

    lines.extend(["", "## Prompts With Non-Core Procedural Competitors", ""])
    lines.append("| Prompt | Gold | Gold score | Above-gold count | Top non-core competitors |")
    lines.append("|---|---|---:|---:|---|")
    for row in sorted(results, key=lambda item: (-item["non_core_above_gold_count"], item["family"], item["id"])):
        if not row["non_core_competitor_count"]:
            continue
        competitors = []
        for competitor in row["top_non_core_competitors"][:5]:
            marker = "+" if competitor["status"] == "above_gold" else "~"
            competitors.append(
                f"{marker}`{competitor['skill']}`/{competitor['family']} ({competitor['score']:.3f}, {competitor['margin_vs_gold']:+.3f})"
            )
        lines.append(
            f"| `{row['id']}` | `{row['gold_skill']}` | {row['gold_score']:.3f} | "
            f"{row['non_core_above_gold_count']} | {'; '.join(competitors)} |"
        )

    lines.extend(["", "## Review Guidance", ""])
    lines.append("- `+` means the non-core skill scored above the gold skill on structured procedural fields.")
    lines.append("- `~` means the non-core skill was within 0.02 of the gold score.")
    lines.append("- Treat high counts as review pressure, not automatic invalidation.")
    lines.append("- If a `+` competitor has the same input type, output artifact, workflow, and success criterion as gold, mark it as acceptable or remove it from the background library.")
    lines.append("- If it only shares generic words such as summary, rewrite, rank, check, evidence, or test while missing the task-specific artifact, keep it as a semantic distractor.")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Compare every non-core skill against every prompt using structured procedural fields.")
    parser.add_argument("--prompts", default=str(repo_root / "prompts" / "*.json"))
    parser.add_argument("--representations", default=str(repo_root / "representations" / "R3_dependency_resource_aware.jsonl"))
    parser.add_argument("--backend", choices=["auto", "embedding", "tfidf", "pure_tfidf"], default="auto")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "all_non_core_procedural_competition_report.md"))
    parser.add_argument("--output-json", default=str(repo_root / "outputs" / "all_non_core_procedural_competition_report.json"))
    args = parser.parse_args()

    prompts = load_prompts(args.prompts)
    rows = load_jsonl(Path(args.representations))
    scorer = SimilarityScorer(args.backend, args.model)
    results = evaluate(prompts, rows, scorer)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(results, scorer), encoding="utf-8")

    prompts_with_above = sum(1 for row in results if row["non_core_above_gold_count"])
    above_pairs = sum(row["non_core_above_gold_count"] for row in results)
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"Similarity backend: {scorer.backend}")
    print(f"Prompts with non-core above gold: {prompts_with_above}/{len(results)}")
    print(f"Above-gold non-core comparisons: {above_pairs}")


if __name__ == "__main__":
    main()
