---
name: public-anthropic-theme-factory
description: "Public-source background skill based on `theme-factory`. Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "theme-factory"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/theme-factory"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/theme-factory/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for theme factory; depends on the source artifact and task context named by the user"
---

# Public Imported Background: theme-factory

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/theme-factory
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/theme-factory/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for theme factory; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- design brief
- brand constraints
- visual assets

## Resource And Structure Signals

- theme factory
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
