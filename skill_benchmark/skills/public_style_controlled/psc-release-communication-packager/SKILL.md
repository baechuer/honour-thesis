---
name: psc-release-communication-packager
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Turn merged changes into audience-appropriate release notes, changelog sections, upgrade notes, and breaking-change warnings."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-github-maintenance
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Release Communication Packager

## Overview

Turn merged changes into audience-appropriate release notes, changelog sections, upgrade notes, and breaking-change warnings. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

The important distinction is not just the file type or tool name. Route here when the user is asking for release notes and the request depends on merged prs, commits, or change list, and audience. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## When to use this skill

Use after changes are merged or ready to ship and the user needs release communication. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Merged PRs, commits, or change list | Release notes |
| Audience | Changelog bullets |
| Release categories | Upgrade caveats |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Quick start

A normal run is usually:

1. Group features, fixes, breaking changes, and migrations.
2. Adjust language to user/developer audience.
3. Keep implementation details only when useful.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Merged PRs, commits, or change list", "Audience"]
  returns: ["Release notes", "Changelog bullets"]
  tools: ["Commit or PR summary"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Output format

The handoff is usually a compact artifact rather than a long essay. Include release notes, changelog bullets, and upgrade caveats when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Release notes
- Changelog bullets
- Upgrade caveats

## When not to use this skill

Not for code review, review-thread resolution, or CI failure debugging. Nearby skills in this cluster include `psc-ci-log-first-failure-reader`, `psc-pr-thread-fix-planner`, `psc-repo-guardrail-hook-installer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## References

This workflow can be carried out with commit or pr summary. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Merged PRs, commits, or change list. Audience. Release categories.

## Examples

- Turn the merged PR list into release notes grouped by features, fixes, and breaking changes, with upgrade notes where needed.
- Prepare user-facing release communication from completed changes. I need release notes/changelog language, not bug-finding or CI triage.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants release notes or a neighbouring artifact, then ask one clarifying question if needed.

## Best Practices

- The response clearly produces release notes.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
