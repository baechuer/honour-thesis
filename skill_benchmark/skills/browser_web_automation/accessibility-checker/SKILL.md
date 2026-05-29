---
name: accessibility-checker
description: Checks a web interface for accessibility issues such as missing labels, keyboard traps, focus order problems, semantic roles, contrast, and screen-reader usability.
---

# Accessibility Checker

Reviews a web UI for accessibility problems.

## Use when

- The user wants accessibility, a11y, keyboard, screen-reader, focus, label, role, or contrast checks.
- The task is to assess whether the interface is usable beyond visual mouse interaction.
- The output should identify accessibility issues and practical fixes.

## Not for

- General UI testing without accessibility criteria.
- Filling forms as the user.
- Capturing screenshots only.
- Debugging non-accessibility frontend bugs as the main task.

## Preconditions

- The target page, route, or flow is available, described, or can be opened in a browser-like environment.
- The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.

## Workflow

1. Identify the target page, component, or flow.
2. Check labels, roles, focus order, keyboard operation, visible focus, and semantic structure.
3. Check contrast and text alternatives when relevant.
4. Separate severe blockers from improvements.
5. Return accessibility findings with suggested fixes.

## Output pattern

- Accessibility findings grouped by severity.
- Affected element or interaction.
- Suggested fix or verification step.

## Writing rules

- Prioritize issues that block use.
- Tie findings to observable UI elements.
- Avoid vague "make it accessible" advice.
- Use `references/accessibility_checks.md` when a checklist is useful.
