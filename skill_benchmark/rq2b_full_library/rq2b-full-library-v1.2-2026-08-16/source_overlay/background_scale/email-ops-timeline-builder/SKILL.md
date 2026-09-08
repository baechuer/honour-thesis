---
name: email-ops-timeline-builder
description: Builds a timeline for email and messaging operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Email Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from draft email, message thread, recipient context, tone constraints.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: draft email, message thread, recipient context, tone constraints.

## Dependencies and resources

- message thread
- recipient relationship
- tone target
- requested action
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
