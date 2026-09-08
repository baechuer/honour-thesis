---
name: environmental-ops-normalizer
description: Normalizes environmental compliance operations material into a consistent naming, schema, format, or taxonomy.
---

# Environmental Ops Normalizer

## Use when

- The user wants consistency and canonicalization for emissions report, permit condition, monitoring data, incident note.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: emissions report, permit condition, monitoring data, incident note.

## Dependencies and resources

- permit
- monitoring data
- emissions factor
- reporting period
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
