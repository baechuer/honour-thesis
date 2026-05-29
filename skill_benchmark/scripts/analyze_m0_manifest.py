#!/usr/bin/env python3

import argparse
import csv
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def parse_selected(raw: str) -> list[str]:
    if not raw:
        return []
    return [part for part in raw.split("|") if part]


def load_prompt_sources(patterns: list[str]) -> dict[str, dict[str, Any]]:
    prompts: dict[str, dict[str, Any]] = {}
    for pattern in patterns:
        paths = sorted(glob.glob(pattern))
        if not paths:
            raise FileNotFoundError(f"No prompt files matched: {pattern}")
        for path in paths:
            with Path(path).open("r", encoding="utf-8") as f:
                rows = json.load(f)
            for row in rows:
                prompt_id = row["id"]
                if prompt_id in prompts:
                    raise ValueError(f"Duplicate prompt id: {prompt_id}")
                prompts[prompt_id] = row
    return prompts


def load_acceptables(path: Path | None) -> dict[str, dict[str, set[str]]]:
    if path is None or not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return {
        prompt_id: {
            "acceptable": set(row.get("acceptable", [])),
            "borderline": set(row.get("borderline", [])),
        }
        for prompt_id, row in raw.items()
    }


def pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def score_rows(
    rows: list[dict[str, str]],
    prompts: dict[str, dict[str, Any]],
    acceptables: dict[str, dict[str, set[str]]],
) -> dict[str, Any]:
    total = len(rows)
    counters: Counter[str] = Counter()
    docs_loaded_total = 0
    exit_codes: Counter[str] = Counter()
    top1_confusions: Counter[str] = Counter()
    by_family: dict[str, Counter[str]] = defaultdict(Counter)
    prompt_results: list[dict[str, Any]] = []

    for row in rows:
        prompt_id = row["prompt_id"]
        prompt_meta = prompts.get(prompt_id, {})
        family = prompt_meta.get("family", "<unknown>")
        gold = row["gold_skill"]
        selected = parse_selected(row.get("selected_skills", ""))
        top1 = selected[0] if selected else ""
        acceptable_set = {gold, *acceptables.get(prompt_id, {}).get("acceptable", set())}
        borderline_set = acceptables.get(prompt_id, {}).get("borderline", set())

        docs_loaded_total += len(selected)
        exit_codes[row.get("exit_code", "")] += 1
        counters["total"] += 1
        by_family[family]["total"] += 1

        if not selected:
            status = "no_explicit_skill"
            counters["no_explicit_skill"] += 1
            by_family[family]["no_explicit_skill"] += 1
        elif top1 == gold:
            status = "gold"
            counters["strict_top1"] += 1
            counters["acceptable_top1"] += 1
            by_family[family]["strict_top1"] += 1
            by_family[family]["acceptable_top1"] += 1
        elif top1 in acceptable_set:
            status = "acceptable"
            counters["acceptable_top1"] += 1
            by_family[family]["acceptable_top1"] += 1
        elif top1 in borderline_set:
            status = "borderline"
            counters["borderline_top1"] += 1
            by_family[family]["borderline_top1"] += 1
            top1_confusions[f"{gold} -> {top1}"] += 1
        else:
            status = "wrong"
            counters["wrong_top1"] += 1
            by_family[family]["wrong_top1"] += 1
            top1_confusions[f"{gold} -> {top1 or '<none>'}"] += 1

        if selected and gold in selected:
            counters["strict_any_hit"] += 1
            by_family[family]["strict_any_hit"] += 1
        if selected and any(skill in acceptable_set for skill in selected):
            counters["acceptable_any_hit"] += 1
            by_family[family]["acceptable_any_hit"] += 1
        if len(selected) > 1:
            counters["multi_skill"] += 1
            by_family[family]["multi_skill"] += 1

        prompt_results.append(
            {
                "prompt_id": prompt_id,
                "family": family,
                "gold": gold,
                "selected": selected,
                "top1": top1 or "<none>",
                "status": status,
                "strict_any_hit": gold in selected,
                "acceptable_any_hit": any(skill in acceptable_set for skill in selected),
                "exit_code": row.get("exit_code", ""),
            }
        )

    family_metrics = {}
    for family, family_counter in sorted(by_family.items()):
        family_total = family_counter["total"]
        family_metrics[family] = {
            "total": family_total,
            "strict_top1": pct(family_counter["strict_top1"], family_total),
            "acceptable_top1": pct(family_counter["acceptable_top1"], family_total),
            "strict_any_hit": pct(family_counter["strict_any_hit"], family_total),
            "acceptable_any_hit": pct(family_counter["acceptable_any_hit"], family_total),
            "no_explicit_skill": pct(family_counter["no_explicit_skill"], family_total),
            "multi_skill": pct(family_counter["multi_skill"], family_total),
        }

    return {
        "total_runs": total,
        "unique_prompts": len({row["prompt_id"] for row in rows}),
        "strict_top1_accuracy": pct(counters["strict_top1"], total),
        "acceptable_top1_accuracy": pct(counters["acceptable_top1"], total),
        "strict_any_hit": pct(counters["strict_any_hit"], total),
        "acceptable_any_hit": pct(counters["acceptable_any_hit"], total),
        "no_explicit_skill_rate": pct(counters["no_explicit_skill"], total),
        "wrong_top1_rate": pct(counters["wrong_top1"], total),
        "borderline_top1_rate": pct(counters["borderline_top1"], total),
        "multi_skill_rate": pct(counters["multi_skill"], total),
        "mean_full_docs_loaded": round(docs_loaded_total / total, 2) if total else 0,
        "exit_codes": dict(exit_codes),
        "family_metrics": family_metrics,
        "top1_confusions": [
            {"pair": pair, "count": count} for pair, count in top1_confusions.most_common(20)
        ],
        "prompt_results": prompt_results,
    }


