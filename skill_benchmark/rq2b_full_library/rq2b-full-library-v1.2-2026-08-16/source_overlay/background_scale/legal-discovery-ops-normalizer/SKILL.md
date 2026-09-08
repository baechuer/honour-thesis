---
name: legal-discovery-ops-normalizer
description: Normalizes legal discovery operations material into a consistent naming, schema, format, or taxonomy.
---

# Legal Discovery Ops Normalizer

## Use when

- The user wants consistency and canonicalization for document production, privilege log, deposition note, evidence request.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
