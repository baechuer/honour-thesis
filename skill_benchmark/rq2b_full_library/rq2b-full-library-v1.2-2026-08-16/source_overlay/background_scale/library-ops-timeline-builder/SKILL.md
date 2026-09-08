---
name: library-ops-timeline-builder
description: Builds a timeline for library and archive operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Library Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from catalog record, archive note, metadata sheet, digitization plan.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: catalog record, archive note, metadata sheet, digitization plan.

## Dependencies and resources

- catalog schema
- collection metadata
- rights note
- preservation policy
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
