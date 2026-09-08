---
name: geospatial-ops-timeline-builder
description: Builds a timeline for geospatial analysis operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Geospatial Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from map layer, coordinate table, spatial query, GIS project note.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: map layer, coordinate table, spatial query, GIS project note.

## Dependencies and resources

- spatial data
- coordinate reference system
- map layers
- analysis boundary
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
