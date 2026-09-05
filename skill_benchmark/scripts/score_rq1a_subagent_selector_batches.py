#!/usr/bin/env python3
"""Score chunked RQ1a subagent selector outputs."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def score_batch(batch_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    manifest = read_json(batch_dir / "manifest.json")
    answers = {row["case_id"]: row for row in read_json(batch_dir / "answer_key.local.json")["answers"]}
    rows: list[dict[str, Any]] = []
    problems: list[str] = []
    for chunk in manifest["chunks"]:
        output_path = Path(chunk["output_path"])
        if not output_path.exists():
            problems.append(f"missing output: {output_path}")
            continue
        try:
            data = read_json(output_path)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"invalid json {output_path}: {exc}")
            continue
        decisions = data.get("decisions", [])
        if len(decisions) != chunk["case_count"]:
            problems.append(f"case count mismatch {chunk['chunk_id']}: {len(decisions)} != {chunk['case_count']}")
        for decision in decisions:
            case_id = decision.get("case_id")
            answer = answers.get(case_id)
            if not answer:
                problems.append(f"no answer for case: {case_id}")
                continue
            condition = answer["condition"]
            is_hidden = condition == "shared_context_only"
            hidden_ok = is_hidden and decision.get("decision") == "ambiguous" and decision.get("selected_label") is None
            exposed_ok = (
                not is_hidden
                and decision.get("decision") == "select"
                and str(decision.get("selected_label")).upper() == answer["gold_label"]
            )
            row = {
                **answer,
                "chunk_id": chunk["chunk_id"],
                "decision": decision.get("decision"),
                "selected_label": decision.get("selected_label"),
                "evidence_field": decision.get("evidence_field"),
                "evidence_quote": decision.get("evidence_quote"),
                "rationale": decision.get("rationale"),
                "confidence": decision.get("confidence"),
                "hidden_ambiguous_correct": 1.0 if hidden_ok else 0.0,
                "exposed_selection_correct": 1.0 if exposed_ok else 0.0,
                "is_correct_for_condition": 1.0 if (hidden_ok or exposed_ok) else 0.0,
            }
            rows.append(row)

    buckets: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        variants = [row["prompt_variant"], "combined"]
        for variant in variants:
            buckets[(row["field"], row["condition"], variant)].append(row)
    summaries: list[dict[str, Any]] = []
    for (field, condition, variant), items in sorted(buckets.items()):
        if condition == "shared_context_only":
            score = sum(row["hidden_ambiguous_correct"] for row in items) / len(items)
            score_name = "ambiguity_correct"
        else:
            score = sum(row["exposed_selection_correct"] for row in items) / len(items)
            score_name = "selection_accuracy"
        summaries.append(
            {
                "field": field,
                "condition": condition,
                "prompt_variant": variant,
                "n": len(items),
                score_name: score,
                "ambiguous_rate": sum(row["decision"] == "ambiguous" for row in items) / len(items),
                "selection_rate": sum(row["decision"] == "select" for row in items) / len(items),
            }
        )
    return rows, summaries, problems


def render_markdown(rows: list[dict[str, Any]], summaries: list[dict[str, Any]], problems: list[str]) -> str:
    lines = [
        "# RQ1a Full Subagent Selector Diagnostic",
        "",
        "- Selector: Codex medium-reasoning subagents, chunked over the same RQ1a cases.",
        "- Hidden condition is scored by correct ambiguity, because candidates are intentionally indistinguishable.",
        "- Exposed condition is scored by selected label matching the local gold label.",
        "",
        "## Summary",
        "",
        "| Field | Condition | Prompt subset | n | Score | Ambiguous rate | Selection rate |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for item in summaries:
        score = item.get("ambiguity_correct", item.get("selection_accuracy"))
        lines.append(
            f"| `{item['field']}` | `{item['condition']}` | `{item['prompt_variant']}` | "
            f"{item['n']} | {score:.3f} | {item['ambiguous_rate']:.3f} | {item['selection_rate']:.3f} |"
        )

    misses = [
        row
        for row in rows
        if row["condition"] == "shared_context_plus_field" and row["exposed_selection_correct"] < 1
    ]
    miss_counts = Counter((row["field"], row["prompt_variant"], row["decision"]) for row in misses)
    lines.extend(["", "## Exposed-Field Misses", ""])
    lines.append(f"- Miss count: {len(misses)}")
    for key, count in sorted(miss_counts.items()):
        lines.append(f"- `{key[0]}` / `{key[1]}` / `{key[2]}`: {count}")
    if misses:
        lines.extend(
            [
                "",
                "| Case | Field | Variant | Decision | Selected | Gold | Rationale |",
                "|---|---|---|---|---|---|---|",
            ]
        )
        for row in misses[:40]:
            rationale = str(row.get("rationale") or "").replace("|", "\\|")
            lines.append(
                f"| `{row['case_id']}` | `{row['field']}` | `{row['prompt_variant']}` | "
                f"`{row['decision']}` | `{row['selected_label']}` | `{row['gold_label']}` | {rationale} |"
            )

    if problems:
        lines.extend(["", "## Problems", ""])
        for problem in problems:
            lines.append(f"- {problem}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-dir", default="skill_benchmark/outputs/rq1a_subagent_selector_batches_25")
    parser.add_argument("--output-prefix", default="rq1a_subagent_selector_full")
    args = parser.parse_args()
    batch_dir = Path(args.batch_dir).resolve()
    rows, summaries, problems = score_batch(batch_dir)
    out_dir = batch_dir.parent
    (out_dir / f"{args.output_prefix}_rows.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    (out_dir / f"{args.output_prefix}.json").write_text(
        json.dumps({"summaries": summaries, "problems": problems, "row_count": len(rows)}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out_dir / f"{args.output_prefix}.md").write_text(render_markdown(rows, summaries, problems), encoding="utf-8")
    print(json.dumps({"rows": len(rows), "summaries": len(summaries), "problems": len(problems)}, indent=2))


if __name__ == "__main__":
    main()
