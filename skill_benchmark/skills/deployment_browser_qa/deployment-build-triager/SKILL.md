---
name: deployment-build-triager
description: "Diagnoses build or deployment failures from logs, environment variables, dependency versions, package scripts, and hosting-platform error context."
---

# Deployment Build Triager

Finds why a deployment failed before the app can be verified in production.

## Use when

- The user provides build logs, CI deploy logs, hosting errors, or package-script output.
- The task is to identify failure cause and remediation steps.
- The output should separate environment, dependency, build, and platform issues.

## Not for

- Verifying a deployed URL after build success.
- Debugging an in-browser UI interaction.
- Reviewing API design quality.

## Preconditions

- Build or deployment logs are available.
- The target platform, build command, and relevant environment are known or inferable.
- The user wants diagnosis rather than a polished release announcement.

## Workflow

1. Identify the failing stage and first meaningful error.
2. Map errors to build scripts, dependencies, runtime versions, or platform settings.
3. Check environment variable and configuration assumptions.
4. Propose the smallest fix and a rerun/verification sequence.
5. List residual risks if logs are incomplete.

## Writing rules

- Do not chase later cascading errors before the first root error.
- Keep commands and config changes explicit.
- Call out missing logs or environment context.

## Default shape

- Failing stage
- Likely root cause
- Evidence from logs
- Fix and rerun check
