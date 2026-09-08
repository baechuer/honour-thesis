---
name: insurance-ops-timeline-builder
description: Builds a timeline for insurance claims operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Insurance Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from claim form, policy wording, incident evidence, assessor notes.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: claim form, policy wording, incident evidence, assessor notes.

## Dependencies and resources

- claim file
- policy document
- incident evidence
- coverage criteria
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
