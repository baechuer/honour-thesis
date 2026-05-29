---
name: public-oh-my-agent-browser
description: "Public-source background skill based on `agent-browser`. Run fresh-session browser automation and deterministic website verification for AI agents. Use when the job needs a clean disposable browser, stable snapshot refs, and explicit before/after evidence across forms, page state, screenshots, and accessibility-tree checks. Not for reusing the user's already-open browser (`playwriter`), exact rendered-UI feedback packets (`agentation`), or plan/diff approval (`plannotator`). Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "agent-browser"
  public_origin: "akillness/oh-my-skills"
  source_url: "https://github.com/akillness/oh-my-skills/tree/main/.agent-skills/agent-browser"
  raw_url: "https://raw.githubusercontent.com/akillness/oh-my-skills/main/.agent-skills/agent-browser/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "browser or webapp testing workflow; depends on a target app, runtime state, interaction flow, and visual evidence"
---

# Public Imported Background: agent-browser

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: akillness/oh-my-skills
- Source page: https://github.com/akillness/oh-my-skills/tree/main/.agent-skills/agent-browser
- Raw artifact: https://raw.githubusercontent.com/akillness/oh-my-skills/main/.agent-skills/agent-browser/SKILL.md
- License note: See source repository for license and skill-specific terms.

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

- agent browser
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
