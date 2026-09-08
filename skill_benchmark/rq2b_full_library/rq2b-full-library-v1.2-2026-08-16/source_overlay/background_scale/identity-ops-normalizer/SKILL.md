---
name: identity-ops-normalizer
description: Normalizes identity and access operations material into a consistent naming, schema, format, or taxonomy.
---

# Identity Ops Normalizer

## Use when

- The user wants consistency and canonicalization for access request, role matrix, audit log, permission review.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: access request, role matrix, audit log, permission review.

## Dependencies and resources

- identity provider
- role matrix
- access logs
- approval policy
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
