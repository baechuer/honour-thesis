---
name: support-ops-timeline-builder
description: Builds a timeline for customer support operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Support Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from support tickets, chat transcripts, issue labels, customer history.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
