---
name: visual-regression-checker
description: "Compares baseline and current screenshots across viewports to identify visual regressions, layout shifts, clipping, contrast changes, and unexpected differences."
---

# Visual Regression Checker

Detects visual changes between expected and current UI states.

## Use when

- The user has baseline and current screenshots or wants a visual diff check.
- The main concern is layout shift, clipping, text overflow, contrast, or responsive rendering.
- The output should classify visual differences and their severity.

## Not for

- Debugging why a button click fails.
- Running a deployment smoke test.
- Auditing slide decks or PDF documents.

## Preconditions

- Baseline and current screenshots, or a repeatable screenshot capture flow, are available.
- Relevant viewport sizes or pages are specified.
- Visual tolerance or acceptance criteria are known or can be stated.

## Workflow

1. Collect comparable screenshots for each target viewport or state.
2. Compare layout, text fit, image rendering, color, spacing, and clipping.
3. Filter expected content differences from regressions.
4. Rank issues by user impact and reproducibility.
5. Return evidence with viewport and page/state references.

## Writing rules

- Do not diagnose backend logic unless visual evidence supports it.
- Name the viewport or state for every finding.
- Separate cosmetic differences from usability regressions.

## Default shape

- Page or state
- Viewport
- Observed difference
- Severity and suggested fix
