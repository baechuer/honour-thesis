---
name: search-ops-comparison-builder
description: Compares multiple search and retrieval operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Search Ops Comparison Builder

## Use when

- The user wants comparison across two or more search and retrieval operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
