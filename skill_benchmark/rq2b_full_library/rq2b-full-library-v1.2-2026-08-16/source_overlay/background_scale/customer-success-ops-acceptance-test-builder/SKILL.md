---
name: customer-success-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for customer success operations outputs against expected behavior and constraints.
---

# Customer Success Ops Acceptance Test Builder

## Use when

- The user wants testable checks for customer success operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: account health note, renewal plan, usage report, success plan.

## Dependencies and resources

- account profile
- usage data
- renewal date
- success criteria
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
