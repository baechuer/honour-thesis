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
    "above",
    "across",
    "after",
    "against",
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
    "do",
    "does",
    "doing",
    "else",
    "for",
    "from",
    "has",
    "have",
    "if",
    "in",
    "include",
    "includes",
    "including",
    "into",
    "is",
    "it",
    "keep",
    "main",
    "may",
    "md",
    "more",
    "must",
    "needed",
    "needs",
    "not",
    "of",
    "on",
    "one",
    "only",
    "or",
    "other",
    "output",
    "rather",
    "requested",
    "result",
    "return",
    "see",
    "should",
    "skill",
    "something",
    "source",
    "specific",
    "task",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "this",
    "to",
    "unless",
    "use",
    "used",
    "user",
    "using",
    "when",
    "where",
    "while",
    "with",
    "without",
    "workflow",
    "wants",
}


AXIS_DEFINITIONS = {
    "input_or_precondition": {
        "label": "input/precondition",
        "fields": ["use_when", "preconditions"],
        "threshold": 0.55,
        "primary": True,
    },
    "output_artifact": {
        "label": "output artifact",
        "fields": ["output_shape"],
        "threshold": 0.60,
        "primary": True,
    },
    "workflow": {
        "label": "workflow",
        "fields": ["workflow"],
        "threshold": 0.62,
        "primary": True,
    },
    "success_criterion": {
        "label": "success criterion",
        "fields": ["output_shape", "writing_rules"],
        "threshold": 0.62,
        "primary": True,
    },
    "dependency_or_resource": {
        "label": "dependency/resource",
        "fields": ["dependency_profile", "external_dependencies", "resource_signals", "resource_files"],
        "threshold": 0.85,
        "primary": True,
    },
    "boundary_signal": {
        "label": "avoid/not-for boundary",
        "fields": ["not_for"],
        "threshold": 0.78,
        "primary": False,
    },
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


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9_\-']*", text.lower())
    normalized = {token.strip("_-'") for token in tokens}
    return {token for token in normalized if len(token) > 2 and token not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def sample_terms(a: set[str], b: set[str], limit: int = 6) -> dict[str, list[str]]:
    return {
        "gold_only": sorted(a - b)[:limit],
        "alternative_only": sorted(b - a)[:limit],
    }


def compare_axis(gold: dict[str, Any], alternative: dict[str, Any], axis: str) -> dict[str, Any]:
    config = AXIS_DEFINITIONS[axis]
    gold_text = field_text(gold, config["fields"])
    alt_text = field_text(alternative, config["fields"])
    gold_tokens = tokenize(gold_text)
    alt_tokens = tokenize(alt_text)
    similarity = jaccard(gold_tokens, alt_tokens)
    has_signal = bool(gold_tokens or alt_tokens)

    if axis == "dependency_or_resource":
        gold_resources = set(flatten(gold.get("resource_files"))) | set(flatten(gold.get("external_dependencies")))
        alt_resources = set(flatten(alternative.get("resource_files"))) | set(flatten(alternative.get("external_dependencies")))
        resource_delta = gold_resources != alt_resources
        strong = has_signal and (similarity <= config["threshold"] or resource_delta)
    else:
        strong = has_signal and similarity <= config["threshold"]

    return {
        "axis": axis,
        "label": config["label"],
        "primary": config["primary"],
        "similarity": round(similarity, 3),
        "strong": bool(strong),
        "terms": sample_terms(gold_tokens, alt_tokens),
    }


def compare_pair(gold: dict[str, Any], alternative: dict[str, Any]) -> dict[str, Any]:
    axes = {axis: compare_axis(gold, alternative, axis) for axis in AXIS_DEFINITIONS}
    primary_strong = [axis for axis, result in axes.items() if result["strong"] and result["primary"]]
    supporting_strong = [axis for axis, result in axes.items() if result["strong"] and not result["primary"]]
    strong_count = len(primary_strong)
    supporting_count = len(supporting_strong)
    pass_step_2 = strong_count >= 1
    high_value = strong_count >= 2

    return {
        "gold_skill": gold["skill"],
        "alternative_skill": alternative["skill"],
        "family": gold.get("family"),
        "strong_axes": primary_strong,
        "supporting_axes": supporting_strong,
        "strong_axis_count": strong_count,
        "supporting_axis_count": supporting_count,
        "pass_step_2": pass_step_2,
        "high_value_pair": high_value,
        "manual_review": not high_value,
        "axes": axes,
    }


def evaluate(prompts: list[dict[str, Any]], rows_by_skill: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    evaluations: list[dict[str, Any]] = []
    for prompt in prompts:
        gold_id = prompt["gold_skill"]
        if gold_id not in rows_by_skill:
            raise KeyError(f"Missing gold skill {gold_id!r} for prompt {prompt['id']}")
        gold = rows_by_skill[gold_id]
        pair_results = []
        for alt_id in prompt.get("closest_alternatives", []):
            if alt_id not in rows_by_skill:
                raise KeyError(f"Missing alternative skill {alt_id!r} for prompt {prompt['id']}")
            pair_results.append(compare_pair(gold, rows_by_skill[alt_id]))

        evaluations.append(
            {
                "id": prompt["id"],
                "family": prompt.get("family"),
                "prompt": prompt.get("prompt"),
                "gold_skill": gold_id,
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "source_file": prompt.get("_source_file"),
                "pairs": pair_results,
                "pass_step_2": all(pair["pass_step_2"] for pair in pair_results),
                "high_value_prompt": all(pair["high_value_pair"] for pair in pair_results),
                "weak_pair_count": sum(1 for pair in pair_results if pair["manual_review"]),
            }
        )
    return evaluations


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/0"
    return f"{numerator}/{denominator} ({numerator / denominator:.1%})"


def status_label(prompt_pass: int, prompt_total: int, strong_pairs: int, pair_total: int) -> str:
    prompt_rate = prompt_pass / prompt_total if prompt_total else 0.0
    strong_rate = strong_pairs / pair_total if pair_total else 0.0
    if prompt_rate == 1.0 and strong_rate >= 0.8:
        return "PASS"
    if prompt_rate >= 0.95 and strong_rate >= 0.65:
        return "WARN"
    return "FAIL"


def terms_cell(terms: dict[str, list[str]]) -> str:
    gold = ", ".join(terms["gold_only"][:4]) or "-"
    alt = ", ".join(terms["alternative_only"][:4]) or "-"
    return f"gold: {gold}; alt: {alt}"


def write_markdown(evaluations: list[dict[str, Any]], path: Path) -> None:
    all_pairs = [pair for prompt in evaluations for pair in prompt["pairs"]]
    prompt_total = len(evaluations)
    pair_total = len(all_pairs)
    prompt_pass = sum(1 for prompt in evaluations if prompt["pass_step_2"])
    pair_pass = sum(1 for pair in all_pairs if pair["pass_step_2"])
    high_value_pairs = sum(1 for pair in all_pairs if pair["high_value_pair"])
    high_value_prompts = sum(1 for prompt in evaluations if prompt["high_value_prompt"])
    status = status_label(prompt_pass, prompt_total, high_value_pairs, pair_total)

    axis_counts = Counter(axis for pair in all_pairs for axis in pair["strong_axes"])
    supporting_counts = Counter(axis for pair in all_pairs for axis in pair["supporting_axes"])
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for prompt in evaluations:
        by_family[prompt["family"]].append(prompt)

    weak_pairs = sorted(
        [pair | {"prompt_id": prompt["id"]} for prompt in evaluations for pair in prompt["pairs"] if pair["manual_review"]],
        key=lambda pair: (pair["strong_axis_count"], pair["family"], pair["prompt_id"], pair["alternative_skill"]),
    )

    lines = [
        "# Procedural Distinctness Report",
        "",
        "This report implements Step 2 of the benchmark rubric: each gold skill should be procedurally distinguishable from its closest alternatives before we test semantic confusability or retrieval accuracy.",
        "",
        "Important interpretation: `not_for` boundaries are treated as supporting evidence, not as a primary reason by themselves. This prevents the benchmark from passing only because a skill contains a negated rule.",
        "",
        "## Overall Status",
        "",
        f"- Step 2 status: **{status}**",
        f"- Prompts with at least one primary procedural differentiator for every alternative: {pct(prompt_pass, prompt_total)}",
        f"- Gold/alternative pairs with at least one primary differentiator: {pct(pair_pass, pair_total)}",
        f"- Gold/alternative pairs with two or more primary differentiators: {pct(high_value_pairs, pair_total)}",
        f"- Prompts where all listed alternatives differ on two or more primary axes: {pct(high_value_prompts, prompt_total)}",
        "",
        "Pass rule used here: every pair needs at least one primary procedural axis; the benchmark is considered strong when at least 80% of pairs have two or more primary axes.",
        "",
        "What this proves: the current controlled skills expose positive procedural differences in their structured fields. What it does not prove yet: that flat metadata, embeddings, tree routing, graph retrieval, or rerankers will recover those differences under semantic similarity and scale. That is tested in later rubric steps.",
        "",
        "Why Step 2 was previously unresolved: the coverage report showed that fields existed, but it did not compare each gold skill against its listed near alternatives. This report performs that pair-level check.",
        "",
        "## Axis Frequency",
        "",
        "| Primary axis | Pair count |",
        "|---|---:|",
    ]
    for axis, config in AXIS_DEFINITIONS.items():
        if config["primary"]:
            lines.append(f"| {config['label']} | {axis_counts.get(axis, 0)} |")

    lines.extend(["", "| Supporting boundary axis | Pair count |", "|---|---:|"])
    for axis, config in AXIS_DEFINITIONS.items():
        if not config["primary"]:
            lines.append(f"| {config['label']} | {supporting_counts.get(axis, 0)} |")

    lines.extend(["", "## Family Summary", "", "| Family | Prompts | Prompt pass | Strong prompts | Weak pairs |", "|---|---:|---:|---:|---:|"])
    for family in sorted(by_family):
        family_prompts = by_family[family]
        family_pairs = [pair for prompt in family_prompts for pair in prompt["pairs"]]
        lines.append(
            f"| {family} | {len(family_prompts)} | "
            f"{sum(1 for prompt in family_prompts if prompt['pass_step_2'])}/{len(family_prompts)} | "
            f"{sum(1 for prompt in family_prompts if prompt['high_value_prompt'])}/{len(family_prompts)} | "
            f"{sum(1 for pair in family_pairs if pair['manual_review'])}/{len(family_pairs)} |"
        )

    lines.extend(["", "## Weak Or Review-Worthy Pairs", ""])
    if not weak_pairs:
        lines.append("- No weak pairs under the current heuristic.")
    else:
        lines.append("These are not automatically bad; they are the first pairs to inspect manually because they have fewer than two primary procedural differentiators.")
        lines.extend(["", "| Prompt | Gold | Alternative | Primary axes | Supporting axes | Main evidence |", "|---|---|---|---|---|---|"])
        for pair in weak_pairs[:80]:
            strongest_axis = next(iter(pair["strong_axes"]), "boundary_signal")
            evidence = pair["axes"].get(strongest_axis, pair["axes"]["boundary_signal"])
            primary = ", ".join(AXIS_DEFINITIONS[axis]["label"] for axis in pair["strong_axes"]) or "-"
            supporting = ", ".join(AXIS_DEFINITIONS[axis]["label"] for axis in pair["supporting_axes"]) or "-"
            lines.append(
                f"| `{pair['prompt_id']}` | `{pair['gold_skill']}` | `{pair['alternative_skill']}` | "
                f"{primary} | {supporting} | {terms_cell(evidence['terms'])} |"
            )

    lines.extend(["", "## Prompt Detail", ""])
    for prompt in sorted(evaluations, key=lambda row: (row["family"], row["id"])):
        status = "PASS" if prompt["pass_step_2"] else "FAIL"
        strength = "strong" if prompt["high_value_prompt"] else "needs review"
        lines.extend(
            [
                f"### `{prompt['id']}`",
                "",
                f"- Family: `{prompt['family']}`",
                f"- Gold skill: `{prompt['gold_skill']}`",
                f"- Status: {status}; {strength}",
                "",
                "| Alternative | Primary axes | Supporting axes | Axis similarities |",
                "|---|---|---|---|",
            ]
        )
        for pair in prompt["pairs"]:
            primary = ", ".join(AXIS_DEFINITIONS[axis]["label"] for axis in pair["strong_axes"]) or "-"
            supporting = ", ".join(AXIS_DEFINITIONS[axis]["label"] for axis in pair["supporting_axes"]) or "-"
            similarities = ", ".join(
                f"{AXIS_DEFINITIONS[axis]['label']}={pair['axes'][axis]['similarity']:.2f}"
                for axis in AXIS_DEFINITIONS
            )
            lines.append(f"| `{pair['alternative_skill']}` | {primary} | {supporting} | {similarities} |")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Analyze procedural distinctness between gold skills and confusable alternatives.")
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
        default=repo_root / "outputs" / "procedural_distinctness_report.md",
        help="Markdown report path.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=repo_root / "outputs" / "procedural_distinctness_report.json",
        help="Machine-readable report path.",
    )
    args = parser.parse_args()

    rows = load_jsonl(args.representations / "R3_dependency_resource_aware.jsonl")
    rows_by_skill = {row["skill"]: row for row in rows}
    prompts = load_prompts(args.prompts_glob)
    evaluations = evaluate(prompts, rows_by_skill)

    write_markdown(evaluations, args.markdown_output)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(evaluations, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_pairs = [pair for prompt in evaluations for pair in prompt["pairs"]]
    prompt_pass = sum(1 for prompt in evaluations if prompt["pass_step_2"])
    high_value_pairs = sum(1 for pair in all_pairs if pair["high_value_pair"])
    print(f"Wrote {args.markdown_output}")
    print(f"Wrote {args.json_output}")
    print(f"Prompt pass: {prompt_pass}/{len(evaluations)}")
    print(f"Pairs with 2+ primary axes: {high_value_pairs}/{len(all_pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
