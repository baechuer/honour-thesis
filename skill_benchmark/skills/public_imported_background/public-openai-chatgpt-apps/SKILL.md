---
name: public-openai-chatgpt-apps
description: "Public-source background skill based on `chatgpt-apps`. Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply Apps SDK metadata or CSP or domain settings, or produce a docs-aligned project scaffold. Prefer a docs-first workflow by invoking the openai-docs skill or OpenAI developer docs MCP tools before generating code. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "chatgpt-apps"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/chatgpt-apps"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/chatgpt-apps/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for chatgpt apps; depends on the source artifact and task context named by the user"
---

# Public Imported Background: chatgpt-apps

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/chatgpt-apps
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/chatgpt-apps/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for chatgpt apps; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- chatgpt apps
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
