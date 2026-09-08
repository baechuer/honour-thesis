---
name: ecommerce-ops-comparison-builder
description: Compares multiple ecommerce operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Ecommerce Ops Comparison Builder

## Use when

- The user wants comparison across two or more ecommerce operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: order export, product listing, refund note, marketplace report.

## Dependencies and resources

- order data
- product catalog
- marketplace rules
- customer message
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
