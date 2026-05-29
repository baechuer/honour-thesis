#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any


FIELDS = [
    "routing_trigger",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "constraints_boundaries",
    "dependencies_tools",
    "resources_references",
    "examples_tests",
    "safety_side_effects",
    "portability_environment",
    "hierarchy_links",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def select_sample(rows: list[dict[str, Any]], sample_size: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_origin[row.get("origin") or "unknown"].append(row)

    selected: list[dict[str, Any]] = []
    for origin_rows in by_origin.values():
        selected.append(rng.choice(origin_rows))

    by_coverage = sorted(rows, key=lambda row: (row["explicit_or_extractable_fields"], row["skill"]))
    candidates = [
        *by_coverage[: max(3, sample_size // 4)],
        *by_coverage[len(by_coverage) // 2 : len(by_coverage) // 2 + max(3, sample_size // 4)],
        *by_coverage[-max(3, sample_size // 4) :],
    ]
    rng.shuffle(candidates)
    for row in candidates:
        if len(selected) >= sample_size:
            break
        if row["skill"] not in {item["skill"] for item in selected}:
            selected.append(row)

    remaining = [row for row in rows if row["skill"] not in {item["skill"] for item in selected}]
    rng.shuffle(remaining)
    for row in remaining:
        if len(selected) >= sample_size:
            break
        selected.append(row)
    return selected[:sample_size]


def render_field_table(row: dict[str, Any]) -> list[str]:
    lines = [
        "| Field | Auto Status | Evidence To Check | Human Status | Notes |",
        "|---|---|---|---|---|",
    ]
    for field in FIELDS:
        data = row["fields"][field]
        evidence = " / ".join(data.get("evidence") or [])
        evidence = evidence.replace("|", "\\|")
        if len(evidence) > 260:
            evidence = evidence[:257] + "..."
        lines.append(f"| `{field}` | `{data['status']}` | {evidence} |  |  |")
    return lines


def render_markdown(rows: list[dict[str, Any]], source_jsonl: Path) -> str:
    lines = [
        "# Public Skill Field Manual Review Packet",
        "",
        "Purpose: manually check whether the automated public-skill field audit is overcounting or undercounting field evidence.",
        "",
        f"Source audit file: `{source_jsonl}`",
        "",
        "Review labels to fill in:",
        "",
        "- `correct`: automatic status is reasonable.",
        "- `overcount`: automatic status claims evidence that is too weak.",
        "- `undercount`: automatic status missed evidence visible to a human.",
        "- `ambiguous`: the skill is too broad or underspecified to label confidently.",
        "",
        "Pass target before final thesis claims: at least 80% of reviewed field labels should be `correct`, and any systematic overcount should be fixed or disclosed.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['skill']}",
                "",
                f"- Origin: `{row.get('origin') or 'unknown'}`",
                f"- Source name: `{row.get('source_name') or ''}`",
                f"- Source URL: {row.get('source_url') or ''}",
                f"- Audit file: `{row['audit_file']}`",
                f"- Word count: {row['body_word_count'] + row['frontmatter_word_count']}",
                f"- Headings: {', '.join(row.get('headings') or [])[:500]}",
                "",
                "Manual decision:",
                "",
                "- Overall: ",
                "- Broad/hierarchical/atomic? ",
                "- Does this skill support our representation-field taxonomy? ",
                "",
                *render_field_table(row),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Build a stratified manual review packet from the public skill audit JSONL.")
    parser.add_argument("--input-jsonl", default=str(repo_root / "outputs" / "public_skill_field_audit.jsonl"))
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "public_skill_field_manual_review_packet.md"))
    parser.add_argument("--sample-size", type=int, default=15)
    parser.add_argument("--seed", type=int, default=4990)
    args = parser.parse_args()

    input_jsonl = Path(args.input_jsonl)
    rows = load_jsonl(input_jsonl)
    sample = select_sample(rows, min(args.sample_size, len(rows)), args.seed)
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(sample, input_jsonl), encoding="utf-8")
    print(f"Loaded audit rows: {len(rows)}")
    print(f"Manual review sample rows: {len(sample)}")
    print(f"Wrote {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
