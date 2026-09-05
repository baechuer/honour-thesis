---
name: psc-devtools-runtime-diagnoser
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Diagnose broken web interactions using DOM state, console errors, network requests, screenshots, and runtime clues."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-browser-quality
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Devtools Runtime Diagnoser

## Capability

Diagnose broken web interactions using DOM state, console errors, network requests, screenshots, and runtime clues. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

The important distinction is not just the file type or tool name. Route here when the user is asking for reproduction trace and the request depends on a target page or flow, and symptom to reproduce. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use this when an interaction fails and browser evidence is needed to identify likely cause. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| A target page or flow | Reproduction trace |
| Symptom to reproduce | Evidence packet |
| Access to browser/runtime evidence | Likely cause |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Reproduce the interaction.
2. Collect console, network, DOM, and screenshot evidence.
3. Separate UI state, API, timing, and JavaScript failure hypotheses.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["A target page or flow", "Symptom to reproduce"]
  returns: ["Reproduction trace", "Evidence packet"]
  tools: ["Browser DevTools or equivalent runtime inspector"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include reproduction trace, evidence packet, likely cause, and verification step when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Reproduction trace
- Evidence packet
- Likely cause
- Verification step

## Boundaries

Not just screenshot capture, accessibility review, or a scripted regression suite. Nearby skills in this cluster include `psc-playwright-regression-suite`, `psc-visual-screenshot-reviewer`, `psc-accessibility-interaction-auditor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with browser devtools or equivalent runtime inspector. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: A target page or flow. Symptom to reproduce. Access to browser/runtime evidence.

## Samples

- The checkout Apply Coupon button stops responding after the first click. Reproduce the path and use browser evidence to explain whether it is DOM state, network, or JavaScript logic.
- Use Chrome DevTools-style evidence for the broken checkout interaction: console errors, network failures, DOM state, and screenshots. Do not only write Playwright assertions.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants reproduction trace or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces reproduction trace.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
