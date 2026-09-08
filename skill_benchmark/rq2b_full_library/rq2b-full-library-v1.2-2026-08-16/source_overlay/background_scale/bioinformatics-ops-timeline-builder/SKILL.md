---
name: bioinformatics-ops-timeline-builder
description: Builds a timeline for bioinformatics operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Bioinformatics Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from sequence file, variant table, pipeline log, sample metadata.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: sequence file, variant table, pipeline log, sample metadata.

## Dependencies and resources

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