def render_markdown(manifest: Path, metrics: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# M0 Progressive Disclosure Baseline Report")
    lines.append("")
    lines.append(f"- Manifest: `{manifest}`")
    lines.append(f"- Runs: {metrics['total_runs']}; unique prompts: {metrics['unique_prompts']}")
    lines.append(f"- Strict top-1 accuracy: {metrics['strict_top1_accuracy']:.1%}")
    lines.append(f"- Acceptable top-1 accuracy: {metrics['acceptable_top1_accuracy']:.1%}")
    lines.append(f"- Strict any-hit rate: {metrics['strict_any_hit']:.1%}")
    lines.append(f"- Acceptable any-hit rate: {metrics['acceptable_any_hit']:.1%}")
    lines.append(f"- No explicit skill loaded: {metrics['no_explicit_skill_rate']:.1%}")
    lines.append(f"- Wrong top-1 rate: {metrics['wrong_top1_rate']:.1%}")
    lines.append(f"- Mean full skill docs loaded: {metrics['mean_full_docs_loaded']}")
    lines.append(f"- Multi-skill consultation rate: {metrics['multi_skill_rate']:.1%}")
    lines.append("")
    lines.append("Interpretation: M0 measures the normal main-agent progressive-disclosure behavior. It is not a clean retriever-only test, because the main agent may answer directly, load no explicit skill, or load multiple full skill documents before responding.")
    lines.append("")
    lines.append("## By Family")
    lines.append("")
    lines.append("| Family | N | Strict Top-1 | Accept Top-1 | Strict Any-Hit | Accept Any-Hit | No Skill | Multi-Skill |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for family, row in metrics["family_metrics"].items():
        lines.append(
            f"| `{family}` | {row['total']} | {row['strict_top1']:.1%} | "
            f"{row['acceptable_top1']:.1%} | {row['strict_any_hit']:.1%} | "
            f"{row['acceptable_any_hit']:.1%} | {row['no_explicit_skill']:.1%} | "
            f"{row['multi_skill']:.1%} |"
        )
    lines.append("")
    lines.append("## Non-Gold Top-1 Outcomes")
    lines.append("")
    if metrics["top1_confusions"]:
        for item in metrics["top1_confusions"]:
            lines.append(f"- `{item['pair']}`: {item['count']}")
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Prompt-Level Results")
    lines.append("")
    lines.append("| Prompt | Family | Gold | Top-1 | Status | Selected Skills |")
    lines.append("|---|---|---|---|---|---|")
    for row in metrics["prompt_results"]:
        selected = ", ".join(f"`{skill}`" for skill in row["selected"]) or "`<none>`"
        lines.append(
            f"| `{row['prompt_id']}` | `{row['family']}` | `{row['gold']}` | "
            f"`{row['top1']}` | {row['status']} | {selected} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Analyze M0 progressive-disclosure manifest results.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=repo_root / "runtime" / "m0_results_core_current" / "manifest.csv",
    )
    parser.add_argument(
        "--prompts-glob",
        action="append",
        default=[str(repo_root / "prompts" / "*_confusability.json")],
    )
    parser.add_argument(
        "--acceptable-alternatives",
        type=Path,
        default=repo_root / "annotations" / "acceptable_alternatives.json",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=repo_root / "outputs" / "m0_progressive_disclosure_core_report.md",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=repo_root / "outputs" / "m0_progressive_disclosure_core_report.json",
    )
    args = parser.parse_args()

    prompts = load_prompt_sources(args.prompts_glob)
    acceptables = load_acceptables(args.acceptable_alternatives)
    rows = load_manifest(args.manifest)
    metrics = score_rows(rows, prompts, acceptables)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(args.manifest, metrics), encoding="utf-8")
    args.output_json.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Wrote {args.output_md}")
    print(f"Wrote {args.output_json}")
    print(
        "M0: "
        f"strict top1={metrics['strict_top1_accuracy']:.1%}, "
        f"accept top1={metrics['acceptable_top1_accuracy']:.1%}, "
        f"any-hit={metrics['strict_any_hit']:.1%}, "
        f"no-skill={metrics['no_explicit_skill_rate']:.1%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
