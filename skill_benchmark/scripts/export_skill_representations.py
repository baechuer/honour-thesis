#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)")
PUBLIC_BACKGROUND_PREFIX_RE = re.compile(r"^\s*Public-source background skill based on `[^`]+`\.\s*")
PUBLIC_BACKGROUND_SUFFIX_RE = re.compile(r"\s*Use as an uncontrolled scale distractor with explicit dependency and resource signals\.\s*$")

BENCHMARK_ARTIFACT_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bbenchmark\b",
        r"\bgold[- ]label\b",
        r"\bcontrolled core\b",
        r"\bconfusable evaluation\b",
        r"\bscale distractor\b",
        r"\bcleanly annotated gold labels\b",
        r"\bsecond routing problem\b",
        r"\bbroad internal routing\b",
    ]
]


MAIN_EVALUATED_FAMILIES = {
    "api_backend_design",
    "browser_web_automation",
    "code_github_workflow",
    "data_spreadsheet",
    "deployment_browser_qa",
    "documents_files",
    "metrics_observability",
    "news_monitoring",
    "office_artifact_workflows",
    "planning_meetings",
    "reading_research",
    "reply_messaging",
    "security_appsec",
    "skill_lifecycle",
}


def parse_scalar(raw: str) -> object:
    value = raw.strip()
    if not value:
        return ""
    if value[0] in {"'", '"'}:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip("'\"")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    frontmatter_text = match.group(1)
    body = text[match.end() :]
    data: dict[str, object] = {}
    current_map: dict[str, object] | None = None

    for line in frontmatter_text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_map is not None:
            key, _, value = line.strip().partition(":")
            if key:
                current_map[key] = parse_scalar(value)
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        if value.strip():
            data[key] = parse_scalar(value)
            current_map = None
        else:
            nested: dict[str, object] = {}
            data[key] = nested
            current_map = nested

    return data, body


def normalize_section_name(name: str) -> str:
    lowered = name.strip().lower()
    lowered = lowered.replace("&", "and")
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    return lowered


