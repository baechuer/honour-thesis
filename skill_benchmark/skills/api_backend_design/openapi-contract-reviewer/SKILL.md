---
name: openapi-contract-reviewer
description: "Reviews OpenAPI or endpoint contracts for schema correctness, status codes, auth behavior, examples, error models, pagination, and client compatibility."
---

# OpenAPI Contract Reviewer

Audits an API contract as a client-facing specification.

## Use when

- The user provides an OpenAPI spec, endpoint documentation, or API contract.
- The task is to find contract ambiguity, schema mismatch, or client integration risk.
- The output should be contract findings tied to endpoints and fields.

## Not for

- Planning a third-party API integration from scratch.
- Designing webhook processing and retry behavior.
- Reviewing high-level service architecture boundaries.

## Preconditions

- Endpoint paths, schemas, status codes, examples, or auth rules are available.
- The user wants contract quality, not implementation debugging.
- Client compatibility or API behavior expectations are known enough to assess.

## Workflow

1. Identify endpoints, schemas, examples, status codes, and auth requirements.
2. Check request/response schema consistency and missing examples.
3. Review error behavior, pagination, filtering, versioning, and backward compatibility.
4. Flag ambiguous or unsafe contract assumptions for clients.
5. Return endpoint-level findings with recommended contract changes.

## Writing rules

- Cite endpoint paths, fields, or status codes when possible.
- Do not redesign service architecture unless contract behavior requires it.
- Separate breaking contract issues from documentation polish.

## Default shape

- Endpoint or schema
- Contract issue
- Client impact
- Recommended change
