---
name: web-page-snapshotter
description: Opens or inspects a web page to capture its visible state, key screens, page content, screenshots, and basic rendering evidence without performing a full interaction test.
---

# Web Page Snapshotter

Captures the observable state of a web page.

## Use when

- The user wants to see what a page currently looks like or contains.
- The task is to capture screenshots, visible text, layout state, or page-level evidence.
- The output should document page state rather than test behavior or diagnose code.

## Not for

- Filling forms or completing a browser task.
- Running a structured UI test.
- Diagnosing the root cause of a frontend bug.
- Extracting a reusable structured dataset from the page.

## Preconditions

- The target page, route, or flow is available, described, or can be opened in a browser-like environment.
- The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.

## Workflow

1. Open or inspect the target page.
2. Capture visible state, key content, layout issues, and screenshots when relevant.
3. Note loading, authentication, or rendering problems that block observation.
4. Avoid changing user data or submitting forms unless explicitly requested.
5. Return a concise page-state report with evidence.

## Output pattern

- Page-state report.
- Key visible content or layout evidence.
- Screenshots or blockers when relevant.

## Writing rules

- Separate what was observed from what is inferred.
- Prefer concrete visible evidence over speculation.
- If screenshots are produced, describe what each one shows.
- Use `references/snapshot_evidence.md` when a structured evidence checklist is useful.
