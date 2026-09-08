---
name: privacy-ops-timeline-builder
description: Builds a timeline for privacy operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Privacy Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from data inventory, DSR request, privacy notice, processing activity.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: data inventory, DSR request, privacy notice, processing activity.

## Dependencies and resources

- data map
- privacy policy
- jurisdiction note
- request details
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
