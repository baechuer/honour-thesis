---
name: travel-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for travel planning operations outputs against expected behavior and constraints.
---

# Travel Ops Acceptance Test Builder

## Use when

- The user wants testable checks for travel planning operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: itinerary, booking email, visa note, travel constraint list.

## Dependencies and resources

- destination
- dates
- booking details
- traveler constraints
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
