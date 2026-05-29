---
name: public-openai-figma-create-new-file
description: "Public-source background skill based on `figma-create-new-file`. Create a new blank Figma file. Use when the user wants to create a new Figma design or FigJam file, or when you need a new file before calling use_figma. Handles plan resolution via whoami if needed. Usage \u2014 /figma-create-new-file [editorType] [fileName] (e.g. /figma-create-new-file figjam My Whiteboard) Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "figma-create-new-file"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/figma-create-new-file"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-create-new-file/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for figma create new file; depends on the source artifact and task context named by the user"
---

# Public Imported Background: figma-create-new-file

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/figma-create-new-file
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-create-new-file/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for figma create new file; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- design brief
- brand constraints
- visual assets

## Resource And Structure Signals

- figma create new file
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
