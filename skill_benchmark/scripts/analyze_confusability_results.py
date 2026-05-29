#!/usr/bin/env python3

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def parse_selected_skills(raw: str) -> list[str]:
    if not raw:
        return []
    return [part for part in raw.split("|") if part]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize(rows: list[dict[str, str]]) -> str:
    by_prompt: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_prompt[row["prompt_id"]].append(row)

    total_runs = len(rows)
    exact_correct = 0
    any_hit = 0
    bypass = 0
    wrong = 0
    multi_skill = 0

    lines: list[str] = []
    lines.append("Overall")
    lines.append(f"- total runs: {total_runs}")

    for row in rows:
        gold = row["gold_skill"]
        selected = parse_selected_skills(row["selected_skills"])
        top1 = selected[0] if selected else None

        if not selected:
            bypass += 1
        if len(selected) >= 2:
            multi_skill += 1
        if gold in selected:
            any_hit += 1
        if top1 == gold:
            exact_correct += 1
        elif selected:
            wrong += 1

    if total_runs:
        lines.append(f"- top-1 accuracy: {exact_correct}/{total_runs} ({exact_correct / total_runs:.1%})")
        lines.append(f"- any-hit accuracy: {any_hit}/{total_runs} ({any_hit / total_runs:.1%})")
        lines.append(f"- bypass rate: {bypass}/{total_runs} ({bypass / total_runs:.1%})")
        lines.append(f"- wrong-skill rate: {wrong}/{total_runs} ({wrong / total_runs:.1%})")
        lines.append(
            f"- multi-skill consultation rate: {multi_skill}/{total_runs} ({multi_skill / total_runs:.1%})"
        )
    else:
        lines.append("- no runs found")

    lines.append("")
    lines.append("By Prompt")

    for prompt_id in sorted(by_prompt):
        prompt_rows = by_prompt[prompt_id]
        gold = prompt_rows[0]["gold_skill"]
        top1_counter: Counter[str] = Counter()
        any_counter: Counter[str] = Counter()
        prompt_bypass = 0
        prompt_multi_skill = 0

        for row in prompt_rows:
            selected = parse_selected_skills(row["selected_skills"])
            if not selected:
                prompt_bypass += 1
                top1_counter["<none>"] += 1
                continue

            if len(selected) >= 2:
                prompt_multi_skill += 1
            top1_counter[selected[0]] += 1
            for skill in selected:
                any_counter[skill] += 1

        total = len(prompt_rows)
        top1_correct = top1_counter.get(gold, 0)
        alt_counts = ", ".join(f"{skill}:{count}" for skill, count in top1_counter.items())
        any_counts = ", ".join(f"{skill}:{count}" for skill, count in any_counter.items()) or "<none>"

        lines.append(f"- {prompt_id}")
        lines.append(f"  gold: {gold}")
        lines.append(f"  top-1 correct: {top1_correct}/{total} ({top1_correct / total:.1%})")
        lines.append(f"  bypass: {prompt_bypass}/{total} ({prompt_bypass / total:.1%})")
        lines.append(
            f"  multi-skill consultation: {prompt_multi_skill}/{total} ({prompt_multi_skill / total:.1%})"
        )
        lines.append(f"  top-1 selections: {alt_counts}")
        lines.append(f"  any selected skills: {any_counts}")

    return "\n".join(lines)


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    default_manifest = repo_root / "runtime" / "confusability_results" / "manifest.csv"

    parser = argparse.ArgumentParser(
        description="Summarize confusability benchmark results from manifest.csv."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=default_manifest,
        help="Path to manifest.csv",
    )
    args = parser.parse_args()

    rows = load_rows(args.manifest)
    print(summarize(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
