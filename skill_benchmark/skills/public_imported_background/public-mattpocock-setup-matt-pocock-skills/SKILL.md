---
name: public-mattpocock-setup-matt-pocock-skills
description: "Public-source background skill based on `setup-matt-pocock-skills`. Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitHub or local markdown), triage label vocabulary, and domain doc layout. Run before first use of `to-issues`, `to-prd`, `triage`, `diagnose`, `tdd`, `improve-codebase-architecture`, or `zoom-out` \u2014 or if those skills appear to be missing context about the issue tracker, triage labels, or domain docs. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "setup-matt-pocock-skills"
  public_origin: "mattpocock/skills"
  source_url: "https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills"
  raw_url: "https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/setup-matt-pocock-skills/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for setup matt pocock skills; depends on the source artifact and task context named by the user"
---

# Public Imported Background: setup-matt-pocock-skills

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: mattpocock/skills
- Source page: https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills
- Raw artifact: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/setup-matt-pocock-skills/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for setup matt pocock skills; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- setup matt pocock skills
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
