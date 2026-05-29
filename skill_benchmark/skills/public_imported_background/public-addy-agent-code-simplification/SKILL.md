---
name: public-addy-agent-code-simplification
description: "Public-source background skill based on `code-simplification`. Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "code-simplification"
  public_origin: "addyosmani/agent-skills"
  source_url: "https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification"
  raw_url: "https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/code-simplification/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for code simplification; depends on the source artifact and task context named by the user"
---

# Public Imported Background: code-simplification

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: addyosmani/agent-skills
- Source page: https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification
- Raw artifact: https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/code-simplification/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for code simplification; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- code simplification
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
