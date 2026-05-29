---
name: public-openai-figma-generate-library
description: "Public-source background skill based on `figma-generate-library`. Build or update a professional-grade design system in Figma from a codebase. Use when the user wants to create variables/tokens, build component libraries, set up theming (light/dark modes), document foundations, or reconcile gaps between code and Figma. This skill teaches WHAT to build and in WHAT ORDER \u2014 it complements the `figma-use` skill which teaches HOW to call the Plugin API. Both skills should be loaded together. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "figma-generate-library"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/figma-generate-library"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-generate-library/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for figma generate library; depends on the source artifact and task context named by the user"
---

# Public Imported Background: figma-generate-library

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/figma-generate-library
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-generate-library/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for figma generate library; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- design brief
- brand constraints
- visual assets

## Resource And Structure Signals

- figma generate library
- public SKILL.md metadata
- design
- brand
- visual
- assets

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
