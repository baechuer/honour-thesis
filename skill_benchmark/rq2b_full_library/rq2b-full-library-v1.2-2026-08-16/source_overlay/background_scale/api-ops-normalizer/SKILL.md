---
name: api-ops-normalizer
description: Normalizes API integration operations material into a consistent naming, schema, format, or taxonomy.
---

# Api Ops Normalizer

## Use when

- The user wants consistency and canonicalization for API spec, endpoint docs, integration error, webhook payload.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: API spec, endpoint docs, integration error, webhook payload.

## Dependencies and resources

- API documentation
- auth method
- payload example
- rate limits
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
