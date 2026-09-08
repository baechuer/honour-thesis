---
name: analytics-ops-timeline-builder
description: Builds a timeline for analytics and experimentation operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Analytics Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from experiment result, metric table, cohort data, analytics request.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
