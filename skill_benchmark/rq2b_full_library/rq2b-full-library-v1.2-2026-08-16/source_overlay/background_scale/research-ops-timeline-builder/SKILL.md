---
name: research-ops-timeline-builder
description: Builds a timeline for research and source review events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Research Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from papers, reports, source notes, citation metadata.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: papers, reports, source notes, citation metadata.

## Dependencies and resources

- source text
- citation metadata
- method section
- evidence snippets
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
