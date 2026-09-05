#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


PROMPT_FILE = Path("skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json")

HARD_PUBLIC_LABEL_CASES = {
    "public_gold_p47_figma_generate_library",
    "public_gold_p65_hf_local_models",
    "public_gold_p81_shopify_automation",
}

PROVIDER_OR_TOOL_TERMS = {
    "airtable",
    "chatgpt",
    "chrome devtools",
    "claude",
    "cloudflare",
    "core web vitals",
    "figma",
    "github",
    "gradio",
    "hugging face",
    "husky",
    "jupyter",
    "linear",
    "lint-staged",
    "markitdown",
    "mcp",
    "mysql",
    "netlify",
    "notion",
    "obsidian",
    "openai",
    "pdfplumber",
    "playwright",
    "postgresql",
    "render",
    "sentry",
    "shopify",
    "sheets",
    "slack",
    "wrangler",
    "zendesk",
}


def provider_cue_status(prompt: str) -> str:
    text = prompt.lower()
    if any(term in text for term in PROVIDER_OR_TOOL_TERMS):
        return "provider_or_tool_explicit"
    return "provider_or_tool_implicit_or_generic"


def prompt_information_level(row: dict) -> str:
    cue_status = provider_cue_status(row.get("prompt", ""))
    if row["id"] in HARD_PUBLIC_LABEL_CASES:
        return "hard_public_case"
    if cue_status == "provider_or_tool_explicit":
        return "provider_explicit_with_procedural_requirements"
    return "provider_implicit_or_generic_with_procedural_requirements"


def label_status(row: dict) -> str:
    if row["id"] in HARD_PUBLIC_LABEL_CASES:
        return "hard_public_label_case"
    if row.get("acceptable_alternatives"):
        return "stable_with_acceptable_alternatives"
    return "stable_strict_public_gold"


def cleanup_note(row: dict, status: str, cue_status: str) -> str:
    axes = ", ".join(row.get("field_axes", [])) or "not recorded"
    if status == "hard_public_label_case":
        return (
            "Retain as a hard public-gold case for external-validity pressure; "
            "manual inspection is required before using this prompt in headline strict-only tables. "
            f"Current procedural axes: {axes}."
        )
    if status == "stable_with_acceptable_alternatives":
        return (
            "Gold skill is defensible, but near-equivalent alternatives are recorded and should count "
            f"under acceptable scoring. Provider/tool cue status: {cue_status}. Procedural axes: {axes}."
        )
    return (
        "Gold skill is currently treated as strict public-gold. Provider/tool names, if present, "
        f"are retained as dependency cues rather than leakage. Procedural axes: {axes}."
    )


def main() -> int:
    rows = json.loads(PROMPT_FILE.read_text(encoding="utf-8"))
    for row in rows:
        cue_status = provider_cue_status(row.get("prompt", ""))
        status = label_status(row)
        row["validation_status"] = "cleaned_public_gold_with_caveats"
        row["label_status"] = status
        row["provider_cue_status"] = cue_status
        row["prompt_information_level"] = prompt_information_level(row)
        row["gold_label_basis"] = row.get("field_axes", [])
        row["gold_label_cleanup_note"] = cleanup_note(row, status, cue_status)
    PROMPT_FILE.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {PROMPT_FILE}")
    print(f"Rows: {len(rows)}")
    print(f"Hard public-label cases: {len(HARD_PUBLIC_LABEL_CASES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
