---
name: facilities-ops-timeline-builder
description: Builds a timeline for facilities operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Facilities Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from maintenance request, space plan, safety report, vendor schedule.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: maintenance request, space plan, safety report, vendor schedule.

## Dependencies and resources

- facility map
- maintenance log
- safety policy
- vendor contact
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
