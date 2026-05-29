---
name: release-note-writer
description: Turns completed product or engineering changes into user-facing release notes that explain what changed, why it matters, and any action users should take.
---

# Release Note Writer

Writes user-facing release notes.

## Use when

- The user wants release notes, announcement copy, or user-facing update text.
- The task is to communicate completed changes to users or stakeholders.
- The output should explain impact rather than list implementation details.

## Not for

- Writing an internal changelog organized mainly for developers.
- Reviewing code or pull requests.
- Debugging CI failures.
- Implementing release changes.

## Preconditions

- The user provides code, a diff, PR context, CI output, review comments, or a completed-change summary.
- The requested artifact is clear: review findings, fixes, debugging notes, changelog text, or release notes.

## Workflow

1. Identify the audience and the completed changes.
2. Translate technical changes into user-visible impact.
3. Note required user action, migration steps, or compatibility warnings when relevant.
4. Keep implementation detail only when it helps users understand impact.
5. Return release-note text in a readable structure.

## Output pattern

- User-facing release note sections.
- What changed and why it matters.
- Required user action or caveat when relevant.

## Writing rules

- Use clear user-facing language.
- Do not overstate benefits beyond the evidence.
- Keep operational caveats visible.
- Separate major changes, fixes, and notes when useful.
