---
name: ml-ops-comparison-builder
description: Compares multiple machine learning operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Ml Ops Comparison Builder

## Use when

- The user wants comparison across two or more machine learning operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: model card, training log, evaluation table, dataset note.

## Dependencies and resources

- model artifact
- dataset split
- training config
- evaluation metric
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
