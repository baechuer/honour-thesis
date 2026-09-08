---
name: email-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for email and messaging operations outputs against expected behavior and constraints.
---

# Email Ops Acceptance Test Builder

## Use when

- The user wants testable checks for email and messaging operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: draft email, message thread, recipient context, tone constraints.

## Dependencies and resources

- message thread
- recipient relationship
- tone target
- requested action
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
