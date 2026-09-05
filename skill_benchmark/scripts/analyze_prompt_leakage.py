#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import json
import re
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


GENERIC_TITLE_TOKENS = {
    "agent",
    "analysis",
    "analyser",
    "analyzer",
    "assessor",
    "auditor",
    "builder",
    "checker",
    "configurer",
    "creator",
    "detector",
    "diagnoser",
    "drafter",
    "editor",
    "evaluator",
    "extractor",
    "finder",
    "forecaster",
    "generator",
    "helper",
    "installer",
    "modeler",
    "monitor",
    "orchestrator",
    "packager",
    "planner",
    "polisher",
    "preparer",
    "ranker",
    "retriever",
    "reviewer",
    "scanner",
    "selector",
    "summariser",
    "summarizer",
    "tester",
    "writer",
}


PROVIDER_OR_TOOL_TOKENS = {
    "airtable",
    "amazon",
    "anthropic",
    "api",
    "bases",
    "base",
    "canvas",
    "canva",
    "chatgpt",
    "chrome",
    "claude",
    "cloudflare",
    "devtool",
    "docs",
    "doc",
    "figma",
    "github",
    "gradio",
    "hugging",
    "husky",
    "jupyter",
    "json",
    "linear",
    "cli",
    "lint",
    "markitdown",
    "mcp",
    "mysql",
    "netlify",
    "notion",
    "obsidian",
    "openai",
    "pdfplumber",
    "playwright",
    "postgresql",
    "render",
    "sentry",
    "shopify",
    "slack",
    "transformers",
    "wrangler",
    "zendesk",
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


POSITIVE_FIELDS = [
    "description",
    "use_when",
    "preconditions",
    "workflow",
    "output_shape",
    "writing_rules",
]


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


def normalized_plain(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def normalize_token(token: str) -> str:
    token = token.lower().strip("_-'")
    token = ALIASES.get(token, token)
    if len(token) > 5 and token.endswith("ing"):
        token = token[:-3]
    elif len(token) > 4 and token.endswith("ed"):
        token = token[:-2]
    elif len(token) > 4 and token.endswith("er"):
        token = token[:-2]
    elif len(token) > 4 and token.endswith("or"):
        token = token[:-2]
    elif len(token) > 4 and token.endswith("s"):
        token = token[:-1]
    return ALIASES.get(token, token)


def tokens(text: str) -> list[str]:
    output: list[str] = []
    for raw in re.findall(r"[a-zA-Z][a-zA-Z0-9_'-]*", text.lower()):
        token = normalize_token(raw)
        if len(token) < 3:
            continue
        if token in STOPWORDS:
            continue
        output.append(token)
    return output


def informative_title_tokens(skill_id: str) -> list[str]:
    raw_tokens = tokens(skill_id.replace("-", " ").replace("_", " "))
    filtered = [token for token in raw_tokens if token not in GENERIC_TITLE_TOKENS]
    return filtered if filtered else raw_tokens


def flatten(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        chunks: list[str] = []
        for item in value:
            chunks.extend(flatten(item))
        return chunks
    if isinstance(value, dict):
        chunks = []
        for item in value.values():
            chunks.extend(flatten(item))
        return chunks
    return [str(value)]


def positive_text(row: dict[str, Any]) -> str:
    chunks: list[str] = []
    for field in POSITIVE_FIELDS:
        chunks.extend(flatten(row.get(field)))
    return "\n".join(chunks)


def ngrams(token_list: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(token_list[index : index + n]) for index in range(0, max(0, len(token_list) - n + 1))}


def longest_shared_ngram(prompt_tokens: list[str], skill_tokens: list[str], min_n: int = 4, max_n: int = 8) -> list[str]:
    best: tuple[str, ...] = ()
    prompt_sets = {n: ngrams(prompt_tokens, n) for n in range(min_n, max_n + 1)}
    for n in range(max_n, min_n - 1, -1):
        shared = prompt_sets[n].intersection(ngrams(skill_tokens, n))
        if shared:
            best = sorted(shared)[0]
            break
    return list(best)


def title_recall(prompt_token_set: set[str], skill_id: str) -> tuple[float, list[str], list[str]]:
    title_tokens = informative_title_tokens(skill_id)
    if not title_tokens:
        return 0.0, [], []
    matched = [token for token in title_tokens if token in prompt_token_set]
    return len(matched) / len(title_tokens), matched, title_tokens


def exact_name_leaks(prompt_plain: str, skill_id: str) -> list[str]:
    leaks: list[str] = []
    hyphen_name = skill_id.lower()
    spaced_name = skill_id.replace("-", " ").replace("_", " ").lower()
    compact_name = skill_id.replace("-", "").replace("_", "").lower()
    prompt_compact = prompt_plain.replace(" ", "")
    if hyphen_name in prompt_plain:
        leaks.append(hyphen_name)
    if spaced_name in prompt_plain and len(spaced_name.split()) >= 2:
        leaks.append(spaced_name)
    if compact_name in prompt_compact and len(compact_name) >= 10:
        leaks.append(compact_name)
    return sorted(set(leaks))


def analyze_prompt(prompt: dict[str, Any], skills: dict[str, dict[str, Any]]) -> dict[str, Any]:
    instruction = instruction_text(prompt["prompt"])
    prompt_plain = normalized_plain(instruction)
    prompt_tokens = tokens(instruction)
    prompt_token_set = set(prompt_tokens)
    gold = prompt["gold_skill"]
    alternatives = prompt.get("closest_alternatives", [])

    gold_exact = exact_name_leaks(prompt_plain, gold)
    gold_title_recall, gold_title_hits, gold_title_tokens = title_recall(prompt_token_set, gold)

    alt_title_rows: list[dict[str, Any]] = []
    alt_max_recall = 0.0
    for alternative in alternatives:
        recall, hits, title_tokens = title_recall(prompt_token_set, alternative)
        alt_max_recall = max(alt_max_recall, recall)
        alt_title_rows.append(
            {
                "skill": alternative,
                "title_recall": round(recall, 4),
                "matched_title_tokens": hits,
                "title_tokens": title_tokens,
                "exact_name_leaks": exact_name_leaks(prompt_plain, alternative),
            }
        )

    title_advantage = gold_title_recall - alt_max_recall

    gold_skill = skills[gold]
    gold_ngram = longest_shared_ngram(prompt_tokens, tokens(positive_text(gold_skill)))
    alt_ngram_lengths = []
    for alternative in alternatives:
        if alternative in skills:
            alt_ngram_lengths.append(len(longest_shared_ngram(prompt_tokens, tokens(positive_text(skills[alternative])))))
    max_alt_ngram = max(alt_ngram_lengths or [0])

    risk_flags: list[str] = []
    if gold_exact:
        risk_flags.append("exact_gold_skill_name")
    if gold_title_recall >= 0.8 and title_advantage >= 0.34 and len(gold_title_tokens) >= 2:
        risk_flags.append("gold_title_tokens_dominate")
    if len(gold_ngram) >= 6 and len(gold_ngram) > max_alt_ngram:
        risk_flags.append("copied_gold_skill_phrase")
    if gold_title_recall >= 1.0 and len(gold_title_tokens) >= 2:
        risk_flags.append("complete_gold_title_overlap")

    if "exact_gold_skill_name" in risk_flags:
        risk_level = "critical"
    elif "gold_title_tokens_dominate" in risk_flags or "copied_gold_skill_phrase" in risk_flags:
        risk_level = "high"
    elif "complete_gold_title_overlap" in risk_flags or gold_title_recall >= 0.67:
        risk_level = "medium"
    else:
        risk_level = "low"

    provider_cue_status = prompt.get("provider_cue_status", "not_recorded")
    provider_dependency_cue = (
        provider_cue_status == "provider_or_tool_explicit"
        and risk_level == "medium"
        and not gold_exact
        and all(token in PROVIDER_OR_TOOL_TOKENS for token in gold_title_hits)
    )
    if provider_dependency_cue:
        risk_level = "low"
        risk_flags.append("provider_tool_dependency_cue")

    return {
        "id": prompt["id"],
        "family": prompt["family"],
        "gold_skill": gold,
        "closest_alternatives": alternatives,
        "instruction_text": instruction,
        "risk_level": risk_level,
        "risk_flags": risk_flags,
        "provider_cue_status": provider_cue_status,
        "prompt_information_level": prompt.get("prompt_information_level", "not_recorded"),
        "provider_dependency_cue": provider_dependency_cue,
        "gold_exact_name_leaks": gold_exact,
        "gold_title_recall": round(gold_title_recall, 4),
        "gold_title_tokens": gold_title_tokens,
        "gold_title_hits": gold_title_hits,
        "max_alternative_title_recall": round(alt_max_recall, 4),
        "title_recall_advantage": round(title_advantage, 4),
        "gold_shared_phrase": " ".join(gold_ngram),
        "gold_shared_phrase_length": len(gold_ngram),
        "max_alternative_shared_phrase_length": max_alt_ngram,
        "alternatives": alt_title_rows,
        "source_file": prompt.get("_source_file"),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["risk_level"] for row in rows)
    provider_dependency_count = sum(1 for row in rows if row.get("provider_dependency_cue"))
    provider_cue_counts = Counter(row.get("provider_cue_status", "not_recorded") for row in rows)
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        family_counts[row["family"]][row["risk_level"]] += 1

    critical = [row for row in rows if row["risk_level"] == "critical"]
    high = [row for row in rows if row["risk_level"] == "high"]

    # Pass means there is no direct skill-name leak and high-risk title/phrase
    # leakage is small enough to handle by manual review rather than benchmark rewrite.
    pass_prompt_leakage = not critical and len(high) <= max(3, int(len(rows) * 0.15))

    return {
        "pass_prompt_leakage": pass_prompt_leakage,
        "total_prompts": len(rows),
        "risk_counts": dict(counts),
        "provider_dependency_cue_count": provider_dependency_count,
        "provider_cue_counts": dict(provider_cue_counts),
        "critical_count": len(critical),
        "high_count": len(high),
        "family_counts": {family: dict(counter) for family, counter in sorted(family_counts.items())},
    }


def render_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# Prompt Leakage Report")
    lines.append("")
    lines.append(
        "This report checks whether prompts accidentally reveal the gold skill through exact skill names, dominant skill-title words, or copied phrases from the gold skill card."
    )
    lines.append("")
    lines.append("## Overall Status")
    lines.append("")
    status = "PASS" if summary["pass_prompt_leakage"] else "REVIEW"
    lines.append(f"- Prompt leakage status: **{status}**")
    lines.append(f"- Total prompts: {summary['total_prompts']}")
    lines.append(f"- Critical exact-name leaks: {summary['critical_count']}")
    lines.append(f"- High-risk title/phrase leaks: {summary['high_count']}")
    lines.append(f"- Provider/tool dependency cues reclassified as low risk: {summary['provider_dependency_cue_count']}")
    if summary.get("provider_cue_counts"):
        cue_parts = [f"{name}: {count}" for name, count in sorted(summary["provider_cue_counts"].items())]
        lines.append(f"- Provider cue status: {', '.join(cue_parts)}")
    for level in ["critical", "high", "medium", "low"]:
        lines.append(f"- {level.title()} risk prompts: {summary['risk_counts'].get(level, 0)}")
    lines.append("")
    lines.append(
        "Interpretation: critical leaks are exact gold skill-name leaks. High-risk cases usually contain distinctive gold title words or copied gold-card phrases that may make lexical selectors look better than they really are."
    )
    lines.append(
        "Provider/tool names are treated separately: when a public skill is provider-specific, terms such as OpenAI, Claude, Obsidian, GitHub, or Playwright are valid dependency cues unless the prompt names the exact skill or lacks procedural support."
    )
    lines.append("")
    lines.append("## Family Summary")
    lines.append("")
    lines.append("| Family | Critical | High | Medium | Low |")
    lines.append("|---|---:|---:|---:|---:|")
    for family, counts in summary["family_counts"].items():
        lines.append(
            f"| `{family}` | {counts.get('critical', 0)} | {counts.get('high', 0)} | {counts.get('medium', 0)} | {counts.get('low', 0)} |"
        )
    lines.append("")

    attention = [row for row in rows if row["risk_level"] in {"critical", "high", "medium"}]
    attention.sort(key=lambda row: {"critical": 0, "high": 1, "medium": 2, "low": 3}[row["risk_level"]])
    lines.append("## Prompts To Review")
    lines.append("")
    if not attention:
        lines.append("No prompts require leakage review.")
    else:
        lines.append("| Risk | Prompt | Gold | Gold title hits | Advantage | Shared phrase | Flags |")
        lines.append("|---|---|---|---|---:|---|---|")
        for row in attention:
            hits = ", ".join(row["gold_title_hits"]) or "-"
            flags = ", ".join(row["risk_flags"]) or "-"
            phrase = row["gold_shared_phrase"] or "-"
            lines.append(
                f"| {row['risk_level']} | `{row['id']}` | `{row['gold_skill']}` | {hits} | {row['title_recall_advantage']:.2f} | {phrase} | {flags} |"
            )
    lines.append("")
    lines.append("## Prompt Detail")
    lines.append("")
    for row in rows:
        lines.append(f"### `{row['id']}`")
        lines.append("")
        lines.append(f"- Family: `{row['family']}`")
        lines.append(f"- Gold skill: `{row['gold_skill']}`")
        lines.append(f"- Risk level: **{row['risk_level']}**")
        lines.append(f"- Risk flags: {', '.join(row['risk_flags']) or '-'}")
        lines.append(f"- Provider cue status: {row['provider_cue_status']}")
        lines.append(f"- Prompt information level: {row['prompt_information_level']}")
        lines.append(f"- Instruction used for scoring: {row['instruction_text']}")
        lines.append(
            f"- Gold title overlap: {row['gold_title_recall']:.2f}; max alternative title overlap: {row['max_alternative_title_recall']:.2f}; advantage: {row['title_recall_advantage']:.2f}"
        )
        lines.append(f"- Gold title hits: {', '.join(row['gold_title_hits']) or '-'}")
        lines.append(f"- Longest copied gold phrase: {row['gold_shared_phrase'] or '-'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze prompt leakage against gold skill labels.")
    parser.add_argument("--prompts", default="skill_benchmark/prompts/*.json")
    parser.add_argument("--representations", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--output-md", default="skill_benchmark/outputs/prompt_leakage_report.md")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/prompt_leakage_report.json")
    args = parser.parse_args()

    prompts = load_prompts(args.prompts)
    skills = {row["name"]: row for row in load_jsonl(Path(args.representations))}
    missing = sorted({prompt["gold_skill"] for prompt in prompts} - set(skills))
    if missing:
        raise ValueError(f"Missing gold skills in representation file: {missing}")

    rows = [analyze_prompt(prompt, skills) for prompt in prompts]
    summary = summarize(rows)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps({"summary": summary, "prompts": rows}, indent=2), encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(summary, rows), encoding="utf-8")

    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    status = "PASS" if summary["pass_prompt_leakage"] else "REVIEW"
    print(f"Prompt leakage status: {status}")
    print(f"Critical exact-name leaks: {summary['critical_count']}")
    print(f"High-risk leaks: {summary['high_count']}")


if __name__ == "__main__":
    main()
