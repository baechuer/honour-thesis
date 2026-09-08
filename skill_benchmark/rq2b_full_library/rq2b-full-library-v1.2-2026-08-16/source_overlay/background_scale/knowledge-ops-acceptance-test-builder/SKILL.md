---
name: knowledge-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for knowledge management operations outputs against expected behavior and constraints.
---

# Knowledge Ops Acceptance Test Builder

## Use when

- The user wants testable checks for knowledge management operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: notes, wiki pages, knowledge base articles, taxonomy.

## Dependencies and resources

- note corpus
- taxonomy
- source links
- owner context
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
