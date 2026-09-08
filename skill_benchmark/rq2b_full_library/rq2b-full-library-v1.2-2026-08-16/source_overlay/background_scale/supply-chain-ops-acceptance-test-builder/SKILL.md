---
name: supply-chain-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for supply chain operations outputs against expected behavior and constraints.
---

# Supply Chain Ops Acceptance Test Builder

## Use when

- The user wants testable checks for supply chain operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: supplier update, demand forecast, inventory plan, risk note.

## Dependencies and resources

- supplier list
- forecast data
- inventory position
- risk register
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
