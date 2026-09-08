---
name: facilities-ops-normalizer
description: Normalizes facilities operations material into a consistent naming, schema, format, or taxonomy.
---

# Facilities Ops Normalizer

## Use when

- The user wants consistency and canonicalization for maintenance request, space plan, safety report, vendor schedule.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: maintenance request, space plan, safety report, vendor schedule.

## Dependencies and resources

- facility map
- maintenance log
- safety policy
- vendor contact
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
