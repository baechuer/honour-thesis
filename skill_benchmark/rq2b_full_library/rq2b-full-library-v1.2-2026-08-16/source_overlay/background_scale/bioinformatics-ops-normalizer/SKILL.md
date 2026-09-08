---
name: bioinformatics-ops-normalizer
description: Normalizes bioinformatics operations material into a consistent naming, schema, format, or taxonomy.
---

# Bioinformatics Ops Normalizer

## Use when

- The user wants consistency and canonicalization for sequence file, variant table, pipeline log, sample metadata.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: sequence file, variant table, pipeline log, sample metadata.

## Dependencies and resources

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
