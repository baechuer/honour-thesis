---
name: procurement-ops-comparison-builder
description: Compares multiple procurement operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Procurement Ops Comparison Builder

## Use when

- The user wants comparison across two or more procurement operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: purchase request, vendor quote, RFP response, approval note.

## Dependencies and resources

- purchase request
- vendor quote
- budget code
- approval policy
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
