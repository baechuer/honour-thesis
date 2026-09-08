---
name: support-ops-comparison-builder
description: Compares multiple customer support operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Support Ops Comparison Builder

## Use when

- The user wants comparison across two or more customer support operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
