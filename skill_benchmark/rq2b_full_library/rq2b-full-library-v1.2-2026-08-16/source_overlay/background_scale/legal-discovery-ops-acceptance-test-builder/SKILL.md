---
name: legal-discovery-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for legal discovery operations outputs against expected behavior and constraints.
---

# Legal Discovery Ops Acceptance Test Builder

## Use when

- The user wants testable checks for legal discovery operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
