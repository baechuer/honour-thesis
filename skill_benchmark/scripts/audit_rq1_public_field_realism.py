#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PUBLIC_ROOT = ROOT / "skill_benchmark" / "skills" / "public_imported_background"
OUTPUT_JSON = ROOT / "skill_benchmark" / "outputs" / "rq1_public_field_realism_audit.json"
OUTPUT_JSONL = ROOT / "skill_benchmark" / "outputs" / "rq1_public_field_realism_audit_rows.jsonl"
OUTPUT_MD = ROOT / "skill_benchmark" / "outputs" / "rq1_public_field_realism_audit.md"


@dataclass(frozen=True)
class FieldSpec:
    label: str
    frontmatter: tuple[str, ...]
    headings: tuple[str, ...]
    keywords: tuple[str, ...]
    concrete: tuple[str, ...] = ()
    noisy: tuple[str, ...] = ()


FIELDS: dict[str, FieldSpec] = {
    "use_condition": FieldSpec(
        label="Use condition",
        frontmatter=("description", "trigger", "triggers", "category", "tags", "capabilities"),
        headings=("when to use", "use when", "trigger", "purpose", "overview", "capabilities"),
        keywords=("use when", "use this skill", "should be used", "when the user", "when user", "trigger", "capabilities"),
    ),
    "input_precondition": FieldSpec(
        label="Input / precondition",
        frontmatter=("input", "inputs", "precondition", "preconditions", "requires", "requirements"),
        headings=("input", "inputs", "preconditions", "requirements", "before you begin", "prerequisites", "getting started"),
        keywords=("input", "requires", "required", "provide", "upload", "file", "document", "repository", "dataset", "prerequisite", "before you"),
    ),
    "output_artifact": FieldSpec(
        label="Output artifact",
        frontmatter=("output", "outputs", "output_format", "deliverable", "deliverables"),
        headings=("output", "outputs", "output format", "deliverables", "result", "response format", "final answer"),
        keywords=("output", "return", "returns", "produce", "produces", "deliverable", "report", "table", "json", "csv", "summary", "final answer"),
    ),
    "workflow_procedure": FieldSpec(
        label="Workflow / procedure",
        frontmatter=("workflow", "steps", "procedure", "instructions"),
        headings=("workflow", "steps", "procedure", "process", "how to use", "instructions", "core tasks", "stage"),
        keywords=("step 1", "step 2", "first", "then", "finally", "workflow", "process", "run the", "execute", "after that"),
    ),
    "boundary_not_for": FieldSpec(
        label="Boundary / not-for",
        frontmatter=("not_for", "limitations", "constraints", "scope", "guardrails", "rules"),
        headings=("not for", "limitations", "constraints", "scope", "do not", "avoid", "guardrails", "rules", "out of scope"),
        keywords=("do not", "don't", "never", "avoid", "must not", "out of scope", "not for", "not use", "limitation", "redact"),
        concrete=("not for", "do not use", "must not", "out of scope", "never", "avoid"),
        noisy=("best practice", "style", "prefer", "should avoid"),
    ),
    "dependency_resource": FieldSpec(
        label="Dependency / resource",
        frontmatter=("dependencies", "tools", "mcp", "env", "environment", "resources", "references", "allowed-tools", "models"),
        headings=("dependencies", "tools", "mcp", "environment", "setup", "installation", "authentication", "resources", "references", "requirements"),
        keywords=("mcp", "api key", "token", "credential", "env var", "environment variable", "cli", "install", "pip install", "npm install", "package.json", "requirements.txt", "docker", "node", "python", "react", "github", "browser", "resource", "reference"),
        concrete=("mcp", "api key", "token", "credential", "env var", "environment variable", "package.json", "requirements.txt", "docker", "node", "python", "react", "postgres", "mysql", "github", "browser", "version"),
        noisy=("install", "pip install", "npm install", "npm ci", "yarn install", "pnpm install", "build", "lint", "test", "setup"),
    ),
    "success_verification": FieldSpec(
        label="Success / verification",
        frontmatter=("success", "verification", "validation", "tests", "acceptance", "criteria"),
        headings=("success", "verification", "validation", "tests", "test", "acceptance", "criteria", "quality", "expected"),
        keywords=("verify", "validate", "validation", "test", "tests", "ensure", "check", "expected", "criteria", "pass", "fail", "assert", "coverage", "schema", "smoke"),
        concrete=("schema", "threshold", "coverage", "assert", "pass/fail", "expected", "exact", "evidence", "source", "smoke", "test", "validate", "json", "%"),
        noisy=("best practice", "high quality", "accurate", "polished", "ensure", "correct"),
    ),
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
        match = re.match(r"^\s*([A-Za-z0-9_-]+)\s*:", line)
        if match:
            keys.add(match.group(1).lower())
    return keys


def headings(body: str) -> list[str]:
    out: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if match:
            heading = re.sub(r"[*_`]", "", match.group(1)).strip().lower()
            out.append(heading)
    return out


def has_phrase(text: str, phrase: str) -> bool:
    low_text = text.lower()
    low_phrase = phrase.lower()
    if re.fullmatch(r"[a-z0-9_-]+", low_phrase):
        return re.search(rf"(?<![a-z0-9_-]){re.escape(low_phrase)}(?![a-z0-9_-])", low_text) is not None
    return low_phrase in low_text


def find_hits(text: str, phrases: tuple[str, ...], limit: int = 12) -> list[str]:
    return [phrase for phrase in phrases if has_phrase(text, phrase)][:limit]


def snippet(text: str, needles: list[str], limit: int = 3) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text)
    out: list[str] = []
    for chunk in chunks:
        compact = re.sub(r"\s+", " ", chunk).strip()
        if len(compact) < 12:
            continue
        if any(has_phrase(compact, needle) for needle in needles):
            out.append(compact[:240])
        if len(out) >= limit:
            break
    return out


