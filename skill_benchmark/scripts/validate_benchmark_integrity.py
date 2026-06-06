#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SCALAR_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
MAIN_EVALUATED_FAMILIES = {
    "api_backend_design",
    "api_mcp_tooling",
    "browser_web_automation",
    "code_github_workflow",
    "data_spreadsheet",
    "deployment_browser_qa",
    "documents_files",
    "github_ci_maintenance",
    "huggingface_ml_workflows",
    "implicit_field_stress",
    "metrics_observability",
    "news_monitoring",
    "observability_reliability",
    "office_business_automation",
    "office_artifact_workflows",
    "pdf_document_operations",
    "planning_meetings",
    "public_style_controlled",
    "reading_research",
    "reply_messaging",
    "security_appsec",
    "skill_lifecycle",
    "skill_representation_analysis",
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith(" ") or not line.strip():
            continue
        scalar = SCALAR_RE.match(line)
        if scalar:
            key, value = scalar.groups()
            values[key] = value.strip().strip("\"'")
    return values


def load_prompts(path_glob: str) -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    for path_string in sorted(glob.glob(path_glob)):
        path = Path(path_string)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a JSON array")
        for row in data:
            row = dict(row)
            row["_source_file"] = str(path)
            prompts.append(row)
    return prompts


def skill_rows(skills_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(skills_root.glob("*/*/SKILL.md")):
        family = path.parts[-3]
        directory_name = path.parent.name
        frontmatter = parse_frontmatter(path)
        rows.append(
            {
                "family": family,
                "directory_name": directory_name,
                "path": str(path),
                "name": frontmatter.get("name", ""),
                "description": frontmatter.get("description", ""),
                "is_main_evaluated": family in MAIN_EVALUATED_FAMILIES,
                "is_public_imported_background": family == "public_imported_background",
            }
        )
    return rows


def evaluate(prompts: list[dict[str, Any]], skills: list[dict[str, Any]], repo_root: Path) -> dict[str, Any]:
    skill_names = {row["name"] for row in skills if row["name"]}
    prompt_ids = [row.get("id") for row in prompts]
    duplicate_prompt_ids = sorted(skill for skill, count in Counter(prompt_ids).items() if count > 1)

    malformed_skills = [
        row
        for row in skills
        if not row["name"] or not row["description"] or row["name"] != row["directory_name"]
    ]
    duplicate_skill_names = sorted(skill for skill, count in Counter(row["name"] for row in skills).items() if skill and count > 1)

    missing_references: list[dict[str, str]] = []
    for prompt in prompts:
        prompt_id = prompt.get("id", "")
        for field in ["gold_skill", "closest_alternatives"]:
            values = prompt.get(field, [])
            if isinstance(values, str):
                values = [values]
            for value in values:
                if value not in skill_names:
                    missing_references.append({"prompt_id": prompt_id, "field": field, "skill": value})

    family_counts = Counter(row["family"] for row in skills)
    prompt_family_counts = Counter(row.get("family", "") for row in prompts)
    public_import_status: dict[str, int] = defaultdict(int)
    public_manifest = repo_root / "skills" / "public_imported_background" / "IMPORT_MANIFEST.json"
    if public_manifest.exists():
        with public_manifest.open("r", encoding="utf-8") as f:
            for row in json.load(f):
                public_import_status[row.get("import_status", "unknown")] += 1

    pass_integrity = (
        not duplicate_prompt_ids
        and not missing_references
        and not duplicate_skill_names
        and not malformed_skills
    )

    return {
        "pass_integrity": pass_integrity,
        "prompt_count": len(prompts),
        "prompt_files": len({row["_source_file"] for row in prompts}),
        "skill_count": len(skills),
        "main_evaluated_skill_count": sum(1 for row in skills if row["is_main_evaluated"]),
        "background_skill_count": sum(1 for row in skills if not row["is_main_evaluated"]),
        "family_counts": dict(sorted(family_counts.items())),
        "prompt_family_counts": dict(sorted(prompt_family_counts.items())),
        "duplicate_prompt_ids": duplicate_prompt_ids,
        "duplicate_skill_names": duplicate_skill_names,
        "missing_references": missing_references,
        "malformed_skills": malformed_skills,
        "public_import_status": dict(sorted(public_import_status.items())),
    }


def render_markdown(report: dict[str, Any]) -> str:
    status = "PASS" if report["pass_integrity"] else "FAIL"
    lines = [
        "# Benchmark Integrity Report",
        "",
        "This report implements Step 1 of the benchmark rubric: prompt references, skill frontmatter, and library partitioning must be valid before retrieval results are meaningful.",
        "",
        "## Overall Status",
        "",
        f"- Step 1 integrity status: **{status}**",
        f"- Prompt files: {report['prompt_files']}",
        f"- Prompts: {report['prompt_count']}",
        f"- Skills: {report['skill_count']}",
        f"- Main evaluated skills: {report['main_evaluated_skill_count']}",
        f"- Background/public/support skills: {report['background_skill_count']}",
        f"- Duplicate prompt IDs: {len(report['duplicate_prompt_ids'])}",
        f"- Duplicate skill names: {len(report['duplicate_skill_names'])}",
        f"- Missing prompt references: {len(report['missing_references'])}",
        f"- Malformed skill frontmatter entries: {len(report['malformed_skills'])}",
        "",
        "## Skill Families",
        "",
        "| Family | Skills |",
        "|---|---:|",
    ]
    for family, count in report["family_counts"].items():
        lines.append(f"| `{family}` | {count} |")

    lines.extend(["", "## Prompt Families", "", "| Family | Prompts |", "|---|---:|"])
    for family, count in report["prompt_family_counts"].items():
        lines.append(f"| `{family}` | {count} |")

    lines.extend(["", "## Public Imports", ""])
    if report["public_import_status"]:
        lines.append("| Import status | Count |")
        lines.append("|---|---:|")
        for status_label, count in report["public_import_status"].items():
            lines.append(f"| `{status_label}` | {count} |")
    else:
        lines.append("- No public import manifest found.")

    if report["missing_references"]:
        lines.extend(["", "## Missing References", "", "| Prompt | Field | Skill |", "|---|---|---|"])
        for row in report["missing_references"]:
            lines.append(f"| `{row['prompt_id']}` | `{row['field']}` | `{row['skill']}` |")

    if report["malformed_skills"]:
        lines.extend(["", "## Malformed Skills", "", "| Family | Directory | Name | Problem |", "|---|---|---|---|"])
        for row in report["malformed_skills"][:200]:
            problems = []
            if not row["name"]:
                problems.append("missing name")
            if not row["description"]:
                problems.append("missing description")
            if row["name"] and row["name"] != row["directory_name"]:
                problems.append("name/directory mismatch")
            lines.append(
                f"| `{row['family']}` | `{row['directory_name']}` | `{row['name']}` | {', '.join(problems)} |"
            )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    parser = argparse.ArgumentParser(description="Validate benchmark skill and prompt integrity.")
    parser.add_argument("--skills-root", default=str(repo_root / "skills"))
    parser.add_argument("--prompts", default=str(repo_root / "prompts" / "*.json"))
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "benchmark_integrity_report.md"))
    parser.add_argument("--output-json", default=str(repo_root / "outputs" / "benchmark_integrity_report.json"))
    args = parser.parse_args()

    prompts = load_prompts(args.prompts)
    skills = skill_rows(Path(args.skills_root))
    report = evaluate(prompts, skills, repo_root)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"Step 1 integrity: {'PASS' if report['pass_integrity'] else 'FAIL'}")
    print(f"Prompts: {report['prompt_count']}; skills: {report['skill_count']}")


if __name__ == "__main__":
    main()
