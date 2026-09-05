#!/usr/bin/env python3

from __future__ import annotations

import argparse
import collections
import glob
import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_prompts(pattern: str) -> dict[str, dict[str, Any]]:
    prompts: dict[str, dict[str, Any]] = {}
    for path in sorted(glob.glob(pattern)):
        data = load_json(path)
        if isinstance(data, list):
            for row in data:
                prompts[row["id"]] = row
    return prompts


def normalize_rows(data: dict[str, Any], result_key: str | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if isinstance(data.get("results"), list):
        return data["results"], data.get("metrics", {})
    if isinstance(data.get("results"), dict):
        key = result_key
        if key is None:
            summary = data.get("summary") or []
            key = summary[0]["result_key"] if summary else next(iter(data["results"]))
        rows = data["results"][key]
        metrics = {}
        for item in data.get("summary", []):
            if item.get("result_key") == key:
                metrics = item.get("metrics", {})
                break
        return rows, metrics
    raise ValueError("Unsupported result JSON shape: expected results list or results dict")


def acceptable_sets(path: str | None) -> dict[str, dict[str, set[str]]]:
    if not path:
        return {}
    raw = load_json(path)
    out: dict[str, dict[str, set[str]]] = {}
    for prompt_id, values in raw.items():
        out[prompt_id] = {
            "acceptable": set(values.get("acceptable", [])),
            "borderline": set(values.get("borderline", [])),
        }
    return out


def skill_kind(name: str | None, r1: dict[str, dict[str, Any]]) -> str:
    if not name:
        return "none"
    meta = r1.get(name, {})
    if name.startswith("public-"):
        return "public_import"
    if meta.get("is_main_evaluated"):
        return "main_evaluated"
    if name.startswith("psc-"):
        return "public_style_controlled"
    return "background_or_support"


def row_ranking(row: dict[str, Any]) -> list[str]:
    ranking = row.get("ranking") or []
    out: list[str] = []
    for item in ranking:
        if isinstance(item, dict):
            out.append(item.get("skill"))
        else:
            out.append(item)
    return [name for name in out if name]


def failure_bucket(
    row: dict[str, Any],
    top1: str | None,
    r1: dict[str, dict[str, Any]],
    acceptables: dict[str, dict[str, set[str]]],
) -> tuple[str, str]:
    gold = row["gold_skill"]
    prompt_id = row["prompt_id"]
    closest = set(row.get("closest_alternatives", []))
    acceptable = {gold} | acceptables.get(prompt_id, {}).get("acceptable", set())
    borderline = acceptables.get(prompt_id, {}).get("borderline", set())
    if top1 == gold:
        return "correct", "gold"
    if top1 in acceptable:
        return "acceptable", "acceptable_alt"
    if top1 in borderline:
        return "borderline", "borderline_alt"

    candidate_count = int(row.get("candidate_count") or len(row_ranking(row)) or 0)
    first_stage_rank = row.get("gold_first_stage_rank")
    final_rank = row.get("gold_final_rank")
    if first_stage_rank is None or (candidate_count and first_stage_rank > candidate_count):
        stage = "first_stage_exclusion"
    elif final_rank is None:
        stage = "reranker_misorder"
    else:
        stage = "reranker_misorder"

    if top1 in closest:
        subtype = "listed_near_alt"
    elif skill_kind(top1, r1) == "public_import":
        subtype = "public_import_win"
    elif skill_kind(top1, r1) == "public_style_controlled":
        subtype = "public_style_controlled_win"
    elif r1.get(top1, {}).get("family") == row.get("family"):
        subtype = "same_family"
    elif skill_kind(top1, r1) == "background_or_support":
        subtype = "background_or_support_win"
    else:
        subtype = "other"
    return stage, subtype


def summarize(
    rows: list[dict[str, Any]],
    prompts: dict[str, dict[str, Any]],
    r1: dict[str, dict[str, Any]],
    acceptables: dict[str, dict[str, set[str]]],
    metrics: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    bucket_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    family_errors: collections.Counter[str] = collections.Counter()
    family_totals: collections.Counter[str] = collections.Counter()
    confusions: collections.Counter[tuple[str, str]] = collections.Counter()
    prompt_level_counts: collections.Counter[str] = collections.Counter()
    provider_cue_counts: collections.Counter[str] = collections.Counter()
    examples: list[dict[str, Any]] = []

    strict_top1 = 0
    acceptable_top1 = 0
    top5 = 0
    first_stage_exclusions = 0
    reranker_misorders = 0

    for row in rows:
        prompt_id = row["prompt_id"]
        prompt = prompts.get(prompt_id, {})
        ranking = row_ranking(row)
        top1 = ranking[0] if ranking else None
        gold = row["gold_skill"]
        acceptable = {gold} | acceptables.get(prompt_id, {}).get("acceptable", set())
        family = row.get("family") or prompt.get("family") or "unknown"
        family_totals[family] += 1
        if top1 == gold:
            strict_top1 += 1
        if top1 in acceptable:
            acceptable_top1 += 1
        if gold in ranking[:5]:
            top5 += 1

        stage, subtype = failure_bucket(row, top1, r1, acceptables)
        bucket_counts[(stage, subtype)] += 1
        if stage == "first_stage_exclusion":
            first_stage_exclusions += 1
        if stage == "reranker_misorder":
            reranker_misorders += 1
        if stage not in {"correct", "acceptable", "borderline"}:
            family_errors[family] += 1
            confusions[(gold, top1 or "<none>")] += 1
            prompt_level_counts[prompt.get("prompt_information_level", "unknown")] += 1
            provider_cue_counts[prompt.get("provider_cue_status", "unknown")] += 1
            if len(examples) < 15:
                examples.append(
                    {
                        "prompt_id": prompt_id,
                        "family": family,
                        "gold": gold,
                        "top1": top1,
                        "bucket": f"{stage}:{subtype}",
                        "gold_first_stage_rank": row.get("gold_first_stage_rank"),
                        "gold_final_rank": row.get("gold_final_rank"),
                        "first_stage_top1": row.get("first_stage_top1"),
                        "closest_alternatives": row.get("closest_alternatives", []),
                        "prompt": prompt.get("prompt") or row.get("instruction_text", ""),
                    }
                )

    n = len(rows)
    worst_families = []
    for family, err in family_errors.most_common():
        total = family_totals[family]
        worst_families.append(
            {
                "family": family,
                "errors": err,
                "total": total,
                "error_rate": round(err / total, 4) if total else 0.0,
            }
        )

    return {
        "label": label,
        "total": n,
        "metrics_from_file": metrics,
        "recomputed": {
            "strict_top1": round(strict_top1 / n, 4) if n else 0.0,
            "acceptable_top1": round(acceptable_top1 / n, 4) if n else 0.0,
            "strict_top5": round(top5 / n, 4) if n else 0.0,
            "first_stage_exclusion_rate": round(first_stage_exclusions / n, 4) if n else 0.0,
            "reranker_misorder_rate": round(reranker_misorders / n, 4) if n else 0.0,
        },
        "failure_buckets": [
            {"bucket": stage, "subtype": subtype, "count": count, "rate": round(count / n, 4)}
            for (stage, subtype), count in bucket_counts.most_common()
        ],
        "worst_families": worst_families[:15],
        "top_confusions": [
            {"gold": gold, "top1": top1, "count": count}
            for (gold, top1), count in confusions.most_common(20)
        ],
        "failure_by_prompt_information_level": dict(prompt_level_counts.most_common()),
        "failure_by_provider_cue_status": dict(provider_cue_counts.most_common()),
        "examples": examples,
    }


def render_md(report: dict[str, Any]) -> str:
    lines = [f"# Failure Mode Analysis: {report['label']}", ""]
    r = report["recomputed"]
    lines += [
        "## Summary",
        "",
        f"- Total prompts: {report['total']}",
        f"- Strict top-1: {r['strict_top1']:.1%}",
        f"- Acceptable top-1: {r['acceptable_top1']:.1%}",
        f"- Strict top-5: {r['strict_top5']:.1%}",
        f"- First-stage exclusion rate: {r['first_stage_exclusion_rate']:.1%}",
        f"- Reranker/order failure rate: {r['reranker_misorder_rate']:.1%}",
        "",
        "## Failure Buckets",
        "",
        "| Bucket | Subtype | Count | Rate |",
        "|---|---|---:|---:|",
    ]
    for item in report["failure_buckets"]:
        lines.append(f"| {item['bucket']} | {item['subtype']} | {item['count']} | {item['rate']:.1%} |")
    lines += ["", "## Worst Families", "", "| Family | Errors | Total | Error rate |", "|---|---:|---:|---:|"]
    for item in report["worst_families"]:
        lines.append(f"| {item['family']} | {item['errors']} | {item['total']} | {item['error_rate']:.1%} |")
    lines += ["", "## Top Confusions", "", "| Gold | Top-1 | Count |", "|---|---|---:|"]
    for item in report["top_confusions"]:
        lines.append(f"| `{item['gold']}` | `{item['top1']}` | {item['count']} |")
    if report["failure_by_prompt_information_level"]:
        lines += ["", "## Failure By Prompt Information Level", ""]
        for key, value in report["failure_by_prompt_information_level"].items():
            lines.append(f"- {key}: {value}")
    if report["failure_by_provider_cue_status"]:
        lines += ["", "## Failure By Provider Cue Status", ""]
        for key, value in report["failure_by_provider_cue_status"].items():
            lines.append(f"- {key}: {value}")
    lines += ["", "## Example Failures", ""]
    for ex in report["examples"]:
        lines.append(
            f"- `{ex['prompt_id']}`: gold `{ex['gold']}`, top-1 `{ex['top1']}`, "
            f"bucket `{ex['bucket']}`, first-stage rank `{ex['gold_first_stage_rank']}`, "
            f"final rank `{ex['gold_final_rank']}`."
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze selector failure modes from benchmark result JSON.")
    parser.add_argument("--result-json", required=True)
    parser.add_argument("--result-key", help="For M6 result files with multiple field-set result keys.")
    parser.add_argument("--prompts", required=True, help="Prompt glob used by the result file.")
    parser.add_argument("--acceptable-alternatives")
    parser.add_argument("--r1", default="skill_benchmark/representations/R1_flat_metadata.jsonl")
    parser.add_argument("--label", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    data = load_json(args.result_json)
    rows, metrics = normalize_rows(data, args.result_key)
    prompts = load_prompts(args.prompts)
    r1 = {row["name"]: row for row in load_jsonl(args.r1)}
    acceptables = acceptable_sets(args.acceptable_alternatives)
    report = summarize(rows, prompts, r1, acceptables, metrics, args.label)
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(report, indent=2), encoding="utf-8")
    Path(args.output_md).write_text(render_md(report), encoding="utf-8")
    print(render_md(report))


if __name__ == "__main__":
    main()
