---
name: dataset-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for dataset and analytics preparation outputs against expected behavior and constraints.
---

# Dataset Ops Acceptance Test Builder

## Use when

- The user wants testable checks for dataset and analytics preparation deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
