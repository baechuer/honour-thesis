---
name: playwright-flow-debugger
description: "Reproduces a broken browser interaction flow with Playwright-style steps, selectors, console/network evidence, screenshots, and a failure hypothesis."
---

# Playwright Flow Debugger

Debugs an interactive web flow through browser automation evidence.

## Use when

- The user reports a broken UI flow, flaky interaction, selector failure, or unexpected browser state.
- The task needs reproduction steps, screenshots, console logs, or network evidence.
- The output should explain why the interaction fails and how to fix or verify it.

## Not for

- Comparing visual screenshots without an interaction failure.
- Checking deployment health after a successful build.
- Reviewing backend API contract design.

## Preconditions

- A target URL, local app, or browser reproduction path is available.
- The failing interaction, expected outcome, and observed behavior are known.
- Browser automation or equivalent evidence can be collected.

## Workflow

1. Open the target flow in a controlled browser session.
2. Reproduce the interaction with stable selectors and state notes.
3. Capture console, network, screenshot, and DOM evidence around the failure.
4. Identify whether the issue is selector, state, timing, data, accessibility, or app logic.
5. Propose a fix and a verification path.

## Writing rules

- Separate observed evidence from hypotheses.
- Prefer stable selectors and reproducible steps.
- Do not present visual preference feedback as a functional failure.

## Default shape

- Reproduction steps
- Evidence captured
- Failure hypothesis
- Fix or verification
