---
name: incident-ops-normalizer
description: Normalizes incident and reliability operations material into a consistent naming, schema, format, or taxonomy.
---

# Incident Ops Normalizer

## Use when

- The user wants consistency and canonicalization for incident timeline, logs, alerts, postmortem notes.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: incident timeline, logs, alerts, postmortem notes.

## Dependencies and resources

- timeline
- service logs
- alert history
- owner map
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