def load_import_metadata(skill_dir: Path) -> dict[str, Any]:
    path = skill_dir / "source" / "IMPORT.json"
    if not path.exists():
        return {}
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def dependency_kind(combined_text: str, keyword_hits: list[str]) -> str:
    hard_patterns = (
        r"\bmcp\b",
        r"\bapi[- ]?key\b",
        r"\btoken\b",
        r"\bcredential",
        r"\boauth\b",
        r"\benv(?:ironment)? var",
        r"\bnode(?:\.js)?\b",
        r"\bpython\b",
        r"\breact\s*\d",
        r"\bvue\s*\d",
        r"\bangular\b",
        r"\bdjango\b",
        r"\bflask\b",
        r"\bfastapi\b",
        r"\bpostgres(?:ql)?\b",
        r"\bmysql\b",
        r"\bsqlite\b",
        r"\bredis\b",
        r"\bfirebase\b",
        r"\bsupabase\b",
        r"\bdocker\b",
        r"\bkubernetes\b",
        r"\bgithub\b",
        r"\bgitlab\b",
        r"\bplaywright\b",
        r"\bchrome\b",
        r"\bhugging\s*face\b",
        r"\bopenai\b",
        r"\banthropic\b",
        r"\b\d+(?:\.\d+){1,3}\b",
    )
    setup_patterns = (
        r"\bpip install\b",
        r"\bnpm install\b",
        r"\bnpm ci\b",
        r"\byarn install\b",
        r"\bpnpm install\b",
        r"\bbrew install\b",
        r"\binstall command\b",
        r"\bsetup command\b",
        r"\brequirements\.txt\b",
    )
    has_hard = any(re.search(pattern, combined_text, flags=re.IGNORECASE) for pattern in hard_patterns)
    has_setup = any(re.search(pattern, combined_text, flags=re.IGNORECASE) for pattern in setup_patterns)
    if has_hard and has_setup:
        return "mixed_hard_and_setup"
    if has_hard:
        return "hard_capability"
    if has_setup or any(hit in {"install", "pip install", "npm install"} for hit in keyword_hits):
        return "setup_or_execution_only"
    return "none_detected"


def success_kind(combined_text: str, keyword_hits: list[str]) -> str:
    concrete_patterns = (
        r"\bschema\b",
        r"\bthreshold\b",
        r"\bcoverage\b",
        r"\bassert",
        r"\bexpected\b",
        r"\bexact\b",
        r"\bevidence\b",
        r"\bsource\b",
        r"\bsmoke\b",
        r"\bpass(?:/fail)?\b",
        r"\bfail\b",
        r"\bvalidate\b",
        r"\btest\b",
        r"\bjson\b",
        r"\b\d+(?:\.\d+)?\s*%",
        r"\bp\d{2}\b",
    )
    generic_patterns = (
        r"\bbest practices?\b",
        r"\bhigh quality\b",
        r"\baccurate\b",
        r"\bcorrect\b",
        r"\bpolished\b",
        r"\bensure\b",
        r"\bcheck\b",
    )
    has_concrete = any(re.search(pattern, combined_text, flags=re.IGNORECASE) for pattern in concrete_patterns)
    has_generic = any(re.search(pattern, combined_text, flags=re.IGNORECASE) for pattern in generic_patterns)
    if has_concrete and has_generic:
        return "mixed_concrete_and_generic"
    if has_concrete:
        return "concrete_acceptance_gate"
    if has_generic or keyword_hits:
        return "generic_quality_only"
    return "none_detected"


