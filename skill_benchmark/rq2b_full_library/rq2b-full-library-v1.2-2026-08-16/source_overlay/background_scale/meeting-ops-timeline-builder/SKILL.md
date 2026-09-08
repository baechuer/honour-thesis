---
name: meeting-ops-timeline-builder
description: Builds a timeline for meeting and planning operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Meeting Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from meeting transcript, agenda notes, calendar constraints, action list.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: meeting transcript, agenda notes, calendar constraints, action list.

## Dependencies and resources

- meeting notes
- participant list
- calendar window
- action owners
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
