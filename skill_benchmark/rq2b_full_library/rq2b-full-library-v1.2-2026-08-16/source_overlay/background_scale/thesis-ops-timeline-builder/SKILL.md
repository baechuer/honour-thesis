---
name: thesis-ops-timeline-builder
description: Builds a timeline for thesis research operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Thesis Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from thesis notes, supervisor feedback, proposal draft, experiment log.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: thesis notes, supervisor feedback, proposal draft, experiment log.

## Dependencies and resources

- research question
- supervisor note
- method plan
- literature notes
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
