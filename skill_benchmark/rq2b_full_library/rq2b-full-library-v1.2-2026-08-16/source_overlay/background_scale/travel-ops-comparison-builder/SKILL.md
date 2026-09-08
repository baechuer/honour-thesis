---
name: travel-ops-comparison-builder
description: Compares multiple travel planning operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Travel Ops Comparison Builder

## Use when

- The user wants comparison across two or more travel planning operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: itinerary, booking email, visa note, travel constraint list.

## Dependencies and resources

- destination
- dates
- booking details
- traveler constraints
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
