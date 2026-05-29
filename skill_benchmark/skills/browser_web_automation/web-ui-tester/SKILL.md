---
name: web-ui-tester
description: Tests web UI behavior by exercising interactions, checking expected outcomes, catching regressions, and reporting whether user-facing flows work correctly.
---

# Web UI Tester

Tests user-facing web interactions.

## Use when

- The user wants to verify that a web flow, component, or interaction works.
- The task involves expected behavior, regression checking, console errors, navigation, or state changes.
- The output should be a test result with pass/fail observations and reproduction steps.

## Not for

- Filling a real form as the user's delegate.
- Capturing page appearance only.
- Finding the source-level root cause or patch for a frontend implementation bug.
- Diagnosing the underlying code cause as the primary task.
- Extracting page data for reuse.

## Preconditions

- The target page, route, or flow is available, described, or can be opened in a browser-like environment.
- The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.

## Workflow

1. Identify the target behavior and expected result.
2. Exercise the relevant UI path with safe test inputs.
3. Observe rendered state, validation behavior, navigation, console/network errors, and persistence.
4. Compare actual behavior with expected behavior.
5. Report pass/fail status, reproduction steps, and evidence.

## Output pattern

- Tested behavior.
- Expected versus actual result.
- Pass/fail/blocked status.
- Reproduction steps and evidence.

## Writing rules

- Keep testing separate from root-cause debugging unless asked.
- Use safe dummy data for tests.
- Do not submit real purchases, messages, or destructive actions.
- Use `references/ui_test_report.md` for report structure when needed.
