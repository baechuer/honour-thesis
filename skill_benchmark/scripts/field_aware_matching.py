#!/usr/bin/env python3

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

from run_offline_selectors import counter_cosine, field_text, tokenize


FIELD_GROUPS = [
    "task",
    "input",
    "output",
    "workflow",
    "dependency",
    "boundary",
    "hierarchy",
]

DEFAULT_FIELD_WEIGHTS = {
    "task": 0.25,
    "input": 0.10,
    "output": 0.20,
    "workflow": 0.15,
    "dependency": 0.08,
    "boundary": 0.12,
    "hierarchy": 0.10,
}

NEGATION_PATTERNS = [
    r"\bdo not\b",
    r"\bdon't\b",
    r"\bnot\b",
    r"\bwithout\b",
    r"\bavoid\b",
    r"\brather than\b",
    r"\binstead of\b",
]

OUTPUT_CUES = {
    "answer",
    "artifact",
    "brief",
    "checklist",
    "chart",
    "code",
    "convert",
    "deliver",
    "draft",
    "email",
    "extract",
    "findings",
    "format",
    "json",
    "markdown",
    "matrix",
    "patch",
    "plan",
    "produce",
    "report",
    "return",
    "rewrite",
    "rows",
    "summary",
    "table",
    "template",
    "write",
}

INPUT_CUES = {
    "api",
    "csv",
    "dataset",
    "doc",
    "docx",
    "file",
    "github",
    "html",
    "image",
    "issue",
    "json",
    "log",
    "notebook",
    "openapi",
    "pdf",
    "pull",
    "repo",
    "repository",
    "screenshot",
    "source",
    "spreadsheet",
    "text",
    "trace",
    "url",
    "xlsx",
    "yaml",
}

WORKFLOW_CUES = {
    "anchor",
    "audit",
    "cite",
    "compare",
    "debug",
    "diagnose",
    "evidence",
    "ground",
    "inspect",
    "preserve",
    "rank",
    "reason",
    "review",
    "root",
    "section",
    "step",
    "test",
    "trace",
    "validate",
    "verify",
}

DEPENDENCY_CUES = {
    "airtable",
    "api",
    "browser",
    "claude",
    "cli",
    "dashscope",
    "figma",
    "github",
    "google",
    "huggingface",
    "mcp",
    "notion",
    "openai",
    "python",
    "qwen",
    "slack",
    "stripe",
    "tool",
    "vercel",
}

BROAD_ROLE_CUES = {
    "all",
    "best",
    "catalog",
    "collection",
    "general",
    "guardrail",
    "hub",
    "index",
    "install",
    "manager",
    "orchestration",
    "overview",
    "pattern",
    "router",
    "routing",
    "skill",
    "system",
    "wrapper",
}


@dataclass
class RequestFields:
    task: str
    input: str
    output: str
    workflow: str
    dependency: str
    boundary: str
    hierarchy: str
    positive: str
    exclusions: str

    def as_dict(self) -> dict[str, str]:
        return {
            "task": self.task,
            "input": self.input,
            "output": self.output,
            "workflow": self.workflow,
            "dependency": self.dependency,
            "boundary": self.boundary,
            "hierarchy": self.hierarchy,
            "positive": self.positive,
            "exclusions": self.exclusions,
        }


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def _clauses(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,;]|\band\b|\bbut\b", text) if part.strip()]


def _has_any_token(text: str, cues: set[str]) -> bool:
    return any(token in cues for token in tokenize(text))


def _cue_text(text: str, cues: set[str]) -> str:
    parts: list[str] = []
    for sentence in _sentences(text):
        if _has_any_token(sentence, cues):
            parts.append(sentence)
    if parts:
        return " ".join(parts)
    return text


def _negative_spans(text: str) -> list[str]:
    spans: list[str] = []
    lowered = text.lower()
    for pattern in NEGATION_PATTERNS:
        for match in re.finditer(pattern, lowered):
            start = match.start()
            tail = text[start:]
            stop_match = re.search(r"[.!?;]", tail)
            if stop_match:
                tail = tail[: stop_match.start()]
            spans.append(tail.strip())
    return spans


def _remove_negative_spans(text: str, spans: list[str]) -> str:
    output = text
    for span in spans:
        if span:
            output = output.replace(span, " ")
    return re.sub(r"\s+", " ", output).strip()


def extract_request_fields(query: str) -> RequestFields:
    negative = _negative_spans(query)
    exclusion_text = " ".join(negative)
    positive = _remove_negative_spans(query, negative)

    output_text = _cue_text(positive, OUTPUT_CUES)
    input_text = _cue_text(positive, INPUT_CUES)
    workflow_text = _cue_text(positive, WORKFLOW_CUES)
    dependency_text = _cue_text(positive, DEPENDENCY_CUES)
    hierarchy_text = _cue_text(positive, BROAD_ROLE_CUES)

    task_clauses: list[str] = []
    for clause in _clauses(positive):
        tokens = tokenize(clause)
        if not tokens:
            continue
        if _has_any_token(clause, OUTPUT_CUES | WORKFLOW_CUES) or len(task_clauses) < 2:
            task_clauses.append(clause)
    task_text = " ".join(task_clauses) or positive

    return RequestFields(
        task=task_text,
        input=input_text,
        output=output_text,
        workflow=workflow_text,
        dependency=dependency_text,
        boundary=exclusion_text,
        hierarchy=hierarchy_text,
        positive=positive,
        exclusions=exclusion_text,
    )


