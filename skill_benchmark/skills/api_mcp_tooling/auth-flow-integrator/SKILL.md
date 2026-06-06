---
name: auth-flow-integrator
description: "Integrates OAuth, API keys, sessions, token refresh, scopes, secret storage, and authorization checks into an application flow."
---

# Auth Flow Integrator

Focuses on authentication and authorization mechanics.

## Use when

- The user asks about OAuth, API keys, sessions, scopes, or token refresh.
- Secrets and permission boundaries matter.

## Not for

- Planning generic webhook retries.
- Writing API documentation.
- Building MCP tools.

## Preconditions

- Provider/auth method and app flow are known.
- Security and token handling are relevant.

## Workflow

1. Map auth actors and token lifecycle.
2. Define scopes, storage, refresh, and revocation.
3. Identify authorization checks.
4. Return integration and test plan.

## Writing rules

- Do not put secrets in client-side storage.
- Separate authentication from authorization.

## Default shape

- Auth flow
- Token/scopes
- Storage/security
- Tests
