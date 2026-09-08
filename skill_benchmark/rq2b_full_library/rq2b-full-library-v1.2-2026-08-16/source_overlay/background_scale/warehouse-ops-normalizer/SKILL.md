---
name: warehouse-ops-normalizer
description: Normalizes warehouse inventory operations material into a consistent naming, schema, format, or taxonomy.
---

# Warehouse Ops Normalizer

## Use when

- The user wants consistency and canonicalization for stock count, pick list, receiving note, inventory adjustment.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: stock count, pick list, receiving note, inventory adjustment.

## Dependencies and resources

- inventory export
- SKU catalog
- location map
- receiving record
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
