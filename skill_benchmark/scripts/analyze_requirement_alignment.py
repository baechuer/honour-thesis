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


def positive_requirement_text(instruction: str) -> str:
    """Remove local negated spans before scoring positive procedural fit."""

    text = instruction
    patterns = [
        r"\bdo not\b[^.;:]*",
        r"\bdon't\b[^.;:]*",
        r"\bnot\b[^.;:]*",
        r"\bwithout\b[^.;:]*",
        r"\bno\b\s+(?:existing|detailed|only|just|need for|requirement for)[^.;:]*",
        r"\brather than\b[^.;:]*",
        r"\binstead of\b[^.;:]*",
    ]
    for pattern in patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    return " ".join(text.split())


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
    unigrams = raw
    bigrams = [f"{raw[i]}_{raw[i + 1]}" for i in range(len(raw) - 1)]
    return unigrams + bigrams


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

    def scores(self, query: str, docs: list[str]) -> list[float]:
        if not docs:
            return []
        if self.backend == "embedding":
            import numpy as np

            embeddings = self.model.encode([query, *docs], normalize_embeddings=True, show_progress_bar=False)
            query_embedding = embeddings[0]
            doc_embeddings = embeddings[1:]
            return [float(score) for score in np.matmul(doc_embeddings, query_embedding)]

        if self.backend == "sklearn_tfidf":
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                min_df=1,
            )
            matrix = vectorizer.fit_transform([query, *docs])
            return [float(score) for score in cosine_similarity(matrix[0:1], matrix[1:]).ravel()]

        query_terms = terms(query)
        doc_terms = [terms(doc) for doc in docs]
        idf = build_idf([query_terms, *doc_terms])
        query_vec = vectorize(query_terms, idf)
        return [cosine(query_vec, vectorize(doc, idf)) for doc in doc_terms]


def overlap_terms(prompt_terms: list[str], skill_terms: list[str], limit: int = 10) -> list[str]:
    prompt_counts = Counter(prompt_terms)
    skill_set = set(skill_terms)
    shared = [term for term, _ in prompt_counts.most_common() if term in skill_set and "_" not in term]
    return shared[:limit]


