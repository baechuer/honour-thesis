---
name: dataset-ops-normalizer
description: Normalizes dataset and analytics preparation material into a consistent naming, schema, format, or taxonomy.
---

# Dataset Ops Normalizer

## Use when

- The user wants consistency and canonicalization for CSV files, data dictionary, metric definitions, quality notes.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
