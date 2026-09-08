---
name: manufacturing-ops-timeline-builder
description: Builds a timeline for manufacturing operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Manufacturing Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from work order, defect log, production schedule, quality report.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: work order, defect log, production schedule, quality report.

## Dependencies and resources

- work order
- production line
- quality criteria
- operator notes
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
