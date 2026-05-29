---
name: public-openai-notion-research-documentation
description: "Public-source background skill based on `notion-research-documentation`. Research across Notion and synthesize into structured documentation; use when gathering info from multiple Notion sources to produce briefs, comparisons, or reports with citations. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "notion-research-documentation"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/notion-research-documentation"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/notion-research-documentation/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "external-service workflow; depends on account permissions, workspace records, API behavior, and side-effect constraints"
---

# Public Imported Background: notion-research-documentation

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/notion-research-documentation
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/notion-research-documentation/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

external-service workflow; depends on account permissions, workspace records, API behavior, and side-effect constraints

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- external SaaS workspace
- account permissions
- records or API access

## Resource And Structure Signals

- notion research documentation
- public SKILL.md metadata
- external service
- workspace
- automation
- permissions

## Use when

- The retrieval setting needs realistic public-skill noise around this capability.
- The selector should consider tool requirements, file types, resource links, or external systems as part of skill suitability.
- The task is closer to this public skill's dependency profile than to a controlled core skill.

## Not for

- Replacing a controlled gold-label core skill in the main confusable evaluation.
- Hiding a second routing problem inside the selected skill.
- Treating public-source imports as cleanly annotated gold labels.

## Benchmark Role

This skill is intended for large-library and dependency-aware retrieval settings. It helps test whether skill representations preserve information such as required tools, file formats, repository context, external services, and optional resources.
