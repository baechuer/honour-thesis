#!/usr/bin/env python3

from __future__ import annotations

import argparse
import gzip
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from export_skill_representations import (  # noqa: E402
    compact_text,
    dependency_aware,
    parse_frontmatter,
    parse_sections,
    structured_procedural,
)
from run_offline_selectors import approximate_tokens  # noqa: E402


ROOT = Path("skill_benchmark/external/skillrouter_eval_core")
RAW_DIR = ROOT / "raw"
DERIVED_DIR = ROOT / "derived"


def iter_jsonl_gz(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def iter_tier_rows(raw_dir: Path, tier: str) -> Iterable[dict[str, Any]]:
    for path in sorted((raw_dir / tier).glob("*.jsonl.gz")):
        yield from iter_jsonl_gz(path)


def load_tier_ids(raw_dir: Path, tier: str) -> set[str]:
    return {row["skill_id"] for row in iter_tier_rows(raw_dir, tier)}


def load_tasks(raw_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with (raw_dir / "tasks.jsonl").open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_relevance(raw_dir: Path) -> dict[str, Any]:
    return json.loads((raw_dir / "relevance.json").read_text(encoding="utf-8"))


def source_family(row: dict[str, Any]) -> str:
    source = str(row.get("source") or "unknown").strip()
    skill_id = str(row.get("skill_id") or "")
    if source:
        return source
    if "/" in skill_id:
        return skill_id.split("/", 1)[0]
    return "unknown"


def record_from_external_skill(row: dict[str, Any]) -> dict[str, Any]:
    body_text = str(row.get("body") or "")
    frontmatter, body = parse_frontmatter(body_text)
    sections = parse_sections(body)
    name = str(row.get("name") or frontmatter.get("name") or row["skill_id"])
    description = str(row.get("description") or frontmatter.get("description") or "")

    return {
        "name": name,
        "family": source_family(row),
        "path": "",
        "skill_dir": "",
        "description": description,
        "metadata": {},
        "body": body,
        "sections": sections,
        "source_body": "",
        "source_sections": {},
        "resources": [],
        "is_main_evaluated": False,
        "is_background": False,
    }


def i1_row(row: dict[str, Any], easy_ids: set[str], hard_only_ids: set[str]) -> dict[str, Any]:
    skill_id = row["skill_id"]
    name = str(row.get("name") or skill_id)
    description = str(row.get("description") or "")
    text = compact_text(
        [
            f"skill_id: {skill_id}",
            f"name: {name}",
            f"source: {row.get('source') or ''}",
            f"description: {description}",
        ]
    )
    return {
        "representation": "I1_flat_metadata",
        "skill_id": skill_id,
        "skill": skill_id,
        "name": name,
        "description": description,
        "source": row.get("source"),
        "in_easy": skill_id in easy_ids,
        "in_hard": True,
        "is_hard_only": skill_id in hard_only_ids,
        "text": text,
        "tokens_approx": approximate_tokens(text),
    }


def i2_row(row: dict[str, Any], easy_ids: set[str], hard_only_ids: set[str]) -> dict[str, Any]:
    skill_id = row["skill_id"]
    name = str(row.get("name") or skill_id)
    description = str(row.get("description") or "")
    body = str(row.get("body") or "")
    text = compact_text(
        [
            f"skill_id: {skill_id}",
            f"name: {name}",
            f"source: {row.get('source') or ''}",
            f"description: {description}",
            body,
        ]
    )
    return {
        "representation": "I2_full_artifact",
        "skill_id": skill_id,
        "skill": skill_id,
        "name": name,
        "description": description,
        "source": row.get("source"),
        "in_easy": skill_id in easy_ids,
        "in_hard": True,
        "is_hard_only": skill_id in hard_only_ids,
        "text": text,
        "tokens_approx": approximate_tokens(text),
    }


def i3_row(row: dict[str, Any], easy_ids: set[str], hard_only_ids: set[str]) -> dict[str, Any]:
    skill_id = row["skill_id"]
    base_record = record_from_external_skill(row)
    structured = structured_procedural(base_record)
    dependency = dependency_aware(base_record)
    text = compact_text(
        [
            str(structured.get("text") or ""),
            "dependency_profile: " + str(dependency.get("dependency_profile"))
            if dependency.get("dependency_profile")
            else "",
            "external_dependencies:\n"
            + "\n".join(f"- {item}" for item in dependency.get("external_dependencies", []))
            if dependency.get("external_dependencies")
            else "",
            "resource_signals:\n"
            + "\n".join(f"- {item}" for item in dependency.get("resource_signals", []))
            if dependency.get("resource_signals")
            else "",
        ]
    )
    return {
        "representation": "I3_structured_selection_fields",
        "skill_id": skill_id,
        "skill": skill_id,
        "name": row.get("name") or skill_id,
        "description": row.get("description") or "",
        "source": row.get("source"),
        "family": structured.get("family"),
        "in_easy": skill_id in easy_ids,
        "in_hard": True,
        "is_hard_only": skill_id in hard_only_ids,
        "use_when": structured.get("use_when", []),
        "not_for": structured.get("not_for", []),
        "preconditions": structured.get("preconditions", []),
        "workflow": structured.get("workflow", []),
        "output_shape": structured.get("output_shape", []),
        "writing_rules": structured.get("writing_rules", []),
        "dependency_profile": dependency.get("dependency_profile", ""),
        "external_dependencies": dependency.get("external_dependencies", []),
        "resource_signals": dependency.get("resource_signals", []),
        "text": text,
        "tokens_approx": approximate_tokens(text),
    }


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def parse_chunk(
    index: int,
    rows: list[dict[str, Any]],
    easy_ids: set[str],
    hard_only_ids: set[str],
    chunk_dir: Path,
    force: bool,
) -> dict[str, Any]:
    output_path = chunk_dir / f"i3_chunk_{index:05d}.jsonl"
    if output_path.exists() and not force:
        existing_count = sum(1 for _ in read_jsonl(output_path))
        if existing_count == len(rows):
            return {
                "chunk": index,
                "path": str(output_path),
                "rows": existing_count,
                "status": "skipped_existing",
            }
    parsed = [i3_row(row, easy_ids, hard_only_ids) for row in rows]
    count = write_jsonl(output_path, parsed)
    return {"chunk": index, "path": str(output_path), "rows": count, "status": "written"}


def chunked(rows: list[dict[str, Any]], size: int) -> Iterable[tuple[int, list[dict[str, Any]]]]:
    for start in range(0, len(rows), size):
        yield start // size, rows[start : start + size]


def write_tier_subset(
    *,
    tier: str,
    representation: str,
    source_path: Path,
    selected_ids: set[str],
    output_dir: Path,
) -> int:
    output_path = output_dir / f"{tier}_{representation}.jsonl"
    return write_jsonl(output_path, (row for row in read_jsonl(source_path) if row["skill_id"] in selected_ids))


def summarize_rows(path: Path) -> dict[str, Any]:
    count = 0
    tokens = 0
    non_empty = {
        "use_when": 0,
        "not_for": 0,
        "preconditions": 0,
        "workflow": 0,
        "output_shape": 0,
        "external_dependencies": 0,
        "resource_signals": 0,
    }
    for row in read_jsonl(path):
        count += 1
        tokens += int(row.get("tokens_approx") or 0)
        for key in non_empty:
            value = row.get(key)
            if isinstance(value, list) and value:
                non_empty[key] += 1
            elif isinstance(value, str) and value.strip():
                non_empty[key] += 1
    return {"rows": count, "tokens_approx": tokens, "non_empty_fields": non_empty}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare SkillRouter-Eval-Core as an external information-layer validation set."
    )
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--derived-dir", type=Path, default=DERIVED_DIR)
    parser.add_argument("--chunk-size", type=int, default=5000)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    raw_dir = args.raw_dir
    derived_dir = args.derived_dir
    derived_dir.mkdir(parents=True, exist_ok=True)

    tasks = load_tasks(raw_dir)
    relevance = load_relevance(raw_dir)
    scored_task_ids = [
        task["task_id"]
        for task in tasks
        if relevance.get(task["task_id"], {}).get("task_type") != "generic_only"
    ]
    easy_ids = load_tier_ids(raw_dir, "easy")
    hard_rows = list(iter_tier_rows(raw_dir, "hard"))
    hard_ids = {row["skill_id"] for row in hard_rows}
    hard_only_ids = hard_ids - easy_ids

    write_jsonl(derived_dir / "tasks_all.jsonl", tasks)
    write_jsonl(
        derived_dir / "tasks_scored.jsonl",
        (task for task in tasks if task["task_id"] in scored_task_ids),
    )
    (derived_dir / "hard_only_skill_ids.txt").write_text(
        "\n".join(sorted(hard_only_ids)) + "\n",
        encoding="utf-8",
    )

    by_id = {row["skill_id"]: row for row in hard_rows}
    all_rows = [by_id[skill_id] for skill_id in sorted(by_id)]

    rep_dir = derived_dir / "representations"
    i1_all = rep_dir / "all_I1.jsonl"
    i2_all = rep_dir / "all_I2.jsonl"
    i3_all = rep_dir / "all_I3.jsonl"

    write_jsonl(i1_all, (i1_row(row, easy_ids, hard_only_ids) for row in all_rows))
    write_jsonl(i2_all, (i2_row(row, easy_ids, hard_only_ids) for row in all_rows))

    chunk_dir = derived_dir / "i3_chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunks = list(chunked(all_rows, args.chunk_size))
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        chunk_reports = list(
            pool.map(
                lambda item: parse_chunk(
                    item[0],
                    item[1],
                    easy_ids,
                    hard_only_ids,
                    chunk_dir,
                    args.force,
                ),
                chunks,
            )
        )

    chunk_paths = [Path(report["path"]) for report in sorted(chunk_reports, key=lambda item: item["chunk"])]
    write_jsonl(i3_all, (row for path in chunk_paths for row in read_jsonl(path)))

    subset_counts: dict[str, int] = {}
    for tier, ids in [("easy", easy_ids), ("hard", hard_ids)]:
        subset_counts[f"{tier}_I1"] = write_tier_subset(
            tier=tier,
            representation="I1",
            source_path=i1_all,
            selected_ids=ids,
            output_dir=rep_dir,
        )
        subset_counts[f"{tier}_I2"] = write_tier_subset(
            tier=tier,
            representation="I2",
            source_path=i2_all,
            selected_ids=ids,
            output_dir=rep_dir,
        )
        subset_counts[f"{tier}_I3"] = write_tier_subset(
            tier=tier,
            representation="I3",
            source_path=i3_all,
            selected_ids=ids,
            output_dir=rep_dir,
        )

    field_summaries = {
        "all_I3": summarize_rows(i3_all),
        "easy_I3": summarize_rows(rep_dir / "easy_I3.jsonl"),
        "hard_I3": summarize_rows(rep_dir / "hard_I3.jsonl"),
    }

    manifest = {
        "source": "pipizhao/SkillRouter-Eval-Core",
        "raw_dir": str(raw_dir),
        "derived_dir": str(derived_dir),
        "task_count_all": len(tasks),
        "task_count_scored_default": len(scored_task_ids),
        "easy_skill_count": len(easy_ids),
        "hard_skill_count": len(hard_ids),
        "hard_only_skill_count": len(hard_only_ids),
        "hard_contains_all_easy": easy_ids.issubset(hard_ids),
        "chunk_size": args.chunk_size,
        "workers": args.workers,
        "i3_chunk_reports": chunk_reports,
        "subset_counts": subset_counts,
        "field_summaries": field_summaries,
        "artifacts": {
            "tasks_all": str(derived_dir / "tasks_all.jsonl"),
            "tasks_scored": str(derived_dir / "tasks_scored.jsonl"),
            "hard_only_skill_ids": str(derived_dir / "hard_only_skill_ids.txt"),
            "representations": str(rep_dir),
            "i3_chunks": str(chunk_dir),
        },
    }
    (derived_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "# SkillRouter Eval Core External Preparation",
        "",
        "This external dataset is kept separate from the controlled benchmark. It is used for portability checks, not as a replacement for the thesis benchmark.",
        "",
        f"- Source dataset: `pipizhao/SkillRouter-Eval-Core`",
        f"- All tasks: {len(tasks)}",
        f"- Default scored tasks: {len(scored_task_ids)}",
        f"- Easy skills: {len(easy_ids)}",
        f"- Hard skills: {len(hard_ids)}",
        f"- Hard-only distractors: {len(hard_only_ids)}",
        f"- Hard contains all Easy skills: {easy_ids.issubset(hard_ids)}",
        f"- I3 chunks: {len(chunk_reports)} blocks of up to {args.chunk_size} skills",
        "",
        "## Derived Representation Files",
        "",
        "| Tier | I1 flat metadata | I2 full artifact | I3 extracted fields |",
        "|---|---:|---:|---:|",
        f"| Easy | {subset_counts['easy_I1']} | {subset_counts['easy_I2']} | {subset_counts['easy_I3']} |",
        f"| Hard | {subset_counts['hard_I1']} | {subset_counts['hard_I2']} | {subset_counts['hard_I3']} |",
        "",
        "## I3 Field Coverage",
        "",
        "| Tier | Rows | Approx tokens | use_when | not_for | preconditions | workflow | output | dependencies | resources |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label in ["easy_I3", "hard_I3"]:
        summary = field_summaries[label]
        fields = summary["non_empty_fields"]
        lines.append(
            f"| {label.split('_')[0].title()} | {summary['rows']} | {summary['tokens_approx']} | "
            f"{fields['use_when']} | {fields['not_for']} | {fields['preconditions']} | "
            f"{fields['workflow']} | {fields['output_shape']} | {fields['external_dependencies']} | "
            f"{fields['resource_signals']} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- I1 corresponds to SkillRouter metadata: name, source, and description.",
            "- I2 corresponds to the full skill artifact: name, description, and body.",
            "- I3 uses the thesis structured-selection extraction logic over the public skill body. It is intentionally heuristic and resumable; model-assisted extraction can be added later as a separate extraction condition.",
            "- Hard-only distractors are listed in `hard_only_skill_ids.txt`.",
        ]
    )
    (derived_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2)[:4000])
    print(f"Wrote {derived_dir / 'README.md'}")


if __name__ == "__main__":
    main()
