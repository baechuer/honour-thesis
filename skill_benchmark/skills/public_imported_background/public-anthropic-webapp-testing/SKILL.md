---
name: public-anthropic-webapp-testing
description: "Public-source background skill based on `webapp-testing`. Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "webapp-testing"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/webapp-testing"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "browser or webapp testing workflow; depends on a target app, runtime state, interaction flow, and visual evidence"
---

# Public Imported Background: webapp-testing

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/webapp-testing
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

browser or webapp testing workflow; depends on a target app, runtime state, interaction flow, and visual evidence

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- browser runtime
- target URL or app
- screenshots
- test flow

## Resource And Structure Signals

- webapp testing
- public SKILL.md metadata
- browser
- DOM
- screenshots
- interaction flow

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
