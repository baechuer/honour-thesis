#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_offline_selectors import (  # noqa: E402
    TfIdfScorer,
    approximate_tokens,
    bm25_scores,
    build_scale_skill_names,
    evaluate_rows,
    instruction_text,
    load_acceptables,
    load_jsonl,
    load_prompts,
    rank_scores,
)


ABLATIONS: list[dict[str, Any]] = [
    {
        "id": "a0_description",
        "label": "Description only",
        "r1": ["description"],
        "r2": [],
        "r3": [],
    },
    {
        "id": "a1_use_when",
        "label": "Description + use conditions",
        "r1": ["description"],
        "r2": ["use_when"],
        "r3": [],
    },
    {
        "id": "a2_preconditions",
        "label": "+ input / preconditions",
        "r1": ["description"],
        "r2": ["use_when", "preconditions"],
        "r3": [],
    },
    {
        "id": "a3_outputs",
        "label": "+ output artifacts",
        "r1": ["description"],
        "r2": ["use_when", "preconditions", "output_shape"],
        "r3": [],
    },
    {
        "id": "a4_workflow",
        "label": "+ workflow / procedure",
        "r1": ["description"],
        "r2": ["use_when", "preconditions", "output_shape", "workflow"],
        "r3": [],
    },
    {
        "id": "a5_constraints",
        "label": "+ constraints / not-for",
        "r1": ["description"],
        "r2": ["use_when", "preconditions", "output_shape", "workflow", "not_for"],
        "r3": [],
    },
    {
        "id": "a6_dependencies_resources",
        "label": "+ dependencies / resources",
        "r1": ["description"],
        "r2": ["use_when", "preconditions", "output_shape", "workflow", "not_for"],
        "r3": ["dependency_profile", "external_dependencies", "resource_signals", "resource_files"],
    },
]

SINGLE_FIELD_ABLATIONS: list[dict[str, Any]] = [
    {"id": "s_description", "label": "Single: description", "r1": ["description"], "r2": [], "r3": []},
    {"id": "s_use_when", "label": "Single: use_when", "r1": [], "r2": ["use_when"], "r3": []},
    {"id": "s_preconditions", "label": "Single: preconditions", "r1": [], "r2": ["preconditions"], "r3": []},
    {"id": "s_output", "label": "Single: output", "r1": [], "r2": ["output_shape"], "r3": []},
    {"id": "s_workflow", "label": "Single: workflow", "r1": [], "r2": ["workflow"], "r3": []},
    {"id": "s_not_for", "label": "Single: not_for", "r1": [], "r2": ["not_for"], "r3": []},
    {
        "id": "s_dependencies_resources",
        "label": "Single: dependencies/resources",
        "r1": [],
        "r2": [],
        "r3": ["dependency_profile", "external_dependencies", "resource_signals", "resource_files"],
    },
]


def field_text(row: dict[str, Any], keys: list[str]) -> str:
    parts: list[str] = []
    for key in keys:
        value = row.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value if str(item).strip())
        elif isinstance(value, dict):
            parts.append(json.dumps(value, sort_keys=True))
        elif value:
            parts.append(str(value))
    return "\n".join(parts)


def build_doc(
    skill_name: str,
    spec: dict[str, Any],
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
) -> str:
    parts = [f"name: {skill_name.replace('-', ' ')}"]
    r1_text = field_text(r1[skill_name], spec["r1"])
    r2_text = field_text(r2[skill_name], spec["r2"])
    r3_text = field_text(r3.get(skill_name, {}), spec["r3"])
    if r1_text:
        parts.append(r1_text)
    if r2_text:
        parts.append(r2_text)
    if r3_text:
        parts.append(r3_text)
    return "\n".join(parts)