def parse_sections(body: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        key = normalize_section_name(match.group(1))
        sections[key] = body[start:end].strip()
    return sections


def lines_from_section(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        cleaned = LIST_MARKER_RE.sub("", stripped).strip()
        if cleaned and cleaned != "```":
            lines.append(cleaned)
    return lines


def remove_benchmark_artifacts(lines: list[str]) -> list[str]:
    return [
        line
        for line in lines
        if not any(pattern.search(line) for pattern in BENCHMARK_ARTIFACT_PATTERNS)
    ]


def clean_description(description: str) -> str:
    cleaned = PUBLIC_BACKGROUND_PREFIX_RE.sub("", description).strip()
    cleaned = PUBLIC_BACKGROUND_SUFFIX_RE.sub("", cleaned).strip()
    return cleaned


def compact_text(parts: list[str]) -> str:
    return "\n".join(part for part in parts if part).strip()


def find_skill_files(skills_root: Path, include_families: set[str] | None) -> list[Path]:
    files = sorted(skills_root.glob("*/*/SKILL.md"))
    if include_families is None:
        return files
    return [path for path in files if path.parts[-3] in include_families]


def resource_files(skill_dir: Path) -> list[str]:
    resources: list[str] = []
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir() or path.name == "SKILL.md":
            continue
        resources.append(str(path.relative_to(skill_dir)))
    return resources


def skill_record(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    sections = parse_sections(body)
    family = path.parts[-3]
    skill_dir = path.parent
    name = str(frontmatter.get("name") or skill_dir.name)
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}

    return {
        "name": name,
        "family": family,
        "path": str(path),
        "skill_dir": str(skill_dir),
        "description": clean_description(str(frontmatter.get("description") or "")),
        "metadata": metadata,
        "sections": sections,
        "resources": resource_files(skill_dir),
        "is_main_evaluated": family in MAIN_EVALUATED_FAMILIES,
        "is_background": family in {"background_scale", "public_imported_background", "email_communication"},
    }


def flat_metadata(record: dict[str, object]) -> dict[str, object]:
    return {
        "representation": "R1_flat_metadata",
        "skill": record["name"],
        "family": record["family"],
        "is_main_evaluated": record["is_main_evaluated"],
        "name": record["name"],
        "description": record["description"],
        "text": compact_text(
            [
                f"name: {record['name']}",
                f"family: {record['family']}",
                f"description: {record['description']}",
            ]
        ),
    }


def structured_procedural(record: dict[str, object]) -> dict[str, object]:
    sections: dict[str, str] = record["sections"]  # type: ignore[assignment]
    use_when = remove_benchmark_artifacts(lines_from_section(sections.get("use_when", "")))
    not_for = remove_benchmark_artifacts(lines_from_section(sections.get("not_for", "")))
    workflow = remove_benchmark_artifacts(lines_from_section(sections.get("workflow", "")))
    preconditions = remove_benchmark_artifacts(lines_from_section(sections.get("preconditions", "")))
    writing_rules = remove_benchmark_artifacts(lines_from_section(sections.get("writing_rules", "")))
    output_shape = remove_benchmark_artifacts(
        lines_from_section(
            "\n".join(
                [
                    sections.get("expected_output", ""),
                    sections.get("output_pattern", ""),
                    sections.get("default_shape", ""),
                ]
            )
        )
    )

    text = compact_text(
        [
            f"name: {record['name']}",
            f"family: {record['family']}",
            f"description: {record['description']}",
            "use_when:\n" + "\n".join(f"- {item}" for item in use_when) if use_when else "",
            "not_for:\n" + "\n".join(f"- {item}" for item in not_for) if not_for else "",
            "preconditions:\n" + "\n".join(f"- {item}" for item in preconditions) if preconditions else "",
            "workflow:\n" + "\n".join(f"- {item}" for item in workflow) if workflow else "",
            "output:\n" + "\n".join(f"- {item}" for item in output_shape) if output_shape else "",
            "writing_rules:\n" + "\n".join(f"- {item}" for item in writing_rules) if writing_rules else "",
        ]
    )

    return {
        "representation": "R2_structured_procedural",
        "skill": record["name"],
        "family": record["family"],
        "is_main_evaluated": record["is_main_evaluated"],
        "name": record["name"],
        "description": record["description"],
        "use_when": use_when,
        "not_for": not_for,
        "preconditions": preconditions,
        "workflow": workflow,
        "output_shape": output_shape,
        "writing_rules": writing_rules,
        "text": text,
    }


def dependency_aware(record: dict[str, object]) -> dict[str, object]:
    base = structured_procedural(record)
    sections: dict[str, str] = record["sections"]  # type: ignore[assignment]
    metadata: dict[str, object] = record["metadata"]  # type: ignore[assignment]
    dependencies = lines_from_section(sections.get("external_dependencies_to_preserve", ""))
    resource_signals = lines_from_section(sections.get("resource_and_structure_signals", ""))
    dependency_profile = str(metadata.get("dependency_profile") or sections.get("dependency_profile", "")).strip()
    public_source = {
        "public_source_name": metadata.get("public_source_name"),
        "public_origin": metadata.get("public_origin"),
        "source_url": metadata.get("source_url"),
        "raw_url": metadata.get("raw_url"),
        "import_status": metadata.get("import_status"),
    }

    text = compact_text(
        [
            str(base["text"]),
            f"dependency_profile: {dependency_profile}" if dependency_profile else "",
            "external_dependencies:\n" + "\n".join(f"- {item}" for item in dependencies) if dependencies else "",
            "resource_signals:\n" + "\n".join(f"- {item}" for item in resource_signals) if resource_signals else "",
            "resource_files:\n" + "\n".join(f"- {item}" for item in record["resources"]) if record["resources"] else "",
        ]
    )

    return {
        **base,
        "representation": "R3_dependency_resource_aware",
        "dependency_profile": dependency_profile,
        "external_dependencies": dependencies,
        "resource_signals": resource_signals,
        "resource_files": record["resources"],
        "public_source": public_source,
        "text": text,
    }


def node_id(kind: str, value: object) -> str:
    value_text = str(value).strip().lower()
    value_text = re.sub(r"[^a-z0-9._/-]+", "-", value_text).strip("-")
    return f"{kind}:{value_text[:120]}"


def graph_edges(record: dict[str, object]) -> list[dict[str, object]]:
    structured = dependency_aware(record)
    skill_node = node_id("skill", record["name"])
    rows: list[dict[str, object]] = [
        {
            "representation": "R4_graph_edges",
            "source": skill_node,
            "edge": "belongs_to_family",
            "target": node_id("family", record["family"]),
            "skill": record["name"],
            "family": record["family"],
            "target_text": record["family"],
        }
    ]

    edge_specs = [
        ("triggered_by", "use_when", "trigger"),
        ("avoid_when", "not_for", "avoid_condition"),
        ("has_precondition", "preconditions", "precondition"),
        ("has_workflow_step", "workflow", "workflow_step"),
        ("produces_output", "output_shape", "output"),
        ("follows_writing_rule", "writing_rules", "writing_rule"),
        ("requires_dependency", "external_dependencies", "dependency"),
        ("has_resource_signal", "resource_signals", "resource_signal"),
    ]

    for edge, field, target_kind in edge_specs:
        values = structured.get(field, [])
        if not isinstance(values, list):
            continue
        for value in values:
            rows.append(
                {
                    "representation": "R4_graph_edges",
                    "source": skill_node,
                    "edge": edge,
                    "target": node_id(target_kind, value),
                    "skill": record["name"],
                    "family": record["family"],
                    "target_text": value,
                }
            )

    for resource in record["resources"]:  # type: ignore[union-attr]
        rows.append(
            {
                "representation": "R4_graph_edges",
                "source": skill_node,
                "edge": "uses_resource",
                "target": node_id("resource", resource),
                "skill": record["name"],
                "family": record["family"],
                "target_text": resource,
            }
        )

    public_source = structured.get("public_source", {})
    if isinstance(public_source, dict) and public_source.get("public_source_name"):
        rows.append(
            {
                "representation": "R4_graph_edges",
                "source": skill_node,
                "edge": "derived_from_public_skill",
                "target": node_id("public_skill", public_source["public_source_name"]),
                "skill": record["name"],
                "family": record["family"],
                "target_text": public_source["public_source_name"],
            }
        )

    return rows


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    parser = argparse.ArgumentParser(description="Export skill representation layers for selector experiments.")
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "representations",
        help="Directory to write JSONL representation files.",
    )
    parser.add_argument(
        "--family",
        action="append",
        dest="families",
        help="Only export the given family. Can be used multiple times.",
    )
    args = parser.parse_args()

    include_families = set(args.families) if args.families else None
    skill_files = find_skill_files(repo_root / "skills", include_families)
    records = [skill_record(path) for path in skill_files]

    flat_rows = [flat_metadata(record) for record in records]
    structured_rows = [structured_procedural(record) for record in records]
    dependency_rows = [dependency_aware(record) for record in records]
    edge_rows = [edge for record in records for edge in graph_edges(record)]

    write_jsonl(args.output / "R1_flat_metadata.jsonl", flat_rows)
    write_jsonl(args.output / "R2_structured_procedural.jsonl", structured_rows)
    write_jsonl(args.output / "R3_dependency_resource_aware.jsonl", dependency_rows)
    write_jsonl(args.output / "R4_graph_edges.jsonl", edge_rows)

    family_counts = Counter(record["family"] for record in records)
    manifest = {
        "skill_count": len(records),
        "families": dict(sorted(family_counts.items())),
        "main_evaluated_count": sum(1 for record in records if record["is_main_evaluated"]),
        "background_count": sum(1 for record in records if record["is_background"]),
        "representations": {
            "R1_flat_metadata": len(flat_rows),
            "R2_structured_procedural": len(structured_rows),
            "R3_dependency_resource_aware": len(dependency_rows),
            "R4_graph_edges": len(edge_rows),
        },
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Exported {len(records)} skills into {args.output}")
    for key, count in manifest["representations"].items():
        print(f"- {key}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
