---
name: insurance-ops-normalizer
description: Normalizes insurance claims operations material into a consistent naming, schema, format, or taxonomy.
---

# Insurance Ops Normalizer

## Use when

- The user wants consistency and canonicalization for claim form, policy wording, incident evidence, assessor notes.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: claim form, policy wording, incident evidence, assessor notes.

## Dependencies and resources

- claim file
- policy document
- incident evidence
- coverage criteria
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
