---
name: ml-ops-normalizer
description: Normalizes machine learning operations material into a consistent naming, schema, format, or taxonomy.
---

# Ml Ops Normalizer

## Use when

- The user wants consistency and canonicalization for model card, training log, evaluation table, dataset note.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: model card, training log, evaluation table, dataset note.

## Dependencies and resources

- model artifact
- dataset split
- training config
- evaluation metric
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
