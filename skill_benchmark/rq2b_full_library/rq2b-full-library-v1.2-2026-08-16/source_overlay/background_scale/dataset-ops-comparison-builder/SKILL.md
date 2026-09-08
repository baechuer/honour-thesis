---
name: dataset-ops-comparison-builder
description: Compares multiple dataset and analytics preparation items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Dataset Ops Comparison Builder

## Use when

- The user wants comparison across two or more dataset and analytics preparation sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
