---
name: release-changelog-generator
description: "Generates release notes or changelog entries from commits, pull requests, categories, and breaking-change markers."
---

# Release Changelog Generator

Summarizes shipped changes for users or developers.

## Use when

- The user provides commits, PR titles, or version changes.
- The output should be a changelog or release note.

## Not for

- Debugging CI.
- Triage of issues.
- Reviewing code for defects.

## Preconditions

- Commit/PR list and target audience are available.
- Release categories are known or inferable.

## Workflow

1. Group changes by category.
2. Identify breaking changes and migrations.
3. Write concise notes.
4. List verification or upgrade caveats.

## Writing rules

- Do not include internal noise unless relevant.
- Mark breaking changes clearly.

## Default shape

- Highlights
- Fixes
- Breaking changes
- Upgrade notes
