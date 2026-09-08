---
name: platform-ops-normalizer
description: Normalizes platform engineering operations material into a consistent naming, schema, format, or taxonomy.
---

# Platform Ops Normalizer

## Use when

- The user wants consistency and canonicalization for developer platform request, service catalog, template repo, platform metric.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: developer platform request, service catalog, template repo, platform metric.

## Dependencies and resources

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
