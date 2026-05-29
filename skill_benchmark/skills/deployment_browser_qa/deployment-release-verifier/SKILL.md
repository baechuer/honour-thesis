---
name: deployment-release-verifier
description: "Verifies a completed deployment through URL checks, smoke tests, environment sanity, asset loading, version evidence, and rollback readiness."
---

# Deployment Release Verifier

Checks whether a release is safely live after build/deploy completes.

## Use when

- The deployment appears successful and the user wants release verification.
- The task includes smoke tests, environment checks, version confirmation, or rollback readiness.
- The output should be a release verification checklist with evidence.

## Not for

- Diagnosing a failed build log.
- Performing a visual regression diff as the main task.
- Planning API integration architecture.

## Preconditions

- A deployed URL, environment, or release artifact is available.
- Expected smoke-test behavior and critical pages are known.
- The user wants readiness evidence, not implementation changes.

## Workflow

1. Confirm deployment URL, version, environment, and critical config.
2. Run smoke checks for key routes, assets, forms, auth boundaries, and console errors.
3. Check monitoring or logs for immediate failures.
4. Confirm rollback path or previous stable release reference.
5. Return pass/fail evidence and release risks.

## Writing rules

- Do not treat build success as release success.
- Record exact URLs, versions, or checks when available.
- Separate blocking release issues from follow-up improvements.

## Default shape

- Check
- Evidence
- Status
- Release risk or next action
