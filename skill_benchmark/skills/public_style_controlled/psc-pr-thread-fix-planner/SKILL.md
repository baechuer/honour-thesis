---
name: psc-pr-thread-fix-planner
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Convert existing pull request review threads into required code changes, response notes, and verification steps."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-github-maintenance
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Pr Thread Fix Planner

## Purpose

Convert existing pull request review threads into required code changes, response notes, and verification steps. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

The important distinction is not just the file type or tool name. Route here when the user is asking for thread action map and the request depends on review comments or pr threads, and code context. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Common requests

Use when reviewer comments already exist and the task is to address them. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Review comments or PR threads | Thread action map |
| Code context | Patch plan |
| Need for response/action mapping | Verification |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Instructions

A normal run is usually:

1. Group comments by requested change.
2. Map each thread to code/test action.
3. Separate accepted fixes from clarification questions.
4. Prepare response notes.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Review comments or PR threads", "Code context"]
  returns: ["Thread action map", "Patch plan"]
  tools: ["GitHub PR review threads"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Response shape

The handoff is usually a compact artifact rather than a long essay. Include thread action map, patch plan, verification, and reply notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Thread action map
- Patch plan
- Verification
- Reply notes

## Common mistakes

Not for fresh code review or CI log diagnosis unless those are requested in the comments. Nearby skills in this cluster include `psc-ci-log-first-failure-reader`, `psc-repo-guardrail-hook-installer`, `psc-release-communication-packager`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Environment notes

This workflow can be carried out with github pr review threads. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Review comments or PR threads. Code context. Need for response/action mapping.

## Example prompts

- Use the review threads on this PR to plan the required fixes, tests, and replies. The comments already exist; I need an action map.
- Address unresolved GitHub PR review comments by mapping each thread to code/test changes and response text. Do not perform a fresh review from scratch.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants thread action map or a neighbouring artifact, then ask one clarifying question if needed.

## Validation

- The response clearly produces thread action map.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
