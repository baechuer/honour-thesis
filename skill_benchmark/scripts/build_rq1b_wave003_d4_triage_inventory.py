#!/usr/bin/env python3
"""Build a source-only D4a navigation inventory for Wave 003 RQ1b artifacts.

The script reads the canonical Wave 003 manifest and byte-preserved originals,
then emits source-provided navigation metadata. It does not score similarity,
form pairs, assign fields or labels, author prompts, or call a model/service.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


CANONICAL_STATUS = "NET_NEW_EXACT_BYTE_DISTINCT_STAGED_ARTIFACT"
INVENTORY_STATUS = "UNREVIEWED_D4_SOURCE_ONLY"
ORIGINAL_FILE = "SKILL.original.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def collapse(value: str, limit: int) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    return compact if len(compact) <= limit else compact[: limit - 3].rstrip() + "..."


def unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def front_matter_and_body(text: str) -> tuple[dict[str, str], str]:
    """Extract a small front-matter subset for navigation, not semantic QA."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    closing_index = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing_index is None:
        return {}, text

    front = lines[1:closing_index]
    fields: dict[str, str] = {}
    index = 0
    while index < len(front):
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", front[index])
        if not match:
            index += 1
            continue
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        if raw_value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block: list[str] = []
            index += 1
            while index < len(front) and (front[index].startswith(" ") or not front[index].strip()):
                block.append(front[index].strip())
                index += 1
            fields[key] = " ".join(part for part in block if part)
            continue
        fields[key] = unquote_scalar(raw_value)
        index += 1
    return fields, "\n".join(lines[closing_index + 1 :])


def markdown_headings(body: str, maximum: int = 6) -> list[str]:
    headings: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.append(collapse(match.group(1), 160))
        if len(headings) == maximum:
            break
    return headings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate-pool-manifest",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_003_candidate_pool_manifest.jsonl"),
    )
    parser.add_argument(
        "--staged-root",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/staged_sources"),
    )
    parser.add_argument(
        "--output-inventory",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_003_d4a_source_navigation_inventory.jsonl"),
    )
    parser.add_argument(
        "--output-summary",
        type=Path,
        default=Path("skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_003_d4a_source_navigation_summary.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_rows = read_jsonl(args.candidate_pool_manifest.resolve())
    canonical_rows = [row for row in source_rows if row.get("candidate_pool_status") == CANONICAL_STATUS]
    if not canonical_rows:
        raise SystemExit("No canonical Wave 003 net-new source rows found")

    output_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    staged_root = args.staged_root.resolve()
    for source_row in canonical_rows:
        stage_directory = str(source_row["stage_directory"])
        skill_id = str(source_row["skill_id"])
        source_path = staged_root / stage_directory / "skills" / skill_id / "source" / ORIGINAL_FILE
        if not source_path.is_file():
            failures.append(f"missing_staged_original:{stage_directory}/{skill_id}")
            continue
        actual_bytes = source_path.stat().st_size
        actual_sha256 = sha256(source_path)
        if actual_bytes != source_row.get("source_bytes"):
            failures.append(f"byte_length_mismatch:{stage_directory}/{skill_id}")
            continue
        if actual_sha256 != source_row.get("source_sha256"):
            failures.append(f"sha256_mismatch:{stage_directory}/{skill_id}")
            continue

        text = source_path.read_text(encoding="utf-8")
        front_matter, body = front_matter_and_body(text)
        source_path_parts = Path(str(source_row["source_repository_path"])).parts
        output_rows.append(
            {
                "d4a_status": INVENTORY_STATUS,
                "skill_id": skill_id,
                "origin": source_row["origin"],
                "stage_directory": stage_directory,
                "repository_url": source_row["repository_url"],
                "pinned_commit": source_row["pinned_commit"],
                "license": source_row["license"],
                "source_repository_path": source_row["source_repository_path"],
                "source_url": source_row["source_url"],
                "source_sha256": actual_sha256,
                "source_bytes": actual_bytes,
                "source_name": collapse(front_matter.get("name", ""), 160),
                "source_description_preview": collapse(front_matter.get("description", ""), 360),
                "source_heading_preview": markdown_headings(body),
                "repository_directory": "/".join(source_path_parts[:-1]),
                "local_original_path": str(source_path.relative_to(Path.cwd())),
                "manual_screening_status": "NOT_STARTED",
                "semantic_evidence_status": "NOT_ASSESSED",
                "cluster_status": "NOT_A_CLUSTER",
            }
        )

    output_rows.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    args.output_inventory.parent.mkdir(parents=True, exist_ok=True)
    args.output_inventory.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in output_rows), encoding="utf-8"
    )
    summary = {
        "status": (
            "D4A_PASS_LOCAL_SOURCE_NAVIGATION_INVENTORY_NOT_A_CLUSTER_OR_RESULT"
            if not failures and len(output_rows) == len(canonical_rows)
            else "D4A_FAIL_OR_INCOMPLETE_LOCAL_SOURCE_NAVIGATION_INVENTORY"
        ),
        "canonical_net_new_input_count": len(canonical_rows),
        "inventory_record_count": len(output_rows),
        "by_origin": dict(sorted(Counter(str(row["origin"]) for row in output_rows).items())),
        "front_matter_name_present_count": sum(bool(row["source_name"]) for row in output_rows),
        "front_matter_description_present_count": sum(bool(row["source_description_preview"]) for row in output_rows),
        "heading_preview_present_count": sum(bool(row["source_heading_preview"]) for row in output_rows),
        "integrity_failures": failures,
        "exclusions": [
            "No semantic similarity score, embedding, or retrieval score was computed.",
            "No pair, family, cluster, prompt, field attribution, gold label, acceptable-set decision, or result was created.",
            "Names, descriptions, directories, and headings are navigation metadata only and do not establish semantic-neighbour validity.",
            "Every promotion or rejection still requires manual full-source reading under D4b/D4c.",
        ],
    }
    args.output_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"].startswith("D4A_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
