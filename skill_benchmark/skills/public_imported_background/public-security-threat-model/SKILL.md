---
name: public-security-threat-model
description: "Public-source background skill based on `security-threat-model`. Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concise Markdown threat model. Trigger only when the user explicitly asks to threat model a codebase or path, enumerate threats/abuse paths, or perform AppSec threat modeling. Do not trigger for general architecture summaries, code review, or non-security design work. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "security-threat-model"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-threat-model/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "repository-grounded AppSec threat modeling; depends on repo path, architecture evidence, and optional prompt-template references"
---

# Public Imported Background: security-threat-model

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-threat-model/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

repository-grounded AppSec threat modeling; depends on repo path, architecture evidence, and optional prompt-template references

## External Dependencies To Preserve

- repository files
- architecture summary
- references/prompt-template.md
- references/security-controls-and-assets.md

## Resource And Structure Signals

- references
- output contract
- repo evidence
- threat taxonomy

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
