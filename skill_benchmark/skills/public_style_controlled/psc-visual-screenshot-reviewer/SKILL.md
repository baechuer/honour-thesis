---
name: psc-visual-screenshot-reviewer
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Compare page screenshots or visual states for layout shifts, clipping, spacing, typography, and responsive regressions."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Visual Screenshot Reviewer

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

## When to use

Use this when the input is screenshot evidence or expected/current visual states.

## Requirements

- Baseline/current screenshots or rendered states
- Viewport or device context
- Visual acceptance criteria

## Instructions

- Compare layout, spacing, clipping, contrast, and text overflow.
- Group issues by viewport and severity.
- Avoid inferring runtime cause without evidence.

## Deliverables

- Visual difference list
- Viewport-specific severity
- Screenshot anchors

## When not to use

Not for full browser test automation or DOM/network diagnosis unless screenshots point there.

## External dependencies to preserve

- Screenshot artifacts

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
