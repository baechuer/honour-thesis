---
name: manufacturing-ops-normalizer
description: Normalizes manufacturing operations material into a consistent naming, schema, format, or taxonomy.
---

# Manufacturing Ops Normalizer

## Use when

- The user wants consistency and canonicalization for work order, defect log, production schedule, quality report.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: work order, defect log, production schedule, quality report.

## Dependencies and resources

- work order
- production line
- quality criteria
- operator notes
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
