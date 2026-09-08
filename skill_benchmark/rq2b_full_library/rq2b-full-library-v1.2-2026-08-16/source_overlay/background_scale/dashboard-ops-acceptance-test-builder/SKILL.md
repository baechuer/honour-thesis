---
name: dashboard-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for dashboard and metric reporting outputs against expected behavior and constraints.
---

# Dashboard Ops Acceptance Test Builder

## Use when

- The user wants testable checks for dashboard and metric reporting deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: dashboard screenshots, metric tables, alert notes, KPI definitions.

## Dependencies and resources

- dashboard export
- metric glossary
- time window
- owner notes
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
