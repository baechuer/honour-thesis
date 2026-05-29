---
name: auth-flow-reviewer
description: Reviews authentication, authorization, sessions, permissions, password reset, token refresh, and account-access flows for security and correctness risks.
---

# Auth Flow Reviewer

Reviews login, session, and permission flows.

## Use when

- The user asks whether an auth, login, permission, role, token, session, or password-reset flow is safe.
- The task focuses on access control behavior rather than all security risks.
- The artifact is a flow, design, or end-to-end access-control path rather than one isolated handler bug.
- The output should identify auth-specific failure modes and tests.

## Not for

- General code review without auth implications.
- Single-function or handler-level security review where redirects, parsing, validation, or implementation bugs are the main concern.
- Reviewing one API handler for concrete code-level security vulnerabilities, open redirects, unsafe validation, incorrect access checks, and implementation fixes.
- Broad pre-implementation misuse analysis across protected assets, external actors, component boundaries, abuse scenarios, mitigations, and residual risk.
- Protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk as a general design exercise.
- Broad architecture threat modeling unrelated to access control.
- Dependency or package audits.
- Privacy review as the main task.

## Preconditions

- The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.
- The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.

## Workflow

1. Identify actors, roles, protected resources, tokens, and session boundaries.
2. Check authentication, authorization, token expiry, refresh, logout, reset, and privilege transitions.
3. Look for bypasses, confused-deputy cases, stale permissions, and insecure defaults.
4. Recommend tests or mitigations for the riskiest flows.
5. Return auth-focused findings and open questions.

## Output pattern

- Auth-flow findings.
- Bypass or privilege-escalation scenarios.
- Tests or mitigations for risky access-control behavior.

## Writing rules

- Keep the analysis centered on access control.
- Distinguish authentication from authorization.
- Include realistic misuse or bypass scenarios.
- Use `references/auth_review_axes.md` when a structured checklist is useful.
