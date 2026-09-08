---
name: security-ops-timeline-builder
description: Builds a timeline for application security operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Security Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from repository files, threat notes, scan findings, architecture description.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
