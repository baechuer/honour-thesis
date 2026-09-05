---
name: psc-playwright-regression-suite
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Create or run Playwright interaction tests with navigation, form actions, assertions, screenshots, and reproducible failure output."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-browser-quality
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Playwright Regression Suite

## About

Create or run Playwright interaction tests with navigation, form actions, assertions, screenshots, and reproducible failure output. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

The important distinction is not just the file type or tool name. Route here when the user is asking for playwright test steps or code and the request depends on target route or flow, and expected behavior. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Use it for

Use this when the desired artifact is an automated browser test or regression check. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Target route or flow | Playwright test steps or code |
| Expected behavior | Expected/actual result |
| Assertions and test data | Trace or screenshot evidence |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Process

A normal run is usually:

1. Define the browser path.
2. Add interactions and assertions.
3. Capture screenshots or traces on failure.
4. Return test code or test report.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Target route or flow", "Expected behavior"]
  returns: ["Playwright test steps or code", "Expected/actual result"]
  tools: ["Playwright"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Expected artifacts

The handoff is usually a compact artifact rather than a long essay. Include playwright test steps or code, expected/actual result, and trace or screenshot evidence when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Playwright test steps or code
- Expected/actual result
- Trace or screenshot evidence

## Do not use for

Not for one-off visual review, manual DevTools debugging, or accessibility-only audits. Nearby skills in this cluster include `psc-devtools-runtime-diagnoser`, `psc-visual-screenshot-reviewer`, `psc-accessibility-interaction-auditor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Runtime assumptions

This workflow can be carried out with playwright. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Target route or flow. Expected behavior. Assertions and test data.

## Examples

- Build a repeatable browser regression check for the checkout form: navigate, fill fields, apply the coupon, assert the discount message, and capture failure evidence.
- Write a Playwright test for the checkout coupon flow with assertions and screenshots. I need reusable regression coverage, not just a manual DevTools diagnosis.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants playwright test steps or code or a neighbouring artifact, then ask one clarifying question if needed.

## Acceptance

- The response clearly produces playwright test steps or code.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
