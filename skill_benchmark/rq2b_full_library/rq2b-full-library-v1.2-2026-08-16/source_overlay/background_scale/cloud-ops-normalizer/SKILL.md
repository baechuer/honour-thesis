---
name: cloud-ops-normalizer
description: Normalizes cloud infrastructure operations material into a consistent naming, schema, format, or taxonomy.
---

# Cloud Ops Normalizer

## Use when

- The user wants consistency and canonicalization for cloud config, resource inventory, deployment note, cost report.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: cloud config, resource inventory, deployment note, cost report.

## Dependencies and resources

- cloud account
- resource inventory
- deployment config
- cost data
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
