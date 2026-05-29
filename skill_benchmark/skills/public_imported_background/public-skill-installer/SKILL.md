---
name: public-skill-installer
description: "Public-source background skill based on `skill-installer`. Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or install a skill from another repo (including private repos). Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "skill-installer"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.system/skill-installer"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-installer/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "skill installation workflow; depends on GitHub or catalog source, local skill path, and install command behavior"
---

# Public Imported Background: skill-installer

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.system/skill-installer
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-installer/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

skill installation workflow; depends on GitHub or catalog source, local skill path, and install command behavior

## External Dependencies To Preserve

- GitHub repository or catalog
- local skill directory
- network access
- installer command

## Resource And Structure Signals

- registry lookup
- download path
- local install path
- restart requirement

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
