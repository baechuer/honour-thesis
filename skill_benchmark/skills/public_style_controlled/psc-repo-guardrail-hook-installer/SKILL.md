---
name: psc-repo-guardrail-hook-installer
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Set up repository guardrails such as pre-commit hooks, protected commands, secret checks, and verification commands."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-github-maintenance
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Repo Guardrail Hook Installer

## Overview

Set up repository guardrails such as pre-commit hooks, protected commands, secret checks, and verification commands. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

The important distinction is not just the file type or tool name. Route here when the user is asking for hook/config plan and the request depends on repository tooling, and risky operations to block. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## When to use this skill

Use when the output is workflow safety configuration rather than analysis of a current failure. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Repository tooling | Hook/config plan |
| Risky operations to block | Blocked actions |
| Verification commands | Verification |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Quick start

A normal run is usually:

1. Choose hook or guardrail mechanism.
2. Define blocked operations and checks.
3. Document bypass/maintenance policy.
4. Verify with safe dry runs.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Repository tooling", "Risky operations to block"]
  returns: ["Hook/config plan", "Blocked actions"]
  tools: ["Git hooks, Husky, pre-commit, or local command wrapper"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Output format

The handoff is usually a compact artifact rather than a long essay. Include hook/config plan, blocked actions, verification, and maintenance notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Hook/config plan
- Blocked actions
- Verification
- Maintenance notes

## When not to use this skill

Not for analyzing CI logs or writing release notes. Nearby skills in this cluster include `psc-ci-log-first-failure-reader`, `psc-pr-thread-fix-planner`, `psc-release-communication-packager`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## References

This workflow can be carried out with git hooks, husky, pre-commit, or local command wrapper. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Repository tooling. Risky operations to block. Verification commands.

## Examples

- Set up repository safeguards so contributors cannot accidentally commit secrets or run destructive git operations without confirmation.
- Design git hook guardrails for secret commits, force pushes, reset --hard, branch deletion, and unsafe clean commands, including verification steps.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants hook/config plan or a neighbouring artifact, then ask one clarifying question if needed.

## Best Practices

- The response clearly produces hook/config plan.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
