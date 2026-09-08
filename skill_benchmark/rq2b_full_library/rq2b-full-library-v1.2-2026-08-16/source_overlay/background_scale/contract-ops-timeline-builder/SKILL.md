---
name: contract-ops-timeline-builder
description: Builds a timeline for contract operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Contract Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from contract text, amendment notes, renewal terms, obligation logs.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: contract text, amendment notes, renewal terms, obligation logs.

## Dependencies and resources

- contract document
- party names
- clause references
- effective dates
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
