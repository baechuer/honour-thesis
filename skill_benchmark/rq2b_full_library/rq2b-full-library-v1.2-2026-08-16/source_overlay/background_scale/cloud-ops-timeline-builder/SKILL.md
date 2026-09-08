---
name: cloud-ops-timeline-builder
description: Builds a timeline for cloud infrastructure operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Cloud Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from cloud config, resource inventory, deployment note, cost report.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: cloud config, resource inventory, deployment note, cost report.

## Dependencies and resources

- cloud account
- resource inventory
- deployment config
- cost data
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
