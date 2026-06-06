---
name: webhook-integration-planner
description: "Plans webhook event subscriptions, signature verification, idempotency keys, retries, ordering, and dead-letter handling."
---

# Webhook Integration Planner

Designs event callback behavior between systems.

## Use when

- The user receives or sends event callbacks.
- Retries, signatures, ordering, or idempotency are central.

## Not for

- Designing REST CRUD endpoints.
- Building an MCP server.
- Documenting an existing API only.

## Preconditions

- Event source and event types are known.
- Receiver behavior and failure handling matter.

## Workflow

1. Select events and payloads.
2. Define signature/idempotency validation.
3. Plan retries and ordering.
4. Return receiver contract and tests.

## Writing rules

- Do not ignore duplicate deliveries.
- State failure storage behavior.

## Default shape

- Events
- Validation
- Retry/idempotency
- Tests
