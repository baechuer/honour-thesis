---
name: psc-visual-screenshot-reviewer
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Compare page screenshots or visual states for layout shifts, clipping, spacing, typography, and responsive regressions."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-browser-quality
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Visual Screenshot Reviewer

## Guide

Compare page screenshots or visual states for layout shifts, clipping, spacing, typography, and responsive regressions. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

The important distinction is not just the file type or tool name. Route here when the user is asking for visual difference list and the request depends on baseline/current screenshots or rendered states, and viewport or device context. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Routing notes

Use this when the input is screenshot evidence or expected/current visual states. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Baseline/current screenshots or rendered states | Visual difference list |
| Viewport or device context | Viewport-specific severity |
| Visual acceptance criteria | Screenshot anchors |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Workflow

A normal run is usually:

1. Compare layout, spacing, clipping, contrast, and text overflow.
2. Group issues by viewport and severity.
3. Avoid inferring runtime cause without evidence.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Baseline/current screenshots or rendered states", "Viewport or device context"]
  returns: ["Visual difference list", "Viewport-specific severity"]
  tools: ["Screenshot artifacts"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Deliverables

The handoff is usually a compact artifact rather than a long essay. Include visual difference list, viewport-specific severity, and screenshot anchors when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Visual difference list
- Viewport-specific severity
- Screenshot anchors

## Anti-patterns

Not for full browser test automation or DOM/network diagnosis unless screenshots point there. Nearby skills in this cluster include `psc-devtools-runtime-diagnoser`, `psc-playwright-regression-suite`, `psc-accessibility-interaction-auditor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Dependencies

This workflow can be carried out with screenshot artifacts. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Baseline/current screenshots or rendered states. Viewport or device context. Visual acceptance criteria.

## Usage examples

- Compare the old and new pricing-page screenshots and call out visible layout regressions, spacing changes, clipped content, and mobile text overflow.
- Do a visual regression review from screenshot pairs across desktop and mobile. I need layout differences and severity, not browser interaction debugging.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants visual difference list or a neighbouring artifact, then ask one clarifying question if needed.

## Quality bar

- The response clearly produces visual difference list.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