def skill_fields(
    skill_name: str,
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
) -> dict[str, str]:
    r1_row = r1[skill_name]
    r2_row = r2[skill_name]
    r3_row = r3.get(skill_name, {})
    return {
        "task": "\n".join(
            [
                skill_name.replace("-", " "),
                str(r1_row.get("family", "")),
                field_text(r1_row, "description"),
                field_text(r2_row, "use_when"),
            ]
        ),
        "input": field_text(r2_row, "preconditions"),
        "output": field_text(r2_row, "output_shape"),
        "workflow": field_text(r2_row, "workflow", "writing_rules"),
        "dependency": field_text(
            r3_row,
            "dependency_profile",
            "external_dependencies",
            "resource_signals",
            "resource_files",
        ),
        "boundary": field_text(r2_row, "not_for"),
        "hierarchy": "\n".join(
            [
                skill_name.replace("-", " "),
                str(r1_row.get("family", "")),
                field_text(r1_row, "description"),
            ]
        ),
    }


def token_overlap_ratio(left_text: str, right_text: str) -> float:
    left = set(tokenize(left_text))
    right = set(tokenize(right_text))
    if not left or not right:
        return 0.0
    return len(left & right) / math.sqrt(len(left) * len(right))


def broad_role_penalty(skill_name: str, fields: dict[str, str], request: RequestFields) -> float:
    skill_terms = tokenize(" ".join([skill_name.replace("-", " "), fields.get("hierarchy", "")]))
    if not skill_terms:
        return 0.0
    broad_count = sum(1 for token in skill_terms if token in BROAD_ROLE_CUES)
    if broad_count == 0:
        return 0.0
    request_terms = set(tokenize(request.positive))
    if request_terms & {"route", "router", "select", "skill", "install", "orchestration", "catalog"}:
        return 0.0
    return min(0.18, 0.04 * broad_count)


def field_aware_pair_score(
    query: str,
    skill_name: str,
    r1: dict[str, dict[str, Any]],
    r2: dict[str, dict[str, Any]],
    r3: dict[str, dict[str, Any]],
    enabled_fields: set[str] | None = None,
    field_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    enabled = enabled_fields or set(FIELD_GROUPS)
    weights = field_weights or DEFAULT_FIELD_WEIGHTS
    request = extract_request_fields(query)
    candidate = skill_fields(skill_name, r1, r2, r3)

    component_scores: dict[str, float] = {}
    for field in FIELD_GROUPS:
        if field not in enabled:
            component_scores[field] = 0.0
            continue
        if field == "boundary":
            positive_mismatch = token_overlap_ratio(request.positive, candidate["boundary"])
            exclusion_alignment = token_overlap_ratio(request.exclusions, candidate["boundary"])
            exclusion_conflict = token_overlap_ratio(request.exclusions, " ".join(candidate[key] for key in ["task", "output", "workflow"]))
            component_scores[field] = max(0.0, exclusion_alignment - 0.8 * positive_mismatch - 0.6 * exclusion_conflict)
        elif field == "hierarchy":
            request_score = counter_cosine(tokenize(request.hierarchy), tokenize(candidate[field]))
            component_scores[field] = request_score
        else:
            request_text = getattr(request, field)
            component_scores[field] = counter_cosine(tokenize(request_text), tokenize(candidate[field]))

    raw_score = sum(weights.get(field, 0.0) * component_scores[field] for field in enabled)
    boundary_penalty = 0.0
    hierarchy_penalty = 0.0
    if "boundary" in enabled:
        boundary_penalty = 0.16 * token_overlap_ratio(request.positive, candidate["boundary"])
        boundary_penalty += 0.10 * token_overlap_ratio(request.exclusions, " ".join(candidate[key] for key in ["task", "output", "workflow"]))
    if "hierarchy" in enabled:
        hierarchy_penalty = broad_role_penalty(skill_name, candidate, request)

    final_score = max(0.0, raw_score - boundary_penalty - hierarchy_penalty)
    return {
        "score": final_score,
        "components": component_scores,
        "boundary_penalty": boundary_penalty,
        "hierarchy_penalty": hierarchy_penalty,
        "request_fields": request.as_dict(),
    }


def parse_field_set(name: str) -> set[str]:
    if name == "task":
        return {"task"}
    if name == "task_output":
        return {"task", "output"}
    if name == "task_output_workflow":
        return {"task", "output", "workflow"}
    if name == "core":
        return {"task", "input", "output", "workflow"}
    if name == "core_dependency":
        return {"task", "input", "output", "workflow", "dependency"}
    if name == "core_boundary":
        return {"task", "input", "output", "workflow", "boundary"}
    if name == "all":
        return set(FIELD_GROUPS)
    if name.startswith("custom:"):
        fields = {part.strip() for part in name.split(":", 1)[1].split("+") if part.strip()}
        unknown = fields - set(FIELD_GROUPS)
        if unknown:
            raise ValueError(f"Unknown custom field groups: {sorted(unknown)}")
        return fields
    raise ValueError(f"Unknown field set: {name}")


def explain_field_set(name: str) -> str:
    return "+".join(sorted(parse_field_set(name)))