def evaluate_prompt(prompt: dict[str, Any], rows_by_skill: dict[str, dict[str, Any]], scorer: SimilarityScorer) -> dict[str, Any]:
    acceptable_alternatives = list(prompt.get("acceptable_alternatives", []))
    candidate_ids = [
        prompt["gold_skill"],
        *prompt.get("closest_alternatives", []),
        *acceptable_alternatives,
    ]
    candidate_ids = list(dict.fromkeys(candidate_ids))
    candidates = [rows_by_skill[skill_id] for skill_id in candidate_ids]
    instruction = instruction_text(prompt["prompt"])
    positive_instruction = positive_requirement_text(instruction)
    positive_prompt_terms = terms(positive_instruction)
    boundary_prompt_terms = terms(instruction)

    positive_texts: dict[str, str] = {}
    negative_texts: dict[str, str] = {}
    positive_terms: dict[str, list[str]] = {}
    negative_terms: dict[str, list[str]] = {}
    for row in candidates:
        positive_texts[row["skill"]] = field_text(row, POSITIVE_FIELDS)
        negative_texts[row["skill"]] = field_text(row, NEGATIVE_FIELDS)
        positive_terms[row["skill"]] = terms(positive_texts[row["skill"]])
        negative_terms[row["skill"]] = terms(negative_texts[row["skill"]])

    positive_score_values = scorer.scores(positive_instruction, [positive_texts[skill_id] for skill_id in candidate_ids])
    negative_score_values = scorer.scores(instruction, [negative_texts[skill_id] for skill_id in candidate_ids])
    positive_scores = dict(zip(candidate_ids, positive_score_values))
    negative_scores = dict(zip(candidate_ids, negative_score_values))

    scores: dict[str, dict[str, Any]] = {}
    for row in candidates:
        skill = row["skill"]
        positive_score = positive_scores[skill]
        negative_score = negative_scores[skill]
        net_score = positive_score
        scores[skill] = {
            "positive": round(positive_score, 4),
            "alternative_boundary": round(negative_score, 4),
            "net": round(net_score, 4),
            "shared_positive_terms": overlap_terms(positive_prompt_terms, positive_terms[skill]),
            "shared_boundary_terms": overlap_terms(boundary_prompt_terms, negative_terms[skill]),
        }

    sorted_candidates = sorted(candidate_ids, key=lambda skill_id: scores[skill_id]["net"], reverse=True)
    gold_or_acceptable = [prompt["gold_skill"], *acceptable_alternatives]
    gold_or_acceptable_rank = min(
        sorted_candidates.index(skill_id) + 1
        for skill_id in gold_or_acceptable
        if skill_id in sorted_candidates
    )
    gold_score = scores[prompt["gold_skill"]]["net"]
    margin_threshold = 0.04 if scorer.backend == "embedding" else 0.02
    boundary_threshold = 0.42 if scorer.backend == "embedding" else 0.08
    pair_results = []
    for alternative in prompt.get("closest_alternatives", []):
        alt_score = scores[alternative]["net"]
        margin = gold_score - alt_score
        alt_boundary = scores[alternative]["alternative_boundary"]
        acceptable_equivalent = alternative in set(acceptable_alternatives)
        pair_pass = acceptable_equivalent or margin >= margin_threshold or alt_boundary >= boundary_threshold
        pair_results.append(
            {
                "alternative_skill": alternative,
                "acceptable_equivalent": acceptable_equivalent,
                "gold_net": round(gold_score, 4),
                "alternative_net": round(alt_score, 4),
                "margin": round(margin, 4),
                "alternative_boundary": round(alt_boundary, 4),
                "margin_threshold": margin_threshold,
                "boundary_threshold": boundary_threshold,
                "pass_requirement_alignment": pair_pass,
                "review_reason": (
                    "acceptable equivalent recorded; not counted as a wrong distractor"
                    if acceptable_equivalent
                    else "" if pair_pass else "gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated"
                ),
            }
        )
    for alternative in acceptable_alternatives:
        alt_score = scores[alternative]["net"]
        margin = gold_score - alt_score
        pair_results.append(
            {
                "alternative_skill": alternative,
                "acceptable_equivalent": True,
                "gold_net": round(gold_score, 4),
                "alternative_net": round(alt_score, 4),
                "margin": round(margin, 4),
                "alternative_boundary": round(scores[alternative]["alternative_boundary"], 4),
                "margin_threshold": margin_threshold,
                "boundary_threshold": boundary_threshold,
                "pass_requirement_alignment": True,
                "review_reason": "acceptable equivalent recorded; not counted as a wrong distractor",
            }
        )

    return {
        "id": prompt["id"],
        "family": prompt.get("family"),
        "gold_skill": prompt["gold_skill"],
        "similarity_backend": scorer.backend,
        "embedding_model": scorer.model_name if scorer.backend == "embedding" else "",
        "instruction_text": instruction,
        "positive_instruction_text": positive_instruction,
        "candidate_rank": sorted_candidates,
        "gold_rank": sorted_candidates.index(prompt["gold_skill"]) + 1,
        "gold_or_acceptable_rank": gold_or_acceptable_rank,
        "acceptable_alternatives": acceptable_alternatives,
        "scores": scores,
        "pairs": pair_results,
        "pass_requirement_alignment": all(
            pair["pass_requirement_alignment"]
            for pair in pair_results
            if not pair.get("acceptable_equivalent")
        ),
    }


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/0"
    return f"{numerator}/{denominator} ({numerator / denominator:.1%})"


def status_label(prompt_pass: int, prompt_total: int, gold_top1: int) -> str:
    pass_rate = prompt_pass / prompt_total if prompt_total else 0.0
    top1_rate = gold_top1 / prompt_total if prompt_total else 0.0
    if pass_rate >= 0.90 and top1_rate >= 0.70:
        return "PASS"
    if pass_rate >= 0.75 and top1_rate >= 0.55:
        return "WARN"
    return "FAIL"


