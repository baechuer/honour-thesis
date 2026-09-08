---
name: personal-ops-timeline-builder
description: Builds a timeline for personal productivity operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Personal Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from task list, personal note, habit log, calendar item.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: task list, personal note, habit log, calendar item.

## Dependencies and resources

- task list
- calendar
- priority context
- personal constraints
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
