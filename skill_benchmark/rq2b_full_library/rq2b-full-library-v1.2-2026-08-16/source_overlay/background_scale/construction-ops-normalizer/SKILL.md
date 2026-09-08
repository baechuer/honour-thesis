---
name: construction-ops-normalizer
description: Normalizes construction project operations material into a consistent naming, schema, format, or taxonomy.
---

# Construction Ops Normalizer

## Use when

- The user wants consistency and canonicalization for site report, change order, drawing register, safety observation.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: site report, change order, drawing register, safety observation.

## Dependencies and resources

- site records
- drawing set
- contract scope
- safety plan
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
