---
name: retail-ops-timeline-builder
description: Builds a timeline for retail operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Retail Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from sales report, product catalog, store note, promotion plan.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: sales report, product catalog, store note, promotion plan.

## Dependencies and resources

- sales data
- store profile
- product catalog
- promotion calendar
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