def run_ablation(
    scorer_name: str,
    spec: dict[str, Any],
    prompts: list[dict[str, Any]],
    skill_names: list[str],
    docs: list[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    start = time.perf_counter()
    scorer = TfIdfScorer(docs) if scorer_name == "tfidf" else None
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        query = instruction_text(prompt["prompt"])
        if scorer_name == "bm25":
            scores = bm25_scores(query, docs)
        elif scorer_name == "tfidf":
            scores = scorer.scores(query)
        else:
            raise ValueError(f"Unknown scorer: {scorer_name}")
        ranking = rank_scores(skill_names, scores)
        rows.append(
            {
                "prompt_id": prompt["id"],
                "family": prompt["family"],
                "gold_skill": prompt["gold_skill"],
                "closest_alternatives": prompt.get("closest_alternatives", []),
                "instruction_text": query,
                "ablation_id": spec["id"],
                "ranking": [
                    {"skill": skill, "score": round(score, 6)}
                    for skill, score in ranking[:20]
                ],
            }
        )
    return rows, {"elapsed_ms": round((time.perf_counter() - start) * 1000, 2)}


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Representation Field Ablation Results",
        "",
        "This report tests which representation fields help retrieve the gold skill.",
        "",
        f"- Prompts: {result['prompt_count']}",
        f"- Ablations: {len(result['summary_rows'])}",
        "",
        "## Cumulative Field Ablations",
        "",
        "| Scorer | Scale | Field Set | Top-1 | Accept Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["summary_rows"]:
        if row["ablation_id"].startswith("s_"):
            continue
        metrics = row["metrics"]
        lines.append(
            f"| `{row['scorer']}` | `{row['scale']}` | {row['label']} | "
            f"{metrics['top1_accuracy']:.1%} | {metrics['acceptable_top1_accuracy']:.1%} | "
            f"{metrics['top5_recall']:.1%} | {metrics['mrr']:.3f} | "
            f"{metrics['non_main_top1_rate']:.1%} | {metrics['selector_visible_tokens_approx']} |"
        )

    lines.extend(
        [
            "",
            "## Single-Field Checks",
            "",
            "| Scorer | Scale | Field | Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |",
            "|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in result["summary_rows"]:
        if not row["ablation_id"].startswith("s_"):
            continue
        metrics = row["metrics"]
        lines.append(
            f"| `{row['scorer']}` | `{row['scale']}` | {row['label']} | "
            f"{metrics['top1_accuracy']:.1%} | {metrics['top5_recall']:.1%} | "
            f"{metrics['mrr']:.3f} | {metrics['non_main_top1_rate']:.1%} | "
            f"{metrics['selector_visible_tokens_approx']} |"
        )

    lines.extend(["", "## Initial Interpretation", ""])
    full_tfidf = [
        row
        for row in result["summary_rows"]
        if row["scale"] == "current_full" and row["scorer"] == "tfidf" and not row["ablation_id"].startswith("s_")
    ]
    if full_tfidf:
        baseline = full_tfidf[0]["metrics"]["top1_accuracy"]
        best = max(full_tfidf, key=lambda row: row["metrics"]["top1_accuracy"])
        lines.append(
            f"- On full scale with TF-IDF, `{best['ablation_id']}` is strongest at "
            f"{best['metrics']['top1_accuracy']:.1%} top-1, compared with "
            f"{baseline:.1%} for description-only."
        )
    lines.append("- Treat these as local lexical ablations; they test representation content, not provider model strength.")
    lines.append("- If a field adds little in this report, it may still matter for execution, downstream validation, or neural reranking.")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local field ablations over skill representations.")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--r2", default="skill_benchmark/representations/R2_structured_procedural.jsonl")
    parser.add_argument("--r3", default="skill_benchmark/representations/R3_dependency_resource_aware.jsonl")
    parser.add_argument("--prompts-glob", default="skill_benchmark/prompts/*_confusability.json")
    parser.add_argument("--acceptables", default="skill_benchmark/annotations/acceptable_alternatives.json")
    parser.add_argument("--scales", default="core,current_full")
    parser.add_argument("--scorers", default="tfidf,bm25")
    parser.add_argument("--include-single", action="store_true")
    parser.add_argument("--output-json", default="skill_benchmark/outputs/field_ablation_results.json")
    parser.add_argument("--output-md", default="skill_benchmark/outputs/field_ablation_results.md")
    args = parser.parse_args()

    r1_rows = load_jsonl(Path(args.r1))
    r2_rows = load_jsonl(Path(args.r2))
    r3_rows = load_jsonl(Path(args.r3))
    r1 = {row["name"]: row for row in r1_rows}
    r2 = {row["name"]: row for row in r2_rows}
    r3 = {row["name"]: row for row in r3_rows}
    prompts = load_prompts(args.prompts_glob)
    acceptables = load_acceptables(Path(args.acceptables))
    scales = [item.strip() for item in args.scales.split(",") if item.strip()]
    scorers = [item.strip() for item in args.scorers.split(",") if item.strip()]
    ablations = [*ABLATIONS, *(SINGLE_FIELD_ABLATIONS if args.include_single else [])]

    summary_rows: list[dict[str, Any]] = []
    detailed_rows: dict[str, list[dict[str, Any]]] = {}
    for scale in scales:
        skill_names = build_scale_skill_names(scale, r1_rows)
        for spec in ablations:
            docs = [build_doc(skill, spec, r1, r2, r3) for skill in skill_names]
            visible_tokens = sum(approximate_tokens(doc) for doc in docs)
            for scorer in scorers:
                rows, timing = run_ablation(scorer, spec, prompts, skill_names, docs)
                metrics = evaluate_rows(rows, r1, len(skill_names), visible_tokens, acceptables)
                key = f"{scale}::{scorer}::{spec['id']}"
                detailed_rows[key] = rows
                summary_rows.append(
                    {
                        "scale": scale,
                        "scorer": scorer,
                        "ablation_id": spec["id"],
                        "label": spec["label"],
                        "fields": {"r1": spec["r1"], "r2": spec["r2"], "r3": spec["r3"]},
                        "timing": timing,
                        "metrics": metrics,
                    }
                )

    result = {
        "prompt_count": len(prompts),
        "summary_rows": summary_rows,
        "detailed_rows": detailed_rows,
    }
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(result), encoding="utf-8")
    print(f"Ran {len(summary_rows)} ablation conditions")
    print(f"Wrote {output_json}")
    print(f"Wrote {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
