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


def sentence_chunks(text: str) -> list[str]:
    text = re.sub(r"^\s*#+\s+.*$", " ", text, flags=re.MULTILINE)
    chunks = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text).strip())
    return [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]


def inferred_fields_from_body(description: str, body: str) -> dict[str, list[str]]:
    """Extract a light structured view when a skill is prose-only.

    This is intentionally conservative: it does not try to rewrite the skill,
    only lifts sentences that already signal routing, output, workflow, or
    boundaries. It models the representation layer as an extractor rather than
    assuming authors supplied clean headings.
    """
    source = "\n".join([description, body])
    sentences = sentence_chunks(source)
    inferred: dict[str, list[str]] = {
        "use_when": [],
        "not_for": [],
        "preconditions": [],
        "workflow": [],
        "output_shape": [],
        "writing_rules": [],
    }

    cue_sets = {
        "use_when": [
            "use this",
            "this routine is for",
            "this routine translates",
            "this routine works",
            "works with",
            "when ",
            "for the moment",
            "assumes there is",
            "starts from hardware",
        ],
        "not_for": [
            "wrong routine",
            "poor fit",
            "not the fit",
            "not for",
            "not a ",
            "belongs elsewhere",
            "choose a different routine",
        ],
        "preconditions": [
            "needs ",
            "requires ",
            "assumes ",
            "there is ",
            "starts from",
            "already has",
        ],
        "workflow": [
            "starts",
            "begins",
            "looks for",
            "checks",
            "collecting",
            "reads",
            "compares",
            "follows",
            "then ",
            "identifies",
            "connects",
        ],
        "output_shape": [
            "output is",
            "deliverable is",
            "result is",
            "artifact is",
            "answer should",
            "response contains",
        ],
        "writing_rules": [
            "should quote",
            "should keep",
            "should not",
            "must ",
            "must not",
        ],
    }

    lowered_pairs = [(sentence, sentence.lower()) for sentence in sentences]
    for field, cues in cue_sets.items():
        for sentence, lowered in lowered_pairs:
            if any(cue in lowered for cue in cues) and sentence not in inferred[field]:
                inferred[field].append(sentence)

    return inferred


def lines_from_section(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        cleaned = LIST_MARKER_RE.sub("", stripped).strip()
        if cleaned and cleaned not in {"```", "---", "***", "___"}:
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


def lines_from_first_sections(sections: dict[str, str], names: list[str], limit: int = 16) -> list[str]:
    lines: list[str] = []
    for name in names:
        lines.extend(lines_from_section(sections.get(name, "")))
    return lines[:limit]


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
    source_body = ""
    source_description = ""
    source_frontmatter: dict[str, object] = {}
    source_sections: dict[str, str] = {}
    source_path = skill_dir / "source" / "SKILL.original.md"
    if family == "public_imported_background" and source_path.exists():
        source_text = source_path.read_text(encoding="utf-8")
        source_frontmatter, source_body = parse_frontmatter(source_text)
        source_description = clean_description(str(source_frontmatter.get("description") or ""))
        source_sections = parse_sections(source_body)
    description = source_description or clean_description(str(frontmatter.get("description") or ""))

    return {
        "name": name,
        "family": family,
        "path": str(path),
        "skill_dir": str(skill_dir),
        "description": description,
        "metadata": metadata,
        "body": body,
        "sections": sections,
        "source_frontmatter": source_frontmatter,
        "source_body": source_body,
        "source_sections": source_sections,
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
    source_sections = record.get("source_sections")
    if isinstance(source_sections, dict) and source_sections:
        sections = source_sections
    body_for_inference = str(record.get("source_body") or record.get("body") or "")
    inferred = inferred_fields_from_body(str(record["description"]), body_for_inference)
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
    if not use_when:
        use_when = remove_benchmark_artifacts(
            lines_from_first_sections(
                sections,
                [
                    "when_to_use",
                    "when_to_use_this_skill",
                    "overview",
                    "core_capabilities",
                    "capabilities",
                    "skill_capabilities",
                ],
                limit=10,
            )
        )
    if not use_when:
        use_when = remove_benchmark_artifacts(inferred["use_when"])
    if not not_for:
        not_for = remove_benchmark_artifacts(
            lines_from_first_sections(
                sections,
                [
                    "not_for",
                    "when_not_to_use",
                    "when_not_to_use_this_skill",
                    "do_not_use_when",
                    "do_not_use_this_skill_when",
                    "wrong",
                    "anti_patterns",
                ],
                limit=10,
            )
        )
    if not not_for:
        not_for = remove_benchmark_artifacts(inferred["not_for"])
    if not workflow:
        workflow = remove_benchmark_artifacts(
            lines_from_first_sections(
                sections,
                [
                    "workflow",
                    "workflows",
                    "how_to_use",
                    "how_to_use_me",
                    "instructions",
                    "core_workflows",
                    "process",
                    "the_process",
                    "build_workflow",
                    "usage",
                ],
                limit=18,
            )
        )
    if not workflow:
        workflow = remove_benchmark_artifacts(inferred["workflow"])
    if not preconditions:
        preconditions = remove_benchmark_artifacts(
            lines_from_first_sections(
                sections,
                [
                    "prerequisites",
                    "preconditions",
                    "requirements",
                    "input_requirements",
                    "required_intake_packet",
                    "before_you_start",
                    "default_operating_assumptions",
                ],
                limit=12,
            )
        )
    if not preconditions:
        preconditions = remove_benchmark_artifacts(inferred["preconditions"])
    if not output_shape:
        output_shape = remove_benchmark_artifacts(
            lines_from_first_sections(
                sections,
                [
                    "output",
                    "output_format",
                    "output_formats",
                    "outputs",
                    "deliverables",
                    "complete_guide_template",
                    "presentation_structure",
                    "content_generation_pattern",
                ],
                limit=14,
            )
        )
    if not output_shape:
        output_shape = remove_benchmark_artifacts(inferred["output_shape"])
    if not writing_rules:
        writing_rules = remove_benchmark_artifacts(inferred["writing_rules"])

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
    source_sections = record.get("source_sections")
    if isinstance(source_sections, dict) and source_sections:
        sections = source_sections
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
