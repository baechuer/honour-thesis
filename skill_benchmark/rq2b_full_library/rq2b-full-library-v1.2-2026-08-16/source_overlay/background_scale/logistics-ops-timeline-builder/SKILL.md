---
name: logistics-ops-timeline-builder
description: Builds a timeline for logistics and shipment operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Logistics Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from shipment manifest, tracking update, carrier note, customs form.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: shipment manifest, tracking update, carrier note, customs form.

## Dependencies and resources

- shipment manifest
- carrier data
- delivery window
- customs details
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
