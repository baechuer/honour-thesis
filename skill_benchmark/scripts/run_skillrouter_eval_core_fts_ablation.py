#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_offline_selectors import approximate_tokens, tokenize  # noqa: E402


ROOT = Path("skill_benchmark/external/skillrouter_eval_core")
RAW_DIR = ROOT / "raw"
DERIVED_DIR = ROOT / "derived"
OUTPUT_DIR = ROOT / "outputs"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def load_relevance(raw_dir: Path) -> dict[str, Any]:
    return json.loads((raw_dir / "relevance.json").read_text(encoding="utf-8"))


def load_scored_tasks(derived_dir: Path) -> list[dict[str, Any]]:
    path = derived_dir / "tasks_scored.jsonl"
    if path.exists():
        return read_jsonl(path)
    raw_tasks = read_jsonl(derived_dir / "tasks_all.jsonl")
    relevance = load_relevance(RAW_DIR)
    return [
        task
        for task in raw_tasks
        if relevance.get(task["task_id"], {}).get("task_type") != "generic_only"
    ]


def escape_fts_token(token: str) -> str:
    cleaned = "".join(ch for ch in token if ch.isalnum() or ch in {"_", "-"})
    return f'"{cleaned}"' if cleaned else ""


def fts_query(text: str) -> str:
    tokens = []
    for token in tokenize(text):
        escaped = escape_fts_token(token)
        if escaped:
            tokens.append(escaped)
    # OR improves candidate recall for long SkillRouter task descriptions.
    return " OR ".join(tokens[:80])


def build_fts_index(db_path: Path, rep_path: Path, force: bool = False) -> None:
    if db_path.exists() and not force:
        return
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute(
        "CREATE VIRTUAL TABLE docs USING fts5(skill_id UNINDEXED, name UNINDEXED, text)"
    )
    batch: list[tuple[str, str, str]] = []
    for row in iter_jsonl(rep_path):
        batch.append(
            (
                str(row["skill_id"]),
                str(row.get("name") or ""),
                str(row.get("text") or ""),
            )
        )
        if len(batch) >= 1000:
            conn.executemany("INSERT INTO docs(skill_id, name, text) VALUES (?, ?, ?)", batch)
            batch.clear()
    if batch:
        conn.executemany("INSERT INTO docs(skill_id, name, text) VALUES (?, ?, ?)", batch)
    conn.commit()
    conn.execute("INSERT INTO docs(docs) VALUES ('optimize')")
    conn.commit()
    conn.close()


def retrieve(conn: sqlite3.Connection, query: str, limit: int) -> list[dict[str, Any]]:
    match_query = fts_query(query)
    if not match_query:
        return []
    rows = conn.execute(
        """
        SELECT skill_id, name, bm25(docs) AS distance
        FROM docs
        WHERE docs MATCH ?
        ORDER BY distance ASC
        LIMIT ?
        """,
        (match_query, limit),
    ).fetchall()
    return [
        {
            "skill_id": skill_id,
            "name": name,
            # Higher is better for consistency with the local benchmark reports.
            "score": round(-float(distance), 6),
        }
        for skill_id, name, distance in rows
    ]


def dcg(grades: list[float]) -> float:
    return sum((2**grade - 1) / math.log2(index + 2) for index, grade in enumerate(grades))


