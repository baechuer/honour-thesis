#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("skill_benchmark/outputs")
BENCHMARK_VERSION = "benchmark-v0.4-2026-06-16"
REPS = {
    "r1": ("I1", "R1 flat card"),
    "r2": ("I3", "R2 structured fields"),
    "full": ("I2", "Full SKILL.md"),
    "FULL": ("I2", "Full SKILL.md"),
}


@dataclass(frozen=True)
class Spec:
    method_id: str
    group: str
    stratum: str
    representation: str
    first_stage: str
    reranker: str
    candidate_budget: str
    path: Path
    result_key: str | None = None
    note: str = ""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.1%}"


def num(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def representation_label(rep: str) -> tuple[str, str]:
    return REPS.get(rep, (rep, rep))


def ranking_names(row: dict[str, Any]) -> list[str]:
    ranking = row.get("ranking") or []
    names: list[str] = []
    for item in ranking:
        if isinstance(item, dict):
            name = item.get("skill")
        else:
            name = item
        if name:
            names.append(str(name))
    return names


def normalize_rows_and_metrics(path: Path, result_key: str | None = None) -> tuple[list[dict[str, Any]] | None, dict[str, Any]]:
    data = load_json(path)
    if isinstance(data.get("results"), list):
        return data["results"], data.get("metrics", {})
    if isinstance(data.get("results"), dict):
        key = result_key
        if key is None:
            summary = data.get("summary") or []
            if summary:
                key = max(summary, key=lambda item: item["metrics"].get("top1_accuracy", -1))["result_key"]
            else:
                key = next(iter(data["results"]))
        metrics = {}
        for item in data.get("summary") or []:
            if (item.get("result_key") or item.get("key")) == key:
                metrics = item.get("metrics", {})
                break
        return data["results"][key], metrics
    return None, data.get("metrics", {})


def candidate_recall(rows: list[dict[str, Any]] | None, k: int) -> float | None:
    if not rows:
        return None
    hits = 0
    for row in rows:
        if row.get("candidate_names"):
            hit = row["gold_skill"] in row["candidate_names"][:k]
        else:
            rank = row.get("gold_first_stage_rank")
            hit = isinstance(rank, int) and rank <= k
        hits += int(hit)
    return hits / len(rows)


def row_metric_values(rows: list[dict[str, Any]] | None) -> dict[str, list[float]]:
    if not rows:
        return {"top1": [], "top5": [], "mrr": []}
    top1: list[float] = []
    top5: list[float] = []
    mrr: list[float] = []
    for row in rows:
        gold = row["gold_skill"]
        names = ranking_names(row)
        top1.append(float(bool(names and names[0] == gold)))
        top5.append(float(gold in names[:5]))
        rank = names.index(gold) + 1 if gold in names else None
        mrr.append(1.0 / rank if rank else 0.0)
    return {"top1": top1, "top5": top5, "mrr": mrr}


def bootstrap_ci(values: list[float], iterations: int = 1000, seed: int = 7) -> tuple[float, float] | None:
    if not values:
        return None
    rng = random.Random(seed)
    n = len(values)
    samples = []
    for _ in range(iterations):
        total = 0.0
        for _ in range(n):
            total += values[rng.randrange(n)]
        samples.append(total / n)
    samples.sort()
    return samples[int(0.025 * iterations)], samples[int(0.975 * iterations)]


def exact_mcnemar_p(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    lower = min(b, c)
    # two-sided exact binomial p-value under p=0.5
    prob = sum(math.comb(n, i) for i in range(lower + 1)) / (2**n)
    return min(1.0, 2 * prob)


def paired_top1(rows_a: list[dict[str, Any]], rows_b: list[dict[str, Any]]) -> dict[str, Any]:
    by_a = {row["prompt_id"]: row for row in rows_a}
    by_b = {row["prompt_id"]: row for row in rows_b}
    common = sorted(set(by_a) & set(by_b))
    b = 0  # A correct, B wrong
    c = 0  # A wrong, B correct
    both_correct = 0
    both_wrong = 0
    for pid in common:
        row_a = by_a[pid]
        row_b = by_b[pid]
        a_hit = bool(ranking_names(row_a) and ranking_names(row_a)[0] == row_a["gold_skill"])
        b_hit = bool(ranking_names(row_b) and ranking_names(row_b)[0] == row_b["gold_skill"])
        if a_hit and b_hit:
            both_correct += 1
        elif a_hit and not b_hit:
            b += 1
        elif (not a_hit) and b_hit:
            c += 1
        else:
            both_wrong += 1
    return {
        "n": len(common),
        "a_only": b,
        "b_only": c,
        "both_correct": both_correct,
        "both_wrong": both_wrong,
        "mcnemar_p": exact_mcnemar_p(b, c),
    }


def collect_specs() -> list[Spec]:
    specs: list[Spec] = []
    for stratum in ["controlled", "public_gold"]:
        for retriever in ["bm25", "tfidf"]:
            for rep in ["r1", "r2", "FULL"]:
                specs.append(
                    Spec(
                        method_id=f"{retriever.upper()}",
                        group="Lexical retrieval",
                        stratum=stratum,
                        representation=rep.lower() if rep != "FULL" else "full",
                        first_stage=retriever.upper(),
                        reranker="none",
                        candidate_budget="all",
                        path=OUTPUT_DIR / "frozen_v0_4_crossed_lexical_matrix.json",
                        result_key=f"{stratum}_{retriever}_{rep.lower()}",
                    )
                )

    for stratum in ["controlled", "public_gold"]:
        for rep in ["r1", "r2", "full"]:
            specs.extend(
                [
                    Spec(
                        method_id="Qwen embedding",
                        group="Dense retrieval",
                        stratum=stratum,
                        representation=rep,
                        first_stage="Qwen text-embedding-v4",
                        reranker="none",
                        candidate_budget="all",
                        path=OUTPUT_DIR / f"frozen_v0_4_{stratum}_qwen_{rep}_embedding.json",
                    ),
                    Spec(
                        method_id="Qwen + Qwen rerank",
                        group="Dense + learned rerank",
                        stratum=stratum,
                        representation=rep,
                        first_stage="Qwen text-embedding-v4",
                        reranker="Qwen qwen3-rerank",
                        candidate_budget="20",
                        path=OUTPUT_DIR / f"frozen_v0_4_{stratum}_qwen_{rep}_qwen_rerank_top20.json",
                    ),
                    Spec(
                        method_id="Qwen + local schema",
                        group="Dense + local schema diagnostic",
                        stratum=stratum,
                        representation=rep,
                        first_stage="Qwen text-embedding-v4",
                        reranker="local schema",
                        candidate_budget="20",
                        path=OUTPUT_DIR / f"frozen_v0_4_{stratum}_qwen_{rep}_local_schema_top20.json",
                        note="diagnostic, not final semantic field matcher",
                    ),
                    Spec(
                        method_id="SkillRouter embedding",
                        group="Skill-specific dense retrieval",
                        stratum=stratum,
                        representation=rep,
                        first_stage="SkillRouter embedding",
                        reranker="none",
                        candidate_budget="all",
                        path=OUTPUT_DIR / f"skillrouter_v0_4_2026_06_17_retry2_{stratum}_{rep}_embedding.json",
                    ),
                    Spec(
                        method_id="SkillRouter + SkillRouter rerank",
                        group="Skill-specific dense + learned rerank",
                        stratum=stratum,
                        representation=rep,
                        first_stage="SkillRouter embedding",
                        reranker="SkillRouter reranker",
                        candidate_budget="20",
                        path=OUTPUT_DIR / f"skillrouter_v0_4_2026_06_17_retry2_{stratum}_{rep}_rerank_top20.json",
                    ),
                    Spec(
                        method_id="SkillRouter + M6-v1 best",
                        group="Skill-specific dense + field-aware diagnostic",
                        stratum=stratum,
                        representation=rep,
                        first_stage="SkillRouter embedding",
                        reranker="M6-v1 lexical field-aware",
                        candidate_budget="20",
                        path=OUTPUT_DIR / f"frozen_v0_4_{stratum}_skillrouter_{rep}_m6v1_top20.json",
                        note="best field set; exploratory diagnostic",
                    ),
                ]
            )
    return specs


def matrix_rows() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    rows_out: list[dict[str, Any]] = []
    row_cache: dict[str, list[dict[str, Any]]] = {}
    for spec in collect_specs():
        if not spec.path.exists():
            rows_out.append(
                {
                    "method_id": spec.method_id,
                    "group": spec.group,
                    "stratum": spec.stratum,
                    "representation": spec.representation,
                    "information_layer": representation_label(spec.representation)[0],
                    "artifact": representation_label(spec.representation)[1],
                    "first_stage": spec.first_stage,
                    "reranker": spec.reranker,
                    "candidate_budget": spec.candidate_budget,
                    "status": "missing",
                    "source": str(spec.path),
                    "note": spec.note,
                }
            )
            continue
        rows, metrics = normalize_rows_and_metrics(spec.path, spec.result_key)
        cache_key = f"{spec.stratum}|{spec.method_id}|{spec.representation}|{spec.reranker}"
        if rows:
            row_cache[cache_key] = rows
        values = row_metric_values(rows)
        top1_ci = bootstrap_ci(values["top1"])
        mrr_ci = bootstrap_ci(values["mrr"])
        rows_out.append(
            {
                "method_id": spec.method_id,
                "group": spec.group,
                "stratum": spec.stratum,
                "representation": spec.representation,
                "information_layer": representation_label(spec.representation)[0],
                "artifact": representation_label(spec.representation)[1],
                "first_stage": spec.first_stage,
                "reranker": spec.reranker,
                "candidate_budget": spec.candidate_budget,
                "status": "done",
                "n": metrics.get("total_prompts"),
                "skills": metrics.get("scale_skill_count"),
                "top1": metrics.get("top1_accuracy"),
                "top1_ci": top1_ci,
                "acceptable_top1": metrics.get("acceptable_top1_accuracy"),
                "top5": metrics.get("top5_recall"),
                "mrr": metrics.get("mrr"),
                "mrr_ci": mrr_ci,
                "candidate_recall_at_20": candidate_recall(rows, 20),
                "candidate_recall_at_100": candidate_recall(rows, 100),
                "tokens": metrics.get("selector_visible_tokens_approx"),
                "non_main_top1": metrics.get("non_main_top1_rate"),
                "source": str(spec.path),
                "result_key": spec.result_key,
                "note": spec.note,
            }
        )

    fixed = OUTPUT_DIR / "frozen_v0_4_m6v2_fixed_task_heavy.json"
    if fixed.exists():
        data = load_json(fixed)
        for source in data.get("sources", []):
            rep = source["representation"]
            metrics = source["best_top1"]["metrics"]
            rows_out.append(
                {
                    "method_id": "M6-v2 fixed task-heavy",
                    "group": "Semantic field-aware diagnostic",
                    "stratum": source["stratum"],
                    "representation": rep,
                    "information_layer": representation_label(rep)[0],
                    "artifact": representation_label(rep)[1],
                    "first_stage": source["candidate_source"],
                    "reranker": "M6-v2 semantic field matcher",
                    "candidate_budget": str(source.get("rerank_candidates", 20)),
                    "status": "done-summary-only",
                    "n": metrics.get("total_prompts"),
                    "skills": metrics.get("scale_skill_count"),
                    "top1": metrics.get("top1_accuracy"),
                    "top1_ci": None,
                    "acceptable_top1": metrics.get("acceptable_top1_accuracy"),
                    "top5": metrics.get("top5_recall"),
                    "mrr": metrics.get("mrr"),
                    "mrr_ci": None,
                    "candidate_recall_at_20": source["best_top1"].get("candidate_recall_at_k"),
                    "candidate_recall_at_100": None,
                    "tokens": metrics.get("selector_visible_tokens_approx"),
                    "non_main_top1": metrics.get("non_main_top1_rate"),
                    "source": str(fixed),
                    "result_key": None,
                    "note": "fixed global policy; summary-only artifact",
                }
            )
    return rows_out, row_cache


def key_for(rows: dict[str, list[dict[str, Any]]], stratum: str, method: str, rep: str, reranker: str) -> str:
    return f"{stratum}|{method}|{rep}|{reranker}"


def paired_tests(row_cache: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    tests: list[dict[str, Any]] = []
    families = [
        ("BM25", "none"),
        ("TFIDF", "none"),
        ("Qwen embedding", "none"),
        ("Qwen + Qwen rerank", "Qwen qwen3-rerank"),
        ("SkillRouter embedding", "none"),
        ("SkillRouter + SkillRouter rerank", "SkillRouter reranker"),
    ]
    for stratum in ["controlled", "public_gold"]:
        for method, reranker in families:
            for left, right in [("r1", "r2"), ("r2", "full")]:
                key_a = key_for(row_cache, stratum, method, left, reranker)
                key_b = key_for(row_cache, stratum, method, right, reranker)
                if key_a not in row_cache or key_b not in row_cache:
                    continue
                test = paired_top1(row_cache[key_a], row_cache[key_b])
                test.update(
                    {
                        "stratum": stratum,
                        "method": method,
                        "reranker": reranker,
                        "comparison": f"{representation_label(left)[0]} vs {representation_label(right)[0]}",
                        "a": left,
                        "b": right,
                    }
                )
                tests.append(test)
    return tests


def sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    stratum_order = {"controlled": 0, "public_gold": 1}
    layer_order = {"I1": 0, "I3": 1, "I2": 2}
    return (
        stratum_order.get(row["stratum"], 9),
        row["group"],
        row["method_id"],
        layer_order.get(row["information_layer"], 9),
    )


def render_md(rows: list[dict[str, Any]], tests: list[dict[str, Any]]) -> str:
    lines = [
        "# Frozen v0.4 Information-Layer Matrix",
        "",
        f"Benchmark: `{BENCHMARK_VERSION}`",
        "",
        "This report is generated from frozen result JSON artifacts. It groups rows by information layer first, then by retrieval/reranking strategy. Controlled and public-gold strata remain separate.",
        "",
        "## Reading Rules",
        "",
        "- Compare `I1`, `I2`, and `I3` only within the same method family, stratum, candidate budget, and reranker.",
        "- `Cand R@20` measures whether the gold skill was available to a top-20 reranker; a reranker cannot recover a missing candidate.",
        "- M6-v1 and M6-v2 rows are diagnostics for field use, not final claims of a new superior reranker.",
        "- M6-v2 fixed rows are summary-only because the fixed-policy artifact currently stores aggregate metrics, not per-prompt rows.",
        "",
    ]
    for stratum in ["controlled", "public_gold"]:
        lines += [
            f"## {stratum.replace('_', ' ').title()} Matrix",
            "",
            "| Group | Method | First stage | Info | Artifact | Candidate budget | Top-1 | Top-1 95% CI | Accept Top-1 | Top-5 | Cand R@20 | MRR | Tokens | Note |",
            "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
        for row in sorted([item for item in rows if item["stratum"] == stratum and item["status"].startswith("done")], key=sort_key):
            ci = row.get("top1_ci")
            ci_text = f"{pct(ci[0])}-{pct(ci[1])}" if ci else "-"
            lines.append(
                f"| {row['group']} | {row['method_id']} | {row['first_stage']} | {row['information_layer']} | {row['artifact']} | "
                f"{row['candidate_budget']} | {pct(row.get('top1'))} | {ci_text} | "
                f"{pct(row.get('acceptable_top1'))} | {pct(row.get('top5'))} | "
                f"{pct(row.get('candidate_recall_at_20'))} | {num(row.get('mrr'))} | "
                f"{row.get('tokens') or '-'} | {row.get('note') or ''} |"
            )
        lines.append("")

    missing = [row for row in rows if row["status"] == "missing"]
    lines += [
        "## Missing From Current Comparable Matrix",
        "",
    ]
    if missing:
        lines += ["| Stratum | Method | Info | Expected source |", "|---|---|---|---|"]
        for row in missing:
            lines.append(f"| {row['stratum']} | {row['method_id']} | {row['information_layer']} | `{row['source']}` |")
    else:
        lines.append("No missing I1/I2/I3 rows for the audited method families.")

    lines += [
        "",
        "## Paired McNemar Tests For Information-Layer Comparisons",
        "",
        "| Stratum | Method | Comparison | A-only | B-only | n | p-value | Interpretation |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for test in tests:
        p = test["mcnemar_p"]
        if p < 0.01:
            interp = "strong paired difference"
        elif p < 0.05:
            interp = "paired difference"
        else:
            interp = "not significant at 0.05"
        lines.append(
            f"| {test['stratum']} | {test['method']} | {test['comparison']} | "
            f"{test['a_only']} | {test['b_only']} | {test['n']} | {p:.4f} | {interp} |"
        )

    lines += [
        "",
        "## First-Pass Interpretation",
        "",
        "- On controlled prompts, `I3` structured fields usually improve over `I1` for lexical, Qwen, and SkillRouter settings. This supports the information-layer claim under deliberately confusable procedural clusters.",
        "- On public-gold prompts, `I3` often improves candidate recall but not always top-1. Public skills contain provider/name cues and messy prose, so compact flat cards sometimes rank better even when structured fields retrieve the gold into the candidate set.",
        "- Full skill artifacts are not a monotonic improvement. They add information, but also noise and token cost; public-gold full-document Qwen rows are especially weak before reranking.",
        "- SkillRouter is stronger than generic Qwen on several frozen v0.4 rows, but the effect interacts with the information layer: SkillRouter reranking helps controlled cases, while public-gold top-1 sometimes drops after reranking.",
        "- M6-v1/M6-v2 are best treated as transparent diagnostics of field signal. Current fixed M6-v2 does not beat learned rerankers; its value is to show where explicit field information helps or hurts and why calibration matters.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    rows, row_cache = matrix_rows()
    tests = paired_tests(row_cache)
    output = {
        "benchmark_version": BENCHMARK_VERSION,
        "rows": rows,
        "paired_tests": tests,
    }
    json_path = OUTPUT_DIR / "frozen_v0_4_information_layer_matrix.json"
    md_path = OUTPUT_DIR / "frozen_v0_4_information_layer_matrix.md"
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    md_path.write_text(render_md(rows, tests), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
