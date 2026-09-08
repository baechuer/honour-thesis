---
name: real-estate-ops-timeline-builder
description: Builds a timeline for real estate transaction operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Real Estate Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from listing brief, offer terms, inspection note, settlement timeline.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: listing brief, offer terms, inspection note, settlement timeline.

## Dependencies and resources

- listing details
- buyer criteria
- offer terms
- inspection evidence
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
