---
name: qa-ops-timeline-builder
description: Builds a timeline for quality assurance operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Qa Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from test plan, defect report, acceptance criteria, release evidence.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: test plan, defect report, acceptance criteria, release evidence.

## Dependencies and resources

- test plan
- defect log
- acceptance criteria
- release scope
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
