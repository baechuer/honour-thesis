---
name: hr-ops-timeline-builder
description: Builds a timeline for human resources operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Hr Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from candidate notes, performance feedback, role description, HR policy.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: candidate notes, performance feedback, role description, HR policy.

## Dependencies and resources

- role profile
- employee context
- policy document
- feedback records
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
