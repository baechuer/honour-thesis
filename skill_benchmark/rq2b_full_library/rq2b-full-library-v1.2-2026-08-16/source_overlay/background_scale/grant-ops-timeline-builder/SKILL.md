---
name: grant-ops-timeline-builder
description: Builds a timeline for grant application operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Grant Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from grant instructions, proposal draft, budget table, eligibility note.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: grant instructions, proposal draft, budget table, eligibility note.

## Dependencies and resources

- grant guidelines
- eligibility criteria
- budget
- submission deadline
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
