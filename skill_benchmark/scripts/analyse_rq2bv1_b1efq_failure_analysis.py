#!/usr/bin/env python3
"""Create a zero-network failure analysis for completed B1E-FQ V2.1.

This reads immutable completed rows, raw strict prompts, and parser records.
It does not score again, contact any provider, alter an executed artifact, or
make a claim about a replacement method.  The output is descriptive evidence
for explaining the observed B1E-FQ negative result.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any

from rq2b_common import (
    read_json,
    read_jsonl,
    relative,
    repo_root,
    sha256_file,
    write_json_new,
    write_text_new,
)
from rq2bv1_b1efq_e2e_v2_1 import RESULT_ROOT, _strict_prompts


FQ_ROWS = "field_aligned_results.jsonl"
PRIMARY_ROWS = "skill_benchmark/rq2bv1/results/qwen_primary_v3/qwen_primary_strict_results.jsonl"
METRIC_KEYS = ("strict_hit_at_1", "strict_mrr_at_10", "strict_recall_at_20")
NEGATION_RE = re.compile(
    r"\b(?:not|no|without|never|exclude|excluding|avoid|rather than|instead of|only)\b",
    re.IGNORECASE,
)
PARSER_SEMANTICS_EXAMPLE = "api_mcp_tooling_p1_rest_api_contract_designer"


def _metrics(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    if not rows:
        return {"rows": 0, **{key: 0.0 for key in METRIC_KEYS}}
    return {
        "rows": len(rows),
        **{key: sum(float(row[key]) for row in rows) / len(rows) for key in METRIC_KEYS},
    }


def _summary(values: list[float | int]) -> dict[str, float | int]:
    if not values:
        return {"count": 0, "mean": 0.0, "median": 0.0, "minimum": 0, "maximum": 0}
    return {
        "count": len(values),
        "mean": float(mean(values)),
        "median": float(median(values)),
        "minimum": min(values),
        "maximum": max(values),
    }


def _interval_union_length(spans: list[dict[str, Any]]) -> int:
    intervals = sorted((int(span["start"]), int(span["end"])) for span in spans)
    if not intervals:
        return 0
    total = 0
    left, right = intervals[0]
    for current_left, current_right in intervals[1:]:
        if current_left > right:
            total += right - left
            left, right = current_left, current_right
        else:
            right = max(right, current_right)
    return total + right - left


def _cross_field_overlap(spans_by_field: dict[str, list[dict[str, Any]]]) -> tuple[int, int]:
    """Return exact text reuse and strict character-interval overlap counts."""
    text_fields: dict[str, set[str]] = defaultdict(set)
    labelled: list[tuple[str, int, int]] = []
    for field, spans in spans_by_field.items():
        for span in spans:
            text_fields[str(span["text"])].add(field)
            labelled.append((field, int(span["start"]), int(span["end"])))
    exact_reused = sum(len(fields) > 1 for fields in text_fields.values())
    interval_pairs = 0
    for index, (left_field, left_start, left_end) in enumerate(labelled):
        for right_field, right_start, right_end in labelled[index + 1 :]:
            if left_field != right_field and max(left_start, right_start) < min(left_end, right_end):
                interval_pairs += 1
    return exact_reused, interval_pairs


def _parser_records(root: Path, prompts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    record_root = root / RESULT_ROOT / "parser_records"
    records: dict[str, dict[str, Any]] = {}
    for index, prompt in enumerate(prompts):
        path = record_root / f"{index:04d}.json"
        if not path.is_file():
            raise ValueError(f"Missing parser record: {path}")
        record = read_json(path)
        records[str(prompt["prompt_id"])] = record
    return records


def _field_presence(
    pure: list[dict[str, Any]], baseline: dict[str, dict[str, Any]], fields: tuple[str, ...]
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for field in fields:
        subset = [row for row in pure if field in row["parser"]["active_fields"]]
        field_metrics = _metrics(subset)
        baseline_metrics = _metrics([baseline[str(row["prompt_id"])] for row in subset])
        result[field] = {
            "field_aligned": field_metrics,
            "single_vector_matched": baseline_metrics,
            "hit_at_1_delta": field_metrics["strict_hit_at_1"] - baseline_metrics["strict_hit_at_1"],
            "recall_at_20_delta": field_metrics["strict_recall_at_20"] - baseline_metrics["strict_recall_at_20"],
        }
    return result


def _active_count(
    pure: list[dict[str, Any]], baseline: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for count in sorted({len(row["parser"]["active_fields"]) for row in pure}):
        subset = [row for row in pure if len(row["parser"]["active_fields"]) == count]
        field_metrics = _metrics(subset)
        baseline_metrics = _metrics([baseline[str(row["prompt_id"])] for row in subset])
        result[str(count)] = {
            "field_aligned": field_metrics,
            "single_vector_matched": baseline_metrics,
            "hit_at_1_delta": field_metrics["strict_hit_at_1"] - baseline_metrics["strict_hit_at_1"],
            "recall_at_20_delta": field_metrics["strict_recall_at_20"] - baseline_metrics["strict_recall_at_20"],
        }
    return result


def _top1_distribution(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(row["top_100"][0]["skill_id"]) for row in rows)
    return {
        "unique_top1_skills": len(counts),
        "most_frequent": [
            {"skill_id": skill_id, "top1_count": count}
            for skill_id, count in counts.most_common(12)
        ],
    }


def _case(
    row: dict[str, Any], base: dict[str, Any], prompt: dict[str, Any], parsed: dict[str, Any]
) -> dict[str, Any]:
    fields = parsed["fields"]
    return {
        "prompt_id": row["prompt_id"],
        "stratum": row["stratum"],
        "group": row["group"],
        "raw_prompt": prompt["prompt"],
        "gold_skill": row["gold_skill"],
        "field_aligned": {
            "gold_rank": row["strict_gold_rank"],
            "top1_skill": row["top_100"][0]["skill_id"],
        },
        "single_vector": {
            "gold_rank": base["strict_gold_rank"],
            "top1_skill": base["top_100"][0]["skill_id"],
        },
        "active_fields": parsed["active_fields"],
        "parsed_exact_spans": {
            field: [span["text"] for span in spans]
            for field, spans in fields.items()
            if spans
        },
    }


def _selected_cases(
    pure: list[dict[str, Any]],
    baseline: dict[str, dict[str, Any]],
    prompts: dict[str, dict[str, Any]],
    parsed: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    base_correct = [
        row
        for row in pure
        if int(baseline[str(row["prompt_id"])]["strict_hit_at_1"]) == 1
        and int(row["strict_hit_at_1"]) == 0
    ]
    # One worst-rank example per group makes the qualitative evidence varied,
    # rather than silently filling it with one popular cluster.
    by_group: dict[str, dict[str, Any]] = {}
    for row in sorted(base_correct, key=lambda item: (-int(item["strict_gold_rank"]), str(item["prompt_id"]))):
        by_group.setdefault(str(row["group"]), row)
    losses = sorted(by_group.values(), key=lambda item: (-int(item["strict_gold_rank"]), str(item["prompt_id"])))[:10]

    field_wins = [
        row
        for row in pure
        if int(row["strict_hit_at_1"]) == 1
        and int(baseline[str(row["prompt_id"])]["strict_hit_at_1"]) == 0
    ]
    wins_by_group: dict[str, dict[str, Any]] = {}
    for row in sorted(field_wins, key=lambda item: (-int(baseline[str(item["prompt_id"])]["strict_gold_rank"]), str(item["prompt_id"]))):
        wins_by_group.setdefault(str(row["group"]), row)
    wins = sorted(wins_by_group.values(), key=lambda item: (-int(baseline[str(item["prompt_id"])]["strict_gold_rank"]), str(item["prompt_id"])))[:6]

    return {
        "single_vector_correct_field_aligned_wrong": [
            _case(row, baseline[str(row["prompt_id"])], prompts[str(row["prompt_id"])], parsed[str(row["prompt_id"])])
            for row in losses
        ],
        "field_aligned_correct_single_vector_wrong": [
            _case(row, baseline[str(row["prompt_id"])], prompts[str(row["prompt_id"])], parsed[str(row["prompt_id"])])
            for row in wins
        ],
    }


def build(root: Path) -> dict[str, Any]:
    result_root = root / RESULT_ROOT
    fq_path = result_root / FQ_ROWS
    primary_path = root / PRIMARY_ROWS
    fq_rows = read_jsonl(fq_path)
    primary_rows = read_jsonl(primary_path)
    _, prompt_rows = _strict_prompts(root)
    prompts = {str(row["prompt_id"]): row for row in prompt_rows}
    baseline = {
        str(row["prompt_id"]): row
        for row in primary_rows
        if row.get("representation") == "i3c-fielded-evidence"
        and row.get("retriever") == "qwen-text-embedding-v4"
    }
    if len(fq_rows) != len(baseline) != len(prompts):
        raise ValueError("B1E-FQ analysis coverage drift")
    if {str(row["prompt_id"]) for row in fq_rows} != set(baseline) or set(baseline) != set(prompts):
        raise ValueError("B1E-FQ analysis identity drift")

    pure = [row for row in fq_rows if row["method_source"] == "pure_query_structured_field_aligned"]
    fallback = [row for row in fq_rows if row["method_source"] == "fallback_i3c_single_vector"]
    if len(pure) != 369 or len(fallback) != 12:
        raise ValueError("B1E-FQ analysis pure/fallback coverage drift")
    records = _parser_records(root, prompt_rows)
    parsed = {
        prompt_id: records[prompt_id]["entry"]["parsed"]
        for prompt_id in {str(row["prompt_id"]) for row in pure}
    }
    if any(value is None for value in parsed.values()):
        raise ValueError("Pure row missing valid parser record")

    field_order = tuple(next(iter(parsed.values()))["fields"])
    raw_chars: list[int] = []
    extracted_chars: list[int] = []
    unique_extracted_chars: list[int] = []
    retention: list[float] = []
    excerpt_counts: list[int] = []
    exact_reused_by_query = 0
    overlap_by_query = 0
    exact_reused_total = 0
    overlap_total = 0
    boundary_active = 0
    boundary_with_polarity = 0
    raw_polarity_with_boundary_without_polarity = 0
    for prompt_id, value in parsed.items():
        spans_by_field = value["fields"]
        all_spans = [span for spans in spans_by_field.values() for span in spans]
        raw = str(prompts[prompt_id]["prompt"])
        raw_chars.append(len(raw))
        extracted = sum(len(str(span["text"])) for span in all_spans)
        unique = _interval_union_length(all_spans)
        extracted_chars.append(extracted)
        unique_extracted_chars.append(unique)
        retention.append(unique / len(raw))
        excerpt_counts.append(len(all_spans))
        exact_reused, interval_pairs = _cross_field_overlap(spans_by_field)
        exact_reused_total += exact_reused
        overlap_total += interval_pairs
        exact_reused_by_query += int(exact_reused > 0)
        overlap_by_query += int(interval_pairs > 0)
        boundary_text = "\n".join(str(span["text"]) for span in spans_by_field["boundary_not_for"])
        if boundary_text:
            boundary_active += 1
            boundary_with_polarity += int(bool(NEGATION_RE.search(boundary_text)))
            raw_polarity_with_boundary_without_polarity += int(
                bool(NEGATION_RE.search(raw)) and not bool(NEGATION_RE.search(boundary_text))
            )

    pure_baseline = [baseline[str(row["prompt_id"])] for row in pure]
    paired = Counter(
        (int(row["strict_hit_at_1"]), int(baseline[str(row["prompt_id"])]["strict_hit_at_1"]))
        for row in pure
    )
    example_parse = parsed[PARSER_SEMANTICS_EXAMPLE]
    example_prompt = prompts[PARSER_SEMANTICS_EXAMPLE]["prompt"]
    return {
        "schema_version": "rq2bv1-v3-b1e-fq-e2e-v2-1-failure-analysis-v1",
        "state": "completed_zero_network_descriptive_analysis_not_thesis_text",
        "network_calls": 0,
        "purpose": "Explain observed B1E-FQ V2.1 failures without rerunning or changing the frozen method.",
        "inputs": {
            "field_aligned_rows": {"path": relative(fq_path, root), "sha256": sha256_file(fq_path), "rows": len(fq_rows)},
            "matched_qwen_i3c_rows": {"path": relative(primary_path, root), "sha256": sha256_file(primary_path), "rows": len(baseline)},
            "strict_prompts": {"path": relative(root / "skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/b1l_preflight_v3/strict_scored_prompts.jsonl", root), "rows": len(prompts)},
        },
        "coverage": {
            "strict_prompts": len(fq_rows),
            "pure_field_aligned": len(pure),
            "fallback_i3c_single_vector": len(fallback),
            "fallback_failure_classes": dict(Counter(row["parser"].get("failure_class") for row in fallback)),
        },
        "matched_retrieval_outcome": {
            "pure_field_aligned": _metrics(pure),
            "matched_qwen_i3c_single_vector": _metrics(pure_baseline),
            "paired_hit_at_1": {
                "field_aligned_only_correct": paired[(1, 0)],
                "single_vector_only_correct": paired[(0, 1)],
                "both_correct": paired[(1, 1)],
                "both_incorrect": paired[(0, 0)],
            },
            "rank_direction": {
                "field_aligned_better": sum(int(row["strict_gold_rank"]) < int(baseline[str(row["prompt_id"])]["strict_gold_rank"]) for row in pure),
                "single_vector_better": sum(int(row["strict_gold_rank"]) > int(baseline[str(row["prompt_id"])]["strict_gold_rank"]) for row in pure),
                "tied": sum(int(row["strict_gold_rank"]) == int(baseline[str(row["prompt_id"])]["strict_gold_rank"]) for row in pure),
            },
        },
        "parse_projection_characteristics": {
            "raw_prompt_characters": _summary(raw_chars),
            "serialised_span_characters_with_cross_field_repetition": _summary(extracted_chars),
            "unique_source_character_coverage": {
                **_summary(unique_extracted_chars),
                "raw_prompt_fraction": _summary(retention),
            },
            "exact_spans_per_query": _summary(excerpt_counts),
            "cross_field_reuse": {
                "queries_with_exact_text_reused_across_fields": exact_reused_by_query,
                "queries_with_any_cross_field_character_interval_overlap": overlap_by_query,
                "distinct_exact_reused_texts_across_all_queries": exact_reused_total,
                "cross_field_interval_overlap_pairs_across_all_queries": overlap_total,
            },
            "boundary_polarity_surface_form": {
                "queries_with_active_boundary_field": boundary_active,
                "active_boundary_fields_containing_an_explicit_polarity_cue": boundary_with_polarity,
                "raw_prompt_has_a_polarity_cue_but_active_boundary_text_has_none": raw_polarity_with_boundary_without_polarity,
                "scope_note": "Surface-form diagnostic only. It does not determine whether a boundary phrase is semantically correct.",
            },
        },
        "descriptive_slices": {
            "by_active_field_count": _active_count(pure, baseline),
            "by_field_presence": _field_presence(pure, baseline, field_order),
            "top1_distribution": {
                "field_aligned": _top1_distribution(pure),
                "single_vector_matched": _top1_distribution(pure_baseline),
            },
        },
        "concrete_parser_semantics_example": {
            "prompt_id": PARSER_SEMANTICS_EXAMPLE,
            "raw_prompt": example_prompt,
            "parsed_exact_spans": {
                field: [span["text"] for span in spans]
                for field, spans in example_parse["fields"].items()
                if spans
            },
            "observation": "The boundary span quotes 'MCP wrapper' but not the preceding 'not'; the use-condition text is also nested within the workflow text. Exact-substring grounding therefore verifies provenance, not preservation of polarity or non-overlapping semantics.",
        },
        "case_examples": _selected_cases(pure, baseline, prompts, parsed),
        "interpretation_boundary": {
            "supported_by_this_analysis": [
                "The fixed parser-to-diagonal-field-cosine-to-equal-mean pipeline loses substantial strict-gold candidate recall relative to a matched I3C single-vector representation.",
                "The result is not explained solely by the 12 explicit fallback rows because the pure 369-row subset remains substantially lower.",
                "The parser projection can duplicate or overlap source language across fields, and can omit local polarity tokens in an observed grounded example.",
                "Equal averaging and diagonal-only matching are plausible contributors, but these descriptive slices do not identify a causal contribution from either one.",
            ],
            "not_supported": [
                "that I3C fields contain no routing information",
                "that all field-aware retrieval designs fail",
                "that query rewriting, learned aggregation, cross-field interaction, or a different parser would fail",
                "a reranking result or a change to the frozen primary B1 matrix",
            ],
        },
        "thesis_result_writing": False,
    }


def _metric(value: float | int) -> str:
    return f"{float(value):.3f}"


def _render(report: dict[str, Any]) -> str:
    outcome = report["matched_retrieval_outcome"]
    field = outcome["pure_field_aligned"]
    base = outcome["matched_qwen_i3c_single_vector"]
    coverage = report["coverage"]
    characteristics = report["parse_projection_characteristics"]
    reuse = characteristics["cross_field_reuse"]
    polarity = characteristics["boundary_polarity_surface_form"]
    rows = [
        "# B1E-FQ V2.1 Failure Analysis",
        "",
        "**Status:** `COMPLETE / ZERO-NETWORK / DESCRIPTIVE / NOT THESIS TEXT`",
        "",
        "## Scope",
        "",
        "This analysis reads the immutable completed B1E-FQ rows, matched Qwen I3C",
        "single-vector rows, raw strict prompts, and parser records. It does not rerun",
        "retrieval or an external model, change any frozen primary result, or propose a",
        "post-hoc replacement selector.",
        "",
        "## Main Observation",
        "",
        f"On the pure {coverage['pure_field_aligned']}-prompt subset, the fixed query-structured",
        f"field-aligned method reached Hit@1/MRR@10/Recall@20 of {_metric(field['strict_hit_at_1'])}/",
        f"{_metric(field['strict_mrr_at_10'])}/{_metric(field['strict_recall_at_20'])}, versus",
        f"{_metric(base['strict_hit_at_1'])}/{_metric(base['strict_mrr_at_10'])}/",
        f"{_metric(base['strict_recall_at_20'])} for matched Qwen I3C single-vector retrieval.",
        "The failure is therefore present before reranking and is not caused only by the",
        f"{coverage['fallback_i3c_single_vector']} declared fallback rows.",
        "",
        "| Paired pure Hit@1 outcome | Prompts |",
        "|---|---:|",
        f"| Field-aligned only correct | {outcome['paired_hit_at_1']['field_aligned_only_correct']} |",
        f"| Single-vector only correct | {outcome['paired_hit_at_1']['single_vector_only_correct']} |",
        f"| Both correct | {outcome['paired_hit_at_1']['both_correct']} |",
        f"| Both incorrect | {outcome['paired_hit_at_1']['both_incorrect']} |",
        "",
        "The field-aligned rank is better on",
        f"{outcome['rank_direction']['field_aligned_better']} prompts, while the single-vector rank",
        f"is better on {outcome['rank_direction']['single_vector_better']} prompts",
        f"({outcome['rank_direction']['tied']} ties).",
        "",
        "## What Appears To Go Wrong",
        "",
        "1. **Projection fragments the intent.** The parser converts an ordinary request",
        "into a set of short field strings. The scoring rule then forbids cross-field",
        "matching and takes an equal mean. A complete single-vector representation can",
        "retain interactions such as object + requested action + exclusion; this fixed",
        "pipeline cannot use an action phrase in one field to disambiguate a related",
        "object phrase in another.",
        "2. **Grounding is not semantic preservation.** Exact-substring validation proves",
        "that parser text occurred in the prompt, but it does not guarantee that negation,",
        "scope, or relations stay inside the quoted span. The concrete example below",
        "contains a boundary quote that drops `not`, and overlapping use/workflow quotes.",
        "3. **The rule treats all active fields as equally decisive.** More fields do not",
        "automatically help: active-field-count slices remain lower than the matched",
        "single vector. This is consistent with dilution by generic fields, but the slice",
        "is descriptive and does not prove equal weighting is the sole cause.",
        "4. **Operational failures are secondary.** There were",
        f"{coverage['fallback_i3c_single_vector']} fallbacks ({coverage['fallback_failure_classes']}),",
        "but the principal comparison is the 369 pure rows, so they cannot explain the",
        "main accuracy gap.",
        "",
        "## Parser Projection Diagnostics",
        "",
        "| Diagnostic | Observed value |",
        "|---|---:|",
        f"| Mean raw prompt characters | {characteristics['raw_prompt_characters']['mean']:.1f} |",
        f"| Mean unique quoted-source characters | {characteristics['unique_source_character_coverage']['mean']:.1f} |",
        f"| Mean unique quoted fraction of raw prompt | {characteristics['unique_source_character_coverage']['raw_prompt_fraction']['mean']:.3f} |",
        f"| Mean exact spans per query | {characteristics['exact_spans_per_query']['mean']:.2f} |",
        f"| Queries with cross-field exact-text reuse | {reuse['queries_with_exact_text_reused_across_fields']} |",
        f"| Queries with cross-field interval overlap | {reuse['queries_with_any_cross_field_character_interval_overlap']} |",
        f"| Active boundary fields with an explicit polarity cue | {polarity['active_boundary_fields_containing_an_explicit_polarity_cue']} / {polarity['queries_with_active_boundary_field']} |",
        f"| Raw prompt has polarity cue but its active boundary text has none | {polarity['raw_prompt_has_a_polarity_cue_but_active_boundary_text_has_none']} |",
        "",
        "The polarity row is a surface-form diagnostic, not a semantic-accuracy measure.",
        "",
        "## Concrete Example",
        "",
        f"`{report['concrete_parser_semantics_example']['prompt_id']}`: {report['concrete_parser_semantics_example']['raw_prompt']}",
        "",
        "Parsed spans:",
    ]
    for field_name, spans in report["concrete_parser_semantics_example"]["parsed_exact_spans"].items():
        rows.append(f"- `{field_name}`: " + "; ".join(f"`{span}`" for span in spans))
    rows.extend([
        "",
        report["concrete_parser_semantics_example"]["observation"],
        "",
        "## Descriptive Slices",
        "",
        "| Active fields | N | Field-aligned H@1 | Single-vector H@1 | Field-aligned R@20 | Single-vector R@20 |",
        "|---:|---:|---:|---:|---:|---:|",
    ])
    for count, values in report["descriptive_slices"]["by_active_field_count"].items():
        fq = values["field_aligned"]
        single = values["single_vector_matched"]
        rows.append(
            f"| {count} | {fq['rows']} | {_metric(fq['strict_hit_at_1'])} | {_metric(single['strict_hit_at_1'])} | {_metric(fq['strict_recall_at_20'])} | {_metric(single['strict_recall_at_20'])} |"
        )
    rows.extend([
        "",
        "| Parser-active field | N | Field-aligned H@1 | Single-vector H@1 | Field-aligned R@20 | Single-vector R@20 |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for field_name, values in report["descriptive_slices"]["by_field_presence"].items():
        fq = values["field_aligned"]
        single = values["single_vector_matched"]
        rows.append(
            f"| `{field_name}` | {fq['rows']} | {_metric(fq['strict_hit_at_1'])} | {_metric(single['strict_hit_at_1'])} | {_metric(fq['strict_recall_at_20'])} | {_metric(single['strict_recall_at_20'])} |"
        )
    rows.extend([
        "",
        "## Interpretation Boundary",
        "",
        "This supports a narrow conclusion: **the executed pipeline of exact-span",
        "parsing, diagonal same-field cosine, and equal averaging is not a competitive",
        "first-stage retriever on this strict corpus.** It does not show that I3C fields",
        "lack routing value, that every field-aware strategy fails, or that learned",
        "aggregation, cross-field interaction, or a different parser would fail.",
        "",
        "Machine-readable evidence is `failure_analysis.json`; selected cases are there",
        "for review. No thesis LaTex/PDF text was modified.",
        "",
    ])
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write new local JSON and Markdown analysis artifacts.")
    args = parser.parse_args()
    if not args.write:
        raise ValueError("Pass --write to materialise the failure analysis")
    root = repo_root()
    output_root = root / RESULT_ROOT
    json_output = output_root / "failure_analysis.json"
    markdown_output = output_root / "FAILURE_ANALYSIS.md"
    if json_output.exists() or markdown_output.exists():
        raise FileExistsError("Refusing to overwrite an existing B1E-FQ failure analysis")
    report = build(root)
    write_json_new(json_output, report)
    write_text_new(markdown_output, _render(report))
    print(f"{relative(json_output, root)}\n{relative(markdown_output, root)}")


if __name__ == "__main__":
    main()
