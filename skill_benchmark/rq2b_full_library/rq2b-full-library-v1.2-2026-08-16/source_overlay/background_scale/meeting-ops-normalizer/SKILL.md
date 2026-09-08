---
name: meeting-ops-normalizer
description: Normalizes meeting and planning operations material into a consistent naming, schema, format, or taxonomy.
---

# Meeting Ops Normalizer

## Use when

- The user wants consistency and canonicalization for meeting transcript, agenda notes, calendar constraints, action list.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: meeting transcript, agenda notes, calendar constraints, action list.

## Dependencies and resources

- meeting notes
- participant list
- calendar window
- action owners
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
