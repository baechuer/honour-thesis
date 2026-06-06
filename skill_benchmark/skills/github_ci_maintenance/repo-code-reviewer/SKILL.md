---
name: repo-code-reviewer
description: "Reviews a repository diff for bugs, regressions, maintainability risks, missing tests, and behavioral concerns."
---

# Repo Code Reviewer

Performs fresh code review on a change.

## Use when

- The user provides a diff, branch, or changed files.
- They want findings ordered by severity.

## Not for

- Resolving existing review comments.
- Debugging CI logs only.
- Generating release notes.

## Preconditions

- A diff or changed files are available.
- The user expects review findings, not implementation.

## Workflow

1. Inspect changed behavior.
2. Identify bugs and missing tests.
3. Prioritize findings by severity.
4. Return concise review comments.

## Writing rules

- Lead with findings.
- Avoid style-only comments unless they hide risk.

## Default shape

- Finding
- File/evidence
- Risk
- Suggested test/fix
