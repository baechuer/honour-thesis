---
name: real-estate-ops-normalizer
description: Normalizes real estate transaction operations material into a consistent naming, schema, format, or taxonomy.
---

# Real Estate Ops Normalizer

## Use when

- The user wants consistency and canonicalization for listing brief, offer terms, inspection note, settlement timeline.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: listing brief, offer terms, inspection note, settlement timeline.

## Dependencies and resources

- listing details
- buyer criteria
- offer terms
- inspection evidence
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
