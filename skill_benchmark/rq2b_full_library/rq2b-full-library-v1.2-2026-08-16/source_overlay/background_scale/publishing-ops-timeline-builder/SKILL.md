---
name: publishing-ops-timeline-builder
description: Builds a timeline for publishing operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Publishing Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from manuscript, production checklist, author query, proof note.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: manuscript, production checklist, author query, proof note.

## Dependencies and resources

- manuscript
- style sheet
- publication schedule
- rights context
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
