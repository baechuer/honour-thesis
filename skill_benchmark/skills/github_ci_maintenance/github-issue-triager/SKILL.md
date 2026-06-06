---
name: github-issue-triager
description: "Classifies GitHub issues by type, severity, reproducibility, ownership, labels, and missing information."
---

# Github Issue Triager

Sorts issue reports into actionable categories.

## Use when

- The user provides issue text or an issue queue.
- They need labels, priority, owner, or reproduction requests.

## Not for

- Addressing PR comments.
- Reviewing a code diff.
- Writing changelog notes.

## Preconditions

- Issue titles/bodies are available.
- Project labels or triage criteria are known or can be proposed.

## Workflow

1. Read issue symptoms and environment.
2. Assign type/severity/owner labels.
3. Identify missing reproduction details.
4. Return triage actions.

## Writing rules

- Do not assume root cause from vague symptoms.
- Ask for minimal reproduction when needed.

## Default shape

- Issue
- Labels
- Priority
- Missing info/action
