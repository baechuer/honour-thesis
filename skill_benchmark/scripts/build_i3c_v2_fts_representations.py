#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_offline_selectors import approximate_tokens  # noqa: E402


ROOT = Path("skill_benchmark/external/skillrouter_eval_core")
REP_DIR = ROOT / "derived" / "representations"
DEFAULT_I3C = REP_DIR / "i3c_v2_full_all" / "I3C_V2_full_all_cleaned.jsonl"

FIELD_ORDER = [
    ("use_conditions", "use_when"),
    ("input_preconditions", "input_preconditions"),
    ("output_artifacts", "output_artifacts"),
    ("workflow_steps", "workflow_steps"),
    ("constraints_boundaries", "constraints_boundaries"),
    ("dependencies_resources", "dependencies_resources"),
    ("success_criteria", "success_criteria"),
]


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return list(iter_jsonl(path))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
            count += 1
    return count


def clean_text(value: Any) -> str:
    text = str(value or "")
    return "".join(ch if not 0xD800 <= ord(ch) <= 0xDFFF else "?" for ch in text)


def clean_list(values: Iterable[Any]) -> list[str]:
    return [clean_text(value) for value in values]


def field_item_text(item: dict[str, Any]) -> str:
    text = clean_text(item.get("text") or item.get("action") or "").strip()
    if text:
        return text
    evidence = clean_text(item.get("evidence") or "").strip()
    return evidence


def serialize_i3c(row: dict[str, Any]) -> str:
    parts: list[str] = [
        f"name: {clean_text(row.get('name') or row.get('skill_id'))}",
        f"description: {clean_text(row.get('description') or '')}",
    ]
    fields = row.get("fields") or {}
    for source_key, label in FIELD_ORDER:
        items = fields.get(source_key) or []
        texts = [field_item_text(item) for item in items if field_item_text(item)]
        if texts:
            parts.append(f"{label}:")
            parts.extend(f"- {text}" for text in texts)
    absent = row.get("absent_fields") or []
    if absent:
        parts.append("absent_fields:")
        parts.append("- " + ", ".join(clean_text(value) for value in absent))
    return "\n".join(part for part in parts if part).strip() + "\n"


def field_counts(row: dict[str, Any]) -> dict[str, int]:
    fields = row.get("fields") or {}
    return {key: len(fields.get(key) or []) for key, _label in FIELD_ORDER}


def build_rows(
    *,
    tier_rows: list[dict[str, Any]],
    i3c_by_id: dict[str, dict[str, Any]],
    representation_name: str,
) -> Iterable[dict[str, Any]]:
    for tier_row in tier_rows:
        skill_id = str(tier_row["skill_id"])
        i3c = i3c_by_id.get(skill_id)
        if i3c is None:
            text = (
                f"name: {clean_text(tier_row.get('name') or skill_id)}\n"
                f"description: {clean_text(tier_row.get('description') or '')}\n"
            )
            parse_failed = True
            absent_fields = [key for key, _label in FIELD_ORDER]
            qa_warning_count = 1
            counts = {key: 0 for key, _label in FIELD_ORDER}
            schema_version = "I3C_MISSING_FROM_FULL_ALL"
        else:
            text = serialize_i3c(i3c)
            parse_failed = bool(i3c.get("parse_failed"))
            absent_fields = i3c.get("absent_fields") or []
            qa_warning_count = len(i3c.get("qa_warnings") or [])
            counts = field_counts(i3c)
            schema_version = str(i3c.get("schema_version") or "I3C_SUBAGENT_EXTRACTION_V2")
        output = {
            "skill_id": skill_id,
            "skill": clean_text(tier_row.get("skill") or skill_id),
            "name": clean_text(tier_row.get("name") or (i3c or {}).get("name") or skill_id),
            "description": clean_text(tier_row.get("description") or (i3c or {}).get("description") or ""),
            "source": clean_text(tier_row.get("source") or (i3c or {}).get("source")),
            "representation": representation_name,
            "schema_version": schema_version,
            "parse_failed": parse_failed,
            "absent_fields": clean_list(absent_fields),
            "field_counts": counts,
            "qa_warning_count": qa_warning_count,
            "in_easy": bool(tier_row.get("in_easy")),
            "in_hard": bool(tier_row.get("in_hard")),
            "is_hard_only": bool(tier_row.get("is_hard_only")),
            "text": text,
            "tokens_approx": approximate_tokens(text),
        }
        yield output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build FTS-ready SkillRouter I3C V2 field representations."
    )
    parser.add_argument("--i3c", type=Path, default=DEFAULT_I3C)
    parser.add_argument("--rep-dir", type=Path, default=REP_DIR)
    parser.add_argument("--tiers", default="easy,hard")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    i3c_by_id = {str(row["skill_id"]): row for row in iter_jsonl(args.i3c)}
    representation_name = "I3C_V2_structured_fields"
    summary: dict[str, Any] = {
        "source_i3c": str(args.i3c),
        "representation": representation_name,
        "tiers": {},
    }

    for tier in [value.strip().lower() for value in args.tiers.split(",") if value.strip()]:
        source = args.rep_dir / f"{tier}_I2.jsonl"
        output = args.rep_dir / f"{tier}_I3C.jsonl"
        if output.exists() and not args.force:
            raise FileExistsError(f"{output} exists; pass --force to overwrite")
        tier_rows = read_jsonl(source)
        count = write_jsonl(
            output,
            build_rows(
                tier_rows=tier_rows,
                i3c_by_id=i3c_by_id,
                representation_name=representation_name,
            ),
        )
        missing = sum(1 for row in tier_rows if str(row["skill_id"]) not in i3c_by_id)
        tokens = sum(int(row.get("tokens_approx") or 0) for row in iter_jsonl(output))
        summary["tiers"][tier] = {
            "source": str(source),
            "output": str(output),
            "rows": count,
            "missing_i3c_rows": missing,
            "tokens_approx": tokens,
        }
        print(f"{tier}: wrote {count} rows to {output} ({missing} missing I3C)")

    summary_path = args.rep_dir / "i3c_v2_fts_representation_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
