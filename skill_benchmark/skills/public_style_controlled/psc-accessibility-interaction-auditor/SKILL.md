---
name: psc-accessibility-interaction-auditor
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Audit web interactions for keyboard access, focus order, labels, ARIA state, contrast, and screen-reader usability."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-browser-quality
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Accessibility Interaction Auditor

## Capability

Audit web interactions for keyboard access, focus order, labels, ARIA state, contrast, and screen-reader usability. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

The important distinction is not just the file type or tool name. Route here when the user is asking for accessibility findings and the request depends on target component or flow, and interaction states. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use this when the success criterion is accessibility rather than visual polish or generic UI behavior. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Target component or flow | Accessibility findings |
| Interaction states | Affected element/state |
| Accessibility criteria such as WCAG or keyboard/screen-reader checks | Severity |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Check labels, roles, focus behavior, keyboard path, contrast, and error announcement.
2. Separate blocker, serious, and minor issues.
3. Return remediation steps.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Target component or flow", "Interaction states"]
  returns: ["Accessibility findings", "Affected element/state"]
  tools: ["Browser accessibility tree or manual keyboard inspection"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include accessibility findings, affected element/state, severity, and recommended fix when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Accessibility findings
- Affected element/state
- Severity
- Recommended fix

## Boundaries

Not for only screenshot comparison, generic UI testing, or performance profiling. Nearby skills in this cluster include `psc-devtools-runtime-diagnoser`, `psc-playwright-regression-suite`, `psc-visual-screenshot-reviewer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with browser accessibility tree or manual keyboard inspection. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Target component or flow. Interaction states. Accessibility criteria such as WCAG or keyboard/screen-reader checks.

## Samples

- Audit the account settings modal for keyboard navigation, focus trapping, labels, contrast, and whether form errors are announced clearly.
- Review this web form specifically for accessibility interaction quality: keyboard path, accessible names, ARIA state, focus order, and screen-reader error feedback.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants accessibility findings or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces accessibility findings.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