def evaluate_task(
    *,
    ranking: list[dict[str, Any]],
    relevance_row: dict[str, Any],
    cutoffs: list[int],
) -> dict[str, Any]:
    ranked_ids = [row["skill_id"] for row in ranking]
    gold_ids = set(relevance_row.get("core_gt_ids") or relevance_row.get("gt_skill_ids") or [])
    graded_relevance = {
        str(skill_id): float(grade)
        for skill_id, grade in (relevance_row.get("relevance") or {}).items()
    }
    if not gold_ids:
        return {
            "hit_at_1": 0.0,
            "mrr_at_10": 0.0,
            "recall": {str(k): 0.0 for k in cutoffs},
            "full_coverage": {str(k): 0.0 for k in cutoffs},
            "ndcg_at_10": 0.0,
        }

    hit_at_1 = float(bool(ranked_ids and ranked_ids[0] in gold_ids))
    first_rank = next((index + 1 for index, skill_id in enumerate(ranked_ids[:10]) if skill_id in gold_ids), None)
    mrr_at_10 = 1.0 / first_rank if first_rank else 0.0
    recall = {
        str(k): len(gold_ids & set(ranked_ids[:k])) / len(gold_ids)
        for k in cutoffs
    }
    full_coverage = {
        str(k): float(gold_ids.issubset(set(ranked_ids[:k])))
        for k in cutoffs
    }

    grades = [graded_relevance.get(skill_id, 0.0) for skill_id in ranked_ids[:10]]
    ideal_grades = sorted(graded_relevance.values(), reverse=True)[:10]
    ideal = dcg(ideal_grades)
    ndcg_at_10 = dcg(grades) / ideal if ideal else 0.0
    return {
        "hit_at_1": hit_at_1,
        "mrr_at_10": mrr_at_10,
        "recall": recall,
        "full_coverage": full_coverage,
        "ndcg_at_10": ndcg_at_10,
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def summarize_task_rows(rows: list[dict[str, Any]], cutoffs: list[int]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "task_count": len(rows),
        "hit_at_1": mean([row["metrics"]["hit_at_1"] for row in rows]),
        "mrr_at_10": mean([row["metrics"]["mrr_at_10"] for row in rows]),
        "ndcg_at_10": mean([row["metrics"]["ndcg_at_10"] for row in rows]),
        "recall": {},
        "full_coverage": {},
        "hard_only_top1_rate": mean([float(row.get("top1_hard_only", False)) for row in rows]),
        "empty_ranking_rate": mean([float(not row["ranking"]) for row in rows]),
    }
    for k in cutoffs:
        key = str(k)
        summary["recall"][key] = mean([row["metrics"]["recall"][key] for row in rows])
        summary["full_coverage"][key] = mean([row["metrics"]["full_coverage"][key] for row in rows])
    by_num_skills: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        label = "single" if int(row.get("num_gold_skills") or 0) == 1 else "multi"
        by_num_skills.setdefault(label, []).append(row)
    summary["by_task_width"] = {
        key: {
            "task_count": len(value),
            "hit_at_1": mean([row["metrics"]["hit_at_1"] for row in value]),
            "mrr_at_10": mean([row["metrics"]["mrr_at_10"] for row in value]),
            "recall_at_20": mean([row["metrics"]["recall"]["20"] for row in value]),
            "full_coverage_at_20": mean([row["metrics"]["full_coverage"]["20"] for row in value]),
        }
        for key, value in by_num_skills.items()
    }
    return summary


def representation_path(derived_dir: Path, tier: str, representation: str) -> Path:
    return derived_dir / "representations" / f"{tier}_{representation.upper()}.jsonl"


def representation_token_count(path: Path) -> int:
    return sum(int(row.get("tokens_approx") or approximate_tokens(str(row.get("text") or ""))) for row in iter_jsonl(path))


def run_condition(
    *,
    tier: str,
    representation: str,
    tasks: list[dict[str, Any]],
    relevance: dict[str, Any],
    derived_dir: Path,
    output_dir: Path,
    ranking_limit: int,
    cutoffs: list[int],
    force_index: bool,
    hard_only_ids: set[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rep_path = representation_path(derived_dir, tier, representation)
    if not rep_path.exists():
        raise FileNotFoundError(rep_path)
    db_path = output_dir / "fts_indexes" / f"{tier}_{representation}.sqlite"
    index_start = time.perf_counter()
    build_fts_index(db_path, rep_path, force=force_index)
    index_elapsed_ms = (time.perf_counter() - index_start) * 1000

    conn = sqlite3.connect(db_path)
    rows: list[dict[str, Any]] = []
    query_start = time.perf_counter()
    for task in tasks:
        task_id = task["task_id"]
        rel = relevance[task_id]
        ranking = retrieve(conn, task["instruction_text"], ranking_limit)
        metrics = evaluate_task(ranking=ranking, relevance_row=rel, cutoffs=cutoffs)
        gold_ids = rel.get("core_gt_ids") or rel.get("gt_skill_ids") or []
        rows.append(
            {
                "task_id": task_id,
                "domain": task.get("domain"),
                "difficulty": task.get("difficulty"),
                "task_type": rel.get("task_type"),
                "num_gold_skills": len(gold_ids),
                "gold_skill_ids": gold_ids,
                "instruction_text": task.get("instruction_text"),
                "ranking": ranking[:ranking_limit],
                "top1_hard_only": bool(ranking and ranking[0]["skill_id"] in hard_only_ids),
                "metrics": metrics,
            }
        )
    query_elapsed_ms = (time.perf_counter() - query_start) * 1000
    conn.close()

    run_summary = summarize_task_rows(rows, cutoffs)
    run_summary.update(
        {
            "tier": tier,
            "representation": representation.upper(),
            "retriever": "SQLite FTS5 BM25",
            "ranking_limit": ranking_limit,
            "selector_visible_tokens_approx": representation_token_count(rep_path),
            "index_elapsed_ms": round(index_elapsed_ms, 2),
            "query_elapsed_ms": round(query_elapsed_ms, 2),
        }
    )
    return rows, run_summary


def pct(value: float) -> str:
    return f"{value:.1%}"


def render_markdown(report: dict[str, Any]) -> str:
    cutoffs = [str(value) for value in report["cutoffs"]]
    recall_headers = [f"Recall@{value}" for value in cutoffs]
    full_coverage_headers = [f"FullCov@{value}" for value in cutoffs]
    summary_headers = [
        "Tier",
        "Information layer",
        "N",
        "Hit@1",
        "MRR@10",
        "nDCG@10",
        *recall_headers,
        *full_coverage_headers,
        "Hard-only top1",
        "Tokens",
        "Query ms",
    ]
    lines = [
        "# SkillRouter-Eval-Core External Information-Layer Ablation",
        "",
        "This report evaluates the thesis information layers on the public SkillRouter-Eval-Core benchmark. It is an external validation track, not a replacement for the controlled v0.4 benchmark.",
        "",
        f"- Source: `pipizhao/SkillRouter-Eval-Core`",
        f"- Scored tasks: {report['task_count']}",
        f"- Retriever: SQLite FTS5 BM25, disk-backed lexical retrieval",
        f"- Ranking limit: top-{report['ranking_limit']}",
        "",
        "## Summary",
        "",
        "| " + " | ".join(summary_headers) + " |",
        "|---|---|" + "|".join(["---:"] * (len(summary_headers) - 2)) + "|",
    ]
    for row in report["summary"]:
        recall_values = [pct(row["recall"][value]) for value in cutoffs]
        full_coverage_values = [pct(row["full_coverage"][value]) for value in cutoffs]
        values = [
            row["tier"],
            row["representation"],
            str(row["task_count"]),
            pct(row["hit_at_1"]),
            f"{row['mrr_at_10']:.3f}",
            f"{row['ndcg_at_10']:.3f}",
            *recall_values,
            *full_coverage_values,
            pct(row["hard_only_top1_rate"]),
            str(row["selector_visible_tokens_approx"]),
            f"{row['query_elapsed_ms']:.1f}",
        ]
        lines.append(
            "| " + " | ".join(values) + " |"
        )
    lines.extend(
        [
            "",
            "## Metric Definitions",
            "",
            "- `Hit@1`: whether the top-ranked skill is one of the core gold skills.",
            "- `MRR@10`: reciprocal rank of the first core gold skill in the top 10.",
            "- `Recall@k`: fraction of core gold skills retrieved in the top k; this matters because many SkillRouter tasks require multiple skills.",
            "- `FullCov@k`: whether all core gold skills are retrieved in the top k.",
            "- `nDCG@10`: graded relevance ranking quality using SkillRouter's relevance labels.",
            "- `Hard-only top1`: on the Hard tier, the rate at which a generated hard distractor is ranked first.",
            "",
            "## Reading Notes",
            "",
            "- Compare the listed representation layers within the same tier to isolate information-layer effects under the same retriever.",
            "- I2 full artifacts are expected to be strong but expensive; I3 is valuable if it improves over I1 or approaches I2 with less visible text.",
            "- This first pass uses lexical FTS/BM25. Dense and reranking validations should be added only after checking that I3 extraction quality is acceptable.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run external SkillRouter information-layer BM25/FTS ablation.")
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--derived-dir", type=Path, default=DERIVED_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--tiers", default="easy,hard")
    parser.add_argument("--representations", default="I1,I2,I3")
    parser.add_argument("--ranking-limit", type=int, default=50)
    parser.add_argument("--cutoffs", default="10,20,50")
    parser.add_argument("--force-index", action="store_true")
    parser.add_argument("--output-prefix", default="skillrouter_eval_core_fts_information_layers")
    args = parser.parse_args()

    tasks = load_scored_tasks(args.derived_dir)
    relevance = load_relevance(args.raw_dir)
    hard_only_path = args.derived_dir / "hard_only_skill_ids.txt"
    hard_only_ids = set(hard_only_path.read_text(encoding="utf-8").split()) if hard_only_path.exists() else set()
    cutoffs = [int(value) for value in args.cutoffs.split(",") if value.strip()]
    tiers = [value.strip().lower() for value in args.tiers.split(",") if value.strip()]
    representations = [value.strip().upper() for value in args.representations.split(",") if value.strip()]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "source": "pipizhao/SkillRouter-Eval-Core",
        "task_count": len(tasks),
        "ranking_limit": args.ranking_limit,
        "cutoffs": cutoffs,
        "summary": [],
        "results": {},
    }

    for tier in tiers:
        for representation in representations:
            key = f"{tier}_{representation}"
            rows, summary = run_condition(
                tier=tier,
                representation=representation,
                tasks=tasks,
                relevance=relevance,
                derived_dir=args.derived_dir,
                output_dir=args.output_dir,
                ranking_limit=args.ranking_limit,
                cutoffs=cutoffs,
                force_index=args.force_index,
                hard_only_ids=hard_only_ids,
            )
            report["summary"].append(summary)
            report["results"][key] = rows
            print(
                f"{key}: Hit@1={summary['hit_at_1']:.1%} "
                f"MRR@10={summary['mrr_at_10']:.3f} "
                f"R@20={summary['recall']['20']:.1%} "
                f"FullCov@20={summary['full_coverage']['20']:.1%}"
            )

    json_path = args.output_dir / f"{args.output_prefix}.json"
    md_path = args.output_dir / f"{args.output_prefix}.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
