---
name: frontend-debugger
description: Diagnoses broken frontend behavior using UI observations, console errors, network state, DOM clues, and relevant source code to identify the likely cause and fix.
---

# Frontend Debugger

Diagnoses frontend failures.

## Use when

- The user reports a broken UI, rendering issue, interaction bug, or browser-side error.
- The task requires connecting symptoms to likely source code, state, data, or network causes.
- The deliverable is a root-cause-and-patch explanation for browser-side implementation behavior.
- The output should explain the implementation cause and suggest or apply the smallest code fix.
- Console errors, failed handlers, broken state updates, and API/DOM mismatches are central evidence.

## Not for

- Running a pass/fail UI test without debugging.
- Filling a browser form for the user.
- Capturing page appearance only.
- Reviewing unrelated backend or repository code.

## Preconditions

- The target page, route, or flow is available, described, or can be opened in a browser-like environment.
- The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.

## Workflow

1. Reproduce or inspect the visible symptom.
2. Check console errors, network failures, DOM state, and recent source changes when available.
3. Separate user-facing symptom from likely implementation cause.
4. Propose or apply the smallest fix.
5. Verify the behavior with the relevant browser or test check when possible.

## Output pattern

- Observed symptom.
- Evidence from UI, console, network, DOM, or code.
- Likely cause.
- Smallest fix and verification.

## Writing rules

- Distinguish confirmed evidence from likely causes.
- Prefer targeted fixes over broad UI rewrites.
- Mention what was verified and what remains uncertain.
- Use `references/frontend_debug_axes.md` for common diagnosis categories.
