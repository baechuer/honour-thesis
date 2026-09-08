---
name: energy-ops-normalizer
description: Normalizes energy operations material into a consistent naming, schema, format, or taxonomy.
---

# Energy Ops Normalizer

## Use when

- The user wants consistency and canonicalization for usage report, meter reading, sustainability plan, tariff note.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: usage report, meter reading, sustainability plan, tariff note.

## Dependencies and resources

- meter data
- tariff schedule
- facility profile
- sustainability target
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
