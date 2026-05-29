#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


FIELD_DEFINITIONS: dict[str, dict[str, list[str]]] = {
    "routing_trigger": {
        "frontmatter": ["description", "trigger", "triggers", "category", "tags", "capabilities"],
        "headings": ["when to use", "use when", "trigger", "trigger conditions", "overview", "purpose"],
        "keywords": ["use when", "trigger when", "trigger conditions", "when user", "when the user", "capabilities"],
    },
    "input_precondition": {
        "frontmatter": ["input", "inputs", "preconditions", "requires", "requirements"],
        "headings": ["inputs", "input", "preconditions", "requirements", "before you begin", "getting started", "quick start"],
        "keywords": ["requires", "required", "input", "provide", "share your", "if not already", "prerequisite", "you need", "user provides"],
    },
    "output_artifact": {
        "frontmatter": ["output", "outputs", "output_format", "deliverables"],
        "headings": ["output", "outputs", "output format", "output formatting", "deliverables", "expected", "result"],
        "keywords": ["output", "return", "returns", "report", "deliverable", "produce", "produces", "expected output", "final answer"],
    },
    "workflow_procedure": {
        "frontmatter": ["workflow", "steps", "instructions", "procedure"],
        "headings": ["workflow", "steps", "procedure", "how to use", "process", "stage", "core tasks", "instructions"],
        "keywords": ["step 1", "step 2", "workflow", "process", "stage", "run the", "execute", "after that"],
    },
    "constraints_boundaries": {
        "frontmatter": ["not_for", "limitations", "constraints", "scope"],
        "headings": ["not for", "limitations", "constraints", "scope", "do not", "avoid", "rules", "guardrails"],
        "keywords": ["do not", "don't", "never", "avoid", "must not", "out of scope", "limitation", "redact", "not use"],
    },
    "dependencies_tools": {
        "frontmatter": ["dependencies", "tools", "mcp", "env", "environment", "binaries", "allowed-tools"],
        "headings": ["tools", "dependencies", "mcp", "environment", "setup", "installation", "cli", "authentication"],
        "keywords": ["cli", "mcp", "install", "auth", "token", "environment variable", "env var", "command line", "api key", "api token", "api call", "api endpoint"],
    },
    "resources_references": {
        "frontmatter": ["resources", "references", "assets", "scripts", "related_skills"],
        "headings": ["resources", "references", "assets", "scripts", "related skills", "source"],
        "keywords": ["references/", "scripts/", "assets/", "see `", "related skills", "template", "artifact"],
    },
    "examples_tests": {
        "frontmatter": ["examples", "tests", "golden_tests", "evals"],
        "headings": ["examples", "example", "tests", "test", "golden test", "sample prompt"],
        "keywords": ["example prompt", "expected", "test input", "golden test", "```", "sample"],
    },
    "safety_side_effects": {
        "frontmatter": ["safety", "permissions", "side_effects", "risk"],
        "headings": ["safety", "permissions", "security", "side effects", "risk", "privacy"],
        "keywords": ["read-only", "redact", "pii", "permission", "approval required", "security", "risk", "auth token", "destructive", "side effect"],
    },
    "portability_environment": {
        "frontmatter": ["models", "languages", "platforms", "os", "compatibility", "version"],
        "headings": ["compatibility", "platform", "environment", "language support", "version"],
        "keywords": ["compatible", "version", "platform", "macos", "windows", "linux", "model", "language support"],
    },
    "hierarchy_links": {
        "frontmatter": ["related_skills", "links", "subskills", "children", "parent"],
        "headings": ["related skills", "subskills", "see also", "links", "handoff"],
        "keywords": ["related skill", "refer to", "see also", "delegate", "subagent", "sub-skill", "another skill"],
    },
}


FIELD_LABELS = {
    "explicit": "explicit",
    "extractable": "extractable",
    "missing": "missing",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.DOTALL)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def frontmatter_keys(frontmatter: str) -> set[str]:
    keys: set[str] = set()
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^\s*([A-Za-z0-9_-]+)\s*:", line)
        if match:
            keys.add(match.group(1).lower())
    return keys


