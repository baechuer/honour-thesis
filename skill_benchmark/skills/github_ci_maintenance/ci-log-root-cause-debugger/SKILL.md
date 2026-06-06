---
name: ci-log-root-cause-debugger
description: "Diagnoses CI failures from logs, failing commands, environment assumptions, and dependency or test errors."
---

# Ci Log Root Cause Debugger

Finds the first meaningful CI failure and a minimal verification path.

## Use when

- The user provides CI logs or failing check output.
- The output should identify root cause and fix sequence.

## Not for

- Reviewing code quality generally.
- Writing release notes.
- Triage of user issues without CI evidence.

## Preconditions

- CI logs, job name, or failing command are available.
- The user wants diagnosis rather than broad repository maintenance.

## Workflow

1. Find the first meaningful error.
2. Map it to test, dependency, environment, or build cause.
3. Propose smallest fix.
4. Give rerun checks.

## Writing rules

- Do not chase cascading errors first.
- Quote log evidence.

## Default shape

- Failing job
- Root cause
- Evidence
- Fix and rerun
