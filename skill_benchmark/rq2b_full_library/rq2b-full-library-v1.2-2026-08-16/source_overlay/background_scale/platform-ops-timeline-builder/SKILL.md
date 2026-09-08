---
name: platform-ops-timeline-builder
description: Builds a timeline for platform engineering operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Platform Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from developer platform request, service catalog, template repo, platform metric.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: developer platform request, service catalog, template repo, platform metric.

## Dependencies and resources

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