def headings(body: str) -> list[str]:
    found: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if match:
            heading = re.sub(r"[*_`]", "", match.group(1)).strip().lower()
            found.append(heading)
    return found


def pattern_in_text(pattern: str, text: str) -> bool:
    if not pattern:
        return False
    pattern_lower = pattern.lower()
    text_lower = text.lower()
    if re.fullmatch(r"[a-z0-9_-]+", pattern_lower):
        return re.search(rf"(?<![a-z0-9_-]){re.escape(pattern_lower)}(?![a-z0-9_-])", text_lower) is not None
    return pattern_lower in text_lower


def sentence_snippets(text: str, needles: list[str], limit: int = 3) -> list[str]:
    if not needles:
        return []
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text)
    snippets: list[str] = []
    for chunk in chunks:
        compact = re.sub(r"\s+", " ", chunk).strip()
        if len(compact) < 8:
            continue
        lower = compact.lower()
        if any(pattern_in_text(needle, lower) for needle in needles):
            snippets.append(compact[:220])
        if len(snippets) >= limit:
            break
    return snippets


def token_count_rough(text: str) -> int:
    return len(re.findall(r"\S+", text))


def code_block_count(text: str) -> int:
    return len(re.findall(r"```", text)) // 2


def detect_file_inventory(skill_dir: Path) -> dict[str, Any]:
    source_dir = skill_dir / "source"
    files = [path for path in skill_dir.rglob("*") if path.is_file()]
    original_source_files = [path for path in source_dir.rglob("*") if path.is_file()] if source_dir.exists() else []
    suffixes = Counter(path.suffix.lower() or "[none]" for path in files)
    return {
        "file_count": len(files),
        "source_file_count": len(original_source_files),
        "has_original": (source_dir / "SKILL.original.md").exists(),
        "has_import_json": (source_dir / "IMPORT.json").exists(),
        "has_scripts_dir": any(part == "scripts" for path in files for part in path.parts),
        "has_references_dir": any(part in {"references", "reference"} for path in files for part in path.parts),
        "has_assets_dir": any(part == "assets" for path in files for part in path.parts),
        "suffixes": dict(sorted(suffixes.items())),
    }


def load_import_metadata(skill_dir: Path) -> dict[str, Any]:
    path = skill_dir / "source" / "IMPORT.json"
    if not path.exists():
        return {}
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return {"import_error": "invalid_json"}


def detect_field(field: str, front: str, body: str, fm_keys: set[str], body_headings: list[str]) -> dict[str, Any]:
    definition = FIELD_DEFINITIONS[field]
    front_lower = front.lower()
    body_lower = body.lower()
    heading_hits = [
        heading
        for heading in body_headings
        if any(pattern_in_text(pattern, heading) for pattern in definition["headings"])
    ]
    fm_hits = [
        key
        for key in definition["frontmatter"]
        if key.lower() in fm_keys or pattern_in_text(f"{key.lower()}:", front_lower)
    ]
    keyword_hits = [
        keyword
        for keyword in definition["keywords"]
        if pattern_in_text(keyword, body_lower) or pattern_in_text(keyword, front_lower)
    ]

    if fm_hits or heading_hits:
        label = FIELD_LABELS["explicit"]
    elif keyword_hits:
        label = FIELD_LABELS["extractable"]
    else:
        label = FIELD_LABELS["missing"]

    evidence_needles = [*definition["keywords"], *heading_hits, *fm_hits]
    return {
        "status": label,
        "frontmatter_hits": fm_hits[:8],
        "heading_hits": heading_hits[:8],
        "keyword_hits": keyword_hits[:8],
        "evidence": sentence_snippets(f"{front}\n{body}", evidence_needles),
    }


