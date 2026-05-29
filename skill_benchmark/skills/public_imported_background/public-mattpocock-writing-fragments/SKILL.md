---
name: public-mattpocock-writing-fragments
description: "Public-source background skill based on `writing-fragments`. Grilling session that mines the user for fragments \u2014 heterogeneous nuggets of writing (claims, vignettes, sharp sentences, half-thoughts) \u2014 and appends them to a single document as raw material for a future article. Use when the user wants to develop ideas before imposing structure, or mentions \"fragments\", \"ideate\", or \"raw material\" for writing. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "writing-fragments"
  public_origin: "mattpocock/skills"
  source_url: "https://github.com/mattpocock/skills/tree/main/skills/in-progress/writing-fragments"
  raw_url: "https://raw.githubusercontent.com/mattpocock/skills/main/skills/in-progress/writing-fragments/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for writing fragments; depends on the source artifact and task context named by the user"
---

# Public Imported Background: writing-fragments

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: mattpocock/skills
- Source page: https://github.com/mattpocock/skills/tree/main/skills/in-progress/writing-fragments
- Raw artifact: https://raw.githubusercontent.com/mattpocock/skills/main/skills/in-progress/writing-fragments/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for writing fragments; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- writing fragments
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
