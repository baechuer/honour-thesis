---
name: web-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for web automation and QA outputs against expected behavior and constraints.
---

# Web Ops Acceptance Test Builder

## Use when

- The user wants testable checks for web automation and QA deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: web page, browser state, test flow, screenshot evidence.

## Dependencies and resources

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
