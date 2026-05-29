---
name: changelog-writer
description: Converts completed technical changes into concise changelog entries organized by change type, scope, and user-visible or developer-visible impact.
---

# Changelog Writer

Writes changelog-style summaries from completed changes.

## Use when

- The user wants a changelog entry or release-history style summary.
- The input is a set of commits, diffs, merged changes, or implementation notes.
- The output should be concise, structured change bullets.

## Not for

- Reviewing code for bugs.
- Debugging a failing CI run.
- Writing marketing-style release notes.
- Writing a commit message for one small change.

## Preconditions

- The user provides code, a diff, PR context, CI output, review comments, or a completed-change summary.
- The requested artifact is clear: review findings, fixes, debugging notes, changelog text, or release notes.

## Workflow

1. Identify the completed changes and affected areas.
2. Separate user-facing changes, fixes, internal improvements, and breaking changes.
3. Remove implementation noise that does not matter to changelog readers.
4. Write concise bullets in a stable changelog structure.
5. Preserve uncertainty when the input does not establish impact.

## Output pattern

- Changelog bullets grouped by change type.
- User-facing or developer-facing impact.
- Breaking changes or caveats when supported.

## Writing rules

- Use past-tense or release-note style consistently.
- Prefer concrete impact over vague improvement language.
- Do not invent features or fixes not supported by the input.
- Keep entries compact and scannable.
