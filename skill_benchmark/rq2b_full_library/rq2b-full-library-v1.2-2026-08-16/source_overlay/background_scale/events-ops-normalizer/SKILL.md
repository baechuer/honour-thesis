---
name: events-ops-normalizer
description: Normalizes event planning operations material into a consistent naming, schema, format, or taxonomy.
---

# Events Ops Normalizer

## Use when

- The user wants consistency and canonicalization for event brief, attendee list, venue note, run sheet.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: event brief, attendee list, venue note, run sheet.

## Dependencies and resources

- event brief
- attendee list
- venue constraints
- run sheet
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
