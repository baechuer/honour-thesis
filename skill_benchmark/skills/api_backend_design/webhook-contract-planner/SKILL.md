---
name: webhook-contract-planner
description: "Designs webhook receiver contracts with event selection, payload validation, signature verification, idempotency, retries, ordering, and dead-letter behavior."
---

# Webhook Contract Planner

Plans inbound event handling where external systems call back into the application.

## Use when

- The user asks how to receive, validate, process, or retry webhook events.
- The task includes signatures, event schemas, idempotency, ordering, or dead-letter handling.
- The output should be a webhook contract and processing plan.

## Not for

- General third-party API polling integration.
- OpenAPI endpoint documentation review.
- Database migration risk analysis.

## Preconditions

- Webhook provider docs, event examples, or expected event types are available.
- Receiver endpoint, persistence model, or processing goal is known.
- The user needs event reliability and security behavior specified.

## Workflow

1. Identify event types, payload shape, signature scheme, and delivery behavior.
2. Define receiver endpoint contract, validation, and auth checks.
3. Plan idempotency keys, retry behavior, ordering assumptions, and dead-letter handling.
4. Map events to internal state changes and audit records.
5. Return test cases for duplicate, delayed, invalid, and failed events.

## Writing rules

- Do not ignore duplicate or replay events.
- Keep provider guarantees separate from application assumptions.
- Include security verification for signatures or shared secrets.

## Default shape

- Event type
- Receiver contract
- Reliability behavior
- Security and test cases
