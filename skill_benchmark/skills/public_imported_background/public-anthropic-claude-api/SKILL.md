---
name: public-anthropic-claude-api
description: "Public-source background skill based on `claude-api`. Build, debug, and optimize Claude API / Anthropic SDK apps. Apps built with this skill should include prompt caching. Also handles migrating existing Claude API code between Claude model versions (4.5 \u2192 4.6, 4.6 \u2192 4.7, retired-model replacements). TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`; user asks for the Claude API, Anthropic SDK, or Managed Agents; user adds/modifies/tunes a Claude feature (caching, thinking, compaction, tool use, batch, files, citations, memory) or model (Opus/Sonnet/Haiku) in a file; questions about prompt caching / cache hit rate in an Anthropic SDK project. SKIP: file imports `openai`/other-provider SDK, filename like `*-openai.py`/`*-generic.py`, provider-neutral code, general programming/ML. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "claude-api"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/claude-api"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/claude-api/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for claude api; depends on the source artifact and task context named by the user"
---

# Public Imported Background: claude-api

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/claude-api
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/claude-api/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for claude api; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- API documentation
- authentication context
- schema or tool contract

## Resource And Structure Signals

- claude api
- public SKILL.md metadata
- API
- tool contract
- auth
- schema

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
