---
name: public-office-airtable-automation
description: "Public-source background skill based on `airtable-automation`. Airtable database automation - views, automations, integrations, and workflow triggers Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "airtable-automation"
  public_origin: "claude-office-skills/skills"
  source_url: "https://github.com/claude-office-skills/skills/tree/main/airtable-automation"
  raw_url: "https://raw.githubusercontent.com/claude-office-skills/skills/main/airtable-automation/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "external-service workflow; depends on account permissions, workspace records, API behavior, and side-effect constraints"
---

# Public Imported Background: airtable-automation

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: claude-office-skills/skills
- Source page: https://github.com/claude-office-skills/skills/tree/main/airtable-automation
- Raw artifact: https://raw.githubusercontent.com/claude-office-skills/skills/main/airtable-automation/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

external-service workflow; depends on account permissions, workspace records, API behavior, and side-effect constraints

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- external SaaS workspace
- account permissions
- records or API access

## Resource And Structure Signals

- airtable automation
- public SKILL.md metadata
- external service
- workspace
- automation
- permissions

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
