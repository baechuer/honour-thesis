---
name: analytics-ops-normalizer
description: Normalizes analytics and experimentation operations material into a consistent naming, schema, format, or taxonomy.
---

# Analytics Ops Normalizer

## Use when

- The user wants consistency and canonicalization for experiment result, metric table, cohort data, analytics request.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
