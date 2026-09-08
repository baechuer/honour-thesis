---
name: operations-ops-timeline-builder
description: Builds a timeline for general business operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Operations Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from SOP, process note, operations checklist, team request.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: SOP, process note, operations checklist, team request.

## Dependencies and resources

- process document
- owner map
- deadline
- operational constraint
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
