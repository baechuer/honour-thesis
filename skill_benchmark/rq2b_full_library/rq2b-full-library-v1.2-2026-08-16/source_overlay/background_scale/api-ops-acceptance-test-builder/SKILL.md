---
name: api-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for API integration operations outputs against expected behavior and constraints.
---

# Api Ops Acceptance Test Builder

## Use when

- The user wants testable checks for API integration operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: API spec, endpoint docs, integration error, webhook payload.

## Dependencies and resources

- API documentation
- auth method
- payload example
- rate limits
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
