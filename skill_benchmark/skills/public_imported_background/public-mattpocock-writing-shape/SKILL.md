---
name: public-mattpocock-writing-shape
description: "Public-source background skill based on `writing-shape`. Take a markdown file of raw material and shape it into an article through a conversational session \u2014 drafting candidate openings, growing the piece paragraph by paragraph, arguing about format (lists, tables, callouts, quotes) at each step. Use when the user has a pile of notes, fragments, or a rough draft and wants help turning it into something publishable. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "writing-shape"
  public_origin: "mattpocock/skills"
  source_url: "https://github.com/mattpocock/skills/tree/main/skills/in-progress/writing-shape"
  raw_url: "https://raw.githubusercontent.com/mattpocock/skills/main/skills/in-progress/writing-shape/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for writing shape; depends on the source artifact and task context named by the user"
---

# Public Imported Background: writing-shape

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: mattpocock/skills
- Source page: https://github.com/mattpocock/skills/tree/main/skills/in-progress/writing-shape
- Raw artifact: https://raw.githubusercontent.com/mattpocock/skills/main/skills/in-progress/writing-shape/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for writing shape; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- writing shape
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
