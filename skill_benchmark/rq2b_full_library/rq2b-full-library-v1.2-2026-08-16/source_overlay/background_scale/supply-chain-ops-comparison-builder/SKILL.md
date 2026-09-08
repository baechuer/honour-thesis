---
name: supply-chain-ops-comparison-builder
description: Compares multiple supply chain operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Supply Chain Ops Comparison Builder

## Use when

- The user wants comparison across two or more supply chain operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: supplier update, demand forecast, inventory plan, risk note.

## Dependencies and resources

- supplier list
- forecast data
- inventory position
- risk register
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
