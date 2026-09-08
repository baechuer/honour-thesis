---
name: academic-admin-ops-timeline-builder
description: Builds a timeline for academic administration operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Academic Admin Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from course policy, enrollment note, assessment record, student request.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: course policy, enrollment note, assessment record, student request.

## Dependencies and resources

- institution policy
- student record
- assessment criteria
- deadline
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
