---
name: vendor-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for vendor and procurement review outputs against expected behavior and constraints.
---

# Vendor Ops Acceptance Test Builder

## Use when

- The user wants testable checks for vendor and procurement review deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: vendor proposal, security questionnaire, pricing sheet, contract summary.

## Dependencies and resources

- vendor profile
- pricing document
- security answers
- procurement criteria
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