def boundary_kind(combined_text: str, keyword_hits: list[str]) -> str:
    scope_patterns = (
        r"\bnot for\b",
        r"\bdo not use\b",
        r"\bout of scope\b",
        r"\bmust not\b",
        r"\bnever\b",
        r"\bdon't\b",
        r"\bdo not\b",
    )
    if any(re.search(pattern, combined_text, flags=re.IGNORECASE) for pattern in scope_patterns):
        return "negative_scope_or_guardrail"
    if keyword_hits:
        return "soft_constraint_or_rule"
    return "none_detected"


def detect_field(field: str, front: str, body: str, fm_keys: set[str], body_headings: list[str]) -> dict[str, Any]:
    spec = FIELDS[field]
    front_low = front.lower()
    body_low = body.lower()
    text_low = f"{front_low}\n{body_low}"

    fm_hits = [key for key in spec.frontmatter if key in fm_keys or has_phrase(front_low, f"{key}:")]
    heading_hits = [
        heading
        for heading in body_headings
        if any(has_phrase(heading, pattern) for pattern in spec.headings)
    ][:12]
    keyword_hits = find_hits(text_low, spec.keywords)

    if fm_hits or heading_hits:
        status = "explicit"
    elif keyword_hits:
        status = "implicit"
    else:
        status = "missing"

    kind = ""
    noisy = False
    field_has_kind = field in {"dependency_resource", "success_verification", "boundary_not_for"}
    if status == "missing" and field_has_kind:
        kind = "none_detected"
    elif field == "dependency_resource":
        kind = dependency_kind(text_low, keyword_hits)
        noisy = kind in {"mixed_hard_and_setup", "setup_or_execution_only"}
    elif field == "success_verification":
        kind = success_kind(text_low, keyword_hits)
        noisy = kind in {"mixed_concrete_and_generic", "generic_quality_only"}
    elif field == "boundary_not_for":
        kind = boundary_kind(text_low, keyword_hits)
        noisy = kind == "soft_constraint_or_rule"

    evidence_needles = [*fm_hits, *heading_hits, *keyword_hits]
    return {
        "status": status,
        "kind": kind,
        "noisy": noisy,
        "frontmatter_hits": fm_hits,
        "heading_hits": heading_hits,
        "keyword_hits": keyword_hits,
        "evidence": snippet(f"{front}\n{body}", evidence_needles),
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

    fields = {
        field: detect_field(field, front, body, fm_keys, body_headings)
        for field in FIELDS
    }
    return {
        "skill": skill_dir.name,
        "source_name": import_meta.get("source_name"),
        "origin": import_meta.get("origin"),
        "source_url": import_meta.get("source_url"),
        "audit_file": str(audit_path.relative_to(ROOT)),
        "used_original": original_path.exists(),
        "frontmatter_keys": sorted(fm_keys),
        "heading_count": len(body_headings),
        "headings": body_headings[:40],
        "word_count": word_count(body),
        "fields": fields,
    }


def public_skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in PUBLIC_ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )


def status_table(rows: list[dict[str, Any]]) -> dict[str, Any]:
    table: dict[str, Any] = {}
    total = len(rows)
    for field, spec in FIELDS.items():
        statuses = Counter(row["fields"][field]["status"] for row in rows)
        noisy = sum(1 for row in rows if row["fields"][field]["noisy"])
        kinds = Counter(row["fields"][field]["kind"] for row in rows if row["fields"][field]["kind"])
        present = total - statuses["missing"]
        table[field] = {
            "label": spec.label,
            "explicit": statuses["explicit"],
            "implicit": statuses["implicit"],
            "missing": statuses["missing"],
            "present": present,
            "explicit_pct": statuses["explicit"] / total if total else 0.0,
            "present_pct": present / total if total else 0.0,
            "noisy": noisy,
            "noisy_pct": noisy / total if total else 0.0,
            "kinds": dict(kinds),
        }
    return table


