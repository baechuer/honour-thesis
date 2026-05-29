---
name: public-oh-my-omx
description: "Public-source background skill based on `omx`. Use when you need multi-agent orchestration for OpenAI Codex CLI. Triggers on: omx, $plan, $ralph, $team, $autopilot, $deep-interview. v0.11.10 \u2014 30+ agents, 35+ workflow skills, tmux team runtime, sparkshell, explore, ralplan. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "omx"
  public_origin: "akillness/oh-my-skills"
  source_url: "https://github.com/akillness/oh-my-skills/tree/main/.agent-skills/omx"
  raw_url: "https://raw.githubusercontent.com/akillness/oh-my-skills/main/.agent-skills/omx/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for omx; depends on the source artifact and task context named by the user"
---

# Public Imported Background: omx

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: akillness/oh-my-skills
- Source page: https://github.com/akillness/oh-my-skills/tree/main/.agent-skills/omx
- Raw artifact: https://raw.githubusercontent.com/akillness/oh-my-skills/main/.agent-skills/omx/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for omx; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- omx
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
