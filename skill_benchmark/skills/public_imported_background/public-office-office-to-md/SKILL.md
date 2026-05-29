---
name: public-office-office-to-md
description: "Public-source background skill based on `office-to-md`. > Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "office-to-md"
  public_origin: "claude-office-skills/skills"
  source_url: "https://github.com/claude-office-skills/skills/tree/main/office-to-md"
  raw_url: "https://raw.githubusercontent.com/claude-office-skills/skills/main/office-to-md/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for office to md; depends on the source artifact and task context named by the user"
---

# Public Imported Background: office-to-md

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: claude-office-skills/skills
- Source page: https://github.com/claude-office-skills/skills/tree/main/office-to-md
- Raw artifact: https://raw.githubusercontent.com/claude-office-skills/skills/main/office-to-md/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for office to md; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- DOCX or Office document
- document structure
- styles or comments

## Resource And Structure Signals

- office to md
- public SKILL.md metadata
- Word
- DOCX
- styles
- tracked changes

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
