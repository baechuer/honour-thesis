---
name: engineering-design-ops-timeline-builder
description: Builds a timeline for engineering design operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Engineering Design Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from design specification, calculation note, review comment, requirement list.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: design specification, calculation note, review comment, requirement list.

## Dependencies and resources

- specification
- requirement set
- calculation record
- review standard
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
