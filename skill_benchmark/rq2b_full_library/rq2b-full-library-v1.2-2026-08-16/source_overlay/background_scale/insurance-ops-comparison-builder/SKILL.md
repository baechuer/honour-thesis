---
name: insurance-ops-comparison-builder
description: Compares multiple insurance claims operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Insurance Ops Comparison Builder

## Use when

- The user wants comparison across two or more insurance claims operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: claim form, policy wording, incident evidence, assessor notes.

## Dependencies and resources

- claim file
- policy document
- incident evidence
- coverage criteria
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
