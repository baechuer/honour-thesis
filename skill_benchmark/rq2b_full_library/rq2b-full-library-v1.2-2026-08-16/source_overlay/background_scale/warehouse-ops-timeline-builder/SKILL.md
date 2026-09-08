---
name: warehouse-ops-timeline-builder
description: Builds a timeline for warehouse inventory operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Warehouse Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from stock count, pick list, receiving note, inventory adjustment.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: stock count, pick list, receiving note, inventory adjustment.

## Dependencies and resources

- inventory export
- SKU catalog
- location map
- receiving record
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
