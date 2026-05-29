---
name: ci-failure-debugger
description: Investigates failing CI checks, test logs, build errors, or workflow failures and identifies the smallest fix needed to make the run pass.
---

# CI Failure Debugger

Diagnoses and fixes continuous integration failures.

## Use when

- The user reports a failing CI check, test suite, build, lint run, or GitHub Actions workflow.
- The task depends on logs, failure output, environment differences, or test commands.
- The output should explain the failure cause and the fix.

## Not for

- Reviewing code for possible issues without an actual failing check.
- Addressing general PR review comments unrelated to CI.
- Writing release notes or changelog prose.
- Creating a new test plan without failure evidence.

## Preconditions

- The user provides code, a diff, PR context, CI output, review comments, or a completed-change summary.
- The requested artifact is clear: review findings, fixes, debugging notes, changelog text, or release notes.

## Workflow

1. Locate the failing command, job, test, or workflow step.
2. Read the first meaningful error and any nearby context.
3. Reproduce or reason about the failure mode.
4. Identify whether the cause is code, test expectation, dependency, configuration, or environment.
5. Apply or propose the smallest fix and verify the relevant command when possible.

## Output pattern

- Failing command or job.
- First meaningful error.
- Likely root cause.
- Minimal fix and verification command.

## Writing rules

- Distinguish symptom from root cause.
- Prefer targeted fixes over broad rewrites.
- Mention any verification that was run or could not be run.
- If useful, consult `references/ci_failure_signals.md` for common failure categories.
