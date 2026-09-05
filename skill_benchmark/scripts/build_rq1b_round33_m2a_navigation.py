#!/usr/bin/env python3
"""Build M2 navigation metadata from M1-pinned originals without semantic scoring.

The output is a local navigation aid. It extracts only source-provided
frontmatter and Markdown headings so that small, full-source M2 reading queues
can be proposed. It does not infer similarity, form a candidate unit, write a
prompt, decide a gold label, or call a model/service.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


M1_STATUS = "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER"
ORIGINAL_FILE = "SKILL.original.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def collapse(value: str, limit: int) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    return compact if len(compact) <= limit else compact[: limit - 3].rstrip() + "..."


def front_matter_and_body(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    closing = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing is None:
        return {}, text
    front, fields = lines[1:closing], {}
    index = 0
    while index < len(front):
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", front[index])
        if not match:
            index += 1
            continue
        key, value = match.group(1), (match.group(2) or "").strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            blocks: list[str] = []
            index += 1
            while index < len(front) and (front[index].startswith(" ") or not front[index].strip()):
                blocks.append(front[index].strip())
                index += 1
            fields[key] = " ".join(part for part in blocks if part)
            continue
        fields[key] = value.strip("\"'")
        index += 1
    return fields, "\n".join(lines[closing + 1 :])


def headings(body: str, maximum: int = 6) -> list[str]:
    result: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            result.append(collapse(match.group(1), 160))
        if len(result) == maximum:
            break
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--m1-manifest",
        type=Path,
        default=Path(
            "skill_benchmark/rq1b_cross_source_public_benchmark/manifest/"
            "m1_round33_byte_verified_source_inventory_2026-08-28.jsonl"
        ),
    )
    parser.add_argument(
        "--staged-root",
        type=Path,
        default=Path("skill_benchmark/rq1b_cross_source_public_benchmark/staged_sources"),
    )
    parser.add_argument(
        "--exclude-stage-directory",
        action="append",
        default=[],
        help=(
            "Staging-directory name to omit from navigation; repeatable. "
            "This preserves byte-staged provenance while holding sources out "
            "of M2 discovery."
        ),
    )
    parser.add_argument(
        "--exclude-skill-id-file",
        type=Path,
        help=(
            "Optional JSON array of staged skill IDs held out of navigation. "
            "Use this for a documented path-level provenance hold without "
            "changing the underlying M1 byte-preserved source manifest."
        ),
    )
    parser.add_argument(
        "--output-inventory",
        type=Path,
        default=Path(
            "skill_benchmark/rq1b_cross_source_public_benchmark/manifest/"
            "m2a_round33_navigation_inventory_2026-08-28.jsonl"
        ),
    )
    parser.add_argument(
        "--output-summary",
        type=Path,
        default=Path(
            "skill_benchmark/rq1b_cross_source_public_benchmark/manifest/"
            "m2a_round33_navigation_summary_2026-08-28.json"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_rows = read_jsonl(args.m1_manifest.resolve())
    excluded_stage_directories = set(args.exclude_stage_directory)
    excluded_skill_ids: set[str] = set()
    if args.exclude_skill_id_file:
        raw_exclusions = json.loads(args.exclude_skill_id_file.read_text(encoding="utf-8"))
        if isinstance(raw_exclusions, dict):
            raw_exclusions = raw_exclusions.get("held_skill_ids")
        if not isinstance(raw_exclusions, list) or not all(isinstance(item, str) for item in raw_exclusions):
            raise SystemExit("exclude_skill_id_file must contain a JSON array of skill IDs")
        excluded_skill_ids = set(raw_exclusions)
    source_rows = [
        row
        for row in input_rows
        if row.get("source_admission_status") == M1_STATUS
        and str(row.get("stage_directory")) not in excluded_stage_directories
        and str(row.get("skill_id")) not in excluded_skill_ids
    ]
    if not source_rows:
        raise SystemExit("No M1-pinned source rows found")

    staged_root = args.staged_root.resolve()
    failures: list[str] = []
    output_rows: list[dict[str, Any]] = []
    for source_row in source_rows:
        stage_directory = str(source_row["stage_directory"])
        skill_id = str(source_row["skill_id"])
        original_path = staged_root / stage_directory / "skills" / skill_id / "source" / ORIGINAL_FILE
        if not original_path.is_file():
            failures.append(f"missing_staged_original:{stage_directory}/{skill_id}")
            continue
        actual_sha = sha256(original_path)
        if actual_sha != source_row.get("source_sha256"):
            failures.append(f"sha256_mismatch:{stage_directory}/{skill_id}")
            continue
        text = original_path.read_text(encoding="utf-8")
        front, body = front_matter_and_body(text)
        path_parts = Path(str(source_row["source_repository_path"])).parts
        output_rows.append(
            {
                "m2_navigation_status": "M2A_UNREVIEWED_SOURCE_NAVIGATION_ONLY",
                "skill_id": skill_id,
                "origin": source_row["origin"],
                "stage_directory": stage_directory,
                "repository_url": source_row["repository_url"],
                "pinned_commit": source_row["pinned_commit"],
                "license": source_row["license"],
                "license_status": source_row.get(
                    "license_status", "DECLARED_REPOSITORY_LICENSE"
                ),
                "source_repository_path": source_row["source_repository_path"],
                "source_url": source_row["source_url"],
                "source_sha256": actual_sha,
                "source_bytes": original_path.stat().st_size,
                "source_name": collapse(front.get("name", ""), 160),
                "source_description_preview": collapse(front.get("description", ""), 360),
                "source_heading_preview": headings(body),
                "repository_directory": "/".join(path_parts[:-1]),
                "local_original_path": str(original_path.relative_to(Path.cwd())),
                "m2_source_screen_status": "NOT_STARTED",
                "candidate_unit_status": "NOT_A_CLUSTER",
            }
        )

    output_rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    args.output_inventory.parent.mkdir(parents=True, exist_ok=True)
    args.output_inventory.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in output_rows),
        encoding="utf-8",
    )
    summary = {
        "status": (
            "M2A_PASS_LOCAL_NAVIGATION_ONLY_NOT_A_CLUSTER_OR_RESULT"
            if not failures and len(output_rows) == len(source_rows)
            else "M2A_FAIL_OR_INCOMPLETE_LOCAL_NAVIGATION_ONLY"
        ),
        "m1_input_count": len(source_rows),
        "excluded_stage_directories": sorted(excluded_stage_directories),
        "excluded_skill_ids_count": len(excluded_skill_ids),
        "inventory_record_count": len(output_rows),
        "by_origin": dict(sorted(Counter(str(row["origin"]) for row in output_rows).items())),
        "frontmatter_name_present_count": sum(bool(row["source_name"]) for row in output_rows),
        "frontmatter_description_present_count": sum(bool(row["source_description_preview"]) for row in output_rows),
        "heading_preview_present_count": sum(bool(row["source_heading_preview"]) for row in output_rows),
        "integrity_failures": failures,
        "exclusions": [
            "No semantic similarity score, embedding, retrieval score, or model call was computed.",
            "No candidate unit, prompt, field attribution, gold label, acceptable-set decision, or result was created.",
            "Navigation metadata only prioritises full-source reading; it does not establish a natural multi-candidate relation.",
        ],
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"].startswith("M2A_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
