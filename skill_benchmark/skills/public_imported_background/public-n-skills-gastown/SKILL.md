---
name: public-n-skills-gastown
description: "Public-source background skill based on `gastown`. Multi-agent orchestrator for Claude Code. Use when user mentions gastown, gas town, gt commands, bd commands, convoys, polecats, crew, rigs, slinging work, multi-agent coordination, beads, hooks, molecules, workflows, the witness, the mayor, the refinery, the deacon, dogs, escalation, or wants to run multiple AI agents on projects simultaneously. Handles installation, workspace setup, work tracking, agent lifecycle, crash recovery, and all gt/bd CLI operations. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "gastown"
  public_origin: "numman-ali/n-skills"
  source_url: "https://github.com/numman-ali/n-skills/tree/main/skills/tools/gastown/skills/gastown"
  raw_url: "https://raw.githubusercontent.com/numman-ali/n-skills/main/skills/tools/gastown/skills/gastown/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for gastown; depends on the source artifact and task context named by the user"
---

# Public Imported Background: gastown

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: numman-ali/n-skills
- Source page: https://github.com/numman-ali/n-skills/tree/main/skills/tools/gastown/skills/gastown
- Raw artifact: https://raw.githubusercontent.com/numman-ali/n-skills/main/skills/tools/gastown/skills/gastown/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for gastown; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- gastown
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
