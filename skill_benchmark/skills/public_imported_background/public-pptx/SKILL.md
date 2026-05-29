---
name: public-pptx
description: "Public-source background skill based on `pptx`. Use this skill any time a .pptx file is involved in any way \u2014 as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \\\"deck,\\\" \\\"slides,\\\" \\\"presentation,\\\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "pptx"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/pptx"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/pptx/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "presentation artifact workflow; depends on slide structure, speaker notes, visual layouts, templates, and render checks"
---

# Public Imported Background: pptx

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/pptx
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/pptx/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

presentation artifact workflow; depends on slide structure, speaker notes, visual layouts, templates, and render checks

## External Dependencies To Preserve

- .pptx file
- slide layouts
- speaker notes
- template assets
- rendering tools

## Resource And Structure Signals

- slides
- layouts
- notes
- theme
- visual QA
- export

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
