---
name: compliance-ops-timeline-builder
description: Builds a timeline for compliance operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Compliance Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from control checklist, audit finding, policy exception, evidence packet.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: control checklist, audit finding, policy exception, evidence packet.

## Dependencies and resources

- control framework
- evidence files
- audit scope
- owner map
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
