---
name: engineering-design-ops-normalizer
description: Normalizes engineering design operations material into a consistent naming, schema, format, or taxonomy.
---

# Engineering Design Ops Normalizer

## Use when

- The user wants consistency and canonicalization for design specification, calculation note, review comment, requirement list.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: design specification, calculation note, review comment, requirement list.

## Dependencies and resources

- specification
- requirement set
- calculation record
- review standard
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
