#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


CORE_FIELDS = [
    "use_when",
    "not_for",
    "preconditions",
    "workflow",
    "output_shape",
    "writing_rules",
]


THRESHOLDS = {
    "use_when": 1.0,
    "workflow": 1.0,
    "writing_rules": 0.9,
    "not_for": 0.8,
    "output_shape": 0.8,
    "preconditions": 0.3,
}


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def pct(value: int, total: int) -> str:
    return f"{value}/{total} ({value / total:.1%})" if total else "0/0"


def pass_label(rate: float, threshold: float) -> str:
    if rate >= threshold:
        return "PASS"
    if rate >= max(0.0, threshold - 0.2):
        return "WARN"
    return "FAIL"


def summarize_field_coverage(rows: list[dict]) -> list[str]:
    main = [row for row in rows if row.get("is_main_evaluated")]
    lines = ["## Structured Field Coverage", ""]
    lines.append("| Field | Main coverage | Threshold | Status |")
    lines.append("|---|---:|---:|---|")
    for field in CORE_FIELDS:
        count = sum(1 for row in main if row.get(field))
        total = len(main)
        rate = count / total if total else 0.0
        threshold = THRESHOLDS[field]
        lines.append(f"| `{field}` | {pct(count, total)} | {threshold:.0%} | {pass_label(rate, threshold)} |")
    return lines


def summarize_by_family(rows: list[dict]) -> list[str]:
    by_family: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("is_main_evaluated"):
            by_family[row["family"]].append(row)

    lines = ["", "## Main Family Coverage", ""]
    lines.append("| Family | Skills | Use when | Not for | Workflow | Output |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for family in sorted(by_family):
        family_rows = by_family[family]
        total = len(family_rows)
        lines.append(
            "| "
            + family
            + f" | {total}"
            + f" | {sum(1 for row in family_rows if row.get('use_when'))}/{total}"
            + f" | {sum(1 for row in family_rows if row.get('not_for'))}/{total}"
            + f" | {sum(1 for row in family_rows if row.get('workflow'))}/{total}"
            + f" | {sum(1 for row in family_rows if row.get('output_shape'))}/{total}"
            + " |"
        )
    return lines


def summarize_dependency(rows: list[dict]) -> list[str]:
    lines = ["", "## Dependency / Resource Coverage", ""]
    public = [row for row in rows if row["family"] == "public_imported_background"]
    main_toolish = [
        row
        for row in rows
        if row.get("is_main_evaluated")
        and row["family"] in {"browser_web_automation", "security_appsec", "code_github_workflow"}
    ]
    dep_count = sum(1 for row in public if row.get("external_dependencies") or row.get("dependency_profile"))
    resource_count = sum(1 for row in public if row.get("resource_signals") or row.get("resource_files"))
    toolish_dep_count = sum(
        1 for row in main_toolish if row.get("external_dependencies") or row.get("dependency_profile") or row.get("resource_files")
    )

    lines.append("| Slice | Skills | Dependency signal | Resource signal | Status |")
    lines.append("|---|---:|---:|---:|---|")
    public_dep_rate = dep_count / len(public) if public else 0.0
    public_resource_rate = resource_count / len(public) if public else 0.0
    lines.append(
        f"| public imported background | {len(public)} | {pct(dep_count, len(public))} | {pct(resource_count, len(public))} | "
        f"{'PASS' if public_dep_rate == 1.0 and public_resource_rate == 1.0 else 'FAIL'} |"
    )
    toolish_rate = toolish_dep_count / len(main_toolish) if main_toolish else 0.0
    lines.append(
        f"| main tool-heavy clusters | {len(main_toolish)} | {pct(toolish_dep_count, len(main_toolish))} | not required | "
        f"{pass_label(toolish_rate, 0.3)} |"
    )
    return lines


def summarize_graph(edges: list[dict]) -> list[str]:
    edge_counts = Counter(row["edge"] for row in edges)
    skills = {row["skill"] for row in edges}
    lines = ["", "## Graph Edge Coverage", ""]
    lines.append(f"- Skills represented in graph: {len(skills)}")
    lines.append(f"- Total edges: {len(edges)}")
    lines.append("")
    lines.append("| Edge type | Count |")
    lines.append("|---|---:|")
    for edge, count in sorted(edge_counts.items()):
        lines.append(f"| `{edge}` | {count} |")
    return lines


def summarize_failures(rows: list[dict]) -> list[str]:
    main = [row for row in rows if row.get("is_main_evaluated")]
    lines = ["", "## Highest Priority Gaps", ""]
    gaps: list[tuple[str, str, str]] = []
    for row in main:
        missing = [field for field in ["not_for", "output_shape", "preconditions"] if not row.get(field)]
        if missing:
            gaps.append((row["family"], row["skill"], ", ".join(missing)))

    if not gaps:
        lines.append("- No high-priority gaps found.")
        return lines

    lines.append("| Family | Skill | Missing fields |")
    lines.append("|---|---|---|")
    for family, skill, missing in sorted(gaps)[:80]:
        lines.append(f"| {family} | `{skill}` | {missing} |")
    return lines


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Analyze coverage of exported skill representation fields.")
    parser.add_argument(
        "--representations",
        type=Path,
        default=repo_root / "representations",
        help="Representation output directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "outputs" / "representation_coverage.md",
        help="Markdown report path.",
    )
    args = parser.parse_args()

    structured = load_jsonl(args.representations / "R2_structured_procedural.jsonl")
    dependency = load_jsonl(args.representations / "R3_dependency_resource_aware.jsonl")
    edges = load_jsonl(args.representations / "R4_graph_edges.jsonl")

    lines = [
        "# Representation Coverage Report",
        "",
        "This report checks whether exported representation fields are populated enough to support the benchmark methodology rubric.",
        "",
        f"- Skills in structured export: {len(structured)}",
        f"- Main evaluated skills: {sum(1 for row in structured if row.get('is_main_evaluated'))}",
        f"- Background/public/support skills: {sum(1 for row in structured if not row.get('is_main_evaluated'))}",
        "",
    ]
    lines.extend(summarize_field_coverage(structured))
    lines.extend(summarize_by_family(structured))
    lines.extend(summarize_dependency(dependency))
    lines.extend(summarize_graph(edges))
    lines.extend(summarize_failures(structured))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
