---
name: public-obsidian-defuddle
description: "Public-source background skill based on `defuddle`. Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page. Do NOT use for URLs ending in .md \u2014 those are already markdown, use WebFetch directly. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "defuddle"
  public_origin: "kepano/obsidian-skills"
  source_url: "https://github.com/kepano/obsidian-skills/tree/main/skills/defuddle"
  raw_url: "https://raw.githubusercontent.com/kepano/obsidian-skills/main/skills/defuddle/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for defuddle; depends on the source artifact and task context named by the user"
---

# Public Imported Background: defuddle

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: kepano/obsidian-skills
- Source page: https://github.com/kepano/obsidian-skills/tree/main/skills/defuddle
- Raw artifact: https://raw.githubusercontent.com/kepano/obsidian-skills/main/skills/defuddle/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for defuddle; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- defuddle
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
