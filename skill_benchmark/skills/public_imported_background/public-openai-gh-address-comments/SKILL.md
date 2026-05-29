---
name: public-openai-gh-address-comments
description: "Public-source background skill based on `gh-address-comments`. Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "gh-address-comments"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/gh-address-comments"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-address-comments/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for gh address comments; depends on the source artifact and task context named by the user"
---

# Public Imported Background: gh-address-comments

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/gh-address-comments
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-address-comments/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for gh address comments; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- gh address comments
- public SKILL.md metadata

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