def write_markdown(results: list[dict[str, Any]], path: Path, scorer: SimilarityScorer) -> None:
    prompt_total = len(results)
    pair_total = sum(len(row["pairs"]) for row in results)
    prompt_pass = sum(1 for row in results if row["pass_requirement_alignment"])
    pair_pass = sum(1 for row in results for pair in row["pairs"] if pair["pass_requirement_alignment"])
    gold_top1 = sum(1 for row in results if row["gold_rank"] == 1)
    gold_or_acceptable_top1 = sum(
        1 for row in results if row.get("gold_or_acceptable_rank", row["gold_rank"]) == 1
    )
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        by_family[row["family"]].append(row)

    weak_pairs = [
        (row, pair)
        for row in results
        for pair in row["pairs"]
        if not pair["pass_requirement_alignment"] and not pair.get("acceptable_equivalent")
    ]

    lines = [
        "# Procedural Requirement Alignment Report",
        "",
        "This is the stricter Step 2 check. Instead of only asking whether skill fields are textually different, it asks whether the prompt-specific requirement aligns better with the gold skill than with each listed alternative.",
        "",
        f"Similarity backend: **{scorer.backend}**"
        + (f" using `{scorer.model_name}`." if scorer.backend == "embedding" else "."),
        "",
        "Method: the script strips long source text where possible, removes local negated spans before scoring positive procedural fit, and still uses the full instruction when matching an alternative's `not_for` boundary. This prevents phrases such as `not a calendar plan` from positively boosting calendar-planning skills while preserving boundary evidence.",
        "",
        "## Overall Status",
        "",
        f"- Step 2 requirement-alignment status: **{status_label(prompt_pass, prompt_total, gold_top1)}**",
        f"- Prompts where every alternative is beaten by gold or rejected by its boundary: {pct(prompt_pass, prompt_total)}",
        f"- Gold/alternative pairs passing requirement alignment: {pct(pair_pass, pair_total)}",
        f"- Gold skill ranked first among gold + listed alternatives: {pct(gold_top1, prompt_total)}",
        f"- Gold or acceptable equivalent ranked first among listed candidates: {pct(gold_or_acceptable_top1, prompt_total)}",
        "",
        "Pass rule used here: for each gold/alternative pair, the gold skill must either score above the alternative by the backend-specific margin threshold, or the prompt must strongly activate the alternative's `not_for` boundary. Recorded acceptable equivalents are scored separately and do not count as wrong distractors. Current thresholds are stored in the JSON report for each pair.",
        "",
        "## Family Summary",
        "",
        "| Family | Prompts | Prompt pass | Gold top-1 | Gold/acceptable top-1 |",
        "|---|---:|---:|---:|---:|",
    ]
    for family in sorted(by_family):
        family_rows = by_family[family]
        lines.append(
            f"| {family} | {len(family_rows)} | "
            f"{sum(1 for row in family_rows if row['pass_requirement_alignment'])}/{len(family_rows)} | "
            f"{sum(1 for row in family_rows if row['gold_rank'] == 1)}/{len(family_rows)} | "
            f"{sum(1 for row in family_rows if row.get('gold_or_acceptable_rank', row['gold_rank']) == 1)}/{len(family_rows)} |"
        )

    lines.extend(["", "## Weak Requirement Pairs", ""])
    if not weak_pairs:
        lines.append("- No weak requirement-alignment pairs under this heuristic.")
    else:
        lines.extend(["| Prompt | Gold | Alternative | Margin | Reason |", "|---|---|---|---:|---|"])
        for row, pair in weak_pairs[:100]:
            lines.append(
                f"| `{row['id']}` | `{row['gold_skill']}` | `{pair['alternative_skill']}` | "
                f"{pair['margin']:.4f} | {pair['review_reason']} |"
            )

    lines.extend(["", "## Prompt Detail", ""])
    for row in sorted(results, key=lambda item: (item["family"], item["id"])):
        lines.extend(
            [
                f"### `{row['id']}`",
                "",
                f"- Family: `{row['family']}`",
                f"- Gold skill: `{row['gold_skill']}`",
                f"- Gold rank among listed candidates: {row['gold_rank']}",
                f"- Instruction used for scoring: {row['instruction_text']}",
                f"- Positive-fit instruction after negation cleanup: {row['positive_instruction_text']}",
                "",
                "| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |",
                "|---|---:|---:|---:|---|---|",
            ]
        )
        for skill in row["candidate_rank"]:
            score = row["scores"][skill]
            positive_terms = ", ".join(score["shared_positive_terms"][:8]) or "-"
            boundary_terms = ", ".join(score["shared_boundary_terms"][:8]) or "-"
            lines.append(
                f"| `{skill}` | {score['net']:.4f} | {score['positive']:.4f} | "
                f"{score['alternative_boundary']:.4f} | {positive_terms} | {boundary_terms} |"
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Analyze whether prompt requirements align with gold skills better than alternatives.")
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
        default=repo_root / "outputs" / "procedural_requirement_alignment_report.md",
        help="Markdown report path.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=repo_root / "outputs" / "procedural_requirement_alignment_report.json",
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

    rows = load_jsonl(args.representations / "R3_dependency_resource_aware.jsonl")
    rows_by_skill = {row["skill"]: row for row in rows}
    prompts = load_prompts(args.prompts_glob)
    scorer = SimilarityScorer(args.backend, args.model)
    results = [evaluate_prompt(prompt, rows_by_skill, scorer) for prompt in prompts]

    write_markdown(results, args.markdown_output, scorer)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    prompt_pass = sum(1 for row in results if row["pass_requirement_alignment"])
    gold_top1 = sum(1 for row in results if row["gold_rank"] == 1)
    gold_or_acceptable_top1 = sum(
        1 for row in results if row.get("gold_or_acceptable_rank", row["gold_rank"]) == 1
    )
    print(f"Wrote {args.markdown_output}")
    print(f"Wrote {args.json_output}")
    print(f"Similarity backend: {scorer.backend}")
    print(f"Prompt pass: {prompt_pass}/{len(results)}")
    print(f"Gold top-1 among listed candidates: {gold_top1}/{len(results)}")
    print(f"Gold-or-acceptable top-1 among listed candidates: {gold_or_acceptable_top1}/{len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
