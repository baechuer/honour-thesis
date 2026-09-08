---
name: construction-ops-timeline-builder
description: Builds a timeline for construction project operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Construction Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from site report, change order, drawing register, safety observation.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: site report, change order, drawing register, safety observation.

## Dependencies and resources

- site records
- drawing set
- contract scope
- safety plan
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
