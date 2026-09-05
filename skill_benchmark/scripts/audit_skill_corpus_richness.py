#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


SECTION_PATTERNS: dict[str, list[str]] = {
    "use": [
        r"\buse when\b",
        r"\bwhen to use\b",
        r"\btrigger",
        r"\bactivation",
        r"\bapplicability",
        r"\boverview\b",
        r"\bpurpose\b",
    ],
    "avoid": [
        r"\bnot for\b",
        r"\bwhen not\b",
        r"\bdo not use\b",
        r"\bavoid\b",
        r"\bout of scope\b",
    ],
    "input": [
        r"\binput",
        r"\bprecondition",
        r"\brequirement",
        r"\bprerequisite",
        r"\bbefore you begin\b",
        r"\bsetup\b",
    ],
    "workflow": [
        r"\bworkflow\b",
        r"\bprocedure\b",
        r"\bprocess\b",
        r"\bsteps?\b",
        r"\binstructions?\b",
        r"\bhow to\b",
        r"\bmethod\b",
    ],
    "output": [
        r"\boutput",
        r"\bdeliverable",
        r"\bresult",
        r"\breturn format\b",
        r"\bexpected\b",
    ],
    "constraints": [
        r"\bconstraint",
        r"\blimitation",
        r"\brules?\b",
        r"\bguardrail",
        r"\bsafety\b",
        r"\bboundar",
    ],
    "dependencies": [
        r"\bdependencies\b",
        r"\bresources?\b",
        r"\btools?\b",
        r"\benvironment\b",
        r"\bapi\b",
        r"\bcli\b",
        r"\bauth",
    ],
    "examples": [
        r"\bexamples?\b",
        r"\bsample\b",
        r"\btests?\b",
        r"\bevaluation\b",
    ],
}

SECTION_REGEXES: dict[str, list[re.Pattern[str]]] = {
    category: [re.compile(pattern, flags=re.I) for pattern in patterns]
    for category, patterns in SECTION_PATTERNS.items()
}

SECTION_TERMS: dict[str, list[str]] = {
    "use": ["use when", "when to use", "trigger", "activation", "applicability", "overview", "purpose"],
    "avoid": ["not for", "when not", "do not use", "avoid", "out of scope"],
    "input": ["input", "precondition", "requirement", "prerequisite", "before you begin", "setup"],
    "workflow": ["workflow", "procedure", "process", "step", "instruction", "how to", "method"],
    "output": ["output", "deliverable", "result", "return format", "expected"],
    "constraints": ["constraint", "limitation", "rule", "guardrail", "safety", "boundar"],
    "dependencies": ["dependencies", "dependency", "resource", "tool", "environment", "api", "cli", "auth"],
    "examples": ["example", "sample", "test", "evaluation"],
}


PROMPT_CUES = {
    "file_or_path": re.compile(r"(/[\w./-]+|\b[\w.-]+\.(?:json|jsonl|csv|pdf|txt|md|yaml|yml|stl|png|jpg|xlsx|docx)\b)"),
    "numbered_steps": re.compile(r"(?m)^\s*\d+\.\s+"),
    "negative_boundary": re.compile(r"\b(do not|don't|not need|instead of|rather than|avoid|without)\b", re.I),
    "explicit_input": re.compile(r"\b(input|file|dataset|provided|given|using|load|parse)\b", re.I),
    "explicit_output": re.compile(r"\b(output|return|produce|write|generate|structured|json|report|answer)\b", re.I),
}

HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_prompt_files(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            for row in data:
                row = dict(row)
                row["_prompt_file"] = str(path)
                rows.append(row)
        elif isinstance(data, dict):
            data = dict(data)
            data["_prompt_file"] = str(path)
            rows.append(data)
    return rows


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def rough_tokens(text: str) -> int:
    return len(text.split())


def normalize_heading(text: str) -> str:
    return re.sub(r"[*_`#]+", "", text).strip().lower()


def markdown_headings(text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for line in text.splitlines():
        if not line.lstrip().startswith("#"):
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((len(match.group(1)), normalize_heading(match.group(2))))
    return headings


def count_bullets(text: str) -> int:
    return len(re.findall(r"(?m)^\s*[-*+]\s+", text))


def count_numbered_steps(text: str) -> int:
    return len(re.findall(r"(?m)^\s*\d+[.)]\s+", text))


def count_file_refs(text: str) -> int:
    return len(PROMPT_CUES["file_or_path"].findall(text[:20000]))


def heading_category_hits(heads: list[tuple[int, str]]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for category, terms in SECTION_TERMS.items():
        matched: list[str] = []
        for _, heading in heads:
            if any(term in heading for term in terms):
                matched.append(heading)
        hits[category] = matched
    return hits


def keyword_category_hits(text: str) -> dict[str, bool]:
    # Keyword hits are only a soft "extractable" signal; explicit headings are
    # computed over the full markdown. Capping keeps the 79k-row external audit
    # comfortably local and repeatable.
    lower = text[:20000].lower()
    hits: dict[str, bool] = {}
    for category, patterns in SECTION_REGEXES.items():
        hits[category] = any(pattern.search(lower) for pattern in patterns)
    return hits


def first_h1(heads: list[tuple[int, str]]) -> str:
    for level, heading in heads:
        if level == 1:
            return heading
    return ""


def audit_skill_text(
    *,
    corpus: str,
    skill_id: str,
    name: str,
    description: str,
    text: str,
    source_path: str = "",
) -> dict[str, Any]:
    front, body = split_frontmatter(text)
    heads = markdown_headings(text)
    heading_hits = heading_category_hits(heads)
    explicit_categories = [cat for cat, values in heading_hits.items() if values]
    # Keep the default audit strict and fast: "extractable" equals explicit
    # markdown heading evidence here. A looser keyword pass can be added later
    # if we need a recall-oriented scan.
    extractable_categories = list(explicit_categories)
    required_core = {"use", "input", "workflow", "output", "constraints"}
    rich_score = len(set(explicit_categories) & required_core)
    tokens = rough_tokens(text)
    numbered_steps = count_numbered_steps(text)
    bullets = count_bullets(text)
    h1 = first_h1(heads)
    has_frontmatter = bool(front)
    has_name_desc = bool(name.strip()) and bool(description.strip())
    template_like = bool(h1) and len(heads) >= 4 and len(explicit_categories) >= 3
    rich_selection = rich_score >= 4 or (rich_score >= 3 and numbered_steps >= 3)
    procedural = bool(heading_hits["workflow"]) or numbered_steps >= 3

    return {
        "corpus": corpus,
        "skill_id": skill_id,
        "name": name,
        "description": description,
        "source_path": source_path,
        "tokens": tokens,
        "description_tokens": rough_tokens(description),
        "has_frontmatter": has_frontmatter,
        "has_name_and_description": has_name_desc,
        "h1": h1,
        "has_h1": bool(h1),
        "heading_labels": [heading for _, heading in heads],
        "h2_labels": [heading for level, heading in heads if level == 2],
        "heading_count": len(heads),
        "bullet_count": bullets,
        "numbered_step_count": numbered_steps,
        "file_ref_count": 0,
        "code_block_count": text.count("```") // 2,
        "explicit_categories": explicit_categories,
        "extractable_categories": extractable_categories,
        "explicit_category_count": len(explicit_categories),
        "extractable_category_count": len(extractable_categories),
        "heading_hits": {cat: values[:6] for cat, values in heading_hits.items() if values},
        "rich_score_core": rich_score,
        "template_like": template_like,
        "rich_selection_schema": rich_selection,
        "procedural_signal": procedural,
    }


def load_external_skills(repo_root: Path) -> list[dict[str, Any]]:
    path = repo_root / "external" / "skillrouter_eval_core" / "derived" / "representations" / "all_I2.jsonl"
    rows = load_jsonl(path)
    audited: list[dict[str, Any]] = []
    for row in rows:
        audited.append(
            audit_skill_text(
                corpus="external_skillrouter_all",
                skill_id=row["skill_id"],
                name=row.get("name", ""),
                description=row.get("description", ""),
                text=row.get("text", ""),
                source_path=str(path),
            )
        )
    return audited


def load_local_skills(repo_root: Path) -> list[dict[str, Any]]:
    skills_dir = repo_root / "skills"
    audited: list[dict[str, Any]] = []
    for path in sorted(skills_dir.glob("**/SKILL.md")):
        if "/source/" in path.as_posix():
            continue
        rel = path.relative_to(skills_dir)
        skill_id = path.parent.name
        family = rel.parts[0] if rel.parts else ""
        text = path.read_text(encoding="utf-8", errors="replace")
        front, _ = split_frontmatter(text)
        name = ""
        description = ""
        for line in front.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip("\"'")
        audited.append(
            audit_skill_text(
                corpus=f"local_family:{family}",
                skill_id=skill_id,
                name=name or skill_id,
                description=description,
                text=text,
                source_path=str(path),
            )
        )
    return audited


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    if not n:
        return {"count": 0}

    def rate(pred) -> float:
        return sum(1 for row in rows if pred(row)) / n

    def numeric(field: str) -> list[float]:
        return [float(row[field]) for row in rows]

    token_values = sorted(numeric("tokens"))
    heading_values = sorted(numeric("heading_count"))
    category_values = sorted(numeric("explicit_category_count"))
    section_rates = {
        category: rate(lambda row, c=category: c in row["explicit_categories"])
        for category in SECTION_PATTERNS
    }
    heading_counter: Counter[str] = Counter()
    h2_counter: Counter[str] = Counter()
    h1_counter: Counter[str] = Counter()
    for row in rows:
        heading_counter.update(row["heading_labels"])
        h2_counter.update(row["h2_labels"])
        if row["h1"]:
            h1_counter[row["h1"]] += 1
    return {
        "count": n,
        "tokens_median": median(token_values),
        "tokens_mean": mean(token_values),
        "tokens_p10": token_values[int((n - 1) * 0.10)],
        "tokens_p90": token_values[int((n - 1) * 0.90)],
        "heading_count_median": median(heading_values),
        "explicit_category_count_median": median(category_values),
        "has_h1_rate": rate(lambda row: row["has_h1"]),
        "has_name_description_rate": rate(lambda row: row["has_name_and_description"]),
        "template_like_rate": rate(lambda row: row["template_like"]),
        "rich_selection_schema_rate": rate(lambda row: row["rich_selection_schema"]),
        "procedural_signal_rate": rate(lambda row: row["procedural_signal"]),
        "numbered_steps_ge3_rate": rate(lambda row: row["numbered_step_count"] >= 3),
        "bullets_ge3_rate": rate(lambda row: row["bullet_count"] >= 3),
        "section_rates": section_rates,
        "top_h1": h1_counter.most_common(20),
        "top_h2": h2_counter.most_common(30),
        "top_headings": heading_counter.most_common(30),
    }


def prompt_audit(rows: list[dict[str, Any]], corpus: str) -> list[dict[str, Any]]:
    audited = []
    for row in rows:
        prompt = row.get("prompt") or row.get("instruction_text") or ""
        gold = row.get("gold_skill") or row.get("skill_names") or []
        if isinstance(gold, str):
            gold_count = 1
            gold_list = [gold]
        else:
            gold_list = list(gold)
            gold_count = len(gold_list)
        alternatives = row.get("closest_alternatives") or []
        audited.append(
            {
                "corpus": corpus,
                "id": row.get("id") or row.get("task_id") or "",
                "tokens": rough_tokens(prompt),
                "file_ref_count": count_file_refs(prompt),
                "numbered_step_count": len(PROMPT_CUES["numbered_steps"].findall(prompt)),
                "negative_boundary_count": len(PROMPT_CUES["negative_boundary"].findall(prompt)),
                "has_explicit_input": bool(PROMPT_CUES["explicit_input"].search(prompt)),
                "has_explicit_output": bool(PROMPT_CUES["explicit_output"].search(prompt)),
                "gold_count": gold_count,
                "closest_alternative_count": len(alternatives),
                "gold": gold_list[:8],
            }
        )
    return audited


def summarize_prompts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    if not n:
        return {"count": 0}

    def rate(pred) -> float:
        return sum(1 for row in rows if pred(row)) / n

    tokens = sorted(row["tokens"] for row in rows)
    return {
        "count": n,
        "tokens_median": median(tokens),
        "tokens_mean": mean(tokens),
        "tokens_p10": tokens[int((n - 1) * 0.10)],
        "tokens_p90": tokens[int((n - 1) * 0.90)],
        "tokens_max": tokens[-1],
        "tokens_lt50_rate": rate(lambda row: row["tokens"] < 50),
        "tokens_50_99_rate": rate(lambda row: 50 <= row["tokens"] < 100),
        "tokens_100_199_rate": rate(lambda row: 100 <= row["tokens"] < 200),
        "tokens_ge200_rate": rate(lambda row: row["tokens"] >= 200),
        "file_ref_rate": rate(lambda row: row["file_ref_count"] > 0),
        "numbered_steps_rate": rate(lambda row: row["numbered_step_count"] > 0),
        "negative_boundary_rate": rate(lambda row: row["negative_boundary_count"] > 0),
        "explicit_input_rate": rate(lambda row: row["has_explicit_input"]),
        "explicit_output_rate": rate(lambda row: row["has_explicit_output"]),
        "gold_count_mean": mean(row["gold_count"] for row in rows),
        "closest_alternatives_mean": mean(row["closest_alternative_count"] for row in rows),
    }


def pct(value: float) -> str:
    return f"{value:.1%}"


def fmt_num(value: float) -> str:
    if abs(value - round(value)) < 0.05:
        return f"{value:.0f}"
    return f"{value:.1f}"


def sample_rows(rows: list[dict[str, Any]], *, richest: bool, limit: int = 8) -> list[dict[str, Any]]:
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            row["rich_score_core"],
            row["explicit_category_count"],
            row["heading_count"],
            row["tokens"],
        ),
        reverse=richest,
    )
    return [
        {
            "skill_id": row["skill_id"],
            "name": row["name"],
            "tokens": row["tokens"],
            "h1": row["h1"],
            "heading_count": row["heading_count"],
            "explicit_categories": row["explicit_categories"],
            "source_path": row["source_path"],
        }
        for row in sorted_rows[:limit]
    ]


def markdown_table_summary(title: str, summaries: dict[str, dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.append(
        "| Corpus | Rows | Median tokens | P90 tokens | H1 | Rich schema | Procedural | Use | Input | Workflow | Output | Constraints | Dependencies |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, summary in summaries.items():
        if not summary.get("count"):
            continue
        sections = summary["section_rates"]
        lines.append(
            f"| {name} | {summary['count']} | {fmt_num(summary['tokens_median'])} | {fmt_num(summary['tokens_p90'])} "
            f"| {pct(summary['has_h1_rate'])} | {pct(summary['rich_selection_schema_rate'])} "
            f"| {pct(summary['procedural_signal_rate'])} | {pct(sections['use'])} "
            f"| {pct(sections['input'])} | {pct(sections['workflow'])} | {pct(sections['output'])} "
            f"| {pct(sections['constraints'])} | {pct(sections['dependencies'])} |"
        )
    lines.append("")
    return lines


def markdown_prompt_summary(summaries: dict[str, dict[str, Any]]) -> list[str]:
    lines = ["## Prompt-Side Explicitness", ""]
    lines.append(
        "| Prompt set | Rows | Mean tokens | Median tokens | P90 tokens | <50 tokens | >=200 tokens | File/path refs | Numbered steps | Negative boundaries | Explicit input | Explicit output | Mean gold skills | Mean closest alternatives |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, summary in summaries.items():
        lines.append(
            f"| {name} | {summary['count']} | {fmt_num(summary['tokens_mean'])} | {fmt_num(summary['tokens_median'])} | {fmt_num(summary['tokens_p90'])} "
            f"| {pct(summary['tokens_lt50_rate'])} | {pct(summary['tokens_ge200_rate'])} "
            f"| {pct(summary['file_ref_rate'])} | {pct(summary['numbered_steps_rate'])} "
            f"| {pct(summary['negative_boundary_rate'])} | {pct(summary['explicit_input_rate'])} "
            f"| {pct(summary['explicit_output_rate'])} | {fmt_num(summary['gold_count_mean'])} "
            f"| {fmt_num(summary['closest_alternatives_mean'])} |"
        )
    lines.append("")
    return lines


def markdown_heading_frequency(summaries: dict[str, dict[str, Any]]) -> list[str]:
    lines = ["## Frequent Heading Labels", ""]
    lines.append("Top repeated normalized headings. H2 headings are usually the main section labels, so they are the cleanest signal of template-like structure.")
    lines.append("")
    for name in ["SkillRouter all", "SkillRouter scored gold names", "Local controlled gold+alts", "Local public import wrappers"]:
        summary = summaries.get(name)
        if not summary or not summary.get("count"):
            continue
        lines.append(f"### {name}")
        lines.append("")
        lines.append("| Top H2 headings | Count | Top headings, any level | Count |")
        lines.append("|---|---:|---|---:|")
        top_h2 = summary.get("top_h2", [])[:12]
        top_any = summary.get("top_headings", [])[:12]
        for idx in range(max(len(top_h2), len(top_any))):
            h2, h2_count = top_h2[idx] if idx < len(top_h2) else ("", "")
            any_heading, any_count = top_any[idx] if idx < len(top_any) else ("", "")
            lines.append(f"| `{h2}` | {h2_count} | `{any_heading}` | {any_count} |")
        lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit skill body richness and prompt explicitness across local and SkillRouter corpora.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="JSON output path. Defaults to skill_benchmark/outputs/skill_corpus_richness_audit.json.",
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=None,
        help="Markdown output path. Defaults to skill_benchmark/outputs/skill_corpus_richness_audit.md.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    json_output = args.json_output or repo_root / "outputs" / "skill_corpus_richness_audit.json"
    md_output = args.md_output or repo_root / "outputs" / "skill_corpus_richness_audit.md"

    external = load_external_skills(repo_root)
    local = load_local_skills(repo_root)

    controlled_prompts = load_prompt_files(sorted((repo_root / "prompts").glob("*.json")))
    public_gold_prompts = load_prompt_files(sorted((repo_root / "prompts_public_gold").glob("*.json")))
    external_tasks = load_jsonl(repo_root / "external" / "skillrouter_eval_core" / "derived" / "tasks_scored.jsonl")

    controlled_skill_slugs: set[str] = set()
    for prompt in controlled_prompts:
        if prompt.get("gold_skill"):
            controlled_skill_slugs.add(prompt["gold_skill"])
        controlled_skill_slugs.update(prompt.get("closest_alternatives") or [])

    public_gold_skill_slugs: set[str] = set()
    for prompt in public_gold_prompts:
        if prompt.get("gold_skill"):
            public_gold_skill_slugs.add(prompt["gold_skill"])
        public_gold_skill_slugs.update(prompt.get("closest_alternatives") or [])

    external_gold_names: set[str] = set()
    for task in external_tasks:
        external_gold_names.update(task.get("skill_names") or [])

    local_controlled = [row for row in local if row["skill_id"] in controlled_skill_slugs]
    local_public_gold = [row for row in local if row["skill_id"] in public_gold_skill_slugs]
    local_public_wrappers = [row for row in local if row["corpus"] == "local_family:public_imported_background"]
    local_non_public = [row for row in local if row["corpus"] != "local_family:public_imported_background"]
    external_gold_like = [row for row in external if row["name"] in external_gold_names]

    corpus_groups = {
        "SkillRouter all": external,
        "SkillRouter scored gold names": external_gold_like,
        "Local all": local,
        "Local non-public": local_non_public,
        "Local controlled gold+alts": local_controlled,
        "Local public-gold gold+alts": local_public_gold,
        "Local public import wrappers": local_public_wrappers,
    }
    summaries = {name: summarize(rows) for name, rows in corpus_groups.items()}

    prompt_groups = {
        "SkillRouter scored tasks": prompt_audit(external_tasks, "external_skillrouter_tasks"),
        "Local controlled prompts": prompt_audit(controlled_prompts, "local_controlled_prompts"),
        "Local public-gold prompts": prompt_audit(public_gold_prompts, "local_public_gold_prompts"),
    }
    prompt_summaries = {name: summarize_prompts(rows) for name, rows in prompt_groups.items()}

    payload = {
        "method": {
            "note": "Static lexical/markdown audit only. It measures explicit structure and prompt cues; it cannot prove whether a skill was AI-generated.",
            "rich_selection_schema_definition": "At least four of use/input/workflow/output/constraints are explicit headings, or at least three plus >=3 numbered steps.",
            "procedural_signal_definition": "Workflow/procedure/steps heading or >=3 numbered steps.",
        },
        "summaries": summaries,
        "prompt_summaries": prompt_summaries,
        "samples": {
            "skillrouter_rich_examples": sample_rows(external, richest=True),
            "skillrouter_sparse_examples": sample_rows(external, richest=False),
            "local_controlled_rich_examples": sample_rows(local_controlled, richest=True),
            "local_controlled_sparse_examples": sample_rows(local_controlled, richest=False),
            "local_public_wrapper_examples": sample_rows(local_public_wrappers, richest=True, limit=5),
        },
    }

    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Skill Corpus Richness Audit",
        "",
        "Static audit of markdown structure in SkillRouter-Eval-Core skills versus the local thesis benchmark skills.",
        "",
        "**Important limitation:** this script can detect explicit structure, headings, and prompt cues. It cannot prove that a skill was AI-generated unless the source metadata says so.",
        "",
        f"- SkillRouter full-body rows audited: {len(external)}",
        f"- SkillRouter scored gold-name rows matched by `name`: {len(external_gold_like)}",
        f"- Local skill wrappers audited: {len(local)}",
        f"- Local controlled gold+alternative skills matched: {len(local_controlled)}",
        "",
        "Rich schema = at least four of use/input/workflow/output/constraints as explicit headings, or at least three plus three numbered steps.",
        "",
    ]
    lines.extend(markdown_table_summary("Skill Body Structure", summaries))
    lines.extend(markdown_heading_frequency(summaries))
    lines.extend(markdown_prompt_summary(prompt_summaries))

    lines.extend(
        [
            "## Interpretation",
            "",
            "- If SkillRouter rows show high H1/heading/procedure rates, then full-body retrieval is partly benefiting from already-normalized markdown skill bodies, not just from raw unstructured text.",
            "- If local controlled prompts show many closest alternatives, that is evidence that the local benchmark is intentionally harder as a near-neighbour discrimination task.",
            "- If SkillRouter prompts show high file/path, input/output, and numbered-step rates, then the external task prompts are also giving strong routing cues.",
            "- This audit should be used as a corpus-difference caveat, not as a replacement for retrieval metrics.",
            "",
            "## Examples",
            "",
            "### Rich SkillRouter Examples",
            "",
        ]
    )
    for row in payload["samples"]["skillrouter_rich_examples"]:
        lines.append(f"- `{row['skill_id']}`: {row['tokens']} tokens, {row['heading_count']} headings, fields={row['explicit_categories']}")
    lines.extend(["", "### Sparse SkillRouter Examples", ""])
    for row in payload["samples"]["skillrouter_sparse_examples"]:
        lines.append(f"- `{row['skill_id']}`: {row['tokens']} tokens, {row['heading_count']} headings, fields={row['explicit_categories']}")
    lines.extend(["", "### Local Controlled Gold/Alternative Examples", ""])
    for row in payload["samples"]["local_controlled_rich_examples"][:5]:
        lines.append(f"- `{row['skill_id']}`: {row['tokens']} tokens, {row['heading_count']} headings, fields={row['explicit_categories']}")

    md_output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {json_output}")
    print(f"Wrote {md_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
