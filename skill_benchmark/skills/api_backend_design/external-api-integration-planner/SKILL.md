---
name: external-api-integration-planner
description: "Plans integration with an external API by mapping authentication, endpoints, payload transformations, rate limits, retries, pagination, and failure handling."
---

# External API Integration Planner

Turns external API documentation into an implementation plan.

## Use when

- The user wants to connect to a third-party or external API.
- The task includes auth, endpoints, payload mapping, rate limits, retries, or pagination.
- The output should be an integration plan rather than a contract review.

## Not for

- Reviewing an already-authored OpenAPI contract for quality.
- Designing webhook receiver semantics only.
- Mapping internal service dependencies without a specific external API.

## Preconditions

- External API docs, endpoint examples, auth method, or provider constraints are available.
- The desired product workflow or data mapping is known.
- Failure handling and rate-limit concerns are relevant.

## Workflow

1. Identify auth method, endpoints, payloads, pagination, and provider limits.
2. Map user workflow data to API request and response shapes.
3. Plan retries, idempotency, caching, error handling, and observability.
4. List secrets, environment variables, and permission requirements.
5. Return implementation sequence and verification cases.

## Writing rules

- Do not assume provider behavior absent from docs.
- Separate required calls from optional enhancements.
- Include failure and rate-limit behavior explicitly.

## Default shape

- Integration goal
- Endpoint and auth plan
- Data mapping
- Failure handling and tests