def pick_examples(rows: list[dict[str, Any]]) -> dict[str, Any]:
    examples: dict[str, Any] = defaultdict(lambda: defaultdict(list))
    for field in FIELDS:
        for bucket in ("explicit", "implicit", "missing", "noisy"):
            for row in rows:
                field_data = row["fields"][field]
                if bucket == "noisy":
                    ok = field_data["noisy"]
                else:
                    ok = field_data["status"] == bucket
                if not ok:
                    continue
                examples[field][bucket].append(
                    {
                        "skill": row["skill"],
                        "origin": row.get("origin"),
                        "kind": field_data.get("kind"),
                        "evidence": field_data.get("evidence", [])[:2],
                    }
                )
                if len(examples[field][bucket]) >= 3:
                    break
    return {field: dict(buckets) for field, buckets in examples.items()}


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_md(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# RQ1 Public Skill Field Realism Audit")
    lines.append("")
    lines.append("Generated by `skill_benchmark/scripts/audit_rq1_public_field_realism.py`.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- Public imported skills audited: {summary['total_skills']}")
    lines.append(f"- Audited from original public `source/SKILL.original.md`: {summary['used_original']}/{summary['total_skills']}")
    lines.append(f"- Mean body word count: {summary['mean_word_count']:.1f}")
    lines.append(f"- Median body word count: {summary['median_word_count']:.1f}")
    lines.append("")
    lines.append("The audit is RQ1b support for the RQ1a field-isolation suites. It checks whether public skill artifacts expose the same seven field types explicitly, implicitly, or not at all. It does not score routing accuracy.")
    lines.append("")
    lines.append("## Field Prevalence")
    lines.append("")
    lines.append("| RQ1 field | Explicit | Implicit | Missing | Present | Noisy / mixed |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for field, item in summary["fields"].items():
        lines.append(
            "| {label} | {explicit} ({explicit_pct}) | {implicit} | {missing} | {present} ({present_pct}) | {noisy} ({noisy_pct}) |".format(
                label=item["label"],
                explicit=item["explicit"],
                explicit_pct=pct(item["explicit_pct"]),
                implicit=item["implicit"],
                missing=item["missing"],
                present=item["present"],
                present_pct=pct(item["present_pct"]),
                noisy=item["noisy"],
                noisy_pct=pct(item["noisy_pct"]),
            )
        )
    lines.append("")
    lines.append("## Noisy / Mixed Evidence Meaning")
    lines.append("")
    lines.append("- `dependency_resource` is noisy when the evidence mixes hard routing capabilities with setup text, or only contains setup/execution commands such as `npm install`, `pip install`, `npm ci`, or similar installation/setup commands.")
    lines.append("- `success_verification` is noisy when concrete acceptance gates are mixed with generic quality language, or when only generic `ensure/check/high quality` language is detected.")
    lines.append("- `boundary_not_for` is noisy when only soft rules or preferences are detected without a clear negative scope, exclusion, or guardrail.")
    lines.append("")
    lines.append("## Kind Breakdown")
    lines.append("")
    for field, item in summary["fields"].items():
        if not item["kinds"]:
            continue
        lines.append(f"### {item['label']}")
        lines.append("")
        for kind, count in sorted(item["kinds"].items(), key=lambda pair: (-pair[1], pair[0])):
            lines.append(f"- `{kind}`: {count}")
        lines.append("")
    lines.append("## Examples")
    lines.append("")
    examples = summary["examples"]
    for field, spec in FIELDS.items():
        lines.append(f"### {spec.label}")
        lines.append("")
        for bucket in ("explicit", "implicit", "noisy", "missing"):
            bucket_examples = examples.get(field, {}).get(bucket, [])
            if not bucket_examples:
                continue
            lines.append(f"**{bucket}**")
            lines.append("")
            for example in bucket_examples:
                evidence = " / ".join(example.get("evidence") or ["no snippet"])
                kind = f" `{example['kind']}`" if example.get("kind") else ""
                lines.append(f"- `{example['skill']}`{kind}: {evidence}")
            lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The public corpus generally contains recoverable evidence for the seven RQ1 field types, but explicitness is uneven. Use condition is nearly universal because public skills usually carry a routing description. Workflow/procedure, output/artifact, input/precondition, and dependency/resource are usually present, but they may be embedded in prose or mixed with implementation/setup detail. Boundary/not-for and success/verification are more conditional: they exist often enough to be worth testing, but their evidence is frequently implicit or noisy.")
    lines.append("")
    lines.append("This supports the current RQ1 framing: RQ1a tests whether each field can discriminate near-neighbour skills under controlled conditions, while RQ1b checks whether those fields are realistically recoverable from public skills. The audit also limits the claim: dependency/resource should be interpreted as capability compatibility when hard dependency evidence is available, not as generic installation text; success/verification is a weaker first-pass retrieval field unless the criteria are concrete.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    rows = [classify_skill(path) for path in public_skill_dirs()]
    word_counts = sorted(row["word_count"] for row in rows)
    total = len(rows)
    median = word_counts[total // 2] if total else 0
    mean = sum(word_counts) / total if total else 0.0
    summary = {
        "total_skills": total,
        "used_original": sum(1 for row in rows if row["used_original"]),
        "mean_word_count": mean,
        "median_word_count": median,
        "fields": status_table(rows),
        "examples": pick_examples(rows),
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_JSONL.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    OUTPUT_MD.write_text(render_md(summary, rows), encoding="utf-8")
    print(json.dumps(summary["fields"], indent=2, sort_keys=True))
    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_JSONL.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
