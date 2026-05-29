---
name: public-anthropic-slack-gif-creator
description: "Public-source background skill based on `slack-gif-creator`. Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like \"make me a GIF of X doing Y for Slack. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "slack-gif-creator"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/slack-gif-creator/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "external-service workflow; depends on account permissions, workspace records, API behavior, and side-effect constraints"
---

# Public Imported Background: slack-gif-creator

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/slack-gif-creator/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

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

- slack gif creator
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
