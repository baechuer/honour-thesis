---
name: public-skill-creator
description: "Public-source background skill based on `skill-creator`. Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "skill-creator"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.system/skill-creator"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "skill authoring workflow; depends on target workflow examples, SKILL.md conventions, optional scripts/references/assets"
---

# Public Imported Background: skill-creator

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.system/skill-creator
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

skill authoring workflow; depends on target workflow examples, SKILL.md conventions, optional scripts/references/assets

## External Dependencies To Preserve

- target workflow examples
- SKILL.md frontmatter
- optional scripts
- optional references
- optional assets

## Resource And Structure Signals

- progressive disclosure
- skill anatomy
- metadata
- optional bundled resources

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
