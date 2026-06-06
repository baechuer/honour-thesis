---
name: psc-accessibility-interaction-auditor
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Audit web interactions for keyboard access, focus order, labels, ARIA state, contrast, and screen-reader usability."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Accessibility Interaction Auditor

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

## When to use

Use this when the success criterion is accessibility rather than visual polish or generic UI behavior.

## Requirements

- Target component or flow
- Interaction states
- Accessibility criteria such as WCAG or keyboard/screen-reader checks

## Instructions

- Check labels, roles, focus behavior, keyboard path, contrast, and error announcement.
- Separate blocker, serious, and minor issues.
- Return remediation steps.

## Deliverables

- Accessibility findings
- Affected element/state
- Severity
- Recommended fix

## When not to use

Not for only screenshot comparison, generic UI testing, or performance profiling.

## External dependencies to preserve

- Browser accessibility tree or manual keyboard inspection

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
