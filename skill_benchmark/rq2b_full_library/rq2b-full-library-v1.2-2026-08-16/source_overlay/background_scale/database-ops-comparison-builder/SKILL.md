---
name: database-ops-comparison-builder
description: Compares multiple database operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Database Ops Comparison Builder

## Use when

- The user wants comparison across two or more database operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: schema, migration file, query plan, data quality note.

## Dependencies and resources

- database schema
- migration file
- query plan
- data sample
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
