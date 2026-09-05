---
name: psc-ci-log-first-failure-reader
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Read CI logs to find the first meaningful failure, likely root cause, minimal fix, and rerun path."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-github-maintenance
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Ci Log First Failure Reader

## Overview

Read CI logs to find the first meaningful failure, likely root cause, minimal fix, and rerun path. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

The important distinction is not just the file type or tool name. Route here when the user is asking for failing job and the request depends on failed job output, and need for first meaningful error. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## When to use this skill

Use when the starting artifact is a failed build or test log. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Failed job output | Failing job |
| Need for first meaningful error | Root-cause hypothesis |
| Rerun or fix sequence | Evidence |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Quick start

A normal run is usually:

1. Ignore cascading failures until the first root error is found.
2. Quote log evidence.
3. Map the error to dependency, config, test, or code cause.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Failed job output", "Need for first meaningful error"]
  returns: ["Failing job", "Root-cause hypothesis"]
  tools: ["CI logs", "GitHub Actions or equivalent CI"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Output format

The handoff is usually a compact artifact rather than a long essay. Include failing job, root-cause hypothesis, evidence, and fix/rerun plan when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Failing job
- Root-cause hypothesis
- Evidence
- Fix/rerun plan

## When not to use this skill

Not a fresh code review, PR-comment resolver, or changelog writer. Nearby skills in this cluster include `psc-pr-thread-fix-planner`, `psc-repo-guardrail-hook-installer`, `psc-release-communication-packager`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## References

This workflow can be carried out with ci logs, and github actions or equivalent ci. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Failed job output. Need for first meaningful error. Rerun or fix sequence.

## Examples

- The build failed after the last push. Read the CI output, identify the first real error, explain the likely cause, and give the smallest rerun sequence.
- Analyze the failed GitHub Actions log for the first meaningful failure and minimal fix path. Do not turn this into a PR review or release note.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants failing job or a neighbouring artifact, then ask one clarifying question if needed.

## Best Practices

- The response clearly produces failing job.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
