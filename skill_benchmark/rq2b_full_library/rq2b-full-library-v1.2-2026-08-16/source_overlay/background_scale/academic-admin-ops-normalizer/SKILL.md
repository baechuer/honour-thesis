---
name: academic-admin-ops-normalizer
description: Normalizes academic administration operations material into a consistent naming, schema, format, or taxonomy.
---

# Academic Admin Ops Normalizer

## Use when

- The user wants consistency and canonicalization for course policy, enrollment note, assessment record, student request.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: course policy, enrollment note, assessment record, student request.

## Dependencies and resources

- institution policy
- student record
- assessment criteria
- deadline
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
