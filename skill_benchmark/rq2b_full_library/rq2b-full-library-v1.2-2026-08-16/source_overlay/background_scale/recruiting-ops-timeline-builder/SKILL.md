---
name: recruiting-ops-timeline-builder
description: Builds a timeline for recruiting pipeline operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Recruiting Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from resume, interview notes, job criteria, candidate comparison table.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: resume, interview notes, job criteria, candidate comparison table.

## Dependencies and resources

- resume file
- job criteria
- interview notes
- candidate stage
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
