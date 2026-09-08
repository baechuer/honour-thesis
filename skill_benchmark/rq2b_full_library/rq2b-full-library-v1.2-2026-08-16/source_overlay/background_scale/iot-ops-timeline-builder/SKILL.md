---
name: iot-ops-timeline-builder
description: Builds a timeline for IoT operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Iot Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from device telemetry, firmware note, sensor log, provisioning record.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: device telemetry, firmware note, sensor log, provisioning record.

## Dependencies and resources

- device registry
- telemetry data
- firmware version
- network context
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
