---
name: pr-reviewer
description: Reviews a GitHub pull request as a PR-level artifact, using the PR diff, changed files, discussion, and checks to identify review findings and merge risks.
---

# PR Reviewer

Reviews a pull request in its repository context.

## Use when

- The user asks for a PR review, pull request review, or review of a branch against a base branch.
- The task depends on PR-level context such as diff scope, changed files, discussion, commits, or checks.
- The output should read like a code review for maintainers.

## Not for

- Reviewing a local code snippet without PR context.
- Implementing reviewer-requested changes.
- Debugging a failing CI job in detail.
- Writing release notes or changelog entries.

## Preconditions

- The user provides code, a diff, PR context, CI output, review comments, or a completed-change summary.
- The requested artifact is clear: review findings, fixes, debugging notes, changelog text, or release notes.

## Workflow

1. Identify the PR scope, changed files, and intended behavior.
2. Inspect the diff and relevant surrounding code.
3. Consider tests, checks, migrations, compatibility, and user-facing behavior.
4. Prioritize correctness and regression findings over style.
5. Return PR review findings with concise evidence and residual risk.

## Output pattern

- PR review findings ordered by severity.
- Affected files or behavior.
- Test/check gaps.
- Merge risk summary.

## Writing rules

- Present findings first, ordered by severity.
- Include file or code references when available.
- Keep summaries brief and secondary to findings.
- If no issues are found, say that clearly and mention remaining test gaps.
