#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any


SAMPLE_PROMPTS = [
    "reply_p2_polish_supervisor",
    "doc_p2_document_rewriter",
    "doc_p4_field_extraction",
    "doc_p6_conversion",
    "data_p3_validation",
    "obs_p5_root_cause",
    "news_p2_briefing",
    "read_p2_general_source_summary",
    "read_p7_multi_source_comparison",
    "sec_p2_security_code_review",
    "skill_p4_edit_existing",
    "skill_p6_package_existing",
]

METHODS = [
    ("m1_bm25_flat::current_full", "M1 BM25 flat"),
    ("m1_tfidf_flat::current_full", "M1 TF-IDF flat"),
    ("m2b_minilm_full_skill::current_full", "M2b MiniLM full skill"),
    ("m3_tfidf_schema::current_full", "M3 TF-IDF schema"),
    ("m6_bm25_schema_rerank::current_full", "M6 BM25 -> schema rerank"),
    ("m6_tfidf_schema_rerank::current_full", "M6 TF-IDF -> schema rerank"),
    ("m6_minilm_full_schema_rerank::current_full", "M6 MiniLM full -> schema rerank"),
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def acceptable_set(prompt_id: str, gold: str, acceptable_data: dict[str, Any]) -> set[str]:
    return {gold, *acceptable_data.get(prompt_id, {}).get("acceptable", [])}


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    evaluation = load_json(repo_root / "outputs" / "offline_selector_evaluation.json")
    acceptable_data = load_json(repo_root / "annotations" / "acceptable_alternatives.json")

    by_method_prompt: dict[tuple[str, str], dict[str, Any]] = {}
    for method_key, rows in evaluation["results"].items():
        for row in rows:
            by_method_prompt[(method_key, row["prompt_id"])] = row

    summary_counts = {
        method_label: {"top1": 0, "top5": 0, "total": 0}
        for _, method_label in METHODS
    }

    lines: list[str] = []
    lines.append("# Step 8 Candidate Readiness Report")
    lines.append("")
    lines.append("Status: retrieval-readiness check only; downstream artifact generation has not been executed.")
    lines.append("")
    lines.append("This report checks whether the planned Step 8 prompt sample has the gold or documented acceptable skill inside each selector's top-5 candidate set.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Method | Top-1 Gold/Accept | Top-5 Gold/Accept |")
    lines.append("|---|---:|---:|")

    detail_rows: list[str] = []
    detail_rows.append("| Prompt | Method | Gold/Accept Rank | Top-1 | Top-5 |")
    detail_rows.append("|---|---|---:|---|---|")

    for method_key, method_label in METHODS:
        for prompt_id in SAMPLE_PROMPTS:
            row = by_method_prompt[(method_key, prompt_id)]
            gold = row["gold_skill"]
            accepted = acceptable_set(prompt_id, gold, acceptable_data)
            top5 = [item["skill"] for item in row["ranking"][:5]]
            top1 = top5[0] if top5 else "<none>"
            rank = next((index + 1 for index, skill in enumerate(top5) if skill in accepted), None)

            summary_counts[method_label]["total"] += 1
            if top1 in accepted:
                summary_counts[method_label]["top1"] += 1
            if rank is not None:
                summary_counts[method_label]["top5"] += 1

            rank_text = str(rank) if rank is not None else "-"
            top5_text = ", ".join(f"`{skill}`" for skill in top5)
            detail_rows.append(
                f"| `{prompt_id}` | {method_label} | {rank_text} | `{top1}` | {top5_text} |"
            )

    for _, method_label in METHODS:
        counts = summary_counts[method_label]
        total = counts["total"]
        lines.append(
            f"| {method_label} | {counts['top1']}/{total} ({counts['top1'] / total:.1%}) | "
            f"{counts['top5']}/{total} ({counts['top5'] / total:.1%}) |"
        )

    lines.append("")
    lines.append("## Prompt Details")
    lines.append("")
    lines.extend(detail_rows)
    lines.append("")
    lines.append("Interpretation: Step 8 downstream runs are fair only when gold/acceptable is present in the candidate set. Missing top-5 cases should be labelled as retrieval failures before judging the main agent's artifact quality.")
    lines.append("")

    output_path = repo_root / "outputs" / "step8_candidate_readiness_report.md"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
