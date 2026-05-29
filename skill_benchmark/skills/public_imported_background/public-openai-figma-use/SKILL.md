---
name: public-openai-figma-use
description: "Public-source background skill based on `figma-use`. **MANDATORY prerequisite** \u2014 you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context \u2014 e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "figma-use"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/figma-use"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-use/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for figma use; depends on the source artifact and task context named by the user"
---

# Public Imported Background: figma-use

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/figma-use
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-use/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for figma use; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- design brief
- brand constraints
- visual assets

## Resource And Structure Signals

- figma use
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
