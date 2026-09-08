---
name: robotics-ops-timeline-builder
description: Builds a timeline for robotics operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Robotics Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from robot log, mission plan, sensor trace, calibration note.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: robot log, mission plan, sensor trace, calibration note.

## Dependencies and resources

- robot platform
- sensor data
- mission objective
- calibration file
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