def classify_skill(skill_dir: Path) -> dict[str, Any]:
    original_path = skill_dir / "source" / "SKILL.original.md"
    wrapper_path = skill_dir / "SKILL.md"
    audit_path = original_path if original_path.exists() else wrapper_path
    text = read_text(audit_path)
    front, body = split_frontmatter(text)
    fm_keys = frontmatter_keys(front)
    body_headings = headings(body)
    import_meta = load_import_metadata(skill_dir)
    inventory = detect_file_inventory(skill_dir)

    fields = {
        field: detect_field(field, front, body, fm_keys, body_headings)
        for field in FIELD_DEFINITIONS
    }
    status_counts = Counter(field_data["status"] for field_data in fields.values())
    explicit_or_extractable = sum(
        1 for field_data in fields.values() if field_data["status"] != FIELD_LABELS["missing"]
    )

    return {
        "skill": skill_dir.name,
        "source_name": import_meta.get("source_name"),
        "origin": import_meta.get("origin"),
        "source_url": import_meta.get("source_url"),
        "raw_url": import_meta.get("raw_url"),
        "audit_file": str(audit_path),
        "used_original": original_path.exists(),
        "frontmatter_keys": sorted(fm_keys),
        "heading_count": len(body_headings),
        "headings": body_headings[:40],
        "body_word_count": token_count_rough(body),
        "frontmatter_word_count": token_count_rough(front),
        "code_block_count": code_block_count(text),
        "inventory": inventory,
        "field_status_counts": dict(status_counts),
        "explicit_or_extractable_fields": explicit_or_extractable,
        "fields": fields,
    }


