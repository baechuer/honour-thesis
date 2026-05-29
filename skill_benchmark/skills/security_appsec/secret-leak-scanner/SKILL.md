---
name: secret-leak-scanner
description: Inspects files, diffs, logs, or configuration snippets for exposed secrets, tokens, keys, credentials, connection strings, and unsafe sensitive values.
---

# Secret Leak Scanner

Checks for exposed secrets and sensitive values.

## Use when

- The user wants to know whether a diff, repository, log, or config contains leaked credentials.
- The task focuses on tokens, keys, passwords, private URLs, connection strings, cookies, or `.env` values.
- The output should identify possible exposures and remediation steps.

## Not for

- General dependency risk assessment.
- Architecture-level threat modeling.
- Security review of logic unrelated to secret exposure.
- Privacy review of ordinary data handling.

## Preconditions

- The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.
- The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.

## Workflow

1. Inspect supplied files, diffs, logs, or config snippets for secret-like values.
2. Distinguish likely real secrets from placeholders and test fixtures.
3. Identify exposure path and likely blast radius when possible.
4. Recommend rotation, removal, history cleanup, and safer config handling.
5. Return findings without reproducing full sensitive values.

## Output pattern

- Potential secret exposures with values redacted.
- Likely source and blast radius.
- Rotation, removal, and history-cleanup recommendations.

## Writing rules

- Redact secret values in outputs.
- Treat uncertain high-entropy credentials conservatively.
- Do not validate a secret by using it.
- Prioritize rotation when a real secret may have been exposed.
