---
name: psc-playwright-regression-suite
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Create or run Playwright interaction tests with navigation, form actions, assertions, screenshots, and reproducible failure output."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Playwright Regression Suite

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

## When to use

Use this when the desired artifact is an automated browser test or regression check.

## Requirements

- Target route or flow
- Expected behavior
- Assertions and test data

## Instructions

- Define the browser path.
- Add interactions and assertions.
- Capture screenshots or traces on failure.
- Return test code or test report.

## Deliverables

- Playwright test steps or code
- Expected/actual result
- Trace or screenshot evidence

## When not to use

Not for one-off visual review, manual DevTools debugging, or accessibility-only audits.

## External dependencies to preserve

- Playwright

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
