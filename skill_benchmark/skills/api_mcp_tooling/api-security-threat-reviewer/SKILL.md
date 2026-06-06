---
name: api-security-threat-reviewer
description: "Reviews API designs for authentication, authorization, input validation, rate limiting, data exposure, and abuse cases."
---

# Api Security Threat Reviewer

Threat-models an API rather than documenting or designing it.

## Use when

- The user asks about API security risks.
- Authz, validation, rate limits, abuse, or sensitive data exposure are central.

## Not for

- Writing developer docs.
- Building MCP tools.
- Creating a normal REST contract without security focus.

## Preconditions

- API endpoints, data classes, or architecture are known.
- Security review is the requested outcome.

## Workflow

1. Identify assets, actors, and trust boundaries.
2. Check authn/authz and validation risks.
3. Assess abuse/rate-limit/data-exposure issues.
4. Return prioritized mitigations.

## Writing rules

- Do not provide only generic security advice.
- Tie each risk to endpoint or data exposure.

## Default shape

- Risk
- Affected endpoint/data
- Impact
- Mitigation
