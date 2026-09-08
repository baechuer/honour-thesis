---
name: docs-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for document operations outputs against expected behavior and constraints.
---

# Docs Ops Acceptance Test Builder

## Use when

- The user wants testable checks for document operations deliverables or workflows.

## Input and preconditions

- Success criteria, expected artifact shape, or user acceptance conditions are available.
- Relevant material: PDF, DOCX, Markdown file, policy draft, extracted text.

## Dependencies and resources

- document file
- layout evidence
- source text
- format target
- task-specific constraints

## Procedure

1. Translate stated behaviour and constraints into observable acceptance conditions.
2. Define representative, edge-case, and failure inputs.
3. State expected outcomes and verification evidence for each case.
4. Return the acceptance-test set.

## Output

Acceptance tests with inputs, expected results, edge cases, and verification notes.
