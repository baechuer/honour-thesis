---
name: geospatial-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for geospatial analysis operations outputs against expected behavior and constraints.
---

# Geospatial Ops Acceptance Test Builder

## Use when

- The user wants testable checks for geospatial analysis operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: map layer, coordinate table, spatial query, GIS project note.

## Dependencies and resources

- spatial data
- coordinate reference system
- map layers
- analysis boundary
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