def skill_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def load_completed(output_jsonl: Path) -> set[str]:
    if not output_jsonl.exists():
        return set()
    completed: set[str] = set()
    with output_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                completed.add(json.loads(line)["skill"])
            except (json.JSONDecodeError, KeyError):
                continue
    return completed


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    origins = Counter(row.get("origin") or "unknown" for row in rows)
    field_counts: dict[str, Counter[str]] = {field: Counter() for field in FIELD_DEFINITIONS}
    for row in rows:
        for field, data in row["fields"].items():
            field_counts[field][data["status"]] += 1
    field_summary = {}
    for field, counts in field_counts.items():
        field_summary[field] = {
            "explicit": counts["explicit"],
            "extractable": counts["extractable"],
            "missing": counts["missing"],
            "explicit_pct": round(counts["explicit"] / total, 4) if total else 0,
            "explicit_or_extractable_pct": round((counts["explicit"] + counts["extractable"]) / total, 4) if total else 0,
        }
    inventory_counts = {
        "has_scripts_dir": sum(1 for row in rows if row["inventory"]["has_scripts_dir"]),
        "has_references_dir": sum(1 for row in rows if row["inventory"]["has_references_dir"]),
        "has_assets_dir": sum(1 for row in rows if row["inventory"]["has_assets_dir"]),
        "has_original": sum(1 for row in rows if row["used_original"]),
    }
    word_counts = [row["body_word_count"] + row["frontmatter_word_count"] for row in rows]
    return {
        "total_skills": total,
        "origins": dict(origins.most_common()),
        "field_summary": field_summary,
        "inventory_counts": inventory_counts,
        "mean_words": round(sum(word_counts) / total, 2) if total else 0,
        "median_words": sorted(word_counts)[total // 2] if total else 0,
    }


def render_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    total = summary["total_skills"]
    lines = [
        "# Public Skill Field Audit",
        "",
        "This report audits imported public `SKILL.md` artifacts for representation-field evidence.",
        "",
        "Statuses:",
        "",
        "- `explicit`: field appears in frontmatter or a clear heading.",
        "- `extractable`: field is not clearly structured, but keywords/body evidence suggest it can be parsed or inferred.",
        "- `missing`: no strong evidence detected by this heuristic audit.",
        "",
        "Important limitation: this is a heuristic audit. It should be followed by a small manual sample review before final thesis claims.",
        "",
        "## Corpus",
        "",
        f"- Public skills audited: {total}",
        f"- Original public `SKILL.md` files used: {summary['inventory_counts']['has_original']}/{total}",
        f"- Mean words per skill: {summary['mean_words']}",
        f"- Median words per skill: {summary['median_words']}",
        f"- Skills with scripts directory: {summary['inventory_counts']['has_scripts_dir']}/{total}",
        f"- Skills with references directory: {summary['inventory_counts']['has_references_dir']}/{total}",
        f"- Skills with assets directory: {summary['inventory_counts']['has_assets_dir']}/{total}",
        "",
        "## Origins",
        "",
        "| Origin | Count |",
        "|---|---:|",
    ]
    for origin, count in summary["origins"].items():
        lines.append(f"| `{origin}` | {count} |")

    lines.extend(["", "## Field Prevalence", ""])
    lines.append("| Field | Explicit | Extractable | Missing | Explicit % | Explicit or Extractable % |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for field, counts in summary["field_summary"].items():
        lines.append(
            f"| `{field}` | {counts['explicit']} | {counts['extractable']} | {counts['missing']} | "
            f"{counts['explicit_pct']:.1%} | {counts['explicit_or_extractable_pct']:.1%} |"
        )

    lines.extend(["", "## Provisional Interpretation", ""])
    for field, counts in summary["field_summary"].items():
        explicit_or_extractable = counts["explicit_or_extractable_pct"]
        if explicit_or_extractable >= 0.75:
            label = "common or broadly extractable"
        elif explicit_or_extractable >= 0.4:
            label = "sometimes present/extractable"
        else:
            label = "rare under current heuristic"
        lines.append(f"- `{field}`: {label}.")

    lines.extend(["", "## Manual Review Sample Candidates", ""])
    lines.append("These examples are useful for checking whether the heuristic labels are reasonable.")
    lines.append("")
    lines.append("| Skill | Origin | Explicit/Extractable Fields | Missing Fields |")
    lines.append("|---|---|---:|---|")
    sample = sorted(rows, key=lambda row: (row["explicit_or_extractable_fields"], row["skill"]))
    sample = sample[:5] + sample[len(sample) // 2 : len(sample) // 2 + 5] + sample[-5:]
    seen = set()
    for row in sample:
        if row["skill"] in seen:
            continue
        seen.add(row["skill"])
        missing = [field for field, data in row["fields"].items() if data["status"] == "missing"]
        lines.append(
            f"| `{row['skill']}` | `{row.get('origin') or 'unknown'}` | "
            f"{row['explicit_or_extractable_fields']} | {', '.join(missing[:5])} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Resumable audit of public imported skill field evidence.")
    parser.add_argument("--skills-root", default=str(repo_root / "skills" / "public_imported_background"))
    parser.add_argument("--output-jsonl", default=str(repo_root / "outputs" / "public_skill_field_audit.jsonl"))
    parser.add_argument("--output-json", default=str(repo_root / "outputs" / "public_skill_field_audit_summary.json"))
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "public_skill_field_audit.md"))
    parser.add_argument("--limit", type=int, default=None, help="Process at most this many new skills.")
    parser.add_argument("--force", action="store_true", help="Delete existing JSONL and reprocess all selected skills.")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    output_jsonl = Path(args.output_jsonl)
    if args.force and output_jsonl.exists():
        output_jsonl.unlink()

    completed = load_completed(output_jsonl)
    dirs = skill_dirs(skills_root)
    processed = 0
    for skill_dir in dirs:
        if skill_dir.name in completed:
            continue
        row = classify_skill(skill_dir)
        append_jsonl(output_jsonl, row)
        processed += 1
        if args.limit is not None and processed >= args.limit:
            break

    rows = load_jsonl(output_jsonl)
    summary = summarize(rows)
    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.write_text(render_markdown(summary, rows), encoding="utf-8")

    print(f"Audited new skills: {processed}")
    print(f"Total audit rows: {len(rows)}")
    print(f"Wrote {output_jsonl}")
    print(f"Wrote {output_json}")
    print(f"Wrote {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
