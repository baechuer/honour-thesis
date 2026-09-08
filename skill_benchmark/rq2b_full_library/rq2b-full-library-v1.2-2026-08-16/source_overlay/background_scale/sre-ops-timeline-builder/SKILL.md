---
name: sre-ops-timeline-builder
description: Builds a timeline for site reliability engineering operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Sre Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from SLO report, runbook, alert history, reliability review.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: SLO report, runbook, alert history, reliability review.

## Dependencies and resources

- service map
- SLO definitions
- alert data
- runbook
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
