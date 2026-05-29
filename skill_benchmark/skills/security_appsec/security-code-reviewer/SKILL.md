---
name: security-code-reviewer
description: Reviews source code or diffs for concrete security vulnerabilities such as injection, authorization bypass, unsafe parsing, insecure defaults, and sensitive-data exposure.
---

# Security Code Reviewer

Reviews code for security vulnerabilities.

## Use when

- The user wants a security-focused code review of implementation or diffs.
- The task involves concrete code paths, input handling, permissions, validation, storage, redirects, parsing, or outputs.
- The artifact is a specific function, handler, diff, or source-code path, including cases where auth checks appear inside that code.
- The user wants code-level vulnerabilities and fixes tied to implementation behavior.
- The output should identify vulnerabilities and fixes at code level.

## Not for

- Building an architecture-level threat model without code.
- Pre-implementation reasoning across protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk.
- Protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk as a general design exercise.
- Auditing dependency versions or supply-chain posture as the main task.
- Looking only for leaked secrets.
- Reviewing ordinary correctness bugs without security impact.

## Preconditions

- The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.
- The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.

## Workflow

1. Identify security-relevant entry points, trust boundaries, and sensitive operations in the code.
2. Check authorization, authentication, validation, escaping, parsing, error handling, and sensitive data handling.
3. Trace realistic exploit paths rather than listing generic issues.
4. Prioritize findings by impact and likelihood.
5. Recommend focused fixes and verification.

## Output pattern

- Concrete security findings tied to code behavior.
- Exploit path or impact.
- Focused fix and verification suggestion.

## Writing rules

- Tie each finding to code behavior.
- Avoid speculative vulnerabilities without a plausible path.
- Separate security findings from ordinary code quality concerns.
- State when no concrete vulnerability is evident from the supplied code.
