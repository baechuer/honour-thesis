---
name: course-ops-timeline-builder
description: Builds a timeline for course and learning operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Course Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from lecture notes, assignment brief, rubric, study material.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: lecture notes, assignment brief, rubric, study material.

## Dependencies and resources

- course material
- rubric
- deadline
- learning objective
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
