---
name: legal-discovery-ops-timeline-builder
description: Builds a timeline for legal discovery operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Legal Discovery Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from document production, privilege log, deposition note, evidence request.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
