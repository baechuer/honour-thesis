---
name: supply-chain-ops-timeline-builder
description: Builds a timeline for supply chain operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Supply Chain Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from supplier update, demand forecast, inventory plan, risk note.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: supplier update, demand forecast, inventory plan, risk note.

## Dependencies and resources

- supplier list
- forecast data
- inventory position
- risk register
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
