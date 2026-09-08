---
name: analytics-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for analytics and experimentation operations outputs against expected behavior and constraints.
---

# Analytics Ops Acceptance Test Builder

## Use when

- The user wants testable checks for analytics and experimentation operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
